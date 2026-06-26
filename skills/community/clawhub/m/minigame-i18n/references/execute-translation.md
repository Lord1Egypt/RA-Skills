# Skill — 执行翻译

## 职责

基于执行计划，翻译项目中的**每一条**文本。对于图片翻译，仅在 MCP 服务可用时通过 MCP 执行。最终输出文本翻译表和图片翻译表。

## 前置条件

- `i18n/scan_report.json` 已生成
- `i18n/glossary.json` 已生成且经用户确认
- `i18n/i18n_plan.md` 已生成且经用户确认
- `i18n-config.json` 存在

## ⚠️ 完整性要求

**scan_report.json 中的每一个 TextEntry 都必须在 text_translations.json 中有对应的翻译条目。** 翻译完成后必须校验条目数量一致。如果因上下文窗口限制无法一次处理完所有条目，必须分批处理并合并结果。

## 执行步骤

### 步骤 1：处理图片翻译（仅 `translateImages` 为 `true` 且 `mcpAvailable` 为 `true` 时执行）

**先读取 `i18n-config.json` 中的 `translateImages` 和 `mcpAvailable` 字段。** 如果 `translateImages` 为 `false` 或 `mcpAvailable` 为 `false`，**跳过步骤 1、步骤 5 和步骤 6**，直接进入步骤 2 开始文本翻译。

**⚠️ 关键变化**：扫描阶段（阶段 1）已经对全部图片执行了 OCR 并筛选出含中文的图片。翻译阶段需要**重新打包上传含中文的图片**（因为翻译需要新的 file_id），然后上传术语表并触发翻译。

**1a. 读取含中文图片列表**：
1. 读取 `i18n/chinese_image_list.txt`（扫描阶段路径 C-5 生成的含中文图片列表）
2. 如果文件不存在或为空，说明没有含中文的图片，跳过图片翻译步骤
3. 读取 `i18n/scan_report.json` 中的 `imageEntries`，确认含中文图片数量

**1b. 重新上传含中文图片**：
1. 执行以下命令，只上传含中文的图片：
   ```
   node scripts/upload-images.js --project <projectRoot> --images-file i18n/chinese_image_list.txt
   ```
2. 从命令输出中捕获 `__FILE_ID__=<id>` 获得新的 `file_id`
3. **如果上传失败**：标记图片翻译为 `failed`，继续执行文本翻译

**1c. 触发 OCR（必需，服务端会复用已有结果）**：
1. 调用 `StartImageOcrMcp`，传入 `{ "file_id": <file_id> }`
2. 调用 `GetImageOcrProgressMcp` 轮询进度（间隔 5 秒，直到 status=2 或 3）
   > 这次 OCR 会复用扫描阶段的识别结果，执行速度很快且不消耗额外资源，但必须执行，否则后续术语表上传和翻译会失败。

**1d. 上传术语表**：
1. 读取 `i18n/glossary.json`，准备术语表数据
2. 调用 `UploadTermDataMcp`：传入 `file_id`、`target_lang`（目标语言列表）和 `text_items`（术语列表），以约束翻译用词

**1e. 触发图片翻译**：
1. 调用 `StartImageTranslateMcp`：传入 `{ "file_id": <file_id> }` 触发图片翻译
2. 图片翻译将在后台运行，**不需要等待完成**，文本翻译可以并行进行
3. 翻译结果在步骤 5 中获取

### 步骤 2：读取执行计划和参考资料

1. 读取 `i18n/i18n_plan.md`，解析出每个步骤的条目 ID 列表
2. 读取 `i18n/scan_report.json`，建立 key → entry 的索引
3. 读取 `i18n/glossary.json`，建立术语查找表
4. **统计总条目数**，作为完成度校验基准

### 步骤 3：按步骤执行文本翻译

按照执行计划中的步骤顺序，逐步翻译。**每个步骤完成后立即继续下一个步骤，不暂停。**

**⚠️ 每批次即时纯度检查**：每翻译完一个批次（一个步骤内的所有条目），立即检查该批次中所有 `target` 是否包含源语言字符（`/[\u4e00-\u9fff]/`）。如果发现中英混杂条目，**立即重新翻译该条目**，不要等到最后的自检环节。这可以避免"偷懒式翻译"——即仅将术语表中的词汇做关键词替换而非整句翻译——在大批量翻译时蔓延。

#### 翻译策略

对每个步骤中的文本条目，根据 `type` 采用不同的翻译策略：

**type: text — 纯文本翻译**

直接翻译文本，确保：
- 术语一致性：查找术语表，使用确认的翻译
- 上下文适配：根据模块类型（UI/战斗/教程等）调整翻译风格
- 长度控制：翻译后文本长度尽量不超过原文的 150%

```json
{
  "key": "5bdd7fcaa1ed9eb1918c22820c690473",
  "source": "开始",
  "target": "Start",
  "filePath": "assets/Scene/game.scene",
  "type": "text",
  "loc": { "start": { "line": 10, "column": 15 }, "end": { "line": 10, "column": 19 } },
  "range": [230, 234],
  "status": "translated"
}
```

**type: template — 模板字符串翻译**

翻译模板字符串中的文本部分，保留 `${...}` 变量占位符：

```json
{
  "key": "tpl_abc123",
  "source": "恭喜 ${name} 获得 ${reward}",
  "target": "Congratulations! ${name} received ${reward}",
  "filePath": "assets/Scripts/RewardManager.ts",
  "type": "template",
  "variables": ["name", "reward"],
  "loc": { "start": { "line": 25, "column": 10 }, "end": { "line": 25, "column": 40 } },
  "range": [580, 610],
  "status": "translated"
}
```

注意事项：
- 变量占位符 `${...}` 必须原样保留
- 翻译时可以调整变量在句子中的位置以符合目标语言的语法
- 但不能修改变量名

**type: concatenation — 拼接字符串翻译（最复杂、最关键）**

拼接字符串需要输出**重构后的完整表达式**，因为不同语言的语序可能不同。

**⚠️ 翻译后的表达式必须是语法正确的 JS 表达式，能直接替换原始代码运行。**

示例 1：简单拼接
```
原文表达式：name + "达到" + lv + "级"
翻译后表达式：name + " reached level " + lv
```

示例 2：复杂拼接
```
原文表达式："你的" + itemName + "已经升到" + level + "级了"
翻译后表达式："Your " + itemName + " has been upgraded to level " + level
```

示例 3：需要调整语序
```
原文表达式：count + "个" + itemName
翻译后表达式：count + " " + itemName
```

示例 4：需要完全重构
```
原文表达式："还需要" + cost + "金币才能购买" + itemName
翻译后表达式："Need " + cost + " Gold to buy " + itemName
```

```json
{
  "key": "concat_abc123",
  "source": "name + \"达到\" + lv + \"级\"",
  "target": "name + \" reached level \" + lv",
  "filePath": "assets/Scripts/GameManager.ts",
  "type": "concatenation",
  "originalExpression": "name + \"达到\" + lv + \"级\"",
  "translatedExpression": "name + \" reached level \" + lv",
  "variables": ["name", "lv"],
  "loc": { "start": { "line": 64, "column": 10 }, "end": { "line": 64, "column": 45 } },
  "range": [1830, 1865],
  "status": "translated"
}
```

拼接字符串翻译原则：
1. **完整输出新表达式**：不能只翻译中文部分，必须输出可以直接替换原始代码的完整表达式
2. **保留变量**：所有变量名必须原样保留
3. **语法正确**：翻译后的表达式必须是合法的 JS 表达式（引号配对正确、+ 运算符正确）
4. **语序调整**：中英文语序不同时，需要重新排列变量和文本的顺序
5. **空格处理**：英文单词之间需要空格，字符串与变量拼接处注意加上空格
6. **引号一致**：翻译后的表达式使用与原始表达式相同的引号类型（单引号或双引号）
7. **自检**：翻译完成后，在脑中"运行"一下表达式，确认结果字符串是自然的目标语言

#### 翻译质量要求

1. **术语一致**：术语表中已确认的翻译必须严格使用，不能自行发挥
2. **自然流畅**：翻译要像目标语言母语者写的，避免直译导致的不自然表达
3. **游戏风格**：根据游戏类型保持一致的翻译风格
4. **简洁有力**：游戏 UI 文本追求简洁，避免冗余
5. **格式保持**：保持原文的标点风格（如感叹号、省略号的使用）
6. **⚠️ 完整翻译，严禁中英混杂**：
   - **每条 target 必须是 100% 目标语言文本**，绝不允许出现源语言（中文）与目标语言混杂的情况
   - ❌ 错误示例：`"剧情或坊市可获得Cultivation Method，装备后会提升Cultivate效率。"` — 只替换了个别词汇，大量中文保留
   - ❌ 错误示例：`"剧情或坊市可获得Spell，装备后可以战斗中Use。"` — 零星翻译个别词，不是完整翻译
   - ✅ 正确示例：`"Obtainable through story or market. Equip to boost cultivation efficiency."` — 整句完整翻译为目标语言
   - **根本原因警示**：当条目数量很大时（如数百条），容易出现"偷懒式翻译"——仅将术语表中的词汇做关键词替换而非整句翻译。这是严格禁止的。每一条都必须作为完整句子/短语重新翻译为目标语言
   - **翻译时必须逐条确认**：target 中不应包含任何 `[\u4e00-\u9fff]` 范围内的中文字符（变量名、HTML 标签属性等非文本内容除外）

### 步骤 4：生成文本翻译表

将所有翻译结果汇总为 `text_translations.json`：

```json
{
  "version": "1.0",
  "sourceLanguage": "zh-CN",
  "targetLanguage": "en",
  "translatedAt": "2026-04-02T17:00:00Z",
  "statistics": {
    "total": 256,
    "translated": 256,
    "skipped": 0,
    "textType": 200,
    "templateType": 12,
    "concatenationType": 8,
    "withGlossaryTerms": 180
  },
  "translations": [
    // ... 翻译条目数组
  ]
}
```

**完整性校验**：生成后立即检查 `statistics.total` == `scan_report.json` 中 `summary.totalTextEntries`。如果不等，找出遗漏条目并补充翻译后重新生成。

每个翻译条目需包含完整的位置信息（`filePath`、`loc`、`range`），这些信息直接复制自 scan_report，供后续替换脚本使用。

### 步骤 5：处理图片翻译结果（仅步骤 1 启动了图片翻译时执行）

如果步骤 1 未执行（`translateImages=false` 或 `mcpAvailable=false` 或无含中文图片），跳过此步骤。

**获取翻译结果**：
1. 调用 `GetImageTranslateProgressMcp`，传入步骤 1b 获得的 `file_id`，查询图片翻译进度（间隔 10 秒，直到 status=2 或 3）
2. 如果 status=1（运行中），继续轮询
3. 翻译完成后（status=2），调用 `GetImageTranslateResultMcp` 获取翻译后图片的下载链接
4. 下载翻译后的图片到 `i18n/assets/{targetLanguage}/` 目录

### 步骤 6：生成图片翻译表（仅 `translateImages` 为 `true` 时执行）

如果 `translateImages` 为 `false`，**跳过此步骤，不生成 `image_translations.json`**。

基于 `scan_report.json` 中的 `imageEntries`（只包含含中文的图片）生成 `image_translations.json`：

**如果步骤 5 获取到了翻译结果**：填入实际翻译文件路径，`status` 设为 `"completed"`
**如果 `mcpAvailable` 为 `false` 或翻译失败**：所有条目 `status` 设为 `"pending_manual"`

```json
{
  "version": "1.0",
  "sourceLanguage": "zh-CN",
  "targetLanguage": "en",
  "translations": [
    {
      "key": "img_abc123",
      "sourceFile": "assets/images/btn_start.png",
      "targetFile": "i18n/assets/en/assets/images/btn_start.png",
      "ocrText": "开始游戏",
      "translatedText": "Start Game",
      "status": "completed",
      "method": "mcp_image_translation"
    }
  ]
}
```

### 步骤 6b：自检

**⚠️ 翻译完成后、输出摘要前，必须执行以下检查。任何一项不通过都必须修正。**

**验证上游产物（阶段 1 + 阶段 2）：**

| 检查项 | 验证方法 | 不通过时 |
|--------|----------|----------|
| 扫描报告存在 | `i18n/scan_report.json` 存在且可解析 | 回到阶段 1 |
| 术语表存在 | `i18n/glossary.json` 存在且可解析 | 回到阶段 2 |
| 执行计划存在 | `i18n/i18n_plan.md` 存在 | 回到阶段 2 |

**验证本阶段产物：**

| 检查项 | 验证方法 | 不通过时 |
|--------|----------|----------|
| 文本翻译表存在 | `i18n/text_translations.json` 存在且可解析 | 回到步骤 4 重新生成 |
| 翻译不为空 | `translations` 数组长度 > 0 | 回到步骤 3 |
| 翻译条目数一致 | `statistics.total` == `scan_report.json` 的 `summary.totalTextEntries` | 找出遗漏条目并补充翻译 |
| 每条翻译字段完整 | 每个 entry 都有 `key`、`source`、`target`、`filePath`、`type`、`status` | 补全缺失字段 |
| 拼接字符串有表达式 | `type="concatenation"` 的 entry 必须有 `translatedExpression` 且非空 | 补充翻译表达式 |
| ⚠️ **目标语言纯度** | 见下方详细检查流程 | 对污染条目重新翻译 |
| 图片翻译表（如需） | `translateImages=true` 时，`i18n/image_translations.json` 存在 | 回到步骤 6 生成 |

#### ⚠️ 目标语言纯度检查（Double Check，必须执行）

**这是防止"部分翻译/中英混杂"的最后一道防线，不允许跳过。**

**检查流程：**

1. **遍历** `text_translations.json` 中**每一条** translation entry
2. **对每条 entry 的 `target` 字段**，使用正则 `/[\u4e00-\u9fff]/` 检测是否包含中文字符
3. **排除合法的中文保留情况**（以下情况不算污染）：
   - `status` 为 `"kept"` 的条目（用户明确标记为保留原文）
   - `target` 中的中文仅出现在 HTML/富文本标签的属性值中（如 `<color=#ff0000>` 内不会有中文，但 `<font name="微软雅黑">` 中的字体名可保留）
   - 品牌名、角色专有名词等在术语表中明确标注为"保留中文"的术语
   - `type` 为 `"concatenation"` 时，`translatedExpression` 中的变量名本身含中文的情况（极少见）
4. **对于检测到包含中文的 target（排除上述合法情况后）**，标记为 **"翻译污染"条目**
5. **统计污染条目数量**，如果 > 0：
   - 输出污染条目清单（key、source、target、filePath）
   - **逐条重新翻译**这些污染条目，确保 target 为 100% 目标语言
   - 更新 `text_translations.json`
   - **重新执行纯度检查**，直到污染条目数为 0
   - 最大重试 3 次，如果 3 次后仍有污染条目，输出错误清单

**检查结果记入 `statistics`**：
```json
{
  "statistics": {
    "total": 256,
    "translated": 256,
    "skipped": 0,
    "targetLanguagePurityCheck": {
      "passed": true,
      "totalChecked": 256,
      "contaminated": 0,
      "reTranslated": 0,
      "excluded": 3
    }
  }
}
```

全部通过后进入步骤 7。

### 步骤 7：输出翻译摘要并继续

输出简短摘要。**本阶段到此结束，由 SKILL.md 控制后续流程。**

```
📝 翻译完成！文本 N/N 条，图片 M 张（MCP/待手动）。
```
（如果 `translateImages` 为 `false`，省略图片部分：`📝 翻译完成！文本 N/N 条。`）

## 关键注意事项

1. **拼接字符串是难点**：这是最容易出错的部分。翻译后的表达式必须是语法正确的 JS 代码，且能在替换后正常运行。

2. **批量翻译 vs 逐条翻译**：为了保证质量和术语一致性，建议按模块批量翻译，一次处理同一模块的所有条目。

3. **上下文参考**：翻译时尽量读取原始代码文件中的上下文，理解文本的使用场景，避免脱离上下文的翻译。

4. **数字和符号**：
   - 阿拉伯数字保留
   - 中文标点转换为英文标点（如 "，" → ","、"。" → "."）
   - 特殊符号保留（如 ★、♦ 等）

5. **HTML/富文本标签**：如果文本中包含 HTML 标签（如 `<color=#ff0000>`），标签需要原样保留，只翻译纯文本部分。

6. **不遗漏**：每一条 scan_report 中的文本都必须翻译，不允许因为"看起来不需要翻译"或"太短"而跳过。如果确实不需要翻译（如品牌名），target 设为与 source 相同，status 设为 `kept`。

# Skill — 应用本地化资源

## 职责

基于翻译结果，使用脚本执行文本替换、图片替换和语言包生成，将本地化资源应用到项目中。

## 前置条件

- `i18n-config.json` 已存在，包含 `translateImages`、`mcpAvailable`、目标语言、本地化策略等
- `i18n/text_translations.json` 已生成（阶段 3 产物）
- `i18n/image_translations.json` 已生成（仅 `translateImages` 为 `true` 时）
- `i18n/scan_report.json` 已生成（阶段 1 产物）

**开始执行前，必须先读取 `i18n-config.json`**，获取以下字段：
- `targetLanguages`：目标语言列表
- `localizationStrategy`：本地化策略（`"replace"` / `"langpack"` / `"both"`）
- `translateImages`：是否翻译图片
- `engine`：游戏引擎类型

## ⚠️ 核心原则

1. **必须使用 `scripts/` 目录下的脚本执行**，不允许 AI 自行编写替换逻辑或直接修改文件
2. **先 dry-run 后实际执行**，每个脚本都必须先预览确认再正式运行
3. **替换后必须验证**，语法检查不通过则回滚

## 执行步骤

根据 `i18n-config.json` 中的 `localizationStrategy`，选择对应的执行路径：

---

### 步骤 1：确定执行计划

读取 `localizationStrategy` 的值，确定需要执行哪些脚本：

| `localizationStrategy` | 执行的脚本 | 说明 |
|-------------------------|------------|------|
| `"replace"` | `replace-text.js --mode direct` + `replace-image.js`（如有图片） | 直接替换代码中的文本和图片资源 |
| `"langpack"` | `generate-langpack.js` → `replace-text.js --mode langpack` | 生成语言包 + 自动将代码中的中文替换为 i18n 调用 + 自动部署语言包到项目目录 + 自动注入初始化代码 |
| `"both"` | `generate-langpack.js` → `replace-text.js --mode langpack` + `replace-image.js`（如有图片） | 生成语言包 + 替换代码为 i18n 调用 + 替换图片 |

对每种目标语言，依次执行对应的脚本。

---

### 步骤 2：生成语言包并替换代码（策略为 `"langpack"` 或 `"both"` 时执行）

对每种目标语言执行：

**2a. 确定引擎对应的 engine 参数值**：

| 引擎 / 环境 | --engine 参数值 | 生成的语言包格式 |
|-------------|----------------|----------------|
| Cocos Creator（<3.6，使用 i18n 插件） | `cocos-creator` | TS 嵌套对象 + `window.languages` 挂载 |
| Cocos Creator（≥3.6，使用 L10N） | `cocos-l10n` | PO 文件 + CSV 翻译表 |
| LayaAir | `laya` | JSON key-value + I18nManager.ts |
| Egret 白鹭 | `egret` | TS 字典 + EXML 映射 + I18nHelper.ts |
| Unity | `unity` | JSON StringTable + CSV + I18nManager.cs |
| 原生微信小游戏 | `native` | JSON key-value + i18n.js 运行时模块 |

**2b. 执行语言包生成**：
```bash
node scripts/generate-langpack.js --project <projectRoot> --engine <engine> --target-lang <lang>
```

脚本 v3.0 会自动完成以下操作：
1. 生成引擎可用的语言包文件到 `i18n/langpack/<engine>/`
2. 生成 `key_mapping.json`（source → i18n key 映射表，供后续代码替换使用）
3. **自动将语言包文件复制到引擎项目的正确目录**（如 Cocos → `assets/resources/i18n/`，Laya → `bin/i18n/` 等）
4. **自动在项目入口文件中注入 i18n 初始化代码**（import 语句 + init 调用）

**2c. 检查输出**：
- 确认生成的语言包文件路径和内容合理
- 确认 `key_mapping.json` 条目数量与 `text_translations.json` 一致
- 确认语言包已被复制到引擎项目目录
- 确认入口文件中已注入 i18n 初始化代码（如果自动注入失败，需手动添加）
- **Cocos Creator i18n 插件**：检查 `assets/resources/i18n/` 下的 `.ts` 文件是否正确
- **Cocos L10N**：检查 `localization-editor/translate-data/` 下的 PO/CSV 文件
- **Unity**：检查 `Assets/Resources/I18n/` 下的 JSON 和 `Assets/Scripts/I18n/` 下的 C#

**2d. 执行代码替换（将中文替换为 i18n 调用）**：

这是关键步骤！语言包生成后，必须将代码中的硬编码中文替换为 `i18n.t("key")` 调用，让语言包真正生效。

**2d-i. dry-run 预览**：
```bash
node scripts/replace-text.js --project <projectRoot> --target-lang <lang> --mode langpack --engine <engine> --dry-run
```

**2d-ii. 检查 dry-run 输出**：
- 确认替换数量合理
- 确认中文文本确实被替换为 `i18n.t("key")` / `l10n.t("key")` / `I18nManager.t("key")` 等引擎对应的 i18n 调用
- ⚠️ JSON/CSV 等数据文件中的条目会被标记为失败（数据文件无法使用函数调用），这是正常的

**2d-iii. 实际执行**：
```bash
node scripts/replace-text.js --project <projectRoot> --target-lang <lang> --mode langpack --engine <engine> --backup
```

**2d-iv. 检查执行结果**：
- 读取 `i18n/replace_report.json`，检查替换成功数和失败数
- 对于 JSON/Scene/Prefab 等数据文件中的失败条目，这些需要通过其他方式处理（如 Cocos Creator 的 L10N 面板绑定）
- 对于代码文件中的失败条目，**AI 必须逐一手动补救**（参见步骤 3f）

**2e. 记录结果**：记录语言包生成路径、代码替换数、入口文件注入状态。

> ⚠️ 策略为 `"langpack"` 时，步骤 2 完成后直接跳到步骤 4（图片替换）或步骤 5（生成报告），**不需要**再执行步骤 3（步骤 3 是 direct 模式专用）。

---

### 步骤 3：执行直接文本替换（**仅**策略为 `"replace"` 时执行）

> ⚠️ 策略为 `"langpack"` 时不执行此步骤（代码替换已在步骤 2d 中通过 `--mode langpack` 完成）。
> 策略为 `"both"` 时，代码文件的替换已在步骤 2d 完成，此步骤仅用于补充替换数据文件（JSON/Scene/Prefab 等无法使用 i18n 调用的文件），使用 `--mode direct`。

对每种目标语言执行：

**3a. dry-run 预览**：
```bash
node scripts/replace-text.js --project <projectRoot> --target-lang <lang> --mode direct --dry-run
```

**3b. 检查 dry-run 输出**：
- 确认替换数量合理（应接近 `text_translations.json` 的总条目数）
- 确认没有异常的失败数量
- 如果失败数量过多（> 总数的 20%），**暂停**，分析原因后再继续

**3c. 实际执行**：
```bash
node scripts/replace-text.js --project <projectRoot> --target-lang <lang> --mode direct --backup
```

**3d. 检查执行结果**：
- 脚本 v3.4 会在**每条替换后即时校验语法**，校验失败的单条替换会被自动回退（不影响同文件其他替换）
- 脚本会**优先替换字符串字面量中的文本**，自动排除注释中的同名文本匹配，避免"替换了注释但漏掉代码"的问题
- 所有替换完成后，脚本还会执行**最终整体语法校验**，校验失败的文件会整体回滚
- 脚本会在 `i18n/replace_report.json` 中生成详细的替换报告，包含 `finalVerification` 字段
- 读取替换报告，检查：
  - `totalReplaced`：成功替换数量
  - `totalFailed`：失败数量（包含即时校验回退的条目）
  - `totalRolledBack`：回滚的文件数量
  - `finalVerification`：每个被修改文件的最终语法校验结果
- 如果有回滚的文件或 `finalVerification` 中有 `syntaxValid: false` 的文件，记录下来供后续质量验证阶段处理

**3e. 如果脚本退出码非 0**（有失败或回滚）：
- 读取 `i18n/replace_report.json` 中的失败详情
- 特别关注 `status: "reverted"` 的条目（逐条校验失败被回退）
- 记录失败原因，不阻塞流程，继续执行步骤 3f

**3f. AI 逐一手动补救替换失败的条目**：

**⚠️ 替换脚本执行后，必须检查替换报告中所有失败的条目并逐一手动完成替换，不允许跳过。**

1. 从 `i18n/replace_report.json` 中筛选所有 `status` 不为 `replaced` 的条目（`failed`、`reverted`、`error`）
2. 如果有失败条目，对每一条：
   - 读取对应的源码文件，在文件中定位该条目的中文文本
   - 根据条目的 `type` 执行替换：
     - **`text`**：将 `source` 替换为 `target`（注意保留引号类型）
     - **`template`**：将整个模板字符串 `` `source` `` 替换为 `` `target` ``，保留 `${...}` 变量表达式不变
     - **`concatenation`**：将 `originalExpression` 替换为 `translatedExpression`
   - 使用 `replace_in_file` 工具执行单条替换
   - 替换后对该文件运行语法检查（JS: `node --check`，JSON: `JSON.parse`）
   - 如果语法检查失败，撤销该条替换，记录为手动补救失败
3. 汇总手动补救结果（成功数、失败数），记入替换报告

---

### 步骤 4：执行图片替换（仅 `translateImages` 为 `true` 且有已完成的图片翻译时执行）

检查 `i18n/image_translations.json` 中是否有 `status: "completed"` 的条目。如果没有，跳过此步骤。

**⚠️ 重要**：图片替换脚本 v2 支持**智能搜索 MCP 翻译后的图片**。翻译后的图片应该已经通过 MCP 的 `GetImageTranslateResultMcp` 下载到 `i18n/assets/{lang}/` 或 `i18n/translated_output/{lang}/` 目录。脚本会在以下路径中自动查找：
1. `image_translations.json` 中指定的 `targetFile` 路径
2. `i18n/assets/{lang}/{sourceFile}` 标准路径
3. `i18n/translated_output/{lang}/` 目录下递归查找同名文件
4. `i18n/assets/{lang}/` 目录下递归查找（匹配路径最相似的文件）

对每种目标语言执行：

**4a. dry-run 预览**：
```bash
node scripts/replace-image.js --project <projectRoot> --target-lang <lang> --mode replace --dry-run
```

**4b. 检查 dry-run 输出**：
- 确认可替换的图片数量合理
- 确认每张图片都找到了翻译后的来源文件（日志会显示来源路径）
- 如果有找不到翻译图片的情况，检查 `i18n/assets/{lang}/` 目录下文件是否正确下载

**4c. 实际执行**：
```bash
node scripts/replace-image.js --project <projectRoot> --target-lang <lang> --mode replace --backup
```

**4d. 检查执行结果**：
- 确认成功替换的图片数量
- 记录失败的图片（翻译后图片缺失等）
- 脚本会生成 `i18n/image_replace_report.json` 替换报告

---

### 步骤 5：生成替换总报告

汇总步骤 2-4 的结果，更新 `i18n/replace_report.json`（如果脚本已生成，则合并；否则创建）：

```json
{
  "timestamp": "2026-04-09T17:00:00Z",
  "targetLanguages": ["en", "ko"],
  "localizationStrategy": "langpack",
  "results": {
    "langpack": {
      "status": "completed",
      "engine": "cocos-creator",
      "files": ["i18n/langpack/cocos-creator/en.ts", "i18n/langpack/cocos-creator/zhCN.ts"],
      "keyMappingFile": "i18n/langpack/key_mapping.json",
      "deployedTo": ["assets/resources/i18n/en.ts", "assets/resources/i18n/zhCN.ts"],
      "i18nInitInjected": true,
      "i18nInitFile": "assets/scripts/Main.ts"
    },
    "codeReplace": {
      "status": "completed",
      "mode": "langpack",
      "totalReplaced": 220,
      "totalFailed": 10,
      "totalRolledBack": 0,
      "failedDetail": "10 条位于 JSON/Scene 数据文件中，不支持 i18n 调用（正常）",
      "backupDir": "i18n/backups/2026-04-09T17-00-00-000Z"
    },
    "textReplace": {
      "status": "skipped",
      "reason": "langpack 策略不需要直接文本替换"
    },
    "imageReplace": {
      "status": "completed",
      "totalReplaced": 12,
      "totalFailed": 2
    }
  }
}
```

---

### 步骤 6：自检

**执行完所有脚本后，必须验证以下检查点：**

| 检查项 | 验证方法 | 不通过时 |
|--------|----------|----------|
| 替换报告存在 | `i18n/replace_report.json` 文件存在 | 回到对应步骤重新执行 |
| 文本替换已执行 | 策略为 `replace` 时，`textReplace.status` 不为空 | 回到步骤 3 |
| 语言包已生成且代码已替换 | 策略为 `langpack`/`both` 时，`langpack.status` 和 `codeReplace.status` 不为空 | 回到步骤 2 |
| i18n 初始化已注入 | 策略为 `langpack`/`both` 时，`langpack.i18nInitInjected` 为 true 或手动确认已添加 | 手动在入口文件添加 |
| 语言包已部署到项目 | 策略为 `langpack`/`both` 时，`langpack.deployedTo` 非空 | 手动复制语言包文件 |
| 图片替换已执行 | `translateImages=true` 且有完成的图片翻译时，`imageReplace.status` 不为空 | 回到步骤 4 |
| 备份已创建 | 策略含替换时，`backupDir` 目录存在 | 记录警告 |

全部通过后，输出摘要。**本阶段到此结束，由 SKILL.md 控制后续流程。**

摘要格式：
```
🔧 资源替换完成！
  - 文本替换：N 处成功 / M 处失败
  - 语言包：已生成 X 个文件
  - 图片替换：Y 张成功 / Z 张失败
  - 备份目录：i18n/backups/xxx
```

## 关键注意事项

1. **绝不允许 AI 自行编辑源码文件来执行替换** — 所有替换操作必须通过脚本完成，AI 只负责调用脚本并检查结果
2. **每次脚本调用都要检查退出码和输出** — 不要盲目认为执行成功
3. **回滚不阻塞流程** — 脚本的回滚机制是安全网，有回滚的文件在质量验证阶段会被重点关注
4. **多语言逐个处理** — 如果有多种目标语言，对每种语言分别执行一轮完整的脚本调用
5. **langpack 策略是完整闭环** — 不仅生成语言包，还会自动完成：语言包部署到引擎目录 → i18n 初始化代码注入 → 源码中的中文替换为 i18n 调用。整个流程无需用户手动接入
6. **langpack 模式下数据文件（JSON/Scene/CSV 等）中的中文无法替换为 i18n 调用** — 这是正常的，数据文件中的文本需要通过引擎的本地化功能（如 Cocos L10N 面板绑定）处理，不影响代码文件的替换
7. **二次复核是可选步骤** — 源码替换完成后，可以在用户重新编译项目后使用 `scripts/verify-build-strings.js` 对编译产物进行扫描，检查是否有遗漏的中文。此步骤在阶段 7 中执行，不在本阶段处理

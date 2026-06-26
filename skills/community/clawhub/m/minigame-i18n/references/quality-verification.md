# Skill — 本地化质量验证

## 职责

验证本地化之后的项目质量。检查代码语法正确性、翻译术语一致性、文本长度变化，以及源语言残留情况。生成验证报告。

## 前置条件

- 资源替换已完成（阶段 4 已执行）
- `i18n/text_translations.json` 存在
- `i18n/image_translations.json` 存在（仅 `translateImages` 为 `true` 时）
- `i18n/glossary.json` 存在
- `i18n/scan_report.json` 存在
- `i18n/replace_report.json` 存在

## ⚠️ 执行原则

1. **自动执行**：验证阶段不需要用户确认，自动完成
2. **发现问题自动修正**：可修正的问题自动修正后重新验证
3. **最大循环 3 次**：修正后重新验证，最多循环 3 次
4. **不可修正的问题**：列出问题清单交给用户

## 执行步骤

### 步骤 0：检查替换报告

先读取 `i18n/replace_report.json`，检查是否有被回滚的文件：
- 如果有回滚文件，记录这些文件作为高优先级问题
- 回滚的文件意味着替换导致了语法错误，需要修正翻译表达式

### 步骤 1：代码语法检查

对所有被修改过的代码文件进行语法检查，确保替换后代码仍然合法。

#### 1a. JavaScript 文件

使用 `node --check <file>` 检查 JS 文件语法：

```bash
node --check assets/Scripts/GameManager.js
```

#### 1b. JSON/Scene/Prefab 文件

使用 JSON.parse 验证格式：

```bash
node -e "JSON.parse(require('fs').readFileSync('<file>', 'utf8'))"
```

#### 1c. TypeScript 文件

如果有 `tsc` 可用：`npx tsc --noEmit`
否则做基础引号/括号配对检查

#### 1d. 记录结果

```json
{
  "syntaxCheck": {
    "status": "pass | fail",
    "total": 30,
    "passed": 28,
    "failed": 2,
    "details": [
      {
        "filePath": "assets/Scripts/GameManager.js",
        "status": "fail",
        "error": "SyntaxError: Unexpected token at line 64",
        "relatedTranslationKeys": ["concat_abc123"]
      }
    ]
  }
}
```

### 步骤 2：术语一致性检查

验证翻译结果中术语的使用是否与术语表一致。

#### 检查方法

1. 读取 `i18n/glossary.json` 中所有已确认（`approved: true`）的术语
2. 遍历 `i18n/text_translations.json` 中的所有翻译
3. 对于每条翻译，检查：
   - 如果原文包含术语表中的源词，翻译结果中是否使用了对应的目标词
   - 同一个源词在不同翻译条目中是否使用了一致的目标词

#### 记录结果

```json
{
  "glossaryConsistency": {
    "status": "pass | fail",
    "total": 50,
    "consistent": 48,
    "inconsistent": 2,
    "details": [...]
  }
}
```

### 步骤 3：文本长度变化检查

检查翻译后文本相对原文的长度变化。对于游戏 UI 来说，文本长度增长过大可能导致显示溢出。

#### 检查规则

1. 遍历 `text_translations.json` 中所有翻译条目
2. 计算 `target.length / source.length` 增长率
3. **阈值**：如果增长超过 **50%**（即翻译后长度 > 原文长度 * 1.5），记录为警告
4. 对于特别短的原文（长度 <= 2 个字符），使用绝对长度差判断：如果目标长度 > 原文长度 + 10，则警告

#### 特殊处理

- 拼接字符串：比较完整翻译表达式中**纯文本部分**的长度变化（去掉变量名后比较）
- 模板字符串：同上，去掉 `${...}` 变量部分后比较

`severity` 分级：
- `low`：增长 50%-100%
- `medium`：增长 100%-200%
- `high`：增长超过 200%

### 步骤 4：源语言残留检查

检查替换后的代码文件中是否仍然存在源语言（中文）文本残留。

#### 检查方法

1. 遍历所有被修改过的代码文件
2. 使用正则 `/[\u4e00-\u9fff]/g` 扫描中文字符
3. 对找到的中文文本，判断是否在 scan_report 中但未被翻译
4. 排除以下合法的中文残留：
   - 注释中的中文（`//`、`/* */`）
   - `console.log()` 等调试语句中的中文
   - 被用户标记为"不翻译"的条目
   - 术语表中标记为保留原文的条目

### 步骤 5：图片翻译验证（仅 `translateImages` 为 `true` 时执行）

如果 `translateImages` 为 `false`，**跳过此步骤**。

检查图片翻译表中的状态：

1. 所有条目都已 `completed` → ✅
2. 存在 `failed` 条目 → ⚠️ 列出失败原因
3. 存在 `pending_manual` 条目 → ⚠️ 提醒用户手动处理（这是无 MCP 时的正常状态）
4. 检查翻译后的图片文件是否确实存在于目标目录

### 步骤 6：生成验证报告

将所有检查结果汇总为 `i18n/verify_report.json`：

```json
{
  "version": "1.0",
  "verifyTime": "2026-04-02T17:30:00Z",
  "overall": "pass | warning | fail",
  "summary": {
    "totalChecks": 5,
    "passed": 3,
    "warnings": 1,
    "failed": 1
  },
  "checks": {
    "syntaxCheck": { ... },
    "glossaryConsistency": { ... },
    "textLengthWarnings": { ... },
    "sourceLanguageResidual": { ... },
    "imageTranslation": { ... }        // 仅 translateImages 为 true 时包含
  },
  "actionItems": [...]
}
```

#### overall 判定规则

- **pass**：所有检查通过（长度警告和图片 `pending_manual` 不影响判定；`translateImages` 为 `false` 时忽略图片相关检查）
- **warning**：存在长度警告或图片翻译部分失败（仅 `translateImages` 为 `true` 时），但无语法错误和术语不一致
- **fail**：存在语法错误或术语不一致

### 步骤 7：自动修正（如需要）

当验证失败时，**自动**尝试修正以下问题（不需要询问用户）：

1. **语法错误（拼接字符串替换导致）**：
   - 从备份恢复该文件
   - 重新检查对应的翻译表达式，修正语法问题
   - 更新 `text_translations.json`
   - 仅对该文件重新执行替换

2. **术语不一致**：
   - 用术语表中正确的翻译替换不一致的翻译
   - 更新 `text_translations.json`
   - 对相关文件重新执行替换

3. **图片文件缺失（仅 `translateImages` 为 `true` 且有 MCP 时）**：
   - 重新从 MCP 下载

修正后重新执行步骤 1-6。**最大循环 3 次。**

如果 3 次修正后仍有问题，生成最终报告交给用户处理。

### 步骤 7b：自检（输出最终摘要前的完整性验证）

**⚠️ 输出最终摘要前，必须执行以下检查。**

**验证上游产物（阶段 3 + 阶段 4）：**

| 检查项 | 验证方法 | 不通过时 |
|--------|----------|----------|
| 翻译表存在 | `i18n/text_translations.json` 存在 | 回到阶段 3 |
| 替换报告存在 | `i18n/replace_report.json` 存在 | 回到阶段 4 |
| 备份已创建 | `i18n/backups/` 目录下有内容（策略含替换时） | 记录警告 |

**验证本阶段产物：**

| 检查项 | 验证方法 | 不通过时 |
|--------|----------|----------|
| 验证报告存在 | `i18n/verify_report.json` 存在且可解析 | 回到步骤 6 生成 |
| 语法检查已执行 | `checks.syntaxCheck` 字段存在 | 回到步骤 1 |
| 术语一致性已检查 | `checks.glossaryConsistency` 字段存在 | 回到步骤 2 |
| 源语言残留已检查 | `checks.sourceLanguageResidual` 字段存在 | 回到步骤 4 |
| overall 判定存在 | `overall` 字段为 `"pass"` / `"warning"` / `"fail"` 之一 | 重新生成验证报告 |

全部通过后进入步骤 8。

### 步骤 8：输出最终摘要

```
✅ 本地化完成！

翻译统计：
  - 文本：256 条（纯文本 200 / 模板 12 / 拼接 8）
  - 图片：15 张（已翻译 13 / 待手动 2）   ← 仅 translateImages 为 true 时显示

验证结果：
  - 代码语法检查：✅ 30/30 通过
  - 术语一致性：✅ 50/50 一致
  - 源语言残留：0 处
  - 文本长度警告：3 条（low 2 / medium 1）

产物目录：i18n/
备份目录：i18n/backups/

⚠️ 以下图片需要手动处理（无 MCP 图片翻译服务）：  ← 仅 translateImages=true 且 mcpAvailable=false 时显示
  - assets/images/start_btn.png
  - assets/images/banner.png
```

**在最终摘要之后，必须追加二次复核提示**（由 SKILL.md 阶段 7 控制）：

```
💡 建议进行编译产物二次复核
   源码替换已完成，但编译后的产物中可能仍有遗漏。
   请重新编译项目后告诉我编译输出目录，我将使用 verify-build-strings.js 进行扫描复核。
   如不需要，可跳过此步骤。
```

# 发布说明 / Publishing Info

> 本文件为发布到 SkillHub（https://skillhub.cn）所需的完整信息，已按需提供**中文 / English** 双语版本。
> This file contains the complete metadata required to publish to SkillHub (https://skillhub.cn), provided bilingually (中文 / English) where applicable.

---

## 1. 基础信息 / Basic Metadata

| 字段 Field | 值 Value | 说明 Note |
|---|---|---|
| `slug` | `iso-multistandard-audit-assistant` | **全网唯一**标识；若发布时提示冲突，请改成专属名（如加 handle 前缀 `yourhandle-iso-multistandard-audit-assistant`）。 / Globally unique id. If a collision occurs, rename to a unique one (e.g. prefix with your handle). |
| `name` | `iso-multistandard-audit-assistant` | 技能内部名 / Internal skill name. |
| `displayName` | `ISO 多标准体系评估陪跑助手 (ISO Multi-Standard Audit Assistant)` | 对外展示名称 / Public display name. |
| `version` | `1.0.0` | 语义化版本 / Semantic version. |
| `license` | `MIT` | 开源许可证 / Open-source license. |
| `tags` | `ISO, 管理体系, 认证审核, 内审, 差距分析, 体系文件, 合规, audit, compliance, gap-analysis` | 检索标签 / Search tags. |

### 网页发布表单字段对照 / Web Publish Form Field Mapping
> 用于 SkillHub 网页「发布 Skill」表单逐项填写，已附中英文。
> Use this to fill the SkillHub web "Publish Skill" form field by field (bilingual).

| 表单字段 Form Field | 填写值 Value | 说明 Note |
|---|---|---|
| **Display name** 展示名 | `ISO 多标准体系评估陪跑助手 (ISO Multi-Standard Audit Assistant)` | 中英文并列 / Bilingual. |
| **Slug** 唯一标识 | `iso-multistandard-audit-assistant` | 全网唯一；冲突时改 `kooui-iso-multistandard-audit-assistant` / Globally unique; rename with handle if collision. |
| **Summary** 简介（≤300 字） | 见下方「简介」区块 / see Summary block below | 中英双语，约 210 字符 / Bilingual, ~210 chars. |
| **Categories** 分类（最多 3） | `Generate` + `Productivity` + `Business` | 若列表无 `Business` 用 `Writing`/`Other` 替代 / Use `Writing`/`Other` if unavailable. |
| **Topics** 主题标签 | `ISO, 管理体系, 认证审核, compliance, audit, gap-analysis` | 中英文混合检索词 / Mixed CN/EN topic tags. |
| **Publishing as** 发布身份 | `@kooui · InitialDD · Owner` | 由账号自动带出，不改 / Auto-filled from account, do not change. |
| **Version** 版本 | `1.0.0` | 语义化版本 / Semantic version. |
| **Release tags** 发布标签 | `v1.0.0` | 或 `initial-release` 首次发布 / or `initial-release`. |

### 一句话描述 / One-line Description
- **中文**：全量多标准 ISO 体系评估陪跑助手，覆盖 28 个管理体系，提供条款解读、文档解析、差距分析、文件生成与存量文档转换。
- **English**: Multi-standard ISO management-system audit companion covering 28 standards: clause interpretation, document parsing, gap analysis, document generation and legacy-document conversion.

### 简介与概述 / Summary
> 表单 `Summary` 字段限 300 字，请用下方**精简版**（约 210 字符）；完整版见上。
> The web form `Summary` is capped at 300 chars — use the **concise version** below (~210 chars); full version above.

**精简版（表单用 / for the form）：**
- 中英双语 / Bilingual:
  ```
  ISO 多标准体系评估陪跑助手：覆盖 28 个 ISO 标准（9001/14001/45001/27001 等），提供条款解读、差距分析、标准文件生成与存量文档转换，陪你轻松过审。
  ISO Multi-Standard Audit Assistant: covers 28 ISO standards (9001/14001/45001/27001…), offering clause interpretation, gap analysis, document generation and legacy-doc conversion to streamline your certification audit.
  ```

**完整版（SKILL.md 同步 / mirrored in SKILL.md）：**
- **中文**：覆盖 ISO 9001/14001/45001/27001/20000/22000/50001/13485/22301/27701/37301/17025/37001/55001/21001 等 28 个管理体系，提供条款大白话解读、现有文档解析、差距分析、一键生成标准格式体系文件，以及把存量文档自动转换为标准评价格式的能力。
- **English**: Covers 28 management-system standards (ISO 9001/14001/45001/27001/20000/22000/50001/13485/22301/27701/37301/17025/37001/55001/21001 and more), offering plain-language clause interpretation, document parsing, gap analysis, one-click generation of standard-format system documents, and automatic conversion of legacy documents into audit-ready formats.

### 详细描述 / Detailed Description
- **中文**：面向需要顺利通过 ISO 管理体系认证 / 监督审核 / 内部审核的在职人员（质量/环安/IT 负责人、内审员、体系工程师）。内置 7 步陪跑工作流与可调用脚本：条款大白话解读+证据清单、现有文档解析、差距分析、一键生成标准格式程序文件、模拟审核问答，以及把存量文档自动转换为标准合规格式。15 个标准拥有专属框架+模板数据，其余 catalog 标准自动回退通用 Annex SL 框架，同样可正常做差距分析与文件生成。
- **English**: For professionals who need to pass ISO management-system certification / surveillance audit / internal audit (quality / EHS / IT leads, internal auditors, system engineers). Ships a 7-step companion workflow and callable scripts: plain-language clause interpretation with evidence checklists, document parsing, gap analysis, one-click generation of standard-format procedure documents, mock-audit Q&A, and automatic conversion of legacy documents into standard-compliant formats. 15 standards have dedicated framework + template data; other catalog standards fall back to the generic Annex SL framework and still work for gap analysis and document generation.

---

## 2. 作者信息 / Author Info

| 字段 Field | 值 Value |
|---|---|
| 作者 / Author | *（发布时由 SkillHub 账号自动带出 / filled from your SkillHub account）* |
| 主页 / Homepage | *（可选 optional）* |
| 仓库 / Repository | *（可选 optional）* |

> 发布前请在 SkillHub 完成**注册 + 实名认证**，否则无法创建 API Token 与发布。
> Before publishing, complete **registration + real-name verification** on SkillHub, otherwise you cannot create an API Token or publish.

---

## 3. 版本变更说明 / Changelog

### v1.0.0 — 首次发布 / First release
- 7 步陪跑工作流（条款解读 → 文档解析 → 差距分析 → 文件生成 → 存量文档转换 → 模拟审核 → 交付）。
- 内置脚本：`parse_docx.py`（文档解析）、`analyze_gap.py`（差距分析）、`generate_document.py`（文件生成）、`convert_document.py`（存量文档转换）。
- 覆盖 28 个管理体系（15 个专属数据 + 13 个回退通用框架）。
- 中英双语文件生成支持（`--lang bilingual`）。

### v1.0.0 — First release
- 7-step companion workflow (clause interpretation → doc parsing → gap analysis → doc generation → legacy-doc conversion → mock audit → delivery).
- Bundled scripts: `parse_docx.py`, `analyze_gap.py`, `generate_document.py`, `convert_document.py`.
- Covers 28 management-system standards (15 dedicated + 13 fallback).
- Bilingual document generation (`--lang bilingual`).

---

## 4. 发布方式 / How to Publish

### 方式一：CLI（推荐 / Recommended）
> 适用：经常迭代、接 CI / GitHub Actions、团队协作走 git。
> Use when: iterating often, wiring CI/GitHub Actions, or team collaboration via git.

```bash
# 1) 安装 CLI（不附带预置 Skill 集合）
curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 2) 登录（Token 在 个人中心 → API keys 创建，仅显示一次）
skillhub login --key 你复制的完整Token --host https://api.skillhub.cn
skillhub auth whoami

# 3) 本地预检（不真正发布，仅校验格式）
skillhub publish <本技能文件夹路径> --dry-run
# 期望输出：✓ Dry-run passed: iso-multistandard-audit-assistant@1.0.0

# 4) 正式发布
skillhub publish <本技能文件夹路径> --changelog "首次发布"
# 期望输出：✓ Published: skillId=xxxxx status=pending_review
```

### 方式二：通过 Agent 自然对话发布 / Via Agent chat
在接入 SkillHub 的 Agent 客户端里发送：
```
根据 https://skillhub.cn/ai/release.md 把 <本技能文件夹路径> 发布到 SkillHub。
```
Agent 会自动读取发布规范，完成参数校验、登录态确认与发布请求。

### 方式三：网页上传 / Web upload
打开 https://skillhub.cn → 右上角「发布 Skill」→ 拖拽本技能文件夹或 Zip 包上传，按表单填写上述第 1 节信息后提交审核。

---

## 5. 发布包结构 / Package Structure

```
iso-multistandard-audit-assistant/
├── SKILL.md              # 必需：YAML frontmatter + Markdown 指令（含双语发布字段）
├── PUBLISH.md            # 本文件：完整发布信息（中英双语）
├── LICENSE               # MIT 许可证
├── scripts/              # 可执行脚本（4 个）
│   ├── parse_docx.py
│   ├── analyze_gap.py
│   ├── generate_document.py
│   └── convert_document.py
├── knowledge/            # 28 个标准框架与模板数据（JSON）
└── examples/             # 交互示例（场景 A–D）
```

> 发布包已**排除** `_test/`（测试产物），仅含可发布内容。
> The publish package **excludes** `_test/` (test artifacts) and contains only publishable content.

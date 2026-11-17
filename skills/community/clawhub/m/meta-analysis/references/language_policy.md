# Language Policy / 双语语言策略

> This file is the detailed companion to the "Language" section in SKILL.md. Applicability: this policy applies to **ct- skills that are statistical-analysis related AND intended for GitHub publication** (e.g. ct-samplesize). The ct-base scaffold itself ships the bilingual setup for library consistency; ct- skills that are NOT published / for internal use only default to Chinese-only and need no bilingual content. / 本文件是 `SKILL.md` 中「Language / 语言」段的详版补充。适用范围：本策略适用于 **ct- 系列中统计分析相关、且准备发布到 GitHub 的技能**（如 ct-samplesize）。ct-base 作为库底座采用双语脚手架以保持一致；不发布、仅自用的 ct- 技能默认纯中文，无需双语。

## Three core rules / 三条核心规则

1. **English by default / 默认英文**: All user-facing prompt content (reports, explanations, menus, warning boxes) defaults to English. / 所有面向用户的提示内容（报告、解释、菜单、警告框）默认使用英文。
2. **Auto-switch on Chinese-OS / 中文环境自动切换**: When the OS is detected as Chinese (locale contains `zh`/`CN`), prompt content auto-switches to Chinese **without explicit user request**. / 检测到操作系统为中文环境（locale 含 `zh`/`CN`）时，给用户的提示内容**自动切换为中文**，**无需用户显式要求**。
3. **Code output unaffected / 代码输出不受影响**: R / Python code itself is always English, shown per `--show-code`; not affected by the language policy. / R / Python 代码本身始终为英文，按 `--show-code` 规则展示，不受上述语言策略影响。
4. **Separator convention / 分隔符规范**: In any bilingual skill doc, join the EN and ZH text on the same line with ` / ` (slash, spaces on both sides). Never use `|` — it is the Markdown table column delimiter and breaks layout if the content is later moved into a table cell. / 双语文档中，中英文一律用 ` / `（斜杠，两侧空格）连同一行；不要用 `|`——它是 Markdown 表格列分隔符，内容移入表格会崩排版。

## Chinese-OS detection method / 中文环境检测方法

| Platform 平台 | Detection method 检测方式 |
|:---|:---|
| Linux / macOS | Read `LANG` / `LC_ALL` / `LANGUAGE`; check if the language code starts with `zh` (e.g. `zh_CN.UTF-8`) / 读取 `LANG` / `LC_ALL` / `LANGUAGE` 环境变量，判断语言代码是否以 `zh` 开头（如 `zh_CN.UTF-8`） |
| Windows | Use `Get-Culture` / `Get-WinSystemLocale` PowerShell cmdlets, or read `os` env to check if the language code starts with `zh` (e.g. `zh-CN`) / 用 `Get-Culture` / `Get-WinSystemLocale` PowerShell cmdlet，或读取 `os` 环境变量判断语言代码是否以 `zh` 开头（如 `zh-CN`） |

If judged "Chinese environment", generate prompts in Chinese automatically; otherwise use English. / 判定为「中文环境」即自动用中文生成提示内容；否则用英文。


## Doc language convention (for maintainers) / 文档语言约定（面向维护者）

- `README.md`: English only, with a top switch link to `README_zh-CN.md`. / 纯英文，顶部保留指向 `README_zh-CN.md` 的切换链接。
- `README_zh-CN.md`: Chinese only, with a top switch link to `README.md`. / 纯中文，顶部保留指向 `README.md` 的切换链接。
- `SKILL.md` / `AGENTS.md` / `references/*.md`: English-only and agent-facing; bilingual human-readable content lives in the two READMEs. / 仅英文、面向 Agent；双语可读内容统一放在两份 README 中。
- Runtime prompts (from `scripts/i18n.py`) switch to Chinese on a `zh-*` locale and English otherwise. / 运行期提示（`scripts/i18n.py`）在 `zh-*` 环境下自动切中文，否则英文。

## i18n module consumers / i18n 模块的消费者

`scripts/i18n.py` is the **single source of truth** for all bilingual strings in the ct- library. Beyond runtime prompts, it is also consumed by **Excel report export**:

- **ct-registry `export_xlsx.py`** injects `../ct-base/scripts` onto `sys.path` and calls `from i18n import t, set_lang`, then renders all UI-frame labels (sheet names, banners, KPIs, block titles, column headers, chart titles) via `xlsx.*` keys. The report is switched with `--lang {auto,zh,en}` (default `auto` = OS locale). / `export_xlsx.py` 把 `../ct-base/scripts` 注入 `sys.path` 后 `from i18n import t, set_lang`，所有界面框架标签（表单名、横幅、KPI、区块标题、列头、图表标题）均经 `xlsx.*` 键渲染；报告以 `--lang {auto,zh,en}` 切换（默认 auto=OS 语言）。

- **Data-fidelity rule (Excel) / 数据保真原则**：only UI-frame labels are translated; **raw data values are NEVER translated** — e.g. CDE Chinese recruitment status ("进行中") and Chinese conditions stay verbatim in the English report. New `xlsx.*` keys must therefore cover labels only. / 仅翻译界面框架标签，**原始数据值一律不翻译**（英文报告中 CDE 中文状态、中文适应症等原样保留）。新增 `xlsx.*` 键只需覆盖标签。

- When adding Excel labels, append them under the `# ── Excel report (ct-registry export_xlsx.py) / Excel 报告专用键 ──` block in `i18n.py` (EN+ZH), never hard-code Chinese/English inside the consumer script. / 新增 Excel 标签时，统一追加到 `i18n.py` 的 `xlsx.*` 键块（EN+ZH 双语），切勿在消费脚本内硬编码中/英文。

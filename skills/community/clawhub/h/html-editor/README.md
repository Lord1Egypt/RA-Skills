# html-visual-editor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Turn any static HTML into a visually editable page — no code changes needed.**

Click text to edit inline, adjust colors/fonts/layout from a side panel, copy style-prompts to paste into any AI, and export the result as a new HTML file.

把任意静态 HTML 变成「可视化编辑版」：点文字直接改，右侧面板调颜色、字号、布局；6 张风格 Prompt 卡片，点击即把"风格描述 + 色板 + 硬约束"复制给 AI 让 AI 重写 CSS；最后导出新 HTML。

```text
┌─────────────────────────────── Page Content ───────────────────────────────┐ ┌── Style Panel ──┐
│  Titles / paragraphs / tables / cards / timelines — all clickable          │ │ Colors          │
│  Hover → hints; Click hint → jump to control                               │ │ Style Prompts   │
│                                                                            │ │ Layout          │
│  Toolbar: Edit / Save / Undo / Export / Reset / 中 / EN  (draggable)       │ │ Font Size       │
└────────────────────────────────────────────────────────────────────────────┘ └─────────────────┘
```

## ✨ Highlights

| Feature | Description |
|---------|-------------|
| 🖱️ **Inline text editing** | Auto-marks headings, paragraphs, tables, labels, stat cards as editable |
| 🎨 **Data-driven Color panel (v1.8)** | Scans the DOM, ranks colors by usage: top 5 text colors (by character count), top 4 backgrounds, top 3 borders. Works for any theme — blue, red, green, dark. Same color across multiple CSS variables auto-links. |
| 🔤 **Font size sliders** | Scans host CSS `font-size` rules → groups related selectors into ≤ 10 sliders across 3 tiers (Heading / Body / Auxiliary) |
| 📐 **Layout sliders** | Page width, padding, section/card spacing, line-height — all mapped to real DOM selectors |
| 🎭 **6 Style Prompts** | Click a card → copies a complete style-prompt (palette + vibe + hard constraints) to clipboard. Paste to any AI to restyle. Scenarios: Cloud Native · Swiss Grid · Editorial Magazine · Sunlit Warmth · Terminal Hacker · Y2K Kawaii |
| 🌐 **i18n 中 / EN (v1.8.3)** | Dual-display switcher in toolbar; auto-detects `navigator.language`; persists in localStorage |
| ✋ **Draggable toolbar** | Drag the toolbar anywhere; position saved per-browser |
| 🔗 **Bidirectional jump + pinned tooltip (v1.8.2+)** | Hover element → see adjustable props; press P to pin → each row shows swatch / value; out-of-panel colors prompt extraction (A-class) or AI prompt copy (B-class) |
| 📤 **Export Clean (v1.7+, ε scheme)** | One click exports stripped HTML; inline `var()` auto-restored to hex (clipboard-friendly); keeps `data-editable` for re-adapt |
| ✅ **Sanity checks** | Auto-verify mapping, coverage, injection order before writing output |
| 🤖 **Optional LLM labels** | Smarter variable names with Anthropic/OpenAI API (falls back to heuristics) |

## 🚀 Quick Start

```bash
pip install beautifulsoup4
python html-visual-editor/scripts/adapt.py your-report.html
open your-report-editable.html
```

**快捷开始（中文）**：只需一行命令，即可把静态 HTML 变成可视化编辑版。

### Specify output path

```bash
python html-visual-editor/scripts/adapt.py your-report.html -o output.html --force
```

### Skip sanity checks (for complex layouts)

```bash
python html-visual-editor/scripts/adapt.py your-report.html --force --skip-checks
```

> ⚠️ `--skip-checks` forces output even if some checks fail. Review the result manually.

## 📺 Demo

```bash
python html-visual-editor/scripts/adapt.py html-visual-editor/examples/demo-report.html --force --verbose
open html-visual-editor/examples/demo-report-editable.html
```

## 🔧 How It Works

```text
HTML
  ↓ parse_css.py       →  Extract CSS variables, font-size, colors, selectors
  ↓ scan_dom.py         →  Scan DOM, build element → panel mapping
  ↓ generate_panel.py   →  Generate color/font/layout/preset panels + window.X constants
  ↓ inject.py           →  Inject toolbar, panel, editor-core CSS/JS, mark data-editable
  ↓ verify.py           →  Run sanity checks; abort if critical issues found
  → Output: *-editable.html
```

## 📋 Compatibility Levels

| Level | Condition | Result |
|-------|-----------|--------|
| **A** ✅ | `<style>` + 5+ CSS variables in `:root` | Full auto — best results |
| **B** ⚠️ | Few variables, external CSS, or Tailwind | Degraded — text editing + data-driven top-N colors still work; inline colors can be extracted via pinned tooltip |
| **C** ⚠️ | Mostly inline styles, canvas/iframe | Partial — text editing works; data-driven colors still list top-N; use Style Prompt to let AI refactor inline → CSS vars first |

## 🛠️ Install as AI Agent Skill

Works with **WorkBuddy**, **CodeBuddy**, **Claude Code**, **Cursor**, or any AI coding agent:

```bash
# WorkBuddy / CodeBuddy
cp -r html-visual-editor/ ~/.workbuddy/skills/html-visual-editor/

# Claude Code
cp -r html-visual-editor/ ~/.claude/skills/html-visual-editor/

# Cursor / Other agents
# Place in project dir, reference scripts/adapt.py in your agent rules
```

Then tell your agent:

> "把这个 HTML 做成可编辑版" / "Make this HTML editable" / "Add a style panel to this page"

## 🤖 LLM-Enhanced Labels (Optional)

Without any API key, the tool works fine with heuristic naming. If environment variables are available, it uses LLM to generate semantic labels (e.g. "主色调 Accent" instead of "蓝色 Blue").

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # or
export OPENAI_API_KEY=sk-...
```

## 📁 File Structure

```text
html-visual-editor/
├── SKILL.md                  # Detailed usage guide (详细使用说明)
├── README.md                 # This file
├── LICENSE                   # MIT
├── assets/                   # Editor core CSS/JS & panel template
│   ├── editor-core.css
│   ├── editor-core.js
│   └── panel.template.html
├── presets/                  # 6 themes + LLM label prompt
│   ├── builtin.json
│   └── llm_label_prompt.txt
├── scripts/                  # Core engine modules
│   ├── adapt.py              # Main entry point
│   ├── parse_css.py          # CSS parser
│   ├── scan_dom.py           # DOM scanner
│   ├── generate_panel.py     # Panel config generator
│   ├── inject.py             # HTML injector
│   ├── verify.py             # Sanity checks
│   └── utils/
│       └── diagnose_css.py
└── examples/                 # Anonymized demo HTML
    └── demo-report.html
```

## 📝 Changelog

### v1.8.4 (2026-05-28)

- **Extract button now branches by type**: A-class (inline `style=` hex) → orange `+ Extract as variable` (rewrites DOM inline to `var()`, auto smart name like `--text-purple`); B/C/D-class (CSS rule / inheritance / complex expr) → blue `📋 Copy prompt for AI` (copies a semantic refactor prompt to clipboard). Fixes "extract button does nothing" UX for non-inline pages.

### v1.8.3 (2026-05-28)

- **Toolbar lang switcher**: changed from single-label (`中` / `EN` toggle) to **dual-display `中 / EN`** with active-state highlight — both languages always visible, current language opacity 1, other 0.4. English users immediately see the EN option.
- **Colors row label de-duplication**: in-row labels now show only the rank word (`主要 Primary` / `次要 Secondary`), since the section title already provides role context (`文字 Text` / `背景 Background` / `边框 Border`).
- **One-click extract (ε scheme)**: A-class colors → smart hue-based variable name (`--text-purple` / `--bg-mint`) + user-editable prompt + DOM inline rewrite to `var()`. Extracted variables register into `CSS_VAR_TO_ELEMENTS` + `PAGE_ELEMENT_TO_PANEL` so hover hints work.
- **Export var() → hex restoration**: `exportHTML()` now walks all inline `style="...var(--xxx)..."` and replaces with current computed hex. Vars-style block stays for full-page rendering. Result: clipping a snippet to Notion / mail / WeChat preserves colors (no `var()` fallback to default black).

### v1.8.2 (2026-05-27)

- **Export bug fix (todo58)**: exported HTML no longer leaks `.panel-highlight-tooltip` (pinned overlay) and `.pinned-page-el` class residues.
- **Pinned tooltip enhanced (todo31)**: each row now shows a 14×14 swatch + hex value (for colors) or px value (for size/layout). When the hovered element uses a color not in the panel, an amber alert + "+ extract as variable" button appears.

### v1.8.1 (2026-05-26)

- **Color label role prefix + flow hint**: color rows show `文字 主要 Text Primary` etc. for unambiguous 3-group display. Style cards get a bottom flow hint "复制后 → 粘贴到 AI 对话 → AI 会改写 CSS" / "Copy → paste into your AI chat → AI rewrites CSS".
- **Size family pattern hardened**: hex threshold tightened (20→12); bare `th`/`td`/`p`/`h1`/`h2` directly hit family map; demo-report.html now passes sanity checks.

### v1.8.0 (2026-05-26)

- **Data-driven Color panel — methodology rewrite**: `scan_dom.py` now aggregates `color_usage` by walking every DOM text node, computing `color` (inline + CSS cascade + recursive `var()`) and weighting by character count; same for `background-color` (by element count) and `border-color` (by element count). Panel rendering consumes this top-N (5 text / 4 bg / 3 border) instead of name-prefix classification.
- **Frequency-semantic naming**: dropped name-with-hex labels; now uses `主要 Primary / 次要 Secondary / 强调 Highlight / 装饰 Accent / 偶用 Subtle` — works for any theme (blue, red, dark) without code change.
- **Render order**: text → bg → border. The independent "Accent" group is dropped (text top 5 already includes blue/purple/white as needed).
- **Size family auto-match fixes (todo40)**: `.section-title` / `.section-icon` / `.banner-sub` correctly grouped into Heading tier.
- **Layout single-slider section title hidden (todo41)**: when a section has only one slider with the same name as the section, the title is omitted (no more "Section Gap / Section Gap" duplication).

### v1.7.0 (2026-05-26)

- **Colors collapsed 38 → 11**: 4 role groups (Accent / Text / Bg / Border) × ≤ 3 each; hex distance < 30 clustering; smart-order by saturation (accent), brightness (text), brightness desc (bg).
- **Size collapsed 25 → 10**: 14 family patterns (h1 / section-title / stat-num / body / strong / upcoming / event / data / tag / footer ...), 3 tiers.
- **Bilingual coverage**: layout labels and section titles all `中文 English`.
- **Export Clean (Scheme B)**: toolbar export renamed to "导出干净版 Export Clean"; strips toolbar/panel/editor-core but keeps `data-editable` (re-adapt friendly).
- **Layout naming + Line Height**: `ZT Gap` → `Card Gap`; new `行高 Line Height` slider (body, 1.2~2.2 step 0.05).

### v1.6.1 (2026-05-26)

- **Undo fix (B1)**: `applyColor` / `applyHex` / `applyLayout` now all call `pushHistory()`, so the Undo button actually works for color, layout, and text edits
- **Tooltip no longer blocks panel (B2)**: Tooltip positioning now respects the right-side panel width via `_getTooltipMaxRight()` — both initial placement and mouse-follow
- **Old injection cleanup fix (B3)**: `_strip_old_injection()` now loops to remove *all* BEGIN/END marker pairs, preventing stale panel data from leaking across `--force` rebuilds
- **i18n for tooltips (B4)**: `TAB_NAME_TO_ID` / `TAB_COLORS` expanded to bilingual keys; tooltip header + tag labels now translate with `_t()` / `_translateTab()`; new keys: `tooltip_pinned`, `tooltip_hover`, `tooltip_pin_hint`

### v1.6.0 (2026-05-26)

- **MECE scenario styles**: Replaced v1.5's 6 similar-looking SaaS palettes with 6 distinct scenario-driven styles — Cloud Native (product) · Swiss Grid (consulting) · Editorial Magazine (brand) · Sunlit Warmth (NGO/community) · Terminal Hacker (tech) · Y2K Kawaii (creative)
- Each style ships with bilingual `name_zh`/`name_en`, full `vibe` description, and a 6-color `palette` (bg, accent, secondary, text, text_soft, line)

### v1.5.0 (2026-05-26)

- **Style Prompt revolution**: Clicking a preset card no longer applies CSS variables — it **copies a complete restyle prompt to clipboard** (style name, vibe, palette hex, 5 hard constraints). Paste into any AI (Claude/ChatGPT/CodeBuddy) to let the AI rewrite the CSS
- Added `copyStylePrompt()`, `_copyToClipboard()` with secure-context primary path + `document.execCommand('copy')` fallback for `file://` / Safari
- `applyPreset()` simplified to only support `'original'` (used by Reset button)
- Preset schema rewrite: `palette` (6 hex) + `vibe_zh/en` + `name_zh/en` + `is_dark`
- 3-layer hint to prevent confusion: section title「风格 Prompt」+ hint「点击复制风格 Prompt 给 AI」+ toast 2.5s

### v1.4.0 (2026-05-26)

- **Draggable toolbar (todo19)**: Default top-right, drag handle (left dots), position persisted in `localStorage.hve_toolbar_pos`; viewport clamping on drag + resize
- **i18n (todo20)**: `data-i18n` attribute + `I18N_STRINGS` dictionary + toolbar `[中|EN]` switcher + auto-detection from `navigator.language` + persistence in `localStorage.hve_lang`
- **Button dedup (todo21)**: Removed redundant `Export .html` / `Save to browser` buttons from panel bottom (kept only `Reset to defaults`); added passive autosave hint; verify `appB10` threshold lowered 3→1
- **Theme switching overhaul (todo22)**: Fixed `_contrastRatio()` rgb→hex bug; `applyPreset()` now resets to original before overlaying; cleared inline color corrections at start of contrast correction pass; updated `HOST_PREFIX_TO_PRESET_ROLE` to prevent strong accents leaking into bg vars

### v1.3.0 (2026-05-26)

- todo15: subtitle 9→11px + tighter copy
- todo16A: preset adds `--banner-bg-2/3/4` keys
- todo16B: `_applyBannerFooterContrast()` dynamic injection
- todo17: `_applyContrastCorrection()` enforces WCAG 4.5:1
- todo18: `extract_solid_hex_to_vars()` stops skipping `#fff` / `#000`

### v1.2.0 (2026-05-26)

- Mapping fix + swatch UI + "原版/Original" restore + localStorage key encoding + Safari comment + export upgrade + relaxed fingerprint check

### v1.1.0 (2026-05-25)

- **Solid color extraction**: `extract_solid_hex_to_vars()` extracts hardcoded non-gradient colors (color/background/border) into CSS variables — color variable count increased from ~6 to ~30
- **`--force` cleanup**: `--force` now strips old injection artifacts *before* parsing/scanning, preventing stale data leaks
- **appB16 demoted to WARNING**: sections < 2 no longer fails the build; outputs a warning instead
- **appB21 DOM-based verification**: uses `soup.select()` to validate DOM element existence, eliminating false positives from CSS-only references (dead code)
- **Slider state persistence**: layout/font-size slider positions are saved to localStorage v3 format and restored on reload
- **Complete color save/restore**: `saveToStorage()` iterates all `.color-row input[data-var]` instead of relying on hardcoded DEFAULT_COLORS keys
- **Preset prefix matching**: `_map_preset_to_host_vars()` adds a 3rd-pass prefix pattern match (--text-N / --bg-N / --line-N) for better cross-file preset coverage
- **Dynamic PEM (Panel-Element Mapping)**: removed all 17 hardcoded gold-edition selectors from `editor-core.js` (SIZE_BOUNDS, PAGE_ELEMENT_TO_PANEL, CSS_VAR_TO_ELEMENTS, LAYOUT_TARGET_LABELS now fall back dynamically)
- **Source annotation**: `_html` parameter in `generate_panel.py` now documented as "scan_dom HTML snapshot"

### v1.0.0 (2026-05-24)

- Initial release — turn any static HTML into a visually editable page

## 🗺️ Roadmap

- [ ] Image editing (replace/resize images from panel)
- [ ] Drag-and-drop layout reordering
- [ ] More preset themes (community contributions welcome!)
- [ ] Browser extension version
- [ ] Undo history with branch visualization

## 🤝 Contributing

PRs are welcome! Please:

1. Fork → Branch → PR
2. Run `python scripts/adapt.py examples/demo-report.html --verbose` to verify nothing breaks
3. Keep the MIT license header in new files

## 📄 License

[MIT](LICENSE) — free for personal and commercial use.

---

**中文说明**

### 核心功能

- **就地文字编辑**：自动给正文、标题、表格、标签、数字卡片等文本元素加可编辑能力
- **颜色面板（v1.8 数据驱动）**：扫 DOM 文字节点的 computed color，按字符数加权聚出 top 5；背景 top 4、边框 top 3；跨主题通用，命名按使用频次（主要 / 次要 / 强调 / 装饰 / 偶用）
- **字号面板**：从 host CSS 的 `font-size` 规则反推 slider，自动合并同族选择器到 ≤10 项，分 3 组（标题层级 / 正文层级 / 辅助）
- **布局面板**：页面宽度、左右内距、段落最大宽、行高、章节间距、卡片间距、卡片内距等 7 项
- **风格 Prompt（v1.5+）**：点击 6 张场景卡片之一，把"风格名 + 氛围 + 色板 + 硬约束"完整 prompt 复制到剪贴板，再粘贴给 AI 让 AI 重写 CSS。6 个场景：云原生企业 / 瑞士网格 / 杂志编辑 / 阳光手账 / 终端骇客 / Y2K 可爱数字
- **可拖动工具栏 + 中英切换（v1.8.3）**：工具栏左侧抓手可拖动，右侧「中 / EN」双显，激活态高亮，让任何语言的用户都能立刻看到切换入口
- **Pinned 弹窗 + 一键提取（v1.8.2+）**：按 P 固定后弹窗每行带色块/数值；面板没有的色自动提示，按按钮颜色分流——A 类 inline 写死→直改 DOM；B 类 CSS 规则→复制 prompt 给 AI 改
- **导出干净版（v1.7+ ε 方案）**：导出时 inline `var()` 自动还原为 hex，剪贴到 Notion / 邮件 / 微信也不丢色；vars-style 块保留供整篇渲染
- **自动 sanity checks**：映射、预设、字号覆盖率、可编辑覆盖率、注入顺序全部自动检查

### 安装为 Skill

把整个 `html-visual-editor/` 目录放到对应工具可读取的位置：

| 工具 | 路径 |
|------|------|
| WorkBuddy / CodeBuddy | `~/.workbuddy/skills/html-visual-editor/` |
| Claude Code | `~/.claude/skills/html-visual-editor/` |
| Cursor / 其它 Agent | 项目目录或任意稳定路径，规则中引用 `scripts/adapt.py` |
| 手动使用 | `python /path/to/scripts/adapt.py <html>` |

### 实操原则

- 优先运行 `adapt.py`，不要手写 panel
- 不修改 `assets/editor-core.js`，所有适配逻辑放在 scripts 和 window.X 常量里
- 生成结果要先人工抽查：文字是否都可编辑、字号 tab 是否覆盖不同文字层级、预设是否明显生效

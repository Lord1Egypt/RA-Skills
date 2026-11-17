---
name: ide-briefing-ppt
slug: ide-briefing-ppt
version: 1.2.1
displayName: Light IDE 简报 PPT
description: >-
  Generates a single-file 1280x720 HTML presentation by reusing the frozen Light
  IDE visual system extracted from LLM Wiki 分享.html. Use only when the user names
  ide-briefing-ppt, asks to reuse that deck's UI, or explicitly requests the combined
  light-gray canvas, white panels, amber accent, terminal, and file-tree style. Do
  not trigger for generic HTML PPT or internal-sharing requests, editable decks, or
  other visual styles.
---

# Light IDE 简报 PPT

> **EN** Single-file 1280×720 deck locked to the Light IDE UI.  
> **中文** 单文件 HTML PPT，界面必须和参考 PPT 长得一样。

**When / 何时用：** 用户明确点名本 skill、LLM Wiki 原稿，或明确要求整套 Light IDE UI  
**Not / 不用：** 泛指 HTML PPT / 内部分享 · 杂志风 · 瑞士风 · 可编辑 slides · 大表格年报

```text
按 Light IDE 风格做一份分享 PPT
做成和那份 LLM Wiki 分享一样的界面
沿用浅灰 + 琥珀 + 终端 + 文件树那套 UI 做新 PPT
```

## 可直接触发的说法

- 用 ide-briefing-ppt 做一份分享。
- 做一份 Light IDE / 终端风 HTML PPT。
- 界面必须和 LLM Wiki 分享那份一样。
- 帮我把大纲做成琥珀面板、浅灰底、等宽页脚的网页 PPT。

## 最小可用输入

**最低可启动**：主题 + 大纲（或可提炼大纲的原文）。

**推荐输入**：标题、场合/日期、页数、每页结论、要不要过程动画、讲稿备注。

**可兼容输入**：

- 只有主题：先给 6–10 页大纲，确认后再生成。
- 用户说「直接做」：按 8 页默认叙事弧生成，并声明假设。
- 用户点名「和那份 PPT 一样」：视为 UI 锁死，不得换肤。

## UI 锁死（违反即失败）

生成结果必须和 `LLM Wiki 分享.html` / [assets/template.html](assets/template.html) **同一套界面**。换主题，不换皮肤。

1. **必须整文件拷贝** [assets/template.html](assets/template.html)。
2. **禁止改 `<style>`**。`:root`、字号、圆角、间距、组件 CSS 全部冻结。
3. **默认只改两个插槽**：`<title>`，以及 `<!-- SLIDES_START -->` 到 `<!-- SLIDES_END -->` 之间的幻灯片。
4. **动画是唯一例外**：用户明确要求过程动画时，只能在 `// ANIMATIONS_START` 到 `// ANIMATIONS_END` 之间新增 `anims.name` 函数；不得改其它 runtime。
5. **禁止发明 class**。只能用模板已有 class；inline `style` 只能使用版式示例已有的布局属性，正文额外字号只允许封面副标题的 `22px`。
6. **禁止换肤**：不准换主色、不准加渐变英雄区、不准引入 WebGL / Google Fonts / 衬线标题 / 瑞士超细大字。
7. **生成后必须跑**：

```bash
python scripts/validate_deck.py path/to/deck.html
```

校验失败就改，不准交付。

详细版式、组件、动画和人工检查项见 references。

## 工作流

```text
1) 对齐主题、页数、大纲、要不要过程动画
2) 拷贝 assets/template.html 到目标路径
3) 每页从 layouts.md 选版式，只替换文案
4) 需要演示过程时再读 animations.md
5) python scripts/validate_deck.py <输出.html>
6) 浏览器打开，和 template / 原 PPT 对界面
```

### 第一步：对齐内容，不讨论换肤

先确认：

| 项 | 默认 |
|---|---|
| 画布 | 1280×720，页内不滚动 |
| 页数 | 短 6–8 / 中 9–12；超出就拆页，不压缩字号 |
| 动画 | 默认关闭；用户明确要「演示过程」再加 |
| 语言 | 跟随用户；中文标题保持原 PPT 的字号阶梯 |

不要问「要不要换个配色」。配色已锁。

默认叙事弧：封面 → 问题/背景 → 2–4 页核心 → 步骤或对比 → 收束。

### 第二步：拷贝模板

```bash
cp "<SKILL_ROOT>/assets/template.html" "path/to/deck.html"
```

立刻替换 `<title>` 和封面占位文案。Grep `[必填]`，交付前必须清零。

### 第三步：按版式填内容

打开 [references/layouts.md](references/layouts.md)，每页选一个骨架粘贴。

| 版式 | 用途 |
|---|---|
| L1 封面 | 第 1 页 |
| L2 双栏讲解 | 判断 + 证据 |
| L3 终端页 | 代码 / 协议 / 命令 |
| L4 目录树 | 文件、分层、结构 |
| L5 对话卡 | 人话 in / 系统 out |
| L6 术语卡 | 名词解释 |
| L7 步骤条 | 3–5 步流程 |
| L8 对比收束 | 左右职责 + 三步行动 |

组件和颜色语义：[references/components.md](references/components.md)。

**内容密度**：一页一个 `h1`/`h2`，要点不超过 4 条，callout 不超过 1 个。装不下就拆页，不准缩小冻结字号。

### 第四步：可选动画

只有用户要「重放 / 演示过程」时才读 [references/animations.md](references/animations.md)。  
给 `<section>` 加 `data-anim`，在已有 `anims` 对象里加函数。不准为了动画改 CSS。

### 第五步：校验与预览

```bash
python <SKILL_ROOT>/scripts/validate_deck.py path/to/deck.html
```

然后打开文件，对照 [references/checklist.md](references/checklist.md) 和模板本身。

快捷键必须能用：`← →` / 空格翻页，`N` 讲稿，`R` 重放，`F` 全屏。

## 和其它 PPT skill 的边界

| 用户要的 | 用谁 |
|---|---|
| 这套浅灰 + 琥珀 + 终端 + 文件树 | **本 skill** |
| 杂志风 / 瑞士风 | guizang-ppt-skill |
| 浏览器里继续拖改 | frontend-slides-editable |

不要混用它们的 class、主题色或模板。

## 输出

| 文件 | 要求 |
|---|---|
| 单文件 `.html` | 从 template 拷贝，`<style>` 与模板一致 |
| 可选讲稿 | 每页 `<aside class="notes">` |

交付时说明：文件路径、页数、快捷键，以及已跑过 `validate_deck.py`。

## Additional resources

- [references/layouts.md](references/layouts.md) — 可粘贴版式
- [references/components.md](references/components.md) — 组件用法
- [references/animations.md](references/animations.md) — 可选过程动画
- [references/checklist.md](references/checklist.md) — 交付前检查

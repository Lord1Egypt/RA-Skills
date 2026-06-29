# html-text-editor-lite

> **EN** · A lightweight, zero-dependency inline **text** editor you inject into any static HTML report/page — so a non-technical user can click-to-edit the wording right in the browser, save to localStorage, and export a clean HTML. The *light* alternative to a full visual editor: it only changes **words**, never colors/fonts/layout.
>
> **中** · 一个零依赖的轻量「改文字」编辑器，注入到任意静态 HTML 报告/页面后，非技术用户可以**在浏览器里点一下就改文案**，存到 localStorage，并导出干净版 HTML。它是重型可视化编辑器的轻量替代：**只改文字**，不动颜色/字号/布局。

---

## 🗣️ Just tell your AI / 直接对 AI 说

You don't run commands — you ask your AI assistant. Paste one of these:
你不用敲命令，对 AI 说人话即可，复制下面任意一句：

> **EN** · "Make this HTML editable so I can change the text myself: `report/index.html`"
>
> **中** · "把这个 HTML 变成可以自己改文字的版本：`report/index.html`"

The AI will inject the editor and hand you back an `*-editable.html`. Open it, click **开始编辑 / Edit**, change any text, then **导出干净版 / Export** to get a clean `index.html`.
AI 会注入编辑器并给你一个 `*-editable.html`。打开它，点**开始编辑**，改任意文字，再点**导出干净版**拿到干净的 `index.html`。

---

## 📦 Install / 安装

1. **From a marketplace (recommended) / 从市场安装（推荐）**
   Search `html-text-editor-lite` on ClawHub / SkillHub and install.
   在 ClawHub / SkillHub 搜索 `html-text-editor-lite` 一键安装。

2. **Ask your AI to install it / 让 AI 帮你装**
   > "Install this skill from its GitHub repo: `https://github.com/ytisvibecoding/html-text-editor-lite`"
   > "从这个 GitHub 仓库安装 skill：`https://github.com/ytisvibecoding/html-text-editor-lite`"

3. **CLI (fallback) / 命令行（兜底）**
   ```bash
   git clone https://github.com/ytisvibecoding/html-text-editor-lite.git
   python html-text-editor-lite/scripts/inject.py your.html
   ```

---

## ✨ What it does / 能力

- **Click-to-edit any text / 点哪改哪** — headings, paragraphs, list items, table cells, card numbers, and even loose text sitting directly inside flex/grid containers.
- **Zero dependencies / 零依赖** — pure vanilla JS, ~6KB injected, no build step, no network.
- **Non-destructive / 不破坏原页** — default output is `<input>-editable.html`; your original file is untouched.
- **Save & resume / 存了不丢** — edits persist in `localStorage` (survives refresh).
- **Export clean HTML / 导出干净版** — one click downloads an `index.html` with the editor fully stripped out.
- **Idempotent / 幂等** — re-running strips the old injected block first, never stacks.

---

## 🚀 Usage / 用法

```bash
# default: writes your.html -> your-editable.html
python scripts/inject.py your.html

# options / 常用参数
python scripts/inject.py your.html -o out.html        # custom output / 指定输出
python scripts/inject.py your.html --force            # overwrite output / 覆盖已存在
python scripts/inject.py your.html --inplace          # write back to input / 直接写回原文件
python scripts/inject.py your.html --exclude ".side-nav,nav,.legend"  # skip these / 排除不可编辑区
```

Then open the `-editable.html` and use the floating toolbar (bottom-right):
然后打开 `-editable.html`，用右下角浮动工具条：

**① 开始编辑 / Edit → ② 保存到浏览器 / Save → ③ 导出干净版 / Export**

---

## 🧠 How it works / 原理

A **hybrid DOM walk** from `<body>` down:
从 `<body>` 向下做**混合 DOM 遍历**：

- An element whose children are **all inline** (`span/a/b/strong/em/img/br`…) is treated as one **editable text block** and marked whole — no further descent.
  孩子**全是 inline** 的元素 → 当作一个「可编辑文本块」整体标记，不再下钻。
- An element with **block children** (`div/section/ul/table`…) is a **container**: its direct text nodes get wrapped in a tiny `<span class="hve-t">` (so "orphan text" inside flex/grid cards becomes editable), then we recurse into each element child.
  含**块级孩子**的元素是「容器」：把它的直接文本节点用 `<span class="hve-t">` 包起来（让卡片里的「孤儿文字」也能改），再递归进每个孩子。
- `SCRIPT/STYLE/SVG/CANVAS/INPUT/BUTTON` and any `--exclude` subtree are skipped.
  跳过脚本/样式/SVG/表单控件，以及 `--exclude` 命中的子树。

This guarantees **no nesting** (parent & child never both editable) and that **loose div text is covered**, which a naive tag-whitelist scanner misses. On a real report this raised text coverage from **318/513 → 496/513** (the rest is the side-nav, excluded on purpose).
这样保证**不嵌套**、且**div 里的散文字也能改**——这正是「窄标签白名单」扫描漏掉的部分。某真实报告实测覆盖率从 **318/513 提升到 496/513**（剩余即左侧导览，故意排除）。

---

## ⚠️ Notes / 注意

- The page must be a complete document with `</body>`; a bare fragment is rejected.
  必须是含 `</body>` 的完整文档；残缺片段会报错。
- `localStorage` is per-browser/domain — clearing cache or switching browser loses edits. For permanent keeping, always **Export**.
  localStorage 按浏览器/域名存，清缓存或换浏览器会丢；正式留存务必**导出干净版**。
- This is the *light* sibling of a full visual editor. Want to change colors / fonts / layout? Use a visual editor instead.
  这是轻量版。想调色/字号/布局？请用可视化编辑器。

---

## License / 许可

MIT © ytisvibecoding

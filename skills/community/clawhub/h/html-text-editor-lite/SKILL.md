---
name: html-text-editor-lite
description: Inject a lightweight, dependency-free inline TEXT editor into any static HTML report/page so a non-technical user can click-to-edit text directly in the browser, then export a small JSON of just-the-changes ({orig,new} per block) that the AI backfills into the original source by content-match and redeploys. Use when the user wants to "edit the text myself", "make this HTML editable", "可编辑版", "我想自己改文字", "只改文字", or to tweak wording on a generated report/dashboard/long-image without sending screenshots back each time. This is the LIGHT alternative to the heavy html-visual-editor (color/font/layout panels). Choose this when the need is purely "change the words", not restyling.
description_zh: 给任意静态 HTML 注入零依赖的轻量「改文字」编辑器：非技术用户在浏览器里点一下就改文案，然后一键「导出改动给AI」（只导出改了哪几段的 orig→new），AI 按内容精确回填进源文件并重新部署。只改文字，不动颜色/字号/布局，是 html-editor（重型）的低阶替代。
description_en: Inject a zero-dependency lightweight inline TEXT editor into static HTML; the user clicks to edit wording, then exports a tiny JSON diff of changed blocks ({orig,new}); the AI backfills it into the original source by content-match and redeploys. Words only — never colors/fonts/layout.
disable: false
agent_created: true
---

# html-text-editor-lite

把任意静态 HTML 升级成「可点击改文字」的版本，建立一个**安全的人改字闭环**：
**editable.html（点着改）→ 导出改动 json → apply_edits.py 按内容回填进源文件 → 重新部署。**
纯原生 JS、零依赖、约 8KB，不破坏页面。是 `html-editor`（重型，调色/字号/布局）的**低阶替代**——只管"改文字"。

## When to use
- 用户说「我想自己改文字」「只改文字」「做个可编辑版」「让我直接改 HTML 文字」「不用每次截图给你改」。
- 已产出 HTML 报告/看板/长图，用户只想微调**文案措辞**（不是调颜色/字号/布局）。

**不适用**：调色、改字号、换布局、重塑视觉 → 用 `html-editor`（html-visual-editor）。

## 核心理念：源文件是唯一真源，浏览器只产出「改动清单」
绝不让浏览器导出的整页 HTML 去覆盖源文件——浏览器重新序列化会**破坏 inline style**（如 `font-family:"X"` 被改成 `font-family:""` 乱码）、**残留编辑器 JS 片段**。所以本 skill 的推荐导出是**「导出改动给AI」**：只导出用户**真正改过**的文本块，每块带 `orig`(原始 innerHTML) + `new`(新 innerHTML)。`apply_edits.py` 按 `orig` 在源文件里**按内容定位**替换为 `new`，免疫位置漂移、绝不污染无关部分。

## Steps
1. 确认目标 HTML 是完整文档（含 `</body>`）。
2. 注入编辑器（默认生成 `<input>-editable.html`，不动原文件）：
   ```bash
   python <skill-dir>/scripts/inject.py <input.html> [-o out.html] [--force] [--inplace] [--exclude ".side-nav,nav,.legend"]
   ```
   默认已 `--exclude ".side-nav,nav"`，避免误编辑导航目录。
3. `present_files` 展示 `*-editable.html`，告诉用户三步：① **开始编辑** 点文字改 → ②（可选）**暂存**（localStorage，刷新不丢）→ ③ **导出改动给AI**，得到 `我的改动-交给AI.json`。
4. 用户把 json 发回。AI 按内容回填进**源文件**（不是 editable，是真源 source/index.html）：
   ```bash
   python <skill-dir>/scripts/apply_edits.py <我的改动.json> <source.html> [--dry-run]
   ```
5. 重新生成/部署（按该项目的部署方式，如 GitHub Pages / Vercel / EdgeOne）。源文件始终是唯一真源。

> 兜底：若**没有可回填的源文件**（一次性页面），可用工具条的「导出干净版」下载独立 clean.html。但只要有源文件，永远用 json-diff 路径。

## How it works
- **混合 DOM 遍历**：从 `body` 递归，元素「孩子全是 inline」→ 整体标 `data-hve`，不再下钻；「含块级孩子」→ 把直接文本节点用 `<span class="hve-t">` 包住（救 flex/grid 卡片里的"孤儿文字"），再递归。跳过 SCRIPT/STYLE/SVG/INPUT/BUTTON 等及 `--exclude` 子树。保证不嵌套、孤儿文字也能改。
- **导出改动给AI（主）**：注入时先 snapshot 每块的**真实原始 innerHTML**（在 localStorage 恢复之前），导出时只收集 `orig.trim()!==now.trim()` 的块，写成 `{changes:[{orig,new}]}`。
- **apply_edits.py 回填**：精确匹配优先（唯一→替换；多处→跳过报警绝不猜）；不中则折叠空白做唯一匹配并用容错正则映射回源串替换；未匹配项报告，至少命中 1 条才写文件。旧版 `{edits:{tN}}`（按位置编号）直接拒绝并提示重导出。
- 编辑块用 `HVE-LITE START/END` 注释包裹 → **幂等**：重跑先剥离旧块。localStorage key 由输出文件名 md5 派生，同源多报告互不覆盖。

### 历史教训（务必记住）
1. **白名单遍历会漏 div 文字**（旧 v1）：只扫 h1-4/p/li/span/b… 会漏掉 `<div class="quote/cs-line/onum">` 这类 div 装的文字和卡片孤儿文字。现用混合遍历，实测覆盖率从 318/513 升到 496/513。
2. **导出整页 HTML 覆盖源文件 = 灾难**：浏览器序列化破坏 `style="font-family:'X'"`（双引号套双引号更会变 `jetbrains=""` 乱码）、残留 `已导出干净版`/`createObjectURL` 等 JS 文本漏到页面底部。→ 改用 json-diff，源文件永不被浏览器整页覆盖。
3. **inline style 字体名用单引号** `'JetBrains Mono'`，不能双引号套双引号（非法 HTML，浏览器自动改坏）。
4. **位置编号会漂移**：按 tN 回填，结构一变就写串位。→ 必须按 `orig` 内容定位。

## Pitfalls
- 导航/目录默认 `--exclude ".side-nav,nav"`；别的类名做导航/图例/工具条要手动加 `--exclude`。
- 必须有 `</body>`，否则报错退出。
- localStorage 按浏览器/域名存，换浏览器/清缓存会丢；正式留存靠「导出改动给AI」+ 回填源文件。
- 用户务必用**最新注入的 editable**导出（旧文件导出的可能是旧格式 json，apply_edits 会拒绝并提示重导）。
- 中文在 Python 模板里用 `\uXXXX` 转义。

## Verification
- 注入后：`grep -c 'HVE-LITE START' out.html` = 2（START 注释 + export 里的剥离正则各 1）；`grep -c 'id="hve-bar"' out.html` = 1；`grep -c 'hve-diff' out.html` ≥ 1。
- 覆盖率自检（带 div 卡片的页面强烈建议）：jsdom `runScripts:'dangerously'` 加载后 `document.querySelectorAll('[data-hve]').length` 应远大于个位数。
- 回填自检：`apply_edits.py --dry-run` 先看命中数；正式回填后 grep 新文案=1、旧文案=0。
- 浏览器：点「开始编辑」→ 绝大多数文字（含 div 文字、孤儿文字）可改、导航不可改；改一句→「导出改动给AI」应得到含该句 orig/new 的 json。

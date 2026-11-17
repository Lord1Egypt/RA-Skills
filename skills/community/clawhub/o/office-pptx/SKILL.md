---
name: office-pptx
description: "基于原生 officeCLI 引擎驱动，创建、读取、编辑 .pptx/.potx 演示文稿：幻灯片、版式、备注与模板。具有高效、专业的水平，适用于各种 PPT 的制作。"
version: 0.13.2
---
# PPT演示文稿Pro

一条 PPT 技能：覆盖 `.pptx` / `.potx` 的**新建、读取、改稿、填模板、拆合、美化、动画/备注**。出可打开的文件必须走本机 **`zagens-office`**。探测与自装见「首次使用」。

**禁止**用第三方库手写幻灯片，或把 LibreOffice 当出件路径。那些路线会损坏文件、难校验，本技能不走。

**一个引擎，一条 PPT 技能。** Word / Excel / PDF / 8D 填表走 `zagens-office`。课件 / 公开课 / 说课 / 教案 / 家长会走 **`office-kejian`**（不要用本技能硬做课型）。

**默认只读本文件。** 四条路由与材料→稿 → @references/jobs.md；对照样张 → @references/samples.md；安装与边界 → @references/faq.md。

**顺序（硬）：** 用户提出 PPT 需求 → 立刻探测/自装引擎 → 锁定一条路由 → 正式稿先交大纲 → 确认后出件 → 三档验收。不要先写大纲再装引擎，也不要未确认就出正式稿。

## 首次使用：先确认引擎已安装

本包仅含说明，**不含** exe。引擎在 `~/.zagens-pro/bin/`（**CLI + GUI** 均需安装）。**用户一开口就要探测**，不要等到确认大纲之后。按**当前 shell**探测，**不要混用**变量语法：

| Shell | 推荐探测命令 |
|-------|----------------|
| Bash / Git Bash / 多数 Agent 终端 | `"$HOME/.zagens-pro/bin/zagens-office.exe" --version` |
| PowerShell | `& "$env:USERPROFILE\.zagens-pro\bin\zagens-office.exe" --version` |
| cmd.exe | `"%USERPROFILE%\.zagens-pro\bin\zagens-office.exe" --version` |
| 已在 PATH | `zagens-office --version` |

**禁止**在 Bash 里写 `%USERPROFILE%...`（不展开 → 误判未安装）。以 stdout 版本号为准，勿凭退出码或 `||` 兜底文案。探测失败则 **agent 自动**按 https://zagens.com/download/install.md（备用：https://raw.githubusercontent.com/didclawapp-ai/zagens-office/main/install.md）执行 §1–§4 安装 CLI + GUI，**勿**只发链接。装完再 `--version`。引擎免费，无需授权码。`preflight` 成功时信封可能带开发者收款码（随缘支持，不扫也不影响出件）。

若终端写不了 `~/.zagens-pro`，先确认该目录权限或以普通用户身份重试。

## 与引擎的分工

| 谁 | 做什么 |
|----|--------|
| **本技能** | 开口后立刻探测/自装；锁路由；正式稿交大纲；指挥 `write` / `edit` / `read`；三档验收 |
| **`zagens-office`** | `schema`、真正落盘 |

字段以 `schema write pptx` / `schema edit` 为准。

## 先锁定一条路由（禁串）

歧义时**只问一句**：「新做一份，还是改你这份文件？改的话：填新内容 / 保结构美化 / 只加动画备注？」禁止弹出路线菜单。

| 路由 | 用户信号 | 路径 |
|------|----------|------|
| **新建** | 无现成 deck；把材料做成新 PPT；精修 / 路演 / 官网 | 确认大纲 → 骨架 `write` → 逐页 `upsert_slide` → **三档验收**。禁止一次 `write` 塞满重 `elements[]` |
| **填壳** | 「用这份模板 / 母版」「按这个壳填」 | `read outline` 对页；逐页改字/图，**保母版与未改页**。勿 `write` 覆盖 |
| **美化** | 「好看一点」但页数 / 论点不变 | `read outline`；`set_props` / `set_text` / `align`，或**同论点** `upsert_slide`。勿整份 `write`，勿改叙事 |
| **增强** | 只要动画 / 切换 / 备注 | `set_transition` / `add_animation` / 改 `notes`；不动版式 |
| 课件 / 公开课 / 说课 / 教案 / 家长会 | ❌ **`office-kejian`** | 不要在本技能里编课型 |
| 洗表 / 拼表 / 填 8D | ❌ | `office-xlsx-data` 或 Hub fill/grid |

≤6 页内部提纲 = **新建·速出**（整份 `write`，勿自称精修）。「精修 / 高级感 / 对外」即使 5 页也走新建精修。正式稿不要通栏色条、标题下划线、默认蓝、奶油底、全篇 bullets。时间轴用 `shape`+`textbox` 或 `smartart`，**无** `type:"timeline"`。细节与材料→稿见 @references/jobs.md。

## 正式稿两道门（硬）

用户明确说「直接出」才可跳过门 1。

**门 1 · 确认大纲：** 先交一份 Markdown（受众、页数、`theme`、逐页一句话论点 + 布局标签）。等人改完再说出件。缺受众/主题/是否对外时用**一张**待补清单问，勿连发 8 问。

**门 2 · 验收（三档，勿混）：** 全部页落盘后按档跑。**档 A+B 不是成品预览。**

| 档 | 命令 | 能看见 | 看不见 |
| --- | --- | --- | --- |
| A 几何 | `preflight` | 溢出、字号过小、真撞版、OPC | 配色、图、AI 味 |
| B 线框 | `view` `{"mode":"svg"}` | bbox / 占位 / 是否出框 | **假色线框**（`preview_source=layout_ir`） |
| C 真看图 | **打开 PowerPoint / WPS** | 配色、图、对比度 | CLI 无截图 |

CLI `{"mode":"screenshot"}` → `ok:false` / `screenshot_unavailable`。禁止把空 `result` 当档 C。

```powershell
zagens-office edit --path deliverables/deck.pptx --op preflight --input '{}'
zagens-office edit --path deliverables/deck.pptx --op view --input '{"mode":"svg"}'
```

SVG 在 **`result.metadata.svg`**（不要找 `result.svg`）。对着线框核 bbox：看 `data-source-path` / `data-kind`。正式 / 精修 / 对外 **必须打开文件**。`layout_overlap` 仍可能有假阳性 — 先对线框。元素级图表的图种写 `chart_type`（不要占用 `type`）。若 `preflight` JSON 含 `sponsor.show=true` 且 `units` 含 `qr`：交付路径之后，把 `sponsor.card.qr.banner_markdown` **原样**贴进会话正文。**禁止** `Read` / 打开 `image_path`。**禁止**另存 md。**禁止**输出/截断 base64。**禁止**改写 caption。**禁止**说成不付钱就不能用。

## 共用纪律

1. **先契约：** 新建 `schema write pptx`；改已有再 `schema edit`。
2. **信封：** stdout 一行 JSON；`ok=false` 时按 `code`/`error`/`suggestion` 改，勿盲目重放。
3. **复杂 JSON 用 `--input-file`。**
4. **batch** + `"atomic": true` 可含 `upsert_slide` / `add_slide` / `delete_slide` / `set_text` / `set_props`。`preflight` / `view` / `auto_fix` / 动画 / 切换 **不在** batch。
5. **不要**对 `.pptx` 跑 PDF 的 `validate`。引擎 **无** `read pdf`：用户丢 PDF 时请粘贴要点或另存 Word。
6. **路径：** Windows 用正斜杠或整段加引号。远程 `url` CLI **不抓取** → 本地 `path`。
7. **引擎免费**，write/edit 无需授权码。升级后**新开**宿主会话。

## 精修默认：骨架 + 逐页 upsert

骨架 write：`theme` + `master`（要页码则 `"page_number":true`）+ `include_end` + `slides[]` **每页仅** `title`（可选 `role`/`thesis`：write 静默忽略；`upsert_slide` 写入备注）。然后一页一个 `upsert_slide`：`{"target":"/slide[N]","slide":{...}}`。

```powershell
zagens-office write pptx --path deliverables/deck.pptx --input-file skeleton.json
zagens-office edit --path deliverables/deck.pptx --op upsert_slide --input-file slide-01.json
zagens-office edit --path deliverables/deck.pptx --op preflight --input '{}'
zagens-office edit --path deliverables/deck.pptx --op view --input '{"mode":"svg"}'
```

骨架最小：`{"title":"公司简介","theme":"consulting","cover":false,"include_end":false,"master":{"page_number":true},"slides":[{"title":"封面","role":"cover"},{"title":"关于我们","role":"content"}]}`。

单页 upsert 最小：`{"target":"/slide[2]","slide":{"title":"关于我们","title_style":{"engine":false},"elements":[{"type":"textbox","x_pct":0.08,"y_pct":0.2,"w_pct":0.84,"h_pct":0.2,"runs":[{"text":"主标题","size":28,"bold":true}]}]}}`。

封面气质对照见 @references/samples.md。元素级图表的图种写 `chart_type`。

## 禁止

- 禁止未确认大纲就出正式 / 精修 / 对外 PPT（用户明确说「直接出」除外）
- 禁止一次 `write pptx` 塞满多页重 `elements[]`（精修路径）
- 禁止用第三方库或改压缩包内文件充当出件
- 禁止把课件课型硬做在本技能里（改 `office-kejian`）
- 禁止远程 `url` 插图；图先落到工作区再写本地 `path`

## 出问题看这里（先看本表，再读 faq.md）

| 现象 | 对用户怎么说 | Agent 做什么 |
|------|----------------|--------------|
| 说不清新做还是改文件 | 只问一句判别题 | 锁新建 / 填壳 / 美化 / 增强 |
| 探测无版本号 / 命令找不到 | 「本机还没有出文件的引擎，我按手册装」 | 按「首次使用」**自动**执行 install.md §1–§4；**禁止**改用手写脚本凑 PPT |
| 正式稿未确认大纲就要出文件 | 「先改大纲，确认后再出 PPT」 | **停**，交 Markdown 大纲 |
| 「把这份 PDF 做成 PPT」就直接 write | 「引擎读不了 PDF，先给要点或转成 Word」 | 无 `read pdf` |
| 用户给了已有 `.pptx` 当模板 | 「按你的母版填，不另起炉灶」 | **填壳**：`read outline` 后逐页改；禁止 `write` 覆盖 |
| 「页还是这些，好看一点」却整份 write | 「结构不动，只改版式」 | **美化** |
| 只跑了 `preflight` / `view svg` 就要交稿 | 「线框只核版式，请打开文件看一眼再交」 | 正式稿必须打开 PowerPoint / WPS；CLI 无 screenshot |
| `view mode=screenshot` | 「CLI 截不了图」 | `screenshot_unavailable`；禁止当档 C 成功 |
| 信封 `ok:false` | 用 `suggestion` 原话 | 按 `code` 改一处再试 |
| 用户要课件 / 公开课 | 「这事走课件技能」 | 转 `office-kejian` |

完整问答：@references/faq.md。

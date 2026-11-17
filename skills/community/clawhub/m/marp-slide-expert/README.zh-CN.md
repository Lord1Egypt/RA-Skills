# Marp Slide Expert

> [English](README.md) · 53 页图例：[examples/infographic-gallery.marp.md](examples/infographic-gallery.marp.md)

**把 Markdown 渲染成咨询顾问级的幻灯片。** 关系图、信息架构图、汇报图表、数据可视化——连同封面、分栏、表格版式，一次渲染成可以直接上演讲台的 PDF。

- **咨询级制图，零拖拽** —— 19 种图形骨架（漏斗、金字塔、桑基、泳道、雷达、平衡轮、2×2……）、6 种叙事外壳、7 套配色（含麦肯锡式咨询蓝）：像咨询顾问一样「选图」，而不是对着对齐线拖框
- **有图有表，也不用自己排版** —— 封面 / 章节页 / 双栏 / 三栏 / 主次分栏 / 上文下图全部内置；尺寸、字号、15 行溢出红线也都替你守着
- **专业演讲、咨询项目直接可用** —— 纯矢量输出：投影不糊、打印不虚、改色只动一个十六进制值
- **彻底解放脑力工作者** —— 把脑力留给「讲什么」；排版、配色、画图，交给 skill

**它是基于 Markdown 的。** Markdown 是纯文本「源码」——一份 deck 就是一个可读、可改、可 diff 的 `.md` 文件：

- **人改得动，AI 更改得动** —— 改数字、换配色、重画一张图，都是改一行文本；一句提示词，AI 就能照着改
- **一份源码，多端交付** —— `marp` 一键导出 **PDF / HTML / PPTX**；`.md` 还能放进 **Obsidian 知识库**，和笔记一起管理、搜索、版本化
- **AI 时代原生 skill** —— 为 Claude Code / Cursor 这类工作流而生；会**静默**破坏渲染的坑（表格半宽、SVG 变源码、空行断图……）已全部前置修好

## 幻灯片示例

![](./assets/sample-gallery.png)

53 页图例总览（[PDF 版](examples/infographic-gallery.marp.pdf)）——每个骨架、每个隐喻、每套风格各一页，选型时一翻到底。


## 为什么用这个 skill

- **Marp 默认主题几处必坏的坑** —— 表格半宽、没有 CJK 字体、内容溢出底部。skill 自带一份能用的配色和 CSS，全部修好
- **内联 SVG 跟着文件走** —— PNG 改一个数字要重画；内联 SVG 改一处十六进制值就够。skill 自带 19 套骨架模板和坐标公式，不用边画边算
- **不靠肉眼赌** —— skill 自带 SVG lint（6 项确定性检查），渲染命令写在卡片里。交付前两道自动关卡

## 安装

**① 安装 skill 本体**（一条命令，从 GitHub 拉取）：

```bash
npx skills add mebusw/marp-slide-expert       # 装到当前项目
npx skills add -g mebusw/marp-slide-expert    # 或全局安装（所有项目可用）
```

不用 CLI 就手动装——克隆进本地 skills 目录：

```bash
git clone https://github.com/mebusw/marp-slide-expert ~/.claude/skills/marp-slide-expert
```

skill 由 Agent Skills 消费：装好后 Claude Code / Cursor 等会自动加载，做 marp 的会话里说一句「用 marp-slide-expert 出图」即可。

**② 安装依赖：marp CLI**（渲染 PDF / PPTX / 图片用）：

```bash
npm install -g @marp-team/marp-cli
# 如果 npm -g 失败，降级为：
npx -y @marp-team/marp-cli --version
```

> GitHub 仓库：[mebusw/marp-slide-expert](https://github.com/mebusw/marp-slide-expert)

## 快速开始

```markdown
---
marp: true
theme: default
paginate: true
style: |-
  /* 从 references/style-bootstrap.md 整段粘过来 */
---

<!-- _class: cover -->

# 我的 deck 标题

## 副标题

---

## 第一页

- 要点 1
- 要点 2
- 要点 3
```

导出 PDF：

```bash
marp deck.marp.md --pdf --allow-local-files
```

一份源码，多端交付——网页、PPT、逐页图片：

```bash
marp deck.marp.md --html        # 网页版（可全屏演示）
marp deck.marp.md --pptx        # PowerPoint（逐页图片版）
marp deck.marp.md --images png  # 逐页 PNG（发帖配图用）
```

> 想要**可编辑**的 PPT？加 `--pptx-editable`（实验特性，需本机装有 LibreOffice）。

如果用了内联 SVG，所有导出都要带 `--html`：

```bash
marp deck.marp.md --html --pdf --allow-local-files
```

## 两条原则

**每页最多 15 行，注释不计入。** 一页显示 15 行可见内容就算满了。HTML 注释不渲染也不占行——演讲者备注就该这么藏。

**页级版式 vs 图级版式。** 不同问题用不同工具：

- 这一页内容很多？ → 分栏 / 分区（`<div class="cols cols-2">`）
- 这一页要表达「节点之间的关系」？ → 内联 SVG

同一份 deck 两类都用，不冲突。

## 里面有什么

| | |
|---|---|
| `references/infographics-svg/` | 19 个骨架模板（阶梯、箭头串、2×2、价值树、桑基、漏斗、泳道、便当格、并列圆圈、图文卡片组、起伏波浪大事记、饼图、雷达图、平衡轮……）+ 6 个叙事外壳（金字塔、飞轮、冰山、漏斗、洋葱、聚焦）+ 7 套配色 |
| `references/layout-patterns.md` | 页级版式菜谱（封面、分隔、内容、分栏、分区、图片叠加） |
| `references/style-bootstrap.md` | UPerform / openclaw 配色 —— 整段粘进 frontmatter 即可 |
| `examples/infographic-gallery.marp.md` | 53 页样例 deck，每个模板都用上 —— 起点就在这 |
| `scripts/svg-lint.mjs` | 6 项确定性 SVG 检查（空行、`---`、id 冲突、坐标越界）。每次渲染前必跑 |
| `scripts/build-gallery.mjs` | 从 references/ 重新生成样例 deck。改了模板重跑就行，不要手改 deck |

## 工作流程

1. 把 `style:` 块从 `references/style-bootstrap.md` 整段粘进 frontmatter
2. 写幻灯片。每页不超过 15 行。内容多用分栏/分区，要表达结构关系就用内联 SVG
3. 如果用了 SVG，跑 `node scripts/svg-lint.mjs deck.marp.md`
4. `marp deck.marp.md --pdf --allow-local-files` 渲染（用了 SVG 加 `--html`）
5. 打开 PDF 逐页看。**不要相信你的 SVG 源码**——渲出来亲眼读
6. 迭代

## 维护

属于 [mebusw/skills](https://github.com/mebusw/skills) 集合。在父仓库提 issue。

---
name: huashu-book-pdf
description: |
  深度调研一个主题，生成100页+书籍级PDF手册。模块化HTML片段架构 + 语义化版本管理 + 多Agent并行写作 + Playwright渲染PDF。
  当用户需要制作完整的PDF手册、电子书、橙皮书、参考指南时触发。即使用户只是说「做一本书」「做个PDF手册」「做个完整指南」「做一本XX的手册」也应触发。
  明确触发词：橙皮书、PDF手册、电子书、参考指南、完整手册、书籍级PDF、做一本。
  与huashu-md-to-pdf的区别：md-to-pdf转换单个md文件；本skill从零开始（调研→规划→多agent并行写作→合并构建→版本管理）。
---

# Book-PDF：书籍级PDF手册全流程

从一个主题到100页+专业PDF。五个阶段：调研 → 规划 → 写作 → 构建 → 版本更新。

## 前置依赖

- Node.js >= 16
- Playwright：`npm install playwright && npx playwright install chromium`

## 参考资料导航

| 需要时读取 | 文件 | 内容 |
|-----------|------|------|
| 写HTML片段时 | [references/design-system.md](references/design-system.md) | CSS变量、主题、组件HTML速查、视觉红线 |
| 新建项目时 | `templates/` 目录 | 可直接复制的骨架文件（build.js/build-pdf.js/update.sh/styles.css） |
| 参考已有项目时 | `01-公众号写作/_过程文件/openclaw-guide/` | 首个实战项目（8 Part、35节、100页+） |

## 项目初始化

用 init 脚本一键创建项目骨架：

```bash
bash scripts/init-project.sh <项目目录> <手册标题>
# 示例：bash scripts/init-project.sh ./my-guide "Python完全指南"
```

自动创建目录结构、复制模板文件、生成 version.json/CHANGELOG.md/PROJECT.md、检查依赖。

## 项目结构

```
{项目名}/
├── PROJECT.md          # 项目中枢（大纲+进度+数据速查）
├── styles.css          # 共享CSS（从templates/复制）
├── build.js            # HTML合并脚本（从templates/复制，改FRAGMENT_ORDER）
├── build-pdf.js        # Playwright PDF渲染（从templates/复制）
├── update.sh           # 一键版本更新（从templates/复制）
├── version.json        # {"version":"1.0.0","build":1,"lastUpdate":"","title":""}
├── CHANGELOG.md        # 更新日志
├── fragments/          # 内容片段（纯HTML，不含<html><head>）
│   ├── 00-cover.html / 01-toc.html
│   ├── part{N}-{中文简称}.html
│   ├── appendix.html / 99-backpage.html
├── research/           # 调研资料
├── output/             # {title}-v{version}.html/.pdf
└── versions/           # 历史PDF存档
```

## 阶段1：调研

1. 与用户确定主题和目标读者
2. 拆分调研维度（6-10个方向）
3. 启动多个background agent并行调研，每份保存到 `{项目目录}/research/YYYY-MM-{关键词}.md`
4. 调研完成后汇总，进入规划

## 阶段2：规划

编辑项目目录下的 `PROJECT.md`，包含：
- 章节大纲表（Part + 节号 + 标题 + 核心内容 + 信息来源）
- 调研资料索引（路径 + 摘要 + 状态）
- Agent并行分工方案（关联性强的Part分给同一个agent）
- 进度追踪表 + 关键数据速查

修改 build.js 中的 `FRAGMENT_ORDER`。与用户确认大纲后进入写作。

## 阶段3：写作

多Agent并行，每个agent输出一个HTML片段。

每个写作agent需要：
1. 读取 [references/design-system.md](references/design-system.md) 了解可用组件和**片段结构规范**
2. 读取对应调研资料
3. 输出纯HTML片段（不含 `<html><head><style>` 标签，只写正文内容）

### ⚠️ 片段结构铁律（必须在agent prompt中明确告知）

每个正文片段**必须**遵循以下结构，否则PDF排版会出错：

```html
<div class="content">
<h2 class="section-title page-break" id="partN"><span class="num">§0N</span> 标题</h2>
<p class="section-en">English Title</p>
<p class="section-intro">概述</p>
<!-- 正文 -->
</div>
```

三条规则：
- **`<div class="content">`** 包裹 → 控制左右边距（没有它内容顶边）
- **`id="partN"`** 属性 → 目录锚点跳转需要
- **`page-break` class** → 每章从新页开始

目录片段使用 `.toc` + `.toc-item` + `<a href="#partN">` 结构。详见 design-system.md。

### 品牌水印（封面+尾页必须包含）

所有PDF手册的封面和尾页**必须**包含以下品牌信息：

**封面**：
- 作者：`<div class="cover-author"><strong>蒲公英</strong><br>公众号「AI编程蒲公英」· B站「AI编程程序猿-蒲公英」</div>`
<!-- - 专属标识：`<div class="cover-exclusive">知识星球「AI编程：从入门到精通」专属内容</div>` -->

**尾页**（class必须是 `back-page`，带连字符）：
<!-- - 知识星球二维码：`<img src="../../知识星球/zsxq-qrcode.jpg">` -->
<!-- - 知识星球链接：`https://wx.zsxq.com/group/48888144124288` -->
- 社交链接：B站 `https://space.bilibili.com/3493114559858979/` · 公众号「AI编程蒲公英」
- 详细模板见 design-system.md 和 `templates/fragments/99-backpage.html`

## 阶段4：构建

```bash
node build.js       # 合并片段 → HTML
node build-pdf.js   # Playwright → PDF
# 或一键：
./update.sh build   # 仅构建
```

## 阶段5：版本更新

修改 `fragments/*.html` 后运行：

```bash
./update.sh patch "修正某个错误"     # 1.0.0 → 1.0.1
./update.sh minor "更新内容"          # 1.0.0 → 1.1.0
./update.sh major "新增章节"          # 1.0.0 → 2.0.0
```

自动：更新version.json → 写CHANGELOG → build HTML（版本号注入封面）→ 生成PDF → 备份到versions/

## 快速启动清单

1. [ ] 确定主题、读者、规模
2. [ ] `bash scripts/init-project.sh <目录> <标题>` 创建项目
3. [ ] 修改 build.js 的 `FRAGMENT_ORDER`
4. [ ] 编辑 PROJECT.md（大纲+调研索引+进度）
5. [ ] 多Agent并行调研 → 并行写作 → `./update.sh minor "初版"` 构建

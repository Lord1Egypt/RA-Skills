# project-intro-generator

一键遍历项目目录，生成项目介绍页，支持本地编辑和长图导出。

**在 OpenCode/Claude AI 中使用此 Skill**: [https://clawhub.ai/kunyashaw/project-intro-generator](https://clawhub.ai/kunyashaw/project-intro-generator)

## 演示视频

<div align="center">
  <a href="https://www.youtube.com/watch?v=6ZRcgbdZSXw">
    <img src="https://img.youtube.com/vi/6ZRcgbdZSXw/maxresdefault.jpg" alt="演示视频" width="600">
  </a>
</div>

## 快速开始

### 聊天中使用（推荐）

在聊天中直接发送项目绝对路径即可自动生成：

```
生成介绍页：/Users/kunyashaw/code/java/myproject
```

生成后会自动返回：
- HTML 文件路径
- PNG 长图路径

### 命令行使用

```bash
# 安装依赖（playwright 可选，用于长图导出）
npm install

# 本地目录，生成 HTML 和长图
node bin/cli.js --project /path/to/your/project --theme ocean

# 直接从已有 HTML 导出长图
node bin/cli.js --html /path/to/介绍.html --image-out /path/to/介绍.png
```

## 常用参数

- `--project`：要扫描的项目路径，默认为当前目录。
- `--html`：已有 HTML 文件路径，直接导出长图。
- `--out`：HTML 输出路径，默认 `<project>/介绍.html`。
- `--theme`：主题（`aurora` | `sunset` | `midnight` | `ocean` | `forest` | `mono`）。
- `--image-out`：长图输出路径，默认 `<project>/介绍.png`。

## 功能要点

- **README 优先**：存在有效 README 时直接渲染 Markdown；无 README 时显示编辑提示。
- **本地代码扫描**：目录结构、语言分布、依赖分析（支持 npm/pip/go.mod/Cargo.toml/composer.json/pom.xml/build.gradle 等）。
- **默认可编辑**：生成的 HTML 页面可直接编辑内容。
- **主题切换**：生成页内置主题切换。
- **长图导出**：基于 playwright 调用 Chromium 截图。
- **CLI 导出**：支持 `--html` 参数直接根据已有 HTML 导出长图。

## 生成规则

1. **README 优先**
   - 存在 README.md 且有效（字数≥30 或行数≥5）→ 直接渲染 README 内容。

2. **无 README 时**
   - 显示"暂无介绍，请点击上方按钮编辑添加..."，方便用户自行编辑。

3. **本地代码扫描**
   - 目录结构、关键大文件、语言分布
   - 依赖解析：package.json、requirements.txt、go.mod、Cargo.toml、composer.json、pom.xml、build.gradle

4. **文案约束**
   - 无数据显示"暂无"，禁止虚构功能

## 目录结构

```
introShow/
├─ bin/cli.js          # CLI 入口
├─ src/                # 核心逻辑
│  ├─ analyzer.js      # 代码扫描、依赖解析
│  ├─ git.js           # git 仓库克隆
│  ├─ image.js         # 长图导出（基于 playwright）
│  ├─ index.js         # 对外 API
│  ├─ template.js      # HTML 模板
│  └─ themes.js        # 主题配置
└─ package.json
```

## 注意

- 长图导出需本地安装 `playwright`（已列为可选依赖）。
- 默认忽略 `node_modules`、`dist`、`build`、`.git` 等目录，防止扫描过慢。
- 页面默认可编辑，点击"保存修改并导出图片"可下载编辑后的 HTML 并获取导出长图的 CLI 命令。

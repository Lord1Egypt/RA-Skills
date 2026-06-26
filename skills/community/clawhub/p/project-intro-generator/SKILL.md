---
name: "project-intro-generator"
version: "0.1.2"
displayName: "项目介绍页生成器"
description: "一键生成项目介绍页，支持本地编辑和长图导出。"
entryPoint:
  type: javascript
  path: "bin/cli.js"
triggers:
  keywords: ["生成介绍页", "项目介绍", "介绍html", "生成长图", "项目截图", "project intro", "readme"]
---

# project-intro-generator

一键生成项目介绍页，支持本地目录扫描、可编辑 HTML 和长图导出。

**GitHub**: [https://github.com/kunyashaw/createRepoIntro](https://github.com/kunyashaw/createRepoIntro)

**演示视频**: [https://www.youtube.com/watch?v=6ZRcgbdZSXw](https://www.youtube.com/watch?v=6ZRcgbdZSXw)

> 💡 通过 ClawHub 安装此 Skill：`project-intro-generator`

## 使用

### 聊天中使用

在聊天中直接发送项目绝对路径即可自动生成：

```
生成介绍页：/Users/kunyashaw/code/java/myproject
```

生成后会自动返回：
- HTML 文件路径
- PNG 长图路径

生成的 HTML 页面默认可编辑，点击「保存修改并导出图片」可下载编辑后的 HTML 并获取导出长图的 CLI 命令。

### 命令行使用

```bash
# 本地目录生成
node bin/cli.js --project <path> --theme ocean

# 从已有 HTML 导出长图
node bin/cli.js --html <html路径> --image-out <png路径>
```

### 参数说明

- `--project`：项目绝对路径（聊天中使用时直接发送路径即可）
- `--theme`：主题（ocean / forest / aurora / sunset / midnight / mono）
- `--html`：已有 HTML 文件路径，直接导出长图
- `--image-out`：长图输出路径

## 功能

- **README 优先**：存在有效 README 时直接渲染。
- **默认可编辑**：生成的 HTML 可直接编辑内容。
- **依赖解析**：支持 npm/pip/go.mod/Cargo.toml/composer.json/pom.xml/build.gradle。
- **主题切换**：aurora / sunset / midnight / ocean / forest / mono。
- **长图导出**：基于 playwright 截图。
- **CLI 导出**：支持 --html 参数直接导出已有 HTML 的长图。

## 生成规则

1. **扫描项目目录**：遍历代码文件，统计语言分布、目录结构、关键文件。
2. **依赖解析**：识别项目使用的包管理器，解析 dependencies。
3. **生成内容**：
   - 标题区域：项目名称
   - 项目概览：文件数，主要语言、目录结构
   - 项目介绍：优先显示 README 内容，无 README 时显示编辑提示
   - 依赖区块：显示项目依赖及用途说明
4. **页面特性**：
   - 默认可编辑（contenteditable）
   - 主题切换
   - 保存修改时自动生成带时间戳的 HTML 文件名
   - 导出长图时提供 CLI 命令

## 输出

- HTML 文件：可编辑的项目介绍页
- PNG 长图：基于 HTML 渲染的整页截图

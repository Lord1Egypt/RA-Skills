# GitToQuark

[![skills.sh](https://skills.sh/b/GitToQuark/GitToQuark)](https://skills.sh/GitToQuark/GitToQuark)

![中文](chinese.png)

<a href="README.md"><img src="https://img.shields.io/badge/English-English-blue" alt="English"></a>

用于将 GitHub 仓库内容保存到夸克网盘的 Agent Skill。

### 夸克网盘 CLI

本项目依赖的夸克网盘 CLI 官方仓库地址：https://github.com/quark-clouddrive/quarkclouddrive_offical

### 安装

```bash
npx skills add GitToQuark/GitToQuark
```

### 使用

安装后，GitToQuark 将在您的 agent 环境中可用。提供 GitHub 仓库 URL 或 `owner/repo` 格式，agent 将引导您完成下载和上传到夸克网盘的操作。

### 功能

- 自动地理定位检测，为国内用户提供代理回退
- GitHub 仓库源码下载（默认分支）
- GitHub Release 资源下载，支持操作系统检测
- 直接上传到夸克网盘
- 支持 Windows、macOS 和 Linux

### 反馈

- Issues: https://github.com/GitToQuark/GitToQuark/issues
- Discussions: https://github.com/GitToQuark/GitToQuark/discussions

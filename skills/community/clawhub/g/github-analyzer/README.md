# GitHub 项目分析助手

> 输入项目想法或 GitHub 链接，自动分析相关开源项目，生成结构化报告，支持代码包下载。

## ✨ 功能

- **意图搜索**：描述你的想法 → 自动搜索相关 GitHub 项目
- **直链分析**：粘贴 GitHub URL → 深度分析项目
- **结构化报告**：技术栈 / 优缺点 / 适用场景 / 综合评分
- **横向对比**：多项目对比表格
- **代码下载**：一键下载评分最高的前3名代码包

## 🚀 使用方式

### 作为 OpenClaw Skill 使用

安装到 OpenClaw 后，直接对话：

```
我想做一个在线文档协作工具，帮我找找 GitHub 上有没有相关开源项目
```

```
帮我分析这个项目：https://github.com/facebook/react
```

### 作为 CLI 工具使用

```bash
# 搜索相关项目
python3 scripts/search_github.py "online document collaboration" --limit 10

# 分析指定仓库
python3 scripts/analyze_repo.py "microsoft/vscode"
python3 scripts/analyze_repo.py "https://github.com/facebook/react" "https://github.com/vuejs/vue"

# 下载代码包
python3 scripts/download_repos.py "microsoft/vscode" "facebook/react"
```

## 📦 环境要求

- Python 3.8+
- 无需安装额外依赖（只用标准库）
- 可选：设置 `GITHUB_TOKEN` 环境变量以提高 API 限速（5000次/小时 vs 60次/小时）

```bash
export GITHUB_TOKEN=your_token_here
```

## 📊 报告示例

```
## microsoft/vscode

> Visual Studio Code

| 维度 | 详情 |
|------|------|
| ⭐ Stars | 158,000 |
| 🍴 Forks | 27,000 |
| 🔤 语言 | TypeScript |
| 📅 最近更新 | 2024-01-20 |

### 核心功能
- 跨平台代码编辑器
- 插件生态系统
- 内置 Git 支持
- 调试功能

### 优点 ✅
- 生态极其丰富，插件数量超10万
- 微软持续维护，更新频繁
- 开源免费，MIT 协议

### 缺点 ⚠️
- 内存占用较高
- 对大文件处理性能一般

### 综合评分：9.5 / 10
```

## 📝 作者

[antonia-sz](https://github.com/antonia-sz) · Powered by OpenClaw

## 📄 License

MIT

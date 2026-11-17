---
name: grok-build
description: "xAI's Grok Build: terminal AI coding agent CLI/TUI - install, build, configure, use"
---

# Grok Build (grok)

xAI 的终端 AI 编码 Agent。全屏 TUI，支持交互式编码、文件编辑、Shell 执行、网页搜索、长任务管理。也支持无头模式（脚本/CI）和编辑器嵌入（ACP 协议）。

Rust 编写，Apache 2.0 开源。

## 仓库信息

- GitHub: https://github.com/xai-org/grok-build
- 官网: https://x.ai/cli
- 文档: https://docs.x.ai/build/overview
- 许可证: Apache 2.0

## 安装

### 预编译二进制（推荐）

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
irm https://x.ai/cli/install.ps1 | iex
grok --version
```

### 源码编译

依赖：Rust 工具链 + DotSlash（cargo install dotslash）+ protoc

```bash
cargo run -p xai-grok-pager-bin
cargo build -p xai-grok-pager-bin --release
cargo check -p xai-grok-pager-bin
```

二进制产物 xai-grok-pager，官方安装为 grok。首次启动浏览器认证。

## 项目结构

```
crates/codegen/
  xai-grok-pager-bin/    组合根包
  xai-grok-pager/        TUI：滚动、提示、弹窗、渲染
  xai-grok-shell/        Agent 运行时 + 入口点
  xai-grok-tools/        工具实现（终端、文件编辑、搜索等）
  xai-grok-workspace/    文件系统、VCS、执行、检查点
crates/common/           共享基础 crate
bin/                     DotSlash 管理工具
third_party/             上游源码
```

## 核心功能

- 全屏 TUI 终端交互
- 代码库理解与文件编辑
- Shell 命令执行 + 网页搜索 + 长任务管理
- 无头模式（脚本/CI）
- 编辑器嵌入（ACP 协议）
- MCP 服务器 + Skills + Plugins + Hooks
- 沙箱 + 主题

## 注意事项

- 不接受外部贡献
- 与 xAI 内部 monorepo 周期性同步
- 首次使用需浏览器认证

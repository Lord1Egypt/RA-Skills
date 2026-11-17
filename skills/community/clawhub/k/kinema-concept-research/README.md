# Concept Research | 概念现状调研

调查一个概念是否已被实现、做成什么样子。通过多语言关键词、多引擎交叉验证、多维度搜索，系统化调研现有解决方案。

## 工作流

1. **概念澄清** — 多轮对话明确用户意图、核心功能、目标用户、差异化期望
2. **关键词拆解** — 核心词变体、技术栈词、场景词、组合词（中英文双语）
3. **广度搜索** — 逐批搜索关键词组，记录链接，标记相关性
4. **深度探索** — 挑选 3-5 个高相关性结果深入分析
5. **输出报告** — 生成摘要清单（链接、概述、基本思路、异同分析）

## 适用场景

- 验证创意是否已有实现
- 调研某领域的现有工具和方案
- 竞品分析和技术选型参考

## 使用方式

本 skill 支持 Codex、Claude Code 和 OpenClaw，安装后可通过对话触发：

```
有没有人做过 xxx？
调研一下 xxx 的现状
查一下 xxx 有哪些现有方案
```

依赖 [searxng-search-cli](https://github.com/KinemaClawWorkspace/searxng-search-cli) 作为搜索工具。

## Codex 安装

```powershell
codex plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace.git
codex plugin add kinema-concept-research@kinema-skills-marketplace
```

同时安装 `searxng-search-cli`，然后新开一个 Codex 对话。

## 项目输出结构

```
projects/research-{uuid}/
├── concepts/       # 概念定义
├── keywords/       # 关键词拆解
├── search/         # 搜索结果
│   ├── broad/      # 广度搜索
│   └── deep/       # 深度探索
├── repos/          # 克隆的仓库
├── papers/         # 下载的论文
└── report.md       # 最终报告
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)

# Kinema TDD Injector

一次性注入器，为目标仓库生成定制版 CLAUDE.md 记忆文件，植入 kinema 的 TDD 方法论。

## 核心特性

> **一句话**：对话式问卷 → 渲染定制 CLAUDE.md → 与既有文件智能融合 → 开箱即用的 TDD 规范

### 三阶测试体系

| 阶段 | 跑什么 | 何时跑 |
|------|--------|--------|
| **unit** | 单文件纯函数 / 类 | 每次保存 |
| **dev-integration** | 跨模块真实依赖（数据库 / 文件系统） | 提交前 |
| **testenv-integration** | 后端 API e2e（直连真实库）+ 前端 Playwright GUI e2e（连真实后端 + 真实库） | 连接配置由测试系统提供；本地许可时复杂任务完成自动触发，否则用户手动 |

### Commit Hook 强制网关

覆盖率不达标，commit 直接拦截。支持 `pre-commit` 本地 hook、CI 远端校验、双保险三种强制模式。

### 无痛升级

- **一键融合既有 CLAUDE.md** — 自动检测冲突章节，智能合并，非冲突内容原样保留
- **一键更新 KDD 版本** — 反解上次问卷答案作为默认值，回车即沿用，无需重新填写

### 规范全家桶

分层 conftest 架构 · 网络/IO 边界规范 · 测试路径三层命名 · Fixture 治理规则 · 覆盖率门槛配置 · Commit message 规范 · 前端 Playwright GUI e2e（连真实后端 + 真实库，配置归属测试系统）

## 安装

### 方法一：通过 Claude Code Marketplace

1. 添加 Marketplace：

```
/plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace
```

2. 安装 Skill：

```
/plugin install kinema-tdd-injector@kinema-skills-marketplace
```

1. 查看已安装的 Skill：

```
/plugin list
```

### 方法二：通过 ClawHub OpenClaw

```bash
openclaw skills install kinema-tdd-injector
```

## 适用场景

| 场景 | 说明 |
|------|------|
| 新仓库初始化 | 对话式问卷 → 一键生成完整 TDD 规范 |
| 已有仓库注入 | 智能检测既有 CLAUDE.md，冲突章节协商合并 |
| 版本升级 | 反解旧参数，回车沿用，一键更新到最新 KDD 规范 |

## 触发方式

本 skill 为 OpenClaw/Claude Code 技能，安装后可通过对话触发：

```
把测试规范注入到这个仓库
init tdd standard here
set up testing methodology
import kinema's test rules
```

首次使用需完成 [references/ONBOARDING.md](references/ONBOARDING.md) 环境配置（安装 jinja2）。

## 文件结构

```
kinema-tdd-injector/
├── .claude-plugin/
│   └── plugin.json       # Claude Code 插件清单
├── SKILL.md              # Skill 定义文件
├── assets/
│   └── claude_md.j2      # Jinja2 模板
├── scripts/
│   └── render.py         # 渲染脚本
├── evals/
│   └── evals.json        # 评估配置
└── references/
    └── ONBOARDING.md     # 首次配置引导
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)

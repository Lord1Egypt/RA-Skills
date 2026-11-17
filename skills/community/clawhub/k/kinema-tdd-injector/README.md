# Kinema TDD Injector

一次性 TDD 方法论注入器，同时支持 Claude Code、Codex 与 OpenClaw：

- Claude Code 生成或升级根级 `CLAUDE.md`
- Codex 生成或升级根级 `AGENTS.md`
- 两端共享同一套问卷、Jinja2 模板、冲突合并和升级反解规则

## 核心特性

> 对话式问卷 → 平台化渲染 → 与既有持久指令智能融合 → 开箱即用的 TDD 规范

### 三阶测试体系

| 阶段 | 跑什么 | 何时跑 |
|------|--------|--------|
| **unit** | 单文件纯函数 / 类 | 每次保存 |
| **dev-integration** | 跨模块真实依赖（数据库 / 文件系统） | 提交前 |
| **testenv-integration** | 后端 API e2e + 前端 Playwright GUI e2e | 按问卷配置自动或手动执行 |

此外包含分层 conftest、fixture 治理、网络/IO 边界、覆盖率门槛、Commit message 规范和可选
Python 编码规范。

## 安装

### Claude Code

```text
/plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace
/plugin install kinema-tdd-injector@kinema-skills-marketplace
```

### Codex

```bash
codex plugin marketplace add KinemaClawWorkspace/kinema-skills-marketplace
codex plugin add kinema-tdd-injector@kinema-skills-marketplace
```

安装或更新后开启一个新会话，让客户端加载新的 skill。

### OpenClaw

```bash
openclaw skills install kinema-tdd-injector
```

## 触发方式

```text
把测试规范注入到这个仓库
init tdd standard here
set up testing methodology
import kinema's test rules
升级已有的 Kinema TDD 规范
```

首次使用需读取 [references/ONBOARDING.md](references/ONBOARDING.md)。

## 双端实现

共享渲染器通过 target 选择输出平台：

```bash
uv run --with jinja2 python scripts/render.py --target claude --params params.json --out CLAUDE.md
uv run --with jinja2 python scripts/render.py --target codex --params params.json --out AGENTS.md
```

`--target` 默认为 `claude`，因此现有 Claude/OpenClaw 调用保持兼容。

## 文件结构

```text
kinema-tdd-injector/
├── .claude-plugin/plugin.json       # Claude Code 清单
├── .codex-plugin/plugin.json        # Codex 清单
├── skills/kinema-tdd-injector/      # Codex skill 适配层
├── SKILL.md                          # Claude/OpenClaw 完整工作流
├── assets/claude_md.j2               # 双端共享模板
├── scripts/render.py                 # --target claude|codex
├── evals/evals.json
└── references/ONBOARDING.md
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)

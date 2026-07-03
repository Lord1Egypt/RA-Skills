# 🛡️ Preflight Workflow

> **动手前强制自检** — Stop before you break.

Free safety workflow: four checks (search / rollback / test / scope) before every agent or CLI operation. If even one check fails, it stops and tells you why.

---

## 🇨🇳 中文简介

Preflight Workflow 是一个轻量级安全自检工具，专为 AI Agent 和开发者设计。每次动手前强制回答四个问题：

1. ✅ **搜过吗？** — 有没有查过前人经验？
2. ✅ **能回滚吗？** — 失败了怎么复原？
3. ✅ **验证过吗？** — 方案在小范围跑过没？
4. ✅ **范围清楚吗？** — 改了哪里、影响谁、多久能恢复？

**四条全过才能动手，一条不过就得停。** 就这么简单。

### 适合谁用
- 用 OpenClaw / Claude Code / Hermes / Cursor 等 AI Agent 的开发者
- 经常手滑、忘备份、反复踩坑的人
- 团队需要统一安全流程的负责人

### 文件清单

| 文件 | 作用 |
|------|------|
| `SKILL.md` | Agent 可加载的技能文档 |
| `preflight.sh` | 命令行自检脚本（交互式问答） |
| `install.sh` | 一键安装脚本 |
| `LEARNINGS.md` | 事后复盘模板 |
| `README.md` | 本说明文件 |

### 使用方式

**方式一：Agent 加载 Skill**
```
加载 preflight-workflow skill，说"先跑 preflight"
```

**方式二：命令行**
```bash
chmod +x preflight.sh
./preflight.sh "要执行的任务描述"
```

**方式三：一键安装**
```bash
curl -sL https://your-domain.com/preflight-workflow.tar.gz | tar xz
cd preflight-workflow && ./install.sh
```

---

## 🇺🇸 English

A zero-cost safety workflow that forces four mandatory checks before every agent or human operation:

1. ✅ **Searched?** — Checked existing solutions and prior experience
2. ✅ **Rollback?** — Can you undo the operation if it fails?
3. ✅ **Tested?** — Validated on a small scale first?
4. ✅ **Scope?** — Know what you're changing and who it affects?

### Users

- OpenClaw / Claude Code / Hermes / Cursor AI agent users
- Individuals who often skip checks and break things
- Teams needing a standardized safety workflow

### How to Use

**Agent:** Load the skill and say "run preflight"

**CLI:**
```bash
./preflight.sh "task description"
```

**Install:**
```bash
chmod +x install.sh && ./install.sh
```

---

## 📦 Package Contents

```
preflight-workflow/
├── SKILL.md          → Agent skill (loadable by any SKILL.md-compatible agent)
├── preflight.sh      → Interactive CLI checklist
├── install.sh        → One-command installer
├── LEARNINGS.md      → Post-mortem template
└── README.md         → This file
```

## License

MIT-0 — Free to use, modify, and redistribute.
Published on [ClawHub](https://clawhub.ai).

---

*Made with 🏮 by 隅舍*

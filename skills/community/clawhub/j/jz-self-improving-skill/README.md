# Self-Improving Skill

让你的 writing style skill 自动从人类修改中学习。

**兼容 Claude Code + OpenClaw (ClawHub)**。`observe.py` 零依赖纯 Python。

## 原理

```
AI 写初稿 → 人类改到满意 → diff 两版 → 提取规则 → 更新 SKILL.md → 下次更准
```

只要两个数据点：**original**（AI 第一版）和 **final**（人类最终版）。中间改了多少轮不管。

## 安装

```bash
# Claude Code
cp -r self-improving-skill ~/.claude/skills/

# OpenClaw / ClawHub
npx clawhub@latest install self-improving-skill
# 或手动: cp -r self-improving-skill ~/clawd/skills/
```

## 快速开始

```bash
# 1. AI 写完内容后，记录原稿
python3 scripts/observe.py record-original draft.md --skill my-writing-style

# 2. 人类改完确认后，记录最终版
python3 scripts/observe.py record-final final.md --match <hash> --skill my-writing-style

# 3. 提取规则（需要 LLM CLI: claude / llm / 自定义）
python3 scripts/improve.py auto --skill ~/path/to/my-writing-style/
```

## 命令

### observe.py（零依赖）

| 命令 | 功能 |
|------|------|
| `record-original <file>` | 记录 AI 原稿 |
| `record-final <file> --match <hash>` | 记录最终版 |
| `pending` | 查看待配对 |
| `stats` | 统计 |

### improve.py（需要 LLM CLI）

| 命令 | 功能 |
|------|------|
| `extract [--days 7]` | 提取改进建议 |
| `auto` | 自动提取 + 应用 P0（cron 用）|
| `show` | 查看提案 |
| `apply <id>` | 应用提案 |
| `rollback` | 回滚 |

## LLM 支持

`improve.py` 自动检测可用 CLI：
- `claude` (Claude Code) — 优先
- `llm` (pip install llm) — 通用
- `IMPROVE_LLM_CMD` 环境变量 — 自定义

`observe.py` 不依赖任何 LLM。

## 安全

- 每次 apply 前自动备份 SKILL.md
- `auto` 模式只应用高置信度 (P0) 规则
- 一键 rollback

## 适用场景

不限于写作。任何 "AI 生成 → 人类修改" 的循环：
- Writing style（推文、文章）
- Code review rules
- Email drafting
- Translation

## License

MIT

# Writing Style Skill

可复用的写作风格 Skill 模板。**内置自动学习** — 从你的修改中自动提取规则，SKILL.md 越用越准。

兼容 **Claude Code** + **OpenClaw (ClawHub)**。

## 原理

```
AI 用 SKILL.md 写初稿 → 你改到满意 → diff 两版 → 提取规则 → 更新 SKILL.md → 下次更准
```

只要两个数据点：**original**（AI 第一版）和 **final**（你最终版）。中间改了多少轮不管。

## 安装

```bash
# Claude Code
git clone https://github.com/jzOcb/writing-style-skill.git
cp -r writing-style-skill ~/.claude/skills/my-writing-style

# OpenClaw / ClawHub
npx clawhub@latest install jz-writing-style-skill
```

## 快速开始

1. **改 SKILL.md** — 把模板里的风格规则改成你自己的（或留空，让自动学习帮你填）
2. **让 AI 用这个 skill 写内容**
3. **你改到满意**
4. 记录：
```bash
python3 scripts/observe.py record-original draft.md
# ... 你修改 ...
python3 scripts/observe.py record-final final.md
```
5. 提取规则：
```bash
python3 scripts/improve.py auto --skill .
```

## 文件结构

```
writing-style-skill/
├── SKILL.md              # 你的写作风格（模板，改成你的）
├── README.md             # 本文件
└── scripts/
    ├── observe.py        # 记录 original / final（零依赖）
    └── improve.py        # 提取 / 应用 / 回滚（需要 LLM CLI）
```

## 自动学习怎么工作

- `observe.py` 记录 AI 原稿和你的最终版
- `improve.py` 用 LLM 分析 diff，提取写作规则
- 规则按置信度分 P0/P1/P2，P0 自动应用
- 每次更新前自动备份，一键回滚

## LLM 支持

`improve.py` 自动检测：
- `claude` (Claude Code) — 优先
- `llm` (pip install llm) — 通用
- `IMPROVE_LLM_CMD` 环境变量 — 自定义

`observe.py` 零依赖纯 Python。

## License

MIT

# 目录结构

使用本 skill 前，确保 Agent 的 workspace 中存在以下目录结构：

```
<workspace>/
├── AGENTS.md
├── SOUL.md
├── TOOLS.md
├── MEMORY.md
├── memory/
│   └── YYYY-MM-DD.md
└── learning/
    ├── LEARNING.md
    ├── notes/
    │   └── YYYY-MM-DD.md
    └── reviews/
        ├── post-learning/     # 模式 A：学后复盘
        │   └── YYYY-MM-DD.md
        ├── weekly/            # 模式 B：周内化报告
        │   └── YYYY-Www.md
        └── application/       # 模式 C：应用检查
            └── YYYY-MM-DD.md
```

## 初始化

如果 `learning/reviews/` 不存在，执行：

```bash
mkdir -p <workspace>/learning/reviews/{post-learning,weekly,application}
```

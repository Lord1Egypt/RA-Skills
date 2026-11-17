# hekouwang-doctor-suite · 体检器三件套

> 竞品多是单点；这套把「项目配置 → 技能包 → 本机环境」串成一条验收链。

```
hekouwang-doctor-suite（概念）
├── md-doctor      → AGENTS.md / CLAUDE.md（运行时配置）
├── skill-doctor   → SKILL.md（Agent 技能包）
└── env-doctor     → 磁盘 / 版本管理器 / AI 宿主目录
```

## 一键跑

```bash
bash scripts/run-all-doctors.sh /path/to/your-project
```

（脚本在 `hekouwang-claude-md-doctor-skill`；`skill-doctor` / `env-doctor` 仓内各有一份相同副本。）

## 建议顺序

1. **md-doctor** — 根配置是否「路由器」而非「图书馆」
2. **skill-doctor** — `.agents/skills/` 下各 skill 是否按需加载
3. **env-doctor** — 本机是否留着已换掉的 nvm / 膨胀的 AI 缓存

## 免费 vs 付费

| | 免费（开源） | 付费增值 |
|---|---|---|
| 机检 | `check.py` / `scan.sh` 文本报告 + JSON | 品牌可视化报告卡（评分弧 + 等级带） |
| CI | 退出码卡关 | — |
| 联系 | GitHub Issue / PR | ClawHub **@huiyonghkw** |

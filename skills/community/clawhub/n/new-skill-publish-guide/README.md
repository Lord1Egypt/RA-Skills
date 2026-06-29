# ClawHub 全新技能发布攻略

## 快速导航

1. [制作技能](#第一阶段制作技能) — SKILL.md + 核心代码
2. [发布到 ClawHub](#第二阶段发布到-clawhub) — sync 或 publish
3. [存档到 IMA](#第三阶段存档到-ima) — 新建笔记
4. [通知 main](#第四阶段通知-main) — sessions_send

## 快速使用

```bash
# 1. 确认环境
clawhub whoami

# 2. 创建技能目录并写入文件

# 3. 发布
cd D:\openclaw-data\workspace\skills
clawhub sync --all --bump minor --changelog "初始版本"

# 4. 存档到 IMA（用 ima_api.cjs）

# 5. 通知 main
```

## 文件结构

- `SKILL.md` — 完整攻略正文
- `README.md` — 本文件

## 依赖

- `clawhub` CLI（npm i -g clawhub）
- IMA 凭证（已配置在 `D:\openclaw-data\workspace\skills\skills\ima-skills\ima_api.cjs`）
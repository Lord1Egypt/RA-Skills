---
name: BadSkill_Example
---

# Bad Skill

这是一个演示「不合格 skill」的夹具，故意踩坑：

- name 用了大写 + 下划线（应 kebab-case）。
- **缺 description**——模型无从判断何时加载本 skill（机检会判 FAIL，退出码 1）。
- 硬编码了绝对路径 /Users/someone/.claude/skills/x/assets/font.woff2（换台机器就废）。

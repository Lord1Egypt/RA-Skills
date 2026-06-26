# 班主任.Skill 安装说明

## 安装到 Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/YZDame/headteacher-skill .claude/skills/headteacher-workbench
```

全局安装：

```bash
git clone https://github.com/YZDame/headteacher-skill ~/.claude/skills/headteacher-workbench
```

## 安装到 OpenClaw

```bash
git clone https://github.com/YZDame/headteacher-skill ~/.openclaw/workspace/skills/headteacher-workbench
```

如果你准备在 OpenClaw 中使用飞书多维表格，额外安装 OpenClaw 官方飞书插件：

- 插件名：`openclaw-lark`
- Skill 在 OpenClaw 中应优先检测并复用这个官方插件
- 安装好插件后，应通过插件提供的飞书 Base API 能力完成多维表格搭建，而不是要求用户再走 `lark-cli`

## Python 依赖

```bash
pip3 install -r requirements.txt
```

## 飞书后端前置条件

若你打算使用飞书多维表格作为工作台后端：

1. 如果你是通过 OpenClaw 接入：
   - 优先安装官方飞书插件 `openclaw-lark`
   - 由 Skill 检测 OpenClaw 运行环境
   - 通过插件的飞书 API 能力完成 Base 初始化
2. 如果你是通过 Codex、Claude Code 或其他本地 Agent 接入：
   - 安装 `lark-cli`
   - 在首次运行 Skill 时完成 `lark-cli config init --new`
   - 让 Skill 使用 `tools/setup_doctor.py` 和 `tools/feishu_bootstrap.py` 完成检查与初始化

Skill 的默认建议顺序是：

1. 先做环境检查
2. 再选后端
3. 最后初始化工作台

## 其他后端

### Notion

第一版只提供结构映射和最小初始化说明，不承诺完整自动写入链路。

### Obsidian

第一版只提供目录骨架、模板和数据规范说明，不承诺完整结构化数据库体验。

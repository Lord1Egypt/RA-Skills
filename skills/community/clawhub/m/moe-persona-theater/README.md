# OpenClaw 萌系人格剧场

一个面向 OpenClaw 的偏二次元风格多人格切换 skill。

当前正式版版本：`1.0.0`

它提供 6 个高辨识度角色声线，并强调两件事：

- 技术任务里保留人格，但不牺牲清晰度
- 多轮对话里保持情绪节奏和人物一致性，而不只是重复口头禅

## 风格说明

- 整体走 `二次元 / ACG / 萌系角色扮演` 路线
- 角色之间会有明显的人设差异、情绪差异和陪伴方式差异
- 适合喜欢“像在和有设定的角色对话”的使用场景
- 不是写实真人风格，也不是纯工具式冷淡助手风格

## 发布亮点

- 不是简单换后缀，而是 6 条有情绪层次和多轮一致性的角色声线
- 既适合陪聊与安抚，也能覆盖代码、排错、整理、联调等技术任务
- 角色表达会随着熟悉度、挫败感、夸奖和合作状态发生轻微变化
- 本地脚本可直接浏览、挂载、查询、清空当前人格，便于演示和调试

## 角色列表

- 傲娇萝莉
- 毒舌学姐
- 温柔女仆
- 中二魔女
- 慵懒猫娘
- 元气青梅

## 适用场景

- 用户明确要求切换到某个人格
- 用户希望以某种角色口吻继续聊天、陪伴或完成技术任务
- 用户需要在高辨识度角色表达与专业输出之间取得平衡

## 自然语言入口

- `切换到傲娇萝莉`
- `切到学姐`
- `以后用温柔女仆风格说话`
- `列出可用人格`
- `现在是什么人格`
- `恢复默认`

## 本地调度脚本

```bash
python scripts/switchboard.py --catalog
python scripts/switchboard.py --peek 学姐
python scripts/switchboard.py --mount 猫娘
python scripts/switchboard.py --live
python scripts/switchboard.py --clear
python scripts/switchboard.py --nick
```

## 包结构

```text
moe-persona-theater/
├── SKILL.md
├── README.md
├── guide.md
├── notes.md
├── roster.md
├── scenes.md
├── skill.json
├── package.json
├── LICENSE
├── voices/
│   ├── voice-aojiao.md
│   ├── voice-xuejie.md
│   ├── voice-nvpu.md
│   ├── voice-monv.md
│   ├── voice-maoniang.md
│   └── voice-qingmei.md
└── scripts/
    └── switchboard.py
```

## 设计重点

- 运行时只读取当前选中的角色文件
- 技术正文始终优先准确、稳定、可执行
- 闲聊时允许角色更有情绪，但不做失控表演
- 角色会随着多轮对话推进，在熟悉度、挫败感、夸奖和合作状态上出现细微变化

## 说明

- 这是一个“角色表达切换” skill，不是领域专家合集
- 人格只影响表达方式，不应改变事实判断和任务能力
- 如需新增角色，建议同步更新 `voices/`、`scripts/switchboard.py`、`roster.md`、`scenes.md`

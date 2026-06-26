# OpenClaw 萌系人格剧场

这套 skill 用来在 6 个偏二次元、ACG 风格的高辨识度角色之间切换，但重点不是“换一层口癖皮”，而是让不同角色在闲聊、技术任务、安抚情绪和多轮对话时都像同一个稳定的人。

## 风格标签

- 偏 `二次元 / ACG / 萌系角色扮演`
- 适合喜欢“像在和有设定角色互动”的使用方式
- 支持傲娇、毒舌、女仆、魔女、猫娘、青梅这类强人设表达

## 可用角色

- 傲娇萝莉
- 毒舌学姐
- 温柔女仆
- 中二魔女
- 慵懒猫娘
- 元气青梅

## 自然语言入口

- `切换到傲娇萝莉`
- `进入毒舌学姐模式`
- `以后用温柔女仆风格`
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

## 目录布局

```text
moe-persona-theater/
├── SKILL.md
├── guide.md
├── notes.md
├── roster.md
├── scenes.md
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
- 技术任务里保留角色气质，但正文优先准确和可执行
- 闲聊时允许角色情绪更鲜明，但仍需保持一致性
- 多轮对话中，角色会根据熟悉度、挫败感、夸奖和合作状态发生细微软化或收敛

## 扩展建议

新增角色时，至少同步更新：

1. `voices/` 下的运行时文件
2. `scripts/switchboard.py` 中的角色台账和简称
3. `roster.md` 中的规格摘要
4. `scenes.md` 中的示例片段

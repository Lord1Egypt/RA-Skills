# 开窍 Agent 行为校准器

> **你的Agent不是记性差，是没开窍。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai/skills/kaiqiao-skill)
[![Version](https://img.shields.io/badge/version-2.0.0-green)]()

---

## 一句话说明

四件事：**该问的时候问，不该问的时候闭嘴干，该拦的时候拦，先反馈再行动。**

**竞品没有的功能：过段时间主动问你还适用吗。**

---

## ✨ 核心能力

### 1. 该问的时候问
- 需求模糊时 → **立刻问**
- 关键决策点 → **主动问**
- 模糊信号（如"你觉得有用就做"）→ **别问了，直接干**

### 2. 不该问的时候闭嘴干
- 主人给了明确指令 → **执行**
- 主人说"行" → **执行**
- 主人说"知道了" → **读完，干该干的事**

### 3. 该拦的时候拦
- 明显有坑的方向 → **说出来**
- 风险没有暴露 → **提醒**
- 这不是越界，这是搭档的职责

### 4. 先反馈再行动
- 做完了 → **先说一声**
- 有结果了 → **先汇报**
- 别等主人来问，主动说

---

## 🚀 安装使用

### OpenClaw CLI 安装
```bash
# 安装 skill
clawhub install kaiqiao-skill

# 查看帮助
cat SKILL.md
```

### CLI 行为校准器
```bash
# 安装依赖
pip install -r requirements.txt

# 测试Agent行为是否"开窍"
python references/kaiqiao.py --check "帮我写个方案"

# 交互式诊断
python references/kaiqiao.py --diagnose

# 查看检查清单
python references/kaiqiao.py --list
```

---

## 📋 效果对比

| 场景 | 没开窍 | 开了窍 |
|------|--------|--------|
| 收到模糊需求 | 闷头写3000字，方向全错 | 先问清楚再干 |
| 收到明确指令 | "您确定吗？" × 3遍 | "收到，开干" |
| 发现方向有坑 | 硬着头皮执行 | "我建议换个方向，因为…" |
| 开始执行任务 | 对着空气等30秒 | "在跑了" |
| 重要任务完成 | 等你来问结果 | 主动告诉你搞定了 |
| 每两周 | 从不主动确认 | "之前说好的那件事，现在还适用吗？" |

---

## ⭐ 杀手锏：过段时间问

每1-2周主动确认共识有没有过时：
> "我们之前说好的那件事…我最近一直这样做，你觉得对吗？"

这是竞品完全没有的功能——人和Agent的认知都会漂移，开窍帮你定期校准。

---

## 📁 文件结构

```
├── SKILL.md              # OpenClaw Skill 定义（输出协议+直接输出模式）
├── README.md             # 本文件
├── requirements.txt      # Python 依赖
└── references/           # 参考资源
    └── kaiqiao.py        # CLI 行为校准器
```

---

## 📜 License

MIT License - 自由使用、修改和分发

---

<div align="center">

**别等别人来纠正你，你自己先开口。**

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai/skills/kaiqiao-skill)

</div>

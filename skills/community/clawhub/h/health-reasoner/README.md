# Health Reasoner 🫀

日常状态健康推理引擎。输入你的睡眠、饮食、运动、压力等数据，输出综合健康评分、风险评估和个性化改善建议。**纯 Python 标准库，零外部依赖。**

## 特性

- **隐私安全** — 所有数据本地处理，不上传云端
- **可解释** — 每条建议都有规则 ID，知道为什么
- **结构化输出** — JSON 格式，可直接用于其他系统
- **趋势追踪** — 连续输入查看健康变化趋势
- **无依赖** — 核心推理模块 `pip install` 都不需要

## 快速开始

```bash
git clone https://github.com/你的用户名/health-reasoner.git
cd health-reasoner

# 交互模式
python health_reasoner.py --cli

# JSON 输入模式
python health_reasoner.py --input '{"age":28,"sleep_hours":6.5,"sleep_quality":"fair","diet_type":"high_fat","exercise_frequency":"weekly","stress_level":"high"}'

# 自检
python health_reasoner.py --test

# API 服务（需要 Flask）
python health_reasoner.py --api
```

## 示例输出

```json
{
  "score": 62,
  "risk_level": "medium",
  "suggestions": [
    {"priority": 1, "category": "sleep", "rule_id": "SLEEP-001", "message": "建议将睡眠延长至7-8小时，有助于降低心血管疾病风险"},
    {"priority": 2, "category": "diet", "rule_id": "DIET-003", "message": "减少高脂食物摄入，增加蔬菜水果比例"}
  ],
  "risk_factors": ["睡眠不足", "高脂饮食"],
  "details": {
    "sleep_score": 55,
    "diet_score": 40,
    "exercise_score": 60,
    "stress_score": 50,
    "substance_score": 100
  }
}
```

## 文档

- [SKILL.md](SKILL.md) — ClawHub 技能说明
- [API_SPEC.md](API_SPEC.md) — API 规范与错误码
- [USE_GUIDE.md](USE_GUIDE.md) — 详细使用指南
- [DESIGN.md](references/DESIGN.md) — 设计文档

## 项目文件结构

```
health-reasoner/
├── health_reasoner.py      ← 核心引擎 (~23KB)
├── SKILL.md                ← ClawHub 技能描述
├── API_SPEC.md             ← API 规范
├── USE_GUIDE.md            ← 使用指南
├── LICENSE                 ← MIT 许可证
├── README.md               ← 本文件
├── references/
│   └── DESIGN.md           ← 设计文档
└── scripts/
    ├── setup.sh            ← Linux/macOS 安装脚本
    └── setup.bat           ← Windows 安装脚本
```

## License

MIT

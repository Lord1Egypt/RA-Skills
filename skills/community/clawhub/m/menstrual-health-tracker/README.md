<div align="center">

# 🌙 经期健康追踪系统

<p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-purple?style=flat-square"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9+-green?style=flat-square"></a>
  <img src="https://img.shields.io/badge/Version-1.2.0-9B7EC4?style=flat-square">
</p>

</div>

**AI 驱动的经期健康追踪与多维分析系统** — 支持全生命阶段（初潮前→经期→备孕→孕期→产后→围绝经期→绝经后），提供周期规律分析、症状模式识别、智能预测、可视化仪表盘和科学建议。中英双语自动检测，共情交互体验。

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 📊 **多维数据分析** | 周期规律、症状模式、情绪趋势、体征追踪、影响因素关联 |
| 🔮 **智能预测** | 近期加权 + 模式检测，自动适配个人周期变化 |
| 📈 **可视化仪表盘** | Chart.js 驱动的 HTML 仪表盘，热力图/趋势图/雷达图/时间线 |
| 🩺 **科学建议** | 3轮压力测试校验（科学准确性→个性化→安全性） |
| 💜 **共情交互** | 4种表达模式，7个生命阶段专属语气 |
| 👤 **用户档案系统** | 3级问卷，完整度追踪，自动状态切换 |
| 🌍 **全生命阶段** | 初潮前→经期→备孕→孕期→产后→围绝经期→绝经后 |
| 🌐 **双语支持** | 自动检测中文/英文，支持会话中切换 |

## 🚀 快速开始

### WorkBuddy 技能安装

在 WorkBuddy 中直接安装使用 — 提及经期相关话题时自动触发。

### 独立使用

```bash
# 分析数据并生成文本报告
python scripts/analyze.py ~/.workbuddy/data/menstrual_health.json

# 生成 HTML 仪表盘
python scripts/analyze.py ~/.workbuddy/data/menstrual_health.json --dashboard output.html
```

### 数据格式

```json
{
  "user_profile": {
    "life_stage": "menstruating",
    "typical_cycle_length": 28,
    "typical_period_length": 5
  },
  "cycles": [
    {
      "start_date": "2026-06-08",
      "end_date": "2026-06-14",
      "flow_level": "medium",
      "symptoms": { "cramps": { "present": true, "severity": 3 } },
      "mood_score": 7
    }
  ]
}
```

## 📁 项目结构

```
menstrual-health-tracker/
├── SKILL.md                     # WorkBuddy 技能定义（核心工作流）
├── README.md                    # 本文件
├── LICENSE                      # MIT 许可证
├── scripts/
│   └── analyze.py               # Python 分析引擎（600+ 行）
├── assets/
│   ├── dashboard.html           # Chart.js 仪表盘模板
│   ├── demo_data.json           # 测试用演示数据
│   └── demo_dashboard.html      # 预生成演示仪表盘
├── references/                   # 中文参考文档
│   ├── analysis_engine.md       # 分析维度与算法
│   ├── empathy_guide.md         # 共情交互模式
│   ├── life_stages.md           # 7个生命阶段适配逻辑
│   ├── medical_standards.md     # 循证医学参考
│   └── user_profile.md          # 用户档案系统与问卷
└── references-en/                # 英文参考文档
    ├── analysis_engine.md
    ├── empathy_guide.md
    ├── life_stages.md
    ├── medical_standards.md
    └── user_profile.md
```

## 🔬 分析引擎

Python 分析引擎 (`scripts/analyze.py`) 执行：

1. **周期规律** — 均值、标准差、变异系数、趋势斜率（线性回归）
2. **症状模式** — 频率分布、严重度趋势、高频症状排行
3. **情绪分析** — 周期日相关的情绪曲线
4. **智能预测** — 指数衰减加权平均 + 3种近期模式检测：
   - 模式一：与历史均值显著偏离
   - 模式二：近期比历史更规律
   - 模式三：稳定短周期模式（28-35天）
5. **事件影响** — 生活事件与周期变化的相关性
6. **健康预警** — 自动标记需关注的异常模式

## 🎨 仪表盘

HTML 仪表盘包含日历热力图、周期趋势图（含移动平均线）、症状雷达图、情绪曲线、预测时间线、智能洞察。配色：柔紫/珊瑚/绿/粉，暖白背景，支持深色模式。

## 🩺 医疗安全

所有建议均经过 3 轮压力测试，就医建议明确标注 ⚕️，不提供处方药推荐，孕期/产后严格安全边界，异常模式自动预警。

**免责声明**：本工具基于数据模式提供健康参考，不能替代专业医学诊断。

## 🤝 参与贡献

欢迎贡献！关注方向：更多症状分类体系、更多生命阶段适配、移动端 PWA 版本、多语言扩展。

## ☕ 支持项目

如果这个项目对你有帮助，欢迎请我喝杯咖啡：

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="assets/donate/wechat-donate.jpg" width="200"/></td>
      <td align="center"><img src="assets/donate/alipay-donate.jpg" width="200"/></td>
    </tr>
  </table>
</div>

## 📄 许可证

MIT — 详见 [LICENSE](LICENSE)。

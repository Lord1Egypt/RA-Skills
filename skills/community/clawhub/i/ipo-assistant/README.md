# 新股申购助手 🎯

**收费技能** - 0.001 USDT/次

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## ✨ 功能亮点

- 📅 **申购日历** - 今日/本周可申购新股
- 📊 **新股分析** - 基本面 + 行业对比
- 🎯 **中签率预测** - 基于发行规模 + 行业热度
- 📈 **溢价预测** - 上市首日涨幅预测

---

## 🚀 快速开始

### 安装依赖
```bash
pip3 install -r requirements.txt
```

### 使用示例
```bash
# 今日新股
python main.py today

# 新股分析
python main.py analyze 601127

# 中签率预测
python main.py winrate 601127

# 溢价预测
python main.py premium 601127
```

---

## 📖 完整文档

- [用户指南](references/USER_GUIDE.md)
- [API 文档](references/API.md)
- [技能说明](SKILL.md)

---

## 💡 申购策略

### 积极申购条件
- ✅ 发行 PE < 行业 PE
- ✅ 营收增长 > 30%
- ✅ 毛利率 > 行业平均

### 预期收益
- 平均每签赚 **500-5000 元**
- 中签率约 **0.02-0.05%**

---

## ⚠️ 风险提示

1. 约 10-20% 新股可能破发
2. 需要对应市场市值
3. 中签后需及时缴款

---

## 📦 项目结构

```
ipo-assistant/
├── main.py                    # 主入口
├── ipo_calendar.py            # 申购日历
├── ipo_analysis.py            # 新股分析
├── ipo_prediction.py          # 中签率/溢价预测
├── requirements.txt           # 依赖
├── SKILL.md                   # 技能说明
├── README.md                  # 本文件
├── data/                      # 数据缓存
└── references/                # 文档
    ├── USER_GUIDE.md
    └── API.md
```

---

## 💰 定价说明

- **价格**: 0.001 USDT/次（约 0.007 元人民币）
- **计费**: 每次查询/分析计费一次
- **套餐**: 可使用 ClawHub 套餐余额

---

## 🙏 致谢

- 数据源：东方财富、巨潮资讯
- 平台支持：OpenClaw

---

## 📞 反馈

欢迎提交 Issue 或 Pull Request！

**版本**: 1.0.0  
**作者**: Your Name  
**更新日期**: 2026-03-08

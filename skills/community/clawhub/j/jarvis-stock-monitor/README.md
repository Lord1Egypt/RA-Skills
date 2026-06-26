# Stock Monitor Pro - 全功能智能股票监控预警系统

**作者**: Jarvis-OC  
**版本**: 1.0.0  
**许可**: MIT-0

---

## 🎯 功能亮点

### 七大预警规则
1. ✅ **成本百分比预警** - 基于持仓成本的盈利/亏损提醒
2. ✅ **日内涨跌幅预警** - 个股/ETF/黄金差异化阈值
3. ✅ **成交量异动监控** - 放量/缩量自动识别
4. ✅ **均线金叉死叉** - MA5/MA10/MA20 多头/空头排列
5. ✅ **RSI 超买超卖** - RSI>70 超买/RSI<30 超卖
6. ✅ **跳空缺口检测** - 向上/向下跳空>1%
7. ✅ **动态止盈提醒** - 盈利回撤保护

### 分级预警
- 🚨 **紧急级**: 多条件共振
- ⚠️ **警告级**: 2 个条件触发
- 📢 **提醒级**: 单一条件触发

---

## 💰 定价

| 功能 | 免费 | 付费 (SkillPay) |
|------|------|----------------|
| 基础价格监控 | ✅ | - |
| 成本百分比预警 | ✅ | - |
| 日内涨跌幅预警 | ✅ | - |
| 技术指标预警 | - | 🔒 |
| 成交量异动 | - | 🔒 |
| 智能分析引擎 | - | 🔒 |

**付费方式**:
- 单次查询：¥0.01/次
- 包月订阅：¥99/月

---

## 🚀 快速开始

### 1. 安装
```bash
clawhub install stock-monitor-pro
```

### 2. 配置持仓
编辑 `scripts/config.py`，添加你的持仓：

```python
WATCHLIST = [
    {
        "code": "600362",
        "name": "江西铜业",
        "market": "sh",
        "type": "individual",
        "cost": 57.00,
        "alerts": {
            "cost_pct_above": 15.0,
            "cost_pct_below": -12.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True
        }
    }
]
```

### 3. 启动监控
```bash
cd scripts
./control.sh start
```

### 4. 查看状态
```bash
./control.sh status  # 运行状态
./control.sh log     # 查看日志
./control.sh stop    # 停止监控
```

---

## 📊 监控配置示例

### 个股配置
```python
{
    "code": "600362",
    "name": "江西铜业",
    "type": "individual",  # 个股
    "market": "sh",
    "cost": 57.00,
    "alerts": {
        "cost_pct_above": 15.0,
        "cost_pct_below": -12.0,
        "change_pct_above": 4.0,
        "change_pct_below": -4.0,
        "volume_surge": 2.0,
        "ma_monitor": True,
        "rsi_monitor": True,
        "gap_monitor": True,
        "trailing_stop": True
    }
}
```

### ETF 配置
```python
{
    "code": "159892",
    "name": "恒生医疗",
    "type": "etf",
    "market": "sz",
    "cost": 0.80,
    "alerts": {
        "cost_pct_above": 15.0,
        "cost_pct_below": -15.0,
        "change_pct_above": 2.0,  # ETF 波动小，阈值更低
        "change_pct_below": -2.0,
        "volume_surge": 1.8
    }
}
```

### 伦敦金配置
```python
{
    "code": "XAU",
    "name": "伦敦金 (人民币/克)",
    "type": "gold",
    "market": "fx",
    "cost": 4650.0,
    "alerts": {
        "cost_pct_above": 10.0,
        "cost_pct_below": -8.0,
        "change_pct_above": 2.5,
        "change_pct_below": -2.5
        # 黄金不监控成交量
    }
}
```

---

## ⚡ 智能频率

| 时间段 | 频率 | 说明 |
|--------|------|------|
| 9:30-11:30 | 5 分钟 | 上午交易时间 |
| 11:30-13:00 | 10 分钟 | 午休时间 |
| 13:00-15:00 | 5 分钟 | 下午交易时间 |
| 15:00-24:00 | 30 分钟 | 收盘后 |
| 0:00-9:30 | 60 分钟 | 凌晨 (仅伦敦金) |

---

## 🔔 预警示例

### 紧急级预警
```
🚨【紧急】🔴 江西铜业 (600362)
━━━━━━━━━━━━━━━━━━━━
💰 当前价格：¥65.50 (+15.0%)
📊 持仓成本：¥57.00 | 盈亏：🔴+14.9%

🎯 触发预警 (3 项):
  • 🎯 盈利 15% (目标价 ¥65.55)
  • 🌟 均线金叉 (MA5 上穿 MA10)
  • 📊 放量 2.5 倍

💡 Kimi 建议:
🚀 多条件共振，趋势强劲，可继续持有。
```

---

## 🛠️ 文件结构

```
stock-monitor-pro/
├── SKILL.md                 # 技能文档
├── README.md                # 本文件
├── _meta.json               # ClawHub 元数据
├── .clawhub/
│   └── origin.json
└── scripts/
    ├── monitor.py           # 核心监控
    ├── monitor_daemon.py    # 后台进程
    ├── analyser.py          # 智能分析
    ├── control.sh           # 控制脚本
    └── config.example.py    # 配置模板
```

---

## ⚠️ 免责声明

1. 本系统仅供参考，不构成投资建议
2. 技术指标有滞后性，请结合其他信息综合判断
3. 市场有风险，投资需谨慎
4. 付费功能一旦使用，不支持退款

---

## 📞 联系方式

- **ClawHub**: @15910701838
- **Moltbook**: u/jarvis-oc-2299
- **GitHub**: (待添加)

---

**版本**: 1.0.0  
**更新日期**: 2026-03-21

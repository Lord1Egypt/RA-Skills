# QVeris 数据获取模块

**目标**: 使用 QVeris API 获取投资数据，同时控制积分消耗

**原则**:
- ✅ 优先使用低消耗工具（< 2 积分）
- ❌ 避免高消耗工具（> 5 积分）用于日常获取
- 📦 做好数据缓存（宏观 7 天，北向 1 天）
- 📊 混合数据源（QVeris + 免费 API）

---

## 🔧 工具函数

### 获取北向资金

```bash
source ~/.openclaw/workspace/investment-framework-skill/data/qveris/fetch-northbound.sh
```

**数据源**: `ths_ifind.hk_connect_stats.v1`  
**消耗**: 1.248 积分/次  
**缓存**: 1 天

### 获取宏观经济

```bash
source ~/.openclaw/workspace/investment-framework-skill/data/qveris/fetch-macro.sh
```

**数据源**: `ths_ifind.macro_china.v1`  
**消耗**: 1 积分/次  
**缓存**: 7 天

### 获取资金流向

```bash
source ~/.openclaw/workspace/investment-framework-skill/data/qveris/fetch-industry-flow.sh
```

**数据源**: `ths_ifind.money_flow.v1`  
**消耗**: 1.56 积分/次  
**缓存**: 7 天

---

## 📊 积分消耗控制

| 工作流 | 频率 | 单次消耗 | 月度消耗 |
|--------|------|----------|----------|
| 每日市场扫描 | 每日 | 1.248 | ~25 积分 |
| 周度行业跟踪 | 每周 | 1.56 | ~6 积分 |
| 月度组合复盘 | 每月 | 6.5×N | ~13-20 积分 |
| **总计** | - | - | **~48-55 积分** |

---

## 🛠️ 使用示例

### 每日市场扫描

```bash
#!/bin/bash
# 获取北向资金（带缓存）
bash ~/.openclaw/workspace/scripts/fetch-northbound.sh

# 解析数据
NORTHBOUND_DATA=$(cat ~/.openclaw/workspace/data/northbound/$(date +%Y-%m-%d).json | jq -r '.[] | select(.类型 | contains("股通"))')

# 提取关键指标
NET_INFLOW=$(echo "$NORTHBOUND_DATA" | jq -r '."净买入额 (亿元，RMB)"')
TURNOVER=$(echo "$NORTHBOUND_DATA" | jq -r '."成交额 (亿元，RMB)"')

echo "北向资金净买入：$NET_INFLOW 亿元"
echo "北向资金成交额：$TURNOVER 亿元"
```

### 周度行业跟踪

```bash
#!/bin/bash
# 获取宏观数据（带缓存）
bash ~/.openclaw/workspace/scripts/fetch-macro.sh

# 解析 GDP 数据
GDP_DATA=$(cat ~/.openclaw/workspace/data/macro/latest.json | jq '.gdp[0]')
GDP_VALUE=$(echo "$GDP_DATA" | jq -r '."GDP:现价：累计值"')
GDP_GROWTH=$(echo "$GDP_DATA" | jq -r '."GDP:现价：累计同比"')

echo "GDP (最新季度): $GDP_VALUE 亿元"
echo "GDP 增速：$GDP_GROWTH%"
```

---

## 📁 目录结构

```
~/.openclaw/workspace/
├── scripts/
│   ├── fetch-northbound.sh      # 北向资金获取
│   ├── fetch-macro.sh           # 宏观经济获取
│   ├── fetch-industry-flow.sh   # 行业资金流向获取
│   └── check-qveris-usage.sh    # 使用情况检查
├── data/
│   ├── northbound/              # 北向资金缓存
│   │   └── YYYY-MM-DD.json
│   ├── macro/                   # 宏观数据缓存
│   │   └── latest.json
│   └── industry/                # 行业数据缓存
│       └── YYYY-Www.json
└── logs/
    └── qveris-usage.log         # 使用日志
```

---

## ⚠️ 注意事项

1. **API Key 配置**: 确保 `QVERIS_API_KEY` 环境变量已设置
2. **缓存检查**: 调用前先检查缓存，避免重复消耗
3. **错误处理**: 捕获 API 失败，降级到免费数据源
4. **日志记录**: 每次调用记录到 `qveris-usage.log`

---

## 🔍 监控命令

```bash
# 检查使用情况
bash ~/.openclaw/workspace/scripts/check-qveris-usage.sh

# 查看本月消耗
cat ~/.openclaw/workspace/logs/qveris-usage.log | grep "^$(date +%Y-%m)"

# 清理旧缓存（保留最近 7 天）
find ~/.openclaw/workspace/data/northbound -mtime +7 -delete
```

---

**更新时间**: 2026-03-23  
**维护者**: ant (一人 CEO 助理)

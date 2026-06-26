# 行业数据手动更新指南

**适用场景：** API 不可用时临时方案  
**更新频率：** 每个交易日 15:30（收盘后）  
**数据来源：** 东方财富网行业板块页面

---

## 📊 数据模板

### 行业涨跌幅数据

**文件位置：** `data/investment/industry-data.json`

**数据格式：**
```json
{
    "date": "2026-03-23",
    "timestamp": "2026-03-23 15:30:00",
    "source": "东方财富",
    "industries": [
        {
            "rank": 1,
            "name": "银行",
            "change_percent": 1.2,
            "volume": 520000000,
            "net_inflow": 520000000,
            "leader": "招商银行",
            "leader_change": 2.5
        },
        {
            "rank": 2,
            "name": "石油石化",
            "change_percent": 0.8,
            "volume": 310000000,
            "net_inflow": 310000000,
            "leader": "中国石油",
            "leader_change": 1.8
        }
    ]
}
```

---

## 🔍 数据获取步骤

### Step 1: 访问东方财富行业板块

**URL：** http://quote.eastmoney.com/center/gridlist.html#industry

### Step 2: 复制数据

**需要字段：**
- 行业名称
- 涨跌幅
- 成交量
- 主力净流入
- 领涨股
- 领涨股涨跌幅

### Step 3: 填充 JSON 模板

**示例：**
```json
{
    "date": "2026-03-23",
    "industries": [
        {"rank": 1, "name": "银行", "change_percent": 1.2, ...},
        {"rank": 2, "name": "石油石化", "change_percent": 0.8, ...}
    ]
}
```

### Step 4: 保存到文件

**文件路径：** `data/investment/industry-data.json`

---

## 📋 更新检查清单

- [ ] 数据日期正确
- [ ] 包含所有行业（至少前 10 和后 10）
- [ ] 涨跌幅数据准确
- [ ] 成交量单位统一（手）
- [ ] 主力净流入单位统一（元）
- [ ] 领涨股名称正确
- [ ] 文件 JSON 格式正确

---

## 🔄 自动化建议

### 未来改进方向

1. **爬虫脚本** - 自动抓取东方财富行业数据
2. **定时任务** - 每日 15:30 自动更新
3. **数据校验** - 对比历史数据检测异常

### 当前替代方案

- 使用腾讯 API 获取个股数据
- 行业数据手动更新
- 周度报告使用最新数据

---

## 📊 数据使用示例

### 在周度行业跟踪中使用

```python
import json

# 加载行业数据
with open('data/investment/industry-data.json', 'r') as f:
    data = json.load(f)

# 获取领涨行业
top_industries = sorted(data['industries'], 
                       key=lambda x: x['change_percent'], 
                       reverse=True)[:5]

# 获取领跌行业
bottom_industries = sorted(data['industries'], 
                          key=lambda x: x['change_percent'])[:5]
```

---

*最后更新：2026-03-23*  
*维护人：ant*

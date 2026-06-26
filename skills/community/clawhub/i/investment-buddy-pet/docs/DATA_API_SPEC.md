# 投资宠物数据接口规范

**统一数据格式，确保宠物 - 大师 - 用户数据互通**

---

## 🎯 渐进披露设计

**核心原则**：宠物技能不重复存储大师配置，按需调用已有大师 Skill。

```
用户触发"召唤大师"
    ↓
宠物检查：用户是否已安装大师 Skill？
    ↓
已安装 → 调用大师 Skill 生成建议
未安装 → 提示用户通过 ClawHub 安装
```

**优势**：
- 宠物技能轻量（不存储 18 位大师配置）
- 大师 Skill 独立更新（不影响宠物技能）
- 用户按需安装（减少初始复杂度）

---

## 一、数据架构总览

### 数据获取能力

**使用现有 data_layer**（`/home/admin/.openclaw/workspace/data_layer`）：

| 数据类型 | 数据源 | 更新频率 | 状态 |
|---------|--------|---------|------|
| **大盘指数** | 腾讯财经 | 实时 | ✅ 已实现 |
| **个股行情** | 腾讯/新浪/东方财富 | 实时 | ✅ 已实现 |
| **个股财报** | 东方财富 | 季度 | ✅ 已实现 |
| **基金净值** | 天天基金 | 每日 | ✅ 已实现 |
| **基金估值** | 天天基金 | 实时 | ✅ 已实现 |
| **北向资金** | Tushare/QVeris | 每日 | ✅ 已实现 |
| **宏观经济** | QVeris | 月度 | ✅ 已实现 |
| **行业数据** | QVeris/东方财富 | 每日 | ✅ 已实现 |
| **新闻搜索** | SearXNG | 实时 | ✅ 已实现 |

**降级策略**：
- 个股行情：腾讯 → 新浪 → 东方财富
- 北向资金：Tushare → QVeris
- 基金数据：天天基金

**缓存策略**：
- 大盘指数：不缓存（实时）
- 个股行情：5 分钟
- 财报数据：1 小时
- 基金净值：1 天
- 宏观数据：7 天

**大师召唤数据注入流程**：

```
用户问题："现在能买贵州茅台吗？"
    ↓
检测股票代码：600519.SH
    ↓
调用 data_layer.get_quote('600519.SH')
    ↓
获取真实数据（Quote 对象）：
  - price: 1850 元
  - change_pct: +2.5%
  - open: 1830 元
  - volume: 125000
    ↓
注入到大师 Skill prompt
    ↓
大师基于真实数据给出建议
```

```
┌─────────────────────────────────────────────────────────┐
│                    用户数据层                            │
│  user_profile.json | holdings.json | transactions.json  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    宠物服务层                            │
│  pet_engine.py | personality_test.py | pet_match.py     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    大师服务层                            │
│  master_summon.py | masters/*.json                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    数据接口层                            │
│  market_data.py | compliance_checker.py                 │
└─────────────────────────────────────────────────────────┘
```

---

## 二、核心数据结构

### 1. 用户画像 (User Profile)

**文件**: `data/users/{user_id}/profile.json`

```json
{
  "user_id": "user_001",
  "created_at": "2026-04-14T10:00:00Z",
  "pet_type": "songguo",
  "pet_level": 3,
  "pet_xp": 1500,
  
  "investment_profile": {
    "risk_tolerance": "conservative",
    "investment_style": "value",
    "decision_style": "cautious",
    "knowledge_level": "beginner",
    "experience_years": 1
  },
  
  "personality_scores": {
    "risk_score": 25,
    "knowledge_score": 40,
    "decision_score": 30,
    "emotion_score": 60,
    "time_score": 80
  },
  
  "preferences": {
    "notification_time": "08:30",
    "reminder_frequency": "daily",
    "data_display": "simple",
    "communication_style": "warm"
  },
  
  "stats": {
    "total_investment_days": 182,
    "total_sip_count": 26,
    "total_learning_hours": 12,
    "last_active": "2026-04-14T09:00:00Z"
  }
}
```

---

### 2. 持仓数据 (Holdings)

**文件**: `data/users/{user_id}/holdings.json`

```json
{
  "user_id": "user_001",
  "updated_at": "2026-04-14T15:00:00Z",
  
  "holdings": [
    {
      "symbol": "000001.SZ",
      "name": "平安银行",
      "type": "stock",
      "quantity": 1000,
      "avg_cost": 12.50,
      "current_price": 13.20,
      "market_value": 13200.00,
      "cost_basis": 12500.00,
      "unrealized_pnl": 700.00,
      "unrealized_pnl_percent": 5.6,
      "weight": 0.15,
      "first_buy_date": "2025-10-14",
      "last_update": "2026-04-14T15:00:00Z"
    },
    {
      "symbol": "510300.SH",
      "name": "沪深 300ETF",
      "type": "fund",
      "quantity": 5000,
      "avg_cost": 4.20,
      "current_price": 4.35,
      "market_value": 21750.00,
      "cost_basis": 21000.00,
      "unrealized_pnl": 750.00,
      "unrealized_pnl_percent": 3.57,
      "weight": 0.25,
      "first_buy_date": "2025-08-01",
      "last_update": "2026-04-14T15:00:00Z"
    }
  ],
  
  "summary": {
    "total_market_value": 87500.00,
    "total_cost_basis": 82000.00,
    "total_unrealized_pnl": 5500.00,
    "total_unrealized_pnl_percent": 6.71,
    "cash_balance": 12500.00,
    "total_asset": 100000.00
  }
}
```

---

### 3. 市场数据 (Market Data)

**接口**: `api/market_data.py`

**获取指数行情**:
```python
def get_index_quotes(index_codes: List[str]) -> Dict:
    """
    获取指数行情
    
    Args:
        index_codes: 指数代码列表，如 ['000001.SZ', '399001.SZ']
    
    Returns:
        {
            "000001.SZ": {
                "name": "上证指数",
                "current": 3050.50,
                "change_percent": -1.2,
                "change": -37.00,
                "high": 3080.00,
                "low": 3040.00,
                "volume": 125000000,
                "turnover": 15000000000,
                "updated_at": "2026-04-14T15:00:00Z"
            }
        }
    """
```

**获取基金净值**:
```python
def get_fund_nav(fund_codes: List[str]) -> Dict:
    """
    获取基金净值
    
    Args:
        fund_codes: 基金代码列表
    
    Returns:
        {
            "510300": {
                "name": "沪深 300ETF",
                "nav": 4.35,
                "nav_date": "2026-04-14",
                "change_percent": 0.8,
                "updated_at": "2026-04-14T15:00:00Z"
            }
        }
    """
```

---

### 4. 宠物消息 (Pet Message)

**接口**: `scripts/pet_message_generator.py`

**消息结构**:
```json
{
  "message_id": "msg_20260414_001",
  "user_id": "user_001",
  "pet_type": "songguo",
  "message_type": "greeting",
  "trigger": "scheduled",
  "created_at": "2026-04-14T08:30:00Z",
  
  "content": {
    "text": "早上好！今天也是存坚果的一天！☀️",
    "market_brief": {
      "sh_index": "3050.50 (-1.2%)",
      "portfolio_change": "+0.8%",
      "reminder": "定投日！记得打卡哦~"
    },
    "actions": [
      {
        "type": "sip_checkin",
        "text": "打卡定投",
        "payload": {"date": "2026-04-14"}
      },
      {
        "type": "view_portfolio",
        "text": "查看持仓",
        "payload": {}
      }
    ]
  },
  
  "metadata": {
    "pet_mood": "cheerful",
    "pet_level": 3,
    "user_streak": 26
  }
}
```

---

### 5. 大师建议 (Master Advice)

**接口**: `scripts/master_summon.py`

**请求**:
```json
{
  "user_id": "user_001",
  "pet_type": "songguo",
  "master_id": "buffett",
  "question": "现在能买贵州茅台吗？",
  "context": {
    "user_profile": {
      "risk_tolerance": "conservative",
      "investment_style": "value"
    },
    "holdings_summary": {
      "total_asset": 100000,
      "cash_ratio": 0.15
    }
  }
}
```

**响应**:
```json
{
  "status": "success",
  "master": {
    "id": "buffett",
    "name": "巴菲特",
    "emoji": "🎯"
  },
  "advice": {
    "principles": [
      "价格是你付出的，价值是你得到的",
      "如果你不愿意持有 10 年，就不要持有 10 分钟",
      "第一条规则是不要亏钱，第二条规则是记住第一条"
    ],
    "content": "贵州茅台是一家好公司，但好公司不等于好投资。关键是价格是否合理。当前 PE 约 30 倍，处于历史中位数。如果你相信茅台的长期竞争力，并且愿意持有 10 年+，可以考虑分批建仓。",
    "confidence": 0.85,
    "risk_warning": "高端白酒可能面临政策风险，建议仓位不超过总资产的 20%。"
  },
  "pet_supplement": {
    "text": "巴菲特的建议很有智慧！结合你的保守型风格，我建议：先用小仓位（5-10%）尝试，用定投方式分批建仓，做好持有 3 年 + 的准备。",
    "action_suggestion": "create_sip_plan"
  },
  "created_at": "2026-04-14T15:30:00Z"
}
```

---

## 三、数据接口 API

### 1. 用户数据接口

```python
# 获取用户画像
GET /api/user/{user_id}/profile

# 更新用户画像
PUT /api/user/{user_id}/profile

# 获取用户持仓
GET /api/user/{user_id}/holdings

# 获取用户统计
GET /api/user/{user_id}/stats
```

### 2. 市场数据接口

```python
# 获取指数行情
GET /api/market/index?codes=000001.SZ,399001.SZ

# 获取基金净值
GET /api/market/fund?codes=510300,000001

# 获取个股行情
GET /api/market/stock?codes=600519.SZ,000001.SZ

# 获取宏观数据
GET /api/market/macro?indicators=gdp,cpi,pmi
```

### 3. 宠物服务接口

```python
# 宠物匹配测试
POST /api/pet/match
Body: {"user_id": "user_001", "answers": [...]}

# 启动宠物
POST /api/pet/start
Body: {"user_id": "user_001", "pet_type": "songguo"}

# 获取宠物消息
GET /api/pet/message?user_id=user_001&date=2026-04-14

# 宠物成长
POST /api/pet/levelup
Body: {"user_id": "user_001", "xp_gain": 100}
```

### 4. 大师服务接口

```python
# 召唤大师
POST /api/master/summon
Body: {
  "user_id": "user_001",
  "pet_type": "songguo",
  "master_id": "buffett",
  "question": "现在能买贵州茅台吗？"
}

# 获取大师列表
GET /api/master/list

# 获取大师详情
GET /api/master/{master_id}
```

---

## 四、数据源规范

### 1. 免费数据源（推荐）

| 数据类型 | 数据源 | API 地址 | 更新频率 |
|---------|--------|---------|---------|
| 指数行情 | 新浪财经 | `http://hq.sinajs.cn/list={code}` | 实时 |
| 基金净值 | 天天基金 | `http://fund.eastmoney.com/pingzhongdata/{code}.js` | 每日 |
| 个股行情 | 腾讯财经 | `http://qt.gtimg.cn/q={code}` | 实时 |
| 宏观数据 | 国家统计局 | `https://data.stats.gov.cn/` | 月度 |

### 2. 付费数据源（可选）

| 数据类型 | 数据源 | 说明 |
|---------|--------|------|
| 深度财务数据 | 东方财富 Choice | 财报、研报 |
| 资金流向 | 港交所披露易 | 北向/南向资金 |
| 行业数据 | 申万宏源 | 行业指数、估值 |

---

## 五、数据缓存策略

### 缓存规则

| 数据类型 | 缓存时间 | 说明 |
|---------|---------|------|
| 指数行情 | 1 分钟 | 交易时段实时更新 |
| 基金净值 | 24 小时 | 每日更新一次 |
| 个股行情 | 1 分钟 | 交易时段实时更新 |
| 宏观数据 | 7 天 | 周度更新 |
| 用户持仓 | 5 分钟 | 用户操作后刷新 |
| 大师建议 | 1 小时 | 同问题复用 |

### 缓存实现

```python
from functools import lru_cache
import time

@lru_cache(maxsize=1000)
def get_index_quote_cached(code: str, timestamp: int) -> Dict:
    """
    带缓存的指数行情获取
    
    timestamp 用于控制缓存失效（每分钟）
    """
    return fetch_index_quote(code)

# 使用示例
def get_index_quote(code: str) -> Dict:
    # 每分钟更新一次缓存
    timestamp = int(time.time()) // 60
    return get_index_quote_cached(code, timestamp)
```

---

## 六、合规检查

### 合规规则

```python
COMPLIANCE_RULES = {
    "no_product_recommendation": True,  # 不推荐具体产品
    "no_return_promise": True,  # 不承诺收益
    "no_market_timing": True,  # 不提供择时建议
    "risk_warning_required": True,  # 必须有风险提示
    "data_disclaimer_required": True  # 必须有数据免责声明
}
```

### 合规检查函数

```python
def check_compliance(message: str) -> Tuple[bool, List[str]]:
    """
    检查消息是否合规
    
    Returns:
        (is_compliant, violations)
    """
    violations = []
    
    # 检查是否推荐具体产品
    if re.search(r'(推荐 | 建议买入 | 建议卖出)\s*(\d{6})', message):
        violations.append("推荐具体产品")
    
    # 检查是否承诺收益
    if re.search(r'(保证 | 一定 | 肯定)\s*(赚钱 | 收益|涨)', message):
        violations.append("承诺收益")
    
    # 检查是否有风险提示
    if not re.search(r'(风险 | 谨慎 | 仅供参考)', message):
        violations.append("缺少风险提示")
    
    return len(violations) == 0, violations
```

---

## 七、错误处理

### 错误码规范

| 错误码 | 说明 | 处理方式 |
|-------|------|---------|
| 1001 | 用户不存在 | 引导用户创建档案 |
| 1002 | 数据未找到 | 返回空数据，不报错 |
| 2001 | 市场数据获取失败 | 使用缓存数据 |
| 2002 | 市场数据延迟 | 标注数据时间 |
| 3001 | 大师建议生成失败 | 降级到宠物建议 |
| 4001 | 合规检查失败 | 拦截消息，提示修改 |

### 错误响应格式

```json
{
  "status": "error",
  "error_code": 2001,
  "error_message": "市场数据获取失败",
  "fallback": {
    "use_cache": true,
    "cache_time": "2026-04-14T14:00:00Z"
  },
  "suggestion": "已使用缓存数据，最新数据将在 1 分钟后更新"
}
```

---

**创建时间**：2026-04-14  
**版本**：v1.0.0  
**状态**：待实现  
**维护者**：燃冰 + ant

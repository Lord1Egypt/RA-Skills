# A股市场数据 API接口

> 龙虎榜 · 资金流向 · 涨跌股池 · 全量行情数据 · 持续更新更多接口
> http://fffy520.gicp.net:8003最新接口和使用方法详见

---

## 数据能力

| 维度 | 覆盖 |
|------|------|
| 龙虎榜 | 2016年至今 · 90,000+ 条，含买5卖5营业部明细 |
| 资金流向 | 个股主力/超大单/大单/中单/小单净流入 |
| 涨跌股池 | 涨停/跌停/炸板/连板/一字板/翘板/地天/天地板 |
| 更新频率 | 每个交易日 17:00 后更新 |

---

## 接口文档

### 1️⃣ 当日龙虎榜

```
GET /api/lhb/daily?date=2026-05-13
```

返回指定交易日完整龙虎榜，每只上榜股票含买入/卖出前5席位明细。

```
curl "http://fffy520.gicp.net:8003/api/lhb/daily?date=2026-05-13"
```

**核心字段：**
- `code` / `name` — 股票代码/名称
- `close` / `change` — 收盘价/涨跌幅
- `net_buy` — 净买入额（万元）
- `brokers.buy[5]` / `brokers.sell[5]` — 买入/卖出前5席位（排名、名称、金额、净额）
- `entry_type` — `daily` 日榜 / `3day` 三日榜
- `reason` — 上榜原因

---

### 2️⃣ 个股历史龙虎榜

```
GET /api/lhb/history?code=002031
```

查询单只股票全部龙虎榜上榜记录，追踪主力资金轨迹。

```
curl "http://fffy520.gicp.net:8003/api/lhb/history?code=002031"
```

---

### 3️⃣ 涨跌股池

```
GET /api/stock-pools?date=2026-05-13&data_type=limit_up
```

8 大股池每日更新，可按类型筛选。

**data_type 参数：**

| 参数 | 说明 |
|------|------|
| `limit_up` | 涨停（含题材/连板天数/涨停时间） |
| `limit_continuous` | 连板 |
| `limit_broken` | 炸板 |
| `limit_down` | 跌停 |
| `one_line_limit` | 一字板 |
| `rebound` | 翘板 |
| `earth_to_heaven` | 地天板 |
| `heaven_to_earth` | 天地板 |

不传 `data_type` 返回全部 8 类。

---

### 4️⃣ 个股资金流向

```
GET /api/moneyflow?code=600519&trade_date=20260513
```

获取个股主力/超大单/大单/中单/小单净流入数据。

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| code | ✅ | 6位股票代码 |
| trade_date | ❌ | YYYYMMDD，默认最新 |

**返回字段：**

| 字段 | 单位 | 说明 |
|------|------|------|
| main_net_inflow | 元 | 主力净流入（超大单+大单） |
| main_net_pct | % | 主力流入占比 |
| super_large_inflow | 元 | 超大单净流入 |
| large_inflow | 元 | 大单净流入 |
| medium_inflow | 元 | 中单净流入 |
| small_inflow | 元 | 小单净流入 |
| close_price | 元 | 收盘价 |
| change_pct | % | 涨跌幅 |

```
curl "http://fffy520.gicp.net:8003/api/moneyflow?code=600519&trade_date=20260513"
```

---

### 5️⃣ 账户信息

```
GET /api/account
```

查询当前的套餐类型、剩余配额和有效期。

```
curl "http://fffy520.gicp.net:8003/api/account"
```

---

## Python 客户端

```python
from client import LHBClient

client = LHBClient()

# 龙虎榜
daily = client.daily("2026-05-13")
history = client.history("002031")

# 资金流向
flow = client.moneyflow("600519", "20260513")
print(flow["data"]["main_net_inflow"])
```

> （日配额 100 次）。

---

## 限制说明

| 项目 | 规则 |
|------|------|
| 日配额 | 100次/天 · 长期不限量 |
| 历史条数 | 非长期套餐 ≤30条 · 长期不限 |
| 频率 | 30次/秒/Key |
| 缓存 | 同参数不重复扣配额 |

| HTTP状态 | 说明 |
|----------|------|
| 200 | 请求成功 |
| 401 | 无效凭证 |
| 403 | 凭证已禁用或当日配额用完 |
| 429 | 请求过于频繁 |

---

## 应用场景

- **跟庄选股** — 每日监控机构/游资净买入排行，锁定主力介入标的
- **游资追踪** — 通过营业部席位分析游资操作风格和偏好
- **个股诊断** — 查看个股历史上榜频率和资金流向变化
- **量化因子** — 将龙虎榜/资金流向作为选股因子构建策略
- **风控参考** — 观察主力出货信号，辅助持仓决策

---

*数据更新：交易所完整披露后更新 | 数据范围：2022-01-04 至今*

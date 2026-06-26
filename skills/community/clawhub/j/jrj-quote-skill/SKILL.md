---
name: jrj-quote-skill
description: >-
  A股实时行情和历史K线数据查询，支持技术指标计算。用于获取股票、场内基金、指数的实时价格、历史K线，以及计算MA、MACD、KDJ、BOLL、RSI等技术指标。
  <example>User: "获取招商银行最近30天的历史K线和MACD指标" Assistant: 使用 kline.js 脚本获取数据</example>
  <example>User: "查看贵州茅台的实时行情" Assistant: 调用 /v1/quote/realtime 接口</example>
metadata:
  {"openclaw": {"requires": {"env": ["JRJ_API_KEY"]}, "primaryEnv": "JRJ_API_KEY", "homepage": "https://ai.jrj.com.cn/claw"}}
---

# 金融界A股行情数据技能（JRJ Quote Skill）
为大模型提供权威、实时、准确的 A 股市场数据，杜绝过时/错误信息输出，支持行情查询、K 线获取、技术指标一站式计算。

## 核心功能
1、获取股票、场内基金、指数的实时行情数据
2、获取A股历史日K线数据，支持前复权/后复权/不复权
3、基于K线数据本地计算技术指标

## 使用场景

### 1、基础行情查询场景
实时行情查询
用户询问单只 / 多只股票、指数、场内基金的当前价格、涨跌幅、成交量等实时数据。
证券基本信息查询
查询股票名称、市场（沪 / 深）、交易状态等基础信息。

### 2、K 线与历史数据场景
历史走势复盘
获取指定股票日 K 线、前复权 / 后复权数据，用于历史走势分析。
区间行情统计
查询某只股票近 N 日 / 某时间段的开盘、最高、最低、收盘、成交额等数据。

### 3、技术指标分析场景
趋势类指标分析
基于 MA、MACD 判断中期 / 长期趋势、金叉死叉。
超买超卖判断
使用 RSI、KDJ、WR 识别高位超买、低位超卖信号。
波动与支撑压力分析
通过 BOLL、ATR 判断价格波动区间、支撑位与压力位。
量价关系分析
结合成交量均线、OBV 评估量价配合度。

### 4、AI 助手典型对话场景
帮用户分析近 30 日走势 + 均线 + MACD，给出趋势判断。
根据 KDJ、RSI 指标，提示当前是否处于超买 / 超卖区间。
输出格式化 K 线表格，方便用户快速查看。
结合多指标给出技术面简要解读，辅助投资参考。

### 5、功能集成场景
接入AI 量化分析系统，作为行情数据底层能力。
为投顾助手、选股机器人、复盘工具提供数据支持。
用于回测框架、指标研究、策略验证等量化研究场景。

## 环境配置

```bash
# 必须设置以下环境变量
export JRJ_API_KEY=sk_live_xxx   # API Key
```

## 快速开始

### 获取实时行情

```bash
# 调用 API 获取实时行情
curl -X POST "https://quant-gw.jrj.com/v1/quote/realtime" \
  -H "X-API-Key: ${JRJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["600036.SH", "000001.SZ"]}'
```

### 获取历史K线数据

使用 `scripts/kline.js` 脚本：

```bash
# 只获取历史K线（不计算指标）
node scripts/kline.js --symbol=600036.SH

# 获取历史K线 + 计算指标
node scripts/kline.js --symbol=600036.SH --with=ma,macd

# 完整参数示例
node scripts/kline.js \
  --symbol=600036.SH \
  --period=daily \
  --adjust=qfq \
  --limit=100 \
  --with=ma,macd,kdj \
  --format=json
```

## 命令行参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--symbol` | 是 | - | 证券代码，如 600036.SH |
| `--period` | 否 | daily | K线周期：目前只支持 daily |
| `--adjust` | 否 | none | 复权类型：none/qfq(前复权)/hfq(后复权) |
| `--limit` | 否 | 100 | K线数量 |
| `--start-date` | 否 | - | 起始日期 YYYYMMDD，从该日期往最新方向取 |
| `--with` | 否 | - | 计算指标，逗号分隔，见下表 |
| `--format` | 否 | json | 输出格式：json/markdown |

## 技术指标

### 可用指标组

| 组名 | 包含指标 | 说明 |
|------|----------|------|
| `ma` | ma5, ma10, ma20, ma60 | 移动平均线 |
| `macd` | macd_dif, macd_dea, macd_hist | MACD指标 |
| `kdj` | kdj_k, kdj_d, kdj_j | KDJ随机指标 |
| `boll` | boll_upper, boll_mid, boll_lower | 布林带 |
| `rsi` | rsi6, rsi12, rsi24 | 相对强弱指标 |
| `wr` | wr14 | 威廉指标 |
| `obv` | obv, obv_ma20 | 能量潮指标 |
| `atr` | atr, atr_ma14 | 真实波幅 |
| `vol` | vol_ma5, vol_ma10 | 成交量均线 |
| `cci` | cci | 顺势指标 |
| `roc` | roc | 变动率指标 |

### 使用示例

```bash
# 使用指标组
node scripts/kline.js --symbol=600036.SH --with=ma,macd

# 使用单个指标
node scripts/kline.js --symbol=600036.SH --with=ma5,ma20,macd_dif

# 混合使用
node scripts/kline.js --symbol=600036.SH --with=ma,rsi6,kdj_k
```

### 指标说明

脚本会自动请求足够的历史数据以确保指标计算准确。例如计算 ma60 时，会额外请求 60 根K线用于预热，最终返回用户请求的数量。

详细指标说明见 [references/indicators-guide.md](references/indicators-guide.md)

### 关于返回数量

当请求的数据量较大时，API 可能无法一次返回全部结果。此时响应会包含 `truncated: true` 标记，脚本会提示：

- **无指标计算时**："可能有更多历史数据未返回"
- **有指标计算时**："指标计算可能不准确（预热数据不足）"

如遇此情况，建议调整 `--limit` 值或使用 `--start-date` 缩小查询范围。

## API 接口

### 实时行情

```
POST /v1/quote/realtime
```

**请求参数**：
```json
{
  "symbols": ["600036.SH", "000001.SZ"]  // 最多 100 个
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "trade_date": 20260320,
    "quotes": [
      {
        "symbol": "600036.SH",
        "name": "招商银行",
        "price": 39.00,
        "change_pct": 0.0125,
        "volume": 12345678,
        "amount": 480000000
      }
    ]
  }
}
```

### K线数据

```
POST /v1/quote/kline
```

获取已收盘的历史日K线数据。

**请求参数**：
```json
{
  "symbol": "600036.SH",
  "period": "daily",
  "adjust": "qfq",
  "limit": 100,
  "start_date": 20260101
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "symbol": "600036.SH",
    "period": "daily",
    "adjust": "qfq",
    "count": 100,
    "klines": [
      {
        "date": 20260320,
        "open": 38.50,
        "high": 39.20,
        "low": 38.30,
        "close": 39.00,
        "volume": 12345678,
        "amount": 480000000
      }
    ],
    "truncated": true
  }
}
```

> **注意**：当 `truncated: true` 时，表示可能有更多数据未返回。

详细 API 文档见 [references/api-reference.md](references/api-reference.md)

## 输出格式

### JSON 格式（默认）

```json
{
  "symbol": "600036.SH",
  "period": "daily",
  "adjust": "qfq",
  "count": 100,
  "klines": [
    {
      "date": 20260320,
      "open": 38.50,
      "high": 39.20,
      "low": 38.30,
      "close": 39.00,
      "volume": 12345678,
      "amount": 480000000,
      "ma5": 38.80,
      "ma20": 37.50,
      "macd_dif": 0.35,
      "macd_dea": 0.28,
      "macd_hist": 0.07
    }
  ]
}
```

### Markdown 格式

```bash
node scripts/kline.js --symbol=600036.SH --with=ma --format=markdown
```

输出：
```markdown
## 600036.SH K线数据

| 日期 | 开盘 | 最高 | 最低 | 收盘 | 成交量 | MA5 | MA20 |
|------|------|------|------|------|--------|-----|------|
| 20260320 | 38.50 | 39.20 | 38.30 | 39.00 | 1234万 | 38.80 | 37.50 |
```

## 常见用例

### 1. 趋势分析

```bash
# 查看均线和MACD判断趋势
node scripts/kline.js --symbol=600036.SH --with=ma,macd --limit=60
```

### 2. 超买超卖判断

```bash
# 使用RSI和KDJ判断
node scripts/kline.js --symbol=600036.SH --with=rsi,kdj --limit=30
```

### 3. 波动性分析

```bash
# 布林带和ATR
node scripts/kline.js --symbol=600036.SH --with=boll,atr --limit=60
```

### 4. 量价分析

```bash
# 成交量均线和OBV
node scripts/kline.js --symbol=600036.SH --with=vol,obv --limit=60
```

## 错误处理

| 错误码 | 说明 |
|--------|------|
| 40001 | 参数错误（如 symbol 格式不正确） |
| 40101 | API Key 无效，请前往金融界App获取最新API Key |
| 42901 | 超出请求限制，请稍后再试 |
| 42902 | 超出每日配额，请前往金融界App获取每日更多配额 |

## 参考文档

- [API 接口文档](references/api-reference.md)
- [技术指标说明](references/indicators-guide.md)

---

## 免责声明

1. **数据仅供参考**：本工具提供的行情数据和技术指标仅供学习和研究使用，不构成任何投资建议。
2. **准确性不保证**：虽然我们尽力保证数据准确，但不对数据的完整性、准确性或时效性作任何保证。
3. **投资风险**：股票投资有风险，投资者应独立判断并承担投资决策的全部责任。
4. **技术指标局限性**：技术指标基于历史数据计算，不能预测未来走势，仅供辅助分析参考。
5. **使用限制**：本工具仅限个人学习研究使用，禁止用于商业用途或非法活动。

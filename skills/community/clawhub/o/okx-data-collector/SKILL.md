# okx-data-collector Skill

OKX 数据采集与分析技能 - 支持实时 WebSocket 采集、REST API 历史补全、回测数据需求分析。

## 功能特性

- ✅ **实时采集**: tick 级数据 WebSocket 实时推送
- ✅ **历史补全**: REST API 批量获取历史 K 线
- ✅ **多周期支持**: 1m, 5m, 15m, 1H, 4H, 1D, 1W 等
- ✅ **需求分析**: 根据策略类型推荐数据采集方案
- ✅ **存储估算**: 计算不同配置下的存储需求

## 使用方法

### 1. 数据需求分析

查看 OKX 数据可获取性和回测建议：

```bash
cat ~/.jvs/.openclaw/workspace/skills/okx-data-collector/OKX_DATA_ANALYSIS.md
```

### 2. 采集历史数据

```bash
# 采集 BTC 永续合约 1H 数据，最近 365 天
cd ~/.jvs/.openclaw/workspace/skills/okx-data-collector
python3 fetch_history.py --symbol BTC-USDT-SWAP --bar 1H --days 365 --output ./data

# 采集 4H 数据，最近 5 年
python3 fetch_history.py --symbol BTC-USDT-SWAP --bar 4H --days 1825 --output ./data

# 采集日线数据，最近 10 年
python3 fetch_history.py --symbol BTC-USDT-SWAP --bar 1D --days 3650 --output ./data
```

### 3. 批量采集（推荐配置）

```bash
# 创建采集脚本
cat > batch_fetch.sh << 'EOF'
#!/bin/bash
SYMBOLS=("BTC-USDT-SWAP" "ETH-USDT-SWAP")
OUTPUT_DIR="./data"

for symbol in "${SYMBOLS[@]}"; do
    # 基础配置
    python3 fetch_history.py -s $symbol -b 1H -d 730 -o $OUTPUT_DIR
    python3 fetch_history.py -s $symbol -b 4H -d 1825 -o $OUTPUT_DIR
    python3 fetch_history.py -s $symbol -b 1D -d 3650 -o $OUTPUT_DIR
done
EOF

chmod +x batch_fetch.sh
./batch_fetch.sh
```

### 4. 使用实时采集器

配合 `tencent-cos-data-collector` skill 进行实时采集：

```bash
# 实时采集 tick 数据并上传 COS
# 参考 tencent-cos-data-collector skill 的文档
```

## 数据需求建议

### 基础配置（推荐起点）

| 周期 | 采集时长 | 用途 |
|------|----------|------|
| 1m   | 90 天    | 高频回测 |
| 5m   | 365 天   | 日内策略 |
| 1H   | 2 年     | 波段策略 |
| 4H   | 5 年     | 趋势策略 |
| 1D   | 10 年    | 因子回测 |

### 完整配置（机构级）

| 周期 | 采集时长 | 用途 |
|------|----------|------|
| 1m   | 365 天   | 完整高频 |
| 5m   | 2 年     | 日内策略 |
| 15m  | 3 年     | 中频策略 |
| 1H   | 5 年     | 波段/趋势 |
| 4H   | 8 年     | 长期趋势 |
| 1D   | 开市至今 | 因子/宏观 |

## 文件结构

```
okx-data-collector/
├── SKILL.md                  # 本说明文件
├── OKX_DATA_ANALYSIS.md      # 详细数据分析报告
├── fetch_history.py          # 历史数据采集脚本
├── data/                     # 采集的数据输出目录
└── README.md                 # 使用文档
```

## OKX API 说明

### REST API

- **端点**: `GET /api/v5/market/candles`
- **支持周期**: 1m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 12H, 1D, 2D, 3D, 1W, 1M
- **单次限制**: 最多 100 条
- **分页参数**: `before`, `after` (毫秒时间戳)
- **速率限制**: 20 次/秒

### WebSocket

- **端点**: `wss://ws.okx.com:8443/ws/v5/public`
- **订阅频道**: trades, books, tickers, candles1m, etc.
- **推送频率**: 实时（毫秒级）

## 数据格式

### K 线数据结构

```json
[
  {
    "ts": "1597026383085",
    "o": "11768.6",
    "h": "11770",
    "l": "11764.7",
    "c": "11768.6",
    "vol": "66.1636",
    "volCcy": "778614.3299"
  }
]
```

### 输出文件格式

**JSON**: 原始 API 响应格式
**CSV**: 
```csv
timestamp,open,high,low,close,volume
2026-04-01 12:00:00,68500.5,68520.0,68480.0,68510.0,1234.56
```

## 存储建议

### 本地存储

- **格式**: Parquet (推荐) / CSV / JSON
- **压缩**: Snappy / Gzip
- **分区**: 按品种 + 日期

### 数据库存储

**DolphinDB** (推荐):
```sql
create table kdata(
    symbol: SYMBOL,
    timestamp: TIMESTAMP,
    open: DOUBLE,
    high: DOUBLE,
    low: DOUBLE,
    close: DOUBLE,
    volume: DOUBLE
) PARTITION BY (symbol, HOUR(timestamp))
```

**ClickHouse**:
```sql
CREATE TABLE kdata (
    symbol String,
    timestamp DateTime,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    volume Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (symbol, timestamp)
```

## 相关 Skill

- **tencent-cos-data-collector**: 实时数据采集 + COS 存储
- **dolphindb-connector**: DolphinDB 数据库连接

## 注意事项

1. **API 限流**: 请求间隔至少 50ms，避免被封禁
2. **数据质量**: 采集后检查连续性和异常值
3. **时区处理**: OKX 使用 UTC 时间戳，注意转换
4. **合约换月**: 永续合约无需换月，季度合约注意到期日

## 故障排查

### 问题：API 请求失败

```bash
# 检查网络连接
curl -I https://www.okx.com/api/v5/market/candles?instId=BTC-USDT&bar=1D&limit=1

# 检查 API 状态
# 访问 OKX 状态页面
```

### 问题：数据不连续

```bash
# 检查缺失时间段
python3 -c "
import json
data = json.load(open('data/BTC-USDT-SWAP_1H_365d.json'))
timestamps = [int(c[0]) for c in data]
gaps = []
for i in range(1, len(timestamps)):
    gap = timestamps[i] - timestamps[i-1]
    if gap > 3600000 * 1.5:  # 大于 1.5 倍间隔
        gaps.append((timestamps[i-1], timestamps[i], gap))
print(f'发现 {len(gaps)} 个数据缺口')
"
```

## 参考文档

- [OKX API 文档](https://www.okx.com/docs-v5/en/)
- [OKX_DATA_ANALYSIS.md](./OKX_DATA_ANALYSIS.md) - 详细数据调研报告

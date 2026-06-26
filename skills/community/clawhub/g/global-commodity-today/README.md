# Global Commodity Today

全球大宗商品行情简报工具，支持查询伦敦金、伦敦银、伦敦铜、纽约铂、布伦特原油的当前价格和当日涨跌幅，生成简洁的行情简报。

## ✨ 功能特性

- 📈 实时获取贵金属（金、银、铜、铂）及布伦特原油行情
- 📊 自动生成结构化行情简报（Markdown 格式）
- 🔍 支持单品种查询和全品种简报两种模式
## 📦 支持品种

| 品种 | 代码 | 单位 | 说明 |
|------|------|------|------|
| 伦敦金 | XAU | 美元/盎司 | London Gold Spot |
| 伦敦银 | XAG | 美元/盎司 | London Silver Spot |
| 伦敦铜 | CAD | 美元/吨 | LME Copper |
| 纽约铂 | PLT | 美元/盎司 | NYMEX Platinum |
| 布伦特原油 | OIL | 美元/桶 | Brent Crude Oil |

## 🚀 快速开始

### 安装依赖

```bash
pip install akshare pandas
```

### 获取全品种行情简报

```bash
python scripts/precious_metals_oil_fetcher.py --mode briefing
```

### 查询单个品种

```bash
# 可选值：gold / silver / copper / platinum / oil
python scripts/precious_metals_oil_fetcher.py --mode single --commodity gold
```

## 📖 参数说明

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--mode` | 运行模式 | `briefing`（全品种简报）/ `single`（单品种查询） | `briefing` |
| `--commodity` | 品种（单品种模式下使用） | `gold` / `silver` / `copper` / `platinum` / `oil` | - |

## 🤖 在 Claw 中使用

本工具已上传至 ClawHub，可作为 Skill 在 Claw 中直接使用。

### 安装 Skill

在 Claw 中搜索并安装 `global-commodity-today` skill，或通过命令行安装：

```bash
npx clawhub@latest install global-commodity-today
```

### 使用方式

安装后，直接用自然语言对话即可触发，例如：

- "帮我看看今天的大宗商品行情"
- "查一下现在伦敦金的价格"
- "布伦特原油今天涨了还是跌了？"
- "给我一份贵金属和原油的行情简报"

Claw 会自动识别意图并调用此 Skill，返回实时行情数据。

## ⚠️ 注意事项

- 数据来源为 [akshare](https://github.com/akfamily/akshare) 聚合的公开行情接口
- 所有价格均以美元计价
- 周末和节假日可能只能获取上一交易日的收盘数据
- 建议获取间隔至少 1 分钟，避免接口限流
- 所有数据仅供参考，不构成投资建议

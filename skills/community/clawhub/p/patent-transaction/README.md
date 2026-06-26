# patent-transaction · 专利交易

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://clawhub.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-Publish-orange.svg)](https://clawhub.ai)

[English](#english) · [中文](#中文)

---

## 中文

对接 **专利交易 Skill API**（`https://trade.9235.net/api/skill`）：在售专利、卖家信息、成交记录、开放许可、采购需求。

### 主要能力

| 命令 | 说明 |
|------|------|
| `search` | 在售专利搜索（表格） |
| `detail` | 交易详情 |
| `sellers` / `orders` | 卖家、成交记录 |
| `open` | 开放许可 |
| `demand` | 采购需求 |
| `export` / `export_orders` | 导出 Excel |

常与 **patent-search** 配合做转让/许可尽调，流程见 [due-diligence.md](due-diligence.md)。

### 配置

```bash
export TRADE_API_TOKEN='你的交易Skill令牌'
export TRADE_API_BASE_URL='https://trade.9235.net/api/skill'
```

或复制 `config.example.json` → `config.json`。

Token 由运维在 `TRADE_SKILL_TOKENS` 配置，或通过服务端 `gen_skill_token.go` 签发。

### 依赖

- Python 3.8+
- `pip install requests`

### CLI 示例

```bash
python3 main.py search 锂电池
python3 main.py detail CN112968234A
python3 main.py orders
python3 main.py open 石墨烯
```

---

## English

**Patent marketplace** skill for listings, sellers, closed deals, open licensing, and buyer demands via `trade.9235.net/api/skill`.

### Commands

| Command | Purpose |
|---------|---------|
| `search` | Search listed patents |
| `detail` | Listing detail |
| `sellers` / `orders` | Seller info and deal history |
| `open` | Open licensing search |
| `demand` | Procurement demands |
| `export` | Excel export |

Pair with **patent-search** for legal/claims due diligence — see [due-diligence.md](due-diligence.md).

### Configuration

```bash
export TRADE_API_TOKEN='your-skill-token'
export TRADE_API_BASE_URL='https://trade.9235.net/api/skill'
```

### Requirements

- Python 3.8+
- `pip install requests`

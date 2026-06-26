---
name: ifind-mcp
description: 同花顺iFinD金融数据MCP工具。用于查询A股股票、公募基金、宏观经济和新闻资讯数据。当用户需要查询股票、基金、宏观经济指标或新闻资讯时使用。
---

# iFind MCP Skill

同花顺 iFinD MCP 服务，提供专业金融数据查询。

## 首次使用指引

### 1. 安装 mcporter

```bash
# 安装 Node.js (如果没有)
# macOS: brew install node
# Linux: sudo apt install nodejs

# 安装 mcporter
npm install -g mcporter
```

### 2. 配置密钥

将密钥配置到 `~/.openclaw/mcporter.json`（推荐，跨平台兼容）：

```bash
mkdir -p ~/.openclaw
cat > ~/.openclaw/mcporter.json << 'EOF'
{
  "mcpServers": {
    "hexin-ifind-stock": {
      "url": "https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-stock-mcp",
      "headers": {
        "Authorization": "Bearer <你的密钥>"
      }
    },
    "hexin-ifind-fund": {
      "url": "https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-fund-mcp",
      "headers": {
        "Authorization": "Bearer <你的密钥>"
      }
    },
    "hexin-ifind-edb": {
      "url": "https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-edb-mcp",
      "headers": {
        "Authorization": "Bearer <你的密钥>"
      }
    },
    "hexin-ifind-news": {
      "url": "https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-news-mcp",
      "headers": {
        "Authorization": "Bearer <你的密钥>"
      }
    }
  }
}
```

> **密钥获取**：在 iFinD 终端下载 MCP 配置文件（tonghuashun_token.rtf），提取 JSON 中的 Authorization 字段值。

### 3. 验证配置

```bash
mcporter --config ~/.openclaw/mcporter.json list
# 应显示 4 个健康的服务器
```

## 调用方式

```bash
# 使用配置文件的路径
mcporter --config ~/.openclaw/mcporter.json call <server>.<tool>
```

### 便捷脚本

```bash
# 修改脚本中的配置路径
sed -i 's|~/.config|~/.openclaw|' scripts/query.sh

./scripts/query.sh stock "贵州茅台"
```

## MCP 服务器

| 服务器 | 用途 |
|--------|------|
| hexin-ifind-stock | A股股票数据 |
| hexin-ifind-fund | 公募基金数据 |
| hexin-ifind-edb | 宏观经济数据 |
| hexin-ifind-news | 公告资讯 |

## 股票工具 (hexin-ifind-stock)

| 工具 | 说明 |
|------|------|
| get_stock_summary | 股票信息摘要 |
| search_stocks | 智能选股 |
| get_stock_perfomance | 历史行情与技术指标 |
| get_stock_info | 基本资料查询 |
| get_stock_shareholders | 股本结构与股东数据 |
| get_stock_financials | 财务数据与指标 |
| get_risk_indicators | 风险指标 |
| get_stock_events | 公开披露事件 |
| get_esg_data | ESG评级 |

### 使用示例

```bash
# 查询股票概况
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-stock.get_stock_summary query:"贵州茅台"

# 智能选股
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-stock.search_stocks query:"新能源汽车行业市值大于1000亿"

# 历史行情
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-stock.get_stock_perfomance query:"宁德时代最近5日涨跌幅"

# 财务数据
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-stock.get_stock_financials query:"比亚迪2025年ROE"
```

## 基金工具 (hexin-ifind-fund)

| 工具 | 说明 |
|------|------|
| search_funds | 模糊基金名称匹配 |
| get_fund_profile | 基金基本资料 |
| get_fund_market_performance | 行情与业绩 |
| get_fund_ownership | 份额与持有人结构 |
| get_fund_portfolio | 投资标的与资产配置 |
| get_fund_financials | 基金财务指标 |
| get_fund_company_info | 基金公司信息 |

### 使用示例

```bash
# 查询基金
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-fund.search_funds query:"易方达科技ETF"

# 基金业绩
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-fund.get_fund_market_performance query:"富国天惠近一年收益率"

# 持仓明细
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-fund.get_fund_portfolio query:"中欧医疗健康混合A2025Q2持仓"
```

## 宏观/新闻工具

### 使用示例

```bash
# 宏观经济
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-edb.get_macro_data query:"中国GDP增速"

# 新闻资讯
mcporter --config ~/.openclaw/mcporter.json call hexin-ifind-news.get_company_news query:"华为最新公告"
```

## API 文档

详细 API 说明见 [references/API.md](references/API.md)

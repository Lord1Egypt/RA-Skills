# MemeCoin 分析师 Skill

## 简介

**MemeCoin 分析师** - 专业的Meme币走势预测和筹码分布分析工具。

## 功能

1. **价格走势分析** - 分析代币价格趋势、技术指标（RSI、MACD）
2. **涨跌预测** - 基于技术面分析给出短期走势判断
3. **筹码分布分析** - 分析持币地址分布，评估控盘风险
4. **完整分析报告** - 综合价格和筹码数据的全面分析

## 定价

- **费用**: 0.001 USDT / 每次调用
- **支付方式**: SkillPay.me
- **API Key**: `sk_e0c26b0e9826d17c309bd5030cbe95ef04ed33cf4f05c03dae0f23358ee5e956`

## 使用方法

### 1. 价格分析

分析 [代币地址] 的价格走势

例如：分析 EpX5r1u6K4g2W5Y8p3qR7vT1nH6jK9LmP0xS2wQ8aB4 的价格走势

支持的链：
- solana
- base  
- ethereum
- arbitrum
- bsc

### 2. 筹码分布分析

分析 [代币地址] 的筹码分布

### 3. 完整分析

给我 [代币地址] 的完整分析报告

## API 接口

如果你需要自行托管服务，可以使用以下API：

### 价格分析
POST /analyze/price
{
  "tokenAddress": "代币合约地址",
  "chain": "solana|base|ethereum|arbitrum|bsc"
}

### 筹码分析
POST /analyze/holders
{
  "tokenAddress": "代币合约地址", 
  "chain": "solana|base|ethereum|arbitrum|bsc"
}

### 完整分析
POST /analyze/full
{
  "tokenAddress": "代币合约地址",
  "chain": "solana|base|ethereum|arbitrum|bsc"
}

## 响应示例

{
  "success": true,
  "token": {
    "address": "EpX5r1u6K4g2W5Y8p3qR7vT1nH6jK9LmP0xS2wQ8aB4",
    "symbol": "PEPE",
    "chain": "solana"
  },
  "price": {
    "current": 0.00000123,
    "change24h": 15.5,
    "volume24h": 5000000
  },
  "indicators": {
    "rsi": 65,
    "macd_signal": "bullish",
    "trend": "bullish"
  },
  "prediction": {
    "short_term": "看涨",
    "confidence": 65,
    "reasoning": "MACD显示金叉信号，短期趋势向上"
  },
  "risk_assessment": {
    "level": "中",
    "summary": "筹码相对分散，需关注大户动向"
  }
}

## 数据来源

- 价格数据：DexScreener API
- 链上数据：各链Explorer API

## 风险提示

重要声明
- 此分析仅供参考，不构成投资建议
- 加密货币波动剧烈，投资需自行承担风险
- Meme币风险极高，请勿投入超过承受能力的资金
- 任何投资决策前请进行充分研究

## 技术栈

- 后端：Node.js + Express
- 数据源：DexScreener API
- 支付：SkillPay.me

## 部署

可以使用 Docker 部署：

docker build -t memecoin-analyst .
docker run -d -p 3000:3000 -e SKILLPAY_API_KEY=your_api_key memecoin-analyst

## 版本

- v1.0.0 - 初始版本

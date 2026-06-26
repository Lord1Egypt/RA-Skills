# A2A Market 上架技能

## 1. 平台简介

A2A Market 是面向 AI Agent 的技能/服务交易市场，开发者可以将 AI 技能（Agent）上架到市场，供其他用户购买和调用。平台支持 Web3 钱包认证（MetaMask），交易使用加密货币结算。

**网址**: https://a2a.market

---

## 2. 注册/登录方式

### 前置准备
- 安装 **MetaMask** 浏览器插件或手机钱包
- 确保钱包中有少量 **ETH**（用于 gas 费用）
- 推荐使用 Ethereum 主网或 Polygon 网络

### 注册/登录流程
1. 访问 A2A Market 网站
2. 点击「Connect Wallet」/「连接钱包」
3. 在弹出的 MetaMask 窗口中点击「签名」
4. 签名完成即完成登录（无需传统账号密码）

### 首次使用
1. 连接钱包后，完善个人资料（如有）
2. 设置显示名称、头像、个人主页链接

---

## 3. 上架技能流程

### 步骤一：准备工作
1. 确认技能已完成开发，功能正常
2. 准备技能相关材料：
   - 技能名称（中英文）
   - 详细描述（用途、功能、使用方法）
   - 定价（ETH / MATIC / USDC 等）
   - 预览图 / 封面图
   - 使用示例 / Demo 视频链接

### 步骤二：进入开发者后台
1. 连接 MetaMask 钱包
2. 点击右上角头像 → 「Dashboard」或「开发者中心」
3. 选择「发布技能」/「List Skill」

### 步骤三：填写技能信息
1. **技能名称**：英文，建议与技能目录名一致
2. **技能描述（Description）**：
   - 详细介绍技能功能
   - 说明输入参数和输出结果
   - 描述使用场景和限制
3. **分类（Category）**：选择对应分类
4. **标签（Tags）**：添加相关标签
5. **定价**：
   - 选择计价方式（一次性买断 / 订阅 / 按次调用）
   - 设置价格（如 0.05 ETH 或 50 USDC）
6. **预览图**：上传封面图（建议 512x512 或 3:4 比例）
7. **演示链接（Optional）**：Demo URL 或演示视频

### 步骤四：配置智能合约（平台自动处理）
1. 平台会自动为技能创建 NFT 或代币合约
2. 确认合约信息（无需手动配置）
3. 签名授权交易

### 步骤五：提交发布
1. 确认所有信息无误
2. 支付少量 gas 费用（发布上链）
3. 等待区块确认（约1-3分钟）
4. 技能上架成功，获得市场链接

---

## 4. 技能上架模板

### 技能元数据 JSON
```json
{
  "name": "Python Data Scraper Agent",
  "description": "A powerful AI agent that automatically scrapes structured data from any website. Supports JavaScript rendering, pagination, and export to CSV/JSON.",
  "category": "data-collection",
  "tags": ["python", "scraper", "web", "automation", "data"],
  "price": {
    "type": "one-time",
    "amount": "0.05",
    "currency": "ETH"
  },
  "images": [
    "https://your-domain.com/preview.png"
  ],
  "demo_url": "https://demo.your-domain.com",
  "version": "1.0.0",
  "compatibility": {
    "platform": ["openclaw", "langchain"],
    "requirements": ["python>=3.8", "selenium"]
  }
}
```

### 技能描述文案模板
```
## 🛠 技能名称

[英文名称] / [中文名称]

## 📖 简介

[一句话描述这个技能解决的问题]

## ✨ 功能特性

- **特性1**：[描述]
- **特性2**：[描述]
- **特性3**：[描述]

## 🎯 使用场景

1. [场景1]
2. [场景2]
3. [场景3]

## 📋 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 目标网站URL |
| selector | string | 否 | CSS选择器 |
| max_pages | number | 否 | 最大页数（默认1） |

## 📤 输出结果

[描述输出的数据格式]

## 💰 定价

- **买断价格**：X ETH / X USDC
- **订阅价格**：X ETH/月（可选）

## 🔗 示例

[演示链接或截图]

## 📦 安装要求

- Python 3.8+
- 依赖库：xxx, xxx

## 🔒 注意事项

[使用限制、隐私说明等]
```

---

## 5. API 操作

### Web 端操作（主要方式）
- 连接 MetaMask 钱包后，在 Web 界面管理技能

### Web3 API（进阶）
如果需要程序化管理，可以使用合约接口：

```javascript
// 伪代码 - 实际需参考平台合约ABI
const contract = new web3.eth.Contract(ABI, CONTRACT_ADDRESS);
await contract.methods.listSkill(skillMetadata).send({ from: walletAddress });
```

### 常见合约操作
```bash
# 查看技能列表
openclaw a2a list

# 上架技能
openclaw a2a publish ./skill-path --price 0.05 ETH

# 更新价格
openclaw a2a update-price <skill-id> --price 0.08 ETH

# 下架技能
openclaw a2a unpublish <skill-id>
```

---

## 6. 注意事项

1. **MetaMask 必须有余额**：发布和交易都需要 gas 费用（ETH/Polygon）
2. **定价要合理**：参考同类技能价格，避免过高或过低
3. **描述要详细**：Web3 买家更看重透明度，详细描述能提高转化率
4. **测试网先试**：建议先在测试网（如 Polygon Mumbai）发布测试
5. **钱包安全**：保护好私钥，不要在不信任的网站签名
6. **智能合约风险**：了解智能合约的风险，平台合约应有审计
7. **跨境支付**：加密货币支付需注意当地法规

---

## 7. 常见问题

**Q: 上架需要费用吗？**
A：发布时需要支付少量 gas 费用（通常 0.01-0.1 美元等值代币）。

**Q: 收益如何提现？**
A：技能收入直接进入你的 MetaMask 钱包，可转账到交易所兑换法币。

**Q: 支持哪些钱包？**
A：主要支持 MetaMask，也支持 WalletConnect、Coinbase Wallet 等。

**Q: 支付使用什么货币？**
A：通常支持 ETH、MATIC、USDC 等，具体看技能设置。

**Q: 如何保证技能不被盗用？**
A：技能代码可选择加密交付，或使用链下交付模式。

**Q: 出现纠纷怎么办？**
A：A2A Market 有链上争议解决机制，具体参考平台规则。

# ClawHub Listing Copy

Use this file when publishing the skill to ClawHub or other skill marketplaces.
Keep the public promise narrow: fast meme token risk triage, not trade execution and not investment advice.

## Chinese Listing Copy

### Title
Meme 风控雷达

### Subtitle
基于 Binance Web3 的 Meme 新币风险扫描器，支持中英双语输出与按次计费。

### One-line Pitch
先发现，再排雷。把新发和异动 Meme 币先压缩成一份可解释的风控清单。

### Short Description
扫描新发、临近迁移或刚迁移的 Meme 代币，结合合约审计、持仓集中度、开发者仓位、税率和流动性，输出可解释的风险评分与重点警示。

### Long Description
`Meme 风控雷达` 面向需要高频筛选 Meme 机会的交易员、研究员、社群运营者和内容创作者。

它不是喊单工具，而是一个风险优先的筛选工作流：
- 从 Binance Web3 的 Meme Rush 获取新发或热度上升代币
- 自动补充 Token Audit 与 Token Info
- 计算统一风险分数并给出原因
- 支持中文和英文输出，方便直接用于研究、群推送和内容整理

适合用在这些场景：
- 每天快速筛出值得进一步研究的 Meme 币
- 在群里发出“先看哪些，先避开哪些”的晨报或快报
- 给研究流程补一层自动排雷，减少肉眼翻数据的时间

### Key Selling Points
- 风险优先，不直接鼓励下单
- 中英双语，适合面向全球用户
- 可解释评分，不是黑盒
- 默认只读，不要求交易 API Key
- 支持 SkillPay 按次收费，适合低门槛试用

### Suggested Pricing Copy
- 免费：`health` 检查
- 付费：每次 `scan` / `audit` 扣费
- 建议初始定价：`0.002 USDT / 次`
- 文案建议：按次付费，只为真正可执行的风控筛选买单

### Suggested Tags
- meme
- risk
- audit
- binance
- research
- bilingual

### Install Notes
- 本 skill 默认只读，不会自动交易
- 如启用付费调用，请通过环境变量提供 `SKILLPAY_APIKEY`
- 建议先用 `SKILLPAY_BILLING_MODE=noop` 本地验证流程

### Disclaimer
本技能仅提供信息整理与风险筛查，不构成任何投资、交易或收益承诺。高风险资产价格波动剧烈，请自行研究并独立决策。

## English Listing Copy

### Title
Meme Risk Radar

### Subtitle
Bilingual meme token risk scanner powered by Binance Web3 with pay-per-use billing.

### One-line Pitch
Discover first, filter fast. Turn meme token noise into an explainable risk-ranked shortlist.

### Short Description
Scan newly launched, finalizing, or recently migrated meme tokens, then enrich them with contract audit, holder concentration, developer exposure, tax, and liquidity checks.

### Long Description
`Meme Risk Radar` is built for traders, researchers, alpha communities, and content operators who need faster meme token triage.

This is not a trade execution bot. It is a risk-first workflow that:
- pulls fresh candidates from Binance Web3 Meme Rush
- enriches each token with Token Audit and Token Info
- computes a normalized risk score with visible reasons
- returns the report in Chinese or English for research, alerts, or publishing workflows

Common use cases:
- build a short research list from noisy meme launches
- publish "watch / avoid" updates for your community
- add a lightweight risk filter before deeper manual analysis

### Key Selling Points
- Risk-first workflow instead of blind signal chasing
- Bilingual output for Chinese and global users
- Explainable scoring, not a black box
- Read-only by default, no trading API key required
- SkillPay-friendly pay-per-use monetization

### Suggested Pricing Copy
- Free: `health` checks
- Paid: each `scan` / `audit` call
- Suggested launch price: `0.002 USDT per call`
- Recommended wording: pay only for actionable risk filtering, not raw token noise

### Suggested Tags
- meme
- risk
- audit
- binance
- research
- bilingual

### Install Notes
- This skill is read-only by default and does not auto-trade
- Provide `SKILLPAY_APIKEY` via environment variable for paid calls
- Start with `SKILLPAY_BILLING_MODE=noop` for local validation

### Disclaimer
This skill provides information aggregation and risk screening only. It is not investment advice, not a trading recommendation, and does not guarantee outcomes.

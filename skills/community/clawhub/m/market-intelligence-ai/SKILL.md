---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_4d1eb3b65cc411f19299525400d9a7a1
    ReservedCode1: UYycvFRoXvGRO/Fb82nBnWwYCcqNb0lBT3/6eLD0cMflBbOsS3sq5pgYf4HhLXL3nTLfL63Ui91FNuxvtFWAw8yuXRbKpE+CBOjPkv/3u7MKyYBvULTxs/Vutr9AnxRXZyJgHMQELQ3MxynWosx7xVWDa1rtlObOTad9/QuVJe1hPMDHbj8Ghw6mXUk=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_4d1eb3b65cc411f19299525400d9a7a1
    ReservedCode2: UYycvFRoXvGRO/Fb82nBnWwYCcqNb0lBT3/6eLD0cMflBbOsS3sq5pgYf4HhLXL3nTLfL63Ui91FNuxvtFWAw8yuXRbKpE+CBOjPkv/3u7MKyYBvULTxs/Vutr9AnxRXZyJgHMQELQ3MxynWosx7xVWDa1rtlObOTad9/QuVJe1hPMDHbj8Ghw6mXUk=
---



# 市场数据洞察 · 竞品监控报告生成器

为企业主、市场人员、电商卖家提供自动化的市场情报采集与分析服务。

## 功能分级与定价

| 档位 | 价格 | 功能 | 输出 |
|------|------|------|------|
| **基础版** | 免费 | Top 5 商品排名 + 价格 | 纯文本列表 |
| **进阶版** | ¥2.99 / 次 | Top 10 排名 + 趋势图表 + 竞品分析 + 建议 | 完整 Markdown 报告 |
| **专业版** | ¥29.9 / 月 | 进阶版全部 + 72h 持续监控 + 价格变动通知 | 报告 + 实时告警 |

## 触发场景

- "分析空气炸锅在 Amazon 上的 Top 10 销量"
- "监控竞品店铺 https://xxx 的价格变动"
- "蓝牙耳机这个品类最近有什么趋势"
- "帮我做一份扫地机器人的市场报告"
- "追踪这些 ASIN 的价格：B0A1B2C3D4, B0E5F6G7H8"

## 环境变量

| 变量 | 必填 | 说明 | 默认值 |
|------|:--:|------|--------|
| `ALIPAY_APP_ID` | ✅ | 支付宝 AI 收应用 ID | 无，必须配置 |
| `ALIPAY_PRIVATE_KEY_PATH` | ✅ (付费) | 支付宝应用私钥文件路径 | 无 |
| `KEEPA_API_KEY` | 否 | Keepa 价格追踪 API | 未配置时用备用源 |
| `AMAZON_ACCESS_KEY` + `AMAZON_SECRET_KEY` | 否 | Amazon PAAPI 5.0 | 未配置时降级 |
| `SERPAPI_KEY` | 否 | SerpAPI / Google Shopping | 未配置时降级 |
| `STOCK_API_KEY` | 否 | 金融市场数据（可选） | 无 |

## 执行流程

### 阶段 0 — 档位判定

根据用户请求自动判定档位：

| 用户表述特征 | 判定档位 |
|-------------|----------|
| "看看" / "查一下" / "有哪些" / 无明确图表要求 | → 基础版（免费） |
| "完整报告" / "图表" / "分析" / "对比" / "建议" | → 进阶版（¥2.99） |
| "监控" / "追踪" / "通知" / "定时" | → 专业版（¥29.9/月） |

### 阶段 1 — 数据采集（基础版、进阶版共用）

按优先级尝试数据源（参考 `{baseDir}/references/market_data_sources.md`）：

```
PAAPI 5.0 → Keepa → Rainforest API → SerpAPI → 公开数据集（降级）
```

1. 解析用户输入：提取产品关键词 / ASIN / 店铺 URL
2. 选择合适的 Amazon 站点（默认 `domain=1` 即美国站）
3. 查询商品列表：搜索关键词 → 获取 Top 5 或 Top 10 ASIN
4. 对每个 ASIN 查询详情：标题、价格、BSR 排名、评分、评论数
5. 如有 Keepa API，拉取 90 天价格历史用于趋势图

**请求频率限制**：严格 ≤ 1次/秒/源，单次任务总请求 ≤ 20 次。

### 阶段 2 — 支付宝 AI 收询价（仅进阶版、专业版触发）

当判定为进阶版或专业版时，**在生成完整报告前**触发支付宝 AI 收流程：

```
Agent → 服务端：POST {ALIPAY_SERVER_URL}/create-payment
  Body: { "tier": "advanced", "amount": 2.99, "product": "{关键词}" }
服务端 → Agent：HTTP 402 + payment_url
Agent → 用户：展示支付二维码
用户 → 支付宝：扫码支付 ¥2.99
支付宝 → 服务端：异步通知支付成功
Agent → 服务端：带支付凭证重试
服务端 → Agent：验证通过，返回完整报告数据
```

**专业版订阅**：首次触发时创建支付宝周期扣款协议，后续监控任务自动续费。

> 参考：[支付宝 AI 收接入指南](https://opendocs.alipay.com/open/ai-receipt)

### 阶段 3 — 语义分析与报告生成

基于采集数据，执行以下分析步骤（确定性规则，无 AI 自由裁量）：

1. **排名评分**：`Score = (1 - BSR_percentile) × avg_rating × log(review_count + 1)`
2. **价格带分析**：按价格从低到高分 3 档（经济型/中端/高端），每档标注商品数
3. **竞争度评估**：评论数 > 1000 → 红海市场 / 100~1000 → 竞争适中 / < 100 → 蓝海机会
4. **趋势判断**（有价格历史时）：90 天内价格上涨 → 📈 看涨 / 下跌 → 📉 看跌 / 波动 ≤ 5% → 稳定
5. **建议总结**：基于以上 4 项指标综合输出 3-5 条可操作建议

### 阶段 4 — 专业版持续监控（仅专业版）

1. 每 4 小时重新采集一次目标商品数据（72 小时内共 18 轮）
2. 价格变动超过 ±5% 时即时通知用户
3. 监控结束后生成一份汇总趋势报告

## 输出格式

### 基础版输出示例

```
## 市场快照：空气炸锅（Amazon US）
采集时间：2026-05-31 15:00 CST | 数据源：Amazon PAAPI

| 排名 | 商品 | 价格 | 评分 | 评论数 |
|------|------|------|------|--------|
| #1 | COSORI Air Fryer 9-in-1 | $89.99 | 4.7 | 124,563 |
| #2 | Ninja AF101 | $79.99 | 4.6 | 98,221 |
| #3 | Instant Vortex Plus | $69.95 | 4.5 | 45,332 |
| #4 | Chefman TurboFry | $49.99 | 4.4 | 67,891 |
| #5 | GoWISE USA GW44800 | $59.99 | 4.3 | 52,110 |

价格区间：$49.99 ~ $89.99 | 均价：$69.98
```

### 进阶版/专业版输出示例

```markdown
# 市场洞察报告：空气炸锅品类分析
**生成时间**：2026-05-31 15:00 CST
**数据源**：Amazon PAAPI + Keepa 价格历史
**覆盖站点**：Amazon.com (US)

---

## 一、Top 10 商品排名

（省略表格，同基础版格式扩展到 Top 10）

## 二、价格趋势分析

（基于 Keepa 90 天价格历史）

## 三、竞争度评估

| 价格带 | 商品数 | 平均评论数 | 竞争度 |
|--------|--------|-----------|--------|
| 经济型 ($40-60) | 3 | 45,210 | 🟡 竞争适中 |
| 中端 ($60-90) | 5 | 98,450 | 🔴 红海市场 |
| 高端 ($90-150) | 2 | 12,340 | 🟢 蓝海机会 |

## 四、建议总结

1. 经济型价位评论增速最快，建议关注差异化功能
2. 高端市场竞品少、溢价空间大，品牌化机会明显
3. 头部商品（COSORI/Ninja）护城河深，新入局建议避开正面竞争
4. 近期 5 款新品集中在"智能App控制"卖点，值得跟进

---

> ⚠️ 免责声明：本报告基于公开数据自动生成，仅供参考，不构成投资或商业决策建议。
```

## 工具依赖

| 工具 | 用途 | 调用阶段 |
|------|------|:--:|
| `web_search` | 补充搜索商品信息和行业新闻 | 阶段 1 |
| `web_fetch` | 抓取电商页面结构化数据 | 阶段 1 |
| `browser` | 处理 JS 渲染页面和反爬场景 | 阶段 1（备用） |
| `analyze_image` | 截图分析（图表 OCR / 验证码识别） | 阶段 1（备用） |
| `shell_executor` | 执行 Python 数据聚合脚本 | 阶段 3 |
| 支付宝 AI 收 SDK | HTTP 402 询价 / 支付验证 | 阶段 2 |

## 注意事项

- 所有 API Key 通过环境变量注入，禁止在 SKILL.md 中硬编码
- 数据采集严格限制频率，避免触发反爬或 API 限流
- 报告中标注数据源和采集时间，确保可追溯
- 遇到所有 API 不可用时，降级为静态公开数据集并提供免责声明
- 专业版订阅到期后自动停止监控，不再续费需用户确认

## references 参考文档

| 文档 | 说明 |
|------|------|
| `{baseDir}/references/market_data_sources.md` | 数据源列表、API 端点、请求示例、降级策略 |
| `{baseDir}/references/clawhub-review-checklist.md` | ClawHub 发布前自检清单 |
*（内容由AI生成，仅供参考）*

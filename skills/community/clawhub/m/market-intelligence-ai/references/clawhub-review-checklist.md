---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_4e4e7a5d5cc411f19299525400d9a7a1
    ReservedCode1: Qye5rRnuqGEwTjj/Z1J1QjE8ttfk0rJdQa0KrtXfy6if5SYdC/TH4+QmrC/gKT2M4Iz1Gl7biTr+/XUyuXZxOcDUkmzg+9KzAvG4YfcCvi6d0RN+IHvzo/IUvziA/RzJ157wGlC7VPhZgVZhpfEFFPCJIfNJS9OStSl8EAk47gT9sA4mmzjsc5B3RyE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_4e4e7a5d5cc411f19299525400d9a7a1
    ReservedCode2: Qye5rRnuqGEwTjj/Z1J1QjE8ttfk0rJdQa0KrtXfy6if5SYdC/TH4+QmrC/gKT2M4Iz1Gl7biTr+/XUyuXZxOcDUkmzg+9KzAvG4YfcCvi6d0RN+IHvzo/IUvziA/RzJ157wGlC7VPhZgVZhpfEFFPCJIfNJS9OStSl8EAk47gT9sA4mmzjsc5B3RyE=
---

# ClawHub 技能审核自检清单

本文件用于发布前自查，确保技能包通过 ClawHub 审核。

---

## 一、元数据完整性

- [ ] SKILL.md 包含合法 YAML frontmatter（`---` 包裹）
- [ ] `name`（slug）与文件夹名称一致
- [ ] `description` 清晰描述技能用途和适用场景
- [ ] `version` 使用语义化版本号（如 `1.0.0`）
- [ ] `author` 字段已填写
- [ ] `metadata.openclaw.emoji` 已设置（非必填但推荐）
- [ ] `metadata.openclaw.requires` 声明了环境变量依赖

## 二、环境变量声明

- [ ] 所有 `requires.env` 中的变量都在 SKILL.md 正文中解释了用途和默认值
- [ ] 必填变量标注「必须配置」，选填变量标注默认值
- [ ] API Key 类变量说明获取方式（注册链接或文档 URL）

**本技能环境变量列表：**

| 变量名 | 必填 | 说明 | 获取方式 |
|--------|:--:|------|----------|
| `KEEPA_API_KEY` | 否 | Keepa API 密钥 | 注册 keepa.com |
| `AMAZON_ACCESS_KEY` | 否 | AWS Access Key | AWS IAM 控制台 |
| `AMAZON_SECRET_KEY` | 否 | AWS Secret Key | AWS IAM 控制台 |
| `SERPAPI_KEY` | 否 | SerpAPI 密钥 | 注册 serpapi.com |
| `ALIPAY_APP_ID` | 是 | 支付宝 AI 收应用 ID | 支付宝开放平台 |
| `STOCK_API_KEY` | 否 | 金融市场数据 API | Alpha Vantage / Finnhub |

## 三、文件行为说明

- [ ] 技能内所有脚本/代码仅执行 **确定性数据采集与报告生成**，无 AI 自主决策链路
- [ ] 不写入任何系统目录（仅写入用户指定的输出路径或技能包内临时目录）
- [ ] 采集频率限制：每个数据源 ≤ 1 次/秒，单次查询总请求 ≤ 20 次
- [ ] 所有 HTTP 请求显式声明 User-Agent：`MarketIntelligenceAI/1.0`

## 四、凭证与密钥安全

- [ ] **全部 API Key 通过环境变量注入**，不在 SKILL.md 或 references 中硬编码
- [ ] 支付宝私钥通过环境变量 `ALIPAY_PRIVATE_KEY_PATH` 指向文件路径（非内容）
- [ ] 示例参数中使用占位符（`{YOUR_KEY}`、`YOUR_APP_ID`），而非真实凭证

## 五、定价声明

- [ ] SKILL.md 清晰区分免费/付费功能边界
- [ ] 付费功能触发前必须通过支付宝 AI 收 SDK 发起询价（HTTP 402 协议）
- [ ] 用户确认支付后才会生成付费报告内容

**本技能定价表：**

| 档位 | 价格 | 触发条件 | 输出内容 |
|------|------|----------|----------|
| 基础版 | 免费 | 默认 | Top 5 商品排名 + 价格，纯文本 |
| 进阶版 | ¥2.99/次 | 用户要求图表/完整分析 | 趋势图表 + 竞品分析，Markdown 报告 |
| 专业版 | ¥29.9/月 | 用户要求持续监控 | 72 小时监控 + 变动通知 |

## 六、输出格式

- [ ] 基础版输出：纯文本列表格式，不含图表
- [ ] 进阶版/专业版输出：Markdown 格式，包含结构化表格、ASCII 趋势图或数据可视化描述
- [ ] 报告中标注数据来源和采集时间
- [ ] 免责声明：「本报告基于公开数据，仅供参考，不构成投资或商业决策建议」

## 七、references 目录

- [ ] `references/` 目录下所有文件通过 SKILL.md 内的相对路径引用
- [ ] 引用格式：`{baseDir}/references/文件名.md`
- [ ] 参考文档不含可执行代码

## 八、示例参数一致性

- [ ] 示例关键词（如"空气炸锅"）为中性通用词，不涉及特定品牌
- [ ] 示例 URL 使用 `example.com` 或占位符而非真实竞品链接
- [ ] 示例输出中的价格/销量为模拟数据，标注「示例」

---

**自检结论：**

以上 8 大类共 28 项检查，逐项确认后即可提交 ClawHub 审核。
*（内容由AI生成，仅供参考）*

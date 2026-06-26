---
name: 行业垂直知识层
description: 10 个 Type Agent 共用的行业专属知识库 — 解决"通用框架套所有行业"导致的平庸问题
version: "5.2.1"
shared: true
---

# 行业垂直知识层 (v5.2.1)

> **本目录是 v5.1 新增、v5.2 扩展、v5.2.1 国际化扩展的 Cold Layer 资源**。每个行业一个文件，按需引用。
> 解决评估报告指出的"10 个 Agent 横向覆盖但缺少行业垂直深度+国际化覆盖"问题。

---

## 🧭 何时引用

| 触发条件 | 引用动作 |
|---------|---------|
| Intake Agent 检测到行业关键词 | 在 Brief 中标注 `industry: [industry-id]` |
| Type Agent 产出方案前 | 调用 load_industry_knowledge(industry_id) 加载对应文件 |
| Benchmark 兜底时 | 优先用本行业的精确区间，而非通用数据库 |
| Tournament / Adversarial 评审 | 引用本行业的"典型雷区"做攻击 |
| Compliance Guard 拦截 | 加载本行业的 Blocker 关键词清单 |

---

## 📚 已支持的行业（v5.2：10 个行业全覆盖）

| 行业 ID | 名称 | 文件 | 关键特征 |
|--------|------|------|---------|
| `beauty` | 美妆个护 | [beauty-personal-care.md](./beauty-personal-care.md) | 高频高复购、强 KOL、强监管（功效宣称） |
| `fnb` | 食品饮料 | [fnb.md](./fnb.md) | 即时消费、地域差异、季节性 |
| `3c` | 3C 数码 | [3c-digital.md](./3c-digital.md) | 高客单、长决策、参数驱动 |
| `maternity` | 母婴用品 | [maternity-baby.md](./maternity-baby.md) | 信任成本高、强合规、生命周期清晰 |
| `education` | 教育（职业/K12/成人） | [education.md](./education.md) | 线索型、长决策、强监管、双减 |
| `saas-b2b` | SaaS / B2B | [saas-b2b.md](./saas-b2b.md) | 长决策链、ABM、内容营销驱动 |
| `medical-aesthetic` | 医美 | [medical-aesthetic.md](./medical-aesthetic.md) | 高客单、强监管、医疗广告审查 |
| `apparel` | 服饰鞋包 | [apparel.md](./apparel.md) | 季节性、高退货、视觉驱动 |
| `finance` | 金融（信用卡/保险/财富） | [finance.md](./finance.md) | 强监管、信任门槛、长决策 |
| `automotive` | 汽车 | [automotive.md](./automotive.md) | 高客单、长决策、O2O 链路 |

### 🌐 国际扩展市场（v5.2.1 扩展至 8 个市场）

| 市场 ID | 名称 | 文件 | 覆盖国家/区域 |
|--------|------|------|-------------|
| `intl-japan` | 日本市场 | [intl-japan.md](./intl-japan.md) | 日本全域（LINE/YouTube/Instagram 生态） |
| `intl-korea` | 韩国市场 | [intl-korea.md](./intl-korea.md) | 韩国全域（Naver/KakaoTalk/Coupang 生态） |
| `intl-southeast-asia` | 东南亚市场 | [intl-southeast-asia.md](./intl-southeast-asia.md) | 印尼/泰国/越南/菲律宾/马来西亚/新加坡 |
| `intl-north-america` | 北美市场 | [intl-north-america.md](./intl-north-america.md) | 美国/加拿大（Google/Meta/Amazon/TikTok 生态） |
| `intl-europe` | 欧洲市场 | [intl-europe.md](./intl-europe.md) | 英/德/法/北欧/南欧/东欧（GDPR/DSA 生态） |
| `intl-middle-east` | 中东北非市场 | [intl-middle-east.md](./intl-middle-east.md) | GCC（沙特/UAE/卡塔尔）、埃及、北非 |
| `intl-central-asia` | 中亚市场 | [intl-central-asia.md](./intl-central-asia.md) | 哈萨克斯坦/乌兹别克斯坦/吉尔吉斯/蒙古 |
| `intl-africa` | 非洲市场 | [intl-africa.md](./intl-africa.md) | 南非/尼日利亚/肯尼亚/加纳/埃塞俄比亚 |

> **未覆盖行业/市场**：用户提及未列出的行业或国际市场时，Intake Agent 应标注 `industry: "custom"` 或 `market: "custom"`，Type Agent 退回到通用 benchmark，并提示用户"该行业/市场暂无专属知识库，输出基于通用框架"。

---

## 📐 每个行业文件的统一结构

```markdown
# [行业名] 营销知识库

## 1. 行业概览
- 市场规模 / 增长率 / 关键趋势
- 大促节点 / 季节性
- 主要玩家与竞争格局

## 2. 消费者决策路径
- 典型决策周期
- 信息获取渠道（社交/搜索/电商/线下）
- 关键决策因子
- 典型转化漏斗

## 3. 渠道权重矩阵
- 各平台优先级（抖音/小红书/微信/B站/微博/快手/...）
- 各平台内容形式偏好
- 渠道预算分配建议

## 4. 精确 KPI 区间
（比 benchmark-database.md 更细的行业专属数据）
- CPM / CPC / CTR / CVR / CAC / LTV / ROAS
- 大促调整系数

## 5. 合规与监管
- 广告法专属限制
- 功效宣称边界
- 平台审核红线
- 行业特殊资质要求

## 6. 典型 Campaign 节奏
- 新品上市
- 大促（618 / 双11 / 行业节点）
- 日常种草
- 品牌建设

## 7. 常见雷区（Adversarial 攻击参考）
- "看着对实际错"的典型陷阱
- 同品类翻车案例
- AI 方案容易踩的坑

## 8. 推荐方法论组合
（叠加在 marketing-frameworks.md 之上）
- 该行业最有效的 2-3 个方法论
- 不推荐的方法论及原因
```

---

## 🔗 引用方式

在 Type Agent 的 `main-agent.md` 中：

```markdown
## 行业知识引用

本 Agent 在产出方案前，必须检查 Brief 的 `industry` 字段：
- 若匹配已支持的行业 ID → Read `<skill-base>/references/industries/[industry-id].md`
- 若未匹配 → 退回 `<skill-base>/references/benchmark-database.md` 通用数据
- 在输出方案中明确标注："本方案基于 [行业名] 行业知识库产出"
```

在 Intake Agent 中：

```markdown
## 行业识别（v5.1 新增）

在第 1 轮追问中，必须明确识别用户所在行业。识别策略：
1. 用户明确说出行业名 → 直接映射
2. 用户说出品类（如"口红""精华"）→ 反推行业
3. 模糊表述（如"消费品"）→ 提供行业选项让用户选择

输出 Brief 时，必须包含 `industry` 字段，值为本目录的行业 ID 或 `custom`。
```

---

## 🆕 扩展规范

新增行业文件时：
1. 文件名：`[industry-id].md`，全小写，连字符分隔
2. 必须遵循上述 8 节统一结构
3. KPI 数据必须明确数据来源（公开报告 / 行业经验估算）
4. 合规模块必须经过本地法律/合规顾问审阅（AI 产出后必须人工 review）
5. 在本 README 的"已支持的行业"表中注册

---

*文档版本：v5.1 | 最后更新：2026-06-08*

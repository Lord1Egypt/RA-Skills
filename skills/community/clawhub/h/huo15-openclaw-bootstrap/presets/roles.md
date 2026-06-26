# 角色预设库（Role Presets）· 49 款

> 角色 = 岗位/职业，决定龙虾带哪套领域知识、默认工具链、默认关心的问题。
> 允许 **1 主 + 0-2 辅**，共最多 3 个叠加（承认斜杠青年）。

---

## 条目结构

```
<slug>
**<中文名> / <English name>**
定位：一句话说清这个角色在做什么
关心三问：A / B / C
默认工具链：T1, T2, T3
融合示例：+ X → Y
```

---

## 一、技术工程（Engineering）· 15 款

### 1. fullstack-engineer
**全栈工程师 / Full-stack Engineer**
- 定位：前后端都能写，独立交付端到端功能
- 关心三问：接口设计 / 性能 / 部署
- 默认工具链：TypeScript / Node.js / Docker / CI/CD
- 融合示例：+ 独立开发者 → indie hacker 的标配

### 2. frontend-engineer
**前端工程师 / Frontend Engineer**
- 定位：浏览器和移动端的用户侧交互
- 关心三问：性能 / 可访问性 / 设计还原度
- 默认工具链：React / Vue / Tailwind / Vite

### 3. backend-engineer
**后端工程师 / Backend Engineer**
- 定位：服务端架构、API、数据模型
- 关心三问：吞吐 / 一致性 / 可扩展
- 默认工具链：Python / Go / Postgres / Redis

### 4. mobile-engineer
**移动开发工程师 / Mobile Engineer**
- 定位：iOS/Android/跨平台 App
- 关心三问：启动时间 / 内存 / 上架合规
- 默认工具链：Swift / Kotlin / React Native / Flutter

### 5. devops-engineer
**DevOps 工程师 / DevOps**
- 定位：CI/CD、基础设施、可观测性
- 关心三问：可用性 SLO / 部署频率 / MTTR
- 默认工具链：Kubernetes / Terraform / Grafana / GitHub Actions

### 6. sre
**SRE / Site Reliability Engineer**
- 定位：让线上稳如山
- 关心三问：错误预算 / on-call 体验 / post-mortem
- 默认工具链：Prometheus / PagerDuty / Runbook

### 7. security-engineer
**安全工程师 / Security Engineer**
- 定位：攻防、审计、合规
- 关心三问：OWASP / 依赖链 / 数据泄露
- 默认工具链：Burp / Semgrep / Snyk

### 8. data-engineer
**数据工程师 / Data Engineer**
- 定位：数据管道、仓库、湖
- 关心三问：新鲜度 / SLA / 血缘
- 默认工具链：Airflow / DBT / Spark / ClickHouse

### 9. data-scientist
**数据科学家 / Data Scientist**
- 定位：统计、建模、可视化
- 关心三问：样本偏差 / 可解释性 / 业务接入
- 默认工具链：Python / Jupyter / scikit-learn / statsmodels

### 10. data-analyst
**数据分析师 / Data Analyst**
- 定位：业务数据洞察
- 关心三问：北极星 / 漏斗 / 留存
- 默认工具链：SQL / Tableau / Metabase

### 11. ml-researcher
**AI/ML 研究员 / ML Researcher**
- 定位：模型、算法、论文
- 关心三问：SOTA / 可复现 / 可扩展
- 默认工具链：PyTorch / Weights & Biases / HuggingFace

### 12. prompt-engineer
**提示词工程师 / Prompt Engineer**
- 定位：LLM 应用层、Agent、RAG
- 关心三问：幻觉率 / 成本 / 延迟
- 默认工具链：Claude/OpenAI SDK / LangGraph / vector DB

### 13. game-engineer
**游戏开发工程师 / Game Engineer**
- 定位：引擎、渲染、玩法编程
- 关心三问：帧率 / 包体 / 手感
- 默认工具链：Unity / Unreal / Godot

### 14. embedded-engineer
**嵌入式工程师 / Embedded Engineer**
- 定位：IoT、硬件固件、实时系统
- 关心三问：功耗 / RTOS / 通信
- 默认工具链：C / Rust / ESP32 / STM32

### 15. blockchain-engineer
**区块链工程师 / Blockchain Engineer**
- 定位：智能合约、DApp、链上
- 关心三问：安全审计 / gas / 去中心化
- 默认工具链：Solidity / Foundry / Ethers.js

---

## 二、产品设计（Product & Design）· 10 款

### 16. product-manager
**产品经理 / Product Manager**
- 定位：需求发现、优先级、落地
- 关心三问：痛点 / 场景 / 闭环
- 默认工具链：Figma / Notion / 飞书 / Jira

### 17. product-director
**产品总监 / Product Director**
- 定位：产品线、路线图、跨团队
- 关心三问：战略 / 资源 / 组织
- 默认工具链：OKR / Roadmap / 季度复盘

### 18. ui-designer
**UI 设计师 / UI Designer**
- 定位：界面视觉、设计系统
- 关心三问：层级 / 呼吸 / 一致性
- 默认工具链：Figma / Sketch / Principle

### 19. ux-designer
**UX 设计师 / UX Designer**
- 定位：交互、信息架构、用户研究
- 关心三问：任务流 / 可用性 / 心智模型
- 默认工具链：Figma / Miro / Maze

### 20. product-designer
**产品设计师 / Product Designer**
- 定位：端到端的设计落地（UI+UX+协作）
- 关心三问：交付 / 开发对齐 / 上线数据
- 默认工具链：Figma / FigJam / Storybook

### 21. brand-designer
**品牌设计师 / Brand Designer**
- 定位：VI、品牌故事、视觉系统
- 关心三问：辨识度 / 调性 / 延展性
- 默认工具链：Illustrator / Figma / 字体库

### 22. graphic-designer
**平面设计师 / Graphic Designer**
- 定位：海报、banner、印刷物
- 关心三问：构图 / 字体 / 色彩
- 默认工具链：Photoshop / Illustrator / InDesign

### 23. illustrator
**插画师 / Illustrator**
- 定位：插画、IP、绘本
- 关心三问：风格 / 情感 / 讲故事
- 默认工具链：Procreate / CSP / Photoshop

### 24. motion-designer
**动效设计师 / Motion Designer**
- 定位：界面动效、MG、品牌动画
- 关心三问：节奏 / 缓动 / 性能
- 默认工具链：After Effects / Lottie / Rive

### 25. industrial-designer
**工业设计师 / Industrial Designer**
- 定位：硬件产品的形态与工艺
- 关心三问：人机 / 材质 / 量产
- 默认工具链：Rhino / KeyShot / Solidworks

---

## 三、内容创作（Content）· 9 款

### 26. tech-writer
**技术作者 / Tech Writer**
- 定位：博客、文档、教程、图书
- 关心三问：受众 / 结构 / 可复现
- 默认工具链：Obsidian / Notion / Markdown / VS Code

### 27. self-media-writer
**自媒体作者 / Self-media Writer**
- 定位：公众号、知乎、博客运营
- 关心三问：选题 / 开头 3 句 / 标题
- 默认工具链：Notion / 秀米 / 壹伴

### 28. xiaohongshu-creator
**小红书博主 / 种草达人 / Xiaohongshu Creator**
- 定位：图文种草、生活方式分享、品牌合作 / 探店
- 关心三问：封面第一眼 / 爆文率 / 粉丝画像
- 默认工具链：小红书 App / 醒图 / VSCO / Lightroom / Notion
- 融合示例：+ 摄影师 → 高质量视觉种草；+ 文案 → 标题工厂

### 29. short-video-creator
**短视频创作者 / Short Video Creator**
- 定位：抖音 / 视频号 / TikTok 短视频
- 关心三问：前 3 秒 / 节奏 / 完播率
- 默认工具链：剪映 / Premiere / CapCut

### 30. youtuber
**视频博主 / YouTuber / B 站 UP 主**
- 定位：长视频、频道运营
- 关心三问：选题 / CTR / 留存曲线
- 默认工具链：Premiere / DaVinci / OBS

### 31. podcaster
**播客主 / Podcaster**
- 定位：音频节目、访谈
- 关心三问：选题 / 嘉宾 / 收听曲线
- 默认工具链：Adobe Audition / Descript / Spotify

### 32. copywriter
**文案 / Copywriter**
- 定位：广告、banner、品牌文案
- 关心三问：转化 / 调性 / 记忆点
- 默认工具链：Hemingway / Notion / Figma

### 33. novelist
**小说作家 / Novelist**
- 定位：长篇虚构、连载、剧本
- 关心三问：人物弧 / 冲突 / 世界观
- 默认工具链：Scrivener / Obsidian / WPS

### 34. photographer
**摄影师 / Photographer**
- 定位：商业 / 人像 / 纪实摄影
- 关心三问：光 / 构图 / 情绪
- 默认工具链：Lightroom / Capture One / Photoshop

---

## 四、商业运营（Business）· 15 款

### 35. founder
**创业者 / Founder**
- 定位：从 0 到 1 / 1 到 10
- 关心三问：PMF / 现金流 / 团队
- 默认工具链：Notion / 飞书 / 数据看板

### 36. indie-developer
**独立开发者 / Indie Developer**
- 定位：一人或小团队的 SaaS/工具
- 关心三问：MRR / 留存 / 获客成本
- 默认工具链：Stripe / Posthog / Intercom

### 37. ceo
**CEO / 总经理**
- 定位：公司一把手、对结果负责
- 关心三问：战略 / 现金 / 人
- 默认工具链：OKR / 财报 / 董事会

### 38. marketing-specialist
**市场营销 / Marketing Specialist**
- 定位：品牌、投放、活动
- 关心三问：ROI / 转化漏斗 / 品牌声量
- 默认工具链：GA / 巨量 / 腾讯广告

### 39. growth-hacker
**增长黑客 / Growth Hacker**
- 定位：病毒增长、转化优化
- 关心三问：AARRR / 实验 / 闭环
- 默认工具链：Mixpanel / Amplitude / Growthbook

### 40. ops-specialist
**运营专员 / Operations Specialist**
- 定位：用户/内容/活动运营
- 关心三问：留存 / 活跃 / 互动
- 默认工具链：企微 / 社群工具 / 表格

### 41. ecommerce-ops
**电商运营 / E-commerce Operator**
- 定位：淘宝/天猫/京东/拼多多/抖店
- 关心三问：GMV / 坑产 / 退货率
- 默认工具链：生意参谋 / 直播后台 / ERP

### 42. cross-border-ecom
**跨境电商 / Cross-border E-commerce**
- 定位：亚马逊/Shopify/TikTok Shop
- 关心三问：选品 / ACoS / 物流
- 默认工具链：Helium10 / Shopify / 货代系统

### 43. sales-rep
**销售代表 / Sales Rep**
- 定位：直接出货、关系经营
- 关心三问：转化 / 客单 / 复购
- 默认工具链：CRM / 企微 / 飞书

### 44. account-manager
**客户成功 / Customer Success**
- 定位：续费、扩展、满意度
- 关心三问：NPS / 续费 / expansion
- 默认工具链：CRM / QBR / 健康度指标

### 45. consultant
**咨询顾问 / Consultant**
- 定位：战略、组织、流程
- 关心三问：诊断 / 方案 / 落地
- 默认工具链：PPT / 财务模型 / 访谈

### 46. investor
**投资人 / Investor**
- 定位：VC/PE/天使/FA
- 关心三问：赛道 / 团队 / 护城河
- 默认工具链：市场分析 / DCF / DD

### 47. hr
**HR / 人力资源**
- 定位：招聘、培训、组织
- 关心三问：JD / 留存 / 文化
- 默认工具链：Boss / Moka / 绩效系统

### 48. legal-counsel
**法务顾问 / Legal Counsel**
- 定位：合同、合规、IP
- 关心三问：合规 / 风险 / 条款
- 默认工具链：合同管理 / 法规库

### 49. finance-accountant
**财务/会计 / Finance & Accounting**
- 定位：账务、税务、现金流
- 关心三问：现金 / 税 / 合规
- 默认工具链：Excel / 金蝶 / 用友

---

## 经典角色叠加（Role Stacks）

这些组合在现实中非常常见，推荐直接抄：

| 组合 | 含义 | 典型场景 |
|------|------|---------|
| 全栈 + PM + 独立开发者 | 一人 SaaS 主理人 | Indie Hacker |
| PM + 数据分析师 | 数据驱动型 PM | 增长 PM |
| 前端 + UI 设计师 | 能写能画 | Design Engineer |
| AI/ML + Prompt 工程师 | LLM 应用开发者 | AI 产品 |
| 品牌 + UI 设计师 | 设计 lead | 初创公司唯一设计 |
| 自媒体 + 短视频 + 文案 | 内容 IP | 个人品牌 |
| 小红书 + 摄影师 + 文案 | 高质量种草达人 | 个人 IP / 探店 / 美妆 |
| 小红书 + 品牌设计师 + 电商 | 独立女装 / 手作品牌 | 设计师创立自有品牌 |
| 创业者 + 销售 + PM | 创始人 CEO | 早期公司 |
| DevOps + SRE | 平台工程 | 中台团队 |
| 数据工程师 + 数据科学家 | Full-cycle DS | 数据团队 |
| 法务 + 财务 | 后台双剑 | 小公司 CFO |

---

## 冲突清单（不建议同选）

以下组合职责背离，同选会让龙虾默认优先级混乱：

- ❌ 投资人 × 创业者（视角根本对立 —— 除非要做"自问自答"演练）
- ❌ 法务 × 增长黑客（一个求稳一个求快）
- ❌ SRE × 深圳创业者路线（稳定 vs 糙快猛）

**规则**：冲突组合允许选，但龙虾要提示"你这组会产生自相矛盾的建议，要不要我按场景切换？"

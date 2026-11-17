## 三、人才寻访 — 渠道、Boolean、GitHub 与被动候选人

### 寻访渠道优先级矩阵

### 按行业推荐最优寻访路径

| 行业 | 首选渠道 | 备选渠道 | 深度渠道 | AI 增强 |
|------|---------|---------|---------|---------|
| 快消零售 | 猎聘/脉脉 | 领英/行业社群 | 线下展会/经销商网络 | AI 批量扫描 LinkedIn |
| 金融 | 领英/猎聘 | 脉脉/金融社群 | CFA/FRM 协会/校友网络 | PeopleGPT 聚合 |
| 新能源 | 猎聘/BOSS | 领英/技术论坛 | 行业峰会/供应商网络 | AI 行业趋势扫描 |
| 医疗医药 | 猎聘/丁香人才 | 领英/学术社群 | 医学会议/CRO 网络 | FidForward 扫描 |
| 互联网/科技 | 脉脉/Boss | 领英/GitHub | **GitHub 开源社区** + 技术大会 | Calyflow 6 步自动化 |
| 半导体/芯片 | 猎聘/脉脉 | 领英/技术论坛 | 学术会议/实验室 | AI 论文/专利追踪 |

***


### ⏱️ 寻访时效标准

> **48-72 小时内启动寻访**是行业参考基准

### 寻访启动 Checklist

1. **关键词确定** — 从 JD 提取 3-5 核心词
2. **平台选择** — 按渠道优先级矩阵
3. **Boolean 构建** — 精准关键词组合
4. **首批 Longlist 生成** — AI 批量扫描 + 人工复核
5. **交叉验证** — 多平台比对候选人信息

### 寻访节奏

| 阶段 | 时间 | 动作 |
|------|------|------|
| Day 0-1 | JD 收到 | 分析 JD + 构建画像 + Boolean |
| Day 1-2 | 启动寻访 | 首批 Longlist（20-30 人） |
| Day 2-3 | 筛选 | Shortlist（5-8 人） |
| Day 3-5 | 触达 | 首次联系 + 价值先行

***


### 🐙 GitHub 开源人才寻访引擎

> **核心理念**：开源贡献 = 最真实的技术能力证明
> GitHub 上有活跃贡献的工程师，往往比简历上写的更靠谱

### 前置准备

**安装 GitHub Skills：**
- `github-cli` — 全面 GitHub CLI 操作
- `github-search` — 仓库深度搜索与分析
- `openclaw-github-assistant` — 仓库/Issue/CI 管理
- `github-workflow` — Actions/PR 工作流
- `github-actions-generator` — CI/CD 场景生成

**认证配置：**
```bash
# 方法 1：GitHub Personal Access Token
GitHub Settings → Developer Settings → Personal Access Tokens → 生成 token（建议 scope: repo, read:user）
export GITHUB_TOKEN="your_personal_access_token"

# 方法 2：GitHub CLI 登录
gh auth login
```

### A. 技术关键词 → 候选人发现

**使用场景：** [猎头顾问姓名] 需要找特定技术栈的人才（如 Kubernetes/Go/AI 工程师）

```bash
# 1. 搜索相关热门仓库
gh search repos "kubernetes operator" --language go --stars ">100" --sort stars

# 2. 搜索活跃贡献者
gh search code "kubernetes" --language go --repo owner/repo

# 3. 追踪高频提交者
gh search commits "fix bug" --author monalisa --repo owner/repo
```

**猎头工作流：**
1. 根据 JD 技术栈 → 提取 3-5 个关键词
2. `gh search repos [关键词]` → 找相关热门项目
3. 提取项目 maintainer/top contributors
4. 交叉比对 → 建立技术人才候选列表
5. 尝试通过 GitHub profile 联系（邮箱/Linkedin 推断）

### B. 目标公司技术栈监控

**使用场景：** 了解目标公司正在用什么技术，推断招聘需求

```bash
# 查看公司开源项目
gh search repos --owner=company-name --sort updated

# 查看 CI/CD 活跃度
gh run list --workflow build.yml --limit 20

# 查看 Issue 增长（= 招聘信号）
gh issue list --state open --limit 50
```

**Hiring Signals from GitHub：**
- 📈 **新仓库创建** → 新业务线启动 → 需要招人
- 🔥 **CI/CD 活跃度飙升** → 项目加速 → 可能缺人
- 📝 **大量 open issues** → 人手不足 → 招聘窗口
- 🔄 **高频 contributor turnover** → 可能有人离职

### C. 技术人才能力评估辅助

**使用场景：** 评估候选人 GitHub 活跃度，验证简历技术能力

```bash
# 查看候选人贡献
gh search repos --author=candidate-username --sort stars

# 查看提交历史
gh search commits --author=candidate-username

# 查看 PR 质量
gh search prs --author=candidate-username --state merged
```

**评估维度：**
| 维度 | 指标 | 权重 |
|------|------|------|
| 代码活跃度 | 过去 12 个月 commits 数 | 30% |
| 项目影响力 | 仓库 stars/forks | 25% |
| 代码质量 | PR merge rate、review 反馈 | 20% |
| 技术广度 | 参与项目数量/语言数 | 15% |
| 社区贡献 | issue 回复、wiki 贡献 | 10% |

### D. CI/CD 技能测试场景生成

**使用场景：** 用 github-actions-generator 生成技术测试，评估候选人 DevOps 能力

```bash
# 生成 CI 测试场景
github-actions-generator ci --lang go

# 生成部署测试场景
github-actions-generator deploy --target kubernetes

# 生成 Docker 测试场景
github-actions-generator docker --registry ghcr
```

**猎头话术：**
> "XX，我们对这个职位有个小技术挑战——你能分享一个你觉得写得最得意的 GitHub Actions 工作流吗？"

### E. 技术人才聚集地地图

**按技术栈分类的人才池：**

| 技术方向 | GitHub 搜索关键词 | 人才聚集项目 |
|----------|------------------|-------------|
| AI/ML | `llm agent rag` | LangChain, AutoGen, LlamaIndex |
| 云原生 | `kubernetes helm istio` | K8s, Helm, Istio |
| 前端 | `react vue nextjs` | Next.js, Vite, TanStack |
| 后端/Go | `go grpc microservices` | Gin, Kratos, Go-zero |
| 数据工程 | `spark airflow data-pipeline` | Airflow, dbt, Delta Lake |
| 安全 | `security pentest vulnerability` | Trivy, Falco, Wazuh |

### F. GitHub 寻访工作流（集成到现有流程）

```
新职位 GitHub 寻访流程：
1. 收到 JD → 提取技术关键词（3-5 个）
2. gh search repos [关键词] → 找到 10-20 个相关仓库
3. 提取各仓库 top contributors → 建立初筛列表
4. gh search commits --author=[名字] → 验证活跃度
5. 交叉比对猎聘/脉脉 → 确认可联系性
6. 输出 Longlist → [猎头顾问姓名] 做 Shortlist
7. Cold Outreach → 用 PMCC 话术触达
```

### Calyflow 6 步 GitHub 自动化 Sourcing

> 开源 Sourcing Agent，单次搜索成本仅 2 美分
> 参考：Calyflow 开源工具，6 步自动化人才寻访

**6 步流程**：
1. **研究目标库** — 分析 JD，确定技术栈和目标人群画像
2. **找库** — `gh search repos [关键词]` 定位相关开源项目
3. **找贡献者** — 提取 maintainer / top contributor 列表
4. **找联系方式** — 从 profile / commit email / 关联社交推断联系方式
5. **评分预选** — 按 commits/stars/PR 质量/技术匹配度评分排序
6. **生成文档** — 自动生成候选人简报，含 GitHub 数据 + 匹配分析

**与传统 Boolean 搜索结合**：
- Boolean 提供关键词和方向 → GitHub 验证真实技术能力 → 交叉比对招聘平台确认可联系性
- **最好的寻访 = 人才地图 + Boolean + AI 自动化三结合**

### G. 布尔搜索 + GitHub 组合拳

**增强版 Boolean 搜索模板：**
```bash
# GitHub + Google 组合搜索
site:github.com "machine learning engineer" "Beijing"
site:github.com "SRE" "Kubernetes" "Shanghai"

# GitHub 用户 profile 搜索
github.com/users?utf8=✓&q=location%3Abeijing+language%3Ago

# 技术栈 + 地点组合
gh search repos "distributed system" --language go --topic distributed-systems
```

### 寻访三十六路 — 优先级策略

> 核心变化：从 "接到 JD 再找人" 转向 "提前 Mapping，有需求时快速启动"

**第一阶段（0-8 小时）：快速出 Longlist**
1. 招聘平台搜索（猎聘/BOSS/脉脉）
2. 内部候选人数据库匹配
3. Boolean 搜索（Google/领英）
4. 社交媒体定向搜索

**第二阶段（2 天后）：深度寻访**
5. 人才 Mapping（目标公司→目标部门→目标人选）
6. F2F 活动（行业会议/展会/沙龙）
7. 社群渗透（微信/知识星球/Reddit）
8. 转介绍激活（已有候选人/客户推荐）
9. 被动候选人池激活
10. Silver Medalist 再触达

**第三阶段（持续）：关系网络**
9. 优秀猎头 2 年后 70%+ 候选来自转介绍
10. 建立行业 KOL 关系
11. 内容获客（行业分析/市场报告）
12. Silver Medalist 运营（面试通过但未入职的候选人）

### Boolean 搜索模板

**基础操作符**
- `AND` / `OR` / `NOT` / `()` / `""` / `-`

**实战模板**
```
# SRE 工程师（阿里/腾讯背景）
("SRE" OR "Site Reliability Engineer") AND ("Kubernetes" OR "K8s") AND ("阿里巴巴" OR "腾讯" OR "字节")

# 快消营销总监
("营销总监" OR "Marketing Director") AND ("快消" OR "FMCG") AND ("品牌" OR "数字营销") -"实习" -"兼职"

# 新能源海外销售
("海外销售" OR "International Sales") AND ("新能源" OR "储能" OR "光伏") AND ("英语" OR "东南亚" OR "欧洲")

# Go 后端工程师（GitHub 开源贡献者）
site:github.com ("Go" OR "Golang") ("微服务" OR "microservice") ("北京" OR "上海")

# AI 工程师（GitHub 活跃贡献者）
site:github.com ("LLM" OR "大语言模型") ("agent" OR "智能体") ("深圳" OR "北京")
```


### 🔬 技术生态寻访引擎

> 核心理念：从"关键词匹配"升级到"技术生态理解"——先理解 JD 背后的技术生态（依赖库、框架、社区），再找贡献者

### 为什么传统 Boolean 不够
- Boolean 搜索只能匹配**写了什么关键词**，不能匹配**实际做了什么**
- 技术候选人真正的能力体现在：GitHub 贡献、技术社区参与、开源项目维护
- AI Sourcing Agent 可以自动读取 JD → 发现相关开源库 → 找贡献者 → 推断联系方式

### 技术生态寻访三步法

**第 1 步：生态映射**
```
JD 关键词 → 依赖的技术栈生态
例："视频编码工程师" → FFmpeg, x264, WebRTC, GStreamer 等
例："AI 工程师" → LangChain, PyTorch, Transformers, vLLM 等
例："SRE" → Kubernetes, Prometheus, Terraform, Istio 等
```

**第 2 步：贡献者发现**
```bash
# GitHub 搜索相关热门仓库
gh search repos "<技术关键词>" --language <语言> --stars ">100"
# 提取 maintainer / top contributor
gh search commits --author=<用户名> --repo <owner/repo>
```

**第 3 步：交叉验证**
- GitHub profile → 推断邮箱/LinkedIn
- 交叉比对猎聘/脉脉/LinkedIn
- 用 Boolean 确认可联系性

### 技术岗位生态映射表

| 岗位 | 核心技术生态 | GitHub 目标项目 |
|------|-------------|----------------|
| AI/LLM 工程师 | PyTorch, Transformers, vLLM, LangChain | llama.cpp, vllm-project, langchain-ai |
| 前端架构师 | React, Next.js, TypeScript, Webpack | next.js, react, typescript |
| SRE/DevOps | K8s, Prometheus, Terraform, Helm | kubernetes, prometheus, terraform |
| 数据工程师 | Spark, Airflow, dbt, Delta Lake | apache/spark, apache/airflow, dbt-labs |
| Go 后端 | Gin, gRPC, etcd, Go-zero | gin-gonic/gin, grpc/grpc-go, etcd-io |
| 视频编码 | FFmpeg, x264, WebRTC, GStreamer | FFmpeg/FFmpeg, WebRTC, gstreamer |

***


### 🎯 被动候选人寻访指南

> LinkedIn 数据：被动候选人占劳动力 75%，主动求职的仅 25%
> 94.2% 的在职求职者对猎头主动推荐有兴趣

### 被动候选人画像

| 特征 | 判断信号 |
|------|---------|
| 在职且稳定 | 当前公司 2 年+，最近有晋升/项目成果 |
| 技术社区活跃 | GitHub 贡献/技术分享/行业会议发言 |
| LinkedIn 有更新 | 但不是"Open to work" |
| 对行业有见解 | 发表过观点/文章/评论 |

### 被动候选人沟通策略

**核心原则**
- 不要用"有个机会薪资翻倍，感兴趣吗"直切式开场
- 用候选人的语言沟通，聊有共鸣的话题
- 向候选人学习比推销一个职位更重要
- 有面试辅导的候选人通过率比无辅导的高 22 个百分点

**分步沟通流程**
1. **第 1 步：研究** — 了解候选人最近的项目/发表/成就
2. **第 2 步：连接** — 基于共同话题建立联系（行业洞察/技术讨论）
3. **第 3 步：价值** — 提供行业信息/市场趋势（不是直接推职位）
4. **第 4 步：试探** — "最近市场上有个方向挺有意思的，想听听你的看法"
5. **第 5 步：深入** — 如果回应积极 → 深入了解职业诉求

### 出海岗位被动候选人沟通要点

- 出海岗位不能直切薪资话题
- 需理解跨文化沟通敏感度，避免文化误判
- 海外面试需要建立雇主品牌吸引力
- 关注候选人对目标市场的了解程度

***


### 🤝 Warm Introduction SOP

### 数据基准 — Warm Intro
- **Warm Intro 回复率 25-40%+**，关键是在第一句提及推荐人
- 内部推荐保留率比其他渠道高 40%（Oracle）
- 优秀猎头 2 年后 70%+ 候选来自转介绍

### Warm Intro 标准流程

**1. 获取推荐人许可**
- 在联系被推荐人之前，先获得推荐人的明确同意
- 话术："XX，你觉得身边有没有同样优秀的同行朋友？我可以先跟你了解一下他的情况吗？"

**2. 24-48 小时内发送**
- 拿到推荐后 24-48 小时内触达，时效性越高回复率越高
- 超过 72 小时，"warm" 变成 "cold"

**3. 第一句必须提及推荐人**
- ✅ "XX 你好，我是猎头 [猎头顾问姓名]，XX（推荐人名字）推荐我联系你的"
- ❌ "XX 你好，我是猎头 [猎头顾问姓名]，在平台上看到你的简历"

**4. 价值先行**
- 附带行业趋势分析、薪资对标、或职业竞争力评估

**5. 低门槛 CTA**
- "不一定要换工作，就当了解一下市场情况"
- "XX 说你在行业里特别有见解，想认识一下"

### Warm Intro 话术模板

**模板 A：推荐人明确同意**
```
XX 你好，我是猎头 [猎头顾问姓名]。
XX（推荐人）推荐我联系你，说你在 [领域] 特别专业。
我这边有一个 [公司] 的 [职位] 机会，
考虑到你的 [某项技能/经验]，觉得非常匹配。
方便的话这周找个时间简单聊 10 分钟？
不一定要换工作，就当了解一下市场情况。
```

**模板 B：推荐人提供信息但未明确同意**
```
XX 你好，我是猎头 [猎头顾问姓名]。
我在做 [行业] 的人才地图时，
通过 [共同渠道/推荐人名字] 了解到你在 [公司] 负责 [方向]。
最近做了一份 [行业] 人才市场趋势分析，
觉得你可能感兴趣，方便分享一下吗？
```

**模板 C：Silver Medalist 转介绍**
```
XX 你好，上次 [候选人姓名] 入职 [公司] 后，
向我推荐了你，说你在 [领域] 特别厉害。
正好我这边有个 [公司] 的机会，
和你们的背景都很匹配，有兴趣了解一下吗？
```

### Warm Intro 追踪表
| 日期 | 被推荐人 | 推荐人 | 触达渠道 | 回复 | 结果 | 下次跟进 |
|------|---------|--------|---------|------|------|---------|

***


### 🔁 ATS 沉睡候选人唤醒流程

> 50% placement 来自已有数据库 —— 但很多候选人"睡着了"就再没被唤醒

### 沉睡候选人定义
- **沉睡标准**：最后触达日期 > 90 天
- **高价值沉睡**：曾经进入过 Screening/Interview/Offer 阶段
- **Silver Medalist**：面试优秀但未录用 = 最高优先唤醒对象

### 唤醒工作流

| 阶段 | 动作 | 负责方 |
|------|------|--------|
| **扫描** | 定期扫描人才库，标记沉睡 >90 天的候选人 | AI 自动 |
| **匹配** | 与新开放职位做匹配度评分 | AI 自动 |
| **排序** | 按匹配度 + 历史价值（曾进入过哪阶段）排序 | AI + [猎头顾问姓名] |
| **唤醒话术** | 生成个性化消息（基于上次沟通记录） | AI 生成，[猎头顾问姓名] 审核 |
| **触达** | 发送个性化消息 | [猎头顾问姓名] 发送 |
| **反馈** | 记录回复/拒绝/无响应 | AI 更新档案 |

### 唤醒话术模板

**Silver Medalist 唤醒**
```
XX，好久不见！上次 [公司/职位] 虽然没成，
但我一直记得你的 [核心优势]。
最近有个 [新公司] 的 [职位]，
和之前的不太一样，[新亮点]，
我觉得和你的匹配度更高。
有兴趣聊聊吗？就当了解市场。
```

**沉睡候选人唤醒（匹配新职位）**
```
XX，好久没联系了，上次聊的时候你还在 [公司]，
现在怎么样？
我这边最近有个 [行业/职位] 的机会，
想到你之前的 [某项经验]，觉得挺匹配的。
方便通个 10 分钟电话聊聊吗？
```

**沉睡候选人唤醒（纯关怀）**
```
XX，好久没聊了，最近怎么样？
上次聊之后，[行业] 出了些新动向，
我做了份最新的市场分析，
想分享给你看看？就当多一个信息。
```

### 自动提醒规则
- **每 30 天**：扫描沉睡候选人，匹配新职位
- **新职位开放时**：自动扫描人才库，推送匹配度 Top 5
- **Silver Medalist**：90 天强制唤醒提醒
- **触发事件发生时**：目标公司融资/高管变动时，唤醒相关沉睡候选人

***


### 🤖 AI Sourcing Agent 十大用例 → Pipeline 映射

> 基于 Curately 2026 AI Sourcing Agent 十大用例，映射到我们的 Pipeline 状态机

| # | AI Sourcing 用例 | 映射 Pipeline 阶段 | 人工决策点 |
|---|-----------------|-------------------|-----------|
| 1 | ATS 沉睡候选人再发现 | Identified → Contacted | 选择哪些沉睡人选值得唤醒 |
| 2 | 相关性排名自动建 Shortlist | Identified → Screening | 确认排名权重是否合理 |
| 3 | 大规模个性化触达 | Contacted | 审核 AI 生成的个性化消息质量 |
| 4 | 端到端招聘自动化 | 全流程 | 设定流程边界（什么不能自动化） |
| 5 | 自动跟进和互动维持 | Contacted → Responded | 跟进频率和时机的判断 |
| 6 | 面试前预筛选 | Screening | 确认筛选标准与客户对齐 |
| 7 | 基于技能的匹配 | Screening | 技能权重调整，非传统背景评估 |
| 8 | 合规/偏见减少/可审计 | 全流程 | 确保合规底线不被突破 |
| 9 | 招聘人员生产力提升 | 全流程 | 释放的时间投入到关系建立 |
| 10 | 大批量招聘支持 | Identified → Contacted | 批量中的质量控制 |

### 关键原则
- **AI 做 1-7 和 9-10，[猎头顾问姓名] 做决策点**
- 端到端自动化（#4）不是"全自动"，而是"AI 执行 + 人工监督"
- 合规（#8）是底线：AI 不能决定是否歧视，只能辅助减少偏见

***


### Resume Triage 批量筛选工作流

### 使用场景 — 候选人画像
[猎头顾问姓名] 收到一批简历（文件夹/列表），需要快速初筛。

### 流程
1. 收集简历 → 放入临时文件夹或提供列表
2. 提供 JD → [猎头顾问姓名] 粘贴或提供路径
3. 批量评分 → 我对每份简历做 9 维度评分
4. 输出 CSV → 排序 + 分级（A/B/C）
5. [猎头顾问姓名] 复核 → 从 Longlist 中选 Shortlist

### 输出格式
```csv
姓名,学历,工作年限,稳定性,当前公司,行业,综合评分,等级,备注
张三,硕士,8,低,阿里,互联网,8.5,A,核心匹配
李四,本科,6,中,腾讯,互联网,7.2,B,技能可迁移
王五,本科,3,高,创业公司,互联网,5.1,C,经验不足
```

### 分级标准
- **A 级（8+）**：强烈推荐，立即安排沟通
- **B 级（6-7.9）**：推荐，可备选
- **C 级（<6）**：不推荐，除非特殊情况

***
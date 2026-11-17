# OppHub 产品总架构设计

**Date**: 2026-07-23
**Status**: draft
**Author**: opencode
**Scope**: opphub-web (Next.js) + opphub-skill (OpenClaw) + opphub-ws (推送服务)

---

## 0. 产品定位与决策

OppHub 是一个 AI 驱动的 B2B 双边撮合平台。用户既是潜在供应商（提供能力/服务），也是潜在需求方（寻找合作方）。两侧共享同一个知识库，靠 AI 在知识图谱层做匹配。

### 0.1 关键决策

| 决策 | 选 | 不选 | 理由 |
|---|---|---|---|
| 用户身份 | 一账号双身份，靠 entryType 区分 | 拆分供/需两种账号 | 用户画像是真实人的多面身份，强行拆会让他分裂体验 |
| 录入入口 | IM (skill) 为主、Web 表单为辅 | 仅 Web 表单 | IM 是用户已经习惯的自然语言入口，AI 蒸馏更准 |
| 撮合推送 | 自动+手动两路 | 仅自动 | 0.65~0.85 之间的边角匹配靠平台运营眼力更准 |
| 路由架构 | 6 个一级入口 + 角色在 Tab 表达 | 拆开供需两套路由 | 减少路径分裂，新人 5 分钟搞清自己在做什么 |
| 通用 IM | 嵌入撮合/订单详情页 | 顶级 `/messages` | 通用 IM 没业务上下文，单独成页浪费用户注意力 |
| 推送服务 | opphub-ws 独立项目 | 内嵌 opphub-web | 解耦：推送不需要部署 Next.js 也能跑 |

### 0.2 一句话产品链路

`录 → 撮 → 谈 → 成`, AI 在每一步都有产物, 用户每一步都有反馈。

---

## 1. 顶层导航 (替代当前 7 个一级)

当前 opphub-web TopBar 7 个入口 (`dashboard / match / demands / orders / messages / me/capabilities / account/security`) 全部重建。

### 1.1 新一级导航 (6 个)

| # | 路径 | 中文 | 一句话 |
|---|---|---|---|
| 1 | `/dashboard` | 工作台 | 一屏看完: 未办 / 待回 / 进行中 / 新撮合 |
| 2 | `/knowledge` | 知识库 | 我能提供 / 我在找 / 上下游 (内部 Tab 切) |
| 3 | `/discover` | 发现 | 浏览公开需求和服务 (不再叫 marketplace, 也不叫 demands) |
| 4 | `/matches` | 撮合 | AI 撮合对、咨询、出价集中处理 |
| 5 | `/orders` | 交易 | 订单状态机: 进行中 / 已完成 / 争议中 |
| 6 | `/wallet` | 钱包 | 收入 / 支出 / 提现 |

次级: `/settings`、`/help`、admin 入口 (仅 isAdmin 可见)

### 1.2 移除 / 改名

- ❌ `/me/capabilities` 移到 `/knowledge` (Tab: 我能提供)
- ❌ `/opc/profile` 移到 `/knowledge/[entryId]` (单条目详情)
- ❌ `/demands` 移到 `/discover?role=buyer`  (我是需求方)
- ❌ `/marketplace` 移到 `/discover?role=seller`  (我是供应方)
- ❌ `/match` 移到 `/matches` (改名复数, 强调是流水)
- ⚠️ `/messages` 留作"通知中心"别名, 但主聊天嵌入订单详情

### 1.3 角色表达 (在 `/knowledge` 内 Tab 自然表达)

```
/knowledge (默认 tab: ability)
  ├ Tab 我能提供   entryType=ability
  ├ Tab 我在找     entryType=downstream
  ├ Tab 我的客户   entryType=peer
  └ Tab 我的依赖   entryType=upstream
```

任何 Tab 内的"+ 新增条目"按钮自动选择对应的 entryType。

---

## 2. 主链路状态机

### 2.1 一笔生意从「AI 看到匹配」到「钱到账」= 8 步

```
[知识库就绪]
    ↓
[AI 撮合发现匹配]   matchings.status = pending
    ↓
[任一方发起咨询]    matchings.status = inquiry
    ↓
[我方出价]          matchings.status = bid_pending
    ↓
[对方接受]          matchings.status = bid_accepted
    ↓
[订单 pending → paid]  orders.status: pending → paid
    ↓
[供应方交付]        orders.status: in_progress → delivered
    ↓
[需求方验收]        orders.status: accepted → completed
    ↓
[平台抽佣 + 钱包到账]  payments.release success
```

### 2.2 状态机操作矩阵

| 当前状态 | 供应方 | 需求方 | 系统 |
|---|---|---|---|
| match.pending | 发起咨询 / 忽略 | 发起咨询 / 忽略 | 失效 (30d) |
| inquiry.open | 发消息 / 出价 | 发消息 / 拒绝 / 出价 | 自动关闭 (30d) |
| bid.pending | 等回应 / 改价 | 接受 / 还价 / 拒绝 | 自动撤 (7d) |
| order.pending | 等付款 | 付款 / 取消 | 取消 (超时 24h) |
| order.paid | 开始干活 / 交付 | 等交付 | 退款通知 (7d) |
| order.delivered | 等验收 | 验收 / 争议 / 延期 | 自动验收 (7d) |
| order.disputed | 提交证据 | 提交证据 | 平台介入 |
| order.accepted | — | — | 自动结算 + 释放 |

### 2.3 关键表 (与现状对齐)

```
matchings                 # 撮合对 (AI 产出或运营手动)
  status: pending | inquiry | bid_pending | bid_countered | bid_accepted | declined | expired | archived

inquiries                 # 咨询 (任一方对撮合发起)
  matchingId, fromOpc, toOpc, status: open | closed

bids                      # 出价 (供需任一方)
  inquiryId, fromOpc, amount, termDays, msg, status: pending | accepted | rejected | countered

orders                    # 订单
  party_a (供应方 opcId) / party_b (需求方 opcId)
  inquiryId, matchingId
  amount, platform_fee (5%), deadline
  status: pending | paid | in_progress | delivered | accepted | disputed | completed | cancelled | refunded

payments                  # 支付流水
  orderId, type: escrow | release | refund | commission
  status: init | success | failed
```

### 2.4 页面状态机

| 页面 | 显示什么 | 用户可做 |
|---|---|---|
| `/matches` | AI 列出"谁和谁匹配上", 每条一卡 | 发起咨询 / 出价 / 标记忽略 |
| `/matches/[id]` | 单撮合详情: 双方公开档案 + 匹配原因 | 聊天窗口 (聊完可一键出价) |
| `/orders` | 我的订单列表 (按状态分组) | Tab: 进行中 / 已完成 / 争议中 |
| `/orders/[id]` | 订单详情 + 合同 + 交付物 + IM + 状态机按钮 | 上家点交付 / 下家点验收 / 任一方发起争议 |
| `/orders/[id]/dispute` | 争议详情 + 证据上传 | 提交证据 / 撤销 / 平台介入 |

---

## 3. 知识库语义 + 录入规范

### 3.1 entryType 四种

| entryType | 含义 | 谁写 |
|---|---|---|
| `ability` | 我能提供: 服务能力 | 供应方 (sender) |
| `downstream` | 我想找: 需求/商机 | 需求方 (receiver) |
| `upstream` | 我的依赖: 上游供应商 | 供应方自报 |
| `peer` | 同行/参考关系 | 双方 |

### 3.2 维度模板 (entryDimension 枚举)

| entryType | 允许的 entryDimension 候选 |
|---|---|
| ability | 短视频脚本 / 达人投放 / 数据分析 / 设计 / 拍摄剪辑 / 程序开发 / 公关传播 / 品牌策划 / KOL孵化 / 私域运营 / 内容运营 / 商业BD / 法律咨询 / 财税咨询 / 人力招聘 / 翻译 / 其他服务 |
| downstream | 找服务商 / 找供应商 / 找合伙人 / 找投资方 / 找分销渠道 / 找联合品牌 / 找流量入口 / 找上游素材 / 其他合作 |
| upstream | 数据来源 / 素材供应 / 人力外包 / 流量平台 / 渠道分销 / 技术依赖 / 云服务 / 其他依赖 |
| peer | 同业联盟 / 同行参考 / 关联企业 / 上下游关系 |

**原则**: 维度先穷举 (10-15 个每类), 用户改模板即可。不允许随便起名, API 层强制 enum 校验。

### 3.3 rawText 强约束结构

每条 entry 的 rawText 必须是:

```
## 1. 核心要素
- 名称: <字符串>
- 类型: <ability|downstream|upstream|peer>
- 维度: <从上面 enum 选>

## 2. 详细描述
<200-1000 字自由描述, AI 据此抽取结构化字段>

## 3. 证据 / 链接
<可选, 官网 / 作品集 / 参考文章 URL>
```

### 3.4 录入的三种引导形式

```
┌─────────────────────────────────────────────┐
│  📥 新增知识条目                              │
│                                              │
│  📇 我能提供什么   (走 ability 模板)            │
│  🔍 我想找什么    (走 downstream 模板)         │
│  🔗 我的上下游    (走 upstream/peer 模板)       │
└─────────────────────────────────────────────┘
```

### 3.5 录入的正反馈循环

```
录入完成 → 后台 worker:
  1. AI 抽取 结构化字段 (法人/规模/价格/城市/可服务时间)
  2. 向量化切 chunk, 算 768 维 embedding
  3. 立即跑撮合试算, 跟全库公开条目算相似度
  4. 实时告知"已匹配 N 个潜在合作方"

用户视角:
  - /knowledge 顶部紫色 banner: "🎉 你的「短视频脚本」已在 X 个匹配中曝光"
  - /dashboard 如果有超过 5 个匹配: 黄色 banner: "🔥 有 N 个匹配在等你"
```

### 3.6 数据建模 (与现状对齐)

```
opc_account              用户账号
  +--opc_knowledge_entry 单条知识
  |   entryType ∈ enum(ability|downstream|upstream|peer)
  |   entryDimension ∈ <上面 3.2 表里对应类型>
  |   rawText (TEXT)
  |   idempotencyKey = sha256(opcId + entryType + entryDimension)
  |   contentHash = sha256(rawText)
  |   status (pending|processing|done|failed)
  |   visibility (PRIVATE|PUBLIC)   -- 默认 PRIVATE
  |   previousEntryId (软链, 覆盖历史)
  |   supersededAt
  |   deletedAt (软删)
  |   +--opc_knowledge_chunk 切向量
  +--opc_matchings 撮合对
  +--opc_orders 订单
  +--opc_payments 支付流水
  +--opc_messages 消息 (撮合/订单的 IM 上下文)
```

---

## 4. 撮合逻辑

### 4.1 触发路径

```
知识库新条目写入
    ↓
  ┌─────┴─────┐
  ↓           ↓
路径 A         路径 B
自动撮合     后台手动撮合
cos≥0.85     cos 0.65~0.85
  │           │
  └─────┬─────┘
        ↓
   matching 写入
        ↓
   给双方默认通道 push
        ↓
   ┌─ 已配对 → /matches/[id]
   ├─ 推送失败 → 自动重试 3 次后入死信
   └─ 超时 → expired
```

### 4.2 严格方向匹配

- `ability ↔ downstream` ✅
- `downstream ↔ ability` ✅
- `upstream ↔ upstream` (同业合作机会) ✅
- 其他 ❌

### 4.3 评分公式

```
match_score = 0.40·semantic
           + 0.20·price_match (双方都填价格且区间重叠)
           + 0.15·geo_match   (同城 +1)
           + 0.15·trust_score (双方信用分差 10 内奖励)
           + 0.10·recency     (最近 7d 录入加权)
```

### 4.4 撮合状态 (状态机视角)

| 状态 | 含义 | UI |
|---|---|---|
| `pending` | AI 新发现, 双方都没人看 | 红色未读角标 |
| `inquiry` | 任一方已发起咨询 | "⏰ 等待对方回应" |
| `bid_pending` | 已出价, 等回应 | "💰 你的 ¥5000 待对方接受" |
| `bid_accepted` | 出价被接受 = 形成订单 | "🎉 进入订单" 按钮 |
| `declined` | 拒绝/忽略 | 灰底, 30d 后归档 |
| `expired` | 30 天无响应 | 仅历史可见 |

### 4.5 后台手动撮合 — 匹配池排序

```
match_pool_score = 0.50·semantic
                 + 0.20·双方信用分差 (对称奖励: 双方都 80+ 给 +1)
                 + 0.15·金额匹配 (双方都填价位且区间重叠)
                 + 0.10·城市匹配 (同城 +1)
                 + 0.05·新鲜度 (5 天内录入加权)
```

后台 UI:
```
📊 待撮合池 (排序分降序)

#1 王老板 (供给) ↔ 上海睿驰 (需求)  0.89
   达人脚本 ↔ 找达人对接  🔥 ¥3-5k 同城
   [✓ 撮合]  [✕ 跳过]  [👀 详情]

#2 张三 (供给)  ↔ 杭州A公司 (需求)   0.83
   ...
```

### 4.6 撮合频控

- 同一对匹配一天最多提示一次 (除非状态变化)
- OPC 一周收到新撮合上限 30 (防疲劳)
- 已 declined 的 14 天不再推送 (除非任一方主动改资料)

### 4.7 撮合的隐私保护

- **默认双方匿名**: 撮合卡片只显示 `维度 + 城市 + 评分 + 信任分`, 不显示公司名
- 任一方"发起咨询"后, 解锁 `displayName`
- 进订单后才显示全名 + 联系方式

---

## 5. 推送通道 (opphub-ws)

### 5.1 推送 API 模板

```
[撮合通知]
🆕 你有一对潜在匹配

对方: [维度] · [城市] · 评分 X.XX
匹配度: NN%

💬 进撮合查看 → /matches/[id]
```

### 5.2 推送通道

| 通道 | 状态 | 备注 |
|---|---|---|
| FCM (Firebase) | active | 当前唯一, 也是默认 |
| Email (SMTP) | planned | 兜底 |
| 微信模板消息 | planned | |
| 短信网关 | planned | 重要通知兜底 |

### 5.3 推送队列 + 重试

```
matching 新建 → 推送任务入 opphub-ws 队列
  ↓
  1st attempt: 默认通道 (FCM)
  ↓ failure
  2nd attempt: 5min 后, 同一通道 (指数退避)
  ↓ failure
  3rd attempt: 1h 后, 同通道
  ↓ failure
  → 入死信表, 后台有 retry 入口

每条推送都存表: PushLog { matchingId, opcId, channel, status, attempt, error? }
```

### 5.4 通道优先级

```
fcm > email > wechat > sms (fallback 链)
当前仅 fcm 实现了, 其余是占位
```

---

## 6. 页面状态规范

### 6.1 五类页面状态 (每页必处理)

```
1. 加载中 (skeleton, 不裸露空白)
2. 空数据 (CTA 引导, 不止"暂无数据")
3. 出错 (明确诊断 + retry)
4. 未登录 (统一跳登录)
5. 已登录但未实名 (灰度 CTA "立即实名解锁撮合")
```

### 6.2 通用组件

- `PageSkeleton variant="list | card | detail"`
- `EmptyState title body primaryCta secondaryCta`
- `ErrorState code message diagnostic retry`

### 6.3 跳转规范

| 入口动作 | 跳哪儿 |
|---|---|
| 录入第 1 条 knowledge | 回 `/knowledge` + 顶部紫色 banner "🎉 已录入, 5 秒内出现匹配" |
| 录入后看到匹配 | `/matches/[id]` |
| 出价被接受 | 弹窗 "🎉 进入订单" → `/orders/[id]` |
| 完成验收 | `/orders?tab=completed` |
| 实名首次通过 | `/dashboard` + banner "现在可以撮合了" |

### 6.4 错误兜底

| 场景 | 兜底 |
|---|---|
| 接口 5xx | retry 3 次 (指数退避) 后报错, 错误存 localStorage, 下次访问恢复 |
| 网络断 | 全局 "网络已断开" banner, 恢复自动消失 |
| 鉴权 401 | 自动跳登录, 登录后回原页 |
| 撮合接口限流 | 显式提示 "太快了, 等 30 秒再来" |
| 文件上传失败 | 单文件单独标红, 其他可继续 |

---

## 7. Onboarding 流程

```
新 OPC 首次登录
  ↓
跳 `/onboarding/intro` 4 屏介绍
  ├ 1 屏: 录 (录入你的能力/需求)
  ├ 2 屏: 撮 (AI 在知识库里匹配)
  ├ 3 屏: 谈 (撮合双方聊天)
  └ 4 屏: 成 (出价 → 订单 → 结算)
  CTA: "开始录入第一条"
  ↓
跳 `/knowledge` 默认 tab=ability
  用户录入
  ↓
  顶部 banner: "等 5 秒, 等匹配出来"
  ↓
  5 秒内首次有匹配 → 横幅 + 声音: "🎉 第一个匹配到了"
  CTA "去看看" → `/matches`
```

---

## 8. 技术栈与依赖

### 8.1 项目地图

```
opphub-web           Next.js
  ├─ 录入: /knowledge (Web 表单, 备用)
  ├─ Knowledge 存储: PostgreSQL
  ├─ Embedding: 服务端 worker (BGE 768 维)
  ├─ 撮合: 服务端 + opc_matchings 表
  ├─ 状态机: 订单/撮合/支付状态全在 opphub-web
  ├─ 前端: Next.js
  └─ 推送: 转 opphub-ws

opphub-ws            独立项目
  ├─ 推送任务队列
  ├─ 重试 + 死信
  ├─ 当前仅实装 FCM
  └─ 占位: email / 微信模板 / 短信

opphub-skill         OpenClaw runtime 上的 skill
  ├─ IM 录入主入口
  ├─ knowledge-discover / knowledge-card / knowledge-submit
  ├─ knowledge-relate / knowledge-search / knowledge-status
  └─ 通过 opphub plugin 拿 access_token, 再调 opphub-web API

opphub plugin        OpenClaw 扩展
  ├─ OAuth device flow
  ├─ token 持久化
  └─ RPC 客户端供 skill 调用
```

### 8.2 关键依赖

- **录入主路** = `opphub skill` (OpenClaw runtime, IM)
- **录入备路** = `opphub-web /knowledge` 表单
- **服务端入口** = `/api/user/knowledge/ingest` (两个入口都走这个)
- **推送发送** = `opphub-ws` (独立项目, `/api/channel/...` 是对接接口)
- **embedding** = 服务端 `opc_knowledge_chunk.embedding` 768 维 (BGE base)
- **状态机** = opphub-web 服务端
- **前端** = Next.js

### 8.3 系统不允许做的事

- `opphub-web` 不直连 FCM / 微信 / 短信, 必须走 opphub-ws
- `opphub-web` 不直接生成 embedding, 由 server worker 跑 (统一的 BGE 模型在 server side)
- `opphub skill` 不直连数据库, 一律通过 opphub-web API (因为 skill 跑在用户机器, 直连 DB 不安全)
- `opphub skill` 是 IM 录入的源头, skill 的"提示"是引导用户的关键
- `opphub-ws` 跟 `opphub-web` 是两个独立项目, API 对接由 `/api/channel/...` 那批路由承担

---

## 9. 实施方案 (Roadmap)

按价值密度排序, 后续 plan 分批实施:

### 阶段 1: 导航 + 角色表达
- 改 TopBar 6 个入口
- 新 `/knowledge/[entryId]` 替代 `/opc/profile` 重名
- `/discover` 新建, 取代 `/demands` + `/marketplace`
- `/matches` 改名 + 改造 (替代 `/match`)
- 旧路径 redirect

### 阶段 2: 知识库语义升级
- entryDimension 枚举 + 服务端验证
- rawText 强约束结构
- 录入"三选一"模板选择
- "我能提供 / 我在找" Tab 自动选 entryType

### 阶段 3: 撮合流转
- matchings / inquiries / bids 三张表 + 状态机
- `/matches` 新版 + 撮合详情页 + 聊条嵌入
- 自动撮合触发器 (写条目 → 跑 cosine)
- 后台 `/admin/match-pool` 待撮合池 + 手动撮合接口

### 阶段 4: 订单状态机
- orders / payments 表
- `/orders` 状态分组 + `/orders/[id]` 详情
- 状态机操作矩阵落 API + 按钮
- 聊天嵌入订单详情

### 阶段 5: 推送 + Onboarding
- opphub-ws 对接 (FCM 通道)
- PushLog 表
- 推送队列重试 + 死信
- Onboarding 4 屏 + 录入正反馈 banner

### 阶段 6: 错误兜底 + 5 状态规范
- 全局 Skeleton / EmptyState / ErrorState 组件
- 跳转规范落页
- 错误 retry + localStorage 兜底

### 阶段 7: 钱包 + 设置
- `/wallet` 新建
- 提现/充值流程
- 银行/支付宝接入

---

## 10. 不在范围内 (YAGNI)

明确不做:

- ❌ 通用 IM (我们没有"私信"概念, 聊天只在撮合/订单里发生)
- ❌ 朋友圈 / 动态 (产品是工具, 不是社区)
- ❌ 评论 / 评分 (信任分走其他机制)
- ❌ 复杂的 CRM (供需双方都靠 auto matching 决策)
- ❌ 富文本编辑器 (rawText 是 markdown-like, 不做实时协作)
- ❌ 多账号体系 (一个 OPC = 一个 opcId)
- ❌ 公开排行榜 / 推荐位

## 11. 开放问题 (后续明确)

| 问题 | 当前假设 | 待澄清 |
|---|---|---|
| 撮合通知是双向还是单向 | 双向 (双方都收到) | 触发时机是否要对齐? |
| 出价是否必须经过咨询 | 当前假设: 必须先开咨询 | 是否允许冷出价? |
| 订单超时具体天数 | 待 schema 定 | 7d 拍 |
| 平台抽佣比例 | 5% | 财务层面待定 |
| 推送默认通道优先级 | FCM > email > 微信 > 短信 | 当 FCM 失败时, 是否自动 fallback 还是仅重试? |

---

## 12. Spec 自审

- ✅ 决策都有理由
- ✅ 各 section 无矛盾
- ✅ 数据模型对齐现状 schema
- ✅ 链接及状态编号明确
- ✅ 范围清晰 (YAGNI list)
- ⚠️ 单独一个 spec 比较长, 后续按阶段拆 7 个 plan 实施
- ⚠️ 一些问题留 `section 11: 开放问题` 待后续明确


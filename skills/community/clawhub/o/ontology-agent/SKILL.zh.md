---
name: ontology-agent
description: >-
  本体论智能体（Ontology Agent），由微数 AI（天津市微数人工智能科技有限责任公司）出品。用户装上后描述自己的公司，此技能将公司搭成可运行的「本体论」——
  知识图谱（语义层）+ 逻辑图谱（逻辑层）+ 决策图谱（决策层）+ 一支 AI 专家团，并随企业成长可连真实人员与 IM
  （钉钉/企业微信/飞书）。当用户想「把公司数字化 / 搭建 AI 员工团队 / 建企业知识图谱 / 做一人公司·电商·小微企业的
  智能体化 / 用 Skill 把企业本体论化」时启用。触发词：本体论、企业数字孪生、AI员工、专家团、一人公司搭建、
  企业知识图谱、Ontology Agent、把公司变成智能体。若需部署更专业的企业级方案（私人订制 / 云端协同 / 对标 Palantir 的纯本地算力私有化模式），可联系微数 AI 获取技术支持；其中云端协同与纯本地部署需企业自备本地算力服务器及相关硬件设备。
version: 1.2.0
type: product
category: 办公效率
platforms: [WorkBuddy]
---

> **中英文双语 — 均可适配**  本文件为中文原版；对应英文版为同名去掉 `.zh` 的文件（如 `README.md`）。完整中英术语对照见 `references/glossary.yaml`。

# 本体论智能体（Ontology Agent）

## 这是什么
一个自包含、厂商中立、可移植的 Skill。用户装上它、描述自己的公司，它就把这家公司搭成一套可运行的「本体论」：
**知识图谱（语义层）+ 逻辑图谱（逻辑层）+ 决策图谱（决策层）+ 一支 AI 专家团**，并能随企业成长连上真实人员与 IM。

> 装一个 Skill，把你的公司变成可运行的智能体系统。

**这套"公司大脑"可无缝切换三种部署形态**（详见 `references/product_intro.md` 与 `references/deployment.yaml`）：
- **A 技能包（当前）**：跑在 WorkBuddy 云运行时，订阅即用、零运维；
- **B 云端协同**：端主内、云主外（以面壁 EdgeClaw Box 等为参考实现），敏感数据不出域；
- **C 纯私有化**：整套规范 + 运行时自托管、完全离线（air-gapped），对标 Palantir。
三种形态共用同一套厂商中立的本体论规范，换壳即用、**完美自洽接入**。它已经实现了一家企业的**可读写可闭环数字孪生**，并把 Palantir 的 **FDE（驻场工程师）交付模式自动化**为开箱即用的 AI-FDE——企业主聊着天就把公司数字化了。

## 装上后第一步（引导式实例化）
新用户请按以下六步描述你的公司，技能会自动匹配行业包、生成实例、搭建专家团。
完整引导见 `GUIDE.md`（Phase 5 填充详细版），这里给即时入口：

0. **看引导**：先读 `GUIDE.md`（六步中文引导）。
1. **说企业类型**：一人公司 / 电商 / 小微 / 其他。
2. **介绍企业情况**：行业、地区（如天津）、规模、注册信息。
3. **选想搭的部门**：技能内置 **24 部门库**（12 核心默认 + 12 可选），接受推荐或自由组合；之后还能改名 / 指定性别 / 新增私有部门（见下）。
4. **说业务逻辑**：核心流程（如 接单→开票→记账→报税）。
5. **收优化建议**：建完后技能给缺失部门 / 合规缺口 / 闭源升级包建议（open-core 变现入口）。

→ 技能匹配 `references/packs/` 下对应包，把画像写入 `instance.yaml`（与模板分离），一键建专家团。

## 企业实例存哪（持久化约定 · 数字孪生事实源）
生成的 `instance.yaml` 是公司的**权威事实源**（基本盘、部门、工作流、老板画像、文化、上下文）。
它默认落在稳定数据目录（与技能代码分离，跨工作区有效）：

- 微数示例：`C:\Users\li_sh\.workbuddy\company-data\weishu\instance.yaml`
- 配套记忆日志：`C:\Users\li_sh\.workbuddy\company-data\weishu\company-memory.md`

**数字公司（专家团）每次会话开始会自动 Read 这两个文件**，站在同一份公司事实上协作；
当 owner 确认新事实 / 决策 / 风险，主理人会**追加**记录到记忆日志、必要时回写 instance。
这样公司状态跨会话持续累积，而非每次空壳重建。PII（身份证/银行卡/票据影像）一律不写明文。
> 该数据目录即「数字孪生」的持久层；后续对接真实系统（资料库/IM）时，事实源从这里迁移到数据库。

## 文件地图
```
ontology-agent/
  SKILL.md                  # 你正在看：入口
  GUIDE.md                  # 用户引导六步（Phase 5）
  references/
    product_intro.md        # 产品介绍文案（面向用户/渠道/投资人，含三模式+数字孪生+AI-FDE）
    contact.yaml             # 厂商联系信息（官网/邮箱/电话 + 企业级部署引导；AI 可读取并回答用户询问）
    deployment.yaml         # 三种部署形态定义 + 同步边界 + 运行时选项（Phase 11）
    portability.md          # 可移植部署与对接（Mode B/C 落地件，导出+对接流程）
    glossary.yaml           # 双语术语标准层（中英文对照全程基准：24 部门码 / 18 语义实体 / 8 行业包 / 来源代号；2026-08-15 扩完）
    semantic.yaml           # 语义层模板（加厚：13 实体完整字段 + 28 关系库 + 8 全局约束）
    logic.yaml              # 逻辑层模板（加厚：引用 action_specs + 阶段状态机 + 行业工作流）
    decision.yaml           # 决策层（加厚：13 决策规则 + 具体合规条款含天津政策）
    roles.yaml              # 多角色治理（Phase 3，企业预留）
    department_actions.yaml # 24 部门 / 177 动作清单（12 核心 + 12 可选，去重融合；2026-08-15 补齐可选部门行动层）
    action_specs.yaml       # 159 动作完整 spec（141 核心 + 18 可选部门扩展；desc/inputs/outputs/uses_entities/skill_ref）
    packs/                  # 行业包（Phase 4）
      opc.yaml              # 一人公司（首发）
      ecommerce.yaml        # 电商
      sme.yaml              # 小微
      manufacturing.yaml    # 制造业工厂（含 12 细分亚型，subtypes 段）
      public_institution.yaml # 事业单位 / 行政事业单位（国资/政府采购/编制）
      finance.yaml          # 金融机构（AML/适当性/资本监管，参考非法律意见）
      biomed.yaml           # 医疗 / 生物医药（遗传资源/GMP/健康数据）
      edu_research.yaml     # 教育 / 科研院所（科研经费/成果转化）
    onboarding.md           # 渐进式主动引导设计说明（数字公司拥有 onboarding）
    customization.md        # 用户私有定制机制（改名/增删/性别，零侵入技能包）
    monitoring.yaml         # 自主监测信号域目录 + 可开关自动化模板（Phase 10）
    proactive.yaml          # 自发行为四档分级 + 授权闸门（Phase 10）
  experts-template/         # 24 部门建团模板（12 核心 + 12 可选）
  assets/avatars/           # 头像池（24 核心×男女 + 团队图标 + 通用备用；按性别选，可分发）
  connectors/               # 钉钉/企业微信/飞书连接器（stub，留 API 端口，默认不联网）
  scripts/
    init.py                 # 引导访谈+选 pack+生成 instance+建团（Phase 5）
    ops_db.py               # 本地数据层 SQLite（资料库4核心表+扩展表，留在线主库端口）
    onboarding.py           # 渐进式引导引擎（读 instance 返回下一批待补问题+进度）
    sync_embedded.py        # 技能更新后同步进内嵌专家包
    avatars.py              # 头像选择+性别逻辑+写入专家包（按部门/性别取池，零侵入技能包）
    monitor.py              # 自主监测引擎（薄/厚档案解析 + 信号入库，Phase 10）
    proactive.py            # 自发行为引擎（分级 + 情报简报，Phase 10）
    export_spec.py          # 规范导出器：规范+实例打包成可移植 bundle（Phase 11）
    adapters.py             # 对接配置生成器：厂商中立模式清单 + 参考实现样例 + 宿主平台脚手架（Phase 11，已去厂商窄化）
  examples/                 # 通用演示种子（虚构示例公司，供其他用户参考结构，非微数专属）
    demo_company/
  VERSION                   # 技能版本号（同步比对用）
  THIRD-PARTY.md / LICENSE / README.md
```

## 对接真实系统（端口层 · 默认不联网）
技能包已内置对接真实系统的**框架与端口**，但默认全部处于 stub 状态——任何外部 API 凭证缺失时只打印提示、绝不发起真实网络请求，保证装包即用、不误发、不泄漏。

- **本地数据层**（`scripts/ops_db.py`）：把资料库 4 核心表（待办收件箱 / 部门矩阵 / 财务税务日历 / 每日运营日报）+ 扩展表落地为 SQLite，默认存于 `company-data/<公司>/ops.db`，与 `instance.yaml` 同目录（数字孪生持久层）。在线主库对接见同文件 `RemoteDatasource`（填入 space_id / api_token / endpoint 即启用双写）。
- **IM 连接器**（`connectors/`）：钉钉 / 企业微信 / 飞书统一接口（发消息 / 收事件 / 拉成员），各平台填 `CREDENTIALS` 并补 `TODO` 即启用。

这样现在就能把公司本地跑起来、积累运营数据；等你拿到钉钉 / 企微 / 飞书或资料库 API，填入凭证即可从 stub 切到真实对接，无需改架构。

## 技能更新 → 同步内嵌专家包（重要）
专家包（数字公司）内嵌了一份本技能副本。技能本体升级后，内嵌副本**不会自动变**。
请运行同步脚本（或让数字公司提醒你运行）：

```bash
python <技能目录>/scripts/sync_embedded.py <专家包目录>
```

- 数字公司（经营主理人）每次会话开始会比对「内嵌副本 VERSION」与「用户级技能 VERSION」
  （`~/.workbuddy/skills/ontology-agent/VERSION`）；若不一致，会主动提示你执行上面的同步命令。
- 同步内容：SKILL.md / GUIDE.md / VERSION / references/ / scripts/ / connectors/ / experts-template/；
  **不会动**你的 `instance.yaml` / `company-memory.md`（那是你的数据，不属技能本体）。

## 数字公司主动引导你（渐进式 Onboarding）
你不用自己回忆「该告诉数字公司什么」——数字公司拥有 onboarding，会按优先级循序渐进补采企业数据：
每次只问 1~2 个最高优缺口，说明用途 + 安全安抚，绝不一次轰炸、不引发安全顾虑。
详见 `references/onboarding.md`；运行期由经营主理人调用 `scripts/onboarding.py` 取下一个问题、发进度播报。
通用演示种子见 `examples/demo_company/`（虚构示例公司，便于新用户照结构填自己的）。

## 24 部门库与用户私有定制（不改技能包整体性）
技能包内置 **24 个部门**（`experts-template/department_experts.yaml`）：
**12 核心**（领导/行政/人力/财税/法务/研发/内容/渠道/SEO/销售/数据/战略，默认团队）
+ **12 可选**（客户服务/产品/设计/运营/采购供应链/质量/IT安全/公关/投融资/客户成功/出海跨境/风控内控，按需激活）。
这样通用版默认还是 12（不破坏已验证体验），但包里弹药充足，覆盖绝大多数商业企业。

**用户可对任意部门做私有定制，且一律只存于自己的 `company-data/<公司>/instance.yaml`，绝不改动技能包本体：**

| 操作 | 命令 | 是否影响技能包 |
|------|------|----------------|
| 改名 | `python scripts/init.py --slug <简称> --rename finance 财务总监` | 否 |
| 指定性别（仅头像/语感） | `python scripts/init.py --slug <简称> --gender sales female` | 否 |
| 停用部门 | `python scripts/init.py --slug <简称> --disable mkt_seo` | 否 |
| 新增私有 AI 员工 | `python scripts/init.py --slug <简称> --add-dept cso --name 首席安全官 --gender male --expertise "安全战略、合规治理"` | 否 |
| 列出当前部门 | `python scripts/init.py --slug <简称> --list-depts` | — |
| 浏览 24 部门库 | `python scripts/init.py --catalog` | — |

> 合并逻辑见 `scripts/init.py: resolve_departments()`；详情见 `references/customization.md`。
> 数字公司在渐进式引导里会温和提议可选部门、并明确告知「这些改动只在你自己的公司数据里，不会改动技能包」。

## 头像与性别（提升体验感）
- 头像池 `assets/avatars/` 已内置：12 核心部门 × 男女两版（24 张）+ 团队图标 `team.png` + 4 张通用备用（男女各 2）。
- 每个部门有 `gender_default`（合理默认），用户用 `--gender` 覆盖后，重新生成/同步专家包即让对应头像生效，**性别只影响头像与语感，绝不改变部门能力**。
- 可选 12 部门与自定义部门若无专属头像，自动回退通用备用池；需要专属头像时一行命令即可生成。
- 把所选头像写入专家包：`python scripts/avatars.py --slug <简称> --pkg <专家包目录>`（已对微数实例执行）。

## 自主监测与自发行为层（锦上添花 · 零侵入 · Phase 10）
在用户**没主动安排工作、且内部正常工作不受影响**的前提下，数字公司额外「隔三差五」给企业挖出相关信息，
让用户感到「像有个好员工在帮我盯着」。本层是核心框架之上的**附加层**，不改动 24 部门模板 / 159 动作库 / 决策治理。

- **监测什么**：见 `references/monitoring.yaml`——8 个信号域（政策 / 行业热点 / 舆情 / 经营健康 / 竞品 / 客户 / 风险 / 人才），每项映射到真实部门 + 已有动作；
  **薄档案**（用户录得少）跑通用域（政策 / 行业 / 舆情 / 经营健康），**厚档案**（录得多）追加精准域（竞品 / 客户 / 风险 / 人才）。
- **自发逻辑**：见 `references/proactive.yaml`——触发管线（信号 → 相关性 → 价值评分 → 授权检查 → 决策 → 留痕）+ 四档分级：
  L0 静默（不相关只记不报）/ L1 轻提醒（汇入选报）/ **L2 草拟待确认（默认档）** / L3 授权内执行（仅低风险常规动作）。
- **运行**：`scripts/monitor.py` 解析薄/厚档案并写入 signals；`scripts/proactive.py` 分级并聚合「情报简报」。
- **护栏**：复用 `decision.yaml` 的 PII / 合规红线与 人设D 授权边界；**越权（报税/开票/重大合同/资金转出）一律降级 L2 草拟 + 等确认**，绝不 L3。
- **默认开**：政策巡检（周）+ 经营日报（日）；其余（舆情 / 竞品 / 客户 / 风险）在专家中心一键开启，不打扰。
- **体验落点**：用户少录也「天天有料」，且被自然引导补档案；厚档案像专属高管助理。统一交付物是隔 1–3 天推一份「企业情报简报」。

## 三档运行时（一份规范三次售卖）
- ③ **WorkBuddy 云**（单人 SaaS 起步）
- ② **端云协同**（企业内网，以面壁 EdgeClaw Box 等为参考实现）
- ① **纯本地私有 agent**（Palantir 式 air-gapped）
- 关键：`template`（随本 Skill 发）与 `instance`（用户运行时生成、存本地/私有）严格分离 → 数据不出域，三档通用。

## 知识产权与许可
本体论智能体（Ontology Agent）是**天津市微数人工智能科技有限责任公司**的产品，其自有架构、整合逻辑、汉化与国内化深度内容、引导引擎等原创表达归微数所有（© 微数），可闭源、可商用。
底层所参考的开源组件版权归各自作者所有，按相应许可保留声明，详见 `THIRD-PARTY.md`。

## 联系方式（厂商）
本产品由**天津市微数人工智能科技有限责任公司**出品。用户若想了解官网、获取技术支持，或升级更专业的企业级部署，可通过以下渠道联系微数 AI（详见 `references/contact.yaml`，AI 可直接读取并回答用户询问）：
- 官方网址：https://ontoagent.net
- 联系邮箱：378330966@qq.com
- 联系电话：15555555966
- 企业级方案（私人订制 / 端云协同 / 对标 Palantir 的纯本地算力私有化数字公司系统）：需企业自备本地算力服务器及相关硬件设备，通过上述渠道联系微数 AI 获取技术支持。

## 行业包（已内置企业类型模板）
技能按企业类型匹配 `references/packs/` 下的包，把行业特有实体/部门侧重/风味/红线注入实例，零侵入通用 24 部门库。

| 包 | 适用企业 | 部门策略 |
|----|----------|----------|
| `opc.yaml` | 一人公司（首发） | 12 核心 |
| `ecommerce.yaml` | 电商 | 12 核心 + 电商风味 |
| `sme.yaml` | 小微 | 12 核心 + 小微风味 |
| `manufacturing.yaml` | 制造业工厂 | 12 核心 + 运营/采购/质量 + 细分亚型 |
| `public_institution.yaml` | 事业单位 / 行政事业单位 | 12 核心 + 运营/采购/质量 + 国资/内审/党务政务(私有定制) |
| `finance.yaml` | 金融机构（银行/证券/保险/基金/信托/支付） | 12 核心 + 风控/IT安全/投融资 + 合规反洗钱(私有定制)，红线参考非法律意见 |
| `biomed.yaml` | 医疗 / 生物医药（医院/制药/器械/基因） | 12 核心 + 质量/IT安全/客服 + 医务/注册/药物警戒(私有定制) |
| `edu_research.yaml` | 教育 / 科研院所（学校/研究院/新型研发） | 12 核心 + 运营/质量/投融资 + 教务/科研管理/成果转化(私有定制) |

**制造业工厂包（manufacturing.yaml）** 采用「一个主包 + 内置 subtypes 段」覆盖细分行业，不为每种细分各写一个文件（避免臃肿）：
- 共性：工厂/产线/设备/工艺/工单/良率/产能/物料/BOM/供应商实体；生产→质检→交付核心循环；
  安全生产/环保/质量体系(ISO9001·IATF16949·GMP·CCC)/特种设备/消防 红线（decision.yaml `manufacturing_safety`）；
  制造特有监测信号（设备停机/OEE、良率波动、断料、安环事故、能耗、召回，见 monitoring.yaml `manufacturing` 域）。
- 12 个细分亚型（按 match_keywords 自动匹配，只补差异）：服装纺织 / 食品饮料 / 电子电器 / 机械装备(重工) /
  化工 / 建材家居 / 医药生物 / 日用消费品 / 汽车及零部件 / 金属冶炼 / 包装印刷 / 塑胶玩具。
- 制造业「心脏」部门（生产制造/设备工程/工艺工程）不在 24 部门通用库，通过 `suggested_custom_departments`
  建议用户私有定制添加，不改动技能包整体性。

## 可移植部署与对接（Mode B / Mode C 落地）
规范层是厂商中立数据，三模式 = 同套规范 + 不同运行时外壳。**换壳即用，业务大脑不丢、不重写**。
- 导出规范：`python scripts/export_spec.py --bundle all --slug <简称> --zip` → 生成自包含 `exports/<简称>_ontology_bundle/`（含全部 `references/` + 实例 + `manifest.json` 契约）。`--bundle source` 只导出空白规范模板，`--bundle instance` 只导出数字孪生。
- 对接运行时：`python scripts/adapters.py --bundle exports/<简称>_ontology_bundle --pattern edge_cloud`（厂商中立模式清单，主产出）
  - 参考实现样例（任选）：`--target edgeclaw`（面壁 EdgeClaw Box）/ `--target joyagent`（京东 JoyAgent-JDGenie）/ `--target both`
  - **Mode B 云端协同（参考实现样例：面壁 EdgeClaw Box）**：产出 `edgeclaw_manifest.yaml`，`sync_boundary` 敏感留端、外脑上云，按部门敏感度自动划端云（`lead/admin/hr/finance/legal` 留端）。
  - **Mode C 纯私有化（参考实现样例：京东 JoyAgent-JDGenie）**：产出 `joyagent_manifest.yaml` + `joyagent.docker-compose.yml`（部署模板提示），完全离线、本地模型、规范零改写、ERP/MES 写回钩子。
- 宿主平台"包装脚手架"（回答"是否只适用于 WorkBuddy"）：`python scripts/adapters.py --slug <简称> --target coze|dify|claude|yuanqi|qianfan|workbuddy` → 把同一套厂商中立规范 port 到竞品平台，规范零改写。
- 两个脚本只读 references / 实例，**绝不修改**核心；对接 manifest 只「引用」规范（`./references`、`./instance`），零改写——这正是「完美自洽接入」的地基。完整流程见 `references/portability.md`。

## 术语约定（双语术语标准层）
所有 yaml 机器 key 用英文、用户面中文，对照见 `references/glossary.yaml`。新增术语先登记 glossary 再使用。

**标准层范围（2026-08-15 扩完）**：`glossary.yaml` 已覆盖——核心四层 / 原子概念 / 打包实例化 / 治理安全 / 8 行业包 / 运行时三档 / 连接器 / 来源代号 / **24 部门码中英** / **18 语义实体中英** / 参考库来源。
该对照层会在专家 `system_prompt` 注入一段「术语标准层·中英对照」附录（见 `scripts/init.py: glossary_block()`），确保每个 AI 员工输出时统一使用中文术语、且能识别系统内部英文标识——标准层**真正被使用**，而非空置。
登记 IP 用途：用户面术语不带「原创/借鉴」标注；来源代号段仅记录动作溯源（OPB/Frog/slav/ReS/sober/easy 为借鉴、WSHU 为微数自创），登记专用附件再走「引用+轻量修改优化+不主张独占」纪律。

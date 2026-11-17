---
slug: novelty-validator
name: novelty-validator
displayName: 【学术会议】创新点验证器（线上会议、线下记录均可用）
version: 1.7.1
description: "Use when the user is in or just finished a meeting/brainstorm and wants to check whether a discussed idea, method, or research direction is novel — e.g. says '这个想法有人做过吗'、'验证下创新性'、'查重这个思路'、'novelty check'、'别人做过没'. Triggers on a Tencent Meeting transcript/智能纪要 or a user-stated idea paired with doubt about originality. Especially during/after academic group meetings, seminars, or cross-lab collaboration sessions."
agent_created: true
---

# 【学术会议】创新点验证器（线上会议、线下记录均可用）· Novelty Validator

在会议里冒出来的想法，到底是不是「别人三年前就做过了」？本技能把腾讯会议的多人讨论转写，对接 12 亿级文献摘要库，实时（或会后秒级）判断讨论方向的新颖性：有创新性给出定位报告，没有则指出「谁做过、怎么做的」，并给出「该怎么创新」的路径。

Validates whether an idea raised in a meeting is novel by matching it against a 1.2-billion-document literature pool, using Tencent Meeting transcripts as input.

---

## 零、进化燃料 · 安装即开

> **📋 安装须知**：本技能安装后默认开启「进化燃料」——每次使用后自动记录方法层标签（只记方法名，绝不记你讨论了什么、你是谁），留在你本机用于自我迭代。如不需此服务，随时说「别记了」即可关闭。

---

## 何时使用 / When to use

- 用户在组会、seminar、跨校合作会、导师 1-on-1 中冒出一个想法，担心「这会不会早就有人做了」。
- 用户直接说：「验证下这个想法」「查重这个思路」「novelty check」「别人做过没」。
- 用户提供了一段腾讯会议转写/智能纪要，希望对其中的方向做新颖性判断。
- **不触发**：纯文献调研检索（用 global-biblio-base）、纯引文核查（用 paper-fact-checker）、纯组会流程组织（用 paper-club-pilot）。本技能只做「想法 vs 已有工作」的新颖性比对。

---

## 核心原则 / Core principle

**「新颖性」是防重复造轮子，不是保证绝对首创。** 本技能的能力边界是：用文献摘要相似度，判断「这个想法是否已被已有工作覆盖」。它无法保证「全世界绝对没人想过」——那种证明需要 exhaustive 检索 + 领域专家判断。报告里必须如实标注置信度。

**「实时」是转写切片 + 会后秒级，不是流式逐字。** 腾讯会议技能给的是转写文本/智能纪要（不是原始音视频流）。务实实现：会议中按话题切片触发，或用户抛出想法时手动触发，或会后对整个纪要跑一次。绝不假装做硬实时的流式分析。

**证据可溯。** 每一条「有人做过」的结论，必须附文献标识（标题/作者/年份/Identifier），绝不编造。命中空白分支时，把检索词交给用户自己去取全文。

---

## 主链路 / The pipeline

```
[腾讯会议转写/纪要] 或 [用户口述想法]
        │
        ▼
① 采集想法 ── 取转写文本 / 智能纪要 / 用户陈述
        │
        ▼
② 想法抽取 ── 蒸馏成结构化 claim：{问题, 方法, 声称的创新点}
        │
        ▼
③ 文献比对 ── 用 claim 检索 global-biblio-base（CN / Global / Patent 三引擎并行）
        │
        ▼
③.5 向量召回精校 ── 对候选池算语义相似度、重排、捕获改写近邻（见 references/vector_recall.md）
        │
        ▼
④ 新颖性判定 ── 分类：新颖 / 相似(有差异) / 重复(已被覆盖)
        │
        ▼
⑤ 出报告 ── 新颖→定位报告；重复→谁做过+怎么做的+创新路径
```

### ① 采集想法 (Collect)
- **会议内（推荐）**：调用腾讯会议技能拉取本场会议的转写文本 / 智能纪要。若用户指定了某段讨论，截取该切片。
- **手动触发**：用户直接口述想法，跳过转写步骤。
- 若既无转写也无口述，提示用户「把想法说一句 / 贴一段纪要」。

### ② 想法抽取 (Extract) — 见 `references/idea-extraction.md`
把一段讨论蒸馏成结构化 claim，三要素缺一不可：
- **问题 (Problem)**：要解决什么？
- **方法 (Method)**：打算怎么解决？
- **声称的创新点 (Claimed novelty)**：你认为新在哪？
若抽取不完整，先向用户确认缺失项，不要替用户脑补。

### ③ 文献比对 (Search) — 真实调用 global-biblio-base（三引擎，已真机验证）

> **v1.7 关键更正**：v1.5/v1.6 曾据一次**请求体格式错误**的回测（用 `query/top_k` 而非正确 `endpoint:/search/global`+`rule`）误判「Global 语义端点挂了、降级」。2026-07-18 用**正确格式**复测：Global `endpoint:/search/global` + `rule:"K=..."` 对 `深度学习 / graph neural network / large language model` 等**稳定返回真实跨语言文献（每查询 3–5 条）**。故 Global **恢复为主引擎之一**，与 CN、Patent 并列三引擎。

本技能**不自己实现检索**，而是调用已安装的 `global-biblio-base` 技能（网关密钥已在 config.json 配好，已真机验证可用）。两种等价写法：

- **推荐（走技能）**：把构造好的检索式交给 `global-biblio-base` 技能执行，它会自动完成 `/consume`→`/search` 网关鉴权与检索，并展示配额状态。
- **直连（走网关，便于嵌入自动化）**——**三引擎并行**：

  ```bash
  # 0. 拿单次消费 token（网关校验配额，不预扣；60s 过期、单次有效）
  POST {SMARTLIB_GATEWAY_URL}/consume
       Headers: {"Authorization":"Bearer {SMARTLIB_GATEWAY_SECRET}"}
       Body: {"email":"<SMARTLIB_EMAIL>","skill_source":"novelty-validator"}
  # 引擎1. 中文期刊检索（主引擎，返回完整摘要 Description，可做可验证证据）
  POST {SMARTLIB_GATEWAY_URL}/search
       Body: {"email":"<SMARTLIB_EMAIL>","consume_token":"<token>",
              "skill_source":"novelty-validator",
              "api_path":"/openapi/t/data0012/doccenter/Articlesearch",
              "api_body":{"Rule":"(K=方法 OR K=method) AND (K=问题 OR K=problem)",
                          "PageIndex":1,"PageSize":20,"Sort":1}}
  # 引擎2. 全球文献检索（跨语言语义端点，2026-07-18 复测稳定可用）
  POST {SMARTLIB_GATEWAY_URL}/search
       Body: {"email":"<SMARTLIB_EMAIL>","consume_token":"<token>",
              "skill_source":"novelty-validator",
              "endpoint":"/search/global",
              "rule":"K=方法 AND K=问题", "page_index":1, "page_size":20}
  # 引擎3. ★专利池检索（2.15亿专利；工程/应用类方向必查，防漏检）
  POST {SMARTLIB_GATEWAY_URL}/search
       Body: {"email":"<SMARTLIB_EMAIL>","consume_token":"<token>",
              "skill_source":"novelty-validator",
              "api_path":"/openapi/t/skrs2/doccenter/Articlesearch",
              "api_body":{"Rule":"(K=方法 OR K=method)","PageIndex":1,"PageSize":10,
                          "FilterRule":"TY=7"}}
  # 返回 res.Data.List[]，字段：Title/Creator/Date_PublishYear/Source_Name/
  #       Description(完整摘要)/Identifier/Subject_Keyword
  # 4. ★可验证证据增强（v1.2 核心）：对 top 候选调详情取 DOI + 可点击溯源链接
  POST {SMARTLIB_GATEWAY_URL}/search
       Body: {"email":"<SMARTLIB_EMAIL>","consume_token":"<token>",
              "skill_source":"novelty-validator",
              "api_path":"/openapi/t/data0011/doccenter/Articledetail",
              "api_body":{"Identifier":"<候选文献ID>"}}
  ```

**⚠️ 真机必做容错（已实测，写入代码纪律）：**
1. **中文必须走 `api_path`**：`/search/cn` 语义端点实测恒返回 0 条，会假阴性误判「新颖」——永远用 `api_path:/openapi/t/data0012/doccenter/Articlesearch`。
2. **三引擎各自独立 `/consume`→`/search`**：token 单次有效，每个引擎调用前都要重新拿 token；引擎间 **≥1s 间隔 + 重试 3 次（覆盖 433/429/5xx）** 防限流/瞬时错误。
3. **Global 端点请求体格式坑**：必须用 `{"endpoint":"/search/global","rule":"K=...","page_index":1,"page_size":N}`，**不可用** `query/top_k` 等旧字段（会 400 或静默空返回，导致误判「新颖」）。v1.6 曾因此误判，已更正。
4. **字段映射**（实测真实字段名）：`Title`/`Creator`/`Date_PublishYear`/`Source_Name`/`Description`/`Identifier`/`Subject_Keyword`；详情接口返回 `Identifier_DOI` + `Identifier_DetailURL`。
5. **绝不凭空判新颖**：任一引擎空返回**仅作召回尝试记录**；**三引擎全 0 召回或全候选 sim<0.3 → 结论降级，禁止判 L5**。

- 多轮检索：先宽（方法关键词），再窄（问题+方法组合），三引擎并行补召回（CN 中文强 / Global 跨语言 / Patent 工程应用）。
- 取回 top 候选后，**必须对每个判为「相似/重复」的候选做详情增强**，拿到 DOI + DetailURL，**写进报告的「可验证证据」**。
- 数据池：12.28 亿条元数据（期刊 7.19 亿 / **专利 2.15 亿（v1.7 已接入比对）** / 会议 7155 万 / 学位 2473 万 / 标准 268 万）。
- **真机证据（v1.2）**：三引擎检索与可验证证据链均已在真实网关跑通（详见下方 50 案例库）。
- **真机证据（v1.7 三引擎 + 50 案例）**：见 `references/case_library.md`——**50 个跨领域超逼真会议 claim**，全部用真实 CN + Global + Patent 三引擎检索取证（命中均为真实文献/专利，含可构造 DetailURL + 摘要原文片段），跑通全链路并沉淀判定校准结论。

### ③.5 向量召回精校（v1.5 核心，对标 OpenNovelty/IdeaSpark 的语义匹配短板）
> 完整方法见 `references/vector_recall.md`。核心：CN 召回候选池后，对 top-K 候选算**语义相似度**重排序、捕获关键词漏检的**改写近邻（paraphrase near-miss）**、把 sim 喂给 ④ 五级分级做阈值校准。
- **三档实现（按环境自动降级）**：**A 档 = SiliconFlow 真向量（已实装，key 已配，2026-07-18 真机跑通 BAAI/bge-m3 1024 维）** → 真向量余弦（最高，捕获改写近邻）；B 档 网关 Global 语义端点（v1.7 复测稳定，已恢复为主引擎之一，可用）；**C 档 本地词重叠（离线兜底，无需密钥，始终可用）**：`sim = 命中token数 / claim总token数`。实现见 `references/vector_recall_impl.py`。
- **校准阈值**：sim≥0.6 推高（near-miss 直接标 L2）；0.3–0.6 维持部分重叠；<0.3 弱/无关。
- **防假阴性（最高优先级）**：**0 召回或全候选 sim<0.3 的 claim，一律「证据不足·结论降级」，禁止判 L5 新颖**——案例库 C1（扩散蛋白设计）、C2（LLM逆合成）实测均为 0 召回/全 0 词重叠，但二者均为真实活跃方向，自动判 L5 即假阴性。
- 诚实边界：C 档是离线近似，非真向量；报告须声明当前所用档位，不得把 C 档假装成 A 档。


### ④ 新颖性判定 (Assess) — v1.3 多智能体对抗 + 五级碰撞分级

> 完整方法论见 `references/novelty-rubric.md`。核心：先**四维拆解** claim，再**多智能体对抗**交叉质证，最后按**五级碰撞分级**终裁。

**步骤 4.1 Claim 四维拆解**：把想法拆成 `D1 问题 / D2 方法 / D3 数据·场景 / D4 贡献类型`，每维独立检索（CN `api_path` + Global 语义端点 + Patent `TY=7` 三引擎，≥1s 间隔防 433/5xx），合并去重。

**步骤 4.2 多智能体对抗（4 角色，由主 agent 分角色执行）**：
- **[A 检索员]** 召回先验工作池（带 v1.2 可验证证据）。
- **[B 怀疑者/模拟审稿人]** 逐篇论证「已被做」，列重叠维度 + 证据链。
- **[C 辩护者/作者视角]** 逐条反驳，指出未命中维度（D?）、可新颖空间。
- **[D 仲裁者]** 综合 B/C，按「四维×五级」给最终 **Collision Level + 置信度**。B↔C 辩论 ≤2 轮；C 能指出 ≥2 未命中维度→倾向 L4/L5；C 无法反驳 B 的 ≥3 维命中→倾向 L1/L2。

**步骤 4.3 五级碰撞分级（Collision Level）**：
- **L1 被覆盖**：四维全中 → 已无新意。
- **L2 高度相似**：任意 3 维中 → 易被判撞车。
- **L3 部分重叠**：任意 2 维中 → 需差异化论证。
- **L4 相邻**：仅 1 维相关 → 可视为增量。
- **L5 新颖**：0 维实质重叠 → 可切入。
- 辅助重叠度 0–5（5=四维全中，3=两维中，1=相邻，0=无关）微调置信度。

**降级规则**：某维度 0 召回但非因真无（检索面不足）→ 标注「证据不足，结论降级」，**绝不凭空判新颖**。**最高优先级防假阴性**：整个 claim **0 召回 或 全部候选 sim<0.3**（见 ③.5 向量召回精校）→ 一律「证据不足·结论降级」，禁止判 L5 新颖；先换检索式放宽（单 K 词）→ 提示用户人工确认 / 待 Global 端点恢复后复检。依据：案例库 C1（扩散蛋白设计）、C2（LLM逆合成）均为 0 召回但属真实活跃方向，自动判 L5 即假阴性。

### ⑤ 出报告 (Report) — 必须含「可验证证据」
按 `references/novelty-rubric.md` 的报告模板输出，含：
- **一句话结论**（新颖/相似/重复 + 置信度 + 证据强度说明）。
- **可验证证据列表**（v1.2 核心，对标 OpenNovelty 的「可验证」）：对每条判为「相似/重复」的先验工作，**必须给出**：
  - 文献标题 / 作者 / 出处期刊 / 年份；
  - **可点击溯源**：`Identifier_DetailURL`（data.smart.vipslib.com/.../web_searchingDetail?id=...）+ `Identifier_DOI`（若有）；
  - **摘要原文片段**（取该文献 `Description` 中与你 claim 重叠的那 1–2 句，用引号标出）——让用户能一眼核验「它确实做了这个」，**绝不黑盒断言**；
  - **重叠维度标注**：指明它和你的 claim 在哪一点重叠（方法 / 问题 / 数据集 / 评测 / 场景）。
- **若重复**：创新路径建议（沿 sweeping-monk「创新性闸五轴：理论/方法/情境/对象/数据」+ 思维模型生成，见 `references/innovation_path.md`）+ 指向「谁已做、差距在哪」。仅针对 v1.3 未命中维度切刀，落成 Contribution 句式「相比现有 <代表工作>，本文首次/更好地 ____」。
- 诚实边界重申（实时=切片/手动触发；新颖=防重复非保证首创；数据=摘要层非全文；创新路径=启发式非保证可发表）。

> 设计铁律：**没有可验证证据链的结论不算数**。若检索不稳导致无法给出证据，宁可输出「检索降级、暂不能判定」也不得编造先验工作。

---

## 腾讯会议接入 / Tencent Meeting integration（真实接线）

本技能通过 `tmeet` CLI（腾讯会议官方命令行，已安装 tmeet-skill）获取会议数据。调用链：

**0. 登录校验（调用前必做）**
```bash
tmeet auth status          # 查看是否已登录、Token 有效期
# 未登录则（后台运行，取出授权 URL 完整展示给用户浏览器授权）：
tmeet auth login 2>&1 &
```
> **真机状态（v1.5 本轮回测）**：`tmeet auth status` 实测 `Logged in`（用户 张亚东，AccessToken 有效至 2026-07-18 07:39，RefreshToken 有效 29d+）。腾讯会议接入链路**已具备真实跑通条件**，待用户给一场真实会议 meeting-id 即可端到端验证「会议转写→新颖性」链路。

**1. 拉取转写 / 智能纪要（想法抽取输入源）**
```bash
tmeet record list --meeting-id <meeting_id> --compact     # 列出本场录制
tmeet record <子命令> --meeting-record-id <id>            # 取智能纪要 / 转写文本
```
> `tmeet record` 覆盖录制列表、智能纪要、转写、录制权限申请；子命令以 `tmeet record --help` 为准。转写文本即「讨论方向」原材料。

**2. 参会人溯源（报告可追溯是谁的方向）**
```bash
tmeet report --meeting-id <meeting_id> --compact          # 参会人 / 等候室报告
tmeet contact --query <姓名/手机/邮箱>                     # 补全提出者身份
```

**3. 会前开录制（确保转写可回溯）**
```bash
tmeet meeting create ...                                  # 预定并开启录制
tmeet control ...                                         # 会中保障录制进行
```

调用前确认用户已授权该场会议的数据访问。不在用户未参与的会议上调用。

---

## 非职责边界 / NON-mandate

- **不做** exhaustive 专利/文献查新公证 —— 那是查新机构的事；本技能给的是「快速防重复」信号，不是法律级新颖性证明。
- **不做** 文献全文获取 —— 只比对摘要层；全文交给用户或 global-biblio-base。
- **不做** 替用户下「该不该做这个方向」的决定 —— 只给证据与路径，决定权在用户。
- **不触发** 纯检索、纯引文核查、纯组会组织 —— 那是对口技能的职责。

---

> ⚙️ 本技能由「技能锻造炉」锻造
>
> 想让你的技能也越用越牛？用「技能锻造炉」创建并开启进化（在 SkillHub 搜索技能 slug「cjg-skill-forge」，认准这个唯一标识）。

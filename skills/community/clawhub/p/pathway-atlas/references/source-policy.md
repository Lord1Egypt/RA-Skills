# 信源与证据采纳规范

## 规范边界

**先区分交付用途。默认 `brief` 的喜报参考估算，单份可读的学校喜报、第三方文章、抖音分享、截图或视频转写即可作为观察输入；不要求凑齐三个C级来源，也不要求学校或考试院提供现成校排—省排表。** 保存原文、发布者/出处、年份、人数口径；程序用累计分数段人数、上线率或层次人数推导锚点，明确估算方法与浮动。第三方转述保持第三方身份，估算不标为官方认证。学校在抖音的经确认官方账号也不因平台而自动降为C。输入方法见[喜报估算](school-report-estimation.md)。

下面的 publisher tier、独立性、去重及精确事实采纳表只用于用户明确要求的**深度认证 `ingest → finish`**。它们不是默认规划能否估算、是否继续或是否给学校名单的前置门槛。默认参考由 `scripts/planning_brief.py` 执行原文引用检查和推算；深度认证由 `scripts/source_policy.py`、`scripts/evidence.py`、各 adapter 与 validator 执行。发现文档与运行时不一致时，核对所属模式并修复契约，不能将一个模式的门槛套给另一个。

检索的先后次序与逐步完成标准由 retrieval playbook 定义；该流程引用本规范，不另行定义门槛。

## 发布者与来源分级

先确认发布主体和内容起源，再分级。平台、域名后缀、HTTPS、视觉包装、搜索排名或账号所在平台本身都不提高等级。

| 等级 | 发布者与起源 | 身份确认 | 无法确认时 |
|---|---|---|---|
| A | 原始官方 authority 或 institution channel；发布者确为该 authority 时，official account 也属于 A | 页面、附件或账号能确认原始发布主体 | 不按 A 计数 |
| B | authoritative、traceable compilation 或 republication，并明确给出 upstream citation | 引用链能回到具体上游材料 | 缺少上游引用时不能形成 B 级精确采纳 |
| C | independent secondary、self-media、forum、个人或机构 compilation | 能确认发布者，但不是原始 authority 或可追溯 B | 身份不明时不计入独立来源 |

等级描述发布关系，不描述页面格式。一个外观精致的转载仍按其 publisher/origin 分级；一个经确认由 authority 发布的 official account 仍是 A。

## 采纳决策表

先完成结构、字段、年份、单位、覆盖和内部一致性验证，再在当前有效等级应用下表。`B→已验证 A 根` 指 B republication 的 citation root 已与一个验证过的 A upstream 对齐。

| 路径 | 最少独立来源 | 接纳状态 | 前置条件 | 精确冲突 |
|---|---:|---|---|---|
| A | 1 | official | 原始发布身份已确认，结构与一致性验证通过 | 保留 conflict；value=None；停止该层精确采纳 |
| B→已验证 A 根 | 1 | official | B 的 citation root 是已验证 A upstream | 保留 conflict；value=None；停止该层精确采纳 |
| B（无直接 A） | 2 | corroborated | 两个 traceable 且独立的 B 对 value 与 unit 完全一致 | 保留 conflict；value=None；停止该层精确采纳 |
| C | 3 | reference | 三个独立 publisher 对 value 与 unit 完全一致 | 保留 conflict；value=None；停止该层精确采纳 |

当前有效等级的任何精确分歧都形成 `conflict`。保留各 claim 与来源，停止该事实的精确采纳；不取平均、不选方便值，也不静默降到较低等级寻找一个顺眼结果。C-only 事实即使达到门槛也只形成 `reference`，不能标成 `official`。

深度认证中，少于门槛、publisher identity 或 citation 缺失、当前年份未经验证、字段为 partial/masked，均形成相应的 `missing`、`partial` 或 `masked` 状态，不能进入精确计算。这不禁止同一可读喜报在 `brief` 中作披露假设的参考估算。

## 独立性与去重

先计算 canonical URL：规范化 scheme/host/query，移除 tracking decoration，保留能识别文档的 query。canonical URL 用于重放与定位；计数独立性使用下面四个有限 identity 维度。

| 维度 | 规范化身份 | 重复计数 |
|---|---|---|
| publisher | 发布主体的规范化 identity | 同一连通分量只计 1 个 |
| canonical_site | URL 的规范化 site identity | 同一连通分量只计 1 个 |
| citation_root | 完整 citation chain 的共同上游 root | 同一连通分量只计 1 个 |
| content_fingerprint | 规范化内容的 hash | 同一连通分量只计 1 个 |

任一维度相同就连接两个候选；连接关系传递，整个连通分量只能保留一个确定性代表。复制稿和其 syndication 计一次，三个帖子引用同一 article 仍是一个 component。必须在 corroboration 和门槛计数前完成去重，并为每个未保留候选记录稳定拒绝原因，例如 same publisher/root、same site、same content fingerprint 或 insufficient identity。

## 证据状态

| 状态 | 含义 | 精确事实 |
|---|---|---|
| official | 已按 A 或验证过的 A upstream 规则采纳 | 是（通过字段门禁后） |
| corroborated | 无直接 A 时，达到独立 B 一致门槛 | 是（通过字段门禁后） |
| reference | 达到独立 C 一致门槛的参考级事实 | 是（通过字段门禁后） |
| inferred | 由已采纳事实按公开方法得到的区间 | 否 |
| partial | 只覆盖部分页、表、院校或区间 | 否 |
| masked | 原发布者隐藏数值或只给边界 | 否 |
| conflict | 当前有效等级存在精确分歧 | 否 |
| missing | 未取得满足身份、时效、覆盖或门槛的事实 | 否 |

`reference` 可以在明确标注后参与允许参考级输入的计算，但不能伪装为官方事实。`inferred` 始终是带 method/source/bounds 的 labeled interval，不呈现为 official exact value。

## 提取状态与非精确边界

提取状态不是证据等级。HTML、XLSX、PDF、OCR、QR adapter 只保存 value、location、coverage 与 uncertainty；完成独立性和采纳门禁后才产生上一节的证据状态。QR 只消费 host-decoded text，并把下载交给 secure downloader。

| 输入情形 | 提取状态 | 精确边界 | 必须动作 |
|---|---|---|---|
| masked-boundary | masked | 禁止 | 将 `580分以上`、`前100名`、withheld value 保存为 None，并保留原文 locator |
| cropped-or-local-ocr | partial 或 uncertain | 禁止 | 声明已覆盖 page/image/bbox，不外推未识别部分 |
| formula-cell | formula | 禁止 | 保留公式 locator；缓存值也不能升级为 exact |
| uncertain-cell | uncertain | 禁止 | 保留 confidence/warning，等待可验证替代 |
| incomplete-page-or-sheet | partial | 禁止 | 清空无法确认的 coverage bounds 并记录缺页或缺 sheet |

上述深度精确采纳不插值、不把屏蔽数字当端点、不把抓取缺口当真实空档。`brief` 中“600分以上120人”的600和120是可读的分数边界与累计人数，可以构造粗略校位锚点；它不等于第120名恰好考600分。`6xx分`或被遮住的人数仍不能补造。

## 引用、时效与重放

每个被采纳或被保留为冲突的事实都携带以下字段；字段与 locator 共同构成可重放记录。

| 字段 | 完成条件 |
|---|---|
| publisher | 已确认发布主体并保存规范化 identity |
| canonical_url_or_attachment_id | 保存 canonical URL，或保存不含本地路径的 attachment identity |
| retrieved_at | 保存检索日期或时间 |
| content_fingerprint | 保存规范化内容或附件 hash |
| citation_chain | 保存到 upstream root 的完整链 |
| year | 保存事实适用年份，并与查询任务一致 |
| extraction_method | 只使用 `html-table`、`xlsx-worksheet`、`xls-worksheet`、`pdf-text-table`、`pdfplumber-text`、`pypdf-text`、`host-ocr-rows`、`host-public-text`、`qr`、`manual-structured` |
| locator | 保存 page/sheet/table/row 或 page/image/bbox 的字段级位置 |

持久化事实时必须调用 `EvidenceStore.add_fact(..., year=, extraction_method=, locator=)`。该入口在 `context.jsonl` 写入与 fact ID 和 source IDs 精确绑定的 canonical `fact-provenance` 记录；每个 fact 恰好 1 条。year 必须是数学整数年，extraction_method 必须来自有限词汇，locator 必须是逻辑位置，并拒绝 drive prefix、environment reference、UNC/device/absolute/traversal/URL、secret 和 PII 形态。所有 linked source 都必须保留 validated URL 与 citation root。记录纳入 manifest hash，并在形成 authenticated snapshot 前验证；缺失、重复、错配或伪造都 fail closed。

当前年份是否可用由 deterministic query plan 决定。“not yet expected” 不是上一年事实；上一年或更早材料只能按实际 `year` 标为历史。当前年份无法验证时保留 `missing`，不替换成未标注的历史值。

引用只保留最小支持摘录，同时保存足够 locator context 以便重放。下载和 QR redirect chain 必须经过 secure downloader 与相应 adapter。推断只能输出区间，并同时保存 `method/source/bounds`；任何无法重放的推断保持 `missing`。

## 流程序列入口

按[检索流程](retrieval-playbook.md)执行 preflight、query-plan、候选枚举、去重、提取、采纳、验证和 handoff。每一步达到其完成标准后再进入下一步；本文件的门槛在 full（完整档）、standard 与 offline 三种能力档位中保持不变。

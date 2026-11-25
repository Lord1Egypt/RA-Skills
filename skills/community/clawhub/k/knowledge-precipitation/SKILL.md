---
name: knowledge-precipitation
version: 0.1.45
description: |
  每日知识沉淀引擎（Knowledge Auto-Precipitation Engine，KAPE）v0.1.38。

## v0.1.26 更新说明（2026-10-29 断档修复）
- **根因**：2026-10-27 07:47 的 cron 无 run 记录，导致 2026-10-26 简报缺失，直到 10-29 心跳发现才补做，中间隔了 3 天无人察觉。每日流程只看「昨天」，不看「有没有缺」。
- **修复**：新增「第一步：归档连续性检查」——生成简报前先扫描最近 7 天的本地简报文件，发现除昨天以外的缺失日期即自动补做（按日期从早到晚）。
- **验证**：2026-10-29 手动补做 2026-10-26 简报，三端同步完成（Get笔记 1925469145576176384 / wiki PV2IwmpmFis3c9ko8mbc9zs2n0d / docx RGjYd8UyLo3lFTxJ8S2cmDYYnjd）。

## v0.1.25 更新说明（2026-10-24 Bug 修复）
- **根因**：飞书 DocxXML 中有序列表写成 `<ol seq="auto">` 会触发 schema 警告（degrade_code=5002）。
- **修复**：生成 XML 时有序列表一律用 `<ol><li>...</li></ol>`，不加 `seq="auto"`；`seq="auto"` 只能出现在 `<li>` 上，且本 skill 统一不使用。
- **验证**：2026-10-24 简报重写后两份文档 warnings 为空。

## v0.1.24 更新说明（2026-10-23 Bug 修复）
- **根因**：Step 4 用 curl 调飞书 drive permissions API 授权，Authorization header 是坏掉的占位符（`Bearer ***}`，语法错误）；且 SecretRef 模式下手动解析 tenant_access_token 只会读到 `***`。同时 `lark-cli wiki +node-create` / `docs +create` 在 bot 身份下自动授权返回 `permission_grant.status=skipped`（"no current CLI user open_id is configured"）。
- **修复**：Step 4 改用 CLI 原生命令显式授权，bot 身份即可生效：
  `${LARK_CLI} drive +member-add --token <document_id> --type docx --member-type openid --member-id ou_d8ace8a146610ca26bc07d8e68a5620f --perm full_access --yes`
- **验证**：2026-10-23 知识沉淀 cron 对知识库 docx 与共享文件夹 docx 两份文档均授权成功。

## v0.1.23 更新说明（2026-09-27 Bug 修复）
- **根因**：新版 OpenClaw（2026-09 大版本）使用 SecretRef 存储凭证，`secrets.json` 中 `apiKey` 字段值为 `***` 而非真实 key，导致 skill 的 base64 Python 脚本读取到无效凭证，Get笔记 save 全部失败（10004 未授权）。
- **修复**：删除所有 base64 Python 凭证读取脚本；`getnote` CLI v1.6.0 会自动从 `~/.getnote/config.json` 读取凭证，只需 `${GETNOTE_CLI} auth status` 验证即可，无需手动注入 key。

## v0.1.22 更新说明（2026-09-03 Bug 修复）
- **根因**：`lark-cli wiki +node-create`、`lark-cli docs +update`、`lark-cli docs +create` 在 `set -e` 环境下，若 lark-cli 返回非 0（网络超时、参数问题等），整个 exec 链中断，cron 报告 error 但文档实际已创建成功。
- **修复**：这三个 lark-cli 命令全部用 `set +e` 包裹，失败时打印警告而非阻断，后续用 `set -e` 恢复。自动完成：下载昨日Get笔记内容 → 结合对话记录 → 深度分析用户学习、感悟、工作状态 → 生成含主题关联图的日志简报 → 同步归档到 Get笔记（带标签）+ 飞书知识库 + 飞书文档。触发场景：「整理昨天的日志」「生成日报简报」「知识沉淀」「整理学习记录」「存档昨天的内容」。

## v0.1.21 更新说明（2026-08-27 Bug 修复）
- **根因**：Agent 实际执行时使用 `grep "${TARGET_DATE} " | grep -v "日志简报"` 管道过滤笔记，set -e 环境下 grep 匹配到 0 结果返回 exit 1，导致整个 exec 链中断。cron 报告 error 但简报文件实际已生成成功。
- **修复**：在任何 exec 命令链中执行 `grep` 过滤操作前，必须先用 `set +e` 包裹；grep exit 1 是正常行为（表示无匹配），不代表命令失败。

## v0.1.20 更新说明（2026-08-06 Bug 修复）
- **根因**：Step 5① `getnote save "<完整简报正文>"` 传的是字面字符串 `<完整简报正文>`，而非实际简报内容。导致 Get笔记保存的笔记内容是错误文字（如 `/dev/stdin` 或路径字符串）。
- **修复**：内容必须从 Step 4 生成的本地简报文件读取，使用 `$(cat "${BRIEFING_FILE}")` 命令替换读取实际内容。

## v0.1.19 更新说明（2026-07-26 Bug 修复）
- **根因**：permission grant curl 失败时 `set -e` 导致整个 exec 链中断，cron 报告 error 但文档实际已创建成功
- **修复**：grant curl 用 `set +e` 包裹，失败时打印警告而非中断；Authorization header 变量拼接改用双引号

## v0.1.18 更新说明（2026-06-27 凭证修复）
- 同步版本号至 0.1.18，修正 skill_workshop 注册信息。

## v0.1.15 更新说明（2026-06-27 Bug 修复）
- **根因**：cron isolated session 不会自动注入 `GETNOTE_CLIENT_ID` 和 `GETNOTE_API_KEY` 环境变量，导致 `getnote auth login` 失败，提示"API未授权"。
- **修复**：新增「运行时凭证读取」章节，所有调用 Get笔记 CLI 的步骤均需先从配置文件（openclaw.json + secrets.json）读取凭证后再执行，彻底摆脱对环境变量的依赖。

## v0.1.14 更新说明（2026-06-06 Bug 修复）
- **根因**：cron 执行时使用了 `grep "^2026-06-05"`（行首匹配），但日期在最后一列（行首是笔记 ID），导致 7 条笔记全部漏读。v0.1.12/v0.1.13 均已警告此 Bug，但执行端仍违反。
- **SKILL.md 强化约束**：在命令示例中直接写出正确的 `grep` 命令，**禁止**使用行首锚 `^`。

## v0.1.13 更新说明
- **Get笔记日期过滤逻辑再次确认**：CLI 输出格式为 `ID | Title | Type | Created`，日期在**最后一列**，行首是笔记 ID（不是日期）。过滤必须用 `grep "${TARGET_DATE} "`（尾部空格避免部分匹配），严禁用 `grep "^${TARGET_DATE}"`（行首不是日期，永远匹配不到）
- **分页读取逻辑补全**：当笔记数量超过 limit（200条）时，用**最后一条笔记 ID** 作为下次 `since-id` 参数继续读取，循环直至 `has_more=false`，确保不漏读

## v0.1.12 更新说明
- **修复 Get笔记 日期过滤 Bug**：`grep "^2026-05-28"` 永远匹配不到（行首是笔记 ID，不是日期），应改为 `grep "2026-05-28 "`（日期在最后一列，尾部加空格避免部分匹配）
- 同时排查其他 skill：getnote/references/list.md 已补充 CLI 输出格式说明；tech-news-daily 和 sci-china-reviewer 均无需修改

## v0.1.11 更新说明
- **修复重复创建 Bug**：SKILL.md 描述的工作流与实际 CLI 命令不匹配，导致 Agent 摸索尝试产生冗余文档/笔记
- **根因**：
  - Get笔记 SKILL 写的是直接调 HTTPS API（会返回 10004 未授权），实际应使用 `getnote save` CLI
  - 飞书文档 SKILL 写了"先创建空文档 → 再写入内容"的两步流程，但写入失败重试时 Agent 又创建了新文档
- **修复**：统一使用 CLI 的原子操作（一次命令完成创建+写入），禁止分步创建空文档再写入

## v0.1.10 更新说明
- **修复飞书知识库同步失败 Bug**：cron 报告成功但实际未同步到知识库「日志简报」节点
- **根因**：Step 5 飞书知识库操作没有明确指定 parent_node_token，导致节点创建到了错误位置（根目录或其他节点下）
- **修复**：在 Step 5② 飞书知识库部分明确写入正确的节点层级结构；必须先创建 wiki 节点（获得 doc_token），再写入文档内容

## v0.1.8 更新说明
- **修复星期几判断 Bug**：Agent 禁止凭推理判断日期对应的星期几，必须用 `date -jf "%Y-%m-%d" <日期> +%A` 命令验证。Bug 原因：Agent 用当前日期倒推"昨天是周几"时出错（2026-05-11 本是周一，推断成周日）
- 第一步增加强制要求：先输出 `目标日期：YYYY-MM-DD（周X）` 再开始生成内容

## v0.1.7 更新说明
- 新增强制完整输出规则：无论输入数据多少，哪怕只有1条笔记，也必须生成完整模板的所有区块（主题关联图、数据概览、核心主题、每条笔记的详细分析、张公子关注什么、可以改进什么、明日关注、关键词、今日洞察）。简报不是摘要，是完整的结构化记录。当某日数据较少时，每个主题下的「分析/联想」部分可以简短，但不得省略整个区块。

## v0.1.6 更新说明
- 新增内容过滤规则：排除科技新闻日报生成的内容（本地文件、飞书文档链接、相关新闻笔记均不纳入日志简报）

## v0.1.5 更新说明
- 新增主题关联图功能：帮助快速定位知识节点
- 日志简报结构优化：主题关联图位于数据概览之后、核心主题之前

## v0.1.4 更新说明
- 新增第零步：Get笔记授权检查与自动刷新（电脑重启后 CLI 认证状态丢失时自动修复）
- API Key 从配置文件读取后直接传给 CLI，不记录任何日志，防止隐私泄露

## v0.1.3 更新说明
- 修复 memory 文件路径格式问题（Markdown 链接语法导致 ENOENT）
- 添加容错机制：memory 文件不存在时跳过，不阻断流程
- 确保 Get笔记 API 始终被调用，不依赖 memory 文件状态
---

## v0.1.34 更新说明（2026-11-07 零输入日：输入量与产出量分账记账）
- **根因**：2026-11-06 Get笔记 新增 9 条记录**全部是系统自身产物，外部素材 0 条**，而当日仍产出 8 份文档。数据概览若只报「系统产出 8 份」，会被读成「高产的一天」——实际是系统在空转。**产出量与价值量首次彻底背离。**
- **修复一**：`references/briefing-template.md` 的「📊 今日数据概览」拆成**「输入侧（外部素材）」与「产出侧（系统产出）」两组固定列**，各带小计（N / M）；并规定 **N = 0 时标题级声明「今日无新素材」并自动降级为「消化回看专刊」**。
- **修复二**：确立判据——**每一份产出必须能指认它对应哪一条新输入；指认不出来的，归「结构归档区」，不占用检索面**。
- **修复三**：**不再新增检查项**（已有 5 个，全部作用在「产出之后」，拦不住零输入日）。**闸门前移到数据获取环节**：当日外部素材 = 0 时，先声明再产出。
- **沉淀的经验**：**「自产 0 条」这个指标在 N = 0 时会失效**——不是"有素材没观点"，而是"连素材都没有"。此时产出量的任何增长都只是旧东西的再包装。

---

# KAPE — 知识自动沉淀引擎 v0.1.39

## v0.1.33 更新说明（2026-11-06 标签归并判定存档）
- **根因**：v0.1.32 交付的 12 组「待归并清单」中，**至少 3 组方向是错的**——`#深度` X `#深度思考课程`、`#过度诊断` X `#过度诊断与过度归档`、`#OpenAI` X `#OpenAI融资`。三者都是 0.90 子串关系，脚本逻辑上完全正确、语义上完全错误；其中 2 组已随简报发出，若按清单批量执行会毁掉 08-14 与 11-04 两条简报的语义，并让事件型标签污染检索入口（正好违反 v0.1.32 自己的规则）。
- **修复一**：新建 `日志管理/标签归并判定.json`——**唯一判定依据**。verdict 四态：`same`（语义等价应归并）/ `refine`（细化关系，两者都留，主标签统一）/ `distinct`（**不同概念，禁止合并**）/ `needs-human`（待人工）。键为 `A|B`，**不要求书写顺序**，脚本加载时自动归一化（按各段去 # 后字典序）。
- **修复二**：`tag_merge.py` 改为**主动读取判定文件**。`distinct` 的组不再出现在归并建议里，改列入「⛔ 已排除」区并附排除理由；`same`/`refine` 覆盖脚本相似度推荐的主/副标签方向。首测：12 组全部命中（应归并 5 / 细化 2 / 已排除 3 / 待人工 2）。
- **修复三**：`日志管理/规则-标签归并与收敛.md` 第四节重写为「人工判定清单」（应归并 / 细化 / 已排除 / 待人工 四表 + 3 组排除的重要意义），并同步 `overwrite` 飞书文档 `P61IdEG1qoDvpWx9nyGc6EgDnAh`（旧版错误清单已被覆盖，回读校验 LEN=8773、无旧错误方向）。
- **沉淀的经验**：**相似度高 ≠ 语义相同，这句话反过来也成立——脚本会错，人也会错，但必须留痕。** 所以判定结论要落盘成文件，而不是每次重新推断；`distinct` 是**永久排除**，避免同一个错误方向被反复推荐。
- **仍然禁止批量自动归并**：脚本只负责把候选推到眼前，最终判断必须逐条做。
- **操作坑**：`lark-cli docs +update` **不支持 `--yes`**（会报 `validation: invalid_argument`），且整篇替换必须用 `--command overwrite`（`str_replace` 不支持整篇替换），内容用 `--content @file.xml`。

## v0.1.32 更新说明（2026-11-06 标签归并/收敛规则）
- **根因**：`reuse_counter.py` 首测显示 183 篇归档 / 512 去重标签中 **490 个仅出现一次（95.7%）**，复用率仅 **4.3%**（≥3 次的仅 2 个：#AI落地 5 次、#Anthropic 3 次）。**「自产 0 条」说的是输入端没东西；复用率 4.3% 说的是产出端——根因不是记性差，是归档机制缺少收敛机制**：每天生成新标签，无任何机制把新标签归并到已有概念上。
- **修复一**：新建 `日志管理/tag_merge.py`（近义检测器）。判据：=1.00 同名 / ≥0.90 子串细化 / ≥0.62 bigram Jaccard 弱相似。**相似度高 ≠ 语义相同，脚本只负责把候选推到眼前，最终判定必须逐条做**。首跑识别 12 组强候选。
- **修复二**：新建 `日志管理/规则-标签归并与收敛.md` —— 核心规则「**新标签必须先回答：这和已有的哪个概念是同一个？答不上来，才允许新开**」，并区分**概念型标签**（可做检索入口）与**事件型标签**（一次性事件，不占检索面；判断标准：三个月后还可能再出现吗）。
- **修复三**：**Step 3 生成关键词前强制执行自查** `python3 日志管理/tag_merge.py --new "#标签"`；Step 5 归档后每周全量复测 `tag_merge.py` + `reuse_counter.py`。
- **为什么不继续加检查项**：检查项已有 5 个（技能自审 / AI量级自检 / AI边界与验收 / 过度诊断与过度归档 / 框架vs介质），收益在明显衰减。**缺的不是更多检查，是一条收敛规则。**
- **目标**：复用率 4.3% → 12 月底 ≥15%；每周新开概念型标签 ≤8 个；事件型标签占比 ≤40%。

## v0.1.31 更新说明（2026-11-06 三栏固化 + wiki 节点去重）
- **根因一（模板缺栏位）**：11-04 简报的「跨素材等式」「落到我身上的行动项」「已回读校验」三条建议此前只是文字，模板里没有对应栏位，所以每天的简报照旧不写。
- **修复一**：`references/briefing-template.md` 新增 4 个**固定栏位**——「🩺 过度诊断 ↔ 过度归档自检」「📎 跨素材等式」「🎯 落到我身上的行动项」「✅ 已回读校验」（末尾固定行）；并新建 `日志管理/检查项-过度诊断与过度归档.md` 作为该栏位的执行依据。台账第 13/14/17 条随之转 ✅。
- **根因二（wiki 节点重复）**：Step 5② 的 `wiki +node-create` 被执行两次（一次取 URL、一次取 obj_token），**每次都会真的建一个节点**，导致同名节点重复。本地在 `日志管理/` 下用标题做查重是查不出来的——飞书知识库里也会多出一份。
- **修复二**：`wiki +node-create` 的输出**一次就同时给 `node_token` 与 `obj_token`**，不要为了取另一个 token 再跑一次；创建后用 `wiki +node-list --parent-node-token ... --page-all --page-limit 30` 按标题计数确认唯一（单页 `node-list` 默认只取一页，会漏检）；若已重复，删多余的那个——注意 `wiki +node-delete` **必须带 `--obj-type`**（`wiki`/`docx`/…），否则报 `validation: invalid_argument`。
- **验证**：2026-11-05 简报三端同步完成，知识库下 11-05 节点计数 = 1；Get笔记 1926209521703903216；知识库 wiki QKTIwfanxiA0wLk0DyxcJCkOnXe / docx OXttdVV5ooFvCwxII2Zc8SzTnFe；共享文件夹 docx XO6adyxdwo3Hh5x4ifacISOqn4g；两份文档 `docs +fetch` 回读 LEN=19277 且首尾完整、`warnings=[]`。

## v0.1.30 更新说明（2026-11-05 待办回看闭环 + 断档哨兵）
- **根因一（悬置 5 天）**：10-31 首提「固定加一节前期待办回看」，至 11-05 仍未落地；11-02 / 11-03 简报的「明日关注」里连续两天写着「需补上回看动作」却依然没做。**建议写进简报不等于被采纳**——所以它必须成为模板的强制结构（第 0 节），而不是每日的自觉动作。
- **修复一**：`references/briefing-template.md` 新增「🔁 前期待办回看（第 0 节，必须最先执行）」，含四状态判定表（✅已落地 / 🔄进行中 / ⛔已放弃 / ⏸️待你决定）、证据要求、连续 3 次未决自动升级为「当面提出」、以及「本节新增待办」回流字段。
- **根因二（检查本身不可靠）**：11-02、11-03 连续两天 cron 缺跑，而「归档连续性检查」只在 KAPE **运行时刻**触发——KAPE 不跑，检查也不跑。检查若与被检查对象同生共死，就不是防线。
- **修复二**：新建独立 automation「日志归档自检（断档哨兵）」`51d8b116-e681-4801-9763-3edabc1160cb`，cron `20 9 * * *` Asia/Shanghai（与 KAPE 07:45 错开 95 分钟），isolated session，1800s 超时，announce → feishu 群 `oc_385ea2cb3bd04d657126af9190d5bb35`。缺档则补做并通知，无缺档则绝对静默（哨兵的价值在于安静）。

## v0.1.29 更新说明（2026-11-02 分页解析与 shell 兼容性修复）
- **根因 1**：`json.load(sys.stdin, strict=False)` 只能容忍裸控制字符，**无法修复非法反斜杠转义**（笔记正文里一个孤立的 `\` 即触发 `Invalid \escape: line N column M`），翻页到第 4 页时解析直接失败。
- **根因 2**：停止条件 `[ "$EARLIEST_DATE" "<" "$TARGET_DATE" ]` 在 **zsh** 下报 `condition expected: <`（zsh 对 `<` 的解析与 bash 不同），导致提前停止条件失效、无谓多翻页。
- **修复**：新增 `日志管理/fetch_notes.py`（稳健解析器：先原样 `json.loads(strict=False)`，失败则做「非法反斜杠加倍」修复后重试）；SKILL.md 中所有分页循环改用该脚本；停止条件改用 `[[ ... < ... ]]`（zsh/bash 通用）。
- **验证**：2026-11-01 简报抓取到当日 3 条笔记（其中 1 条为自身产物，剩 2 条有效），三端同步 + 回读校验全部通过。

## v0.1.28 更新说明（2026-11-01 DocxXML 标签白名单修复）
- **根因**：飞书 DocxXML 中 `<heading>` / `<quote>` / `<code_block>` 均为不支持的标签，会触发 `degrade_code=4010` 并被剥除（此前只记录了 `<ol seq="auto">` 的告警，标签白名单不完整）。
- **修复**：Step 5 新增完整 DocxXML 标签白名单表；要求 `docs +create` 必须含 `<title>`（否则显示 Untitled）；新增 `日志管理/md2docx.py` 转换器（Markdown → DocxXML）。
- **验证**：2026-10-31 简报两份飞书文档写入 `result: success`，`warnings: []`，回读校验内容完整。

## v0.1.27 更新说明（2026-10-30 Bug 修复）
- **根因**：`getnote notes --output json` 的输出含裸控制字符，`json.load(sys.stdin)` 严格模式报 "Invalid control character: line 10 column 43"，导致按日期筛选笔记的循环直接中断。
- **修复**：SKILL.md 中所有 `json.load(sys.stdin)` 统一改为 `json.load(sys.stdin, strict=False)`。
- **验证**：2026-10-29 简报正常抓取到 4 条当日笔记（其中 2 条为有效素材），三端同步完成。

## v0.1.38 更新说明（2026-11-08 心跳：重复节点定档依据的算术更正）
- **触发**：本轮心跳复核 11-07 简报时，顺带核「重复节点清理」这条**待张公子定档**的依据，发现诊断报告 `日志管理/诊断报告-飞书知识库重复节点.md` 的指标表**层级错位**。
- **错在哪**：表里写「多余副本总数 **15** = 5 个空壳 + **21** 个不同版本」——`5 + 21 = 26`，而 **26 是「组内副本总数」，不是「多余副本 15」的拆分**。两级口径被混进了同一张表。
- **实测复核**（逐份 `docs +fetch` 取 LEN，26 份全测）：重复组 **11** ｜ 组内副本 **26** ｜ 多余副本 **15** ｜ 空壳(LEN=36) **5** ｜ 有内容的历史版本 **10**。
  - 核对路径：每组保留 1 份 → 11 组留 11 份 → 26 − 11 = **15**；空壳 5 份；15 − 5 = **10**。
- **为什么必须修**：档一/档二/档三的差别**恰好就在这 10 份上**——「5 个空壳零损失」是档一的依据（不受影响），但**档二要删的正是那 10 份有内容的历史版本**。把 21 写进「多余副本」会让档一的「零损失」看起来只覆盖 15 份中的 5 份，**结论会读反**。
- **已修**：诊断报告指标表重写（新增「组内副本总数」行、把两行「其中」改为 `├`/`└` 层级）+ 加算术更正说明段；台账第 22 条同步更正；两端（飞书 docx `IFcCdABaMoz1h9xoWGOclTsznhf` / Get笔记 `1926211026014736992`）已同步并回读。**另修正**：表内「子节点总数 205」→ 实测 **207**（新增为 11-06 / 11-07 两篇正常简报，**不影响重复判定**）。
- **沉淀的经验**：
  1. **表格里的「其中」行必须与父行算术自洽**——父行是子集时，子项之和 = 父项；不等就是层级错位，一眼扫过去极难发现。
  2. **把诊断结论交给人裁定时，被裁定的数字本身必须先复核**——定档三选一完全建立在「空壳 vs 有内容」的拆分上，拆分错了，选项的**代价**就错了。
  3. **口径（层级）比数值更容易错，且错得极其安静**——既不报错也不崩，数字各自看着都合理。这与 v0.1.37 的「宽松解析口径比错误数据更危险」同族。
- **同日另修**：`~/self-improving/heartbeat-state.md` 的 `last_reviewed_change_at` 上一轮被写成**未来时间戳**（08:22 > 当时实际 08:16）——心跳靠「mtime > 基线」判断有无变更，未来时间戳会让该比较**恒失效**、之后所有真实变更都被忽略。已修正，并写入 `~/self-improving/memory.md`（30 行）与 `~/proactivity/session-state.md`（教训第 12 条）。

---

## v0.1.37 更新说明（2026-11-08 复用度量三 bug：宽松正则 / --since 静默截断 / 同篇重复）

> 触发：2026-11-08 心跳**独立复核** 11-07 简报发布的「存量复用盘点」结论，发现**发布的数字与脚本实跑结果对不上**。经排查是**三个度量 bug 叠加**，且互相掩盖。

- **Bug 1｜`reuse_audit.py` 宽松正则把说明段当数据**
  - 原实现用 `##\s*🔑\s*关键词(.*?)(?=\n##\s|\Z)` 扫整节，把**该节下「标签收敛自查」说明段落里提到的 # 标签也当成标签实例**。实测：11-06 真实 **10** 个被数成 **26** 个、11-07 真实 **14** 个被数成 **34** 个。
  - **并直接造出假复用**：`#过度诊断`（11-04→11-06）被判为「复用」，但 11-06 的**真实关键词行里根本没有它**——它只出现在 11-06 的说明段里。**尤其讽刺**：`#过度诊断` 与 `#过度诊断与过度归档` 恰恰是 11-06 声明 ⛔ distinct（禁止合并）的一对，照旧数字执行归并会**把当天刚定下的结论自己推翻**。
- **Bug 2｜`reuse_counter.py --since` 静默截断**
  - 原实现用 `basename[:7]`（只到 `YYYY-MM`）与 `since` 比较。传完整日期 `--since 2026-10-25` 时 `'2026-10' >= '2026-10-25'` 为假 → **静默只返回部分文件、不报错、不提示**，数字全错却毫无迹象。
- **Bug 3｜`reuse_counter.py` 同篇重复计为复用**
  - 直接 `tags[t] += 1` 数**出现次数**，而其文档写明口径是「出现在 **≥2 篇不同简报** 里」。实测 2026-11-01 关键词行里 `#三不腐` 写了两次 → 被误判为「复用的概念」。

- **修复一**：`reuse_audit.py` 改用与 `reuse_counter.py` **完全相同**的 `TAG_RE`（只取「🔑 关键词」标题后**第一行**）。**两个度量脚本口径必须严格一致**——否则「两个口径互相印证」就是空话。
- **修复二**：`reuse_counter.py --since` 改为**按输入精度比较**（`YYYY-MM-DD` 按日比、`YYYY-MM` 按月比），两种写法都正确工作。
- **修复三**：`reuse_counter.py` 改为**同篇内重复标签只计一次**，并新增 `tag_days` 集合按「不同简报数」判定，与文档口径对齐。

- **修复后的权威数字**（14 篇窗口 10-25~11-07，**两脚本现已真正互证**）：

  | 脚本 | 标签实例 | 去重 | ≥2次 / 前向复用 | 复用率 |
  |------|---------|------|---------------|--------|
  | `reuse_audit.py`（前向口径） | 134 | — | 3 | **2.2%** |
  | `reuse_counter.py --since 2026-10-25` | 134 | 131 | 3 | **2.3%** |

  旧值 **123 / 5 / 118 / 4.1%** 是 **13 篇窗口**（10-25~11-06）的数却写成 14 篇；且「4.1% 与 4.8% 几乎一致、互相印证」**是假的**——两者窗口与定义都不同。

- **11-07 简报已更正并四端同步**：本地 + 飞书知识库 docx `EpofdKs8AoFxygxVs2RcpTzQnUg` + 共享 docx `KN8Jd4Z25oQtQRxb8m0cHkNZnfe`（**两份回读逐字相等**，故不自记具体字符数——写入即改变）+ Get笔记 `1926395570021742176`；简报内新增「度量口径更正」小节记录三个 bug 与权威数字
- **沉淀的经验**：
  1. **宽松的解析口径比错误的数据更危险**——它不报错、不崩溃，只是安静地把说明段当成数据。
  2. **指标一旦被用来支撑结论，口径就必须和参照脚本严格对齐，且两个脚本要能真的互证**；不能像原报告那样声称「几乎一致」却连窗口都没对齐。
  3. **v0.1.35 的教训在度量脚本上再次应验**：「凡是按字面执行就会做错事的规则，必须写成不可能被误读的代码」——但这次的错误不在「规则写得含糊」，而在「**解析写得宽松**」。
  4. **独立复核时不要只核对结论，要核对它引用的那个脚本的实跑输出**——本次正是靠实跑才发现三个 bug；只看报告里的数字是发现不了的。

---

## v0.1.36 更新说明（2026-11-07 素材回归日：Q2 措辞修正 + 存量复用盘点脚本）

> 背景：2026-11-07 是连续 6 天零输入后的**第一条外部素材**（EA / 有效利他主义剪藏），同时是「自产 0 条」**连续第 7 天**——恰好命中 `检查项-过度诊断与过度归档.md` 的 Q2 判据。**Q2 建立于 11-06，11-07 是它第一次到期**，于是立刻暴露了自己的措辞缺陷。

- **根因一（Q2 措辞缺陷）**：Q2 原文写「7 天+ → **停止日更简报**，先做一次存量素材复用盘点」。它把两件事混成一件——**想叫停的是「增量」，不是「产出」**。实测：Q2 触发日恰好素材恢复，按字面执行会在**最该盘点的时候要求停产**；而若当天仍是零输入，停产又确实无新东西可写。
  - **修复**：`检查项-过度诊断与过度归档.md` Q2 改为「**当日产出降级为「存量盘点专刊」**——不停产，但重心从「新增」转为「盘点」」，并附「v0.1.36 措辞修正」说明段。
  - **沉淀的经验**：**规则写成「按字面执行就会做错事」的形态时，必须改成不可能被误读的措辞。** 这与 v0.1.35 的连续性检查 bug 同类——**两处缺陷都在「规则被首次真实触发」时才显形**，说明它们不是偶发，而是设计缺陷。

- **根因二（复用率口径不可靠）**：`reuse_counter.py` 测的是「标签出现次数」，无法区分「**前向复用**」（被更晚的简报再引用）与「**同日镜像**」（同一天在多个平台出现）。后者不是复用，是同步。
  - **修复**：新增 `日志管理/reuse_audit.py`——**前向复用口径**：同一标签在**更晚的**简报里再次出现才算复用。输出落盘 `reuse_audit.json`。
  - **首测**（最近 14 篇）：标签实例 123 / 前向被复用 **5** / 从未再引用 118 / **前向复用率 4.1%**（与 `reuse_counter.py` 的 4.8% 互相印证 → 低复用是结构性的，不是统计误差）。
  - **附带发现**：**5 个真正沉淀的概念全部发生在 11-06 一天**——复用发生在**消化端**，不发生在生产端。

- **新增判据（度量换维度）**：**最锋利的度量不是复用率，是「反事实影响」**。复用率是代理指标，可以被优化行为腐蚀（11-06 标签归并 12 组错 3 组 = 指标腐蚀的预演）；「如果我不在，这会怎样」无法被伪造。

- **本日的标签决策**：新增 14 个候选标签逐条跑 `tag_merge.py --new`，12 组返回「无近义候选」（真新概念）；**`#AI安全`、`#Anthropic` 复用已有标签不新开**；**未开 `#EA`**（与 `#有效利他主义` 同义，只留全称作检索入口）。

- **验证**：2026-11-07 简报三端同步 + 回读全部通过（本地 33,144B / 飞书知识库 docx EpofdKs8AoFxygxVs2RcpTzQnUg LEN=25,467 / 共享文件夹 docx KN8Jd4Z25oQtQRxb8m0cHkNZnfe LEN=25,467 / Get笔记 1926395570021742176）；附带落地 `决策清单-EA四问.md`（Get笔记 1926395582907297344 / 飞书 IkMGdsHthoKnE4xABxFcs5R5n1c）；台账新增第 25 / 26 条并四端同步。

---

---

## v0.1.39 更新说明（2026-11-09 重复节点复发巡检固化）
- **触发**：2026-11-08 一次性清理了飞书知识库「日志简报」下的 15 个重复节点（5 个空壳 + 10 个有内容的历史版本，节点总数 207 → 192，重复组 11 → 0），**但产生重复的路径本身没有变**——同一父节点下同名节点被创建两次。
- **修复**：Step 5② 的「wiki 节点去重」小节升级为**强制四步巡检**——① `wiki +node-create` 只调用一次（一次返回 `node_token` 与 `obj_token`）；② 创建后立即 `wiki +node-list --page-all --page-limit 30` 按标题计数；③ **计数 > 1 即为复发**，按 `wiki +node-delete --node-token <多余> --obj-type wiki --yes` 清理；④ 再次枚举复核计数 = 1。
- **为什么第④步不可省**：`wiki +node-delete` 的 **stdout 只输出版本升级提示**，看不出成功与否——**唯一可信判据是重新枚举后的计数**。2026-11-08 的删除之所以能确认生效，靠的正是「207 → 202 → 192」这三次重新枚举，而不是命令返回成功。
- **配套**：台账新增第 28 条（巡检已落地）/ 第 29 条（主体性 → 口径核对，🔄 进行中）/ 第 30 条（「26 个环节能否变三五个」，⏸️ 待张公子决定）；诊断报告新增「七、复发预防」节。
- **沉淀的经验**：**存量清理是一次性动作，复发巡检才是防线**——只清不清，等于给同一 bug 续期。

---

## 安全说明

本 skill 需要以下工具权限：
- `exec`：调用 getnote CLI 获取笔记数据（只读操作）
- `feishu_wiki`、`feishu_doc`：写入飞书文档
- `sessions_list`、`sessions_history`：读取对话记录

**不会执行任何本地文件写入之外的 shell 命令**，所有外部 API 调用均为只读请求。

**重要**：禁止直接调用 `https://openapi.biji.com/...` HTTPS API（会返回 `10004 未授权`），必须使用 `getnote` CLI。

## 凭证配置

> ⚠️ **v0.1.23 简化**：`getnote` CLI v1.6.0 自动从 `~/.getnote/config.json` 读取凭证，无需手动配置或注入。

飞书 appSecret → `secrets.json` 的 `channels.feishu.accounts.main.appSecret`

飞书机器人需已加入知识库成员，否则 `feishu_wiki(spaces)` 返回空。

## 运行时凭证读取

> ⚠️ **v0.1.23 简化**：新版 OpenClaw 使用 SecretRef 存储凭证，手动解析 `openclaw.json`/`secrets.json` 会读到 `***` 而非真实 key。`getnote` CLI v1.6.0 会自动从 `~/.getnote/config.json` 读取凭证，**无需手动注入 key**，只需验证认证状态即可。

```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/bin/getnote"

# 验证凭证：getnote CLI 自动读 ~/.getnote/config.json，无需手动注入
${GETNOTE_CLI} auth status
```

---

## 共享文件夹配置

飞书文档统一存放在共享文件夹「牛管家日志」，确保张公子有删除权限。

| 配置项 | 值 |
|--------|---|
| 文件夹名称 | 牛管家日志 |
| 文件夹 token | `FQfXfYBGGllxxydJ1SgcJZWqnpf` |
| 文件夹 URL | https://qcnu4qzh46f0.feishu.cn/drive/folder/FQfXfYBGGllxxydJ1SgcJZWqnpf |
| 张公子权限 | full_access（可删除文档） |

---

## 核心工作流

每天自动生成日志简报，三端同步归档。**每个平台每次只执行一次原子操作，不允许先创建空文档再单独写入。**

---

### 第一步：归档连续性检查（防断档，v0.1.26 新增，必须先执行）

> ⚠️ **背景**：2026-10-27 07:47 的 cron 无 run 记录，导致 2026-10-26 简报缺失，直到 10-29 才补做，中间隔了 3 天无人察觉。**知识归档不能断。**

**执行断档检测**
```bash
set +e  # find/grep 无匹配返回非 0，属正常行为
BRIEF_DIR="/Users/openclawer/.openclaw/workspace/日志管理"
TARGET_DATE="$(date -v-1d +%Y-%m-%d)"
echo "=== 最近 7 天简报连续性检查 ==="
for i in 1 2 3 4 5 6 7; do
  D="$(date -v-${i}d +%Y-%m-%d)"
  if [ -f "${BRIEF_DIR}/${D}-日志简报.md" ]; then
    echo "OK      ${D}"
  else
    echo "MISSING ${D}"
  fi
done
```

> ⚠️ **v0.1.35 修复：循环必须从 `i=1` 开始（昨天），不能从 `i=0` 开始（今天）。**
> 原写法 `for i in 0 1 2 3 4 5 6` 会把**今天**算进检查范围，而运行时刻（早上 07:45）今天的简报**必然还没生成**，
> 于是**每次运行都稳定产生一个假 MISSING（今天）**。而「处理规则」写的是「除昨天以外出现 MISSING → 补做该日期」，
> 照字面执行就会**去补做今天**，生成一份无来源材料的错简报。
> **实测（2026-11-07 08:0x）**：原写法输出 `MISSING 2026-11-07` + 6 个 OK，与简报头部写的「近 7 天仅 11-06 为 MISSING」不符；
> 改为 `for i in 1 2 3 4 5 6 7` 后输出全部 OK（11-01 ~ 11-07 窗口内 11-06 已存在）。
> 断档哨兵（automation `51d8b116-e681-4801-9763-3edabc1160cb`）一直用的是 `for i in 1 2 ... 10`，**起点本来就是对的**——只有 KAPE 这一处写错了。

**处理规则**
- 检查窗口 = **昨天往前 7 天**（`i=1..7`），**不含今天**
- 若输出中 `TARGET_DATE`（昨天）显示 `MISSING` → **正常情况，继续生成昨天简报**
- 若**除昨天以外**的日期出现 `MISSING` → **补做该日期**：把 `TARGET_DATE` 改为该缺失日期，完整重跑本 skill 流程（生成 → 三端同步），每个缺失日期单独跑一次
- 若所有日期都 `OK` → 直接继续正常流程
- ⚠️ 补做时简报头部的「整理时间」必须写**实际补做时间**，并在数据来源行注明「补做，原 cron 缺跑」
- ⚠️ **简报头部「归档连续性检查」这句话必须与实际命令输出一致**。正确表述应类似「近 7 天无缺失」或「缺失日期列表」，
  **不得写成「仅 X 为 MISSING」**——除非 X 确实是命令输出里的 MISSING 行。

- ⚠️ **v0.1.40 硬约束（2026-11-11 心跳）：凡简报写了「降级为存量盘点专刊」，正文必须真有盘点章节。**
  - **根因**：2026-11-10 简报在**头部**与**自检栏位**两处宣称「Q2 触发 → 降级为存量盘点专刊」，但**正文没有任何盘点章节**（11-07 有 2 处、11-09 有 2 处、11-10 为 0）。即**声明降级 ≠ 执行盘点**。这与 v0.1.35 的「头部表述必须与实际输出一致」同族，但那次是**数字不符**，这次是**动作缺席**——更隐蔽，因为通篇读下来看不出断点。
  - **判据（两条同时满足才算执行）**：① 正文存在**标题含「盘点」的章节**；② 该章节引用的数字与 `reuse_audit.py` / `reuse_counter.py` **实跑一致**（可复现）。
  - **动作**：Q2 触发日必须实跑两个脚本并把输出写进盘点章节：
    ```bash
    python3 日志管理/reuse_audit.py
    python3 日志管理/reuse_counter.py --since 2026-11-01
    ```
  - **工具层已修（v0.1.40）**：两个脚本的 `TAG_RE` 原只匹配「🔑 关键词」标题后**紧跟**的第一行，而 2026-11-10 在该标题下先放了一行「标签收敛自查」说明 → 正则失配 → **该篇 11 个标签被整篇漏计**（审计输出「标签 0」）。已改为**先定位小节、再取小节内第一行以 `#` 开头的行**（两脚本同步改，保持互证）。**验证**：用修好的脚本重算 2026-11-09 简报声称的窗口，得 144 / 4 / 2.9%，与其声称的 144 / 4 / 2.8% 一致 → 修复正确。
  - **度量口径**：复用率**必须剔除「盘点专刊日作为消费者」**后再报——盘点专刊的特征就是重印旧标签，60% 的复用事件是盘点行为自己刷出来的（11-10 实测：表面 6.1%，剔除后真实 **2.5%**）。否则每次盘点都会让指标好看一点。

- ⚠️ **v0.1.41 硬约束（2026-11-14 心跳）：复用率的「剔除盘点专刊日」必须由脚本内置，简报不得手工剔除。**
  - **根因（台账 #37）**：盘点专刊日会把既有标签重印一遍，于是「复用事件」被盘点行为自己刷出来。
    11-13 实测：表面 6.7%，剔除盘点专刊日消费者后真实 **2.2%**——**约六成的「复用」是盘点动作的副产品**。
    该剔除**连续 4 次（11-10 ~ 11-13）只在简报正文里手工做**，脚本始终没有这个开关——漏做一次数字就错一次，
    且手工剔除无法被第三方复现。**规则写在正文里 ≠ 规则被执行。**
  - **工具层已修（v0.1.41）**：`reuse_audit.py` 与 `reuse_counter.py` **同步**新增内置剔除：
    - 盘点专刊日判据（两脚本一致）：① 正文存在 markdown 标题且标题含「盘点」（如 `## 五、存量盘点（实跑，非声明）`）；
      ② 文档首行标题含「存量盘点专刊」。**只看标题行**，正文提及「盘点」是叙述，不算。
    - `reuse_audit.py` 新增输出：`前向被复用(剔除盘点日)` 与 `前向复用率(剔除盘点日 = 权威值)`；
      逐条明细中仅被盘点日重印的标签会标注 `← 仅被盘点专刊日重印，不计真实复用`。
    - `reuse_counter.py` 新增输出：`剔除后真复用标签数` / `表面复用标签数`，并在 JSON 里给出
      `tags_ge2_real` / `reuse_rate_pct_real` / `reused_real` / `inventory_days`。
  - **⚠️ 口径纪律（本次修复中踩到的坑，必须遵守）**：剔除逻辑**不得改写原始计数**。
    标签总数/去重数是「素材产出量」的原始度量；若被剔除逻辑改写，同一个脚本里两个指标的口径就混了
    （实测：改写后总数从 172 掉到 164，差额正好等于被降级的 8 个标签——数字看着像「素材少了 8 个」，其实是口径变了）。
    正确做法：**原始计数保持不变，另算一份「剔除盘点日消费者」后的真实复用集合**，两个数并排输出。
  - **权威数字口径**：对外只报**剔除后的真实复用率**，并同时给出表面值与被剔除的盘点日集合，三者一起出现。
  - **验收**：跑 `python3 日志管理/reuse_audit.py` 与 `python3 日志管理/reuse_counter.py --since <日期>`，
    输出里**必须出现**「剔除盘点日」相关行；否则视为未落地。

- ⚠️ **v0.1.42 硬约束（2026-11-15 心跳）：「已回读校验」必须**写出四端坐标本身**，不得用「见下方回读记录」代替。**
  - **根因（台账 #42）**：2026-11-14 简报的「✅ 已回读校验」写了两条
    `- Get笔记：见下方回读记录（…）` / `- 飞书知识库 docx / 飞书共享文件夹 docx：见下方回读记录（…）`，
    但**全文没有「回读记录」这个小节**，也**不含任何 doc / wiki token**（对照 11-13 含 3 个）。
    → **悬空引用**：文字声称「有回读证据」，实际没有，第三方无法定位四端。
  - **注意这不是模板问题**：`references/briefing-template.md` 的对应栏位**本来就有坐标占位符**
    （`{note id / 回查条目存在且标题正确}`、`{doc token / result=success / …}`），
    是**生成时把占位符替换成了「见下方回读记录」**——所以修文件没用，**必须修生成约束**。
  - **判据**：四端坐标（Get笔记 id、飞书知识库 doc token + wiki node token、飞书共享文件夹 doc token）
    必须**逐字出现在简报正文里**；不得出现「见下方回读记录」「详见后文」等**指向别处的占位说法**。
  - **动作**：生成「已回读校验」时，坐标**先从实际 API 返回里取**，再写进正文；不要凭记忆写，也不要留待补。
  - **自检（生成后必须跑）**：
    ```bash
    python3 日志管理/check_briefing_refs.py 日志管理/{date}-日志简报.md
    ```
    退出码非 0 = 简报存在悬空引用或缺坐标，**必须修完再归档**。
  - **验收**：脚本输出 `OK` 才算通过；仅靠肉眼看「已回读校验」这一节存在是不够的。
- ⚠️ **v0.1.43 硬约束（2026-11-19 心跳，台账 #54 落地）：复用度量必须报「剔除前 / 剔除后」两个数，且自引剔除已在脚本内置。**
  - **背景**：11-17 / 11-18 两篇简报正文都写了「本日引用了前几日标签，但属自我循环 → 不计」，
    但**两个脚本里都没有这个开关** → 权威值被自己刷高（11-18: 14）。
  - **已落地**：`reuse_audit.py` 与 `reuse_counter.py` **同步**新增第三个内置剔除维度
    （盘点日消费者 / **自我循环自引**），边界写死且**可计算**：
    消费者日 C 的「标签收敛」自查块里存在标签 T 的复用声明，且其**声明窗口**
    同时满足「含日期溯源」且「不含当日素材指称」→ 判为自我复述，不计入真实复用。
  - **互证已通过**：脚本算出的 11-17 自引集合 `{信息回声, 局部规则涌现, 身份认同, 少犯错原则}`
    与 11-17 **正文自己写的**「11-16 的 4 个标签」**逐个一致**；11-18 同理一致。
  - **写简报时的纪律（新增）**：
    ① 复用率**必须写清窗口起止日**（沿用 #45），且**必须同窗口对比**——
       11-18 的「8 → 14」对比**混了窗口滑动**（8 是 11-03~11-16 测的，14 是 11-04~11-17），
       「跳涨全部是自引」这个归因**不成立**；同窗口下 8→3（11-03~11-16）、14→9（11-04~11-17）。
    ② **不能只报一个数**：必须「表面 / 剔盘点日 / 再剔自引」三档并排。
    ③ **明细必须与脚本实跑一致**：11-18 正文的「14 个明细」与脚本实跑的 14 个**不是同一集合**
       （正文缺 `#指标腐蚀` 11-07→11-14、`#多智能体` 11-08/11-10→11-17，
       却多列了已标注「已剔除」的 11-12→11-13 两项）→ **明细要贴脚本输出，不要手写**。
- ⚠️ **v0.1.44 硬约束（2026-11-20 心跳，台账 #56 落地）：凡报复用率，**三档必须并排 + 每档必须给「偏移归因」**，禁止只报单档。**
  - **来源**：素材《柳叶剑·数字健康》的药品广告研究给出「**临床等效区**」概念 —— 几个选项都站得住时，一条广告成了打破平局的小砝码；且准确率反而从 89.4% 升到 93%，**可答案已被整体推移 12.7 个百分点**。研究者原话：「这些答案看起来都太合理了，常规 AI 评测极易漏掉。」
  - **直接映射**：复用率三档（表面 24 / 剔盘点日 17 / 再剔自引 9）里，**每一档的偏移都来自一个具体动作**（盘点日消费者 / 自我复述）。只报一个数 = 「只看对错、不看怎么得出的」。
  - **写简报时的纪律（新增）**：
    ① 凡报复用率，**三档并排**：`表面 N（x%）` → `剔盘点日 N（x%）` → `再剔自引 N（x%）= 权威值`，
       **每档后面必须写清这一档剔掉了什么、是谁的动作造成的**。
    ② **禁止只报单档**（哪怕只报权威值）—— 只报权威值同样违反本条，因为读者无法判断它是「多」还是「少」。
    ③ **分母必须写清**（沿用 #45 / v0.1.43）：分母 = 标签实例总数，并给出去重标签数作对照。
  - **11-20 实跑范式（可直接照抄）**：24（表面）→ 17（−7 = **盘点专刊日消费者**，盘点动作自己刷的）
    → 9（−8 = **自我复述**，引用方是本系统自己）→ 权威值 **9 / 148 = 6.1%**。
  - **同族**：v0.1.43「明细必须贴脚本输出」—— 同样是「别手写、贴实跑」；#45「同名指标必须自带定义」
    → 与本条并列为指标族的第 3 条形式要求。
- ⚠️ **v0.1.45 硬约束（2026-11-20 10:12，张公子明确）：**待办台账不再同步到 Get笔记 —— 只落「本地 md（唯一数据源）+ 飞书」。**
  - **原委**：待办台账此前是「四端同步」的一端（Get笔记 id + 飞书主档 + 本地）。张公子 10:12 明确：**「我的 Get笔记 里不需要待办事项」** → Get笔记 只保留**简报与素材**两类内容。
  - **已处置**：两篇台账笔记（主台账 1926211165601174112、历史存档 1927515425835337864）**已移入 Get笔记 回收站**；顺带清掉同日为排查长度上限而建的 **4 条「尺寸实验」测试笔记** —— **测试数据不留在用户的库里**。
  - **流程变更（此后不再做）**：
    ① **不要**再把 `日志管理/待办台账.md` / `待办台账-历史存档.md` 同步到 Get笔记；
    ② 简报「✅ 已回读校验」栏位里，**台账坐标改为写本地路径 + 飞书 doc token**，**不再写 Get笔记 id**；
    ③ 简报本体与素材**照旧**进 Get笔记（那才是他的知识库）。
  - **理由（不只是「他不喜欢」）**：Get笔记 的检索面是**他自己的知识库**，把**系统内部工作台账**塞进去会污染检索 —— 同族：11-06「标签归并方向错 3 组」、#53「指标没有闸门」，都是「往该放的地方塞了不该放的东西」。**待办的消费者是简报第 0 节与本系统，不是他的检索。**
  - **⚠️ 但简报的「已回读校验」仍要求写四端坐标** —— 那是**简报**的坐标（简报确实在 Get笔记），与「台账不进 Get笔记」不冲突，**别搞混**：**不删简报的 Get笔记 id，只删台账的。**
  - **同族教训（本次一并吸收）**：**盘点章节引用的数字必须能被第三方按简报声明的窗口复现。**
    11-13 简报写「178 实例 / 151（141 去重）」，其窗口是**生成时点**的 `10-30 ~ 11-12`
    （当时本地尚无 11-13 的 8 个标签）。独立复算用 `10-30 ~ 11-12` 得 178 / 151(141) **逐字相等** →
    简报数字**正确**，不是缺陷。但它**没声明窗口**，导致按默认窗口（最近 14 篇）复算得 172 而对不上，
    一度被误判为「数字造假」。→ **硬约束：盘点章节的每个表必须写出窗口起止日**（如「14 篇（2026-10-30 ~ 2026-11-12）」），
    否则第三方无法复现，数字再对也会被当成错。
  - **教训**：**规则里的「必须」如果没有对应的可检查动作，就只是愿望。** 凡写「必须执行 X」，必须同时写下「怎么验证 X 做了」——否则同族缺陷会在下个真实周期复发（11-08 数字不符 → 11-10 动作缺席，间隔 2 天）。

> ℹ️ 补做顺序：按日期从早到晚，避免连续多天缺失时顺序颠倒。

---

### 第零步：Get笔记 凭证读取与授权检查

> ⚠️ **v0.1.23 简化**：`getnote` CLI v1.6.0 自动读 `~/.getnote/config.json`，isolated session 无需手动注入 key。

**第一步：验证认证状态**
```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/bin/getnote"

# getnote CLI 自动从 ~/.getnote/config.json 读凭证，无需手动注入
${GETNOTE_CLI} auth status
```

**第二步：根据认证状态决定操作**
- 若返回 `Not authenticated`：
  ```bash
  # 使用 device code 流登录（无需 key，会打开浏览器）
  ${GETNOTE_CLI} auth login
  ```
  等待 `Logged in successfully.` 确认后再继续。
- 若返回 `Authenticated`：直接继续，不做任何操作。

---
- **目标日期**：昨天
- **获取方式**：
  1. 使用 `date` 命令获取当前日期：`date +%Y-%m-%d`
  2. 用 `date` 命令计算昨天的日期：`date -v-1d +%Y-%m-%d`
  3. 用 `date` 命令验证星期：`date -jf "%Y-%m-%d" "<目标日期>" +%A`
- **输出要求**：在生成简报前，先输出 `目标日期：YYYY-MM-DD（周X）`，并用 `date` 命令确认
- **日期格式**：`YYYY-MM-DD`（用于字符串前缀匹配）

---

### 第二步：获取数据（并行）

#### Get笔记读取

> ⚠️ **重要**：Get笔记 API 必须通过 `getnote` CLI 调用，**禁止**直接调用 `https://openapi.biji.com/...`（会返回 `10004 未授权`）。
> ⚠️ **grep 假阳性防护**：在任何 exec 命令链中执行 `grep` 过滤操作前，**必须**先用 `set +e` 包裹整条命令链，防止 grep exit 1 触发 set -e 导致整个 run 中断。示例：
> ```bash
> set +e  # 必须：grep 0 结果 = exit 1，set -e 会误判为失败
> # 你的 grep 命令...
> set -e
> ```
> grep 匹配到 0 行时返回 exit code 1 是**正常行为**，不代表命令失败。

**读取步骤：**

1. **设置 CLI 路径**（`getnote` CLI v1.6.0 自动读 `~/.getnote/config.json`，无需手动注入凭证）：
   ```bash
   GETNOTE_CLI="/Users/openclawer/.npm-global/bin/getnote"
   # getnote CLI 自动读 ~/.getnote/config.json
   ```

2. **检查认证状态**（如未认证则用 device code 流登录）：
   ```bash
   ${GETNOTE_CLI} auth status
   ```
   - 若返回 `Not authenticated`：
     ```bash
     ${GETNOTE_CLI} auth login  # device code 流，无需 key
     ```
   - 若返回 `Authenticated`：直接继续
   - 若返回 `Authenticated`：直接继续

3. **读取并过滤目标日期笔记（必须完成全部分页读取）**：
   ```bash
   # ⚠️ CLI 输出格式：JSON（data.notes 数组），字段名是 created_at 不是 created
   # ⚠️ 过滤方式：用 python3 解析 JSON，按 created_at 字段筛选目标日期笔记
   # ❌ 禁止使用 grep —— CLI 输出是 JSON 不是纯文本
   # ⚠️ getnote notes --cursor 接受的是 API 返回的 next_cursor token（字符串），不是数字偏移量！
   # ⚠️ v0.1.29：改用稳健解析器 fetch_notes.py。
   # inline `json.load(sys.stdin, strict=False)` 无法修复非法反斜杠转义，
   # 笔记正文含孤立 `\` 时会报 Invalid \escape 并中断翻页循环。
   TARGET_DATE="2026-05-28"  # 昨日日期，格式 YYYY-MM-DD
   FETCHER="/Users/openclawer/.openclaw/workspace/日志管理/fetch_notes.py"
   CURSOR=""
   PAGE=0
   while true; do
     PAGE=$((PAGE+1))
     PAGE_FILE="/tmp/gn_page_${PAGE}.json"
     ${GETNOTE_CLI} notes --cursor "${CURSOR}" --limit 200 --output json > "${PAGE_FILE}" 2>&1
     # 解析并输出目标日期笔记 + 元数据（已修复非法转义）
     python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}"
     # 提取元数据（同样用稳健解析器）
     HAS_MORE=$(python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}" 2>/dev/null | awk -F': ' '/^HAS_MORE:/{print $2; exit}')
     EARLIEST_DATE=$(python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}" 2>/dev/null | awk -F': ' '/^EARLIEST:/{print $2; exit}')
     # ⚠️ 用 [[ ]] 而非 [ ]：zsh 下 [ "a" "<" "b" ] 会报 condition expected: <
     if [[ -n "$EARLIEST_DATE" && "$EARLIEST_DATE" < "$TARGET_DATE" ]]; then
       echo "=== 最旧笔记 $EARLIEST_DATE 早于目标日期 $TARGET_DATE，停止翻页 ==="
       break
     fi
     if [[ "$HAS_MORE" != "True" ]]; then
       break
     fi
     CURSOR=$(python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}" 2>/dev/null | awk -F': ' '/^NEXT_CURSOR:/{print $2; exit}')
     if [[ -z "$CURSOR" ]]; then
       echo "警告：has_more=True 但 next_cursor 为空，停止翻页"
       break
     fi
   done
   ```


4. **分页读取（防止遗漏）**：当笔记数超过 200 条时，用 `next_cursor` token 继续翻页，循环直至 `has_more=false`。**必须用 python3 解析 JSON 过滤日期**，禁止用 grep：
   ```bash
   # getnote notes --cursor 接受的是 API 返回的游标 token（字符串），不是数字偏移量！
   # ❌ 错误示例：--cursor 0 / --cursor 200 / --cursor PAGE*200（这些都是数字，会翻到错误位置）
   # ✅ 正确方式：用 API 返回的 next_cursor token
   # ⚠️ v0.1.29：解析一律走稳健解析器 fetch_notes.py（能修复非法反斜杠转义）；
   #    停止条件一律用 [[ ]]（zsh 下 [ "a" "<" "b" ] 会报 condition expected: <）。
   #    完整循环见上文第 3 步，本段为同一实现的最小可复制版本。
   TARGET_DATE="2026-05-28"  # 昨日日期，格式 YYYY-MM-DD
   FETCHER="/Users/openclawer/.openclaw/workspace/日志管理/fetch_notes.py"
   CURSOR=""
   PAGE=0
   while true; do
     PAGE=$((PAGE+1))
     PAGE_FILE="/tmp/gn_page_${PAGE}.json"
     ${GETNOTE_CLI} notes --cursor "${CURSOR}" --limit 200 --output json > "${PAGE_FILE}" 2>&1
     python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}"
     HAS_MORE=$(python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}" 2>/dev/null | awk -F': ' '/^HAS_MORE:/{print $2; exit}')
     EARLIEST_DATE=$(python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}" 2>/dev/null | awk -F': ' '/^EARLIEST:/{print $2; exit}')
     if [[ -n "$EARLIEST_DATE" && "$EARLIEST_DATE" < "$TARGET_DATE" ]]; then
       echo "=== 最旧笔记 $EARLIEST_DATE 早于目标日期 $TARGET_DATE，停止翻页 ==="
       break
     fi
     if [[ "$HAS_MORE" != "True" ]]; then
       break
     fi
     CURSOR=$(python3 "${FETCHER}" "${TARGET_DATE}" "${PAGE_FILE}" 2>/dev/null | awk -F': ' '/^NEXT_CURSOR:/{print $2; exit}')
     if [[ -z "$CURSOR" ]]; then
       echo "警告：has_more=True 但 next_cursor 为空，停止翻页"
       break
     fi
   done
   ```

5. **获取单条笔记详情**：
   ```bash
   ${GETNOTE_CLI} note <note_id> --field content  # 获取正文
   ${GETNOTE_CLI} note <note_id> --field title   # 获取标题
   ```

#### 对话记录获取

1. 用 `sessions_list` 获取所有 session（设置足够的 `activeMinutes` 覆盖目标日期）
2. 判断 session 在目标日期有活动的条件：`updatedAt` >= 目标日期开始时间 AND `updatedAt` < 今日开始时间
3. 用 `sessions_history` 读取符合条件的 session 内容（`includeTools=false`）
4. 解析用户消息（`role: user`）作为对话记录

#### 词汇存档（若有）

- **容错读取**：用 `exec` + `cat` 读取 `workspace/vocabulary/{target_date}.md`，若文件不存在或读取失败则跳过，不阻断流程
- 统计当日新增单词数量（如有）

> ⚠️ **路径处理规范**：所有从 `memory_search` 或 `sessions_list` 等工具返回的路径，返回格式可能为 Markdown 链接（如 `[2026-04-05.md](http://...`）或纯路径。传给 `read` 工具前，**必须先去除 Markdown 链接格式**，只提取纯路径部分。

---

### 第三步：深度分析与整理

> ⚠️ **内容过滤规则（v0.1.6 新增，必须执行）**
> 整理前需剔除【科技新闻日报】自动生成的内容：
> - **排除文件**：`memory/YYYY-MM-DD-tech-news.md`
> - **排除文档**：飞书文档标题含「科技新闻日报」或「科技新闻热榜」
> - **排除笔记**：Get笔记标签或来源为「科技新闻日报」相关条目
> - **仅保留**张公子个人学习、播客、录音、网页剪藏、手动笔记等主动获取内容

**生成日志简报结构**（见 `references/briefing-template.md`）

> ⚠️ **v0.1.30 强制结构**：简报必须包含「🔁 前期待办回看」第 0 节，且必须先于「🗺️ 主题关联图」。该节内容来自最近 3 天简报的「明日关注」与「改进建议」，逐条判定状态并附证据。**跳过本节 = 简报不合格**，即使素材充足、洞察深刻。

> ⚠️ **强制完整输出规则（v0.1.7 新增）**：无论输入数据多少，哪怕只有1条笔记，也必须生成完整模板的所有区块。简报不是摘要，是完整的结构化记录。

> ⚠️ **v0.1.32 标签收敛规则（必须执行，写关键词前先做）**
> 背景：复用率实测仅 **4.3%**（512 个去重标签中 490 个只出现过一次）。根因不是记性差，是**没有收敛机制**——每天都在开新标签，没人把它们归并回已有概念。
> **规则：新标签必须先回答「这和已有的哪个概念是同一个？」，答不上来才允许新开。**
>
> ```bash
> cd ~/.openclaw/workspace/日志管理
> python3 tag_merge.py --new "#你要用的标签"   # 逐个自查
> ```
> 三种处置：
> - 语义等价 → **复用已有标签，不新开**
> - 新标签是已有标签的细化 → 两者都留，主标签指向细分
> - 确为不同概念 → 才新开
>
> 另外先分清**概念型标签**（可做检索入口，如 `#泛函`）与**事件型标签**（一次性事件，如 `#WAIC`，**不占检索面**）。判断标准：**三个月后还可能再出现吗？**
> 详见 `日志管理/规则-标签归并与收敛.md`。

**生成主题关联图（v0.1.5 新增）：**
根据当日笔记和对话记录，自动提取3-5个核心主题，标注主题间的关联关系。

**关联类型标签：**
- `→` 因果关系（A导致B）
- `⟶` 支撑关系（A证实/支持B）
- `⇄` 竞争关系（A与B竞争）
- `↙` 衍生关系（A衍生出B）

**飞书文档中使用列表格式替代 ASCII 图形。**

---

### 第四步：写入本地文件

**必须先确保目录存在**：
```bash
mkdir -p /Users/openclawer/.openclaw/workspace/日志管理
```

**文件路径**：`/Users/openclawer/.openclaw/workspace/日志管理/{target_date}-日志简报.md`

---

### 第五步：三端同步归档（一次性操作到位）

> ⚠️ **核心原则**：每个平台每次只执行一次原子操作。不允许先创建空文档/空笔记，再单独写入内容的分步操作。如果写入失败，**先删除已创建的半成品**，再重新执行完整的原子操作。

**CLI 路径常量**（所有 `lark-cli` 命令必须使用完整路径）：
```bash
LARK_CLI="/Users/openclawer/.npm-global/bin/lark-cli"
```

---

#### ① Get笔记（使用 `getnote save` 原子操作）

```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/bin/getnote"

# v0.1.23：getnote CLI v1.6.0 自动读 ~/.getnote/config.json，无需手动注入凭证
# ⚠️ 重要：内容必须从 Step 4 生成的本地简报文件读取，禁止传入字面字符串
set +e  # 文件内容含特殊字符时 set -e 会导致 exit 非 0，用 set +e 防止误中断
BRIEFING_FILE="/Users/openclawer/.openclaw/workspace/日志管理/{target_date}-日志简报.md"
${GETNOTE_CLI} save "$(cat "${BRIEFING_FILE}")" \
  --title "日志简报 {target_date} | 张公子" \
  --tag AI整理 \
  --tag 日志简报
set -e
```

> ⚠️ **禁止**直接调用 `https://openapi.biji.com/...` HTTPS API，必须使用 `getnote save` CLI。

---

#### ② 飞书知识库（先创建节点 → 再写入内容，两步都是原子的）

> ⚠️ **节点层级结构**：
> - 个人知识库（space_id: `7621391289904516315`）
> - `日志简报` 节点（node_token: `SERDwHBAniUqqBkx5vNctvgKn6f`）
> - **每日日志简报文档**（创建在此节点下）

**步骤 1：创建 wiki 节点（原子操作）**
```bash
cd /Users/openclawer/.openclaw/workspace/日志管理
set +e  # lark-cli 非 0 不阻断（文档可能已创建成功）
${LARK_CLI} wiki +node-create \
  --space-id 7621391289904516315 \
  --parent-node-token SERDwHBAniUqqBkx5vNctvgKn6f \
  --title "日志简报 {target_date} | 张公子"
WIKI_RC=$?
set -e
if [ $WIKI_RC -ne 0 ]; then
  echo "⚠️ wiki 节点创建失败（exit $WIKI_RC），文档可能已创建，请检查知识库"
fi
```
- 从返回的 `obj_token` 提取新文档的 doc token
- 从返回的 `node_token` 提取新 wiki 节点 token

> ⚠️ **v0.1.31 去重（重要）**：`node-create` **每次调用都会真的建一个节点**，返回值里 `node_token` 与 `obj_token` 一次就有，**不要为了取另一个 token 再跑一次**。创建后必须验证唯一性：
> ```bash
> # 注意 --page-all：单页 node-list 只返回一页，会漏检并误判为「没建上」
> ${LARK_CLI} wiki +node-list --space-id 7621391289904516315 \
>   --parent-node-token SERDwHBAniUqqBkx5vNctvgKn6f --page-all --page-limit 30 \
>   | grep -c "日志简报 {target_date}"
> ```
> 若计数 > 1，删掉多余的（**`--obj-type` 必填**）：
> ```bash
> ${LARK_CLI} wiki +node-delete --node-token "<多余节点>" --obj-type wiki --yes
> ```
>
> ⚠️ **v0.1.39 强制四步巡检（复发预防，不可省略第 ④ 步）**：
> 2026-11-08 一次性清理了 15 个重复节点（5 空壳 + 10 有内容历史版本，207 → 192，重复组 11 → 0），但**产生重复的路径没变**。故每次 `node-create` 后必须走完：
> 1. `node-create` **只调用一次**（一次返回里同时给 `node_token` 与 `obj_token`）
> 2. 创建后立即 `wiki +node-list --page-all --page-limit 30` 按标题计数 → **计数 > 1 即为复发**
> 3. 删多余者：`wiki +node-delete --node-token "<多余>" --obj-type wiki --yes`
> 4. **再次枚举复核计数 = 1**
>
> **第 ④ 步为什么不可省**：`wiki +node-delete` 的 **stdout 只输出版本升级提示**，看不出成功与否——**唯一可信判据是重新枚举后的计数**。2026-11-08 的删除之所以能确认生效，靠的正是「207 → 202 → 192」这三次重新枚举，而不是命令返回成功。**只看退出码会漏掉「命令报成功但没生效」。**

**步骤 2：写入简报内容（原子操作）**
```bash
set +e  # lark-cli 非 0 不阻断
${LARK_CLI} docs +update \
  --api-version v2 \
  --doc "<obj_token>" \
  --command overwrite \
  --doc-format xml \
  --content -
DOC_RC=$?
set -e
if [ $DOC_RC -ne 0 ]; then
  echo "⚠️ 文档写入失败（exit $DOC_RC），请检查文档内容是否完整"
fi
```
> ⚠️ `--doc-format xml` 必须明确指定（默认 xml）。
> ⚠️ **重要**：飞书文档 **不支持 Markdown 表格**（写入时表格内容会丢失）。如简报包含表格，**必须使用 `--doc-format xml` 并提供 XML 格式内容**，XML 表格结构为 `<table><thead><tr><th>...</th></tr></thead><tbody><tr><td>...</td></tr></tbody></table>`。
> ⚠️ **有序列表不要写 `seq="auto"`**：`<ol seq="auto">` 会触发 DocxXML schema 警告（degrade_code=5002）。统一写成 `<ol><li>...</li></ol>`。

> ⚠️ **v0.1.28 DocxXML 标签白名单（必须遵守）**：只有下列标签被支持，使用白名单外的标签会触发 `degrade_code=4010` 并被**剥除**（内容保留但结构丢失，`result` 变为 `partial_success`）：
>
> | 用途 | 正确标签 | ❌ 错误写法 |
> |------|---------|-----------|
> | 文档标题（每篇唯一） | `<title>…</title>` | — |
> | 各级标题 | `<h1>` … `<h9>` | `<heading level="2">` |
> | 引用块 | `<blockquote>…</blockquote>` | `<quote>` |
> | 代码块 | `<pre lang="text"><code>…</code></pre>` | `<code_block>` |
> | 段落 / 列表 / 表格 | `<p>` `<ul><li>` `<ol><li>` `<table><thead><tr><th><tbody><tr><td>` | — |
> | 行内样式 | `<b>` `<em>` `<u>` `<del>` `<code>` `<a>` `<br>` `<span>` | — |
> | 分隔线 / 图片 | `<hr/>` `<img href="…"/>` | — |
>
> ⚠️ `docs +create` 时必须包含 `<title>`，否则告警 `missing_document_title`，文档显示为 Untitled。
> ℹ️ 完整规范见 `~/.openclaw/workspace/.agents/skills/lark-doc/references/lark-doc-xml.md`。
> ℹ️ **推荐做法**：用现成转换器 `日志管理/md2docx.py`（Markdown → DocxXML，已处理表格/代码块/标题/引用），生成 XML 后 `lark-cli docs +create --doc-format xml --content - < {file}.xml`。

**步骤 3：记录知识库 URL**

---

#### ③ 飞书文档（创建+写入一次完成，再授权）

**步骤 1：获取 tenant_access_token**
```bash
python3 -c "import base64;open('/tmp/gn_misc.py','w').write(base64.b64decode('CgppbXBvcnQganNvbiwgdXJsbGliLnJlcXVlc3QKd2l0aCBvcGVuKCciJyInL1VzZXJzL29wZW5jbGF3ZXIvLm9wZW5jbGF3L29wZW5jbGF3Lmpzb24nIiciJykgYXMgZjoKICAgIGQgPSBqc29uLmxvYWQoZikKIyBhcHBTZWNyZXQg5LuOIHNlY3JldHMuanNvbiDor7vlj5YKd2l0aCBvcGVuKCciJyInL1VzZXJzL29wZW5jbGF3ZXIvLm9wZW5jbGF3L3NlY3JldHMuanNvbiciJyInKSBhcyBmOgogICAgc2VjID0ganNvbi5sb2FkKGYpCmFwcF9zZWNyZXQgPSBzZWMuZ2V0KCciJyInY2hhbm5lbHMnIiciJyx7fSkuZ2V0KCciJyInZmVpc2h1JyInIicse30pLmdldCgnIiciJ2FjY291bnRzJyInIicse30pLmdldCgnIiciJ21haW4nIiciJyx7fSkuZ2V0KCciJyInYXBwU2VjcmV0JyInIicsJyInIicnIiciJykKcmVxID0gdXJsbGliLnJlcXVlc3QuUmVxdWVzdCgKICAgICciJyInaHR0cHM6Ly9vcGVuLmZlaXNodS5jbi9vcGVuLWFwaXMvYXV0aC92My90ZW5hbnRfYWNjZXNzX3Rva2VuL2ludGVybmFsJyInIicsCiAgICBkYXRhPWpzb24uZHVtcHMoeyciJyInYXBwX2lkJyInIic6JyInIidjbGlfYTk0YjRhMWU0Mzc4MWNjNyciJyInLCciJyInYXBwX3NlY3JldCciJyInOmFwcF9zZWNyZXR9KS5lbmNvZGUoKSwKICAgIGhlYWRlcnM9eyciJyInQ29udGVudC1UeXBlJyInIic6JyInIidhcHBsaWNhdGlvbi9qc29uJyInIid9CikKcmVzcCA9IHVybGxpYi5yZXF1ZXN0LnVybG9wZW4ocmVxLCB0aW1lb3V0PTEwKQpwcmludChyZXNwLnJlYWQoKS5kZWNvZGUoKSkK').decode());exec(open('/tmp/gn_misc.py').read())"
```

**步骤 2：创建文档并写入内容（原子操作）**
```bash
cd /Users/openclawer/.openclaw/workspace/日志管理
set +e  # lark-cli 非 0 不阻断
${LARK_CLI} docs +create \
  --api-version v2 \
  --parent-token FQfXfYBGGllxxydJ1SgcJZWqnpf \
  --doc-format xml \
  --content -
DOC_RC=$?
set -e
if [ $DOC_RC -ne 0 ]; then
  echo "⚠️ 文档创建失败（exit $DOC_RC），请检查内容格式是否正确"
fi
```
> ⚠️ **禁止先创建空文档再单独写入**。必须在 `--content` 中直接提供完整内容。
> ⚠️ **重要**：飞书文档 **不支持 Markdown 表格**，如简报包含表格，必须改用 `--doc-format xml` 并提供 XML 格式内容。
> ⚠️ **必须包含 `<title>`**（否则文档显示 Untitled），且**只能使用 DocxXML 白名单标签**（`<title>` `<h1>-<h9>` `<blockquote>` `<pre><code>` `<p>` `<ul><li>` `<ol><li>` `<table>` `<b>` `<em>` `<hr/>`），详见 Step 5② 的白名单表。

**步骤 3：提取 document_id（从返回的 `document.document_id`）**

**步骤 4：授予张公子 full_access 权限**
```bash
set +e  # lark-cli 非 0 不阻断后续步骤

# ✅ 首选：CLI 原生命令显式授权（bot 身份可用，无需 tenant_access_token）
${LARK_CLI} drive +member-add \
  --token <document_id> \
  --type docx \
  --member-type openid \
  --member-id ou_d8ace8a146610ca26bc07d8e68a5620f \
  --perm full_access \
  --yes
GRANT_RC=$?
set -e
if [ $GRANT_RC -ne 0 ]; then
  echo "⚠️ 权限授予失败（exit $GRANT_RC），文档已创建，张公子可在飞书文档内手动申请权限"
fi
```
> ⚠️ **不要用 curl 调 drive permissions API**：新版 OpenClaw 用 SecretRef 存储凭证，手动解析 tenant_access_token 会读到 `***` 而非真实 token；且 `lark-cli wiki +node-create` / `docs +create` 返回的 `permission_grant.status=skipped`（提示 "no current CLI user open_id is configured"）是 bot 身份下的正常现象，需靠上面的 `drive +member-add` 显式补授权。
> ℹ️ 两份飞书文档（知识库 docx + 共享文件夹 docx）都要各自执行一次 `drive +member-add`。

**步骤 5：记录文档 URL**

---

### 第六步：用户反馈

向用户发送完成通知，包含：
- Get笔记数量（分类统计：录音/播客/纯文本等）
- 参考对话记录数量
- 简报核心发现摘要（1-3句话）
- 各端存储结果链接

---

## 错误处理原则

1. **任何一步失败不影响其他步骤**：三端归档是独立的，写入本地文件是最基本的保障
2. **明确告知用户失败原因**：如果某个平台失败，需要在反馈中说明
3. **不要静默失败**：如果关键步骤（如获取数据）失败，必须通知用户
4. **写入前先查重**：仅当目标平台已有同名内容时才需查重。由于使用日期标题策略（三端均以 `{target_date}` 命名），同一天重复运行时才需要查重。若执行查重，**禁止**用 `ls | grep` pipe 方式（macOS `ls -la` 格式与 Linux 不同，容易误判）；直接用 `find ... -name "*${TARGET_DATE}*"` 查本地文件；`grep` 匹配到 0 结果时返回 exit code 1，这是**正常行为不是错误**，不要把 `grep exit 1` 当作命令失败处理。
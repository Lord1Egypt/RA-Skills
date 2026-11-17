> **何时读我**：看不懂退出码/错误码。
> **最短路径**：先查第一节退出码表，再查违规类别表。
> **回 [INDEX](INDEX.md)**

# 错误码与处置速查（Error Codes Reference）

> 全部 CLI 脚本的退出码、违规/告警类别、触发条件与处置动作的统一映射表。
> 程序化集成请以 `verify.py` 的退出码为契约（见下表）；其余脚本把判定写在输出里。

## 一、退出码（CLI 契约）

**缺省口径**（不带 `--exit-verdict`，人读/人工流程）：

| 退出码 | 脚本 | 含义 | 处置 |
|---|---|---|---|
| 0 | 全部 | 完成（verify: 完整性 PASS） | 正常继续；其余脚本的判定读输出报告 |
| 1 | **仅 verify.py** | 完整性守卫 FAIL——改稿动了数字/引用/术语 | **修改改稿**，不是改守卫、不是换参数 |
| 2 | 全部 | 用法或文件错误（compare 在 --exit-verdict 下另含「分块降级=部分覆盖」拦停，v4.6.0） | 看 stderr 提示：路径错/文件空/二进制/编码/超限，每条提示自带处置建议 |
| 1 | check_terms.py（独立口径） | 发现术语不一致（报变体对与次数） | 按「建议统一为」人工统一；`--report` 出 markdown 明细；或 `--unify 统一稿` 一键生成（复核替换清单后采用，v4.4.0） |
| 1 | check_terms.py --batch 目录（v3.7.0） | 跨文件变体漂移或文件内不一致（files→变体映射） | 按建议变体跨文件统一；`--report` 含逐文件明细 |
| 1 | check_stats.py（同 check_terms 口径） | 发现统计一致性问题（求和/分组 n/风格混用；--batch 含跨文件聚合） | 核对原始数据后改稿；`--report` 出 markdown 明细 |
| 2 | detect/pipeline（PDF 输入） | PDF 置信度低于门闸被拒（v3.8.0 起缺省门=中） | 按建议导出 UTF-8 文本/OCR 后重试；`--pdf-min-confidence 低` 恢复仅标注旧行为 |
| 0（附警告） | detect/pipeline --batch | 同批 ≥3 个 PDF 被门闸拒收→批级熔断警告 | 查 PDF 来源质量（扫描件/导出器），勿逐个硬调门闸 |

> pipeline.py / compare.py 的守卫判定在输出报告的「完整性守卫: PASS/FAIL」行；按退出码分支的脚本请调 verify.py。check_terms.py 的 0/1/2 是自己的契约（0=一致），与 verify 的 1=FAIL 语义不同表，勿混用。

**自动化口径**（v2.3.0：detect/compare/pipeline 加 `--exit-verdict` 后）：

| 退出码 | 含义 | 典型 CI 动作 |
|---|---|---|
| 0 | 干净（低档、无残留；pipeline 另含完整性 PASS） | 合并/继续 |
| 1 | 完整性守卫 FAIL（仅 pipeline 会产出；与 verify 契约同义） | 拒绝该改稿，回给 agent 重改 |
| 3 | 风格特征中及以上（≥28，需要深改） | 进深改队列（plan.py 排优先级） |
| 4 | 命中模型残留（critical） | 先跑 transform.py 清理 |
| 2 | 用法/文件错误（不受 --exit-verdict 影响） | 修调用 |

> `--batch + --exit-verdict` 聚合口径（v3.7.0 备案；v4.2.0 增补降级）：detect 逐行取
> 最坏档输出 0/3/4，扫描不出或**带 ⚠[降级] 标记的行** fail-closed 直接 2；
> pipeline 聚合最坏行——**降级行优先 2**（扫描残缺时 FAIL 判定本身不可信，
> 取更严重档）、integrity FAIL 1、错误行 2、其余按分数档 0/3/4。

> detect/compare 的 `--exit-verdict` 只出 0/3/4（完整性仍只写报告——exit 1 契约专属 verify/pipeline）；
> **pipeline 是唯一 1/3/4 全档判定命令**，CI 门禁推荐 `pipeline.py 原稿 --rewrite 改稿 --exit-verdict`。

## 一B、集中异常层（v2.5.0）

全部 CLI 的 `__main__` 统一经 `hxt_core.cli_entry(main)` 进入：任何用户侧
异常输出**两行中文**——「错误: <发生了什么>」+「处置建议: <怎么办>」——并以
exit 2 结束。`CliError(msg, hint)` 是脚本内主动报错的规范方式；SystemExit
原样穿透，各脚本语义化退出码不受影响。程序内部 bug 仍带完整 traceback
冒出（宁可吵，不可吞）。

### 分块扫描降级（v3.9.0）

超 1MB 文本自动分块后，单块扫描超时不再中止整体：先以 2× 预算重试一次，
仍超时则该块标记「降级」并继续其余块；报告与 JSON 的 degraded_chunks 字段
透出降级区间与覆盖率注记（「覆盖不全，勿当完整报告使用」）。
`--exit-verdict` 把降级视为扫描不完整（fail-closed，exit 2；detect 默认人读
出口同款拦停，批量降级行带「⚠[降级]」标记并同样拦停）；全部分块超时
则响亮报错（部分覆盖的降级语义不成立）。范围注记：plan（含 build_queue）
与 pipeline --batch 仍为超时整体失败口径（fail-closed 不变，未接降级）；
≤80 万字符单块文本不走分块，degrade 参数不生效。verify 的 JSON 报告新增 remedies
字段（每类违规的处置处方+数字丢失的原句锚点），人读输出同款「怎么修」行。

### 批量断点续传（v3.7.0）

`detect/pipeline --batch` 每完成一个文件即把结果原子落进批量目录的
`.pr_batch_state.json`；中断后 `--resume` 跳过「已完成且文件未变」的文件，
失败与已变更的自动重跑；不加 `--resume` 只重置本 CLI 的进度分区。detect 与
pipeline 在状态文件内各占一个分区（kind 分区制），交叉运行互不覆盖、互不串读
（两 CLI 行结构不同，跨 CLI 复用会污染输出 schema）。状态文件可随时删除
（等价全部重置）；写盘失败只提示不中断主流程。续跑请使用与首跑相同的
参数（--profile/--lang/--terms/--pdf-min-confidence 等）——进度只存结果不存参数，
换参续跑会把两种口径的行混进一张汇总表。

## 二、verify.py 违规类别（exit 1 = violations；WARN = 告警继续）

| 类别 | 级别 | 含义 | 常见原因与处置 |
|---|---|---|---|
| numbers | E_NUM_LOST | ✗ 红线 | 数字丢失/被改 | 深改时把数据句改写了——恢复原数字或重写该句 |
| comparison | E_CMP_FLIP | ✗ 红线 | 比较方向被改（P<0.05→P>0.05 级） | 结论方向反转，必须恢复原文方向 |
| doi / pmid | ✗ 红线 | DOI / PMID 丢失 | 引用被删或改写——恢复 |
| latin_abbr | E_ABBR_LOST | ✗ 红线 | 大写缩写丢失（DNA/PCR 类） | 缩写被中文化或删除——恢复原缩写 |
| terms | E_TERMS_LOST | ✗ 红线 | 术语表条目缺失/减少 | 术语被替换——恢复，或把该词从术语表移除（若确认非术语） |
| cjk_ratio | E_CJK_SHIFT | ✗ 红线 | 中英占比漂移超阈 | 整段被删或被译——检查是否误删段落 |
| length | E_LEN_DRIFT | ✗ 红线 | 长度变化超阈（长文 ±25%，短文放宽） | 内容被整段删除——核对删减是否有意 |
| fullwidth | E_NUM_WIDTH | ✗ 红线 | 数字/字母被改写为全角（２０２５≡2025 值等价但字符已变；v2.8.0） | 中文输入法所致——全部改回半角后重跑（学术稿件必须半角） |
| numbers_added | W_NUM_ADDED | ⚠ 告警 | 出现原稿没有的数字 | **编造防线**：深改时凭空补的数字必须删除 |
| number_context | W_CTX_SWAP | ⚠ 告警 | 数字上下文/顺序变化 | 两臂互换/方位错位——人工核对方向 |
| sentences_added | W_SENT_ADDED | ⚠ 告警 | 改稿新增原稿没有的完整句（≥8 字符，无数字也提示；v2.8.0） | 逐句核对是否擅自加内容（编造防线的一部分） |
| years | W_YEARS | ⚠ 告警 | 年份数量变化 | 年份引用被删——核对 |

阈值均可 CLI 覆盖：`--max-length-change`、`--max-cjk-shift`。

## 三、退出码 2 的常见触发与处置

| 触发 | 提示关键词 | 处置 |
|---|---|---|
| 文件不存在 | 无法读取 | 核对路径（相对路径基于技能目录） |
| 输入为空 | 输入为空 | 文件无内容或只传了空白 |
| 二进制/损坏文件 | 疑似二进制或损坏文件 | Word 用 .docx 直读；其他用编辑器另存 UTF-8 .txt（.doc/.rtf/.mht 不支持） |
| 编码错误 | 不是 UTF-8/GBK/UTF-16 等可识别文本编码 | 编码自适应已覆盖 UTF-8/UTF-16/GBK·GB2312·GB18030（v4.0 自动转码）；到这一步=彻底未识别——确认是纯文本后转 UTF-8 |
| —（无错误） | stderr 出现「已自动转码」提示 | v4.0 编码自适应生效：GBK/UTF-16 输入被透明转码处理，文件本体未动；建议顺手另存 UTF-8 |
| 文件超限 | 超过 50MB 上限 | 拆分文件分批处理 |
| docx 缺部件 | 缺少正文部件 | 可能只是改了扩展名——另存为真正 .docx |
| docx 加密 | 受密码保护 | 解除密码后另存 |
| 参数错误 | argparse 提示 | `--help` 查看合法取值（如 --profile academic/general） |

## 四、detect/pipeline 报告中的级别

| 级别 | 含义 | 建议 |
|---|---|---|
| 低（0-27） | 基本无模板腔特征 | 无需处理 |
| 中（28-49） | 有一定模板腔 | 可按 style_guide 选择性处理 |
| 高（50-74） | 模板腔特征明显 | 按 style_guide 深改 |
| 极高（75+ 或含硬残留） | 特征极重/含模型残留 | 先 transform.py 清硬残留，再按指南深改 |

分数口径：本地启发式风格诊断，非任何官方检测分数；短文本（<15 单元）自动降权并标注「仅供参考」。

## verify 输出分级（v5.10.0）

| 类别 | 语义 | 退出码 |
|---|---|---|
| violations（数字丢失/DOI/引用/术语漂移/长度漂移） | **硬失败**——改稿动了受保护内容，必须修复后重跑 | 1 |
| warnings（W_SENT_ADDED 新增原稿没有的句子/W_NUM_ADDED 新增数字/W_CTX_SWAP 上下文互换/W_YEARS 年份对调/length 接近警戒线） | **警告**——人工核对项，缺省不拦停 | 0 |
| `--strict` | 集成方零警告门禁：任何 warning 也判失败 | 1 |

判定口径：ok=true 只反映 violations 为空；警告是否算失败由 `--strict` 决定——集成方按需选择。

# FAQ（高频问题与排障）

> 从 SKILL.md 迁出的独立 FAQ（v6.3.0）：判定 → 模式 → 输出 → 安全 → 工具 → 具体技术问题。
> 命令行检索：`python3 scripts/pp.py faq <关键词>`（如 `pp.py faq 医学`、`pp.py faq PDF`）。
> **阅读分层**：前五组+「技术问答·用户高频」面向所有用户；「技术问答·集成者与进阶」面向集成方与深度排障，普通使用可跳过。
> 判断类铁律（哪些用法是错的）集中在 SKILL.md § 反模式——本文件管「怎么做」，那边管「不该怎么做」。

---

## 判定与边界（英文版）


### Verdicts & boundaries

**Q: Why no risk verdict for texts under 100 characters?**
Short-text false positives are uncontrollable (a few sentences carry no style distribution). The tool returns `risk=unknown` by design; submit 100+ chars (300+ recommended).

**Q: Why is my medical text scored high?**
You are most likely in degraded mode (optional supervised model not installed). Rules-only scoring systematically over-scores medical register (held-out human FPR at @medium: ~59% medical vs ~2% general). For medical text trust only @high verdicts, or install the supervised layer (next question).

### Modes & install

**Q: How do I install the supervised model and confirm it works?**
one command: `python3 scripts/pp_setup.py --model <author-signed model.onnx>` — it verifies the md5 against the signed registry, installs, and runs an inference canary (GREEN = active; `degraded_mode=false` in reports confirms it). Manual placement of the two files at `~/.cache/paper-polisher/qwen3-detector/` still works and `python scripts/pp_doctor.py` remains the full check.

**Q: What do degraded_mode / degraded_notice mean?**
Engine-mode disclosure: true = rules+spectrum fallback, reason in the notice (model missing / PP_NO_SUP=1 / English language gating). See the capability boundary matrix.

**Q: Is this score interchangeable with CNKI/Wanfang official checks?**
No. Thresholds are calibrated on our own held-out corpus and are not interchangeable with any institutional detector; self-check only (stated in journal-profile output too).

### Output & interpretation

**Q: A deai_gate layer shows "解析失败" (parse failure) — what now?**
That layer falls back to a neutral 50; other layers and the verdict are unaffected. Usually a subprocess timeout or odd input encoding; retry once, then run `pp_doctor.py`.

**Q: What is the edit-extent estimate?**
A supervised-layer regression head estimating how much the text was AI-edited (0-1). Limited discriminative power (ρ=0.54) — report metadata only, never used in verdicts.

**Q: Is English supported?**
Partially: the supervised layer is Chinese-trained, so English skips fusion by design and gets rules-only skeleton scoring, advisory only (stated in the report).

**Q: What about documents that mix human and AI writing?**
Watch the mixed-register signal (`mixed_signal=true`): document-level scores are diluted by human paragraphs or pushed up by AI ones — unreliable either way. Run `paragraph_report.py` for per-paragraph attribution and work paragraph by paragraph.

**Q: Why does a real, human-written journal paper still score medium/high?**
Two measured reasons: distribution shift (our held-out corpus differs from real journal PDF→text, which carries layout noise) and register calibration. Paragraph attribution is the actionable signal — use it to locate suspect passages for human review; the document-level score is a triage hint, not a verdict. The journal precheck (distribution口径) offers a second view and may disagree with the main score by design.

**Q: The fingerprint attribution says GPT-4o but my text is from another model?**
Attribution is heuristic (top-n candidates, never scored) and may misattribute — known case: GLM-generated text has been attributed elsewhere. Treat family hints as weak evidence; the detection score and paragraph attribution are the substantive outputs.

**Q: How do I use the AIGC label check?**
`python scripts/aigc_label_check.py manuscript.docx figures/*.png` — checks metadata / C2PA watermark / explicit declaration (China 2025-09 labeling rules). Exit 0 = labeled, 1 = unlabeled; both are normal runs.

### Safety & verification

**Q: How can I verify the "100% local / zero upload" claim myself?**
Run `python3 scripts/pp_verify.py` — an AST-level structural scan of every script. It flags network imports/calls and curl/wget-style subprocess commands, while URL strings in report footers are correctly treated as data (the old grep advice could not tell the two apart). Exit 0 = zero network calls. For behavior-level checks, the bundled test suite (`python -m unittest discover -s tests -t .`) exercises the iron laws and report contracts on your own machine.

**Q: Does the style-norm check produce a score or a verdict?**
No. `pp_style_norm.py` is a mechanical convention check (full/half-width, number styles, abbreviation definitions, unit formats). It lists findings with concrete advice; nothing is scored and nothing feeds into the AI-rate engine. The short-text iron law does not apply because no verdict is produced — but statistical checks (numbers/abbreviations) are naturally weak on very short samples and the output says so.

**Q: Can several batch runs write to the same CSV safely?**
Yes — since v4.9.0 batch CSV writes are atomic (write to a temp file, then rename into place). Two concurrent batch runs pointing at the same CSV cannot interleave or clobber each other's rows; the file always contains one complete run's output.

**Q: How should I read `degraded_notice`?**
It tells you which full-mode ingredient was skipped and why: supervised model missing, `PP_NO_SUP=1`, or English language gating. Consequences differ — degraded rules-only mode systematically over-scores medical register (see the boundary matrix), while English gating only means the Chinese-trained supervised layer does not apply. The notice names the reason so you can decide whether to install the model, unset the toggle, or treat scores as advisory.

### Tools & workflow

**Q: What do the rewrite suggestions do — do they change my text?**
No. `pp_fix_suggest.py` (`pp.py fix`) only locates sentences carrying improvable features and explains the improvement strategy per feature type (e.g., replace an AI cliché with a concrete claim, split a template sentence). It never edits your file; the editing decision and execution stay with the author. `--demo` shows a built-in two-sample walkthrough.

### Script cheat sheet

| Script | Purpose | Key flags | Output |
|---|---|---|---|
| ai_detector.py | Main AI-writing detector | `--lang auto\|zh\|en` `--format json\|text\|summary` `--profile journal` `--batch DIR` | Score + paragraph detail + fingerprints (JSON incl. degraded_mode/integrity_notice) |
| pp_fix_suggest.py | Sentence-level rewrite suggestions (v5.0.0) | `--top N` `--json` `--demo` | Per-sentence features + rewrite strategies (locates and suggests, never auto-rewrites) |
| pp_doctor.py | Environment self-check | `--json` | Data/deps/model probes; exit 0 = green |
| docx_text.py | .docx → text extraction (v5.3.0) | `file` `--output` | Paragraph-preserving text; zip-bomb guarded |
| freshness_refresh.py | Monthly freshness pipeline / status (v5.4.0) | `--status` `--json` | Last run, latest eval record, baseline drift, due flag |
| pp_report_bundle.py | Submission self-check bundle (v5.3.0) | `file` `--outdir` | Dated directory: workflow + paragraph HTML + suggestions + norm + manifest |
| pp_style_norm.py | Academic style-norm self-check (v5.2.0; +consistency v5.5.0; +llm_jargon v5.6.0) | `--json` `--checks a,b` | Findings with advice (fullwidth/numbers/abbrev/units); no score |
| pp_rewrite_check.py | Rewrite-effect regression check (v5.1.0) | `original revised` `--json` `--demo` | Score/risk-band migration + paragraph deltas + feature-type clears/remaining |
| pp_batch_report.py | Batch CSV → HTML summary (v5.1.0) | `csv_file` `-o out.html` | Totals/mean/band cards + histogram + per-file table |
| pp_report_html.py | Single-document visual dashboard (v5.8.0) | `json...` `-o out.html` `--title` | Self-contained HTML: gauge + histogram + paragraph/finding/ledger tables; zero external resources |
| pp_trend.py | Multi-run trend dashboard (v6.0.0) | `workflow.json.../目录` `-o` | Score trajectory SVG + per-run delta table (↓/↑ flagged); degraded-mode runs marked |
| pp_verify.py | Structured zero-network self-verification (v5.0.0) | `--json` | AST-level scan verdict; exit 0 = zero network calls |
| quality_report.py | Overall quality report | `--json` | Readability/quality dimensions for the manuscript |
| deai_gate.py | 4-layer fused gate | `--json` | composite score + verdict band (<35 pass / 35-55 review / ≥55 suspect) |
| paragraph_report.py | Paragraph attribution | `--output report.html` | HTML report |
| term_check.py | Terminology (2,344 terms) | `--auto-fix` `--output` | Standardization rate + fixed file |
| translation_smell_check.py | Translation-smell scan | `--json` | Hits + blind-spot terms |
| style_distance.py | Stylometry (human-likeness) | `--json` | style_score + verdict (advisory outside academic register) |
| aigc_label_check.py | AIGC compliance labels | files: docx/pdf/png/txt | Per-file label verdict |

## Architecture & fingerprint freshness (reference)

Everyday use needs none of this. The full architecture diagram, module map and the
fingerprint-freshness pipeline notes (calibration split strategy, monthly freshness
workflow, model-generation coverage) moved to [`references/architecture.md`](references/architecture.md) —
read on demand. Scenario-level how-to advice lives in [`references/best-practices.md`](references/best-practices.md).

---

## 判定与边界（中文版）


### 判定与边界

**Q：为什么不足 100 字的文本不给风险判定？**
短文本误报在学界公认失控（几句话撑不起文风分布）。工具按铁律输出 `risk=unknown`，分数仅供参考；请提交 100 字以上（建议 300 字以上）。

**Q：为什么我的医学文本分数偏高？**
大概率在跑降级模式（未装可选监督层）。纯规则引擎对医学语域系统性高估（留出集实测 @medium 档误报：医学约 59%、普通约 2%）。医学文本请只采信 @high 档结论，或安装监督层（下一条）。

### 模式与安装

**Q：监督层模型怎么装？怎么确认生效？**
一条命令：`python3 scripts/pp_setup.py --model <作者签发的模型文件>`——校验签发指纹、安装、推理金丝雀自检（GREEN 即生效；报告 `degraded_mode=false` 同样可确认）。手动把两个文件放到 `~/.cache/paper-polisher/qwen3-detector/` 仍然有效，`python scripts/pp_doctor.py` 仍是全量自检。

**Q：报告里的 degraded_mode / degraded_notice 是什么？**
引擎档位披露：true=纯规则+词频谱降级档，原因写在 notice 里（模型未装 / PP_NO_SUP=1 / 英文语言门控）。档位对照见「能力边界矩阵」。
**Q：`degraded_notice` 应该怎么读？**
它说明完整档的哪个成分被跳过及原因：监督模型缺失、`PP_NO_SUP=1`、或英文语言门控。后果不同——降级纯规则档对医学语域系统性高估（见能力边界矩阵），而英文门控只意味着中文训练的监督层不适用。提示里写了原因，据此决定装模型、去掉开关、或把分数当参考。


**Q：这个 AI 率和知网/万方的结果能互换吗？**
不能。阈值基于自有留出集校准，与任何机构官方检测不可互换，仅供投稿前自查（journal 预检输出内含此声明）。

### 输出与解读

**Q：deai_gate 某层显示"解析失败"怎么办？**
该层自动走中性 50 分兜底，不影响其他层与总判定。通常为子进程超时或输入编码异常；重跑一次，复现则用 `pp_doctor.py` 自检。

**Q：编辑程度估计（edit_extent）是什么？**
监督层附加回归头，估计文本被 AI 改写的程度（0-1）。判别力有限（ρ=0.54），仅作报告元数据，不参与判级。

**Q：支持英文吗？**
部分支持：监督层仅中文语料训练，英文按设计跳过监督融合、走纯规则骨架评分，结论仅供参考（报告会明示）。

**Q：一段人写、一段 AI 写的混合文档怎么办？**
注意报告中的"混写预警"（`mixed_signal=true`）：文档级分数会被人类段落稀释或被 AI 段落顶起，均不可单独采信；请运行 `paragraph_report.py` 逐段归因，按段落处理。

**Q：真实期刊论文（人写的）为什么也可能判 medium/high？**
两个实测原因：分布差异（自有留出集与真实期刊 PDF→文本存在排版噪声与分布偏移）+ 语域校准。**段落归因才是可用信号**——用它定位可疑段供人工复核；文档级分数只是 triage 提示，不构成定罪。期刊口径预检（分布口径）提供第二视角，与主评分方向不一致属设计内。

**Q：指纹归因说是 GPT-4o，但我的文本来自别的模型？**
归因是启发式参考（top-n 候选，只归因不进分），存在误归因——已知案例：GLM 生成的文本可能被归为其他家族。家族提示请当弱证据；检测分数与段落归因才是实质输出。

**Q：AIGC 合规标识检查怎么用？**
`python scripts/aigc_label_check.py manuscript.docx figures/*.png`——检查元数据/C2PA 水印/显式声明三类（对标《标识办法》2025-09）。rc=0 有标识、rc=1 无标识，均属正常执行。

### 安全与验证

**Q：「100% 本地 / 零上传」我自己怎么验证？**
跑 `python3 scripts/pp_verify.py`——AST 级结构化扫描全部脚本：网络 import/调用与 curl/wget 式子进程命令一律命中，报告页脚的 URL 字符串被正确视为数据（旧 grep 建议区分不了这两者）。exit 0=零网络调用。行为级验证可跑随包测试套件（`python -m unittest discover -s tests -t .`），铁律与报告契约在你自己的机器上逐条过。

### 工具与工作流

**Q：规范自查会出分数或判定吗？**
不会。`pp_style_norm.py` 是机械体例核对（全半角、数字写法、缩写定义、单位格式），只列 findings 与具体改法；不产生任何分数，也不进 AI 率引擎。短文本判定铁律不适用（因为根本没有判定）——但极短样本上的统计类检查（数字/缩写）天然不可靠，输出中会注明。

**Q：多个批处理任务写同一个 CSV 安全吗？**
安全——v4.9.0 起 batch CSV 为原子写（先写临时文件再改名落位）。两个并发批任务指向同一 CSV 不会互相穿插或覆盖；文件内容始终是某一次完整跑批的结果。

**Q：改写建议会改我的文件吗？**
不会。`pp_fix_suggest.py`（`pp.py fix`）只定位带有可改进特征的句子，并按特征类型解释改进策略（例如：AI 套话换成具体判断、模板句拆分改主动）。它从不编辑你的文件；改写与否、怎么改由作者本人决定。`--demo` 可看内置双样例演示。

### 各脚本速查

| 脚本 | 作用 | 关键参数 | 输出 |
|---|---|---|---|
| ai_detector.py | AI 痕迹检测主引擎 | `--lang auto\|zh\|en` `--format json\|text\|summary` `--profile journal` | 综合分+段落明细+指纹归因（JSON 含 degraded_mode/integrity_notice） |
| pp_fix_suggest.py | 句子级改写建议（v5.0.0） | `--top N` `--json` `--demo` | 逐句特征+改写策略（只指位与策略，不代改） |
| pp_doctor.py | 环境自检 | `--json` | 数据/依赖/模型/功能探针，exit 0=绿 |
| docx_text.py | .docx → 文本抽取（v5.3.0） | `file` `--output` | 按段落保留文本；解压炸弹防护 |
| freshness_refresh.py | 月度保鲜流水线/状态自检（v5.4.0） | `--status` `--json` | 最近执行/最新评测/基线漂移/到期旗标 |
| pp_report_bundle.py | 投稿前自查包（v5.3.0） | `file` `--outdir` | 带日期目录：workflow+段落 HTML+建议+规范+清单 |
| pp_style_norm.py | 学术写作规范自查（v5.2.0） | `--json` `--checks a,b` | findings 带改法（全半角/数字/缩写/单位）；不评分 |
| pp_rewrite_check.py | 改写效果回归验证（v5.1.0） | `原稿 改稿` `--json` `--demo` | 分数/风险带迁移+段落 delta+特征清除/残留 |
| pp_batch_report.py | 批量 CSV → HTML 汇总（v5.1.0） | `csv_file` `-o out.html` | 总数/均分/分档卡片+直方图+逐文件表 |
| pp_report_html.py | 单文档可视化仪表盘（v5.8.0） | `json...` `-o out.html` `--title` | 自包含 HTML：仪表盘+直方图+段落/建议/规范/台账表；零外部资源 |
| pp_trend.py | 多轮趋势仪表盘（v6.0.0） | `workflow.json.../目录` `-o` | 分数轨迹 SVG+逐轮 delta 表（↓改善/↑回升标注）；降级轮标记 |
| pp_verify.py | 结构化零网络自证（v5.0.0） | `--json` | AST 级扫描判定，exit 0=零网络调用 |
| quality_report.py | 综合质量报告 | `--json` | 可读性/质量多维度指标 |
| deai_gate.py | 四层融合门禁 | `--json` | composite 分+判定带（<35 通过 / 35-55 复核 / ≥55 疑似） |
| paragraph_report.py | 段落级人机归因 | `--output report.html` | HTML 报告 |
| term_check.py | 术语标准化（加载 2,344 条） | `--auto-fix` `--output` | 标准率+修复文件 |
| translation_smell_check.py | 翻译腔筛查 | `--json` | 命中清单+盲区新词 |
| style_distance.py | 文体特征（人类相似分） | `--json` | style_score+verdict（学术域外仅供参考） |
| aigc_label_check.py | AIGC 合规标识 | 文件可为 docx/pdf/png/txt | 逐文件标识判定 |

## 架构与指纹保鲜（参考）

日常使用无需阅读本节内容。完整架构图、模块地图与指纹保鲜流水线说明
（校准切分策略、月度保鲜流程、模型代际覆盖）已迁移至
[`references/architecture.md`](references/architecture.md)——按需阅读。
场景级怎么用建议见 [`references/best-practices.md`](references/best-practices.md)。

---

## 具体技术问题（中文版）

#### 用户高频（怎么用/为什么这样设计）

**Q: 「熔断」是什么？**
批处理模式遇到**连续**多个文件解析失败时提前中止剩余队列（默认连续 5 个，`--circuit 0` 关闭），防止对整目录坏文件白烧时间。已完成的文件照常出 CSV/报告，中止事实写入 JSON 与摘要。非连续的偶发失败只记 ERROR 行不触发。

**Q: 批量里有几个文件失败了，要手动重跑吗？**
不用。v6.4.0 起失败文件在首轮结束后自动补扫（`--retries` 轮，默认 2；`--retries 0` 关闭）：瞬时错误（文件被占用、读取抖动）大多当场自愈，补扫成功的行标 `retried: true`。耗尽仍失败的进 JSON `failed_files` 清单（附诊断指引行）；首轮已熔断则不补扫（坏批次明确，补扫只是白烧时间）。单个失败文件想看完整错误：`python3 scripts/pp.py detect <该文件>`。

**Q: 批量时某个文件把整个任务弄崩了怎么办？**
不会了。v6.8.0 起批量默认子进程隔离（`--isolate auto`：装了监督模型即开启——崩溃源是模型原生层）：每个文件在独立 worker 里检测，硬崩溃只损失该文件、批处理继续，错误行如实标注；输入类错误（如损坏 docx）直接透传友好提示。纯规则档默认进程内快路径，`--isolate on` 可显式开启。

**Q: 集成方怎么校验拿到的输出结构？**
四大核心输出（detect/fix_suggest/workflow/term_report）随包 JSON Schema 契约：`python3 scripts/pp.py schema --selfcheck` 用真引擎输出逐一过契约（v7.7.0）；集成方在自己的环境里调 `pp_api.schema_selfcheck()` 验证拿到的结构。顶层必填键与类型是兼容性承诺——新增键不破坏契约，删除/改型会在 CHANGELOG 声明。

**Q: 怎么确认我下载的包没被截断/篡改？**
`python3 scripts/pp_doctor.py --deep`：包内 `data/INTEGRITY_MANIFEST.json` 记录全部数据与词表 JSON 的 SHA256 与字节数，--deep 逐文件核对哈希+解析（v7.6.0）。若某文件哈希不符，输出会给出文件名与期望/实际哈希——那是分发链路问题，请带着该输出提 issue。

**Q: MCP server 有 HTTP 形态吗？**
有（v7.2.0）：`python3 scripts/pp_mcp_server.py --transport http --port 8815`——仅监听 127.0.0.1 回环（与零网络立场一致，跨机访问不在支持范围也未加鉴权，勿端口转发暴露）；`POST /mcp` 收单条 JSON-RPC，`GET /health` 探活；适合同机多个客户端复用一个 server。

**Q: 学位论文整个要自查一遍，有没有一条命令的？**
有。`python3 scripts/pp.py project 章节目录/ --outdir project_report/`（v6.9.0 项目工作台）：逐文件跑完整自查（每章 workflow 报告照常落盘）、内嵌跨文件术语一致性矩阵、产出项目总览 HTML（逐文件分数对照+项目聚合+统一建议）。单文件失败只损失该文件（与批量同哲学）。

**Q: 学位论文多个章节的术语写法不统一，怎么查？**
`python3 scripts/pp.py term-project 章节目录/`：跨文件写法矩阵 + 统一建议（以库标准名为准）。边界如实声明：只覆盖术语库内概念（224 个概念带别名映射）；库外自由写法本工具不可见，可配合 `term_check --neologism` 的词典外提示。

**Q: 被质疑 AI 写作，想要一份说明材料怎么办？**
`python3 scripts/pp.py evidence 文稿 --outdir evidence/` 生成检测证据报告（HTML+Markdown）：分数与风险带、逐特征命中定位、阈值口径、模型指纹、固定局限声明与学术诚信声明。诚实定位：如实呈现判定与证据，供自查与说明；**不构成「未使用 AI」的任何证明**。

**Q: 为什么不支持 PDF？**
零依赖（纯标准库）无法保证中文 PDF 抽取的正确性——与其给你可能错乱的文字，不如明确拒绝。把 PDF 另存为 .docx 或导出纯文本即可；需要保持排版翻译 PDF 用 doc-holmes。

**Q: 英文文本为什么只有参考分？**
监督层是中文训练的，英文按语言门控设计跳过融合，走纯规则骨架评分——仅供参考，不与中文结果混比。这是如实披露，不是缺陷隐藏。


#### 集成者与进阶（退出码/自证/装模/漂移排障）

**Q: 退出码 0/1/2/3 怎么用？**
0=成功；1=运行完成但未通过（verify 漂移、test 失败）；2=用法/输入错误（文件不存在、<100 字）；3=环境不满足（装模失败）。脚本与集成方按此分诊；环境问题先 `pp.py doctor`。

**Q: verify 报「AST 级扫描」是什么意思？**
pp_verify 用语法树扫描每个脚本：真正的网络调用（import/connect）会被发现；报告页脚里的 URL 只是字符串常量（数据），不算命中。exit 0 = 零网络调用。旧式 grep 会把 URL 字符串误当网络代码，AST 区分两者。

**Q: 装模失败/提示指纹不符？**
只接受作者签发注册表内的模型（md5_12 比对）。重新获取当前签发版：`pp_setup.py --guide`。不要绕过——签名保护的是打分可信度。

**Q: 为什么我的分数和上次不一样？**
先看档位：监督模型在位与否会改变分数（报告 degraded_mode 字段如实披露）；引擎版本升级也可能重校准。同稿同档同版本应当逐位一致——不一致就是 bug，欢迎提 issue。


---

找不到答案？环境问题先 `pp.py doctor`；确认是 bug 请到 GitHub 仓库（docsor1212/paper-polisher-pro）提 issue 附 `pp.py doctor` 输出。

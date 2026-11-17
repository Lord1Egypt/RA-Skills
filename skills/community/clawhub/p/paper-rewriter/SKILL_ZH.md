---
name: paper-rewriter
description: >
  论文改写与降AI率工具：对论文、期刊稿做去AI味改写、学术改写、段落改写与风格自然化——
  AI 味自查报告、模型残留清理、深改指引与句级优先级计划，全程守住数字、DOI、PMID、年份与
  术语（改文不改动数据）。check_stats 查数字打架，check_terms 查术语混用（八域变体组）；
  支持中英双语与 .docx/.pdf 输入，--batch 支持分章跨文件核对。
  适合行文生硬、模板腔重或非母语（ESL）的作者做投稿前自查。Skip when：纯语法润色、
  全文翻译、与学术写作无关的改写——请用对应工具。内置 AIGC 使用披露合规检查
  （中国 2025-09 标识办法）与学术诚信护栏：本工具只做写作质量自查与改进，不用于误代署名、
  隐瞒应披露的 AI 使用或对抗学术诚信审查。100% 本地运行，零上传，仅 Python 标准库。
  相关工具：paper-polisher-pro（综合润色）、pubmed-verifier、cite-holmes、academic-figures、
  cn-med-oa、doc-holmes。
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
metadata:
  displayName: 毕业论文降AI率·去AI味改写｜论文改写·学术表达优化
---

# 论文降AI率 · 去AI味 · 风格自然化（paper-rewriter）

**TL;DR**：`python scripts/pipeline.py draft.txt -o out.txt` → 读报告 →（要排优先级
就 `plan.py --handoff`）→ 按 style_guide 深改 → `verify.py` → 完成；Word 直读；守卫保数字引用。
**阅读地图（30 秒路由，等价 [references/INDEX.md](references/INDEX.md)）**——按需取用：

- **上手 / 排错**：快速上手 · [pitfalls](references/pitfalls.md)+[errors](references/errors.md)
- **流程 / 场景**：[deep_rewrite_guide](references/deep_rewrite_guide.md) · [best_practices](references/best_practices.md) · CI/agent→自动化节
- **边界 / 合规**：[honest_boundaries](references/honest_boundaries.md) · [permissions](references/permissions.md) · [compliance](references/compliance.md)
- **参考 / 工具**：[api](references/api.md) · [pdf_confidence](references/pdf_confidence.md) · [calibration](references/calibration.md) · [customization](references/customization.md)
**两层分工一句话**：机械清理（transform/pipeline 自动，确定性）与质量深改（agent 按 style_guide）是两层——先跑 pipeline 看报告再决定深改。

中英双语的学术写作风格工具箱：找出书面语里生硬、模板化、机器腔的表达模式，清掉
机械垃圾，按写作质量原则深改——每一步都带完整性护栏。

> **一句话路由**：改语法、改通顺、按期刊格式润色 → 用润色工具（paper-polisher-pro）；
> 去模板腔、清模型残留、降AI率/去AI味的风格自查与改写 → 用本工具。两者都要时先润色再跑本管线。

## 学术诚信护栏——先读这一节

- **正当用途**：润色自己的稿件；在学校/期刊**允许或要求披露**的前提下，把 AI 辅助
  的文本对齐到自己的行文习惯；清理合规草稿里粘贴带进的模型残留（oaicite/[cite:]
  等垃圾 token）；提升正式文体的清晰度、节奏与具体性。
- **不做的事**：不用于误代署名、隐瞒按规定应披露的 AI 使用、对抗学术诚信审查。
  如果请求的表述是「改到没人看得出来」「帮我瞒过审查」，agent 应拒绝这一目的、
  说明披露义务，并转而提供正当的质量改写路径。运行本技能的 agent 有责任守住这条线。
- **本工具从不动数据**：数字、p 值、置信区间、DOI、PMID、年份、术语全部由
  `verify.py` 守卫（见下）。文字可以改好，事实一个不能少。
- 合规：中国 AIGC 标识办法（2025-09-01 施行）、期刊披露政策与 arXiv 政策要点
  见 `references/compliance.md`——披露义务的主体是作者，不是工具。

## 能力×边界（分工 + 做到/做不到 + 去处）

| 能力 | 做到 | 做不到（边界） | 去处 |
|---|---|---|---|
| 风格自查 | 套话密度/句长均匀/公文腔启发式报告，章节感知降权；.md 输入自动剥离结构（医学知识库友好） | 非 AI 检测器——流畅模型文本几乎不触发（低分≠无 AI 参与） | `detect.py`；边界详见 [honest_boundaries](references/honest_boundaries.md) |
| 机械清理 | 模型残留（oaicite/[cite:]）、聊天客套、标点归一、全角数字 | 不改写句式——只做零信息损失层 | `transform.py`（`--deep` 句式级） |
| 质量深改 | 去模板化/节奏/具体性/立场（指南七步） | 不编造数据；凭空新增数字被守卫告警（W_NUM_ADDED，人工核对） | **agent 本人**按 style_guide；交接块 `plan --handoff` |
| 完整性守卫 | 数字/DOI/PMID/年份/术语原样保留，篡改即 exit 1（FAIL 自带怎么修处方+原句锚点） | 真伪判断——以原始数据为准，工具只核一致性 | `verify.py` |
| 前后对比 | 特征分变化+完整性判定+画像差值 | 不替代人工通读 | `compare.py` / `stylecheck --compare` |
| 术语一致性 | 八域 27 组变体（HF/心力衰竭/心衰 一组报齐）；`--batch` 跨文件漂移（各文件各自一致、合起来不一致）；`--unify` 一键统一稿（逐处替换计数透出，复核后采用） | 不判断术语用得对不对，只查称谓统一 | `check_terms.py --pack` / `--unify` |
| 统计一致性 | 百分比清单求和（划分用语句）/跨文件分组 n/p 与 P 风格 | 非统计审查——不判定结果真伪 | `check_stats.py`（`--batch` 跨文件） |
| 改写动作明细 | 删八股开场（众所周知→直入论点）/拆「不仅X而且Y」/清残留/标点全角化/２０２５→2025 | ——（全部确定性零信息损失） | `transform --deep` 自动 |
| 深改动作明细 | 黑话/翻译腔替换、节奏、具体性（**绝不编造数据**） | 重写句必须过 verify 才算完成 | agent 深改 |

**功能状态（v5.12.0）**——⚠️ 行 = 实验性（可能拒收合法文件或需人工复核）；**完整逐代际清单已下沉 [references/feature_status.md](references/feature_status.md)**，明细见 references/errors.md 与各专题文档。稳定速览（全部稳定）按五类：**诊断**（风格自查·章节专项 · 统计一致性 · 术语漂移/统一稿 · 阈值校准证据化 · EN 特征库 v3）｜**深改**（句级计划·指令单行号锚 · pipeline --handoff 交接块 · EN/CN 特征库与密度镜像）｜**守卫**（完整性 verify+守卫处方报告 · 编造防线 · 守卫自学习可导出共享 · 输出分级[violations 硬失败/warnings 警告/--strict 升级]）｜**批量**（断点续传·并发隔离 · 工作单/统计卡 · 修订记录）｜**交付**（投稿自查包 12 件·写入清单自证 · 体检报告/前后对照 · docx 回写 · 打印友好报告 · 包内自检 selfcheck · 外挂词表 --lexicon 多 skill 共享）。唯一 ⚠️ 实验性：

| 能力 | 状态 | 版本 |
|---|---|---|
| ⚠️ **PDF 直读+置信度自评**（嵌字体/ToUnicode 先试抽取封顶「中」；硬门闸校准表见 references/pdf_confidence.md；**v3.8.0 起缺省门=中**——乱码形态默认拒收，`--pdf-min-confidence 低` 恢复仅标注） | ⚠️ 实验性 | v1.6–3.8 |

**规模上限**：单块 800,000 字符（块间 2000 重叠）· 文件 50MB · 单步 120 秒。**PDF 置信度分档**：高=放心用 · 中=抽查关键数字 · 低=乱码形态（v3.8 起缺省拒收）。

## 自动化与 CI 集成（v2.3.0）

所有判定双口径机器可读：

- **缺省口径（人读流程）**：`verify.py` 独占退出码 0/1/2（1=完整性 FAIL）；
  detect/transform/compare/pipeline 跑完恒 0，判定写在报告里。不要按它们的
  缺省退出码写分支。
- **机器口径**——detect / compare / pipeline 加 `--exit-verdict`（或等价短别名
  `--ci`，v3.1.0 起，方便 CI 里少打字）：
  `0` 干净（低档、无残留）· `3` 风格特征中及以上（需深改）· `4` 命中模型残留
  （先跑 transform）· `1` 完整性 FAIL（仅 pipeline 产出，与 verify 契约同义）·
  `2` 用法错误（不受影响）。**pipeline 是唯一 1/3/4 全档门禁**，CI 推荐：
  `pipeline.py 原稿.txt --rewrite 改稿.txt --terms terms.txt --exit-verdict`。
- **JSON**：`detect -j`（完整扫描结果）、`pipeline --json`（前后分/verify 判定/
  `exit_verdict` 字段/处置提示/深改简报）、`compare --json`（变化量+verify）、
  `plan.py --json`（句级队列+预算投影）。一行门禁示例：
  `python scripts/pipeline.py 原稿.txt --rewrite 改稿.txt --json --exit-verdict || echo "拦截: $?"`
- 两套口径的退出码全表：`references/errors.md` 第一节。

## 快速上手

**装好先自检**：`python scripts/selfcheck.py`——环境/结构/核心功能冒烟/文档对账四段一条命令，exit 0 才算装好（发布包自带，CI/agent 用 `--json`）。

**普通作者怎么开口**（不用记命令，把这些话原样说给 agent 即可）：

| 你可以这样说 | agent 会做的 |
|---|---|
| 「帮我把这篇论文的 AI 味去掉 / 降一下 AI 率」 | detect 自查 → transform 清残留 → 按指南深改 → verify 守卫 |
| 「这段读起来太模板腔了 / 太像 AI 写的」 | 同上，重点走深改（style_guide 去八股） |
| 「文里有 oaicite、[cite: 1] 这种乱码残留」 | transform 一步清掉（确定性，不碰你的句子） |
| 「先告诉我哪几句最该改」 | `plan.py` 出句级优先级清单（要交接给另一个 agent 就加 `--handoff`） |
| 「改完了，帮我确认没改坏数字和引用」 | `verify.py` 守卫 + `compare.py` 前后对比 |
| 「给我一份风格体检报告 / 量化看看改没变好」 | `stylecheck.py` 画像（单稿体检或 `--compare` 看差值） |
| 「多章节文件术语要统一」 | `check_terms.py --batch 目录` 看跨文件漂移；单文件一键统一加 `--unify 统一稿`（替换计数全透出，复核后采用） |
| 「重点看看摘要/结论像不像 AI 写的」 | `detect.py 文稿 --section abstract`（或 conclusion）单节专项诊断——摘要是审稿人第一眼，模板腔在此最显眼 |
| 「量化看看改没变好」（大文件） | `compare.py 原稿 改稿`——超过 100 万字符自动分块扫描，降级块在报告显著标注 |
| 「查查数字有没有前后打架 / 百分比加起来对不对」 | `check_stats.py` 统计一致性报告（退出码同 check_terms） |
| 「给我一份能直接发给导师/编辑的自查材料」 | `pipeline.py 原稿 --bundle 目录` 生成投稿自查包（12 件，含体检报告与守卫处方） |
| 「扫到的 XX 是正常术语，别再报它」 | `learn_guards.py` 固化守卫，类似上下文下不再误报（守卫按上下文窗口豁免，全新语境仍会报） |

无需 agent——以下全部命令可直接在终端运行。
所有脚本内建 `--help`（完整参数说明与权威口径）与 `--version`；跨脚本常用参数
语义速查见 [references/api.md](references/api.md) 首节（与本表曾载内容同口径，v4.7.0 起下沉该处）。

一条命令（自查→清理→深改简报→完整性守卫）：

```bash
python scripts/pipeline.py draft.txt -o out.txt --terms terms.txt
```

- **可视化/批量/章节**：`--html` 单文件报告（compare 含逐句对照）；`--batch 目录` 汇总；`detect --structure` 分章评分（方法/结果按领域惯例降权，各章原始分逐项展示）；`-o`/`--unify` 输出路径以 `.docx` 结尾即回写 Word（v4.4.0，纯段落回写——与 docx 直读构成闭环；表格/图片/样式不重建，复杂格式建议人工合并）。
- **输入格式**：`.txt`/`.md` 直读（**UTF-8/UTF-16〔带 BOM〕/GBK 编码自动识别转码**，v4.0） · `.docx`（Word）直读 · PDF 实验性直读
  （**v3.8.0 缺省安全门=中：乱码形态直接拒收**，`低` 恢复仅标注——见 faq Q15）。
- **术语表**：`python scripts/extract_terms.py draft.txt -o terms.txt` 自动抽候选，
  人工删改后给 `--terms`；任何运行加 `--suggestions 路径.md` 同时出修订建议工作单。

非学术文本（博客、公众号、公文）加 `--profile general`，学术八股/公文过渡与
模板结构类信号降权 60% 减少误报；默认 `academic` 按学术论文口径标定。
两档分数口径不同（general 分数整体偏低），不可跨档直接对比——同一文本只与
同档历史扫描比。

或分步执行（请在技能所在目录内运行，或把 `scripts/…` 换成绝对路径）：

```bash
python scripts/detect.py draft.txt            # 风格自查（-j JSON / -s 只看分）
python scripts/transform.py draft.txt -o step1.txt
# ……按指南对 step1.txt 做质量深改……
python scripts/verify.py draft.txt step2.txt --terms terms.txt
python scripts/compare.py draft.txt step2.txt
```

端到端完整输入输出样例：`references/examples.md`。统一错误码与处置速查：
`references/errors.md`。**集中式常见错误用法清单（27 条）：`references/pitfalls.md`**
——首次实战前先读。Python API 参考：`references/api.md`。常见问题：
`references/faq.md`。

修订追踪：transform/pipeline 加 `--track base` 把机械清理的**每一处修改**记录为
base.md+base.json 可审计清单。

### Agent 调用协议

被触发时先选路径，再执行：

- **触发词**：论文降AI率 / 去AI味 / 去AI味改写 / 降AI改写 / 风格自然化 /
  写作风格自查 / 论文改写 / 学术改写 / 段落改写 / 表达优化 / 去模板腔 /
  翻译腔清理（=欧化句式：「被…所」「对…进行」「…性/…化」堆叠、长定语链——见 style_guide_zh 第 5 步）/
  论文润色（限风格自然化语义，见下方消歧）——英文同样生效：rewrite for academic
  tone / reduce AI-flavored patterns / style naturalization / clean model artifacts /
  unify terminology / check number consistency → 跑上面的管线。
  （参数速查表见「快速上手」节；两套退出码表见 references/errors.md——
  均从本节链接直达，避免跨节翻找。）
- **场景直达（v3.8.0 收拢，不再散落 references）**：CI/批量门禁 → `--exit-verdict`（短别名 `--ci`）；
  批量中断 → `--batch 目录 --resume`；误报固化 → `learn_guards.py from-text`；
  深改无从下手 → `pipeline 原稿 -o 改稿 --handoff 交接块.md` 一句出逐句指令单。
- **语义消歧（本工具 ≠ 润色工具）**：「论文改写/润色」指风格自然化/去模板腔（降AI味）。
  判断标准——只关乎语言正确性/通顺的给润色工具（paper-polisher-pro）：「帮我改下语法」「按期刊风格改写摘要」；
  关乎模板腔或模型残留的给本工具：「这篇读起来像 AI 写的」「文里有 [cite: 1] 这种残留」；
  两者都要时先润色再跑本管线——互不替代。
- **用户想知道先改哪里** → `plan.py draft.txt -o plan.md`（P0 句级队列 + 预算投影）；
  要把深改交给另一个 agent 执行时加 `--handoff`（逐句指令单，含守卫铁律与验收命令）。
- **术语称谓混用**（缩写与中文全称、同义术语不一致）→ `check_terms.py 文稿
  --pack <域>`；要直接出统一稿加 `--unify 统一稿路径`（每组归一为出现最多的
  变体、逐处替换计数全透出——建议产物，复核后采用，随后建议 verify；
  v4.4.0）；`--list-packs` 列出八个域包（v3.0.0）。
- **数字前后打架**（百分比清单不凑整、同一分组 n 不同、p/P 风格混用）→
  `check_stats.py 文稿`（v3.2.0，退出码同 check_terms：0 一致 / 1 有问题）。
- **用户想量化验收改稿** → `stylecheck.py 原稿 改稿 --compare`（v2.6.0 风格
  画像差值；触发词：风格画像 / 量化验收 / 深改验收 / style profile）。
- **批量跑到一半中断（Ctrl-C/断电/超时）** → `--batch 目录 --resume` 续跑（跳过已完成、
  失败与变更的自动重跑；进度在目录内 .pr_batch_state.json）。
- **多章节文件术语要统一** → `check_terms.py --batch 目录`（跨文件变体漂移：
  各文件各自一致、合起来不一致，单文件模式看不见）。
- **扫描误报了正当术语** → 不要手改词表文件；用 `learn_guards.py from-text
  术语 样本.txt`（或 `add`）固化守卫——升级不丢，之后每次扫描自动生效。
- **用户只想复核已有改稿** → `pipeline.py draft.txt --rewrite 改稿.txt --terms terms.txt`。
- **用户要求隐瞒 AI 使用、误代署名或对抗诚信审查** → 拒绝该目的，指向
  `references/compliance.md`，改提供正当质量改写路径；不得把本工具用于该目的。
- 退出码：`verify.py` 是严格契约方——`0` 完整性 PASS、`1` 完整性 FAIL
  （修改稿，不修守卫）、`2` 用法/文件错误；`detect/transform/compare/pipeline`
  把判定写在输出报告里，跑完恒返回 `0`（用法/文件错误为 `2`）；
  `check_terms.py` 独立口径：`0` 术语一致、`1` 发现不一致、`2` 用法错误
  （`--unify` 模式恒 `0`=统一稿已生成或已一致，机器分支读 `--json`）。
  agent/CI 按退出码分支时加 `--exit-verdict`（v2.3.0）：detect/compare 出
  0/3/4，pipeline 出全档 0/1/3/4——见「自动化与 CI 集成」节。
  所有脚本支持 `--version`。

## 工作流（按序执行）

1. **自查**：`detect.py draft.txt`——启发式风格特征报告（套话、句长均匀、
   公文过渡语、模型残留）。报告供作者本人复查；分数是本地启发式，不代表
   任何官方测量，也不说明署名归属。
   （注：`--deep` 的句首套话删除/合并会改变句边界，`verify` 的「新增句子」
   告警对这些改写句属预期——以 `--track` 修订记录为准；管线内路径已自动豁免。）
2. **机械清理**：`transform.py draft.txt -o step1.txt`——清除粘贴带进的各家
   模型残留（`oaicite`/`turn0search`/`[cite: 1]`/`grok_card`/`attached_file`）、
   聊天客套句、Markdown 残留与语法安全的填充短语；中文半角标点自动全角化
   （小数保护）。`-a` 激进档追加破折号降噪、空泛开场删除。`--deep`（v2.4.0）
   追加句式级确定性转换——句首八股删除、「不仅X，而且Y」→「X，且Y」合并——
   只做零信息损失操作，每笔进 `--track` 可审计——该记录即审计凭据。无命中的文本保持零改动（全角字母数字归一为唯一例外）；每笔替换计数可用 `--track` 复跑核对，本节宣称均可本地复验。
3. **质量深改**（真正的活）：可先用 `python scripts/plan.py draft.txt -o plan.md`
   生成句级改写优先级计划（P0 队列：每句带章节归属、命中类别、处理原则与
   预算投影），把深改力气花在贡献最大的句子上；加 `--handoff` 直接产出
   **深改交接块**——逐句「原句+操作指令+守卫铁律+验收命令」的指令单，
   交给执行改写的 agent 可照做（v3.0.0）。然后按文本语言读对应指南——
   - 中文：`references/style_guide_zh.md`（去骨架模板→黑话→节奏→具体化→
     立场→完整性红线）
   - 英文：`references/style_guide_en.md`（小词→拆意义框架→散句化→节奏→
     真归因→亮立场）
   - 逐段改写；事实、数字、引用、术语全部保留。
3b. **量化验收**（`stylecheck.py`，v2.6.0）：段落级风格画像——黑话命中定位
    到段、句长节奏 CV、开场词多样性，逐项标「自然/观察/偏机器」并给指南
    锚点；`stylecheck.py 原稿 改稿 --compare` 看差值，深改验收从凭感觉变
    看指标。档位只是校准提示，不改变任何评分。`--json` 下另有 `stats` 统计面板
    （TTR/虚词比例/句长分位，v3.1.0，信息性口径——看改稿前后的趋势，不判档）。
4. **守卫**：`verify.py draft.txt step2.txt --terms terms.txt`——exit 1=有数字/
   引用/术语被动过，改改稿不改守卫；FAIL 自带处方（怎么修+原句锚点+修复三步）。医学文本建议先做术语表
   （药名/基因名/量表名，每行一个；鼠源基因首字母大写形态如 Myc 也要列入）；
   同义称谓混用（如「肝功能/肾脏功能」「SLE/系统性红斑狼疮」）另跑
   `check_terms.py 文稿 --pack 心血管`（v3.0.0 八个学科域包，`--list-packs` 看全表）；
   数字内部自洽（百分比清单求和/分组 n 前后一致/p 与 P 风格）在**定稿/送审前**
   对原稿跑 `check_stats.py 文稿`（审稿人对数字打架的容忍度远低于文风问题；
   先核对原始数据是笔误还是口径差异，再改表述）；分章分稿写长文用
   `check_stats.py --batch 目录`（v3.3.0 跨文件分组 n 聚合——摘要 vs 方法/结果
   的数字打架单文件检查看不见；只核 n= 记法，散文形态的数字打架需人工）。一条命令全带：`pipeline.py 原稿 --check-stats`；要交付级汇总用
   `pipeline.py 原稿 --bundle 目录`（投稿自查包一次生成：体检报告/前后对照/守卫处方全在包内，00-11 共 12 个编号件）。
   守卫还会对「凭空新增的数字」告警（编造防线）与「数字上下文互换」提示
   （两臂/方向核对）。
5. **复核**：`compare.py draft.txt step2.txt`——特征下降 + 完整性判定。
   建议保留前后稿；如学校/期刊要求 AI 使用披露，请如实声明——本报告只是
   质量自查记录，不能替代披露。

## 诚实边界（摘要）

风格分=本地启发式统计，非任何官方检测，不说明作者身份；本工具不与任何外部
评审系统交互、不协助隐瞒 AI 使用；对流畅模型文本几乎不触发（**低分≠没有 AI 参与**）。
**完整边界与实测数据：[references/honest_boundaries.md](references/honest_boundaries.md)**（承诺任何事之前必读）。

## 权限与环境声明（摘要）

只读显式传入路径+自带词表；只写显式输出路径（-o/--report/--html/--track/--bundle/
--suggestions 等，逐旗标清单见下沉文档）、user_guards.json 与批量目录内的断点进度
.pr_batch_state.json 及其并发锁 .pr_batch_state.json.lock；**零网络、零第三方依赖、
不读环境变量、不建子进程**。完整清单与验证命令：
[references/permissions.md](references/permissions.md)（审核者/安全扫描必读）。

## 自定义（摘要）

误报固化用 `learn_guards.py`（写 user_guards.json，升级不丢——**不要手改 patterns_*.json**）。
词表/标定文件位置与改动须知：[references/customization.md](references/customization.md)。

## 相关工具

- pubmed-verifier —— 批量核验 PMID/DOI 引用真实性
- cite-holmes —— 课题深度调研，引用逐条自证
- paper-polisher-pro —— 综合润色与降重
- academic-figures —— 出版级论文配图
- doc-holmes —— 保持排版的 PDF 精准翻译
- 医学知识库：docsor.cn

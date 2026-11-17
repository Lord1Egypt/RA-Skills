---
name: humanize-ai-text
description: >
  学术写作风格工具箱（中英双语，academic writing style toolkit）：论文降AI率、去AI味的风格自查与自然化改写工具（style naturalization & style-pattern scan）。
  写作风格特征自查报告、确定性文本清理（各家模型残留、标点、填充短语）、完整性
  守卫（数字/DOI/PMID/术语必须原样保留）、以及由 agent 执行的风格自然化深改
  （去模板化、去翻译腔、节奏、具体性），让正式文体更清晰自然——特别适合行文
  生硬、模板腔重的作者与非母语（ESL）学者。内置 AIGC
  使用披露合规检查（中国 2025-09 标识办法）与学术诚信护栏：本工具只做写作质量
  自查与改进，不用于误代署名、隐瞒应披露的 AI 使用或对抗学术诚信审查。100% 本地
  运行，零上传，仅 Python 标准库。家族：paper-polisher-pro（综合润色）、pubmed-verifier、
  cite-holmes、academic-figures、cn-med-oa、doc-holmes。
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# 论文降AI率 · 去AI味 · 风格自然化（paper-rewriter）

**TL;DR**：`python scripts/pipeline.py draft.txt -o out.txt` → 读报告 → 按 style_guide
深改 → `verify.py` → 完成。Word（.docx）直读、英文 PDF 实验性直读；完整性护栏保住
每一个数字与引用。

中英双语的学术写作风格工具箱：找出书面语里生硬、模板化、机器腔的表达模式，清掉
机械垃圾，按写作质量原则深改——每一步都带完整性护栏。

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

## 分工设计

| 层 | 谁做 | 做什么 |
|---|---|---|
| 风格自查 | `scripts/detect.py` | 启发式风格特征报告（模板腔、节奏均匀、公文 boilerplate），供作者自查 |
| 机械清理 | `scripts/transform.py` | 模型残留、聊天客套句、标点归一、语法安全的填充短语替换——只做语法安全层。**何时直接用它**：只需要残留/填充清理、不需要风格诊断时（快、确定性） |
| **质量深改** | **你（agent 本人）** | 按 `references/style_guide_zh.md`（英文用 `_en.md`）：去模板化、节奏、具体性、立场 |
| 完整性守卫 | `scripts/verify.py` | 数字/DOI/PMID/年份/缩写/术语必须原样保留 |
| 前后对比 | `scripts/compare.py` | 特征分变化 + 完整性判定 |

## 快速上手

一条命令（自查→清理→深改简报→完整性守卫）：

```bash
python scripts/pipeline.py draft.txt -o out.txt --terms terms.txt
```

可视化与批量（v1.5.0）：detect/pipeline/compare 均支持 `--html report.html` 生成
单文件 HTML 报告（评分卡/分类明细/修订工作单/完整性红绿结论；compare 额外含逐句
增删对照）。`--batch 目录` 批量扫描整目录（detect 出逐文件评分汇总；pipeline 逐
文件「清理+守卫」出汇总 CSV）——多章节论文批量诊断场景。

**章节感知扫描**（`detect --structure`，v1.7.0）：识别论文结构（摘要/引言/方法/
结果/讨论/结论/参考文献，中英双语）分章节评分。方法/结果的固定句式是领域惯例
而非机器特征——降权只归一综合分，各章节原始分仍逐项展示；缺章节有提醒。

术语表准备：`python scripts/extract_terms.py draft.txt -o terms.txt` 自动抽取候选
（大写缩写按频次/书名号引号内专业词），生成带注释头的草稿，人工删改后即用。
输入格式：`.txt`/`.md` 直读，v1.3.0 起 **`.docx`（Word）直读**，v1.6.0 起 PDF 实验性直读（限英文文本型；详见下文与 faq）；PDF 相关旧表述已由上方 v1.6.0 条目取代
可靠抽取——请先导出为文本。任何运行都可加 `--suggestions 路径.md` 同时生成
**修订建议工作单**（类别/样本/处理原则/指南锚点）——工具只提议，改不改、怎么改
由你和指南决定。

非学术文本（博客、公众号、公文）加 `--profile general`，学术八股/公文过渡信号
降权 60% 减少误报；默认 `academic` 按学术论文口径标定。

或分步执行（请在技能所在目录内运行，或把 `scripts/…` 换成绝对路径）：

```bash
python scripts/detect.py draft.txt            # 风格自查（-j JSON / -s 只看分）
python scripts/transform.py draft.txt -o step1.txt
# ……按指南对 step1.txt 做质量深改……
python scripts/verify.py draft.txt step2.txt --terms terms.txt
python scripts/compare.py draft.txt step2.txt
```

端到端完整输入输出样例：`references/examples.md`。统一错误码与处置速查：
`references/errors.md`。**集中式常见错误用法清单（20 条）：`references/pitfalls.md`**
——首次实战前先读。Python API 参考：`references/api.md`。常见问题：
`references/faq.md`。

修订追踪与 PDF（v1.6.0）：transform/pipeline 支持 `--track base` 把机械清理做过的
**每一处修改**记录为 base.md+base.json（可审计清单）。**PDF 直读（实验性）**：英文
文本型 PDF 直读；CJK/嵌入字体 PDF 明确拒收并引导导出文本。分块阈值已量化：单块 800,000 字符；文件大小护栏 50MB（扫描自动分块，完整性守卫整文）。

### Agent 调用协议

被触发时先选路径，再执行：

- **触发词**：论文降AI率 / 去AI味 / 风格自然化 / 写作风格自查 / 论文改写 /
  去模板腔 / 翻译腔清理 → 跑上面的管线。
- **用户只想复核已有改稿** → `pipeline.py draft.txt --rewrite 改稿.txt --terms terms.txt`。
- **用户要求隐瞒 AI 使用、误代署名或对抗诚信审查** → 拒绝该目的，指向
  `references/compliance.md`，改提供正当质量改写路径；不得把本工具用于该目的。
- 退出码：`verify.py` 是严格契约方——`0` 完整性 PASS、`1` 完整性 FAIL
  （修改稿，不修守卫）、`2` 用法/文件错误；`detect/transform/compare/pipeline`
  把判定写在输出报告里，跑完恒返回 `0`（用法/文件错误为 `2`）。
  所有脚本支持 `--version`。

## 工作流（按序执行）

1. **自查**：`detect.py draft.txt`——启发式风格特征报告（套话、句长均匀、
   公文过渡语、模型残留）。报告供作者本人复查；分数是本地启发式，不代表
   任何官方测量，也不说明署名归属。
2. **机械清理**：`transform.py draft.txt -o step1.txt`——清除粘贴带进的各家
   模型残留（`oaicite`/`turn0search`/`[cite: 1]`/`grok_card`/`attached_file`）、
   聊天客套句、Markdown 残留与语法安全的填充短语；中文半角标点自动全角化
   （小数保护）。`-a` 激进档追加破折号降噪、空泛开场删除。人写的干净文本
   逐字节原样通过。
3. **质量深改**（真正的活）：按文本语言读对应指南——
   - 中文：`references/style_guide_zh.md`（去骨架模板→黑话→节奏→具体化→
     立场→完整性红线）
   - 英文：`references/style_guide_en.md`（小词→拆意义框架→散句化→节奏→
     真归因→亮立场）
   - 逐段改写；事实、数字、引用、术语全部保留。
4. **守卫**：`verify.py draft.txt step2.txt --terms terms.txt`——退出码 1 表示
   有数字/引用/术语被动过：改的是改稿，不是守卫。医学文本建议先做术语表
   （药名/基因名/量表名，每行一个；鼠源基因首字母大写形态如 Myc 也要列入）。
   守卫还会对「凭空新增的数字」告警（编造防线）与「数字上下文互换」提示
   （两臂/方向核对）。
5. **复核**：`compare.py draft.txt step2.txt`——特征下降 + 完整性判定。
   建议保留前后稿；如学校/期刊要求 AI 使用披露，请如实声明——本报告只是
   质量自查记录，不能替代披露。

## 诚实边界（承诺任何事之前先读）

- 风格分是对写作模式的本地启发式度量，不代表任何外部服务的测量结果，
  更不说明文字由谁写成。永远不要把它当成那种东西来展示。
- 正式学术文体与非母语写作经常被自动化评审误判；如果你是作者本人，请保留
  草稿、版本历史与写作笔记——署名问题靠过程证据解决，不靠风格分数。
- 本工具不与任何外部评审系统交互，不移除官方内容标识或水印，不协助隐瞒
  应做的披露。详见 `references/compliance.md`。
- 规模边界：回归测试覆盖至 ~1MB 级文本；扫描为线性复杂度（有界量词，无灾难性
  回溯）。内存约为文件 3 倍；超长稿件建议按章节切分处理，报告更可读。

## 权限与环境声明

供审核者、安全扫描与谨慎的用户查阅：

- 只**读取**你作为参数传入的文件路径（以及 stdin 管道输入，含 `--batch` 目录
  下的 .txt/.md/.docx 文件）和技能自带的词表文件（`scripts/patterns_*.json`）。可自行验证：

  ```bash
  grep -rnE "urllib|requests|socket|subprocess|os\.environ" scripts/ || echo "clean"
  ```

  （本版实测输出 clean——承诺可复现，不是修辞。）
- 只**写入**你用 `-o`/`--output`/`--suggestions`/`--html`/`--track` 指定的
  输出路径（`--track` 写 base.md + base.json 双文件）。
- **零网络访问**——无 HTTP 请求、无下载、无任何 API 密钥。
- **零第三方依赖**——仅 Python 标准库。
- **不读任何环境变量**；不创建子进程；不创建定时任务；不使用临时文件。
- 测试语料与开发笔记仅存在于开发仓库，不随发布包分发。

## 自定义

- `scripts/patterns_zh.json` / `patterns_en.json`：词表（含改写建议）、正则信号、
  术语保护（正当学术用法不误报，如 mutational landscape、pivotal trial、
  序列对齐、沉淀反应）、自动修复清单。
- 评分标定系数在 `scripts/hxt_core.py`（`_LANG_K`）；开发仓库 `tests/` 四语料
  （发布包不含）记录了预期分离度。

## 家族导流（Paper Toolbox 论文全家桶）

- **paper-polisher-pro** — 综合润色：术语、翻译腔、比喻审计、AIGC 标识合规、期刊预检
  （全面润色找它；风格自然化找本技能，两者可同时使用互不冲突）
- **pubmed-verifier** — 投稿前 PMID/DOI 引用验证，防幻觉引用
- **cite-holmes** — 深度调研 + 全链引用核查
- **academic-figures** — 一条命令出顶刊级论文配图
- **cn-med-oa** — 中文医学文献 OA 免费下载与元数据
- **doc-holmes** — 保持排版的 PDF 精准翻译
- 医学知识库：docsor.cn

---

## 版权与许可 (Rights & License)

© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
代码许可 (code license) : MIT（见 LICENSE）。转载/二次分发请保留本署名块与 LICENSE。

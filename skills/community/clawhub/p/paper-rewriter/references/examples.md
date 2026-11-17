> **何时读我**：想先看完整输入输出再动手。
> **最短路径**：照第一个样例跑通再改。
> **回 [INDEX](INDEX.md)**

# 完整输入输出样例（End-to-End Examples）

> 每个样例 = 真实命令 + 真实输出（来自回归语料，可复现）。样例中的数字/事实仅用于演示格式。

## 样例 1：中文改写全流程

**输入** `draft.txt`（节选，模板腔密集）：

```
综上所述，智慧医疗作为一项新兴范式，正在为整个行业赋能。一方面，它能够整合海量医疗数据，为临床决策提供新的思路；另一方面，它还可以优化资源配置，为分级诊疗制度的落地保驾护航。
```

**Step 1 自查**：

```console
$ python scripts/detect.py draft.txt
==============================================================
写作风格特征自查（本地启发式 · 非任何官方检测分数）
==============================================================
文件: draft.txt
语言: 中文 | 规模: 216.5 单元 / 13 句

综合评分: 58/100  [高]
...
改写建议(前10条):
  · 「赋能」→ 「支持 / 帮助 / 为…提供能力」
  · 「抓手」→ 「工具 / 途径 / 切入点」
```

**Step 2 机械清理**（本例无模型残留/客套句，清理近零改动——正常）：

```console
$ python scripts/transform.py draft.txt -o step1.txt
{
  "applied_fixes": {"半角逗号→全角": 2},
  "removed_sentences": [],
  "note": "机械清洗只覆盖语法安全层；黑话/八股/节奏需 agent 按指南深改，..."
}
```

**Step 3 深改**（agent 按 `references/style_guide_zh.md` 七步法执行，改后节选）：

```
智慧医疗的价值集中在两处：把分散的病历、影像和检验数据汇到一起供临床调用，以及让上级医院的诊断能力透过远程会话下沉到基层。前者的瓶颈是数据标准，后者是责任认定——这两点不解决，分级诊疗借不上智慧医疗的力。
```

**Step 4+5 守卫与对比**：

```console
$ python scripts/verify.py draft.txt step2.txt --terms terms.txt
完整性守卫 verify：PASS ✓
  数字/DOI/PMID/缩写/术语 全部保全。

$ python scripts/compare.py draft.txt step2.txt
风格特征分: 58 [高] → 12 [低]  （-46）
完整性守卫: PASS ✓
```

## 样例 2：英文模型残留清理 + 守卫拦截

**输入** `ai_paste.txt`（从聊天窗口粘贴的稿子，带残留与客套句）：

```
综上所述，本研究纳入 128 例患者，其中 68 例进入试验组（p = 0.031）。
值得注意的是，两组基线具有可比性 [cite: 1][cite: 3]，随访 24 个月。
希望以上内容对您有所帮助！如需进一步修改请告诉我。
```

**一键管线**：

```console
$ python scripts/pipeline.py ai_paste.txt -o clean.txt
==============================================================
一键管线报告（机械清理）
==============================================================
风格特征分: 47 [中] → 18 [低]
完整性守卫: PASS ✓
  数字/DOI/PMID/缩写/术语 全部保全。
深改任务简报:
  指南: references/style_guide_zh.md
  · 剩余特征: 学术八股（人写也有，看密度） ×3
  下一步: agent 按 references/style_guide_zh.md 对 clean.txt 做深度改写（保护数字/引用/术语），然后重跑本命令 --rewrite 改稿文件复核
口径: 本地启发式风格特征评分，非任何官方检测分数
```

清理效果：`[cite: 1][cite: 3]` 行内摘除（句子保留）、客套句整句移除、数字 128/68/0.031/24 全部原样。

## 样例 3：完整性守卫拦截演示（守卫不讲价）

```console
$ python scripts/verify.py 原稿.txt 改稿.txt
完整性守卫 verify：FAIL ✗（学术安全红线）
  ✗ [numbers] 数字丢失/被改: 62
  ✗ [comparison] 比较方向/比较数字被改: <0.05
判定: 未通过——请修复改稿后重跑
$ echo $?
1
```

改稿把「血沉 62mm/h」改成 58、把「P<0.05」改成「P>0.05」——无论措辞多流畅，exit 1。修的是改稿，不是守卫。

## 样例 4：术语保护（正当学术用法不误报）

```console
$ python scripts/detect.py -s
The mutational landscape was profiled in this pivotal trial; robust regression confirmed the effect. (×3)
6/低
```

mutational landscape / pivotal trial / robust regression 全部豁免；换成 "the startup landscape ... plays a pivotal role" 这类非学术语境则正常计分。

## 样例 5：markdown 稿件全链路（v2.2.0：章节感知 + 句级计划 + 守卫拦截）

**输入** `case_medical.md`（markdown 医学综述，模板腔密度中等）。v2.2.0 起
`## 摘要`/`## 方法` 等 markdown 标题直接进章节感知，.md 语法残留自动豁免。

**Step 1 自查 + 章节感知**：

```console
$ python scripts/detect.py case_medical.md --structure
章节: 题引 / 摘要 / 引言 / 方法 / 讨论 / 结论（markdown 标题逐一识别）
综合评分: 23/100  [低]
  · 学术八股（人写也有，看密度）      9 处   （综上所述 / 值得注意的是 / 众所周知…）
  · 排比/对仗结构（一方面…另一方面）   1 处
节奏统计: 句长变异系数 0.62 | 连接词 0.41/句
```

**Step 2 改写优先级计划**（v2.2.0 新增，先定位再动手）：

```console
$ python scripts/plan.py case_medical.md --json
P1 [结论] 2.2点  「…从而为临床决策的落地保驾护航。」
P2 [引言] 0.9点  「众所周知，IRAK4在Toll样受体…」
P3 [摘要] 0.8点  「取得了显著进展，为新型治疗策略的开发…」
预算投影: 改完前5句→11 | 前10句→4 | 全部→2   （线性近似，仅供排序）
```

**Step 3 agent 深改**（按 style_guide 改 P0 队列，事实全保留：1/250000、
48 篇、2005-2026、8 例/12 个月）。

**Step 4 守卫拦截过度删减**——第一版深改把 IRAK4 从 12 次引述压到 11 次：

```console
$ python scripts/verify.py case_medical.md case_medical_v2.md
  ✗ [numbers] 数字丢失/被改: 4        ← IRAK4 里的 4 连带丢失
  ✗ [latin_abbr] 大写缩写丢失: IRAK4
判定: 未通过——请修复改稿后重跑（exit 1）
```

补回自然引述（「IRAK4抑制剂的耐药机制」）后重跑：

```console
$ python scripts/verify.py case_medical.md case_medical_v2.md
判定: 通过（exit 0）| 规模 694 → 609 字符

$ python scripts/compare.py case_medical.md case_medical_v2.md
  学术八股          已清除 9 处
  翻译腔/空泛过渡    已清除 4 处
  中文 AI 黑话      已清除 2 处
  排比/对仗结构      已清除 1 处
完整性守卫: PASS ✓
```

**要点**：markdown 章节直接被识别；plan 把深改力气指向贡献最大的句子；
verify 连「缩写次数被压低」都能抓到——守卫拦的是内容损失，不是措辞。

## 样例 6：误报 → 守卫固化（v2.2.0 learn_guards）

「抓手」在词表里是营销黑话，但机械工程语境的「机械抓手」是正当术语——
守卫按上下文豁免，不是整词洗白：

```console
$ echo "装配平台的机械抓手采用气驱动设计，抓取力可调。" | python scripts/detect.py -s
46/中                                  ← 误报

$ python scripts/learn_guards.py add 抓手 --before "机械,装置" --after "采用,夹持"
已保存守卫：抓手（lang=zh，前文 2 项 / 后文 2 项）

$ echo "装配平台的机械抓手采用气驱动设计，抓取力可调。" | python scripts/detect.py -s
0/低                                   ← 机械语境豁免

$ echo "以创新为抓手，全面赋能业务增长。" | python scripts/detect.py -s
35/中                                  ← 营销语境照常计分（对照）
```

守卫存进 `scripts/user_guards.json`（升级词表不丢）；`list` 查看、
`remove 抓手` 撤销、`from-text 术语 样本.txt` 从真实语料自动提取上下文
（中英双语口径）。强制要求 `--before/--after` 上下文——纯词白名单会被拒绝。

## 样例 7：CI/agent 门禁——机器退出码（v2.3.0 --exit-verdict）

把改稿质量卡进自动化流程：改稿不达标就拦截，不需要人读报告。

```console
$ # 坏改稿：改稿=原稿（一句没改），门禁应拦截
$ python scripts/pipeline.py draft.txt --rewrite draft.txt --exit-verdict
$ echo $?
3                                    ← 风格特征中及以上（52/高），进深改队列

$ # 好改稿：事实保留、模板腔清除，门禁放行
$ python scripts/pipeline.py draft.txt --rewrite rewritten.txt --exit-verdict
完整性守卫: PASS ✓
$ echo $?
0

$ # JSON 里的同源字段（agent 管线直接读）
$ python scripts/pipeline.py draft.txt --rewrite draft.txt --json | jq .exit_verdict
3
```

退出码全表（0/1/3/4/2 两套口径）：`references/errors.md` 第一节。
`detect --exit-verdict` / `compare --exit-verdict` 只出 0/3/4——完整性 FAIL
的 exit 1 契约专属 verify.py 与 pipeline。

## 样例 8：确定性深改档（v2.4.0 --deep）+ 处置提示

**输入**（模板腔中文段落）：

```
综上所述，本研究验证了假设。值得注意的是，该方法不仅提升了精度，而且降低了成本。众所周知，数据见第3.2节，p=0.03。
```

**transform --deep（句式级确定性转换，--track 可审计）**：

```console
$ python scripts/transform.py in.txt -o out.txt --deep --track track
深改档: 句首八股删除 ×3
深改档: 排除式连接合并 ×1

$ cat out.txt
本研究验证了假设。该方法提升了精度，且降低了成本。数据见第3.2节，p=0.03。
```

**守卫确认零损失**：

```console
$ python scripts/verify.py in.txt out.txt
  数字/DOI/PMID/缩写/术语 全部保全。
判定: 通过
```

track.md 里每笔深改操作独立可查（`深改档:句首八股删除 ×3`）。
--deep 只做零信息损失操作（删纯套话标记/拆排除式连接）；黑话替换、
节奏重排、立场重写仍由 agent 按指南执行——两层互补，不互相替代。

**处置提示（v2.4.0，报告尾部 + JSON hints 字段）**——非论文文体自动建议切 profile：

```console
$ python scripts/detect.py blog_post.txt
…
处置提示:
  → 深改排序：python scripts/plan.py <文件> -o plan.md 生成句级优先级计划
  → 未识别到论文章节且特征以标点/翻译腔为主——非论文文体（博客/公文/通知）
    可加 --profile general 降权八股信号
```

## 样例 9：集中异常层 + 批量重试 + 单步超时（v2.5.0）

**两行中文错误（错误 + 处置建议）**——所有 CLI 统一格式，非技术用户也能照着做：

```console
$ python scripts/detect.py photo.png
错误: 输入疑似二进制文件（含 NUL 字节）——请转存为 UTF-8 纯文本（.txt/.md）再处理
```

**批量二遍重试**——首遍失败的文件自动以双倍时间预算重扫一次，瞬时故障
（负载抖动导致超时等）第二遍即恢复；真坏文件如实标注"已重试"：

```console
$ python scripts/detect.py --batch ./papers
[重试] 二遍扫描：1 个失败文件重试，0 个恢复
  a.txt                                0/低
  broken.txt                           错误: 输入疑似二进制文件…（已重试 1 次）
```

`--json` 输出逐文件携带 `retried` 字段（true=重试后成功）。

**单步超时与耗时透明**——`--step-timeout`（缺省 120 秒）管住清理与扫描
每一步，超时干净报错；JSON 报告新增 `timings`：

```console
$ python scripts/pipeline.py draft.txt -o out.txt
耗时: 清理 0.0s | 扫描 0.1s | 守卫 0.0s（合计 0.2s，单步预算 120 秒）

$ python scripts/pipeline.py draft.txt -o out.txt --json | jq .timings
{ "cleanup_s": 0.0, "scan_s": 0.11, "verify_s": 0.0, "total_s": 0.11 }
```

## 样例 10：风格画像——深改的量化验收（v2.6.0 stylecheck）

**单文件画像**（AI 语料演示，黑话命中定位到段）：

```console
$ python scripts/stylecheck.py draft.txt
| 指标 | 值 | 档位 |
|---|---|---|
| 黑话密度（每千字） | 36.81 | 偏机器 |
| 句长变异系数 | 0.388 | 自然 |
| 最高频句首占比 | 0.077 | 自然 |
| 最长连续同开场 | 1 | 自然 |

## 重点段落（黑话命中降序）
- 第 1 段（104 字/3 句，命中 4）：赋能 → 支持 / 帮助 / 为…提供能力
- 第 2 段（112 字/4 句，命中 5）：保驾护航 → 保障 / 支持
- 第 4 段（126 字/2 句，命中 5）：抓手 → 工具 / 途径 / 切入点
```

**--compare 验收差值**（AI 语料 → 人写语料的演示对比，深改实际效果介于其间）：

```console
$ python scripts/stylecheck.py 原稿.txt 改稿.txt --compare
| 黑话密度（每千字） | 36.81 | 0.0 | 偏机器 → 自然 |
黑话命中合计：18 → 0（-18）
```

档位阈值用本地语料校准（AI 语料黑话密度 17-37/千字 vs 人写 0），只做验收
提示、不改评分；改稿完整性仍以 verify.py 为准。深改验收闭环：
plan.py 排队列 → agent 按指南改 → --compare 看画像差值 → verify 过守卫。


## 样例 11：--terms auto 与画像 HTML（v2.7.0）

```console
$ python scripts/pipeline.py manuscript.txt -o clean.txt --terms auto
[术语] 术语表=自动草稿 clean.terms.auto.txt（12 条，未经人工确认）——正式稿件建议人工过一遍后重跑

$ python scripts/pipeline.py manuscript.txt -o clean.txt --terms auto --json | jq .terms_note
"术语表=自动草稿 clean.terms.auto.txt（12 条，未经人工确认）——…"

$ python scripts/stylecheck.py clean.txt --html profile.html
HTML 画像报告已写入 profile.html
```

CJK 相邻缩写抽取修复（v2.7.0）：`IRAK4抑制剂` 里的 IRAK4 此前因 \b 在汉字旁
失效而抽不到——与 verify.py v2.1.0 同族问题，本版统一为 CJK 安全 lookaround。

## v3.3/v3.4 新能力速览

### 统计一致性并入管线（--check-stats）

```bash
python scripts/pipeline.py draft.txt -o out.txt --check-stats
# 报告尾部多一节「统计一致性：N 项」（JSON 字段 stats_consistency）；
# 仅提示，不改退出码
```

### 跨文件分组 n 聚合（分章写作数字打架）

```bash
python scripts/check_stats.py --batch 章节目录
# 输出逐文件问题 + 「跨文件聚合」段（摘要 n=120 vs 方法 n=118 类硬伤）；
# 时点差异（随机化 vs 完成随访）标为候选，不计入退出码
```

### 投稿自查包（--bundle，00-11 共 12 个编号件）

```bash
python scripts/pipeline.py draft.txt -o out.txt --bundle 自查材料
# 生成 自查材料/自查包_YYYYMMDD_HHMMSS/：
#   00_写入清单.json 01_风格自查报告.html 02_修订记录.md/.json 03_风格画像对比.md
#   04_统计一致性.md 05_术语一致性.md 06_完整性判定.json 07_问题台账.md
#   08_体检报告.html 09_深改指令单.md 10_前后对照.html 11_守卫处方.html README.txt
```

### verify FAIL 的处方化输出（v3.9.0）

```bash
python scripts/verify.py 原稿.txt 改稿.txt
#   ✗ [numbers] 数字丢失/被改: 120, 24
#       原句锚点: 研究纳入 120 例患者，随访 24 个月。
#       怎么修: 把上述原句里的数字/统计量原样恢复进改稿对应位置（学术红线，不可放宽口径绕过）
#   判定: 未通过——请修复改稿后重跑
#   修复三步: ①按「怎么修」逐条恢复（术语误伤用 learn_guards.py 固化豁免）
#             ②重跑至 PASS ③交付前再跑 compare.py 留档
# --json 时报告带 remedies 字段（agent/CI 可程序化消费）

### 分块扫描降级（v3.9.0）

```bash
python scripts/detect.py 超大文本.txt
# stderr: [降级] 1 块超时未评分（2× 预算重试未恢复），该行分数仅覆盖部分正文（detect）
#         [降级] 分块 800000–1600000 字符超时未评分…（pipeline）；行内带 ⚠[降级:N 块] 标记
# JSON: degraded_chunks:[{start,end,chars,retried}]；--exit-verdict 对降级 exit 2
```

### 一句命令出深改指令单（v3.8.0 pipeline --handoff）

```bash
python scripts/pipeline.py draft.txt -o out.txt --handoff 交接块.md
# 报告照常输出之外，另得逐句指令单（plan --handoff 同款）：
#   1. [摘要] 众所周知，本研究具有重要意义。
#      操作：模板结构：删仪式感开场/拆投票式列举（指南第 1 步）；翻译腔：改为直接陈述
#   深改 agent 照单执行，每 3-5 句跑一次 verify——省去单独跑 plan 一步
```

### 批量断点续传（v3.7.0 --resume）

```bash
python scripts/detect.py --batch 全部章节/            # 中途 Ctrl+C / 断电
python scripts/detect.py --batch 全部章节/ --resume   # 跳过已完成，只补没跑的
# stderr 提示: [续传] 跳过 N 个已完成文件（进度 .pr_batch_state.json；…）
# 规则：文件未变（大小+修改时间）→ 复用结果；变更过/上次失败 → 自动重跑
# detect 与 pipeline 进度互不干扰（同目录各认各的记录）；删 .pr_batch_state.json = 重置
```

### 跨文件术语漂移（v3.7.0 check_terms --batch）

```bash
python scripts/check_terms.py --batch 全部章节/
# 发现 1 组跨文件变体漂移：
#   [通用] 摘要.txt→患者 / 讨论.txt→病人 → 建议「患者」
# exit 1=有漂移或文件内不一致；--report 出逐文件明细；--json 出机器口径
# 场景：多章节论文各章分头改写后，「各章内部一致、合起来不一致」的术语病
```

### v4.4.0 新能力速览：docx 回写闭环 + 术语统一稿

```bash
# ① Word 工作流闭环：docx 直读 → 机械清理 → 回写 .docx（纯段落）
python scripts/pipeline.py draft.docx -o 改稿.docx
# 输出路径以 .docx 结尾即回写 Word（transform/compare -o 同样生效）
# 诚实边界：只回写段落文本——表格/图片/样式不重建，复杂格式人工合并

# ② 术语统一稿：检查报告 → 一键统一（建议产物，复核后采用）
python scripts/check_terms.py 稿件.txt --unify 统一稿.txt
# 统一稿已写入 统一稿.txt（2 组术语 / 共 5 处替换）：
#   心力衰竭 → 心衰（4 处）
#   病人 → 患者（1 处）
# 提示：统一稿是建议产物——逐处复核清单后再采用；
#       随后建议跑 verify.py 确认数字与引用完整性。
# 输出路径以 .docx 结尾同样回写 Word；已一致时不生成文件、exit 0
```

### v4.5.0 新能力速览：EN 2026 特征 + 章节专项 + 统一稿头清单

```bash
# ① 章节专项：审稿人第一眼重点节独立诊断（全文总分跑不带 --section 的 detect）
python scripts/detect.py thesis.txt --section abstract
python scripts/detect.py thesis.txt --section conclusion
# 分数: 32 [中]  （本节独立评分；全文诊断跑不带 --section 的 detect）
#   - [结构性对冲/框架化短语] It is important to note that ...

# ② EN 2026 特征（自动生效，无需参数）：em-dash 密度过载 / 段落开头副词
#    均匀化 / 结构性对冲（It is important to note that…）/ 三连同构
#    （engaging, rewarding, and lasting）/ profound 等词带医学语境守卫

# ③ 统一稿头清单：打开统一稿第一屏就是替换清单（复核零切换）
python scripts/check_terms.py 稿件.txt --unify 统一稿.txt
# 稿件头部自动注入：
# ════ 术语统一稿 · 复核后删除本块 ════
#   病人 → 患者（1 处）
#   共 1 组 / 1 处替换
# 头块自带「复核后删除本块再跑 verify」——删块后再跑 verify（否则头块
# 数字/行会被守卫按新增内容告警）
# .md 稿用 HTML 注释（渲染不可见）；.docx 不注入；--no-header 关闭
```

### v4.6.0 新能力速览：中文密度镜像 + compare 大文件分块

```bash
# ① 中文密度特征自动生效（无需参数）：「——」连接滥用、段落开头公式化
#    随着深度学习的发展，……（×多段）→ 报告出现「段落开头公式化」
#    结果显著——且安全性良好——…… → 报告出现「——连接滥用」
#    校准哲学与 EN 侧一致：阈值以下属正常修辞，不扣分
#    阈值以上若属文体正当（人文随笔高频破折号/综述引言公式开场），
#    报告样本自带实测密度与逐处位置——人工复核后按指南取舍；
#    非学术文本加 --profile general 可降低八股/公文类信号权重

# ② compare 大文件：超过 100 万字符自动分块扫描（不再单遍硬超时）
python scripts/compare.py 原稿_全本.txt 改稿_全本.txt
# ⚠[降级] 大文件分块扫描中 1 个块超时被标记降级——对比基于部分覆盖，
# 请人工抽查未覆盖段落
# --exit-verdict 下有降级块时 exit 2（部分覆盖不判干净）
```

### v4.7.0 新能力速览：特征可解释层 + general 降权矩阵

```bash
# ① 每个命中类带「依据」——为什么报我，一眼可查
python scripts/detect.py draft.txt
#   · AI vocabulary                   5 处
#       依据: 空洞拔高名词族（主导族，命中 3 处）：tapestry/testament/realm 类
#             抽象大词缺乏信息增量，模型用它替代具体陈述
#       - testament → 直接给可核对的证据
# --json 的 categories 每类自动带 rationale 字段（程序化消费同口径）

# ② 非学术文本的机制级出路：--profile general 下密度/结构信号整体降权
python scripts/detect.py 公众号文章.txt --profile general
# 八股/公文/密度/段落结构类信号 ×0.4（v4.7.0 起覆盖全部密度信号）
```

### v4.8.0 新能力速览：批量工作单 + HTML 统计卡 + general 矩阵扩全

```bash
# ① 批量「改哪里」清单：≥中 档文件逐个详扫，top 命中带依据
python scripts/detect.py --batch 全部章节/ --suggestions 要改清单.md
# # 批量修订建议工作单：全部章节/
# # > 3 个文件 · ≥中 档 1 个进入清单
# ## a.txt（64 [高]）
# - **学术八股** ×4
#   依据: 学术八股套语——人写也有，密度是关键……
#   - 综上所述

# ② 批量 HTML 汇总带统计卡（降级/失败不再只藏在 stderr）
python scripts/detect.py --batch 目录/ --html 汇总.html
# 统计：扫描 3 · ≥中 1 · ≥高 1 · ⚠残留 0 · 失败/降级 0

# ③ --profile general 矩阵扩全：八组结构信号全部 ×0.4（v4.7 宣称的代码补全）
```

### v4.9.0 新能力速览：命中行号定位

```bash
python scripts/detect.py 论文.txt
# 分类明细:
#   · 中文 AI 黑话                        2 处
#       - L3: 赋能 → 支持 / 帮助 / 为…提供能力
#       - L3: 闭环 → 完整流程 / 形成回路（工程语境豁免）
#   · 学术八股（人写也有，看密度）        2 处
#       - L2: 综上所述
# 直接跳到原文第 3 行改——「找得到改哪里」的最后一公里。
# 大文件分块扫描的行号同样对齐原文（>1MB 也直接定位）；工作单/JSON 同口径。
```

### v5.0.0 新能力速览：投稿自查包 2.0（体检报告 dashboard）+ CN 特征库 v2

```bash
python scripts/pipeline.py 原稿.txt --rewrite 改稿.txt --bundle 自查材料/
# 自查包_时间戳/ 新增 08_体检报告.html：单页聚合总览
#   分数卡（改前→改后 + Δ + 完整性判定）
#   命中明细（L 行号定位 + 每类依据原生折叠，零 JS 离线可读）
#   术语一致性 / 统计一致性 / 问题台账 三面板
# README.txt 已记载 08 说明。

# CN 特征库 v2（自动生效）：路线图公式（本文余下部分将组织如下：首先…）/
# 不难看出、归根结底、究其原因族 +12 词——零参数
```

### v5.1.0 新能力速览：指令单行号锚 + EN v2 镜像 + 计数对账

```bash
python scripts/pipeline.py 原稿.txt -o 改稿.txt --handoff 交接块.md
# 深改交接块每句带原文行号——执行改写的 agent 零定位成本：
# 1. [结论]（原文 L23 行） 综上所述，本文具有重要意义。
#    操作：模板结构：删仪式感开场/拆投票式列举（指南第 1 步）

# EN 特征库 v2 镜像（自动生效）：en_roadmap 结构预告组 /
# shed light on、a plethora of、at the forefront of 等 +12 句式族

# 文档计数对账：python tests/check_doc_counts.py（电池内置）
# pitfalls 条数/术语组数/套件数/双语版本不同步 = FAIL
```

### v5.2.0 新能力速览：体检报告行动清单 + 口径统一



### v5.3.0 新能力速览：bundle 深改指令单 + 批量修订记录

```bash
# ① 自查包自包含「改哪里+怎么改」：08 行动清单 + 09 指令单（每句带原文行号）
python scripts/pipeline.py 原稿.txt --rewrite 改稿.txt --bundle 自查材料/
# 自查包_时间戳/09_深改指令单.md：
# 1. [结论]（原文 L23 行） 综上所述，本文具有重要意义。
#    操作：模板结构：删仪式感开场/拆投票式列举（指南第 1 步）

# ② 批量改写可审计：--batch --track 逐文件修订记录
python scripts/pipeline.py --batch 全部章节/ --track 修订记录/
# [批量修订记录] 2 个文件 → 修订记录/（transform 同款口径）
#   base_a.md base_a.json base_b.md base_b.json
```

### v5.4.0 新能力速览：写入清单自证

```bash
python scripts/pipeline.py 原稿.txt --rewrite 改稿.txt --bundle 自查材料/
# 自查包_时间戳/ 新增 00_写入清单.json：本次运行全部写入路径的实测工件
#   {"generated_by": "pipeline --bundle", "writes": [...12 项...]}
#   00_写入清单.json（清单自身）01 风格自查报告 … 09 深改指令单 README
# permissions.md 的「写什么」声明随包可验——权限不再只是文档承诺。
```

### v5.5.0 新能力速览：对照报告行号 + 打印友好

```bash
python scripts/compare.py 原稿.txt 改稿.txt --html 对照.html
# 逐句 diff 每行带「L原文→L改稿」锚列：
#   同 L1→L1
#   改 L2→L2  <del>综上所述，本文具有重要意义。</del> <ins>直接给出结论…</ins>
# 改稿命中明细带依据折叠（与 detect/体检报告同口径）。
# 全部 HTML 报告内置 @media print——浏览器打印即交付级排版（卡片防断页）。
```

### v5.6.0 新能力速览：守卫库共享 + bundle 前后对照

```bash
# ① 守卫库导出/导入（多项目/多机共享，术语级去重合并）
python scripts/learn_guards.py export 守卫库.json
python scripts/learn_guards.py import 守卫库.json --dry-run   # 先预览
python scripts/learn_guards.py import 守卫库.json             # 新术语追加

# ② 自查包新增 10_前后对照.html（render_compare 直出：L 行号锚+依据节）
python scripts/pipeline.py 原稿.txt --rewrite 改稿.txt --bundle 自查材料/
# 自查包 00-11 共 12 件
```

### v5.7.0 新能力速览：守卫处方报告 + 口径大扫除

```bash
python scripts/verify.py 原稿.txt 改稿.txt --html 守卫报告.html
# PASS：简洁通过卡（数字/DOI/术语 全部保全）
# FAIL：单页处方——违规类别+原句锚点+怎么修+修复三步，打印即可发给协助者
#（复用 reporter 打印友好样式；exit 0 才算过）
```

> **何时读我**：场景对号入座（期刊投稿/学位论文/ESL/审稿回复…）。
> **最短路径**：找你的场景节，照该节命令序列。
> **回 [INDEX](INDEX.md)**

# 最佳实践手册（Best Practices）——按场景组织的端到端工作法

> 与 pitfalls.md（错误用法清单，条数以该文件为准）互补：这份手册按**真实场景**组织，每个场景给
> 标准命令序列、预期输出形态、该场景特有的避坑点。所有分数与档位均为本地
> 启发式口径，非任何外部检测分数。

## 场景 1：期刊投稿前的自查（最常见）

**目标**：投稿前把模板腔降下来，同时确保一个数据都没动。

```bash
# 1. 术语表先行（医学/生科稿件必做——守卫的弹药）
python scripts/extract_terms.py manuscript.txt -o terms.txt
#   人工过一遍 terms.txt：删掉普通词、补上缩写变体（如 Myc 与 MYC 都要）

# 2. 一键管线出底稿
python scripts/pipeline.py manuscript.txt -o clean.txt --terms terms.txt

# 3. agent 深改（按 style_guide_zh/en 七步法，重点看 plan 排出的 P0 句）
python scripts/plan.py clean.txt -o plan.md        # 句级优先级队列+预算投影
#   ……按 plan.md 逐句深改，产出 revised.txt……

# 4. 量化验收（改前 vs 改后画像差值）
python scripts/stylecheck.py clean.txt revised.txt --compare

# 5. 守卫+复核（铁闸：exit 0 才算过）
python scripts/verify.py manuscript.txt revised.txt --terms terms.txt
python scripts/compare.py manuscript.txt revised.txt
```

**本场景避坑**：改稿时最常见的 FAIL 是缩写次数被压低（如 IRAK4 从 12 次
引述删到 11 次）——守卫连「缩写出现次数」都守；这不是误报，把引述补回自然
位置即可。投稿版务必保留 AI 使用披露（如期刊要求）——本报告不能替代披露。

## 场景 2：学位论文（长文档、分章处理）

**目标**：几万字的论文不塞给单次扫描——按章处理，报告才可读。

```bash
# 长文先看结构
python scripts/detect.py thesis.md --structure
# 按章拆分后逐章走场景 1 流程；方法/结果章的固定句式会被自动降权，
# 不要因为「方法章分数高」就回去改方法章的表述——那是文体常态。
```

**本场景避坑**：学位论文的摘要常是「结构式摘要」（目的/方法/结果/结论带
冒号标签）——冒号后带内容的行不会被误判为章节标题，放心。中文摘要与
英文 Abstract 分开处理，语言口径各自更准。

## 场景 3：回复审稿人（revision letter）

**目标**：response letter 语气自然、逐条回应，但**引用的审稿意见原文一字不能动**。

```bash
# 只对"自己的回应"部分跑管线；审稿意见原文用手动引用块隔开
python scripts/pipeline.py my_response.txt -o clean.txt --terms terms.txt
```

**本场景避坑**：response letter 里复制粘贴的审稿意见会被当作改写对象——
把原文放进引用块（> 前缀）并在深改时跳过；verify 的数字守卫会拦住大部分
误伤（审稿意见里的数据句被动过会 exit 1），但别依赖守卫兜底，先分好区域。

## 场景 4：批量处理（课题组/编辑部）

**目标**：一个目录的稿件先摸底再逐篇精修。

```bash
# 摸底：全目录扫描（JSON 便于汇总）
python scripts/detect.py --batch ./submissions --json > overview.json
# 逐篇精修只挑高分的；批量清理用 pipeline --batch 出 CSV 台账
python scripts/pipeline.py --batch ./submissions -o batch_report.csv
```

**本场景避坑**：批量模式不生成 --html/--track/--suggestions（见输出提示）；
需要报告的稿子单跑。批量二遍重试会自动救回瞬时失败的文件
（detect --batch --json 的 retried 字段；pipeline 的 CSV 在 integrity 列标注
「已重试 1 次」），两遍都失败的文件如实标注，人工看一眼即可。

## 场景 5：CI/agent 门禁（自动化集成）

**目标**：改稿质量卡进自动化流程，机器判定不达标就拦截。

```bash
# 全档门禁（0=干净 1=完整性 FAIL 3=需深改 4=模型残留）
python scripts/pipeline.py orig.txt --rewrite new.txt --terms terms.txt --exit-verdict
# JSON 里拿同源字段
python scripts/pipeline.py orig.txt --rewrite new.txt --json | jq .exit_verdict
```

**本场景避坑**：批量 + `--exit-verdict` 是 fail-closed——目录里有扫描失败的
文件门禁不予放行：错误文件贡献退出码 2，最终退出码取各文件最坏值（可为
2/3/4），必为非零（宁可拦错不可放错；CI 断言请用「非 0」而非「==2」）。预算投影（plan.py）是线性
近似，只用于排序，不要写进 CI 断言。

## 场景 6：误报治理（领域术语被误判）

**目标**：正当术语不再每次都被计分，且升级词表不丢。

```bash
# 从真实语料提取上下文固化守卫（中英双语口径）
python scripts/learn_guards.py from-text 抓手 机械样本.txt
python scripts/learn_guards.py add 抓手 --before "机械,装置" --after "采用,夹持"
python scripts/learn_guards.py test "装配平台的机械抓手采用气驱动设计。"
```

**本场景避坑**：守卫是上下文豁免不是整词洗白（营销语境的「抓手」照常计分）；
守卫存 `scripts/user_guards.json`，升级词表不丢。给 agent 的术语守卫固化
后，把 `learn_guards.py list` 的输出贴进稿件交接说明，团队共享口径。

## 场景 7：中文投稿的标点与格式

**目标**：半角标点/Markdown 残留一次清干净，不误伤小数和文献著录。

```bash
python scripts/transform.py draft.txt -o step1.txt    # 标点全角化（小数保护）
python scripts/verify.py draft.txt step1.txt           # 确认文献行未被误改
```

**本场景避坑**：参考文献行的半角标点是著录规范（已豁免不检测）；`3.14` 这类
小数点受保护；中文输入法把 `2025` 打成 `２０２５` 会被 verify 以 E_NUM_WIDTH
拦截——transform 已自动归一为半角（--track 记为「全角字母数字归一」）；`--deep` 深改档只删零信息损失成分（句首八股/排除式连接），
黑话与节奏仍要按指南深改——两层互补不互相替代。

---

**通用收尾三连**（所有场景通用）：

```bash
python scripts/verify.py 原稿 新稿 --terms terms.txt   # exit 0 才算过
python scripts/compare.py 原稿 新稿                     # 特征下降+完整性
python scripts/stylecheck.py 原稿 新稿 --compare        # 画像差值
```

如学校/期刊要求 AI 使用披露，请如实声明——本工具箱是质量自查记录，
不能替代披露。

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

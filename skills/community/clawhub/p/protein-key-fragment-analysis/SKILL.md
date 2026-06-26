---
name: protein-key-fragment-analysis
description: 蛋白质关键序列片段预测分析。对任意蛋白质家族的多物种FASTA序列执行完整分析流程，提取共识序列并识别关键功能片段、统计氨基酸组成、预测片段主要功能。适用于：（1）用户提到"提取蛋白关键序列/片段"、"分析蛋白保守区"、"预测蛋白功能片段"时，（2）对新物种/类群运行完整分析流程，（3）从已有FASTA序列提取共识序列并识别关键片段，（4）跨物种横向对比关键片段差异，（5）生成结构化分析报告。适用于任何蛋白质家族。
---

# 蛋白质关键序列片段预测分析

> 本流程适用于**任何蛋白质家族**，对多物种 FASTA 序列执行 MSA → 共识序列 → 关键片段识别 → 氨基酸组成统计 → 功能预测的完整分析链路。

## 核心文件

- **主分析脚本**：`scripts/protein_key_fragment_analysis.py`（完整分析流程）
- **批量运行入口**：`scripts/run_full_analysis.py`（多物种批量 + 大样本采样）
- **方法细节**：`references/method.md`
- **功能域参考**：`references/functional_domains.md`（分析新蛋白家族时，在此补充对应 Pfam 保守域）

---

## 快速运行

```bash
# 单物种分析
python3 protein_key_fragment_analysis.py <物种名> <fasta路径>

# 多物种批量分析（推荐）
# 1. 将各物种 .fasta 文件放入 input_clean/ 目录
# 2. 运行批量脚本
python3 run_full_analysis.py
```

---

## 分析流程

### Step 1：序列读取
- 解析标准 FASTA 格式，统计序列数量和长度分布
- **大样本处理**：序列数超过阈值时随机采样（seed=42，保证可复现）

### Step 2：多序列比对（MSA）
- 工具：**ClustalOmega**（`apt install clustalo` 或 `conda install clustalo`）
- 单序列物种跳过 MSA，直接使用原始序列

### Step 3：共识序列提取
- 各位点最高频氨基酸占比 ≥ 阈值（默认 0.5）则写入，否则标 X
- 去除 gap（`-`）后得到连续共识序列

**共识序列生成原理**：
```
MSA比对结果（多序列对齐）
位置:  1 2 3 4 5 ...
Seq1:  M K H L P ...
Seq2:  M K H L P ...
Seq3:  M K H L A ...
      ↓ 统计频率
位置1: M(100%) → 写入 M
位置5: P(67%), A(33%) → 写入 P（若阈值≤67%）或 X（若阈值>67%）
```

**关键参数**：
- 共识序列提取阈值：50%（默认）
- 关键片段识别阈值：90%（推荐，见下文调整阈值部分）

### Step 4：关键片段识别（三维度并行）
1. **已知功能块匹配**：在共识序列中搜索目标蛋白家族的 Pfam 保守域特征序列（需在 `functional_domains.md` 中预先配置）
2. **高保守连续区检测**：保守率 ≥ 90%、长度 ≥ 6aa 的连续区段
3. **保守 Cys 检测**：统计共识序列中 Cys 数量（潜在二硫键网络）

> 分析新蛋白家族时，在 `KNOWN_MOTIFS` 和 `CONSERVED_BLOCKS` 中补充对应的 Pfam 特征序列（来源：Pfam / InterPro / UniProt）。

### Step 4.5：片段氨基酸组成与理化性质分析

对每个关键片段统计各功能类别氨基酸的出现频率：

| 类别 | 氨基酸 |
|------|--------|
| Hydrophobic（疏水性） | V, L, I, M |
| Nucleophilic（亲核性） | S, T, C |
| Aromatic（芳香性） | F, Y, W |
| Amide（酰胺类） | N, Q |
| Acidic（酸性） | D, E |
| Cationic（阳离子性） | H, K, R |
| **排除不统计** | X, A, G, P |

> ⚠️ 此分类体系与 `aa-pair-analysis` 完全一致，A/G/P 排除不统计。

- **主导类别判定**：某类别占比 ≥ 35% 则为该类主导，否则判定为 Mixed（混合型）
- 结果写入 `composition` 字段（含各类别计数、比例、主导类别、理化性质描述）

### Step 5：基于氨基酸组成的功能预测

根据各类别比例按优先级推断主要功能，结果写入 `function_prediction` 字段：

| 优先级 | 判断条件 | 功能预测 |
|--------|---------|---------|
| 1 | Pfam 已知功能块命中 | 🔴 已知功能位点——高度保守催化/结合区域 |
| 2 | Cys 在片段中占比 ≥ 12% | 🟡 二硫键网络/结构骨架 |
| 3 | Nucleophilic ≥ 40% | 🟢 催化活性位点/磷酸化调控区（Ser/Thr/Cys核心） |
| 4 | Hydrophobic ≥ 45% | ⬛ 疏水折叠核心/跨膜区 |
| 5 | Aromatic ≥ 20% | 🟣 底物识别/π-π堆叠区 |
| 6 | Cationic ≥ 35% | ⚡ 正电荷底物结合区 |
| 7 | Acidic ≥ 35% | 🔵 金属离子螯合/催化酸基区 |
| 8 | Nucleophilic ≥ 25% + Cationic ≥ 15% | 🔵 亲核-阳离子协作底物识别区 |
| 9 | Hydrophobic ≥ 25% + Nucleophilic ≥ 25% | ⬛ 两亲性蛋白-蛋白相互作用界面 |
| 10 | Acidic ≥ 20% + Cationic ≥ 20% | ⚡ 电荷互补区（盐桥网络/静电引导） |
| 11 | Amide ≥ 20% | 🔵 酰胺富集区（氢键网络/糖基化位点） |
| 12 | 以上均不满足 | 🔵 混合型功能区（Linker/多功能结合界面） |

### Step 6：生成报告
- 每物种：`_分析报告.md` + `_key_fragments.json`（含 `composition` 和 `function_prediction` 字段）
- 全物种：`汇总分析报告_含功能预测.md`

---

## 输出文件结构

### 推荐目录结构（按物种整合模式）

```
analysis_results/
├── 分类名_按物种整合/
│   ├── 物种名/
│   │   ├── 氨基酸对分析/
│   │   │   ├── formulation.json       # 配方数据
│   │   │   ├── formulation.txt        # 人类可读配方
│   │   │   └── top5_details.json      # Top5对型详情
│   │   ├── 关键片段预测/
│   │   │   ├── *_consensus.fasta      # 共识序列
│   │   │   ├── *_key_fragments.json   # 关键片段数据
│   │   │   └── *_分析报告.md          # 片段分析报告
│   │   └── 物种综合分析报告.md         # 完整综合分析报告
│   └── 物种B/
│       └── ...
├── _所有物种配方总览.md                # 所有物种配方汇总
└── _所有物种配方总览.csv               # CSV格式汇总
```

**优势**：
- 每个物种的数据独立完整，便于查阅
- 支持跨物种横向对比
- 便于后续分析调用

### 旧版结构（已弃用）

```
results/
├── Species_A/
│   ├── Species_A_aligned.fasta
│   ├── Species_A_consensus.fasta
│   ├── Species_A_key_fragments.json
│   └── Species_A_分析报告.md
└── ...
```

---

## 自定义配置

### 添加新蛋白家族的功能域

编辑 `scripts/protein_key_fragment_analysis.py`：

```python
KNOWN_MOTIFS = {
    # 你的蛋白家族特征序列
    "你的功能域名称": {
        "pattern": ["序列模式"],
        "context_note": "描述",
        "function": "功能说明",
        "criticality": "重要性级别"
    }
}
```

### 调整保守性阈值

**关键片段识别阈值**（推荐）：
```python
# 严格模式（推荐用于核心功能位点识别）
# 连续区域保守率 ≥ 90%，长度 ≥ 6aa
# 结果更精细，片段更短但保守性更高

# 宽松模式（默认）
# 连续区域保守率 ≥ 50%，长度 ≥ 6aa
# 结果片段更长，但可能包含保守性较低的区域
```

> **实践建议**：
> - 研究核心功能位点 → 使用 **90%阈值**
> - 初步筛选保守区域 → 使用 **50%阈值**
> - 不同阈值会导致完全不同的生物学解释，需根据研究目的选择

**命令行调整**：
```python
python3 protein_key_fragment_analysis.py <物种> <fasta> --threshold 0.9
```

---

## 依赖安装

```bash
# Ubuntu/Debian
sudo apt install clustalo

# 或 conda
conda install -c bioconda clustalo
```

---

## 数据独立性检查清单

**⚠️ 重要：多分类分析时必须验证数据独立性**

当对同一批数据的不同分类（如阳离子-pi、贻贝粘附蛋白）进行分析时：

- [ ] 每个分类使用独立的FASTA源文件
- [ ] MSA缓存目录分开（`shared_alignments_分类名`）
- [ ] 物种列表无重叠（除非确实为同物种）
- [ ] 配方数据无重复
- [ ] 共识序列和关键片段分别提取

**常见问题**：
不同分类错误地共享了相同的氨基酸对分析CSV数据，导致结果不可靠。

**验证方法**：
```bash
# 检查MSA缓存独立性
ls shared_alignments_分类A/
ls shared_alignments_分类B/
# 应无相同文件名（同物种名除外）

# 检查配方独立性
# 对比不同分类的 species_formulations.csv
# 同物种的配方应不同（若数据来源不同）
```

---

## 与 aa-pair-analysis 的关系

| 维度 | aa-pair-analysis | protein-key-fragment-analysis（本工具） |
|------|------------------|--------------------------------------|
| **关注点** | 氨基酸类别组合统计规律 | 具体序列片段的结构/功能 |
| **输出** | φ值、Top5对型排名 | 片段序列、位置、功能注释 |
| **配合** | 可作为本工具的前置输入 | 需先进行 MSA 获取共识序列 |

**联合分析推荐流程**：
```bash
# 1. 先用 aa-pair-analysis 进行统计筛选
# 2. 再用本工具进行详细功能片段分析
python3 run_combined_analysis.py <任务名> <FASTA目录>

# 3. 生成物种综合分析报告（包含完整共识序列）
python3 integrate_species_results.py
```

---

## 物种综合分析报告

### 报告内容

每个物种生成 `物种综合分析报告.md`，包含：

1. **氨基酸对频率分析**
   - 总对数、配方
   - 各类别φ值分布
   - Top 5氨基酸对详情

2. **共识序列（Consensus Sequence）**
   - 完整FASTA格式序列
   - 每行60个氨基酸
   - 氨基酸组成统计

3. **关键功能片段预测**
   - 高保守片段列表（90%阈值）
   - 每个片段的序列、位置、保守率
   - 保守半胱氨酸位置

### 生成命令

```bash
# 批量生成所有物种的综合分析报告
python3 generate_species_reports.py \
  --input-base analysis_results/ \
  --output-dir 整合分析结果/
```

---
name: protein-mining
description: 自动化蛋白质挖掘完整流程，从文献调研到潜在蛋白确定，生成可发表的学术成果
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["mafft", "hmmbuild", "iqtree"]
        },
        "install": []
      },
    "version": "1.0.0",
    "author": "Computational Biology Lab",
    "category": "Computational Biology / Bioinformatics"
  }
---

# Protein Mining Skill - 蛋白质挖掘自动化流程

本skill实现了系统化的蛋白质挖掘工作流，包含7个核心模块，每个模块产生可交付的实验结果和可视化图表，适用于高质量学术论文发表。

---

## Module 1: Literature Survey & Target Identification
**模块1：文献调研与靶标确定**

### Objectives
- 系统性文献检索与分析
- 确定研究靶标蛋白家族
- 建立研究假设和科学问题

### Workflow
1. **文献数据库检索**
 - PubMed/Google Scholar关键词搜索
 - 检索策略：蛋白家族名 + 功能 + 物种
 - 时间范围：近10年高影响因子文献优先

2. **文献筛选与分析**
 - 提取关键蛋白序列信息
 - 总结已知功能域和保守位点
 - 识别研究空白和创新点

3. **靶标蛋白确定**
 - 选择代表性种子序列（seed sequences）
 - 记录UniProt/NCBI登录号
 - 确定研究物种范围

### Deliverables
- `01_literature_review.pdf` - 文献综述报告
- `01_target_proteins.csv` - 靶标蛋白列表（含登录号、物种、功能注释）
- `01_research_hypothesis.md` - 研究假设和科学问题陈述

---

## Module 2: Protein Sequence Collection
**模块2：蛋白序列收集**

### Objectives
- 从公共数据库获取目标蛋白序列
- 序列质量控制和去冗余
- 构建初始序列数据集

### Deliverables
- `02_raw_sequences.fasta` - 原始序列集
- `02_filtered_sequences.fasta` - 质控后序列集
- `02_nr_sequences.fasta` - 非冗余序列集
- `02_sequence_statistics.csv` - 序列统计信息
- `02_length_distribution.png` - 序列长度分布图

---

## Module 3: HMM Profile Construction
**模块3：隐马尔可夫模型构建**

### Objectives
- 构建蛋白家族特异性HMM模型
- 验证模型敏感性和特异性
- 优化模型参数

### Deliverables
- `03_msa_alignment.fasta` - 多序列比对结果
- `03_protein_family.hmm` - HMM模型文件
- `03_model_validation.csv` - 模型验证统计
- `03_roc_curve.png` - ROC曲线图

---

## Module 4: Cross-Species Sequence Search
**模块4：跨物种序列搜索**

### Objectives
- 使用HMM模型进行全基因组搜索
- 跨物种同源蛋白识别
- 构建候选蛋白数据集

### Deliverables
- `04_hmm_search_results.tbl` - HMM搜索原始结果
- `04_candidate_proteins.fasta` - 候选蛋白序列
- `04_species_distribution.csv` - 物种分布统计
- `04_species_heatmap.png` - 物种分布热图

---

## Module 5: Structure-Based Search (Foldseek)
**模块5：基于结构的搜索**

### Objectives
- 利用AlphaFold2预测结构
- Foldseek结构相似性搜索
- 识别远程同源蛋白

### Deliverables
- `05_predicted_structures/` - AlphaFold2预测结构
- `05_plddt_scores.csv` - 结构置信度评分
- `05_foldseek_results.m8` - Foldseek搜索结果

---

## Module 6: Phylogenetic Analysis
**模块6：进化树构建与分析**

### Objectives
- 构建高质量系统发育树
- 进化关系分析
- 功能分化预测

### Deliverables
- `06_refined_alignment.fasta` - 优化后的多序列比对
- `06_phylogenetic_tree.nwk` - Newick格式进化树
- `06_tree_visualization.pdf` - 高质量进化树图
- `06_positive_selection_sites.csv` - 正选择位点

---

## Module 7: Candidate Protein Prioritization
**模块7：候选蛋白优先级排序**

### Objectives
- 整合多维度数据
- 候选蛋白评分与排序
- 确定高优先级实验验证靶标

### Deliverables
- `07_feature_matrix.csv` - 候选蛋白特征矩阵
- `07_scoring_results.csv` - 综合评分结果
- `07_top_candidates.csv` - Top 20候选蛋白列表
- `07_experimental_design.md` - 实验验证方案建议

---

## Technical Requirements

### Software Dependencies
- HMMER 3.3+, MAFFT 7.0+, CD-HIT 4.8+, TrimAl 1.4+
- IQ-TREE 2.0+, PAML 4.9+, CAFE 5.0+
- AlphaFold2 / ColabFold, Foldseek 8.0+, PyMOL 2.5+
- Biopython 1.79+, pandas, numpy, scipy, matplotlib, seaborn, scikit-learn

### Computational Resources
- CPU: ≥16核心（推荐32核心）
- RAM: ≥64GB（推荐128GB）
- GPU: 用于AlphaFold2结构预测（推荐NVIDIA A100/V100）

---

## Usage

```bash
# 启动完整流程
protein-mining --target "ABC transporter" --species plants

# 分步执行
protein-mining --module 1 --target "ABC transporter"
```

---

## Citation

- HMMER: Eddy SR. (2011) PLoS Comput Biol.
- IQ-TREE: Nguyen et al. (2015) Mol Biol Evol.
- AlphaFold2: Jumper et al. (2021) Nature.
- Foldseek: van Kempen et al. (2023) Nat Biotechnol.

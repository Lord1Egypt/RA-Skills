# 蛋白质关键片段预测分析报告

**物种/类群：** Bacillus toyonensis  
**分析日期：** 2026-03-19 12:23  
**输入序列数：** 10  
**共识序列长度：** 413 aa  
**共识序列保守率：** 100.0%（阈值≥0.5）  

---

## 1. 共识序列

```
   1 MDHLKRQDEKVFAAIEAELGRQRSKIELIASENFVSEAVMEAQGSVLTNKYAEGYPGKRY
  61 YGGCEHVDVVEDIARDRVKEIFGAEHVNVQPHSGAQANMAVYFTILEQGDTVLGMNLSHG
 121 GHLTHGSPVNFSGVQYNFVEYGVDADSHRINYDDVLAKAKEHKPKLIVAGASAYPRVIDF
 181 KRFREIADEVGAYLMVDMAHIAGLVAAGLHPNPVPHAHFVTTTTHKTLRGPRGGMILCEE
 241 QFAKQIDKSIFPGIQGGPLMHVIAAKAVAFGEVLQDDFKTYAQNIINNANRLAEGLQKEG
 301 LTLVSGGTDNHLILIDVRNLEITGKVAEHVLDEVGITVNKNTIPFETASPFVTSGVRIGT
 361 AAVTSRGFGLEDMDEIAALIAYTLKNHENEAALEEARKRVEALTSKFPMYTDL
```

---

## 2. 关键功能片段

### 🔵 高保守连续区_1_413

| 属性 | 内容 |
|------|------|
| **片段序列** | `MDHLKRQDEKVFAAIEAELGRQRSKIELIASENFVSEAVMEAQGSVLTNKYAEGYPGKRYYGGCEHVDVVEDIARDRVKEIFGAEHVNVQPHSGAQANMAVYFTILEQGDTVLGMNLSHGGHLTHGSPVNFSGVQYNFVEYGVDADSHRINYDDVLAKAKEHKPKLIVAGASAYPRVIDFKRFREIADEVGAYLMVDMAHIAGLVAAGLHPNPVPHAHFVTTTTHKTLRGPRGGMILCEEQFAKQIDKSIFPGIQGGPLMHVIAAKAVAFGEVLQDDFKTYAQNIINNANRLAEGLQKEGLTLVSGGTDNHLILIDVRNLEITGKVAEHVLDEVGITVNKNTIPFETASPFVTSGVRIGTAAVTSRGFGLEDMDEIAALIAYTLKNHENEAALEEARKRVEALTSKFPMYTDL` |
| **位置** | 1-413 |
| **重要性** | 高保守（功能待确认） |
| **功能** | 高度保守连续区域，可能涉及结构稳定或功能活性位点 |
| **证据** | 连续413aa保守性分析（平均99.69%） |
| **平均保守率** | 99.69% |
| **氨基酸组成** | Hydrophobic: 47.9% | Cationic: 14.0% | Acidic: 13.3% | Nucleophilic: 9.7% | Amide: 7.7% | Aromatic: 7.3% |
| **主导类别** | Hydrophobic（47.9%） |
| **主要理化性质** | 疏水性（Hydrophobic）——倾向埋藏于蛋白质疏水核心，参与疏水堆积/折叠 |

### 🟡 保守半胱氨酸_二硫键

| 属性 | 内容 |
|------|------|
| **片段序列** | `C×2（位置：64, 238）` |
| **位置** | 多位置 |
| **重要性** | 结构关键 |
| **功能** | 形成二硫键，维持蛋白三维构象稳定性 |
| **证据** | 共识序列中检测到2个保守Cys残基 |

---

## 3. 输入序列列表

- **WP_390192168.1**（413 aa）
- **WP_284555611.1**（413 aa）
- **WP_262716513.1**（413 aa）
- **WP_142348975.1**（413 aa）
- **WP_142340758.1**（413 aa）
- **WP_142336256.1**（413 aa）
- **WP_142333362.1**（413 aa）
- **WP_141546112.1**（413 aa）
- **WP_141522976.1**（413 aa）
- **WP_129111151.1**（413 aa）

---

## 4. 分析方法说明

1. **MSA**：使用 ClustalOmega 1.2.4 进行多序列比对
2. **共识序列**：各位置最高频氨基酸占比 ≥ 0.5 则写入，否则标X
3. **关键片段识别**：
   - 匹配已知保守块（Pfam注释特征序列）
   - 连续保守区检测（保守率 ≥ 90%，长度 ≥ 6aa）
   - 检测保守Cys残基（潜在二硫键）
4. **片段氨基酸组成分析（新）**：对每个高保守连续区段统计各功能类别氨基酸比例
   - 分类方案（含A/G/P归入疏水类）：
     Hydrophobic(V/L/I/M/A/G/P) | Nucleophilic(S/T/C) | Aromatic(F/Y/W)
     Amide(N/Q) | Acidic(D/E) | Cationic(H/K/R)；X不参与统计
   - 主导类别判定：最高占比 ≥ 35% 则为该类别主导，否则为 Mixed
5. **功能注释**：基于Pfam/InterPro已知蛋白结构-功能数据库

---

*本报告由自动化分析pipeline生成，关键片段功能解读基于已知蛋白家族注释。*

# 蛋白质关键片段预测分析报告

**物种/类群：** Citrobacter freundii  
**分析日期：** 2026-03-19 12:23  
**输入序列数：** 10  
**共识序列长度：** 417 aa  
**共识序列保守率：** 100.0%（阈值≥0.5）  

---

## 1. 共识序列

```
   1 MLKREMNIADYDAELWQAMEQEKVRQEEHIELIASENYTSPRVMQAQGSQLTNKYAEGYP
  61 GKRYYGGCEYVDIVEQLAIDRAKELFGADYANVQPHSGSQANFAVYTALLQPGDTVLGMN
 121 LAQGGHLTHGSPVNFSGKLYNIIPYGIDESGKIDYEDMAKQAKEHKPKMIIGGFSAYSGV
 181 VDWAKMREIADSIGAYLFVDMAHVAGLIAAGVYPNPVPHAHVVTTTTHKTLAGPRGGLIL
 241 AKGGDEELYKKLNSAVFPSAQGGPLMHVIAAKAVALKEAMEPEFKVYQQQVAKNAKAMVE
 301 VFLNRGYKVVSGGTENHLFLLDLVDKNLTGKEADAALGRANITVNKNSVPNDPKSPFVTS
 361 GIRIGSPAITRRGFKEAEAKELAGWMCDVLDNINDEAVIERVKGKVLDICARFPVYA
```

---

## 2. 关键功能片段

### 🔵 高保守连续区_1_417

| 属性 | 内容 |
|------|------|
| **片段序列** | `MLKREMNIADYDAELWQAMEQEKVRQEEHIELIASENYTSPRVMQAQGSQLTNKYAEGYPGKRYYGGCEYVDIVEQLAIDRAKELFGADYANVQPHSGSQANFAVYTALLQPGDTVLGMNLAQGGHLTHGSPVNFSGKLYNIIPYGIDESGKIDYEDMAKQAKEHKPKMIIGGFSAYSGVVDWAKMREIADSIGAYLFVDMAHVAGLIAAGVYPNPVPHAHVVTTTTHKTLAGPRGGLILAKGGDEELYKKLNSAVFPSAQGGPLMHVIAAKAVALKEAMEPEFKVYQQQVAKNAKAMVEVFLNRGYKVVSGGTENHLFLLDLVDKNLTGKEADAALGRANITVNKNSVPNDPKSPFVTSGIRIGSPAITRRGFKEAEAKELAGWMCDVLDNINDEAVIERVKGKVLDICARFPVYA` |
| **位置** | 1-417 |
| **重要性** | 高保守（功能待确认） |
| **功能** | 高度保守连续区域，可能涉及结构稳定或功能活性位点 |
| **证据** | 连续417aa保守性分析（平均99.74%） |
| **平均保守率** | 99.74% |
| **氨基酸组成** | Hydrophobic: 49.4% | Cationic: 13.2% | Acidic: 12.0% | Nucleophilic: 8.6% | Amide: 8.6% | Aromatic: 8.2% |
| **主导类别** | Hydrophobic（49.4%） |
| **主要理化性质** | 疏水性（Hydrophobic）——倾向埋藏于蛋白质疏水核心，参与疏水堆积/折叠 |

### 🟡 保守半胱氨酸_二硫键

| 属性 | 内容 |
|------|------|
| **片段序列** | `C×3（位置：68, 387, 410）` |
| **位置** | 多位置 |
| **重要性** | 结构关键 |
| **功能** | 形成二硫键，维持蛋白三维构象稳定性 |
| **证据** | 共识序列中检测到3个保守Cys残基 |

---

## 3. 输入序列列表

- **WP_463689776.1**（417 aa）
- **WP_435387104.1**（417 aa）
- **WP_406907711.1**（417 aa）
- **WP_374175656.1**（417 aa）
- **WP_283146408.1**（417 aa）
- **WP_230121799.1**（417 aa）
- **WP_191225812.1**（417 aa）
- **WP_181639020.1**（417 aa）
- **WP_163219575.1**（417 aa）
- **WP_153983678.1**（417 aa）

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

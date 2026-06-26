# FEL 分析

## 概述

自由能景观（FEL, Free Energy Landscape）绘制蛋白质构象的能量表面，识别稳定状态、能垒和转变途径。使用 RMSD + Gyrate 或主成分（PC）作为反应坐标。适用于识别稳定构象、量化能垒、理解构象转变、分析折叠/展开。

## 工作流程

### 方法 1：RMSD + Gyrate（结构坐标）

```bash
# 步骤 1：计算 RMSD
echo -e "Backbone\nProtein\n" | gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
```
- **目的**：计算结构偏差作为反应坐标 1
- **参数说明**：参见 RMSD 分析文档

```bash
# 步骤 2：计算 Gyrate
echo -e "Protein" | gmx gyrate -s md.tpr -f md.xtc -o gyrate.xvg
```
- **目的**：计算紧致性作为反应坐标 2
- **参数说明**：参见 Gyrate 分析文档

```bash
# 步骤 3：组合数据
dit xvg_combine -f rmsd.xvg gyrate.xvg -c 0,1 1 -o sham.xvg
```
- **目的**：组合两个反应坐标为 sham 输入文件
- **参数说明**：
  - `-f rmsd.xvg gyrate.xvg`：输入两个 XVG 文件
  - `-c 0,1 1`：列选择，第一个文件取第 0,1 列（时间,RMSD），第二个文件取第 1 列（Gyrate）
  - `-o sham.xvg`：输出组合文件，包含时间、RMSD、Gyrate 三列
- **原理**：时间列用于对齐数据，RMSD 和 Gyrate 作为两个反应坐标

```bash
# 步骤 4：生成 FEL
gmx sham -tsham 310 -nlevels 100 -f sham.xvg -ls gibbs.xpm -g gibbs.log
```
- **目的**：计算二维自由能景观
- **参数说明**：
  - `-tsham 310`：温度（K），需匹配模拟温度（如 310 K = 37°C）
  - `-nlevels 100`：能级数量，控制自由能图的分辨率
  - `-f sham.xvg`：输入反应坐标文件
  - `-ls gibbs.xpm`：输出吉布斯自由能景观（XPM 格式）
  - `-g gibbs.log`：输出能量极小值日志
- **原理**：G(x,y) = -kT ln P(x,y)，从概率分布计算自由能

### 方法 2：主成分（PCA 坐标）

```bash
# 步骤 1：执行 PCA 分析
echo -e "C-alpha\nC-alpha\n" | gmx covar -s md.tpr -f md.xtc -o eigenvalues.xvg -v eigenvectors.trr
gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 1 -last 1 -proj pc1.xvg
gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 2 -last 2 -proj pc2.xvg
```
- **目的**：计算 PC1 和 PC2 投影作为反应坐标
- **参数说明**：参见 PCA 分析文档

```bash
# 步骤 2：组合 PC 投影
dit xvg_combine -f pc1.xvg pc2.xvg -c 0,1 1 -o sham.xvg
```
- **目的**：组合 PC1 和 PC2 为 sham 输入文件
- **参数说明**：
  - `-c 0,1 1`：第一个文件取第 0,1 列（时间,PC1），第二个文件取第 1 列（PC2）

```bash
# 步骤 3：生成 FEL
gmx sham -tsham 310 -nlevels 100 -f sham.xvg -ls gibbs.xpm -g gibbs.log
```
- **参数说明**：同方法 1

### 输出
- **gibbs.xpm**：自由能景观（XPM 格式），颜色表示自由能值
- **gibbs.log**：能量极小值信息和帧索引
- **bindex.ndx**：能量极小值的帧分配索引

### 可视化
```bash
dit xpm_show -f gibbs.xpm -m contour -cmap jet -o fel.png
```
- `-m contour`：等高线模式
- `-cmap jet`：jet 配色，蓝色低能、红色高能

## 结果解释

### 能量极小值
- **深极小值（蓝色）**：稳定的构象状态，系统停留时间长
- **浅极小值**：亚稳态或瞬时构象
- **多个极小值**：存在多个稳定状态
- **单个极小值**：单个主导构象，蛋白质刚性

### 能垒
- **高能垒**：缓慢转变，稀有事件
- **低能垒**：快速转变，频繁互变
- **能垒高度**：与转变速率相关，k ∝ exp(-ΔG/kT)

### 反应坐标解释（RMSD + Gyrate）
- **低 RMSD、低 Rg**：紧密、类天然构象
- **高 RMSD、低 Rg**：错误折叠或塌陷结构
- **低 RMSD、高 Rg**：展开但有序
- **高 RMSD、高 Rg**：展开或伸展构象

### 景观拓扑
- **漏斗形状**：典型蛋白质折叠景观，导向单一稳定态
- **多个漏斗**：多个折叠途径或构象状态
- **粗糙景观**：许多局部极小值，动力学缓慢
- **平滑景观**：少数能垒，快速动力学

## 常见问题

**Q: FEL 显示不切实际的能垒（> 20 kT）？**  
A: 可能采样不足，延长模拟时间；或温度设置错误，检查 `-tsham` 参数。

**Q: FEL 显示噪声或碎片化？**  
A: 增加 `-nlevels` 参数值或延长模拟时间改善采样。

**Q: 没有显示清晰的极小值？**  
A: 蛋白质可能刚性（单个构象）或模拟质量问题，检查轨迹。

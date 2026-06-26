# PCA 分析

## 概述

主成分分析（PCA, Principal Component Analysis）通过将蛋白质运动分解为主成分来识别集体运动和主要构象变化，降低维度同时保留重要动力学信息。适用于识别集体运动、提取主要模式、降低维度、分析结构域运动。

## 工作流程

### 输入文件
- `-s`：结构文件（.tpr）
- `-f`：轨迹文件（.xtc/.trr）

### 命令

```bash
# 步骤 1：计算协方差矩阵和特征向量
echo -e "C-alpha\nC-alpha\n" | gmx covar -s md.tpr -f md.xtc -o eigenvalues.xvg -v eigenvectors.trr
```
- **目的**：计算原子位置协方差矩阵并进行特征值分解
- **参数说明**：
  - `-s md.tpr`：输入拓扑文件
  - `-f md.xtc`：输入轨迹文件
  - `-o eigenvalues.xvg`：输出特征值文件，每个特征值对应一个主成分的方差贡献
  - `-v eigenvectors.trr`：输出特征向量文件（TRR 格式），包含主成分的运动方向
- **管道输入**：`"C-alpha\nC-alpha\n"` 第一次选择拟合组（消除整体运动），第二次选择计算协方差的原子组
- **选择原因**：C-alpha 代表残基位置，计算效率高且结果易于解释

```bash
# 步骤 2：投影到主成分
gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 1 -last 1 -proj pc1.xvg
gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 2 -last 2 -proj pc2.xvg
```
- **目的**：将轨迹投影到指定主成分，获取时间序列
- **参数说明**：
  - `-v eigenvectors.trr`：输入特征向量文件（来自 covar 步骤）
  - `-first 1 -last 1`：选择第 1 个主成分（PC1）
  - `-proj pc1.xvg`：输出投影值时间序列
- **原理**：投影值表示每一帧在主成分方向上的坐标，反映运动幅度

```bash
# 步骤 3：提取极端构象（可选）
gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 1 -last 1 -extreme pc1_extreme.pdb
```
- **目的**：提取 PC1 方向上的极端构象（最大和最小投影值对应的帧）
- **参数说明**：
  - `-extreme pc1_extreme.pdb`：输出极端构象 PDB 文件，包含两个结构
- **用途**：可视化主成分运动方向，理解集体运动模式

```bash
# 步骤 4：提取平均结构（可选）
gmx anaeig -s md.tpr -f md.xtc -v eigenvectors.trr -first 1 -last 1 -average average.pdb
```
- **目的**：提取平均结构
- **参数说明**：
  - `-average average.pdb`：输出平均结构 PDB 文件

### 原子组选择

| 原子组 | 适用场景 | 说明 |
|--------|---------|------|
| C-alpha | 残基运动分析（推荐） | 每残基一个点，计算效率高 |
| Backbone | 主链运动 | 包含更多自由度 |
| Protein | 全原子运动 | 计算量大，需更多内存 |

### 输出
- **eigenvalues.xvg**：特征值（PC 编号-特征值）
- **eigenvectors.trr**：特征向量
- **pc1.xvg, pc2.xvg**：投影到主成分的时间序列
- **pc1_extreme.pdb**：极端构象

### 可视化
```bash
# 特征值谱（贡献分布）
dit xvg_show -f eigenvalues.xvg -x "PC Number" -y "Eigenvalue"

# PC1 投影时间序列
dit xvg_show -f pc1.xvg -x "Time (ps)" -y "PC1 Coordinate"

# PC1 vs PC2 散点图
dit xvg_combine -f pc1.xvg pc2.xvg -c 0,1 1 -o pc12.xvg
dit xvg_show_scatter -f pc12.xvg -c 1,2,0 -x "PC1" -y "PC2" -z "Time(ps)"
```
- **xvg_combine 参数**：`-c 0,1 1` 表示从 pc1.xvg 取第 0,1 列（时间,PC1），从 pc2.xvg 取第 1 列（PC2）
- **xvg_show_scatter 参数**：`-c 1,2,0` 指定 PC1（第1列）为 X 轴，PC2（第2列）为 Y 轴，第0列（时间）用于颜色映射

## 结果解释

### 特征值分析
- **特征值大小**：表示主成分捕获的方差，特征值越大贡献越大
- **贡献百分比**：单个 PC 贡献 = 特征值 / 总方差 × 100%
- **累积方差**：前 N 个特征值之和 / 总方差
- **典型值**：前 3 个 PC 通常捕获 50-80% 的总运动

### PC 投影
- **振幅**：投影范围表示运动幅度
- **时间尺度**：振荡频率与运动时间尺度相关
- **转变**：跳跃或位移表示构象变化

### 生物学解释
- **结构域运动**：大规模结构域间相对运动
- **环灵活性**：环和末端的局部运动
- **变构途径**：表示变构通讯的相关运动
- **功能运动**：与活性相关的运动（铰链弯曲、通道开放）

## 常见问题

**Q: 特征值分布均匀？**  
A: 可能模拟时间不足或蛋白质刚性，延长模拟时间。

**Q: PC 投影没有清晰模式？**  
A: 检查轨迹拟合和原子选择一致性。

**Q: 前几个 PC 没有捕获显著方差？**  
A: 可能蛋白质刚性或运动均匀分布，考虑使用更多 PC。

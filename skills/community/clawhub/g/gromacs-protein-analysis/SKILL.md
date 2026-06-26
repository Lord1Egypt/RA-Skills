---
name: gromacs-protein-analysis
description: "蛋白质分子动力学模拟分析的流程知识指南。当 Agent 需要执行某个分析但不清楚具体流程时调用。涵盖九种核心分析的完整工作流：(1) PBC 修正 - 消除周期性边界伪影，居中蛋白质/配体；(2) RMSD 分析 - 测量结构稳定性和模拟收敛性；(3) RMSF 分析 - 评估每个残基的灵活性；(4) 回转半径分析 - 评估蛋白质紧密性和折叠状态；(5) SASA 分析 - 研究溶剂可及性和表面性质；(6) DCCM 分析 - 动态互相关矩阵，研究原子间相关运动；(7) RDCM 分析 - 残基距离接触矩阵，分析残基间空间关系；(8) PCA 分析 - 主成分分析，识别集体运动和构象变化；(9) FEL 分析 - 自由能景观映射，使用 RMSD/Gyrate 或 PCA 作为反应坐标。包含分析间的依赖关系说明（如 FEL 依赖 PCA 或 RMSD/Gyrate 结果）。"
---

# GROMACS 蛋白质分析

本技能为分析 GROMACS 蛋白质分子动力学模拟结果提供了综合工作流程。它涵盖了蛋白质动力学研究中常用的九种主要分析类型。

## 前提条件

- GROMACS 模拟已完成，包含轨迹文件（.xtc/.trr）和拓扑文件（.tpr）
- 了解 GROMACS 命令（需要时调用 `gromacs-skills`）
- 可视化：DuIvyTools 技能（需要时调用 `duivytools-skills`）

## 平台兼容性说明

本文档中的命令使用 `echo -e` 格式传递管道输入，适用于 Linux/macOS 或 Git Bash 环境。

**Windows CMD 用户**请使用以下替代格式：

| Linux/Git Bash | Windows CMD |
|----------------|-------------|
| `echo -e "Protein\n" \| gmx cmd` | `cmd /c "(echo Protein) \| gmx cmd"` |
| `echo -e "Protein\nProtein\n" \| gmx cmd` | `cmd /c "(echo Protein & echo Protein) \| gmx cmd"` |
| `echo -e "C-alpha\nC-alpha\n" \| gmx anaeig ...` | `cmd /c "(echo C-alpha & echo C-alpha) \| gmx anaeig ..."` |

**示例转换**：
```bash
# Linux/Git Bash
echo -e "Protein\nProtein\n" | gmx trjconv -s md.tpr -f md.xtc -o center.xtc -center

# Windows CMD
cmd /c "(echo Protein & echo Protein) | gmx trjconv -s md.tpr -f md.xtc -o center.xtc -center"
```

**Windows CMD 格式说明**：
- 使用 `cmd /c` 启动 CMD 子进程执行命令
- 使用 `(echo text & echo text)` 组合多个输入行
- 每行输入之间用 `&` 分隔
- 整个管道命令用双引号包裹

**建议**：Windows 用户推荐使用 Git Bash 或 WSL 执行本文档中的命令，或使用上述 CMD 格式。

## 分析类型

### 1. 周期性边界条件（PBC）修正

修正轨迹以消除 PBC周期性问题，防止分子跨越模拟盒边界，确保下游分析的正确对齐。

**目的**：消除 PBC周期性问题，居中蛋白质/配体，消除整体平移/旋转

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：修正后的轨迹（fit.xtc），修正后的拓扑（fit.tpr）

**使用时机**：当分子跨越盒边界或 RMSD 显示突然跳跃时进行任何分析之前

**详细工作流程**：参见 [周期性校正指南](references/pbc-correction.md)

### 2. 均方根偏差（RMSD）

计算 RMSD 以测量结构稳定性并评估模拟收敛性。

**目的**：监测结构稳定性，识别平衡阶段，评估模拟收敛性，比较结构

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），参考结构

**输出**：RMSD 时间序列（rmsd.xvg），可视化（rmsd.png）

**可视化**：使用 `duivytools-skills` 技能绘制 RMSD 随时间的变化

**详细工作流程**：参见 [RMSD 分析指南](references/rmsd-analysis.md)

### 3. 均方根涨落（RMSF）

计算 RMSF 以评估每个残基的灵活性，识别柔性/刚性区域。

**目的**：识别柔性区域，评估局部稳定性，分析环动力学，比较残基灵活性

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：每个残基的 RMSF（rmsf.xvg），B 因子（bfactor.pdb），可视化（rmsf.png）

**可视化**：使用 `duivytools-skills` 技能绘制每个残基的 RMSF

**详细工作流程**：参见 [RMSF 分析指南](references/rmsf-analysis.md)

### 4. 回转半径（Gyrate）

计算回转半径以评估蛋白质紧致性和折叠状态。

**目的**：监测蛋白质紧致性，检测展开/折叠转变，评估整体大小变化

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：Gyrate 时间序列（gyrate.xvg），每个轴的数据（gyrate_axes.xvg），可视化（gyrate.png）

**可视化**：使用 `duivytools-skills` 技能绘制 Gyrate 随时间的变化

**详细工作流程**：参见 [Gyrate 分析指南](references/gyrate-analysis.md)

### 5. 溶剂可及表面积（SASA）

计算 SASA 以研究蛋白质的溶剂可及性和表面性质。

**目的**：分析溶剂暴露，识别疏水/亲水表面，研究配体结合位点，监测蛋白质展开

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：总 SASA 时间序列（sas.xvg），每个残基的 SASA（sas_per_residue.xvg），可视化（sas.png）

**可视化**：使用 `duivytools-skills` 技能绘制 SASA 随时间的变化

**详细工作流程**：参见 [SASA 分析指南](references/sasa-analysis.md)

### 6. 动态互相关矩阵（DCCM）

分析原子对之间的相关运动，识别蛋白质中的协调运动。

**目的**：识别一起移动的原子对（正相关）或反向移动的原子对（负相关）

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：协方差矩阵（covar.dat），DCCM 矩阵（dccm.xpm），可视化（dccm.png）

**可视化**：使用 `duivytools-skills` 技能生成热图

**详细工作流程**：参见 [DCCM 分析指南](references/dccm-analysis.md)

### 7. 残基距离接触矩阵（RDCM）

计算残基对之间的平均距离，分析残基间接触和空间关系。

**目的**：绘制残基-残基距离，识别长程接触，分析蛋白质结构

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：距离接触矩阵（rdcm.xpm），可视化（rdcm.png）

**可视化**：使用 `duivytools-skills` 技能生成热图

**详细工作流程**：参见 [RDCM 分析指南](references/rdcm-analysis.md)

### 8. 主成分分析（PCA）

通过将蛋白质运动分解为主成分，识别集体运动和主要构象变化。

**目的**：提取主要集体运动，分析构象灵活性，降维

**输入**：轨迹文件（.xtc），拓扑文件（.tpr），索引文件（.ndx）

**输出**：特征值（eigenvalues.xvg），特征向量（eigenvectors.trr），投影（pc1.xvg, pc2.xvg）

**关键指标**：前几个主成分的贡献百分比

**可视化**：使用 `duivytools-skills` 技能绘制特征值和投影

**详细工作流程**：参见 [PCA 分析指南](references/pca-analysis.md)

### 9. 自由能景观（FEL）

绘制自由能表面，使用 RMSD/Gyrate 或 PCA 理解构象状态和转变。

**目的**：识别稳定构象，量化能垒，理解构象景观

**方法 1 - RMSD + Gyrate**：使用结构偏差和紧致性作为反应坐标

**方法 2 - PCA**：使用主成分作为反应坐标

**输入**：RMSD 数据（rmsd.xvg），Gyrate 数据（gyrate.xvg）或 PC 投影（pc1.xvg, pc2.xvg）

**输出**：自由能景观（gibbs.xpm），能量极小值（gibbs.log），帧索引（bindex.ndx），可视化（fel.png）

**可视化**：使用 `duivytools-skills` 技能生成 2D/3D FEL 图

**详细工作流程**：参见 [FEL 分析指南](references/fel-analysis.md)

## 通用工作流程

### 任何分析之前

1. **检查轨迹质量**：目视检查轨迹是否有问题
2. **周期性校正**（如需要）：使用 周期性校正工作流程
3. **确保一致的原子选择**：对相关分析使用相同的索引组

### 分析独立性

大多数分析是独立的，可以按任意顺序进行：

**独立分析**（无依赖）：
- RMSD、RMSF、Gyrate、SASA - 基本稳定性和性质分析
- DCCM、RDCM - 接触和相关分析
- PCA - 集体运动分析

**依赖分析**（需要其他分析）：
- FEL - 需要 RMSD/Gyrate 或 PCA 结果作为反应坐标

### 推荐的预分析步骤

**周期性校正**（可选但建议）：
- 如果 RMSD 显示突然跳跃或分子跨越盒边界，考虑 周期性校正
- 周期性校正并非总是必要的 - 仅在轨迹质量指示时应用或用户明确要求时进行
- 分析问题可能有 PBC周期性问题以外的其他原因

### 每次分析之后

- **验证输出文件**：检查是否生成了所有预期文件
- **目视检查**：使用适当的可视化评估结果
- **文档记录**：记录分析参数和观察结果

## 关键考虑因素

### 原子选择

- **主链**：用于整体蛋白质运动和 RMSD 分析
- **C-alpha**：用于 PCA 和 DCCM（降低计算成本）
- **蛋白质**：用于全蛋白质分析
- **Protein_Lig**：用于蛋白质-配体复合物

### 时间选择

- **平衡阶段**：排除初始平衡期（通常是模拟的前 10-20%）
- **生产阶段**：使用生产阶段进行分析
- **一致性**：对相关分析使用相同的时间范围

### 索引组

- 使用 `gmx make_ndx` 创建适当的索引组
- 确保索引组符合分析要求
- 记录索引组的组成
- **查看索引文件内容**：使用 `dit ndx_show -f index.ndx` 快速查看 .ndx 文件中包含的所有原子组名称和原子数

## 何时调用 DuIvyTools-Skills

为可视化任务调用 `duivytools-skills` 技能：

- **XVG 文件**：绘制 RMSD、RMSF、能量、氢键、Gyrate
- **XPM 文件**：可视化 DCCM、RDCM、FEL 矩阵
- **投影**：绘制 PC1、PC2 投影
- **统计分析**：计算平均值、分布

## 故障排除

### 错误处理原则

**遇到错误时，按以下优先级寻求解决方案**：
1. **首选**：查询本技能包的参考文档（`references/` 目录下的详细指南）
2. **次选**：查询 `gromacs-skills` 或 `duivytools-skills` 相关文档
3. **最后**：仅当技能文档无相关内容时，才进行联网搜索或自行测试
4. **禁止**：猜测参数或随意尝试命令

### 常见问题

**RMSD 显示突然跳跃**：PBC周期性问题 - 应用 周期性校正

**DCCM 值都接近零**：检查原子选择，确保有足够的动力学

**PCA 显示均匀的特征值**：可能表示没有主导的集体运动或过多的噪声

**FEL 显示不切实际的能垒**：检查时间范围选择，确保足够的采样

**文件不匹配**：验证 tpr 和 xtc 具有相同的原子数，如需要使用 `gmx convert-tpr`

## 参考文档

有关详细的逐步工作流程，请参阅这些参考资料：

### 基础分析

- **[周期性校正指南](references/pbc-correction.md)** - 完整的 周期性校正工作流程
- **[RMSD 分析指南](references/rmsd-analysis.md)** - 用于稳定性评估的均方根偏差
- **[RMSF 分析指南](references/rmsf-analysis.md)** - 用于灵活性分析的均方根涨落
- **[Gyrate 分析指南](references/gyrate-analysis.md)** - 用于紧致性分析的回转半径
- **[SASA 分析指南](references/sasa-analysis.md)** - 用于表面性质的溶剂可及表面积

### 高级分析

- **[DCCM 分析指南](references/dccm-analysis.md)** - DCCM 计算和解释
- **[RDCM 分析指南](references/rdcm-analysis.md)** - 距离接触矩阵分析
- **[PCA 分析指南](references/pca-analysis.md)** - 主成分分析工作流程
- **[FEL 分析指南](references/fel-analysis.md)** - 自由能景观映射

## 快速参考

### 必需的输入文件

- **轨迹**：来自 GROMACS 模拟的 .xtc 或 .trr 文件
- **拓扑**：.tpr 文件（必须与轨迹原子数匹配）
- **索引**：包含自定义原子组的 .ndx 文件

### 常见输出文件

- **XVG**：时间序列数据（RMSD、特征值、投影）
- **XPM**：矩阵数据（DCCM、RDCM、FEL）
- **TRR**：向量数据（特征向量）
- **PDB**：结构文件（平均、极端构象）

### 分析顺序建议

可以根据研究问题灵活进行分析：

**用于基本稳定性评估**：从 RMSD、RMSF、Gyrate、SASA 开始（任意顺序）

**用于接触和相关分析**：执行 DCCM 和 RDCM（独立）

**用于集体运动分析**：执行 PCA（独立）

**用于构象景观**：在获得 RMSD/Gyrate 或 PCA 数据后生成 FEL

**注意**：仅当 RMSD 显示突然跳跃或轨迹质量问题或用户要求时考虑 周期性校正。许多分析在没有 周期性校正的情况下也能正常工作。

## 最佳实践

- **永远不要覆盖**现有文件 - 使用唯一的输出文件名
- **对所有相关分析使用一致的时间范围**
- **记录所有参数**和索引组选择
- **可视化中间结果**以尽早发现问题
- **验证原子数一致性**在 tpr 和 xtc 文件之间
- **在解释结果之前检查统计收敛性**


# SASA 分析

## 概述

溶剂可及表面积（SASA, Solvent Accessible Surface Area）测量蛋白质可被溶剂分子接触的表面积，提供蛋白质-溶剂相互作用和表面性质信息。适用于分析溶剂暴露、识别疏水/亲水区域、研究结合位点可及性、监测展开/聚集。

## 工作流程

### 输入文件
- `-s`：结构文件（.tpr）
- `-f`：轨迹文件（.xtc/.trr）

### 命令

```bash
echo -e "Protein\n" | gmx sasa -s md.tpr -f md.xtc -o sasa.xvg
```
- **目的**：计算蛋白质总溶剂可及表面积的时间序列
- **参数说明**：
  - `-s md.tpr`：输入拓扑文件
  - `-f md.xtc`：输入轨迹文件
  - `-o sasa.xvg`：输出 SASA 时间序列文件
- **管道输入**：`"Protein"` 选择计算 SASA 的表面组
- **选择原因**：Protein 包含所有蛋白质原子，计算完整表面

### 可选参数：每残基 SASA

```bash
echo -e "Protein\n" | gmx sasa -s md.tpr -f md.xtc -o sasa.xvg -or sas_residue.xvg
```
- `-or sas_residue.xvg`：输出每个残基的平均 SASA
- **用途**：识别暴露残基和被掩埋残基

### 可选参数：探针半径

```bash
echo -e "Protein\n" | gmx sasa -s md.tpr -f md.xtc -o sasa.xvg -probe 0.14
```
- `-probe 0.14`：探针半径设为 0.14 nm（水分子半径，默认值）
- **用途**：模拟水分子在蛋白质表面的滚动探测

### 原子组选择

| 原子组 | 适用场景 | 说明 |
|--------|---------|------|
| Protein | 整体 SASA（推荐） | 所有蛋白质原子表面 |
| Backbone | 主链表面 | 侧链被忽略 |
| 非标准组 | 特定区域 | 如结合位点、活性位点 |

### 输出
- **sasa.xvg**：时间-SASA 数据
  - 第 1 列：时间（ps）
  - 第 2 列：总 SASA（单位：nm²）

### 可视化
```bash
dit xvg_show -f sasa.xvg -x "Time (ns)" -y "SASA (nm²)"
```

## 常见问题

**Q: SASA 持续增加？**  
A: 可能蛋白质展开，检查结构或延长模拟时间。

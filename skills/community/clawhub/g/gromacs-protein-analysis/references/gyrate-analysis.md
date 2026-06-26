# Gyrate 分析

## 概述

回转半径（Rg, Radius of Gyration）测量原子相对于质心的质量加权均方根距离，评估蛋白质紧致性和折叠状态。适用于监测紧致性变化、检测折叠/展开转变、比较不同状态、验证蛋白质稳定性。

## 工作流程

### 输入文件
- `-s`：结构文件（.tpr）
- `-f`：轨迹文件（.xtc/.trr）

### 命令

```bash
echo -e "Protein\n" | gmx gyrate -s md.tpr -f md.xtc -o gyrate.xvg
```
- **目的**：计算蛋白质回转半径时间序列，评估紧致性
- **参数说明**：
  - `-s md.tpr`：输入拓扑文件
  - `-f md.xtc`：输入轨迹文件
  - `-o gyrate.xvg`：输出 Rg 时间序列文件
- **管道输入**：`"Protein"` 选择计算 Rg 的原子组
- **选择原因**：使用全蛋白原子可获得质量加权的 Rg，反映整体紧致性

### 输出
- **gyrate.xvg**：时间-Rg 数据
  - 第 1 列：时间（ps）
  - 第 2 列：总 Rg（单位：nm）
  - 第 3-5 列：Rg_x, Rg_y, Rg_z

### 可视化
```bash
dit xvg_show -f gyrate.xvg -x "Time (ns)" -y "Rg (nm)" -t "Radius of Gyration"
```

## 常见问题

**Q: Rg 显示突然跳跃？**  
A: 检查 PBC 问题，应用周期性校正。

**Q: Rg 持续增加？**  
A: 可能蛋白质展开，检查结构或延长模拟时间。

**Q: 各轴 Rg 差异大？**  
A: 可能是天然细长蛋白质（如纤维状蛋白），属正常现象。
---
name: gromacs-skills
description: "GROMACS 分子动力学模拟软件命令参考。当 Agent 需要执行 GROMACS 命令但不清楚用法时调用。功能覆盖：(1) 拓扑与结构处理 - pdb2gmx、editconf、solvate、insert-molecules、genrestr；(2) 模拟设置与运行 - grompp、mdrun；(3) 轨迹处理 - trjconv（PBC修正、格式转换）、trjcat（轨迹拼接）；(4) 能量分析 - energy、eneconv、bar；(5) 轨迹分析 - rms、rmsf、gyrate、hbond、distance、angle、dihedral、sasa、cluster、mindist；(6) 结构分析 - covar、anaeig（PCA）、mdmat、sham（FEL）；(7) 索引与选择 - make_ndx、select、genion；(8) 工具 - xpm2ps、check、wham。强调优先使用 gmx <command> -h 查看本地帮助。"
---

# GROMACS

> **重要：始终先查看本地帮助**
>
> GROMACS 版本差异可能导致参数不同。**务必**先运行 `gmx <command> -h` 获取该命令最准确的参数信息。

GROMACS 是分子动力学模拟软件包，可模拟从几百到数百万粒子的系统。本技能提供 GROMACS 命令参考和工作流指南。

## 快速入门

### 检查版本

```bash
gmx --version
```

记录版本号以便查阅对应文档。

### 获取帮助

**优先级 1：本地帮助（最快、版本匹配）**
```bash
gmx <command> -h
```

**优先级 2：在线文档（详细、官方）**
```bash
# 带版本号搜索
web_search: "site:manual.gromacs.org gmx <command> <version>"
# 示例: "site:manual.gromacs.org gmx rms 2024.3"
```

## 命令分类

| 分类 | 主要命令 | 说明 |
|------|----------|------|
| **拓扑与结构** | `pdb2gmx`, `editconf`, `solvate`, `insert-molecules`, `genrestr` | 生成拓扑、定义盒子、添加溶剂 |
| **模拟设置** | `grompp`, `mdrun` | 生成运行文件、执行模拟 |
| **能量分析** | `energy`, `eneconv`, `bar` | 提取能量、自由能计算 |
| **轨迹分析** | `rms`, `rmsf`, `gyrate`, `hbond`, `distance`, `angle`, `dihedral`, `cluster`, `mindist`, `sasa`, `principal`, `do_dssp` | RMSD/RMSF、氢键、距离、二级结构等 |
| **结构分析** | `covar`, `anaeig`, `mdmat`, `sham`, `order`, `rotacf`, `dielectric` | PCA、距离矩阵、自由能景观 |
| **轨迹处理** | `trjconv`, `trjcat`, `trjorder`, `dump` | 格式转换、PBC 修正、轨迹拼接 |
| **索引与选择** | `make_ndx`, `select`, `genion` | 创建索引组、选择原子、添加离子 |
| **工具** | `xpm2ps`, `x2top`, `check`, `wham`, `tune_pme` | 格式转换、检查文件、WHAM 分析 |

完整命令说明请参阅 [command-categories.md](references/command-categories.md)。

## 常用参数

### 输入输出

| 参数 | 说明 |
|------|------|
| `-f INPUT` | 输入轨迹/结构文件 |
| `-s TOPOLOGY` | 输入拓扑文件（.tpr） |
| `-n INDEX` | 输入索引文件（.ndx） |
| `-o OUTPUT` | 输出文件 |
| `-deffnm BASENAME` | 默认文件名前缀 |

### 时间选择

| 参数 | 说明 |
|------|------|
| `-b TIME` | 起始时间（ps） |
| `-e TIME` | 结束时间（ps） |
| `-dt TIME` | 时间步长（ps） |

### 轨迹处理

| 参数 | 说明 |
|------|------|
| `-pbc TYPE` | PBC 处理（none, mol, atom, com, nojump） |
| `-center` | 居中坐标 |
| `-fit TYPE` | 拟合轨迹（none, rot+trans 等） |

### 性能参数

| 参数 | 说明 |
|------|------|
| `-nt NUMBER` | 线程数 |
| `-ntomp NUMBER` | OpenMP 线程数 |
| `-nb TYPE` | 邻居搜索（cpu, gpu） |

完整参数说明请参阅 [common-parameters.md](references/common-parameters.md)。

## 如何使用 GROMACS 命令

**核心原则：始终先查看本地帮助**

```bash
# 查看命令帮助
gmx <command> -h

# 示例
gmx rms -h
gmx trjconv -h
gmx energy -h
```

本地帮助提供：
- 完整参数列表
- 默认值说明
- 输入/输出文件要求
- 使用示例

**在线文档查询**（本地帮助不够时）：

```bash
# 带版本号搜索官方文档
web_search: "site:manual.gromacs.org gmx <command> <version>"
# 示例: "site:manual.gromacs.org gmx rms 2024.3"
```

## 文件格式

### 输入格式

| 格式 | 说明 |
|------|------|
| `.pdb` | Protein Data Bank 格式 |
| `.gro` | GROMACS 坐标格式 |
| `.tpr` | GROMACS 运行输入文件（拓扑+参数） |
| `.xtc` | 压缩轨迹（有损，适合长模拟） |
| `.trr` | 全精度轨迹 |
| `.ndx` | 索引文件（原子组） |
| `.mdp` | 分子动力学参数文件 |
| `.top` | 拓扑文件 |

### 输出格式

| 格式 | 说明 |
|------|------|
| `.xvg` | Grace/XVG 图表格式（时间序列数据） |
| `.xpm` | 像素图格式（矩阵、热图） |
| `.edr` | 能量文件（二进制） |
| `.log` | 日志文件 |
| `.cpt` | 检查点文件（用于续算） |

## 版本兼容性

不同 GROMACS 版本可能有参数差异：

- `.tpr` 文件**不兼容**不同主版本
- 升级版本后需重新生成 `.tpr` 文件
- 始终检查 `.mdp` 参数是否有效
- 版本差异请查询官方文档：`site:manual.gromacs.org <version>`

## 与 DuIvyTools 配合

GROMACS 输出文件可使用 DuIvyTools 可视化：

- **.xvg 文件**：RMSD、RMSF、能量、氢键等时间序列数据
- **.xpm 文件**：DCCM、FEL、DSSP 等矩阵数据

使用 `duivytools-skills` 技能进行可视化：

```bash
# 可视化 RMSD
dit xvg_show -f rmsd.xvg -x "Time (ns)" -y "RMSD (nm)"

# 可视化 DCCM
dit xpm_show -f dccm.xpm -cmap coolwarm -zmin -1 -zmax 1

# 可视化自由能景观
dit xpm_show -f fel.xpm -m 3d -eg plotly
```

## 性能优化

### 并行执行

```bash
# OpenMP（多线程）
gmx mdrun -nt 4 -s topol.tpr -deffnm md

# MPI（多节点）
mpirun -np 4 gmx_mpi mdrun -s topol.tpr -deffnm md

# 混合 MPI+OpenMP
mpirun -np 2 gmx_mpi mdrun -ntomp 2 -s topol.tpr -deffnm md
```

### GPU 加速

```bash
# GPU 用于非键相互作用
gmx mdrun -ntomp 4 -nb gpu -s topol.tpr -deffnm md

# GPU 用于更新
gmx mdrun -ntomp 4 -nb gpu -update gpu -s topol.tpr -deffnm md
```

## 常见问题

**"Fatal error: No such group"**：索引组未找到
- 解决方案：使用 `make_ndx` 创建正确的索引文件

**"Fatal error: Domain decomposition error"**：并行设置问题
- 解决方案：调整 MPI 进程数或域分解参数

**"Fatal error: Number of coordinates does not match topology"**：文件不匹配
- 解决方案：重新生成拓扑或坐标文件

## 最佳实践

- 使用前**检查版本**
- **优先使用本地帮助**获取准确参数
- 大模拟前**先在小系统测试**
- 生产运行时**监控能量守恒**
- 修改前**备份文件**
- **记录所有参数**以便复现
- 使用 DuIvyTools 进行**可视化分析**

## 重要安全提示

> **Production Run（生产运行）**
>
> Agent **不应主动执行** `mdrun` 生产运行。正确的做法是：
> - 生成运行脚本（如 `run.sh`）供用户执行
> - 脚本应包含完整的运行命令和参数
> - 让用户在合适的计算环境中自行运行
>
> 示例脚本：
> ```bash
> #!/bin/bash
> # run_md.sh - 生产运行脚本
> gmx mdrun -s md.tpr -deffnm md -ntomp 4 -nb gpu
> ```
>
> Agent 可以执行的操作：
> - ✅ 能量最小化（短时间）
> - ✅ NVT/NPT 平衡（短时间）
> - ✅ 分析命令（rms, rmsf, hbond 等）
> - ✅ 轨迹处理（trjconv）
> - ❌ 长时间生产运行（应由用户执行）

## 参考文档

- **[command-categories.md](references/command-categories.md)** - 完整命令列表和说明
- **[common-parameters.md](references/common-parameters.md)** - 常用参数详解

## 相关资源

- 官方文档: https://manual.gromacs.org/
- GitHub: https://github.com/gromacs/gromacs
- 用户论坛: https://gromacs.bioexcel.eu/
- 教程: http://www.mdtutorials.com/gmx/
- 引用: Abraham et al., SoftwareX 1-2, 19-25 (2015)

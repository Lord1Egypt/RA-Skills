# GROMACS 命令分类

本文档按功能分类列出 GROMACS 命令。

> **重要**：不同版本参数可能有差异。始终使用 `gmx <command> -h` 查看准确参数。

## 目录

- [1. 拓扑与结构](#1-拓扑与结构)
- [2. 模拟设置](#2-模拟设置)
- [3. 能量分析](#3-能量分析)
- [4. 轨迹分析](#4-轨迹分析)
- [5. 结构分析](#5-结构分析)
- [6. 轨迹处理](#6-轨迹处理)
- [7. 索引与选择](#7-索引与选择)
- [8. 工具与实用程序](#8-工具与实用程序)

---

## 1. 拓扑与结构

### `pdb2gmx`
从 PDB 结构生成 GROMACS 拓扑。

**用途**：将 PDB 文件转换为 GROMACS 拓扑和坐标文件。

**常用参数**：
- `-f INPUT`：输入 PDB 文件
- `-o OUTPUT`：输出 GROMACS 坐标文件
- `-p OUTPUT`：输出拓扑文件
- `-i OUTPUT`：输出位置限制文件
- `-ff STRING`：力场选择
- `-water ENUM`：水模型（none, spc, spce, tip3p, tip4p, tip5p）
- `-[no]ignh`：忽略 PDB 中的氢原子
- `-merge ENUM`：合并多条链（no, all, interactive）
- `-chainsep ENUM`：链分隔方式（id_or_ter, id_and_ter, ter, id, interactive）

**示例**：
```bash
gmx pdb2gmx -f protein.pdb -o protein.gro -p topol.top -water tip3p
```

### `editconf`
编辑结构文件（盒子定义、尺寸）。

**用途**：定义模拟盒子、修改盒子尺寸、居中分子。

**常用参数**：
- `-f INPUT`：输入结构文件
- `-o OUTPUT`：输出结构文件
- `-bt ENUM`：盒子类型（triclinic, cubic, dodecahedron, octahedron）
- `-d REAL`：分子与盒子边缘的距离
- `-[no]c`：在盒子中居中
- `-center VECTOR`：将几何中心移到指定位置
- `-box VECTOR`：盒子尺寸
- `-angles VECTOR`：盒子角度（三斜）

**示例**：
```bash
gmx editconf -f protein.gro -o protein_box.gro -bt cubic -d 1.0 -c
gmx editconf -f protein.gro -o protein_dod.gro -bt dodecahedron -d 1.0 -c
```

### `solvate`
向模拟盒子添加溶剂分子。

**用途**：用溶剂分子填充模拟系统。

**常用参数**：
- `-cp INPUT`：输入结构（盒子中的蛋白质）
- `-cs INPUT`：溶剂结构（如 spc216.gro）
- `-o OUTPUT`：输出溶剂化结构
- `-p TOPOLOGY`：输出拓扑文件

**示例**：
```bash
gmx solvate -cp protein_box.gro -cs spc216.gro -o protein_solv.gro -p topol.top
```

### `insert-molecules`
向模拟盒子插入分子。

**用途**：向模拟盒子插入多个分子的副本。

**常用参数**：
- `-f INPUT`：输入结构
- `-ci INPUT`：要插入的结构
- `-nmol INT`：插入分子数量
- `-o OUTPUT`：输出结构
- `-radius REAL`：分子间最小距离

**示例**：
```bash
gmx insert-molecules -f protein_solv.gro -ci ligand.gro -nmol 10 -o protein_lig.gro
```

### `genrestr`
生成位置限制文件。

**用途**：为平衡阶段创建位置限制文件。

**常用参数**：
- `-f INPUT`：输入结构
- `-o OUTPUT`：输出位置限制文件
- `-i INPUT`：索引文件
- `-fc REAL REAL REAL`：力常数（x, y, z 方向）

**示例**：
```bash
echo "Protein-H" | gmx genrestr -f protein.gro -o posre.itp -fc 1000 1000 1000
```

---

## 2. 模拟设置

### `grompp`
从拓扑和参数生成模拟运行输入文件（.tpr）。

**用途**：编译拓扑、参数和模拟条件到 .tpr 文件。

**常用参数**：
- `-f INPUT`：输入参数文件（.mdp）
- `-c INPUT`：输入结构文件
- `-p INPUT`：输入拓扑文件
- `-o OUTPUT`：输出 .tpr 文件
- `-r INPUT`：参考结构（用于位置限制）
- `-n INPUT`：索引文件
- `-t INPUT`：输入轨迹（用于重启）
- `-e INPUT`：能量文件（用于重启）
- `-po OUTPUT`：输出处理后的 .mdp 文件
- `-maxwarn INT`：最大警告忽略数

**示例**：
```bash
gmx grompp -f minim.mdp -c ions.gro -p topol.top -o em.tpr
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
```

### `mdrun`
运行分子动力学模拟。

**用途**：执行分子动力学模拟。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-deffnm STRING`：默认文件名前缀
- `-o OUTPUT`：输出轨迹
- `-x OUTPUT`：压缩轨迹
- `-c OUTPUT`：最终坐标
- `-e OUTPUT`：输出能量文件
- `-g OUTPUT`：输出日志文件
- `-cpt REAL`：检查点间隔（分钟）
- `-nt INT`：总线程数
- `-ntmpi INT`：线程 MPI 进程数
- `-ntomp INT`：每个 MPI 进程的 OpenMP 线程数
- `-nb ENUM`：非键相互作用位置（auto, cpu, gpu）
- `-pme ENUM`：PME 计算位置（auto, cpu, gpu）
- `-update ENUM`：更新和约束位置（auto, cpu, gpu）
- `-[no]tunepme`：优化 PME 负载（默认 yes）
- `-gpu_id STRING`：GPU 设备 ID 列表
- `-nsteps INT`：覆盖步数
- `-replex INT`：副本交换周期（步数）

**示例**：
```bash
gmx mdrun -s em.tpr -deffnm em
gmx mdrun -s md.tpr -deffnm md -ntomp 4 -nb gpu
mpirun -np 4 gmx_mpi mdrun -s md.tpr -deffnm md
```

---

## 3. 能量分析

### `energy`
从能量文件提取能量组分。

**用途**：从 .edr 文件提取和分析能量项。

**常用参数**：
- `-f INPUT`：输入能量文件
- `-o OUTPUT`：输出 XVG 文件
- `-b TIME`：起始时间
- `-e TIME`：结束时间

**示例**：
```bash
echo "Potential" | gmx energy -f md.edr -o potential.xvg
echo "Temperature" | gmx energy -f npt.edr -o temp.xvg
echo "Pressure" | gmx energy -f npt.edr -o press.xvg
```

### `eneconv`
转换能量文件格式。

**用途**：合并或转换能量文件。

**常用参数**：
- `-f INPUT`：输入能量文件
- `-o OUTPUT`：输出能量文件

**示例**：
```bash
gmx eneconv -f part1.edr part2.edr -o combined.edr
```

### `bar`
使用 Bennett 接受比率计算自由能。

**用途**：从热力学积分计算自由能差。

**常用参数**：
- `-f INPUT`：输入能量文件
- `-o OUTPUT`：输出 XVG 文件

**示例**：
```bash
gmx bar -f lambda0.edr lambda1.edr -o dg.xvg
```

---

## 4. 轨迹分析

### `rms`
计算均方根偏差（RMSD）。

**用途**：计算相对于参考结构的 RMSD。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-o OUTPUT`：输出 XVG 文件
- `-n INPUT`：索引文件

**示例**：
```bash
echo "Backbone\nProtein" | gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
```

### `rmsf`
计算均方根涨落（RMSF）。

**用途**：计算每个原子的 RMSF。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-o OUTPUT`：输出 XVG 文件
- `-n INPUT`：索引文件
- `-[no]res`：按残基输出

**示例**：
```bash
echo "C-alpha" | gmx rmsf -s md.tpr -f md.xtc -o rmsf.xvg -res
```

### `gyrate`
计算回转半径。

**用途**：计算回转半径及其分量。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-o OUTPUT`：输出 XVG 文件
- `-n INPUT`：索引文件

**示例**：
```bash
echo "Protein" | gmx gyrate -s md.tpr -f md.xtc -o rg.xvg
```

### `hbond`
分析氢键。

**用途**：计算和分析氢键（GROMACS 2024 新版）。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-num OUTPUT`：输出氢键数量
- `-dist OUTPUT`：输出氢键距离分布
- `-ang OUTPUT`：输出氢键角度分布
- `-r SELECTION`：参考选择
- `-t SELECTION`：目标选择

**示例**：
```bash
gmx hbond -s md.tpr -f md.xtc -r "protein" -t "protein" -num hb.xvg
```

### `distance`
计算原子组间距离。

**用途**：计算两组原子间的距离随时间变化。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-n INPUT`：索引文件
- `-oall OUTPUT`：输出所有距离
- `-select STRING`：选择字符串

**示例**：
```bash
gmx distance -s md.tpr -f md.xtc -select "com of group \"Protein\" com of group \"Ligand\"" -oall dist.xvg
```

### `angle`
计算角度。

**用途**：计算三组原子间的角度。

**示例**：
```bash
gmx angle -s md.tpr -f md.xtc -n index.ndx -oall angle.xvg
```

### `dihedral`
计算二面角。

**用途**：计算四组原子间的二面角。

**示例**：
```bash
gmx dihedral -s md.tpr -f md.xtc -n index.ndx -oall dih.xvg
```

### `cluster`
构象聚类分析。

**用途**：基于 RMSD 对轨迹帧进行聚类。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-method ENUM`：聚类方法（linkage, jarvis-patrick, monte-carlo, diagonalization, gromos）
- `-cutoff REAL`：截断距离
- `-cl OUTPUT`：输出聚类文件
- `-o OUTPUT`：输出聚类矩阵（.xpm）
- `-g OUTPUT`：输出日志文件
- `-sz OUTPUT`：输出聚类大小

**示例**：
```bash
echo "Backbone" | gmx cluster -s md.tpr -f md.xtc -method gromos -cutoff 0.2 -cl clusters.pdb
```

### `mindist`
计算组间最小距离。

**用途**：计算原子组间的最小距离。

**示例**：
```bash
echo "Protein\nLigand" | gmx mindist -s md.tpr -f md.xtc -od mindist.xvg
```

### `sasa`
计算溶剂可及表面积。

**用途**：计算选定原子的 SASA。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-o OUTPUT`：输出 XVG 文件
- `-probe REAL`：探针半径（默认 0.14 nm）
- `-surface SELECTION`：表面计算选择
- `-output SELECTION`：输出选择

**示例**：
```bash
gmx sasa -s md.tpr -f md.xtc -surface "protein" -o sasa.xvg
```

### `principal`
分子的主成分分析。

**用途**：计算主轴和惯性矩。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-n INPUT`：索引文件
- `-a1 OUTPUT`：输出第一主轴
- `-a2 OUTPUT`：输出第二主轴
- `-a3 OUTPUT`：输出第三主轴
- `-om OUTPUT`：输出惯性矩

**示例**：
```bash
echo "Protein" | gmx principal -s md.tpr -f md.xtc -a1 paxis1.xvg -om moi.xvg
```

### `do_dssp`
二级结构分析（DSSP）。

**用途**：使用 DSSP 算法分配二级结构。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-n INPUT`：索引文件
- `-o OUTPUT`：输出 XPM 文件（每残基二级结构）
- `-sc OUTPUT`：输出 XVG 文件（二级结构比例）

**示例**：
```bash
echo "Protein" | gmx do_dssp -s md.tpr -f md.xtc -o ss.xpm -sc ss.xvg
```

---

## 5. 结构分析

### `covar`
协方差矩阵分析（用于 PCA）。

**用途**：计算原子涨落的协方差矩阵。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-n INPUT`：索引文件
- `-o OUTPUT`：输出特征值（.xvg）
- `-v OUTPUT`：输出特征向量（.trr）
- `-av OUTPUT`：输出平均结构
- `-ascii OUTPUT`：输出 ASCII 协方差矩阵
- `-xpm OUTPUT`：输出协方差矩阵（.xpm）
- `-xpma OUTPUT`：输出原子协方差矩阵
- `-[no]fit`：拟合到参考结构
- `-[no]mwa`：质量加权协方差分析

**示例**：
```bash
echo "C-alpha\nC-alpha" | gmx covar -s md.tpr -f md.xtc -o eigenval.xvg -v eigenvec.trr
```

### `anaeig`
分析协方差分析的特征向量。

**用途**：将轨迹投影到特征向量上，进行 PCA 分析。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-v INPUT`：输入特征向量文件
- `-first INT`：第一个特征向量
- `-last INT`：最后一个特征向量
- `-proj OUTPUT`：输出投影
- `-2d OUTPUT`：输出 2D 投影
- `-extr OUTPUT`：输出极端结构
- `-over OUTPUT`：输出重叠矩阵

**示例**：
```bash
echo "C-alpha\nC-alpha" | gmx anaeig -s md.tpr -f md.xtc -v eigenvec.trr -first 1 -last 2 -proj pc.xvg
```

### `mdmat`
计算残基间距离矩阵。

**用途**：计算残基间的平均距离矩阵。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-mean OUTPUT`：输出平均距离矩阵

**示例**：
```bash
echo "Protein" | gmx mdmat -s md.tpr -f md.xtc -mean rdcm.xpm
```

### `sham`
生成自由能景观。

**用途**：从反应坐标生成自由能景观。

**常用参数**：
- `-f INPUT`：输入 XVG 文件（包含反应坐标）
- `-tsham REAL`：温度
- `-ls OUTPUT`：输出 Gibbs 自由能
- `-nlevels INT`：等高线数量

**示例**：
```bash
gmx sham -f reaction.xvg -tsham 310 -nlevels 100 -ls fel.xpm
```

### `order`
计算序参数。

**用途**：计算脂质序参数。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-n INPUT`：索引文件
- `-d ENUM`：膜法线方向（z, x, y）
- `-o OUTPUT`：输出序参数
- `-od OUTPUT`：输出氘序参数

**示例**：
```bash
gmx order -s md.tpr -f md.xtc -d z -o order.xvg
```

### `rotacf`
计算旋转自相关函数。

**用途**：计算旋转相关时间。

**示例**：
```bash
gmx rotacf -s md.tpr -f md.xtc -o rotacf.xvg
```

### `dielectric`
计算介电性质。

**用途**：计算介电常数和性质。

**示例**：
```bash
gmx dielectric -f dipole.xvg -d dielectric.xvg
```

---

## 6. 轨迹处理

### `trjconv`
转换轨迹格式、应用 PBC 修正、拟合结构。

**用途**：处理轨迹文件（格式转换、PBC 修正、拟合）。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-f INPUT`：输入轨迹
- `-o OUTPUT`：输出轨迹
- `-n INPUT`：索引文件
- `-pbc ENUM`：PBC 处理（none, mol, res, atom, nojump, cluster, whole）
- `-[no]center`：居中
- `-fit ENUM`：拟合（none, rot+trans, rotxy+transxy, translation, transxy, progressive）
- `-ur ENUM`：晶胞表示（rect, tric, compact）
- `-b TIME`：起始时间
- `-e TIME`：结束时间
- `-dt TIME`：时间步长

**示例**：
```bash
echo "Protein\nProtein" | gmx trjconv -s md.tpr -f md.xtc -o centered.xtc -pbc mol -center
echo "Backbone\nProtein" | gmx trjconv -s md.tpr -f md.xtc -o fit.xtc -fit rot+trans
```

### `trjcat`
合并多个轨迹文件。

**用途**：将多个轨迹文件合并为一个。

**常用参数**：
- `-f INPUT`：输入轨迹文件
- `-o OUTPUT`：输出轨迹

**示例**：
```bash
gmx trjcat -f part1.xtc part2.xtc -o combined.xtc
```

### `trjorder`
重排轨迹中的原子。

**用途**：重排轨迹文件中的原子顺序。

**示例**：
```bash
gmx trjorder -s md.tpr -f md.xtc -o ordered.xtc
```

### `dump`
将轨迹转储为文本格式。

**用途**：将轨迹转换为 ASCII 文本格式。

**示例**：
```bash
gmx dump -s md.tpr -f md.xtc -o md.txt
```

---

## 7. 索引与选择

### `make_ndx`
创建或编辑索引文件。

**用途**：创建和修改包含原子组的索引文件。

**常用参数**：
- `-f INPUT`：输入结构或 .tpr 文件
- `-o OUTPUT`：输出索引文件
- `-n INPUT`：输入索引文件

**示例**：
```bash
gmx make_ndx -f md.tpr -o index.ndx
echo "r 1-100\nname 10 Residues1-100\nq" | gmx make_ndx -f md.tpr -o index.ndx
```

### `select`
使用选择语言选择原子。

**用途**：使用强大的选择语法选择原子。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-select STRING`：选择字符串
- `-on OUTPUT`：输出索引文件
- `-os OUTPUT`：输出结构

**示例**：
```bash
gmx select -s md.tpr -select "resid 1 to 100 and name CA" -on ca.ndx
gmx select -s md.tpr -select "protein" -os protein.pdb
```

### `genion`
用水分子替换离子。

**用途**：替换溶剂分子以中和系统或添加离子。

**常用参数**：
- `-s INPUT`：输入 .tpr 文件
- `-p INPUT`：输入拓扑
- `-o OUTPUT`：输出结构
- `-pname STRING`：正离子名称
- `-nname STRING`：负离子名称
- `-np INT`：正离子数量
- `-nn INT`：负离子数量
- `-conc REAL`：盐浓度（mol/L）
- `-[no]neutral`：中和系统

**示例**：
```bash
echo "SOL" | gmx genion -s ions.tpr -p topol.top -o ions.gro -pname NA -nname CL -neutral
echo "SOL" | gmx genion -s ions.tpr -p topol.top -o ions.gro -pname NA -nname CL -np 10 -nn 10
```

---

## 8. 工具与实用程序

### `xpm2ps`
将 XPM 矩阵文件转换为 PostScript。

**用途**：将 XPM 矩阵文件转换为 PostScript 用于可视化。

**常用参数**：
- `-f INPUT`：输入 XPM 文件
- `-o OUTPUT`：输出 PostScript 文件
- `-[no]rainbow`：使用彩虹色

**示例**：
```bash
gmx xpm2ps -f matrix.xpm -o matrix.eps
```

### `x2top`
从坐标生成拓扑。

**用途**：使用力场从坐标生成拓扑。

**示例**：
```bash
gmx x2top -f molecule.gro -o molecule.top
```

### `check`
检查模拟文件错误。

**用途**：验证模拟文件并检查错误。

**示例**：
```bash
gmx check -s md.tpr -f md.xtc
```

### `wham`
加权直方图分析方法。

**用途**：从伞形采样计算自由能剖面。

**常用参数**：
- `-it INPUT`：输入 tpr 文件列表
- `-if INPUT`：输入拉力文件列表
- `-o OUTPUT`：输出剖面

**示例**：
```bash
gmx wham -it tprs.dat -if pullf-files.dat -o profile.xvg
```

### `tune_pme`
优化 PME 参数。

**用途**：为特定硬件优化 PME 参数。

**示例**：
```bash
gmx tune_pme -s md.tpr -np 4
```

---

## 命令分类总结

| 分类 | 命令 |
|------|------|
| 拓扑/结构 | pdb2gmx, editconf, solvate, insert-molecules, genrestr |
| 模拟设置 | grompp, mdrun |
| 能量分析 | energy, eneconv, bar |
| 轨迹分析 | rms, rmsf, gyrate, hbond, distance, angle, dihedral, cluster, mindist, sasa, principal, do_dssp |
| 结构分析 | covar, anaeig, mdmat, sham, order, rotacf, dielectric |
| 轨迹处理 | trjconv, trjcat, trjorder, dump |
| 索引/选择 | make_ndx, select, genion |
| 工具/实用 | xpm2ps, x2top, check, wham, tune_pme |

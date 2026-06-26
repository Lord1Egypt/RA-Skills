# Common GROMACS Parameters

This document explains frequently used GROMACS parameters across different commands.

> **重要**：不同命令支持的参数不同。以下为常见参数概述，具体参数请使用 `gmx <command> -h` 查看。

## 目录

- [输入输出参数](#输入输出参数)
- [时间选择参数](#时间选择参数)
- [轨迹处理参数](#轨迹处理参数)
- [性能参数](#性能参数)
- [其他常用参数](#其他常用参数)
- [参数分组](#参数分组)

---

## 输入输出参数

### `-f INPUT`
**输入轨迹或结构文件**

- 常见格式：.xtc, .trr, .gro, .pdb, .edr
- 示例：
  ```bash
  gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
  gmx energy -f md.edr -o energy.xvg
  ```

### `-s INPUT`
**输入拓扑文件（.tpr）**

- 格式：仅 .tpr
- 示例：
  ```bash
  gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
  gmx trjconv -s md.tpr -f md.xtc -o fit.xtc
  ```

### `-n INPUT`
**输入索引文件（.ndx）**

- 格式：仅 .ndx
- 示例：
  ```bash
  echo "Protein" | gmx rms -s md.tpr -f md.xtc -n index.ndx -o rmsd.xvg
  ```

### `-o OUTPUT`
**输出文件**

- 格式取决于命令：.xvg, .xtc, .trr, .gro, .pdb 等
- 示例：
  ```bash
  gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
  gmx trjconv -s md.tpr -f md.xtc -o fit.xtc
  ```

### `-deffnm BASENAME`
**默认文件名前缀**

- 用于 mdrun 简化输出文件命名
- 示例：
  ```bash
  gmx mdrun -s em.tpr -deffnm em  # 生成 em.log, em.edr, em.trr 等
  ```

### `-c INPUT`
**输入结构文件**

- 用于 grompp, editconf 等命令
- 格式：.gro, .pdb
- 示例：
  ```bash
  gmx grompp -f minim.mdp -c ions.gro -p topol.top -o em.tpr
  ```

### `-p INPUT`
**输入拓扑文件（.top）**

- 用于 grompp, genion
- 格式：仅 .top

---

## 时间选择参数

### `-b TIME`
**起始时间**

- 单位：皮秒（ps）
- 示例：
  ```bash
  gmx rms -s md.tpr -f md.xtc -b 10000 -o rmsd.xvg
  ```

### `-e TIME`
**结束时间**

- 单位：皮秒（ps）
- 示例：
  ```bash
  gmx rms -s md.tpr -f md.xtc -e 50000 -o rmsd.xvg
  ```

### `-dt TIME`
**时间步长**

- 单位：皮秒（ps）
- 用于选择输出帧
- 示例：
  ```bash
  gmx trjconv -s md.tpr -f md.xtc -o reduced.xtc -dt 100
  ```

### `-tu ENUM`
**时间单位**

- 选项：fs, ps, ns, us, ms, s
- 示例：
  ```bash
  gmx trjconv -s md.tpr -f md.xtc -b 10 -tu ns -o out.xtc
  ```

---

## 轨迹处理参数

### `-pbc ENUM`
**周期性边界条件处理**

- **选项**：
  - `none`：不处理 PBC（默认）
  - `mol`：将分子质心放入盒子（需要 .tpr 文件）
  - `res`：将残基质心放入盒子
  - `atom`：将所有原子放入盒子
  - `nojump`：检查原子是否跳过盒子边界并放回
  - `cluster`：聚类选中的原子
  - `whole`：仅使断裂分子完整
- 示例：
  ```bash
  echo "Protein" | gmx trjconv -s md.tpr -f md.xtc -o mol.xtc -pbc mol
  echo "Protein" | gmx trjconv -s md.tpr -f md.xtc -o nojump.xtc -pbc nojump
  ```

### `-[no]center`
**居中坐标**

- 开关选项，默认 no
- 示例：
  ```bash
  echo "Protein\nProtein" | gmx trjconv -s md.tpr -f md.xtc -o centered.xtc -center
  ```

### `-fit ENUM`
**拟合轨迹到参考结构**

- **选项**：
  - `none`：不拟合（默认）
  - `rot+trans`：旋转 + 平移（最常用）
  - `rotxy+transxy`：xy 平面旋转 + xy 平移
  - `translation`：仅平移
  - `transxy`：仅 xy 平移
  - `progressive`：渐进式拟合
- 示例：
  ```bash
  echo "Backbone\nProtein" | gmx trjconv -s md.tpr -f md.xtc -o fit.xtc -fit rot+trans
  ```

### `-ur ENUM`
**晶胞表示方式**

- **选项**：
  - `rect`：矩形（默认）
  - `tric`：三斜
  - `compact`：紧凑表示
- 示例：
  ```bash
  echo "Protein" | gmx trjconv -s md.tpr -f md.xtc -o compact.xtc -ur compact
  ```

### `-boxcenter ENUM`
**盒子中心位置**

- **选项**：
  - `tric`：盒子向量和的一半
  - `rect`：盒子对角线的一半
  - `zero`：零点

---

## 性能参数

以下参数主要用于 `gmx mdrun`。

### `-nt INT`
**总线程数**

- 0 表示自动检测
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -nt 4
  ```

### `-ntmpi INT`
**线程 MPI 进程数**

- 0 表示自动检测
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -ntmpi 4
  ```

### `-ntomp INT`
**每个 MPI 进程的 OpenMP 线程数**

- 0 表示自动检测
- 示例：
  ```bash
  mpirun -np 2 gmx_mpi mdrun -s md.tpr -deffnm md -ntomp 4
  ```

### `-nb ENUM`
**非键相互作用计算位置**

- **选项**：
  - `auto`：自动选择（默认）
  - `cpu`：使用 CPU
  - `gpu`：使用 GPU
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -ntomp 4 -nb gpu
  ```

### `-pme ENUM`
**PME 计算位置**

- **选项**：`auto`, `cpu`, `gpu`
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -nb gpu -pme gpu
  ```

### `-pmefft ENUM`
**PME FFT 计算位置**

- **选项**：`auto`, `cpu`, `gpu`

### `-bonded ENUM`
**键合相互作用计算位置**

- **选项**：`auto`, `cpu`, `gpu`

### `-update ENUM`
**更新和约束计算位置**

- **选项**：`auto`, `cpu`, `gpu`

### `-[no]tunepme`
**优化 PME 负载**

- 开关选项，默认 yes
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -notunepme
  ```

### `-gpu_id STRING`
**GPU 设备 ID 列表**

- 指定可用的 GPU 设备 ID
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -gpu_id 01
  ```

### `-gputasks STRING`
**GPU 任务映射**

- 指定每个任务映射到哪个 GPU

---

## 其他常用参数

### `-maxwarn INT`
**最大警告忽略数**

- 用于 grompp，谨慎使用
- 示例：
  ```bash
  gmx grompp -f md.mdp -c npt.gro -p topol.top -o md.tpr -maxwarn 1
  ```

### `-cpt REAL`
**检查点间隔**

- 单位：分钟，默认 15
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -cpt 30
  ```

### `-nsteps INT`
**覆盖步数**

- -1 表示无限，-2 表示使用 .mdp 设置（默认）
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -nsteps 100000
  ```

### `-replex INT`
**副本交换周期**

- 单位：步数
- 示例：
  ```bash
  gmx mdrun -s md.tpr -deffnm md -replex 1000
  ```

### `-select STRING`
**选择字符串**

- 使用选择语言选择原子
- 示例：
  ```bash
  gmx select -s md.tpr -select "resid 1 to 100" -on res1-100.ndx
  gmx select -s md.tpr -select "backbone" -on backbone.ndx
  gmx select -s md.tpr -select "protein and not hydrogen" -on protein_noH.ndx
  ```

---

## 参数分组

| 分组 | 参数 |
|------|------|
| 输入文件 | `-f`, `-s`, `-n`, `-c`, `-p` |
| 输出文件 | `-o`, `-deffnm` |
| 时间选择 | `-b`, `-e`, `-dt`, `-tu` |
| 轨迹处理 | `-pbc`, `-center`, `-fit`, `-ur` |
| 性能 | `-nt`, `-ntmpi`, `-ntomp`, `-nb`, `-pme`, `-bonded`, `-update`, `-gpu_id` |
| 控制 | `-maxwarn`, `-cpt`, `-nsteps`, `-replex` |

---

## 最佳实践

1. **始终使用 `gmx <command> -h`** 查看准确的参数信息
2. **注意版本差异**：不同 GROMACS 版本参数可能不同
3. **使用绝对路径**：在集群或复杂目录结构中运行时
4. **记录所有参数**：以便复现
5. **小系统测试**：在大模拟前先测试

# 周期性校正

## 概述

周期性边界条件（PBC, Periodic Boundary Conditions）校正消除分子跨越模拟盒边界产生的问题。仅当轨迹质量问题（如 RMSD 突然跳跃）或用户要求时应用，非必须步骤。适用于分子跨越盒边界、RMSD显示突变、可视化显示分子碎片化。

## 工作流程

### 输入文件
- `-s`：结构文件（.tpr）
- `-f`：轨迹文件（.xtc）

### 命令

```bash
# 步骤 1a：提取第一帧结构
echo -e "Protein\n" | gmx trjconv -s md.tpr -f md.xtc -o first_frame.gro -dump 0
```
- **目的**：提取轨迹第一帧用于查找中心原子
- **参数说明**：
  - `-dump 0`：提取时间戳为 0 的帧（第一帧）
  - `-o first_frame.gro`：输出 GRO 格式结构文件
- **管道输入**：`"Protein\n"` 选择输出的原子组

```bash
# 步骤 1b：找到蛋白质几何中心最近的原子
dit find_center -f first_frame.gro
```
- **目的**：找到蛋白质几何中心最近的原子，输出原子索引
- **参数说明**：
  - `-f first_frame.gro`：输入 GRO 结构文件
- **输出**：终端显示最接近几何中心的原子索引和坐标
- **原理**：计算所有蛋白质原子的几何中心，然后找到距离该中心最近的原子

```bash
# 步骤 1c：创建中心原子索引组
# 若无 index.ndx，先生成默认索引文件
echo -e "q\n" | gmx make_ndx -f md.tpr -o index.ndx
# 追加中心原子索引组
printf "\n[ CenterAtom ]\n{原子索引}\n" >> index.ndx
```
- **目的**：创建包含中心原子的新索引组
- **参数说明**：
  - `gmx make_ndx -f md.tpr -o index.ndx`：生成默认索引文件
  - `q`：直接退出 make_ndx，保留默认组
  - `>> index.ndx`：追加新索引组到文件末尾
- **格式说明**：`[ CenterAtom ]` 为组名，`{原子索引}` 替换为步骤 1b 输出的原子编号
- **示例**：若原子索引为 567，则执行：`printf "\n[ CenterAtom ]\n567\n" >> index.ndx`
- **注意**：若已有 index.ndx 文件，可跳过第一步，直接执行追加命令

```bash
# 步骤 1d：以中心原子居中
echo -e "CenterAtom\nProtein\n" | gmx trjconv -s md.tpr -f md.xtc -n index.ndx -o center.xtc -pbc atom -center
```
- **目的**：以中心原子为参考将蛋白质居中到盒子中心
- **参数说明**：
  - `-n index.ndx`：输入自定义索引文件
  - `-pbc atom`：以原子为单位处理周期性
  - `-center`：启用居中功能
- **管道输入**：`"CenterAtom\nProtein\n"` 第一个 CenterAtom 为居中参考组（单个原子），第二个 Protein 为输出组
- **选择原因**：以单个中心原子居中可避免蛋白质组居中时的漂移问题，对于蛋白质构象变化大的模拟更稳定

### 备选方法：以蛋白质组居中

```bash
# 直接以蛋白质组居中（适用于构象变化小的模拟）
echo -e "Protein\nProtein\n" | gmx trjconv -s md.tpr -f md.xtc -o center.xtc -pbc atom -center
```
- **目的**：将蛋白质整体居中到模拟盒中心
- **管道输入**：`"Protein\nProtein\n"` 第一个 Protein 为居中参考组，第二个 Protein 为输出组
- **适用场景**：蛋白质构象变化较小、对居中精度要求不高的情况

---

```bash
# 步骤 2：保持分子完整性
echo -e "Protein\n" | gmx trjconv -s md.tpr -f center.xtc -o mol.xtc -pbc mol -ur compact
```
- **目的**：确保分子不被盒子边界切断，保持分子完整
- **参数说明**：
  - `-f center.xtc`：输入上一步的居中轨迹
  - `-o mol.xtc`：输出分子完整的轨迹
  - `-pbc mol`：以分子为单位处理周期性，确保同一分子的所有原子在同一周期镜像中
  - `-ur compact`：使用紧凑单位元表示，将所有原子放置在最紧凑的周期性图像中
- **管道输入**：`"Protein\n"` 选择输出组

```bash
# 步骤 3：消除整体平移和旋转（可选）
echo -e "Backbone\nProtein\n" | gmx trjconv -s md.tpr -f mol.xtc -o fit.xtc -fit rot+trans
```
- **目的**：消除蛋白质的整体平移和旋转，仅保留内部运动
- **参数说明**：
  - `-f mol.xtc`：输入上一步的轨迹
  - `-o fit.xtc`：输出拟合后的最终轨迹
  - `-fit rot+trans`：拟合消除旋转和平移，使结构最小二乘对齐到参考
- **管道输入**：`"Backbone\nProtein\n"` 第一个 Backbone 为最小二乘拟合参考组，第二个 Protein 为输出组
- **注意**：此步骤可选，仅当需要消除整体运动时使用

```bash
# 步骤 4：更新拓扑文件
echo -e "Protein\n" | gmx convert-tpr -s md.tpr -o fit.tpr
```
- **目的**：生成与修正后轨迹匹配的新拓扑文件
- **参数说明**：
  - `-s md.tpr`：输入原始拓扑文件
  - `-o fit.tpr`：输出更新后的拓扑文件
- **管道输入**：`"Protein\n"` 选择要保留的原子组（与轨迹输出组一致）
- **注意**：如果轨迹原子数与原 tpr 不同，必须执行此步骤

### 输出
- **fit.xtc**：修正后的轨迹文件
- **fit.tpr**：修正后的拓扑文件

### 验证
```bash
# 提取样本结构进行目视检查
echo -e "Protein\n" | gmx trjconv -s md.tpr -f fit.xtc -o fit.pdb -dt 1000
```
- **目的**：每隔 1000 ps 提取一帧用于可视化检查
- **参数说明**：
  - `-dt 1000`：时间间隔 1000 ps，减少输出帧数

## 原子组选择原则

| 场景 | 居中参考组 | 拟合参考组 | 输出组 |
|------|-----------|-----------|--------|
| 纯蛋白质 | Protein或中心原子 | Backbone | Protein |
| 蛋白质-配体复合物 | Protein或中心原子 | Backbone | Protein_Lig |
| 膜蛋白 | Protein或中心原子 | Backbone | System |

## 结果判断

- **修正成功**：分子完整无碎片化、蛋白质/配体居中、RMSD 曲线没有突升突降
- **需要修正**：RMSD 显示突变、分子跨越盒边界、可视化显示碎片化

## 常见问题

**Q: 修正后分子仍然碎片化？**  
A: 检查原子组选择，确保居中参考组包含所有应保持完整的原子。

**Q: tpr 和 xtc 原子数不匹配？**  
A: 在组选择更改后运行 `gmx convert-tpr` 更新拓扑文件。

---
name: molecular-docking-autodock
description: 实现分子对接全流程自动化，支持输入蛋白结构文件（PDB格式）、小分子SMILES表达式、口袋位置描述（文本描述或坐标范围），输出对接后打分最高的复合物结构及对接打分结果，默认使用AutoDock VINA算法。使用场景：用户需要进行蛋白-小分子对接预测结合模式、筛选小分子配体、获取对接复合物结构时触发。
---

# 分子对接自动化技能（AutoDock VINA实现）

## Overview
本技能提供端到端的蛋白-小分子分子对接自动化流程，无需手动处理中间文件，支持文本描述的口袋位置自动识别，内置AutoDock VINA作为默认对接引擎，输出对接后TopN复合物结构、结合亲和力打分及结果可视化。

## 依赖安装
运行前确保已安装以下依赖：
```bash
conda install -c conda-forge autodock-vina pymol-open-source rdkit openbabel
pip install meeko biopython
```
若需要从文本描述预测口袋位置，需额外安装`p2rank`：
```bash
# 安装p2rank口袋预测工具
wget https://github.com/rdk/p2rank/releases/download/2.4/p2rank_2.4.tar.gz
tar -xzf p2rank_2.4.tar.gz && export PATH=$PATH:$(pwd)/p2rank_2.4
```

## 核心工作流程
### 步骤1：输入校验
- 校验输入蛋白文件是否为有效PDB格式
- 校验小分子SMILES是否合法可生成3D构象
- 解析口袋位置：支持两种输入形式
  1. 坐标范围：`center_x=xxx center_y=xxx center_z=xxx size_x=xxx size_y=xxx size_z=xxx`
  2. 文本描述：如"结合位点在蛋白的ATP结合口袋"、"靠近残基LYS123和ASP145的区域"，将自动调用p2rank预测口袋或根据残基编号计算坐标

### 步骤2：蛋白预处理
- 自动去除蛋白中的水分子、非标准残基
- 加氢、计算电荷
- 输出预处理后的蛋白PDBQT格式文件

### 步骤3：小分子预处理
- 从SMILES生成最优3D构象
- 加氢、计算Gasteiger电荷
- 输出小分子PDBQT格式文件

### 步骤4：运行AutoDock VINA对接
- 默认exhaustiveness=8，num_modes=9
- 支持自定义对接参数调整

### 步骤5：结果输出
- 输出打分最高的1个（可配置）复合物结构（PDB格式，蛋白+配体）
- 输出所有对接结果的结合亲和力打分表
- 可选生成对接结果可视化图片

## 脚本使用说明
### scripts/molecular_docking.py
主执行脚本，调用方式：
```python
python scripts/molecular_docking.py \
  --protein path/to/protein.pdb \
  --smiles "C1=CC=C(C=C1)C(=O)O" \
  --pocket "center_x=10.5 center_y=20.3 center_z=-5.2 size_x=20 size_y=20 size_z=20" \
  --output_dir ./docking_results
```
参数说明：
- `--protein`: 输入蛋白PDB文件路径
- `--smiles`: 小分子SMILES表达式
- `--pocket`: 口袋位置描述，支持坐标格式或文本描述
- `--output_dir`: 结果输出目录，默认./docking_results
- `--num_modes`: 输出对接构象数目，默认1
- `--exhaustiveness`: 对接搜索穷尽度，默认8

## references/
- `references/autodock_vina_manual.md`: AutoDock VINA官方使用手册
- `references/pocket_prediction_guide.md`: 口袋位置描述规范及预测工具使用指南

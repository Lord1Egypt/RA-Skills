# 多序列比对与建树

## MAFFT 比对

```bash
# 自动选择最佳算法
mafft --auto --thread N input.fasta > aligned.fasta

# 大数据集用 FFT-NS-2（快）
mafft --retree 2 --thread N input.fasta > aligned.fasta

# 高精度用 L-INS-i（慢但准）
mafft --localpair --maxiterate 1000 --thread N input.fasta > aligned.fasta
```

### 选择指南

| 序列数 | 推荐策略 |
|--------|----------|
| < 200 | `--auto` |
| 200-2000 | `--auto` 或 `--retree 2` |
| > 2000 | `--retree 2` 或 PartTree |

## FastTree 建树

```bash
# 蛋白序列
fasttree -gamma input.fasta > tree.nwk 2>fasttree.log

# 核酸序列
fasttree -nt -gamma input.fasta > tree.nwk 2>fasttree.log

# 带 bootstrap（约 10x 慢）
fasttree -gamma -boot 1000 input.fasta > tree_boot.nwk
```

### FastTree vs IQ-TREE

| 特性 | FastTree | IQ-TREE |
|------|----------|---------|
| 速度 | 快（近似 ML） | 较慢（精确 ML） |
| Bootstrap | 支持 | 支持（ultrafast） |
| 模型选择 | 自动 | 自动（ModelFinder） |
| 大数据 | ✅ 好 | ⚠️ 内存大 |
| 推荐场景 | 大作业/快速探索 | 正式发表 |

## 树后处理

```R
library(ape)

# 读取
tree <- read.tree("tree.nwk")

# 中点根化
tree_rooted <- midpoint(tree)

# 梯子化
tree_rooted <- ladderize(tree_rooted)

# 保存
write.tree(tree_rooted, "tree_rooted.nwk")
```

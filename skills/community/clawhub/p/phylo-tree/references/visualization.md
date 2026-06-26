# 系统发育树可视化

## 基础绘图（ape）

```R
library(ape)
tree <- read.tree("tree.nwk")

# 四种基本类型
plot(tree, type = "phylogram")   # 系统树图
plot(tree, type = "cladogram")   # 支序图
plot(tree, type = "fan")         # 环形
plot(tree, type = "unrooted")    # 无根图
```

## phytools 美化

```R
library(phytools)

# 彩色末端
colors <- setNames(rainbow(n), tree$tip.label)
plotTree(tree, type = "phylogram", fsize = 0.7,
         color = colors[tree$tip.label])

# 带节点标签
plotTree(tree, fsize = 0.6, ftype = "i")
nodelabels(tree$node.label, frame = "none", cex = 0.5)
```

## ggtree（高级）

```R
library(ggtree)
library(ggplot2)

ggtree(tree, layout = "circular") +
  geom_tiplab(size = 2, align = TRUE) +
  theme_tree2() +
  ggtitle("Phylogenetic Tree")
```

## 推荐配色

```R
library(RColorBrewer)
# 分类数据
brewer.pal(8, "Set2")
brewer.pal(9, "Set1")
# 渐变数据
brewer.pal(9, "YlOrRd")
```

## 输出格式

| 格式 | 优点 | 缺点 |
|------|------|------|
| PDF | 矢量图，无限放大 | 文件大 |
| PNG | 兼容性好 | 分辨率固定 |
| SVG | 矢量+可编辑 | 浏览器支持 |

**推荐：** PDF 用于论文，PNG 用于展示

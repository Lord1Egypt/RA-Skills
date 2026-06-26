# R Scripts

Publication-quality phylogenetic tree visualization using R.

## Available Scripts

### plot_tree.R

**Purpose:** Generate multiple tree layouts (rectangular, circular, cladogram, unrooted)

**Usage:**
```bash
Rscript plot_tree.R <tree.newick> <output_prefix>
```

**Example:**
```bash
Rscript plot_tree.R tree.contree output/tree
```

**Output:**
- `tree_rectangular.pdf` - Standard phylogram (PDF, vector)
- `tree_rectangular.png` - Standard phylogram (PNG, 300 DPI)
- `tree_circular.pdf` - Circular tree (PDF, vector)
- `tree_circular.png` - Circular tree (PNG, 300 DPI)
- `tree_cladogram.pdf` - Topology only (no branch lengths)
- `tree_unrooted.pdf` - Unrooted tree

**Dependencies:**
```R
install.packages("ape")
install.packages("phytools")
```

Or via conda:
```bash
conda install -c conda-forge r-ape r-phytools
```

**Features:**
- ✅ Multiple tree layouts
- ✅ Bootstrap support values displayed
- ✅ Publication-quality (300 DPI PNG, vector PDF)
- ✅ Automatic tree statistics
- ✅ Scale bars
- ✅ Customizable colors and sizes

## Tree Layouts

### 1. Rectangular (Phylogram)
- Shows branch lengths (evolutionary distance)
- Best for: Showing evolutionary relationships with time
- Use when: Branch lengths are meaningful

### 2. Circular (Fan)
- Radial layout, saves space
- Best for: Large trees (>100 sequences)
- Use when: You need to fit many sequences

### 3. Cladogram
- Topology only, no branch lengths
- Best for: Showing groupings/clades
- Use when: Branch lengths are unreliable or not important

### 4. Unrooted
- No root assumption
- Best for: Showing relationships without directionality
- Use when: Root position is uncertain

## Integration with Shell Scripts

The phylogeny script can call R automatically:

```bash
# In 04_phylogeny.sh
if command -v Rscript &> /dev/null; then
    Rscript scripts/R/plot_tree.R tree.contree output/tree
fi
```

## Customization

Edit `plot_tree.R` to customize:

```R
# Change colors
edge.color = "blue"
tip.color = "red"

# Change sizes
cex = 0.8  # Larger labels
edge.width = 3  # Thicker branches

# Change layout
type = "phylogram"  # or "fan", "cladogram", "unrooted"

# Add colors by clade
tip_colors <- rep("black", length(tree$tip.label))
tip_colors[1:50] <- "red"  # First 50 tips in red
plot(tree, tip.color = tip_colors)
```

## Advanced Usage

### Color by Bootstrap Support

```R
# Color branches by bootstrap support
edge_colors <- ifelse(as.numeric(tree$node.label) >= 95, "green",
                     ifelse(as.numeric(tree$node.label) >= 70, "orange", "red"))
plot(tree, edge.color = edge_colors)
```

### Highlight Specific Clades

```R
# Highlight a clade
clade_tips <- c("seq1", "seq2", "seq3")
clade_node <- getMRCA(tree, clade_tips)
plot(tree)
nodelabels(node = clade_node, pch = 21, bg = "yellow", cex = 2)
```

### Add Heatmap

```R
# Add trait heatmap next to tree
library(phytools)
traits <- matrix(rnorm(length(tree$tip.label) * 3), 
                 ncol = 3,
                 dimnames = list(tree$tip.label, c("Trait1", "Trait2", "Trait3")))
phylo.heatmap(tree, traits)
```

## Tree Statistics

The script automatically calculates:

- **Tree depth:** Mean/median/min/max distance from root to tips
- **Branch lengths:** Total tree length, mean/median branch length
- **Bootstrap support:** Distribution of support values

Example output:
```
Tree Statistics
================================================================================
Tree depth:
  Mean: 0.234 substitutions/site
  Median: 0.228 substitutions/site
  Min: 0.180 substitutions/site
  Max: 0.310 substitutions/site

Branch lengths:
  Total tree length: 12.345 substitutions/site
  Mean branch length: 0.027 substitutions/site
  Median branch length: 0.018 substitutions/site

Bootstrap support:
  Strong (≥95%): 288 (63.6%)
  Moderate (70-95%): 105 (23.2%)
  Weak (<70%): 60 (13.2%)
  Total branches: 453
```

## Troubleshooting

**Issue:** `Error: package 'ape' is not installed`  
**Solution:** `install.packages("ape")`

**Issue:** `Error: package 'phytools' is not installed`  
**Solution:** `install.packages("phytools")`

**Issue:** Tree labels are too small  
**Solution:** Increase `cex` parameter: `cex = 0.8` or `cex = 1.0`

**Issue:** Tree is too crowded  
**Solution:** Use circular layout or increase figure size:
```R
pdf("tree.pdf", width = 20, height = 30)
```

**Issue:** Bootstrap values overlap  
**Solution:** Adjust position with `adj` parameter:
```R
nodelabels(tree$node.label, adj = c(0.5, -1.0))
```

## Performance

**Typical runtime:**
- 100 sequences: <5 seconds
- 500 sequences: <10 seconds
- 1000 sequences: <30 seconds

**Memory usage:**
- ~50 MB for 100 sequences
- ~200 MB for 500 sequences
- ~500 MB for 1000 sequences

## Citation

If you use these R scripts, please cite:

- Paradis, E. & Schliep, K. (2019). "ape 5.0: an environment for modern phylogenetics and evolutionary analyses in R". *Bioinformatics* 35: 526-528.

- Revell, L.J. (2012). "phytools: An R package for phylogenetic comparative biology". *Methods Ecol Evol* 3: 217-223.

# Visualization - Publication-Quality Figures

## Overview

Generate publication-ready figures (300 DPI) for all analysis results: conservation heatmaps, coevolution networks, phylogenetic trees, and quality metrics.

## Figure Standards

### Publication Requirements

**Resolution:** 300 DPI minimum (600 DPI for line art)  
**Format:** PNG (raster), PDF (vector), or SVG (vector)  
**Color:** Colorblind-friendly palettes  
**Fonts:** Arial, Helvetica, or Times (10-12 pt)  
**Size:** Single column (3.5"), double column (7"), or full page

### Nature/Science Standards

- Clear axis labels with units
- Legible legends (outside plot area)
- Consistent color schemes across figures
- High contrast (black/white printable)
- Minimal decorations (no 3D effects, shadows)

## Figure Types

### 1. Conservation Heatmap

**Purpose:** Show conservation landscape across alignment

**Data:** Shannon entropy for each position

**Code:**
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Read conservation data
df = pd.read_csv('conservation_detailed.csv')

# Create matrix (sequences × positions)
# For visualization, we show entropy profile
fig, ax = plt.subplots(figsize=(20, 4))

# Plot entropy profile
positions = df['position'].values
entropies = df['norm_entropy'].values

ax.fill_between(positions, 0, entropies, 
                 where=(entropies < 0.3), 
                 alpha=0.5, color='green', label='Highly conserved')
ax.fill_between(positions, 0, entropies, 
                 where=((entropies >= 0.3) & (entropies < 0.6)), 
                 alpha=0.5, color='yellow', label='Moderately conserved')
ax.fill_between(positions, 0, entropies, 
                 where=(entropies >= 0.6), 
                 alpha=0.5, color='red', label='Variable')

ax.plot(positions, entropies, linewidth=1, color='black')
ax.axhline(y=0.3, color='green', linestyle='--', linewidth=0.5)
ax.axhline(y=0.6, color='orange', linestyle='--', linewidth=0.5)

ax.set_xlabel('Alignment Position', fontsize=12)
ax.set_ylabel('Normalized Entropy', fontsize=12)
ax.set_title('Conservation Landscape', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('conservation_landscape.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 2. Coevolution Network

**Purpose:** Visualize coevolved position pairs and hub positions

**Data:** Mutual information scores, hub degrees

**Code:**
```python
import networkx as nx
import matplotlib.pyplot as plt
import json

# Read network data
with open('network_data.json', 'r') as f:
    data = json.load(f)

# Build graph
G = nx.Graph()
for node in data['nodes']:
    G.add_node(node['id'], degree=node['degree'])

for edge in data['edges']:
    if edge['weight'] > 0.5:  # Only strong coevolution
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

# Layout
pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

# Node colors (hubs in red)
hub_threshold = 5
node_colors = ['red' if G.nodes[node].get('degree', 0) >= hub_threshold 
               else 'lightblue' for node in G.nodes()]

# Node sizes (proportional to degree)
node_sizes = [G.degree(node) * 100 for node in G.nodes()]

# Edge widths (proportional to MI)
edge_widths = [G[u][v]['weight'] * 5 for u, v in G.edges()]

# Plot
fig, ax = plt.subplots(figsize=(12, 12))

nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                       node_size=node_sizes, alpha=0.7, ax=ax)
nx.draw_networkx_edges(G, pos, width=edge_widths, 
                       alpha=0.3, edge_color='gray', ax=ax)
nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

ax.set_title('Coevolution Network (MI > 0.5)', fontsize=16, fontweight='bold')
ax.axis('off')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='red', label='Hub (degree ≥ 5)'),
    Patch(facecolor='lightblue', label='Non-hub')
]
ax.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('coevolution_network.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 3. Phylogenetic Tree

**Purpose:** Show evolutionary relationships with bootstrap support

**Code (R):**
```R
library(ape)
library(phytools)

# Read tree
tree <- read.tree("tree.contree")

# Plot rectangular tree
pdf("phylogenetic_tree.pdf", width=12, height=20)
plot(tree, type="phylogram", cex=0.6, 
     edge.width=2, label.offset=0.01,
     edge.color="black")

# Add scale bar
add.scale.bar(cex=0.8, lwd=2)

# Add bootstrap support
nodelabels(tree$node.label, cex=0.5, 
           bg="white", frame="circle", adj=c(0.5, -0.5))

# Add title
title("Maximum Likelihood Phylogenetic Tree", 
      cex.main=1.5, font.main=2)

dev.off()
```

**Code (Python):**
```python
from Bio import Phylo
import matplotlib.pyplot as plt

# Read tree
tree = Phylo.read("tree.contree", "newick")

# Plot
fig, ax = plt.subplots(figsize=(12, 20))
Phylo.draw(tree, axes=ax, do_show=False)

ax.set_title('Maximum Likelihood Phylogenetic Tree', 
             fontsize=16, fontweight='bold')
ax.set_xlabel('Branch Length (substitutions/site)', fontsize=12)

plt.tight_layout()
plt.savefig('phylogenetic_tree.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 4. Bootstrap Distribution

**Purpose:** Show confidence in tree topology

**Code:**
```python
from Bio import Phylo
import matplotlib.pyplot as plt
import numpy as np

# Read tree and extract bootstrap values
tree = Phylo.read("tree.contree", "newick")
bootstrap_values = []

for clade in tree.find_clades():
    if clade.confidence is not None:
        bootstrap_values.append(clade.confidence)

# Plot histogram
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(bootstrap_values, bins=20, color='steelblue', 
        edgecolor='black', alpha=0.7)

ax.axvline(x=95, color='green', linestyle='--', linewidth=2,
           label='Strong support (≥95%)')
ax.axvline(x=70, color='orange', linestyle='--', linewidth=2,
           label='Moderate support (≥70%)')

ax.set_xlabel('Bootstrap Support (%)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Bootstrap Support Distribution', fontsize=14, fontweight='bold')
ax.legend()

# Add statistics
mean_bs = np.mean(bootstrap_values)
median_bs = np.median(bootstrap_values)
ax.text(0.05, 0.95, f'Mean: {mean_bs:.1f}%\nMedian: {median_bs:.1f}%',
        transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))

plt.tight_layout()
plt.savefig('bootstrap_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 5. Hub Heatmap

**Purpose:** Show coevolution strength between hub positions

**Code:**
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Read coevolution data
df = pd.read_csv('coevolution_detailed.csv')

# Read hub positions
hubs = []
with open('hub_positions.txt', 'r') as f:
    for line in f:
        if line.startswith('Position'):
            pos = int(line.split()[1].rstrip(':'))
            hubs.append(pos)

# Top 10 hubs
hubs = hubs[:10]

# Build matrix
matrix = np.zeros((len(hubs), len(hubs)))

for _, row in df.iterrows():
    if row['pos1'] in hubs and row['pos2'] in hubs:
        i = hubs.index(row['pos1'])
        j = hubs.index(row['pos2'])
        matrix[i, j] = row['MI']
        matrix[j, i] = row['MI']

# Plot
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(matrix, cmap='YlOrRd', 
            xticklabels=hubs, yticklabels=hubs,
            cbar_kws={'label': 'Mutual Information'},
            square=True, linewidths=0.5, ax=ax)

ax.set_title('Hub Position Coevolution Heatmap', 
             fontsize=14, fontweight='bold')
ax.set_xlabel('Position', fontsize=12)
ax.set_ylabel('Position', fontsize=12)

plt.tight_layout()
plt.savefig('hub_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 6. Quality Metrics Summary

**Purpose:** Show dataset quality metrics

**Code:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Example metrics (replace with actual values)
metrics = {
    'Original sequences': 1000,
    'After QC': 100,
    'Highly conserved': 32,
    'Coevolved pairs': 9552,
    'Strong bootstrap (≥95%)': 288
}

# Plot bar chart
fig, ax = plt.subplots(figsize=(10, 6))

categories = list(metrics.keys())
values = list(metrics.values())

bars = ax.bar(categories, values, color='steelblue', edgecolor='black')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=10)

ax.set_ylabel('Count', fontsize=12)
ax.set_title('Analysis Quality Metrics', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('quality_metrics.png', dpi=300, bbox_inches='tight')
plt.close()
```

## Color Palettes

### Colorblind-Friendly Palettes

**Okabe-Ito palette (recommended):**
```python
colors = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'red': '#D55E00',
    'pink': '#CC79A7',
    'black': '#000000'
}
```

**Viridis (sequential):**
```python
import matplotlib.pyplot as plt
cmap = plt.cm.viridis
```

**RdYlGn (diverging):**
```python
cmap = plt.cm.RdYlGn_r  # Reversed (red=high, green=low)
```

## Figure Composition

### Multi-Panel Figures

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Panel A: Conservation
ax1 = fig.add_subplot(gs[0, :])
# ... plot conservation ...
ax1.text(-0.05, 1.05, 'A', transform=ax1.transAxes,
         fontsize=16, fontweight='bold')

# Panel B: Coevolution network
ax2 = fig.add_subplot(gs[1, 0])
# ... plot network ...
ax2.text(-0.05, 1.05, 'B', transform=ax2.transAxes,
         fontsize=16, fontweight='bold')

# Panel C: Bootstrap distribution
ax3 = fig.add_subplot(gs[1, 1])
# ... plot bootstrap ...
ax3.text(-0.05, 1.05, 'C', transform=ax3.transAxes,
         fontsize=16, fontweight='bold')

plt.savefig('figure_combined.png', dpi=300, bbox_inches='tight')
```

## Export Formats

### Raster (PNG, TIFF)

**Advantages:** Universal compatibility, exact rendering  
**Disadvantages:** Fixed resolution, large file size

```python
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.savefig('figure.tiff', dpi=600, bbox_inches='tight')  # For print
```

### Vector (PDF, SVG, EPS)

**Advantages:** Scalable, small file size, editable  
**Disadvantages:** Complex figures may render slowly

```python
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')
plt.savefig('figure.eps', bbox_inches='tight')  # For LaTeX
```

## Common Issues

### Issue 1: Text Too Small

**Problem:** Labels unreadable at publication size

**Solution:**
```python
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
```

### Issue 2: Overlapping Labels

**Problem:** Axis labels overlap

**Solution:**
```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

### Issue 3: Low Contrast

**Problem:** Colors too similar

**Solution:**
- Use colorblind-friendly palettes
- Test in grayscale
- Increase line widths

### Issue 4: Large File Size

**Problem:** PNG files > 10 MB

**Solution:**
- Reduce DPI (300 is usually sufficient)
- Use vector formats (PDF, SVG)
- Compress with `pngquant` or `optipng`

## Automation Script

Complete visualization pipeline:

```bash
#!/bin/bash
# Generate all figures

python3 plot_conservation.py
python3 plot_coevolution.py
python3 plot_phylogeny.py
python3 plot_bootstrap.py
python3 plot_hub_heatmap.py
python3 plot_quality_metrics.py

echo "All figures generated!"
```

## References

1. Rougier, N.P. et al. (2014). "Ten simple rules for better figures". *PLoS Comput Biol* 10(9): e1003833.

2. Kelleher, J. & Wagener, T. (2011). "Ten guidelines for effective data visualization in scientific publications". *Environ Model Softw* 26(6): 822-827.

3. Crameri, F. et al. (2020). "The misuse of colour in science communication". *Nat Commun* 11: 5444.

## See Also

- [Conservation Analysis](02-conservation.md) - Data for conservation plots
- [Coevolution Analysis](03-coevolution.md) - Data for network plots
- [Phylogenetic Analysis](04-phylogeny.md) - Data for tree plots

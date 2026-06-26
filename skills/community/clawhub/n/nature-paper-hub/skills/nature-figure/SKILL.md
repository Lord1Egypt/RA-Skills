---
name: nature-figure
description: Generate publication-quality figures for Nature-series journals using Python (matplotlib) or R (ggplot2). Trigger when user wants to create, polish, or redesign scientific figures for high-impact journals. Handles multi-panel layouts, Nature color palettes, correct typography, and exports SVG/PDF/PNG.
---

# nature-figure

## Purpose
Generate multi-panel scientific figures that meet Nature portfolio visual standards:
correct typography, semantic colour palette, accessible design, and editable SVG output.

---

## Trigger Conditions
Activate when user mentions:
- "画图" / "figure" / "plot" / "科研绘图"
- "Nature figure" / "publication figure" / "publication plot"
- "matplotlib" / "ggplot" / "seaborn"
- "配色" / "color palette" / "color scheme"
- Wants to improve or reformat an existing figure

---

## Nature Figure Standards

### Typography
- Font family: **Arial** or **Helvetica** (sans-serif, never Times New Roman in figures)
- Minimum font size in final print: **7 pt** (axis labels, tick labels)
- Panel labels (a, b, c...): **8 pt bold**, lowercase
- Figure title (if any): not embedded in figure — goes in legend
- All text must be editable (not rasterized)

### Size & Resolution
| Format | Width | Resolution |
|--------|-------|------------|
| Single column | 89 mm (3.5 in) | 300 DPI min |
| 1.5 column | 120 mm (4.7 in) | 300 DPI min |
| Double column | 183 mm (7.2 in) | 300 DPI min |
| Line art | any | **600 DPI** |
| Final submission | PDF or TIFF | vector preferred |

### Colour Palette (Nature-approved, colorblind-safe)
```python
NATURE_COLORS = {
    "blue":    "#4878CF",
    "red":     "#D65F5F", 
    "green":   "#6ACC65",
    "orange":  "#EE854A",
    "purple":  "#956CB4",
    "teal":    "#82C6E2",
    "brown":   "#D5BB67",
    "gray":    "#8C8C8C",
    # Colorblind-safe primary pair:
    "cb_blue": "#0072B2",
    "cb_orange":"#E69F00",
}
```
- Never use pure red + green together (colorblind conflict)
- Use filled symbols + different shapes for accessibility, not colour alone
- Grayscale must remain distinguishable

### Panel Architecture
- Each panel makes **one clear point**
- Panel (a): overview / schematic / representative image
- Panels (b–d): quantitative evidence
- Final panel: comparison or generalizability
- Panels are labelled **a, b, c** (lowercase bold, top-left corner)
- White background; minimal gridlines (light gray, 0.5pt)
- No chartjunk: remove top and right spines

### Statistical Annotations
- Error bars: always define in legend (mean ± s.d. or ± s.e.m.)
- Significance: *, **, ***, **** for p < 0.05, 0.01, 0.001, 0.0001; prefer exact p-values
- n must be stated (e.g., n = 5 independent experiments)
- Box plots: show median, IQR, whiskers to 1.5×IQR, individual points overlaid

---

## Workflow

### Step 0: Auto-figure from data file (fastest path)
If user provides a CSV, Excel, or JSON data file:
```bash
python3 ~/.openclaw/workspace/skills/nature-paper-hub/scripts/auto_figure.py \
  --input <data_file> \
  --output ~/Downloads/figure_<date>.pdf \
  --title "[figure title]" \
  --xlabel "X axis label" \
  --ylabel "Y axis label" \
  --type [auto|line|bar|scatter|heatmap|box]
```
The script auto-detects column types, chooses appropriate chart type, applies Nature style, and saves PDF + PNG.

### Step 1: Gather requirements (if no data file yet)
Ask the user:
1. What data do you have? (paste CSV, describe columns, or share values)
2. How many panels? What does each panel show?
3. Single/1.5/double column width?
4. Python (matplotlib/seaborn) or R (ggplot2)?
5. Any specific colour requirements or journal sub-style?

### Step 2: Generate figure code

#### Python template (matplotlib):
```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# --- Nature style settings ---
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'pdf.fonttype': 42,   # editable text in PDF
    'ps.fonttype': 42,
})

COLORS = {
    "blue": "#4878CF", "red": "#D65F5F", "green": "#6ACC65",
    "orange": "#EE854A", "purple": "#956CB4", "teal": "#82C6E2",
    "cb_blue": "#0072B2", "cb_orange": "#E69F00",
}

# --- Figure layout ---
fig = plt.figure(figsize=(7.2, 4.0))  # double column, adjust height
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.4, hspace=0.4)

ax_a = fig.add_subplot(gs[0])
ax_b = fig.add_subplot(gs[1])
ax_c = fig.add_subplot(gs[2])

# --- Panel labels ---
for ax, label in zip([ax_a, ax_b, ax_c], ['a', 'b', 'c']):
    ax.text(-0.15, 1.05, label, transform=ax.transAxes,
            fontsize=8, fontweight='bold', va='top', ha='right')

# --- YOUR DATA GOES HERE ---
# ax_a: ...
# ax_b: ...
# ax_c: ...

plt.savefig('figure1.pdf', format='pdf')
plt.savefig('figure1.png', dpi=300)
print("Saved: figure1.pdf, figure1.png")
```

#### R template (ggplot2):
```r
library(ggplot2)
library(patchwork)

# Nature theme
theme_nature <- function() {
  theme_classic(base_size = 8, base_family = "Arial") +
  theme(
    axis.line = element_line(linewidth = 0.5),
    axis.ticks = element_line(linewidth = 0.5),
    axis.ticks.length = unit(2, "pt"),
    strip.background = element_blank(),
    legend.key.size = unit(3, "mm"),
    plot.margin = margin(2, 2, 2, 2, "mm")
  )
}

nature_colors <- c(
  blue = "#4878CF", red = "#D65F5F", green = "#6ACC65",
  orange = "#EE854A", purple = "#956CB4", teal = "#82C6E2"
)

# --- YOUR PLOTS ---
# p1 <- ggplot(...) + theme_nature()
# p2 <- ggplot(...) + theme_nature()
# combined <- p1 | p2
# ggsave("figure1.pdf", combined, width = 183, height = 80, units = "mm", dpi = 300)
```

### Step 3: Validate
Before outputting, check:
- [ ] Font ≥ 7pt in all elements
- [ ] No top/right spines
- [ ] Colorblind-safe palette used
- [ ] Error bars defined
- [ ] Panel labels present (a, b, c lowercase bold)
- [ ] Resolution ≥ 300 DPI (600 for line art)
- [ ] Figure width matches column format
- [ ] PDF/SVG output for vector editability

### Step 4: Figure legend
Generate the corresponding figure legend text:
- Bold "Figure X |" prefix
- Short title (one phrase)
- One sentence per panel
- Error bar definition
- n values and statistical test used
- Scale bar definition (for images)

---

## Common Figure Types

### Line plot (time series / trends)
Use solid lines with markers; different line styles + colours for groups.

### Bar chart
Prefer horizontal bars for many categories; overlay individual data points.
Use `plt.bar()` with `edgecolor='black', linewidth=0.5`.

### Scatter plot
Include regression line with 95% CI if showing correlation.
State Pearson/Spearman r and p-value on plot.

### Heatmap
Use diverging colourmap (e.g., `RdBu_r`) for correlation; sequential for intensity.
Always include colourbar with label and units.

### Box/Violin plot
Always overlay individual data points (`stripplot` or `geom_jitter`).
State n per group.

### Schematic / Mechanism diagram
Recommend using BioRender (biorender.com) or Inkscape for schematics.
Export as SVG and embed in figure.

---

## Output
Provide the user with:
1. Complete, runnable Python or R code
2. Instructions to save in the correct format (PDF + PNG)
3. The figure legend text
4. A checklist of what to verify before submission

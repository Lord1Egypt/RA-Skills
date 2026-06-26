# MetaEdit journal-club mapping and crop notes

This reference captures a concrete correction pattern for a Science paper deck where the first-pass slides failed because support panels were handled as summaries or page-adjacent crops instead of real supplementary figures.

## Paper
- Title: Metagenomic editing of commensal bacteria in vivo using CRISPR-associated transposases
- Journal: Science
- Year: 2025
- DOI: 10.1126/science.adx7604

## Core recovery lesson
For experimental paper results slides, do not treat the support area as a flexible note box. The support area must be grounded in the same conclusion as the main figure and should use the real supplementary figure if available.

In this case, the paper PDF itself contained supplementary pages after the main article. That means support summaries were no longer acceptable once this was discovered.

## Main-figure to supplementary-figure mapping used here

### Results slide 1
- Main figure: Fig. 1
- Question: Can MetaEdit deliver efficient and highly specific in vivo insertion?
- Best support set by logic:
  - Fig. S2: CAST arrangement / self-targeting optimization behind Fig. 1B
  - Fig. S3: computational megRNA design and off-target filtering
  - Fig. S4-S5: gnotobiotic colonization workflow plus sensitive integration detection behind Fig. 1F-G
- First true support figure used in the repaired deck: Fig. S2

### Results slide 2
- Main figure: Fig. 2
- Question: Can MetaEdit hit a native target inside a complex microbiome?
- Best support set by logic:
  - Fig. S7: integration specificity across replicates and time
  - Fig. S8: alternate Bt target site with similar specificity / expression
  - Fig. S9: PCR confirmation of tagged isolates
  - Fig. S10: fitness burden decomposition
- First true support figure used in the repaired deck: Fig. S7

### Results slide 3
- Main figure: Fig. 3
- Question: Can a large metabolic payload create a controllable phenotype?
- Best support set by logic:
  - Fig. S11: selects inulin as the useful dietary lever
  - Fig. S12: shows WT Bt cannot use inulin while engineered Bt can
  - Fig. S13: limited microbiome diversity shift
  - Fig. S14: in vitro engineered ATCC-Bt comparison
- First true support figure used in the repaired deck: Fig. S11

### Results slide 4
- Main figure: Fig. 4
- Question: Can MetaEdit access genetically intractable SFB?
- Best support set by logic:
  - Fig. S15: donor colonization and FACS gating setup
  - Fig. S16: junction PCR detection over time
  - Fig. S17: microscopy / negative controls
- First true support figure used in the repaired deck: Fig. S15

## Main-figure crop lessons from this paper
Use safe full-figure crops first.

### Fig. 1 page type lesson
Watch for:
- left-side schematic/tree areas
- bottom time axis and lower labels
- right-side bar-chart labels and legends
Do not crop tightly around the central panels only.

### Fig. 2 page type lesson
Watch for:
- left phylogeny / system-tree region
- bottom abundance strips
- right legends and species text
This figure is easy to break with aesthetic crop tightening.

### Fig. 3 page type lesson
Watch for:
- top inulin-supplement labels
- E-panel side legend
- F-panel right-edge late-timepoint data
A slightly wider crop is safer than trying to make the figure look cleaner.

### Fig. 4 page type lesson
Watch for:
- FACS axis labels and titles
- microscopy labels and scale bars
- caption boundary when using a whole-page crop

## Supplementary-page crop lessons from this paper
When a support figure page is dense, a full-page miniature may technically be correct but still perform poorly on slides.

### Fig. S2 page type
- Full supplementary page is clearly figure-dominant and safe to use.
- Best fallback: whole-page safe crop with caption intact.
- Better final option if more time is available: crop around the actual A-D figure body and trim excess empty margin.

### Fig. S7 page type
- Dense multi-panel matrix across mouse replicates and time.
- Whole-page support insertion is valid but becomes hard to read when small.
- Better final option: crop the figure body tightly enough to keep axes and row/column labels while dropping excess lower whitespace.

### Fig. S11 page type
- Three-panel growth curve page with long caption.
- Safer and more readable than S7 when shrunk.
- Can often be used as a whole-page support figure.

### Fig. S15 page type
- Multi-panel supplementary figure with long caption.
- Whole-page version preserves integrity, but for final stage readability consider cropping the A-H figure body while keeping labels intact.

## What failed in the bad version
- Support area was converted into a summary card instead of a real support figure.
- The support card was treated as if it satisfied the user's main-plus-support rule.
- Rounded cards were too visible and UI-like.
- Main/support figure scale was imbalanced.
- The workflow initially missed that the supplementary figures were already present later in the same PDF.

## What the corrected version fixed
- Real supplementary figures were extracted from the back half of the PDF.
- Results slides used true support figures instead of summaries.
- Support figure pairing followed the paper logic rather than page proximity.
- Rounded corners were reduced substantially.
- Main/support blocks were given comparable external footprint.

## Remaining final-stage lesson
Even after switching to true support figures, whole-page supplementary crops can still be too dense on a talk slide. Final refinement should often move from:
- whole-page true support figure
into
- safe local crop of the support figure body
while still preserving figure identity and key labels.

## Reusable rule from this case
If a user says:
- put the support figure in, not a summary card
- make support size similar to the main figure
- stop using oversized rounded cards
then the correct response is:
1. verify whether real supplementary figures exist in the PDF or companion files
2. extract the true support figure immediately
3. place it on the same slide as the main figure at comparable footprint
4. reduce figure-frame styling to minimal or near-invisible
5. re-render and judge readability, not just correctness

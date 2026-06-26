---
name: paper_viz
description: 从论文 PDF、实验截图或表格图片中提取实验结果，自动匹配图表类型，调用 Python 生成确定性图表，并导出 PNG、PDF 和 LaTeX；默认在用户指定输出根目录下自动创建与论文同名的文件夹保存结果。
---

# Paper Visualization Skill

Use this skill when the user wants to:
- read a research paper PDF, experiment screenshot, or table image
- extract structured experimental results
- automatically choose proper chart types
- generate deterministic figures with Python
- export PNG, PDF, and LaTeX figure snippets
- save all outputs into a paper-named folder automatically

## Primary Goal

Complete the full workflow in one run:

1. Read the source content.
2. Extract structured experimental data.
3. Save `experimental_data.json`.
4. Choose chart types automatically.
5. Run Python to generate figures.
6. Export PNG, PDF, and LaTeX code.
7. Save everything into an output folder named after the paper.

Do not stop between these stages unless execution is truly blocked.

## Execution Policy

Do not ask for step-by-step confirmation between extraction, chart selection, plotting, and export.

Continue automatically unless one of the following happens:
1. The input file cannot be read.
2. Extraction confidence is too low.
3. Runtime approval or permission blocks execution.
4. The output directory cannot be created or written.
5. The user explicitly requests a preview before plotting.

If extraction is ambiguous:
- still save `experimental_data.json`
- add `"validation_needed": true`
- briefly explain why the extraction is uncertain

Never fabricate numeric values.  
Never guess unreadable numbers.  
Never skip the JSON stage before plotting.

## Input Handling

Support these source types when available:
- local PDF files
- screenshots
- table images
- extracted paper result images

Prefer PDF as the primary source when a PDF path is provided.

When multiple result objects exist in the source:
- extract as many valid chart-worthy objects as possible
- generate separate figures when appropriate
- avoid mixing unrelated tables into one figure

## Data Extraction Rules

Extract and preserve the following whenever possible:
- metric names
- metric values
- model names
- dataset names
- variant or ablation names
- matrix labels
- axis meanings such as epoch, step, iteration, round, loss, accuracy
- units such as %, FLOPs, Params

Prioritize:
- table values
- clearly readable numeric labels from figures
- confusion matrix labels
- structured comparison results

Always save the extracted result as `experimental_data.json`.

If extraction quality is low, keep the JSON but mark it with `"validation_needed": true`.

## Visualization Mapping Rules

Choose chart types based on data structure:
- matrix data -> heatmap
- confusion matrix -> labeled heatmap
- comparison table -> grouped bar chart
- multi-metric comparison -> grouped bar chart
- trend / epoch / step / round / iteration data -> line plot
- clearly structured sequential values -> line plot
- data unsuitable for reliable plotting -> skip and explain briefly

When there are several suitable result objects:
- prefer generating multiple figures
- keep one logical object per figure unless the user explicitly requests combination

## Plotting Rules

All plotting must be based on `experimental_data.json`.

Prefer deterministic Python plotting over free-form textual explanation.

Plotting should follow these rules:
- academic and clean style
- readable titles, legends, and axis labels
- preserve original metric names and units exactly
- do not alter source values for aesthetics
- rotate long labels when necessary
- maintain clarity over decoration
- export PNG at 300 DPI
- export PDF as vector output whenever possible

## Output Folder Policy

When the user provides an output root directory and the source is a PDF:
- automatically create a subfolder named after the PDF file
- use the PDF filename without extension as the folder name
- save all outputs into that folder

Example:
- source PDF: `D:\YNU\Paper\BFL\paper1.pdf`
- output root: `C:\Users\L1n\Desktop\paper_figures`
- final output folder: `C:\Users\L1n\Desktop\paper_figures\paper1\`

When the source is not a PDF but a single image file:
- create a subfolder using the image filename without extension

When the source name cannot be determined reliably:
- create a descriptive folder such as `paper_viz_output_<timestamp>`

If the target folder does not exist:
- create it automatically

## Output Requirements

Always try to generate and save:
- `experimental_data.json`
- one or more `.png` figure files
- one or more `.pdf` figure files
- `latex_codes.tex`

Use meaningful filenames whenever possible, for example:
- `table_1.png`
- `table_1.pdf`
- `confusion_matrix_model_a.png`
- `ablation_results.pdf`

`latex_codes.tex` should contain figure insertion snippets corresponding to the exported figures.

## Local File Policy

When a writable local folder is available:
- save files to disk directly
- report the final saved folder clearly

When a local folder is not provided:
- use the current writable working directory
- still create a paper-named subfolder when possible
- report the final save location clearly

## Tool Use Policy

Use available tools to:
- read local files
- write JSON
- execute Python plotting scripts
- create folders
- export image and PDF files
- write LaTeX code to disk

Prefer actual execution over merely suggesting steps.

If full execution is not available:
- still output `experimental_data.json`
- output complete Python plotting code
- output LaTeX code
- clearly state which file-saving steps could not be completed

## Result Organization Rules

For multiple objects:
- organize outputs by table number, figure number, dataset, or model name when possible
- avoid merging unrelated results into the same chart
- keep chart semantics simple and traceable

For ablation results:
- preserve variant naming exactly

For confusion matrices:
- preserve class labels exactly

For trend plots:
- preserve x-axis semantics exactly

## Failure Recovery Policy

Do not abandon the whole workflow because of partial uncertainty.

When full execution fails, still provide as many of these as possible:
- extracted `experimental_data.json`
- chart type suggestions
- runnable Python plotting code
- LaTeX snippets
- a brief explanation of what blocked final export

## User Interaction Style

Default to execution-first behavior.

Do not repeatedly ask:
- “Should I continue extraction?”
- “Should I continue plotting?”
- “Should I continue export?”

Only interrupt when execution cannot proceed safely or meaningfully.

At the end, provide a concise summary including:
- which result objects were extracted
- which figures were generated
- where files were saved
- whether any object needs manual validation

## Standard End-to-End Behavior

The ideal run should follow this sequence:

1. Read the source PDF or image.
2. Detect chart-worthy experimental result objects.
3. Extract numbers and labels.
4. Save `experimental_data.json`.
5. Determine chart types.
6. Create the output folder named after the paper.
7. Run Python plotting.
8. Export PNG and PDF figures.
9. Generate `latex_codes.tex`.
10. Save all outputs into the final folder.
11. Report the final save path.

## Final Non-Negotiable Rules

- do not fabricate values
- do not skip JSON extraction
- do not ask for confirmation after every step
- do not silently drop outputs
- do create a paper-named output folder automatically
- do finish the full pipeline whenever execution is possible
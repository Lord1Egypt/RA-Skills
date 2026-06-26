# Examples

Read this reference for good/bad comparisons when writing skill content.

## Description Comparison

Bad:

```
A powerful tool for working with databases.
```

Problems: generic filler ("powerful tool"), no specific action, no trigger phrasing, no object specificity.

Good:

```
Back up and restore PostgreSQL databases with automated scheduling, retention policies, and disaster recovery verification. Use when you need to create a database backup, restore from a dump, set up a backup schedule, verify backup integrity, or configure WAL archiving.
```

Why it works: leads with actions (back up, restore), names the system (PostgreSQL), states the outcome, and covers common trigger phrases.

---

Bad:

```
Use when user needs to work with images.
```

Problems: starts with "Use when" (wastes the first sentence), vague object ("images"), no actions.

Good:

```
Generate and transform images through text-to-image and image-to-image workflows. Use when you need to create images from text prompts, transform existing images with style transfer, upscale low-resolution images, or generate variations of a reference image.
```

Why it works: first sentence names the actions and output, second sentence covers trigger scenarios.

## Example Prompts Comparison

Bad:

```
- `Process PDF`
- `Handle document`
- `Work with files`
```

Problems: too abstract, no realistic user language, identical vague structure.

Good:

```
- `I have two versions of a contract and I need to see what changed between them.`
- `Generate a redline diff of these two PDFs and highlight the deletions.`
- `Compare the original NDA with the revised version and produce a summary of changes.`
```

Why it works: realistic user phrasing, varies in formality, covers different aspects of the same capability.

## Workflow Comparison

Bad:

```
## Workflow

1. Get the input.
2. Process it.
3. Return the output.
```

Problems: no concrete actions, no tool references, could describe any skill.

Good:

```
## Workflow

1. Identify the two PDF files to compare. Ask the user if the file paths are unclear.
2. Run the diff script to extract text and generate a structured comparison:

   ```sh
   python3 {baseDir}/scripts/pdf_diff.py <original> <revised> --output diff.html
   ```

3. Review the generated diff for accuracy. Flag any pages where text extraction failed.
4. Present the summary to the user with a count of additions, deletions, and modifications.
```

Why it works: each step is a concrete action, commands use `{baseDir}`, failure cases are acknowledged.

## Minimal Complete Skill (Instruction-Only)

A working skill in about 50 lines:

```markdown
---
name: git-changelog
description: Generate a formatted changelog from git commit history between two tags or dates. Use when you need to create release notes, summarize recent commits, produce a changelog for a version bump, or document what changed since the last release.
metadata: { "openclaw": { "emoji": "📋", "requires": { "bins": ["git"] } } }
---

# Git Changelog

Generate formatted changelogs from git history. Supports tag ranges, date ranges, and conventional commit grouping.

## Prerequisites

- `git` available in PATH.
- Must run inside a git repository.

## Example Prompts

- `Generate a changelog for everything since v2.1.0.`
- `What changed between last Monday and today? Format it as release notes.`
- `Create release notes for v3.0.0 grouped by type (feat, fix, chore).`

## Workflow

1. Identify the git range: two tags, a tag and HEAD, or a date range.
2. Run `git log` with the appropriate range and format.
3. Group commits by type if using conventional commits.
4. Format the output as Markdown with sections per group.
5. Present the changelog to the user for review.

## Definition of Done

- The changelog covers all commits in the specified range.
- Commits are grouped by type when conventional commit format is detected.
- The output is valid Markdown.

## When Not to Use

- The repository does not use git.
- The user wants to edit commit messages rather than generate a changelog.
```

## Script-Backed Skill Example

A skill that bundles a reusable script:

```markdown
---
name: csv-to-chart
description: Convert CSV data into chart images using matplotlib. Use when you need to visualize CSV data, create bar charts, line charts, or scatter plots from tabular data, or generate chart images for reports and presentations.
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"] } } }
---

# CSV to Chart

Turn CSV files into chart images. Supports bar, line, and scatter plots.

## Prerequisites

- Python 3.10+ with matplotlib installed.
- `pip install matplotlib` if not available.

## Example Prompts

- `Plot the monthly revenue from sales.csv as a bar chart.`
- `Create a line chart showing temperature trends from weather_data.csv.`
- `Generate a scatter plot of height vs weight from participants.csv.`

## Workflow

1. Read the CSV file and identify the columns to plot.
2. Ask the user which chart type to use if not specified.
3. Run the chart generation script:

   ```sh
   python3 {baseDir}/scripts/csv_chart.py <input.csv> --x <col> --y <col> --type bar --output chart.png
   ```

4. Show the generated chart to the user for feedback.
5. Adjust labels, colors, or chart type if requested and regenerate.

## Commands

```sh
# Bar chart
python3 {baseDir}/scripts/csv_chart.py data.csv --x month --y revenue --type bar --output chart.png

# Line chart with title
python3 {baseDir}/scripts/csv_chart.py data.csv --x date --y temperature --type line --title "Temperature Trends" --output chart.png
```

## Definition of Done

- A chart image file exists at the specified output path.
- The chart accurately represents the data from the CSV.
- Axis labels and title are present and readable.
```

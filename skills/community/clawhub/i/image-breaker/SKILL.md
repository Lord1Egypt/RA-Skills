---
name: image-breaker
description: Extract and break down content from web documents, PDFs, images, and URLs into structured markdown notes stored locally and synced to Obsidian. Use when the user shares a URL, PDF, screenshot, or document and wants the content converted to organized notes with proper tagging and categorization.
---

# Image Breaker

Convert documents, PDFs, images, and web content into structured markdown notes saved to workspace and synced to Obsidian.

## Workflow

### 1. Extract Content

**For URLs/PDFs:**
```
Use web_fetch to extract content
```

**For images:**
```
Use image tool to analyze and extract text
```

**For already-analyzed content:**
```
User may paste content directly or you've already extracted it
```

### 2. Structure the Content

Convert raw content into organized markdown:

**Sections to create:**
- **Overview** - What is this document/content about?
- **Key Points** - Bullet list of main takeaways
- **Detailed Breakdown** - Organized subsections with headers
- **Reference Ranges/Standards** (if applicable) - Tables for numerical data
- **Action Items** (if applicable) - What to do with this information
- **Source** - Original URL or document name

**Formatting guidelines:**
- Use tables for numerical data (reference ranges, standards, comparisons)
- Use bullet lists for key points
- Use headers (##, ###) for organization
- Include code blocks for technical content
- Bold important terms on first mention

### 3. Save and Sync

Create the markdown note with proper frontmatter and save to workspace:

```python
# Prepare frontmatter
date = "2026-02-10"
tags = ["research", "bloodwork", "nmr"]  # Auto-assigned based on content
title = "NMR Lipid Panel Reference Ranges"

# Build full markdown content
content = f"""---
date: {date}
tags:
  - {tag1}
  - {tag2}
  - {tag3}
source: {original_url_or_source}
type: image-breaker-note
---

# {title}

## Overview
[Brief description of what this document is]

## Key Points
- Point 1
- Point 2
- Point 3

## [Main Section]
[Detailed content with subsections]

## Reference
- **Source:** [URL or document name]
- **Extracted:** {date}
"""

# Save to workspace
output_dir = "research/image-breaker-notes"  # Default
# or user-specified: "research/bloodwork", "content/references", etc.

# Write file
filepath = f"{output_dir}/{date}-{slugified-title}.md"
write(filepath, content)

# Sync to Obsidian (using obsidian-sync skill)
exec: python3 skills/obsidian-sync/scripts/sync_to_obsidian.py {filepath} /Users/biohacker/Desktop/Connections ImageBreaker
```

## Tag Assignment

**Auto-assign 3 most relevant tags based on content:**

Common tags:
- `research` - Academic papers, studies, references
- `bloodwork` - Lab results, biomarkers, panels
- `nmr` - NMR lipid panels specifically  
- `cholesterol` - Cholesterol and lipid-related
- `peptides` - BPC-157, TB-500, etc.
- `supplements` - Vitamins, minerals, compounds
- `protocols` - Treatment/optimization protocols
- `founders` - Business/entrepreneur health content
- `longevity` - Anti-aging, healthspan
- `performance` - Cognitive/physical optimization
- `training` - Exercise, workouts
- `toku` - Nattokinase, Toku Flow related

Prioritize specific tags over generic ones.

## Output Directories

**Default:** `research/image-breaker-notes/`

**Content-specific alternatives:**
- Research documents → `research/papers/` or `research/protocols/`
- Lab results → `research/bloodwork/`
- Marketing materials → `content/references/`
- Training content → `research/training/`
- Business documents → `projects/business-docs/`

Choose the most appropriate directory based on content type.

## Example Usage

**User provides Labcorp NMR document URL:**

1. Extract content using `web_fetch`
2. Structure into markdown with:
   - Overview of what NMR measures
   - Key reference ranges table
   - Interpretation guide
   - Comparison to standard lipids
3. Assign tags: `bloodwork`, `nmr`, `research`
4. Save to `research/image-breaker-notes/2026-02-10-nmr-lipid-panel-reference.md`
5. Sync to Obsidian vault at `ImageBreaker/2026-02-10-nmr-lipid-panel-reference.md`
6. Report to user with file path and Obsidian link

## Best Practices

- **Always extract content first** - Use web_fetch or image tool before structuring
- **Create comprehensive notes** - Include context, not just raw data
- **Use tables for data** - Reference ranges, comparisons, standards
- **Tag intelligently** - Maximum 3 tags, most specific/relevant
- **Choose output directory wisely** - Match content type to workspace organization
- **Auto-sync by default** - User wants notes in Obsidian for cross-referencing
- **Report file location** - Give user both workspace and Obsidian paths

## Output Message Template

After completing the workflow:

```
✅ **Document broken down and saved**

📝 **Title:** [Note Title]
📂 **Location:** research/image-breaker-notes/2026-02-10-note-title.md
🔗 **Obsidian:** ImageBreaker/2026-02-10-note-title.md
🏷️  **Tags:** tag1, tag2, tag3

**Sections created:**
- Overview
- Key Points  
- [Main sections listed]
- Reference

The note is now in your Obsidian vault for tagging and cross-referencing.
```

## Integration with Other Skills

**Obsidian Sync:** Automatically called after note creation  
**Paper Fetcher:** If user provides DOI, use paper-fetcher first, then break down the PDF  
**Research Automation:** Can batch-process multiple documents from research runs

---
name: mindflow
description: Converts text, Markdown files, or Txt files into mind map images. Use this skill when users want to generate mind maps/brain maps from articles, broadcast scripts, notes, or any text content. Supports specifying output format and resolution. This skill should be triggered whenever text needs to be converted into image-based mind maps, regardless of whether users explicitly mention "mind map" or "思维导图"
compatibility: "Requires JavaScript runtime environment (Node.js or Bun) dependencies: markmap-cli, markmap-lib, markmap-render, puppeteer"
---

## Text to Mind Map Skill

This skill converts user-input text, Markdown files, or Txt files into mind map images.

### Dependency Installation

```bash
# Using npm
npm install markmap-cli markmap-lib markmap-render puppeteer

# Using bun
bun install markmap-cli markmap-lib markmap-render puppeteer
```

### Workflow

```
Input Content → text-to-markdown → markdown-to-html → html-to-image → Output Image
→ [If user uses openclaw, send the image to the user as a file]
```

---

### Step 1: text-to-markdown

Use LLM to convert input content into mind map Markdown format according to the following rules:

**Rule Specifications:**

- **Extract Core Content:** Extract key points from broadcast scripts with high information density, concise and clear, without omitting important points
- **Reduce Hallucinations:** Generated content must come from the input broadcast script; do not fabricate, rewrite, exaggerate, flatter, omit, or produce hallucinations
- **Strictly Follow Node Hierarchy:** Only one root node, subsequent nodes progress by hierarchy levels
- **Support All Basic Markdown Syntax:** Bold, code, links, and LaTeX formulas can be embedded in node text
- **Output Format Compliance:** Strictly follow the format below; do not output any other extraneous content
- **Use Appropriate Emoji:** Use relevant emojis appropriately to enhance visual expression, but avoid excessive use
- **Content Limit:** Ensure output content is **limited to 300 tokens**
- **Hierarchy Limit:** Mind map generates maximum 4 levels (root node counts as level 1)

**Output Format:**

```markdown
# Root Node (must have exactly one)
## Level 2 Node
### Level 3 Node
- List items are also supported
- **Bold**, `code`, [link](url)
- $LaTeX formula$
```

---

### Step 2: markdown-to-html

Use markmap command to convert Markdown to HTML:

```bash
markmap --offline --no-open --no-toolbar -o <html_file> <markdown_file>
```

---

### Step 3: html-to-image

Use html-to-image.js to convert HTML to image (default: jpg format):

```bash
node (or bun) scripts/html-to-image.js --auto-fit <input-html> <output-image>
```

**Parameter Specifications:**

| Parameter | Description |
|-----------|-------------|
| `-t jpg` | Output format is png (default) |
| `--auto-fit` | Auto-detect mindmap content size and adapt dimensions |
| `input-html` | Input HTML file path |
| `output-image` | Output image path |

---

### Execution Steps

1. Read user-input text content or file path
2. Call LLM to convert content into mind map Markdown format according to the rules above
3. Save the generated Markdown to a temporary file (e.g., `/tmp/mindmap.md`)
4. Execute `markmap --offline --no-open --no-toolbar -o <html_file> <markdown_file>` to generate HTML
5. Execute `node (or bun) scripts/html-to-image.js --auto-fit <html_file> <output-image>` to generate PNG image
6. Inform user of the output image path | If user uses openclaw, send the image to the user as a file

---

### Input Types

- Directly input text content
- `.md` file path
- `.txt` file path

### Output

- Generated mind map image file (default: PNG format)

---

### Examples

**Example 1:**
- **User Input:** "How to learn React"
- **Output:** PNG image of React learning path mind map

**Example 2:**
- **User Input:** "Help me convert this markdown file to a mind map: /path/to/notes.md"
- **Output:** PNG image of mind map corresponding to notes.md content

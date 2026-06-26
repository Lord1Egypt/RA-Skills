---
name: pptx-notes-editor
description: |
  PowerPoint speaker notes editor for AI agents. Use when the user needs to: (1) modify PPT speaker notes, (2) export notes to Markdown, (3) rewrite notes in narrative/concise/verbatim style, (4) unpack/pack PPTX files. Works with Claude Code, OpenClaw, and any agent that supports SKILL.md.
---

# PPTX Notes Editor

## Workflow Decision Tree

```
User Request
├── Modify Notes → 1,2,3,4,5,6
├── Export to MD Only → 1,2 → 7
├── Pack Existing Content Only → 5 (optional verify → 6)
└── Unpack and View Only → 1
```

## 1. Unpack PPTX

```bash
# Unpack to specified directory
mkdir -p pptx-unpacked && unzip your-presentation.pptx -d pptx-unpacked
```

**File Structure**:
```
pptx-unpacked/
├── ppt/
│   ├── slides/              # Slides
│   │   ├── slide1.xml
│   │   ├── slide2.xml
│   │   └── _rels/          # Slide relationships
│   │       ├── slide1.xml.rels
│   │       └── slide2.xml.rels
│   ├── notesSlides/        # Notes files
│   │   ├── notesSlide1.xml
│   │   └── notesSlide2.xml
│   └── _rels/
│       └── presentation.xml.rels
└── [Content_Types].xml
```

## 2. Confirm Slide-to-Notes Mapping

**Important**: The numbering of `notesSlideN.xml` does NOT necessarily correspond to PPT page numbers! You MUST confirm via the relationship files.

### Method 1: Check Precise Mapping (Recommended)

```bash
# Check which notes file corresponds to slide N
cat pptx-unpacked/ppt/slides/_rels/slideN.xml.rels | grep -i "notesSlide"

# Example output:
# <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide2.xml"/>
# This means slideN.xml corresponds to notesSlide2.xml
```

### Method 2: Quick View All Mappings

```bash
# List all slide-to-notes correspondences
for f in pptx-unpacked/ppt/slides/_rels/slide*.xml.rels; do
  slide=$(basename "$f" .xml.rels)
  notes=$(grep -o 'notesSlide[0-9]*\.xml' "$f" | head -1)
  if [ -n "$notes" ]; then
    echo "$slide -> $notes"
  fi
done
```

### Edge Cases

- **Slide has no notes**: grep returns no output, this slide has no notes
- **Notes file exists but no corresponding slide**: may be orphaned notes, can be ignored

## 3. Read Notes Content

### XML Namespace Reference

PPTX XML uses these namespace prefixes:
- `a:` - DrawingML namespace (text, shapes)
- `p:` - PresentationML namespace (slide structure)
- `r:` - Relationships namespace

Notes text is inside `<a:t>` tags.

### Method 1: Read Page by Page

```bash
# List all notes files
ls pptx-unpacked/ppt/notesSlides/

# Use file reading tool to read individual notes file
# Notes text is in <a:t> tags
```

### Method 2: Batch Extract All Notes Text

```bash
# Extract text from all notes files (macOS compatible)
grep -oh '<a:t>[^<]*</a:t>' pptx-unpacked/ppt/notesSlides/*.xml | sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g' | head -50
```

### Method 3: Extract Single Page Notes by File

```bash
# Extract all text from notesSlide2.xml (macOS compatible)
grep -oh '<a:t>[^<]*</a:t>' pptx-unpacked/ppt/notesSlides/notesSlide2.xml | sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g'
```

### Handling XML Escaped Characters

Notes text may contain these escape sequences:
- `&lt;` → `<`
- `&gt;` → `>`
- `&amp;` → `&`
- `&quot;` → `"`

Decode with sed:
```bash
sed 's/&lt;/</g; s/&gt;/>/g; s/&amp;/\&/g; s/&quot;/"/g'
```

## 4. Rewrite in Narrative Style

### Narrative Style Guidelines
- Tell a story with beginning, development, turning point, and conclusion
- Conversational and natural transitions
- Specific examples and scenarios as support
- Create empathy and engagement with the audience

### Important Notes
- **MUST confirm before modifying**: After generating notes draft, show it to the user and get explicit confirmation before executing any XML modification. Do NOT modify any notes without user confirmation
- If the original PPT notes are dry bullet-point lists, you need to **completely rewrite** them in narrative style
- If the original notes are already in narrative style, you can refine and improve them
- Do NOT assume "keep the original style" - determine the style based on the target presentation context

### Modification Process

#### Step 0: Ask user to select page range and notes style

Present the user with the following choices before starting:

**Page Range Selection**:
- All pages
- Only pages without notes
- Only pages with existing notes
- Custom range (user inputs e.g. "1-5,8,10-12")

**Notes Style Selection**:
- Narrative style (storytelling, conversational, with beginning/development/climax/conclusion)
- Concise bullet points (distill key information, brief and powerful)
- Verbatim script (complete spoken script that can be read aloud directly)
- Custom style (user describes desired style)

**Language Selection** (optional):
- Keep original language
- Chinese
- English

#### Step 1: Read through entire PPT content (build global context)

Before modifying page by page, **you MUST read through all slides to build global context**:

```bash
# Batch extract text summary from all slides (macOS compatible)
for f in pptx-unpacked/ppt/slides/slide*.xml; do
  slide=$(basename "$f" .xml)
  echo "=== $slide ==="
  grep -oh '<a:t>[^<]*</a:t>' "$f" | sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g'
  echo ""
done
```

After reading, present a global overview to the user:
```
[PPT Global Overview]
Total: X pages, Theme: xxx
Page 1: Opening - xxx
Page 2: Background - xxx
Page 3: Core argument - xxx
...
Page X: Summary - xxx

Narrative arc: xxx → xxx → xxx
```

**Purpose of reading through**:
- Understand the overall narrative arc and logical structure
- Know each page's role (setup, core argument, case study, turning point, summary)
- Avoid content duplication or logical gaps between notes
- Provide contextual support for subsequent page-by-page design

#### Step 2+: Page-by-page modification

1. Based on selected page range, read slide content summary page by page (extract key text from slideN.xml)
2. Read current notes (from corresponding notesSlide), **leverage Step 1's global context to understand this page's role**
3. Show both to user in this format:

```
--- Page N ---
[Slide Content]
Title: xxx
Points: aaa, bbb, ccc
Charts: [brief description if any]

[Current Notes]
(show full existing notes, or "None" if empty)
```

4. Generate notes draft according to user's selected style, **present to user**
5. **MUST wait for user's explicit confirmation** before modifying `<a:t>` text in XML. Do NOT execute any modification without user confirmation
6. Get user confirmation before moving to next page

### XML Modification Notes

- Require exact string matching when modifying XML
- Newlines in XML may display as literal `\n`
- Recommend searching file content first to confirm exact string

```xml
<!-- Replace entire <a:t> tag content -->
<!-- Wrong: replacing text directly will break XML structure -->
<!-- Correct: replace the entire <a:t> tag content -->
<a:t>Old text</a:t>  →  <a:t>New text</a:t>
```

**Example**:
```xml
<!-- Before -->
<a:t>This is old notes content</a:t>

<!-- After -->
<a:t>This is new notes content</a:t>
```

### Handling Multiple Paragraphs

If notes contain multiple paragraphs, there will be multiple `<a:t>` tags:
```xml
<a:p>
  <a:r><a:t>First paragraph</a:t></a:r>
</a:p>
<a:p>
  <a:r><a:t>Second paragraph</a:t></a:r>
</a:p>
```

Modify each `<a:t>` tag separately.

### Batch Operations Guide

If you need to uniformly modify similar content in multiple places:
1. Search file content to confirm all locations that need modification
2. Modify each one individually
3. Verify after each modification

## 5. Pack PPTX

```bash
cd pptx-unpacked && zip -r ../pptx-packed.pptx . -x "*.py" -x "*.txt" -x "*.json" -x ".DS_Store"
```

## 6. Verify Modifications

```bash
# Unpack newly packed file and verify XML structure is correct
mkdir -p /tmp/verify && unzip -o pptx-packed.pptx -d /tmp/verify

# Check if modified content exists
grep "new text" /tmp/verify/ppt/notesSlides/*.xml

# Verify XML format is correct (no parse errors)
# If xmllint is installed:
# xmllint --noout /tmp/verify/ppt/notesSlides/*.xml 2>&1 && echo "XML format correct"
```

## 7. Export to MD

### Extract Slide Titles

```bash
# Extract title text from slides (macOS compatible)
# Titles are usually in the first <a:t> tag
grep -oh '<a:t>[^<]*</a:t>' pptx-unpacked/ppt/slides/slideN.xml | sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g' | head -1
```

### Export Format

Organize all page notes into a single MD file:

```markdown
# Presentation Name - Speaker Notes

## Page 1: Title
Notes content...

## Page 2: Title
Notes content...
```

### Correct Export Script (Based on Actual Mapping)

```bash
#!/bin/bash
# Export notes in slide order using actual mapping (macOS compatible)

output="notes-export.md"
echo "# PPT Speaker Notes Export" > "$output"
echo "" >> "$output"

slide_num=0
for slide_rels in pptx-unpacked/ppt/slides/_rels/slide*.xml.rels; do
  slide_num=$((slide_num + 1))

  # Get the notes file for this slide (macOS compatible)
  notes_file=$(grep -o 'notesSlide[^"]*\.xml' "$slide_rels" | head -1)

  if [ -n "$notes_file" ] && [ -f "pptx-unpacked/ppt/notesSlides/$notes_file" ]; then
    # Get slide title (first <a:t>)
    slide_file="pptx-unpacked/ppt/slides/slide${slide_num}.xml"
    title=""
    if [ -f "$slide_file" ]; then
      title=$(grep -oh '<a:t>[^<]*</a:t>' "$slide_file" | sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g' | head -1)
    fi

    echo "## Page ${slide_num}${title:+: $title}" >> "$output"
    echo "" >> "$output"

    # Extract notes text
    grep -oh '<a:t>[^<]*</a:t>' "pptx-unpacked/ppt/notesSlides/$notes_file" | \
      sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g' | \
      sed 's/&lt;/</g; s/&gt;/>/g; s/&amp;/\&/g; s/&quot;/"/g' >> "$output"

    echo "" >> "$output"
    echo "---" >> "$output"
    echo "" >> "$output"
  fi
done

echo "Export complete: $output"
```

---

## Appendix: Troubleshooting

### Issue: PPT Won't Open After Modification
- **Cause**: XML structure was corrupted (e.g., unclosed tags, special characters not escaped)
- **Solution**: When modifying XML, ensure complete `<a:t>...</a:t>` structure is preserved

### Issue: Modified Text Has No Effect
- **Cause**: Modified the wrong notesSlide file
- **Solution**: Re-confirm the mapping between slideN.xml and notesSlide

### Issue: Text Contains Special Characters
- **Cause**: Characters like `& < > "` need escaping
- **Solution**: When modifying, ensure these characters are properly escaped as `&amp; &lt; &gt; &quot;`

## Complete Example

```bash
# 1. Unpack
mkdir -p pptx-unpacked && unzip demo.pptx -d pptx-unpacked

# 2. Confirm mapping (find which notes correspond to page 5)
cat pptx-unpacked/ppt/slides/_rels/slide5.xml.rels | grep -i "notesSlide"
# Output: Target="../notesSlides/notesSlide3.xml"

# 3. Read page 5 notes (corresponds to notesSlide3.xml, macOS compatible)
grep -oh '<a:t>[^<]*</a:t>' pptx-unpacked/ppt/notesSlides/notesSlide3.xml | sed 's/<a:t>\([^<]*\)<\/a:t>/\1/g'

# 4. Modify notes (edit XML file)
# Replace <a:t>Old content</a:t> with <a:t>New content</a:t> in notesSlide3.xml

# 5. Pack
cd pptx-unpacked && zip -r ../demo-new.pptx . -x "*.py" -x ".DS_Store"
cd ..

# 6. Verify
mkdir -p /tmp/verify && unzip -o demo-new.pptx -d /tmp/verify
grep "new text" /tmp/verify/ppt/notesSlides/notesSlide3.xml

# 7. Export MD (using script above)
```

## Reuse Checklist

- [ ] Unpack PPTX to pptx-unpacked
- [ ] Confirm slide-to-notes mapping
- [ ] Determine modification scope (all/some pages)
- [ ] Confirm narrative style requirements
- [ ] Modify page by page with user confirmation
- [ ] Pack PPTX after modification
- [ ] Verify modifications took effect
- [ ] Export to MD if needed

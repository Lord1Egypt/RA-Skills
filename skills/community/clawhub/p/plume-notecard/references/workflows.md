# Notecard Workflow Examples

This document provides practical examples of common notecard generation workflows.

## Topic-Based Notecard

User request: "Generate a notecard about the history of coffee"

**Process:**
1. Agent recognizes topic-only request, information incomplete
2. Agent replies with content plan:
   ```
   Here's my plan for the coffee history notecard:

   1. Origins (Ethiopia, Kaldi legend)
   2. Spread to Arabia and Europe
   3. Modern coffee culture

   Browse styles: [Template Gallery](https://design.useplume.app/notecard/templates?lang=en)

   Does this work?
   ```
3. User confirms: "Looks good"
4. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode article \
     --article "Coffee originated in Ethiopia... [full content]" \
     --style-hint "vintage warm"
   ```

## Long-Form Text to Notecard

User request: [Pastes 2000-word article] + "Turn this into a notecard"

**Process:**
1. Information complete (has full content)
2. Agent sends waiting message: "Generating now, please wait"
3. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode article \
     --article "[pasted article content]" \
     --style-hint "professional"
   ```

## Reference Image: Sketch to Notecard

User: Uploads hand-drawn diagram + "Turn this sketch into a notecard"

**Process:**
1. Agent calls transfer:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py transfer --file /path/to/sketch.png
   # Returns: {"success": true, "image_url": "https://...", "width": 1080, "height": 1440}
   ```
2. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode reference \
     --reference-type sketch \
     --reference-image-urls https://... \
     --reference-image-width 1080 \
     --reference-image-height 1440
   ```

## Reference Image: Style Transfer

User: Uploads existing notecard + "Use this style for a notecard about quantum computing"

**Process:**
1. Transfer image (same as above)
2. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode reference \
     --reference-type style_transfer \
     --reference-image-urls https://... \
     --reference-image-width 1080 \
     --reference-image-height 1440 \
     --reference-topic "quantum computing"
   ```

## Reference Image: Content Rewrite

User: Uploads notecard + "Replace the content with solar system facts"

**Process:**
1. Transfer image (same as above)
2. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode reference \
     --reference-type content_rewrite \
     --reference-image-urls https://... \
     --reference-image-width 1080 \
     --reference-image-height 1440 \
     --reference-article "[detailed solar system content]"
   ```

## Batch: Series Notecards

User: "Generate 5 notecards about different programming languages"

**Process:**
1. Information incomplete (need specific languages and content)
2. Agent proposes:
   ```
   I'll create a 5-part programming language series:
   1. Python - "Batteries included"
   2. JavaScript - "Language of the web"
   3. Rust - "Safety first"
   4. Go - "Simple and fast"
   5. TypeScript - "Typed JavaScript"

   Style: unified tech/minimalist

   OK?
   ```
3. User confirms
4. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode article \
     --article "[content covering all 5 languages]" \
     --count 5 --child-reference-type content_rewrite \
     --style-hint "tech minimalist"
   ```

## Deck: Slide Deck Notecards

User: "Make a slide deck about climate change, 5 pages"

**Process:**
1. Agent plans structure:
   ```
   I'll create a 5-page climate change deck:
   Page 1: Cover - "Climate Change: A Global Challenge"
   Page 2: Causes - greenhouse gases, deforestation
   Page 3: Effects - rising temps, extreme weather
   Page 4: Solutions - renewable energy, policy
   Page 5: Call to action

   Style: urgent, data-driven

   Ready?
   ```
2. User confirms
3. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode article --deck-mode \
     --page-count 5 \
     --pages '[
       {"role":"cover","title":"Climate Change","subtitle":"A Global Challenge"},
       {"role":"detail","title":"Causes","content":"Greenhouse gases..."},
       {"role":"detail","title":"Effects","content":"Rising temperatures..."},
       {"role":"detail","title":"Solutions","content":"Renewable energy..."},
       {"role":"back","title":"Act Now","content":"Together we can make a difference"}
     ]' \
     --style-hint "data urgent"
   ```

## Retry: Switch Style

User: After seeing result, says "换个风格" (switch style)

**Process:**
1. Agent reads history:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py history --channel user123
   # Returns last successful entry with task_id
   ```
2. Agent calls create:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 \
     --action switch_style \
     --last-task-id abc123 \
     --article "[original content from history]"
   ```

## Using History

To check previous operations for a channel:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py history --channel user123
```

Returns:
```json
{
  "success": true,
  "channel": "user123",
  "count": 2,
  "entries": [
    {"timestamp": "2024-01-15T10:30:00Z", "action": "create", "task_id": "abc123", "status": "success"},
    {"timestamp": "2024-01-15T11:00:00Z", "action": "retry", "task_id": "def456", "status": "success"}
  ]
}
```

## PDF Merge: Auto-merge on Creation

User: "Generate 5 notecards about programming languages, merge to PDF"

**Process:**
1. Agent plans content (same as batch workflow)
2. User confirms
3. Agent calls create with `--merge-to-pdf`:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode article \
     --article "[content covering all 5 languages]" \
     --count 5 --merge-to-pdf \
     --style-hint "tech minimalist"
   ```
4. Returns:
   ```json
   {
     "success": true,
     "task_id": "abc123",
     "images": ["/path/to/img1.png", "/path/to/img2.png", ...],
     "pdf": {
       "path": "/path/to/merged_20260407_123456.pdf",
       "page_count": 5,
       "file_size_mb": 2.3
     }
   }
   ```

## PDF Merge: Post-generation

User: After batch generation, says "merge to PDF"

**Process:**
1. Agent reads history to get image paths:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py history --channel user123
   ```
2. Agent calls merge-pdf:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py merge-pdf \
     --images /path/to/img1.png,/path/to/img2.png,/path/to/img3.png
   ```
3. Returns:
   ```json
   {
     "success": true,
     "pdf_path": "/path/to/merged_20260407_123456.pdf",
     "page_count": 3,
     "file_size_mb": 1.5
   }
   ```

## ZIP Package: Auto-package on Creation

User: "Generate 5 notecards about programming languages, package as ZIP"

**Process:**
1. Agent plans content (same as batch workflow)
2. User confirms
3. Agent calls create with `--create-zip`:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
     --channel user123 --mode article \
     --article "[content covering all 5 languages]" \
     --count 5 --create-zip \
     --style-hint "tech minimalist"
   ```
4. Returns:
   ```json
   {
     "success": true,
     "task_id": "abc123",
     "images": ["/path/to/img1.png", "/path/to/img2.png", ...],
     "zip": {
       "path": "/path/to/notecards_20260407_123456.zip",
       "file_count": 5,
       "file_size_mb": 1.8
     }
   }
   ```

## ZIP Package: Post-generation

User: After batch generation, says "package to ZIP"

**Process:**
1. Agent reads history to get image paths:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py history --channel user123
   ```
2. Agent calls create-zip:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create-zip \
     --images /path/to/img1.png,/path/to/img2.png,/path/to/img3.png
   ```
3. Returns:
   ```json
   {
     "success": true,
     "zip_path": "/path/to/notecards_20260407_123456.zip",
     "file_count": 3,
     "file_size_mb": 1.2
   }
   ```

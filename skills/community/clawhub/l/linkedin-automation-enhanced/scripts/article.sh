#!/bin/bash
# LinkedIn Article Script (Native Long-Form)
# Usage: ./article.sh --title "Title" --subtitle "Subtitle" --content "Content" [--cover-image /path/to/image]

set -e

TITLE=""
SUBTITLE=""
CONTENT=""
COVER_IMAGE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
            shift 2
            ;;
        --subtitle)
            SUBTITLE="$2"
            shift 2
            ;;
        --content)
            CONTENT="$2"
            shift 2
            ;;
        --cover-image)
            COVER_IMAGE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
    echo "Usage: ./article.sh --title \"Title\" --subtitle \"Subtitle (optional)\" --content \"Content\" [--cover-image /path/to/image]"
    exit 1
fi

# Output instructions for the agent to execute via browser tool
cat << EOF
📝 LINKEDIN ARTICLE WORKFLOW (Native Long-Form)
═══════════════════════════════════════════════════

Article Details:
---
Title: $TITLE
Subtitle: ${SUBTITLE:-"(none)"}
Cover Image: ${COVER_IMAGE:-"(none)"}
---

Content (first 500 chars):
---
$(echo "$CONTENT" | head -c 500)...
---

Steps to execute via browser tool:

1. Navigate to https://www.linkedin.com/feed/

2. Wait for page load, then find the "Write article" button:
   - Location: Top of feed, near "Start a post" box
   - Look for text "Write article" or pencil icon
   - Click it to open the article editor

3. In the article editor:
   
   a) Enter TITLE in the title field:
      - Selector: input[placeholder*="title"] or h1[contenteditable]
      - Type: $TITLE
   
   b) Enter SUBTITLE (if provided):
      - Selector: input[placeholder*="subtitle"] or similar
      - Type: ${SUBTITLE:-"(skip if not provided)"}
   
   c) Enter CONTENT in the body editor:
      - Selector: div[contenteditable="true"] or div.editor-content
      - Type the full content (supports markdown-like formatting)
      - Use formatting toolbar for H1/H2, bold, lists, etc.
   
   d) Add COVER IMAGE (if provided):
      - Click the image/cover photo button at top
      - Upload: $COVER_IMAGE
      - ${COVER_IMAGE:-"(skip if not provided)"}

4. Review the article preview

5. Click "Publish" button:
   - Selector: button containing "Publish" text
   - Usually top-right corner

6. Wait for confirmation (article published + redirect to article view)

⚠️  Rate limit: Max 1-2 articles per day recommended
⚠️  Articles are searchable on Google and permanent on your profile
⚠️  Editor supports: headings, bold, italic, lists, links, images, embeds

EOF

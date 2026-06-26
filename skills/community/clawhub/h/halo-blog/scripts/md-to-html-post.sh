#!/bin/bash
set -e

PROFILE=$1
MD_FILE=$2

if [ -z "$PROFILE" ] || [ -z "$MD_FILE" ]; then
  echo "Usage: $0 <profile> <markdown-file>"
  exit 1
fi

if [ ! -f "$MD_FILE" ]; then
  echo "Error: file not found: $MD_FILE"
  exit 1
fi

# 从 front matter 提取 title 和 slug
TITLE=$(grep -m1 '^title:' "$MD_FILE" | sed 's/^title: *//; s/^"//; s/"$//; s/^'\''//; s/'\''$//')
SLUG=$(grep -m1 '^slug:' "$MD_FILE" | sed 's/^slug: *//; s/^"//; s/"$//; s/^'\''//; s/'\''$//')

if [ -z "$TITLE" ] || [ -z "$SLUG" ]; then
  echo "Error: front matter must contain 'title' and 'slug'"
  exit 1
fi

TMP_DIR=$(mktemp -d)
HTML_MODE=false

# 去掉 front matter，保留正文
sed '1,/^---$/d' "$MD_FILE" | sed '1{/^---$/d}' > "$TMP_DIR/body.md"

# 尝试 Markdown -> HTML
if npx marked "$TMP_DIR/body.md" > "$TMP_DIR/body.html" 2>/dev/null; then
  HTML_MODE=true
else
  echo "Warning: HTML conversion failed, falling back to Markdown import."
  HTML_MODE=false
fi

if [ "$HTML_MODE" = true ]; then
  # 尝试用 HTML 发布
  if python3 -c "
import subprocess, sys
with open('$TMP_DIR/body.html', 'r', encoding='utf-8') as f:
    html = f.read()
result = subprocess.run([
    'halo', 'post', 'create',
    '--profile', '$PROFILE',
    '--name', '$SLUG',
    '--title', '$TITLE',
    '--slug', '$SLUG',
    '--content', html,
    '--raw-type', 'html',
    '--publish', 'true'
], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)
sys.exit(result.returncode)
" 2>/dev/null; then
    POST_NAME=$(halo post get "$SLUG" --profile "$PROFILE" --json | python3 -c "import sys,json; print(json.load(sys.stdin)['post']['metadata']['name'])")
    halo post update "$POST_NAME" --profile "$PROFILE" --visible PUBLIC
    echo "Done (HTML): https://blog.codingshen.top/archives/$SLUG"
    rm -rf "$TMP_DIR"
    exit 0
  else
    echo "Warning: HTML post creation failed, falling back to Markdown import."
  fi
fi

# 降级：直接用 Markdown 导入
halo post import-markdown --profile "$PROFILE" --file "$MD_FILE" --force
POST_NAME=$(halo post get "$SLUG" --profile "$PROFILE" --json | python3 -c "import sys,json; print(json.load(sys.stdin)['post']['metadata']['name'])")
halo post update "$POST_NAME" --profile "$PROFILE" --visible PUBLIC
halo post update "$POST_NAME" --profile "$PROFILE" --publish true

echo "Done (Markdown fallback): https://blog.codingshen.top/archives/$SLUG"
rm -rf "$TMP_DIR"

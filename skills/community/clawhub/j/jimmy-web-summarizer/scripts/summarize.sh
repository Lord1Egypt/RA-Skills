#!/bin/bash
# Web Content Summarizer
# Usage: bash summarize.sh <url> [focus]

URL="$1"
FOCUS="${2:-main points}"

if [ -z "$URL" ]; then
    echo "Usage: bash summarize.sh <url> [focus]"
    echo "Example: bash summarize.sh https://news.ycombinator.com 'interesting posts'"
    exit 1
fi

# Validate URL
if ! echo "$URL" | grep -q "http"; then
    echo "❌ Invalid URL. Must start with http:// or https://"
    exit 1
fi

echo "🔍 Fetching: $URL"
echo ""

# Fetch content
CONTENT=$(curl -s --max-time 15 -L \
    -A "Mozilla/5.0 (compatible; AI-Agent/1.0)" \
    "$URL" 2>/dev/null)

if [ -z "$CONTENT" ]; then
    echo "❌ Failed to fetch content"
    exit 1
fi

# Extract title
TITLE=$(echo "$CONTENT" | python3 -c "
import sys, re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        
    def handle_starttag(self, tag, attrs):
        skip_tags = {'script','style','nav','footer','header','aside'}
        if tag in skip_tags:
            self.skip = True
            
    def handle_endtag(self, tag):
        if tag in {'script','style','nav','footer','header','aside'}:
            self.skip = False
            
    def handle_data(self, data):
        if not self.skip:
            text = data.strip()
            if text:
                self.text.append(text)

html = sys.stdin.read()
# Remove comments
html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
# Remove extra whitespace
html = re.sub(r'\s+', ' ', html)

parser = TextExtractor()
try:
    parser.feed(html)
    text = ' '.join(parser.text)
    # Get first 3000 chars
    print(text[:3000])
except:
    print('')
" 2>/dev/null)

if [ -z "$TITLE" ]; then
    echo "⚠️ Could not extract content"
    exit 1
fi

# Generate summary (simple extractive)
SUMMARY=$(echo "$TITLE" | python3 -c "
import sys
text = sys.stdin.read()

# Split into sentences
import re
sentences = re.split(r'[.!?]+', text)
sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

# Score sentences by length and position
scored = []
for i, s in enumerate(sentences[:20]):
    score = len(s) / 50 + (1 / (i + 1))  # longer + earlier = better
    scored.append((score, s))

scored.sort(reverse=True)

# Print top 5
print('## Key Points\n')
for _, s in scored[:5]:
    print(f'- {s.strip()}.')
" 2>/dev/null)

echo "$SUMMARY"
echo ""
echo "📄 Source: $URL"
echo "📝 Generated at: $(date '+%Y-%m-%d %H:%M')"

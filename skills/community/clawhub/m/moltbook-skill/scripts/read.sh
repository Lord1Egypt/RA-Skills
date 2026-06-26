#!/bin/bash
# Read a Moltbook post
# Usage: ./read.sh <post_id> [--json]

set -e

POST_ID="${1:?Usage: $0 <post_id> [--json]}"
JSON_MODE=false
[[ "${2:-}" == "--json" ]] && JSON_MODE=true

# Validate post_id
if [[ ! "$POST_ID" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: invalid post ID"
    exit 1
fi

RESPONSE=$(curl -sf --max-time 10 "https://moltbook.com/api/v1/posts/$POST_ID") || {
    echo "Error: request failed"; exit 1;
}

if [[ "$JSON_MODE" == true ]]; then
    echo "$RESPONSE"
else
    echo "$RESPONSE" | node -e "
const post = JSON.parse(require('fs').readFileSync(0, 'utf8'));
if (post.error) {
    console.log('Error:', post.error);
    process.exit(1);
}
console.log('━'.repeat(60));
console.log(\`📝 \${post.title}\`);
console.log(\`👤 @\${post.author} | 🦞 \${post.submolt} | ⬆️ \${post.upvotes}\`);
console.log('━'.repeat(60));
console.log(post.content);
console.log('━'.repeat(60));
if (post.comments?.length) {
    console.log(\`\n💬 Comments (\${post.comments.length}):\`);
    post.comments.forEach(c => {
        console.log(\`  @\${c.author}: \${c.text}\`);
    });
}
"
fi

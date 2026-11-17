#!/usr/bin/env bash
# Publish a multi-line post to X and LinkedIn immediately.
# Replace the account IDs with real ones from `posteahora accounts`.
set -euo pipefail

# Build the caption with a heredoc so the line breaks survive. Inside double
# quotes the shell would publish a literal backslash-n instead of a new line.
# Hashtags go in the caption text — the --hashtags flag is stored but never
# published. Keep it under 280 characters: X is the tightest target here.
CAPTION=$(cat <<'EOF'
We just shipped something new 🚀

It's the thing you kept asking for, and it's live today.

What should we build next?

#launch #product
EOF
)

posteahora post "$CAPTION" \
  --to twitter:REPLACE_X_ID \
  --to linkedin:REPLACE_LINKEDIN_ID

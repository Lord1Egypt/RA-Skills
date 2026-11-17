#!/usr/bin/env bash
# Schedule a week of posts to X in one go.
# Replace REPLACE_X_ID with a real account id from `posteahora accounts`.
set -euo pipefail

ACCOUNT="twitter:REPLACE_X_ID"

posteahora post "Monday: kick off the week with a tip 💡"      --to "$ACCOUNT" --at 2026-07-20T09:00:00Z
posteahora post "Tuesday: behind-the-scenes of what we build"  --to "$ACCOUNT" --at 2026-07-21T09:00:00Z
posteahora post "Wednesday: a customer win 🎉"                 --to "$ACCOUNT" --at 2026-07-22T09:00:00Z
posteahora post "Thursday: a contrarian take 🔥"               --to "$ACCOUNT" --at 2026-07-23T09:00:00Z
posteahora post "Friday: recap + what's next 🚀"               --to "$ACCOUNT" --at 2026-07-24T09:00:00Z

echo "Scheduled 5 posts. Verify with: posteahora posts --status scheduled"

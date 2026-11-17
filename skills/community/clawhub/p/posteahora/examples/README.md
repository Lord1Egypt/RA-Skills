# Examples

Ready-to-run examples for the PosteAhora CLI. Replace account IDs with real ones
from `posteahora accounts`, and set your key first:

```bash
posteahora auth --key pah_live_xxxxxxxx
```

## Files

- [`publish-now.sh`](publish-now.sh) — publish a multi-line post to multiple channels immediately.
- [`schedule-post.sh`](schedule-post.sh) — upload media and schedule a post.
- [`weekly-plan.sh`](weekly-plan.sh) — schedule a week of posts in one script.
- [`analytics-report.sh`](analytics-report.sh) — pull a 30-day performance report.

Run any of them with `bash <file>.sh`.

## Multi-line captions

Captions publish byte for byte, and the shell does **not** expand a backslash-n
inside double quotes — `posteahora post "a\nb"` publishes the characters `\n`.
Build anything longer than one line with a heredoc, as `publish-now.sh` does:

```bash
CAPTION=$(cat <<'EOF'
Hook line

Body line

#tag #tag
EOF
)

posteahora post "$CAPTION" --to instagram:ACCOUNT_ID
```

See [PUBLISHING.md](../PUBLISHING.md#caption-formatting) for the full contract.

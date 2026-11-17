Expected plan-mode behavior:

- Discovers three local images and skips the already-public URL.
- Calculates one stable object key for each local file.
- Writes `article.md.image-publish-plan.json`.
- Does not change `article.md`, upload data, or create a backup.

Expected reviewed-map apply behavior:

- Requires both `--apply` and `--confirm-write`.
- Creates `article.md.bak` before rewriting.
- Replaces the three local image references while preserving the Markdown title and HTML attributes.
- Keeps the existing public URL unchanged.
- Records replacement details and any missing files in the plan report.

Safety checks:

- An upload attempt requires `--apply --confirm-upload` and all required `R2_*` environment variables.
- A missing local image, a path outside the reviewed project root, or an incomplete URL map stops that file from being rewritten.
- The report must never include access-key values or secret-key values.

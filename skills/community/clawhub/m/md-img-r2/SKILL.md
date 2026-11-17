---
name: md-img-r2
description: Prepare local image references in Markdown for Cloudflare R2 or another S3-compatible object store, upload them only after explicit confirmation, and replace references with public URLs. Use when a user wants to publish Markdown images for a blog, Zhihu, Xiaohongshu, WeChat, or other distribution channels; inspect image paths; create a dry-run replacement plan; or safely apply image URL replacements. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.4
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/publishing/md-img-r2
---

# Markdown Images to R2

Prepare Markdown image references for public distribution without exposing private configuration or changing files by default.

## Position In A Publishing Workflow

Use this skill after reviewed local images have been inserted into the target Markdown with relative paths. It is the image transport and URL-rewrite layer; illustration decisions, image generation, captions, tags, and final publish approval belong to upstream or downstream content skills.

When an image manifest exists, compare its target Markdown files, local paths, and R2 states with the generated plan. Return the plan or replacement report to the final publish check.

## Workflow

1. Read the target Markdown and identify local Markdown, HTML, and reference-style image links.
2. Run the bundled script without `--apply` first. It writes an image-publish plan and predicts stable public URLs without uploading or rewriting.
3. Review missing files, skipped remote URLs, object keys, and the planned replacements.
4. Choose one apply path:
   - Upload to an R2 or S3-compatible endpoint with `--apply --confirm-upload`.
   - Apply a reviewed URL map with `--apply --confirm-write --url-map`.
5. Inspect the backup and replacement report after every applied change.
6. Verify required public URLs separately, update the manifest to `verified`, and hand the report to the final publish check.

## Commands

```bash
# Default: plan only. No upload and no Markdown rewrite.
./run.sh path/to/article.md

# Scan a directory.
./run.sh path/to/posts --recursive

# Upload only after an explicit confirmation gate.
# Set reviewed R2_* values through your secure shell environment first.
./run.sh path/to/article.md --apply --confirm-upload

# Apply a previously reviewed URL map without contacting object storage.
./run.sh path/to/article.md --apply --confirm-write --url-map replacements.json
```

The script uses `R2_REGION=auto` and `R2_KEY_PREFIX=md-assets` when they are not supplied. `R2_ACCOUNT_ID` is optional when `R2_ENDPOINT` is set.

## Output Contract

- Plan mode writes `<article>.image-publish-plan.json` and leaves the Markdown unchanged.
- Apply mode creates `<article>.bak`, writes the same plan with result details, and changes only successful local-image references.
- Object keys use a content hash plus a sanitized filename so repeat runs are stable.
- Remote URLs, data URLs, and missing files stay unchanged and are recorded in the report.
- A successful upload or rewrite is not a publish approval; the downstream release gate still decides readiness.

## Boundaries

- Do not use it to publish private material, account credentials, or local paths.
- Do not run `--apply` until the user has reviewed the plan and explicitly confirmed the upload or write path.
- Do not infer a public base URL, bucket, endpoint, or key prefix from a personal environment.
- Stop when a local image is missing, outside the reviewed project root, or the planned URL is not acceptable for the target platform.
- Verify the resulting public URLs separately when a publishing workflow requires network acceptance.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)

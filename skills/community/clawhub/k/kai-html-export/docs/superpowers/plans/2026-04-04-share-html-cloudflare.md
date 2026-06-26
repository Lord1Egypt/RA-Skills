# HTML Sharing Implementation Plan

Date: 2026-04-04

## Steps

1. Add regression tests for the new share router behavior.
2. Add regression tests for Cloudflare CLI command construction and URL parsing.
3. Implement a shared environment guard for hosted sandbox detection with explicit env overrides.
4. Implement `scripts/deploy-cloudflare.py` for Cloudflare Pages static deploys.
5. Implement `scripts/share-html.py` to route to Cloudflare by default and Vercel on request.
6. Update `SKILL.md`, `README.md`, and `README.zh-CN.md` to document:
   - Cloudflare as default
   - Vercel as fallback
   - hosted sandbox manual-share guidance
7. Run focused tests and fix regressions until green.

## Verification

- `uv run --with pytest pytest tests/test_share_deploy.py -q`
- `python -m py_compile scripts/deploy-cloudflare.py scripts/deploy-vercel.py scripts/share-html.py`

## Risk Notes

- `wrangler` via `npx` can fail on Windows when the optional `workerd` package is missing; the helper should recover by retrying with the missing package name.
- `wrangler whoami` may print an unauthenticated message with exit code `0`; authentication must be checked from output content, not only return code.

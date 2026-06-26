# GPT-Image-2 for OpenClaw 1.0.1 plan

## Recommended changes
- Add `scripts/e2e-check.sh` for post-install end-to-end validation
- Mention ClawHub listing optimization on next publish:
  - improve changelog wording
  - consider tags when the registry supports meaningful discovery tags
- Keep public guidance explicit about the two common pitfalls:
  - gateway may still hold an old provider registry until restart
  - `resolution` must not be sent to `hnbc/gpt-image-2`

## Release checklist
1. Run `scripts/self-check.sh`
2. Run `scripts/e2e-check.sh`
3. Confirm `image_generate(action="list")` shows `hnbc`
4. Confirm a real image generation works without `resolution`
5. Publish as `1.0.1`

## Suggested publish command
```bash
clawhub publish /root/.openclaw/workspace/skills/gpt-image-2-toolkit \
  --slug gpt-image-2-toolkit \
  --name "GPT-Image-2 for OpenClaw" \
  --version 1.0.1 \
  --changelog "Add end-to-end validation script and tighten installation verification guidance."
```

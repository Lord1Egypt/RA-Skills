# Pexo AI Video Agent — Setup & Troubleshooting

## First-Time Setup

### 1. Get Your Pexo API Key

1. Go to **https://pexo.ai**
2. Sign up / log in to your account
3. Navigate to **Settings → API Keys**
4. Generate a new API key
5. Copy it (starts with `sk-...`)

### 2. Create the Config File

Create a file at `~/.pexo/config` with:

```
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-your-api-key-here"
```

Or set environment variables:
```bash
export PEXO_BASE_URL="https://pexo.ai"
export PEXO_API_KEY="sk-your-api-key-here"
```

### 3. Verify Setup

Run `pexo-doctor.sh` (if available) or test with:
```bash
pexo-project-create.sh "Test Project"
```
If it returns a project ID, you're ready!

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing PEXO_API_KEY` | Config not found | Create `~/.pexo/config` |
| `INVALID_TOKEN` | Wrong or expired API key | Regenerate at pexo.ai |
| `404 Project not found` | Wrong project ID | Check project ID from create step |
| `rate limit exceeded` | Too many requests | Wait 60s and retry |

---

## Tips for Best Results

- **Be specific** in your video request — include subject, setting, mood, and duration
- **Upload reference images** — helps Pexo match your brand/product
- **Start with 15s videos** — good balance of quality and speed
- **Use vertical (9:16)** for TikTok/Instagram Reels
- **Use 16:9** for YouTube and ads

---

## Need Help?

- Docs: https://pexo.ai/connect/openclaw
- Support: hello@pexo.ai
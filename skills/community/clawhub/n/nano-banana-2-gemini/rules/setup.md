---
name: nano-banana-2-setup
description: |
  Configure the GEMINI_API_KEY environment variable required by nano-banana-2.
  The key authenticates all requests to the Gemini generativelanguage API.
---

# nano-banana-2 Setup

## API Key Configuration

nano-banana-2 requires a Google Gemini API key set as `GEMINI_API_KEY`.

### Step 1: Obtain a Key

1. Go to https://aistudio.google.com/app/apikey
2. Create a new project key or copy an existing one
3. Confirm the key has access to `gemini-3.1-flash-image-preview`

### Step 2: Set the Environment Variable

**Recommended — shell profile (persists across sessions):**

```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Current session only:**

```bash
export GEMINI_API_KEY="your-key-here"
```

**Project `.env` file:**

```bash
echo 'GEMINI_API_KEY=your-key-here' >> .env
echo ".env" >> .gitignore   # add immediately — never commit keys
source .env
```

### Step 3: Verify

```bash
echo $GEMINI_API_KEY
```

A non-empty string confirms the key is set. nano-banana-2 never prints the full
key value in command output.

## Output Directory

nano-banana-2 writes all images to `.nano-banana/` in the current directory.
Set it up once per project:

```bash
mkdir -p .nano-banana
echo ".nano-banana/" >> .gitignore
```

## Quota and Billing

Image generation with `gemini-3.1-flash-image-preview` consumes API quota.
Monitor usage at https://aistudio.google.com/app/apikey.

Higher quota consumption per request:
- Larger `imageSize` values (`2048`, `4096`)
- `thinkingBudget: "high"`
- Search-grounded generation (also incurs grounding tool costs)

## Troubleshooting

**`GEMINI_API_KEY` is empty after setting it**

You may need to reload the shell profile or open a new terminal:

```bash
source ~/.zshrc
echo $GEMINI_API_KEY
```

**`API_KEY_INVALID` error**

Check for extra spaces or newline characters in the key. Inspect safely:

```bash
python3 -c "import os; k=os.environ.get('GEMINI_API_KEY',''); print('len:', len(k), 'first8:', repr(k[:8]))"
```

**`404 Not Found` / model not available**

`gemini-3.1-flash-image-preview` is a preview model. Confirm model access in
your Google AI Studio project settings. If unavailable, the model may require
explicit allowlisting or a newer API key from a supported region.

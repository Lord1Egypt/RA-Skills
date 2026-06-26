# Gemini Deep Research — Setup Guide

Prerequisite: a paid Google AI API key with billing enabled on your Google Cloud project.

## 1. Install Gemini CLI

```bash
npm install -g @google/gemini-cli
```

Verify:
```bash
gemini --version
```

## 2. Authenticate

```bash
gemini auth
```

This opens a browser for Google account auth (free_tier够用 for CLI auth).

## 3. Install the Deep Research Extension

```bash
gemini extensions install https://github.com/allenhutchison/gemini-cli-deep-research --auto-update
```

Verify installation:
```bash
gemini extensions list
# ✓ gemini-deep-research (0.2.x)
```

## 4. Configure API Key

> **Important:** The Gemini CLI strips environment variables containing `KEY` from MCP server processes. You must use extension settings — shell `GEMINI_API_KEY` will not work.

Get a paid API key from [Google AI Studio](https://aistudio.google.com/apikey) (ensure billing is enabled on your Google Cloud project).

```bash
gemini extensions config gemini-deep-research
# Navigate to "API Key" → paste your key → confirm
```

The extension stores the key securely in your system keychain.

## 5. Verify MCP Server Connects

```bash
node ~/.gemini/extensions/gemini-deep-research/dist/index.js &
# Should print: "Gemini Deep Research MCP server running on stdio"
# Press Ctrl+C to exit
```

Or test via the CLI:
```bash
gemini --extensions gemini-deep-research --prompt "test" -p
```

## Notes

- **Paid API key required.** Deep Research uses the Gemini Interactions API, which has separate quota. Free-tier keys get 429 errors.
- **Quota:** Check your usage at [Google AI Studio](https://aistudio.google.com) → API Keys → manage.
- **Extension updates:** Run `gemini extensions update` periodically to stay on latest version.
- **Platform:** Requires Node.js 18+.

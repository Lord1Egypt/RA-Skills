# Setup Guide

## Prerequisites

- MiniMax Token Plan: https://platform.minimaxi.com/subscribe/token-plan
- API Key from Token Plan

## Step 1: Install uvx

**Recommended: Homebrew (macOS)**
```bash
brew install uv
```

**Alternative: pipx**
```bash
pipx install uv
```

**Fallback: Official installer (curl|sh)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 2: Set API Key (Environment Variable)

```bash
export MINIMAX_API_KEY="YOUR_TOKEN_PLAN_API_KEY"
```

Add to shell profile for persistence:
```bash
echo 'export MINIMAX_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

Note: `MINIMAX_API_HOST` is set automatically by the scripts (defaults to `https://api.minimaxi.com`).

## Step 3: Verify

```bash
python3 scripts/understand_image.py /path/to/test.jpg "测试"
```

## Getting Your API Key

1. Go to https://platform.minimaxi.com/subscribe/token-plan
2. Subscribe to a plan
3. Copy your API Key from the dashboard

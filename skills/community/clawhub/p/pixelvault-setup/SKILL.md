---
name: pixelvault-setup
description: Set up PixelVault CLI — install the CLI and configure API key authentication. Use when the user wants to configure PixelVault, "set up image hosting", "connect PixelVault", get an API key for image uploads, or when pixelvault-upload fails due to missing auth.
disable-model-invocation: true
---

# PixelVault Setup

Install and configure the PixelVault CLI for image hosting.

## Steps

### 1. Check if CLI is installed

```bash
which pixelvault
```

If not found, install it:

```bash
npm install -g pixelvault-cli
```

### 2. Check if already configured

```bash
pixelvault whoami --json
```

If this succeeds, the user is already set up. Show them their current config and ask if they want to reconfigure.

### 3. Configure authentication

Ask the user which option they prefer:

**Option A — Existing API key:**
If the user already has a PixelVault API key, set it directly:

```bash
pixelvault config set api_key <their-key>
```

**Option B — Environment variable:**
For CI/CD or headless usage, suggest adding to their shell profile:

```bash
export PIXELVAULT_API_KEY=pv_live_xxx
```

**Option C — Create new account:**
If the user doesn't have an account, register:

```bash
pixelvault register
```

This will prompt for email and password, create the account, and auto-save the API key.

### 4. Verify

Confirm setup works:

```bash
pixelvault whoami
```

Should show email, project ID, and masked API key.

### 5. Done

Tell the user they're ready to upload images with `/pixelvault-upload <file>`.

---
name: lix-agents
description: Obtain temporary Lix API tokens via CLI with human email approval. Use when you need authenticated access to the Lix API, need to enrich data via Lix, or need API credentials for any Lix service.
---

# Lix Agents

Use `lix-agents` to get temporary API tokens for the Lix API. Tokens require human approval via email, so agents never hold unsupervised credentials.

**Always tell the user what you're doing and why before running each command.** Don't silently run commands — explain the purpose of each step so the user can follow along.

## When to use this

- You need to call any `https://api.lix-it.com` endpoint that requires authentication
- You need to enrich LinkedIn profiles, companies, or other data via Lix
- You don't already have a valid Lix API token in your environment

## Step-by-step workflow

Follow these steps in order. Before each step, explain to the user *why* you're running the command.

### Step 1: Check if `lix-agents` is installed

Tell the user: *"First, I'll check if the lix-agents CLI is installed on your machine."*

```bash
which lix-agents
```

If the command is not found, tell the user you need to install it and why — it's a CLI that manages Lix API authentication for AI agents. Then install it:

```bash
brew tap lix-it/lix-agents && brew install lix-agents
```

If brew is unavailable, suggest `go install github.com/lix-it/lix-agents@latest` or downloading from [GitHub Releases](https://github.com/lix-it/lix-agents/releases).

### Step 2: Check if the user is already logged in

Tell the user: *"Now I'll check if you already have a Lix session. This avoids asking you to log in again if you've done it before."*

```bash
lix-agents auth status
```

- If already logged in, skip to Step 4.
- If not logged in, continue to Step 3.

### Step 3: Log in (only if needed)

Tell the user: *"You're not logged in yet. I'll start the login flow — this will give you a URL to open in your browser. You only need to do this once; your session will be saved locally."*

```bash
lix-agents auth login
```

Share the URL with the user and wait for them to confirm they've signed in.

### Step 4: Request a temporary API token

Tell the user: *"Now I'll request a temporary API token. For security, Lix will send you an approval email — please check your inbox and approve the request. I'll wait for the approval before continuing."*

```bash
lix-agents auth token
```

The command blocks until the user approves via email. Once approved, it prints the token to stdout. Save this token for use in subsequent API calls.

### Step 5: Use the token

Set the token in the `Authorization` header for API requests:

```
Authorization: Bearer <token>
```

All requests go to `https://api.lix-it.com`. See the [Lix API docs](https://lix-it.com/docs) for available endpoints, request formats, and response formats.

## Reference

Run `lix-agents --help` for the full command reference.

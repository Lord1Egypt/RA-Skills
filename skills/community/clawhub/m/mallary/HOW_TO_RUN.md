# How to Run the Mallary CLI

You can run the CLI in several ways.

## Option 1: Run the Built File Directly

The built file at `cli/dist/index.js` is executable.

```bash
# From the repository root
node cli/dist/index.js --help

# Or run it directly (it has a shebang)
./cli/dist/index.js --help

# Example authenticated command. Set MALLARY_API_KEY from a secret store first
test -n "${MALLARY_API_KEY:-}" && echo "MALLARY_API_KEY is set"
node cli/dist/index.js posts list
node cli/dist/index.js profiles list
```

## Option 2: Link Globally (Recommended for Development)

This creates a global `mallary` command you can use anywhere.

```bash
# From the CLI directory
cd cli
npm link

# Now you can use it anywhere
mallary --help
mallary profiles list
mallary posts list

# To unlink later
npm unlink -g @mallary/cli
```

After you link the package, you can use `mallary` from any directory.

## Option 3: Use npm Scripts (From `cli/`)

```bash
# From the CLI directory
cd cli
npm run build
npm run start -- --help
npm run start -- profiles list
npm run start -- posts list
```

## Option 4: Use npm/npx (Published Package)

After you publish or install the package from npm:

```bash
# Install globally
npm install -g @mallary/cli

# Or use with npx (no global install)
npx @mallary/cli --help
npx @mallary/cli profiles list
npx @mallary/cli posts list
```

## Quick Setup Guide

Use `mallary profiles list` to find a non-default profile ID. Replace `AbC123xYz90` in examples with a real public profile ID, or omit `--profile-id` to use the default profile.

### Step 1: Build the CLI

```bash
# From the repository root
cd cli
npm install
npm run build
```

### Step 2: Set Your API Key

Security: `MALLARY_API_KEY` is a bearer secret. Do not commit it, paste it into prompts or tickets, print it in logs, or expose it in shell history. Use your password manager, a locked-down untracked env file, or a CI secret store for persistent use.

```bash
read -rsp "Mallary API key: " MALLARY_API_KEY; echo; export MALLARY_API_KEY
```

### Step 3: Choose Your Method

For quick testing:

```bash
node cli/dist/index.js --help
```

For regular use:

```bash
cd cli
npm link
mallary --help
```

## Troubleshooting

### "Command not found: mallary"

If you linked globally but still get this error:

```bash
# Make sure that the link exists
which mallary

# If it is not found, link it again
cd cli
npm link

# Or look at your PATH
echo $PATH
```

### "MALLARY_API_KEY is not set"

```bash
read -rsp "Mallary API key: " MALLARY_API_KEY; echo; export MALLARY_API_KEY

# Make sure that it is set without printing the key
test -n "${MALLARY_API_KEY:-}" && echo "MALLARY_API_KEY is set"
```

### Permission Denied

If you get permission errors when you run the built file directly:

```bash
# Make the file executable
chmod +x cli/dist/index.js

# Then try again
./cli/dist/index.js --help
```

### Rebuild After Changes

After you change the code, build it again:

```bash
cd cli
npm run build
```

If you linked globally, the new build applies to the `mallary` command.

## Testing the CLI

### Test Help Command

```bash
mallary --help
node cli/dist/index.js help posts create
```

### Test with Safe Read-Only Commands (requires API key)

```bash
test -n "${MALLARY_API_KEY:-}" && echo "MALLARY_API_KEY is set"

# Health check
mallary health

# Profile discovery
mallary profiles list
```

### Optional Real Publish Check

Warning: `mallary posts create` publishes or schedules content on the selected connected social-media account. Do not run it as a harmless test. First, make sure that the profile ID and the platform point to the account for the real public post.

```bash
# Publishes a real Facebook post to the selected profile
mallary posts create \
  --message "Intentional publish from Mallary CLI" \
  --platform facebook \
  --profile-id AbC123xYz90
```

## Development Workflow

### 1. Make Changes

Edit files in `cli/src/`.

### 2. Rebuild

```bash
cd cli
npm run build
```

### 3. Test

```bash
# If linked globally
mallary --help

# Or direct execution
node cli/dist/index.js --help
```

### 4. Run Tests

```bash
cd cli
npm test
```

## Environment Variables

### Required

- `MALLARY_API_KEY` - your Mallary API key

Treat `MALLARY_API_KEY` as a bearer credential. Store it in a secret manager, a locked-down untracked env file, or a masked CI secret. Do not commit it. Do not paste it into prompts or tickets. Do not print it with `echo` or `printenv`. Do not enable shell tracing around it. Do not share logs that contain it. If the key is exposed, rotate or revoke it.

### Setting Environment Variables

Temporary:

```bash
# For bash/zsh, without printing the key
read -rsp "Mallary API key: " MALLARY_API_KEY; echo; export MALLARY_API_KEY

# For fish, without printing the key
read --silent --prompt-str "Mallary API key: " MALLARY_API_KEY; set -gx MALLARY_API_KEY $MALLARY_API_KEY

# For PowerShell
$env:MALLARY_API_KEY="your_key"
```

Persistent local storage:

Use a password manager, a shell secret plugin, an OS keychain, or an untracked env file with restrictive permissions. Do not write real keys into shared dotfiles. Do not write them into commands that the shell history can save.

## Using Aliases

If you want a shorter command:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias my='mallary'

# Now you can use
my posts list
```

## Production Deployment

### Install from npm

```bash
# Global install
npm install -g @mallary/cli

# Project-specific or one-off use
npx @mallary/cli --help
```

## Summary of Methods

| Method                | Command                      | Best For               |
| --------------------- | ---------------------------- | ---------------------- |
| Direct node execution | `node cli/dist/index.js ...` | Quick local testing    |
| Direct executable     | `./cli/dist/index.js ...`    | Quick local testing    |
| npm link              | `mallary ...`                | Day-to-day development |
| npm scripts           | `npm run start -- ...`       | Working inside `cli/`  |
| npm global install    | `mallary ...`                | Published usage        |
| npx                   | `npx @mallary/cli ...`       | One-off usage          |

## Recommended Setup

```bash
# 1. Build
cd cli && npm install && npm run build

# 2. Link globally
npm link

# 3. Confirm API key is available without printing it
test -n "${MALLARY_API_KEY:-}" && echo "MALLARY_API_KEY is set"

# 4. Test
mallary health

# 5. Start with read-only commands
mallary profiles list
```

Do not include `mallary posts create` in setup smoke tests. It publishes or schedules a post on a connected social-media account. Before you use the optional real publish check above, make sure that the target profile and the platform are correct. Also make sure that the message and the media are correct. Also make sure that the user wants a public or scheduled post.

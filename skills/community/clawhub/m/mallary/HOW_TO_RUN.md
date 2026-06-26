# How to Run the Mallary CLI

There are several ways to run the CLI, depending on your needs.

## Option 1: Direct Execution (Quick Test)

The built file at `cli/dist/index.js` is executable.

```bash
# From the repository root
node cli/dist/index.js --help

# Or run it directly (it has a shebang)
./cli/dist/index.js --help

# Example command
export MALLARY_API_KEY=your_key
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
mallary posts create --message "Hello!" --platform facebook --profile-id AbC123xYz90

# To unlink later
npm unlink -g @mallary/cli
```

After linking, you can use `mallary` from any directory.

## Option 3: Use npm Scripts (From `cli/`)

```bash
# From the CLI directory
cd cli
npm run build
npm run start -- --help
npm run start -- profiles list
npm run start -- posts list
npm run start -- posts create --message "Hello" --platform facebook
```

## Option 4: Use npm/npx (Published Package)

Once published or installed from npm:

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

```bash
export MALLARY_API_KEY=your_api_key_here

# To make it permanent, add to your shell profile:
echo 'export MALLARY_API_KEY=your_api_key_here' >> ~/.zshrc
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
# Check if it's linked
which mallary

# If not found, try linking again
cd cli
npm link

# Or check your PATH
echo $PATH
```

### "MALLARY_API_KEY is not set"

```bash
export MALLARY_API_KEY=your_key

# Verify it's set
echo $MALLARY_API_KEY
```

### Permission Denied

If you get permission errors when running the built file directly:

```bash
# Make the file executable
chmod +x cli/dist/index.js

# Then try again
./cli/dist/index.js --help
```

### Rebuild After Changes

After making code changes, rebuild:

```bash
cd cli
npm run build
```

If you linked globally, your changes will be reflected after the rebuild.

## Testing the CLI

### Test Help Command

```bash
mallary --help
node cli/dist/index.js help posts create
```

### Test with Sample Command (requires API key)

```bash
export MALLARY_API_KEY=your_key

# Health check
mallary health

# Profile discovery
mallary profiles list

# Create a test post
mallary posts create \
  --message "Test post from CLI" \
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

### Setting Environment Variables

Temporary:

```bash
# For bash/zsh
export MALLARY_API_KEY=your_key

# For fish
set -x MALLARY_API_KEY your_key

# For PowerShell
$env:MALLARY_API_KEY="your_key"
```

Permanent:

```bash
# For bash
echo 'export MALLARY_API_KEY=your_key' >> ~/.bashrc

# For zsh
echo 'export MALLARY_API_KEY=your_key' >> ~/.zshrc
```

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

# 3. Set API key
export MALLARY_API_KEY=your_key

# 4. Test
mallary health

# 5. Start using
mallary profiles list
mallary posts create --message "My first post" --platform facebook --profile-id AbC123xYz90
```

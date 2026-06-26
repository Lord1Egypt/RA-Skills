---
name: nvs-node-version-switcher
description: Manage Node.js versions using NVS (Node Version Switcher). Use when switching Node.js versions, installing new versions, managing version aliases, or when the user mentions NVS, node version management, or needs to change the active Node.js version in the current environment.
---

# NVS Node.js Version Manager

NVS (Node Version Switcher) is a cross-platform tool for managing multiple Node.js versions. It allows you to easily install, switch between, and manage different Node.js versions and their associated npm packages.

## Quick Start

### Check if NVS is installed
```bash
nvs --version
```

### If NVS is not installed, install it first

#### Windows (PowerShell or Command Prompt)
```powershell
# Using winget (Windows 11+)
winget install jasongin.nvs

# Or using chocolatey
choco install nvs

# Manual installation
$env:NVS_HOME="$env:LOCALAPPDATA\nvs"
git clone https://github.com/jasongin/nvs "$env:NVS_HOME"
. "$env:NVS_HOME\nvs.ps1" install
```

#### Mac/Linux
```bash
export NVS_HOME="$HOME/.nvs"
git clone https://github.com/jasongin/nvs "$NVS_HOME"
. "$NVS_HOME/nvs.sh" install
```

## Basic Commands

### Install Node.js versions
```bash
# Install latest version
nvs add latest

# Install latest LTS version
nvs add lts

# Install specific version
nvs add 18.20.0

# Install with specific architecture
nvs add 18.20.0/x64
```

### Switch between versions
```bash
# Use a version in current shell session
nvs use 18.20.0

# Use LTS version
nvs use lts

# Set default version (permanent)
nvs link 18.20.0

# Remove default link
nvs unlink 18.20.0
```

### List versions
```bash
# List locally installed versions
nvs ls

# List available remote versions
nvs ls-remote

# Filter remote versions
nvs ls-remote 18
nvs ls-remote lts
```

### Remove versions
```bash
nvs rm 16.20.0
```

## Advanced Features

### Automatic version switching
Enable automatic switching based on `.node-version` or `.nvmrc` files:
```bash
# Enable auto-switching
nvs auto on

# Disable auto-switching
nvs auto off

# Manual trigger for current directory
nvs auto
```

### Version aliases
```bash
# Create an alias
nvs alias myproject 18.20.0

# List all aliases
nvs alias

# Remove an alias
nvs alias myproject
```

### Run commands with specific versions
```bash
# Run a script with specific Node version
nvs run 18.20.0 app.js

# Execute a command with specific version
nvs exec 18.20.0 npm test
```

### Migrate global packages
```bash
# Migrate global npm packages from one version to another
nvs migrate 16.20.0 18.20.0
```

### Remote configuration
```bash
# List configured remotes
nvs remote

# Add custom remote (e.g., nightly builds)
nvs remote add nightly https://nodejs.org/download/nightly/

# Use custom remote
nvs add nightly/18
```

## Common Workflows

### Project Setup Workflow
1. Check if project has `.node-version` or `.nvmrc` file
2. If NVS not installed, install it
3. Install required Node.js version
4. Enable auto-switching if needed
5. Verify the correct version is active

### Version Upgrade Workflow
1. Check current version: `nvs ls`
2. Install new version: `nvs add latest`
3. Test with new version: `nvs use latest`
4. Migrate global packages if needed: `nvs migrate <old> <new>`
5. Set as default if satisfied: `nvs link latest`

### Troubleshooting
- If `nvs` command not found, ensure NVS is properly installed and shell is restarted
- Check `NVS_HOME` environment variable points to correct directory
- Use `nvs which <version>` to verify version paths
- For permission issues on Mac/Linux, check NVS installation directory permissions

## Environment Variables
- `NVS_HOME`: Directory where NVS stores Node.js versions (default: `~/.nvs` on Mac/Linux, `%LOCALAPPDATA%\nvs` on Windows)
- `NVS_NODE_HOME`: Alternative location for Node.js installations

## Integration with VS Code
NVS integrates with Visual Studio Code for debugging with specific Node.js versions. Configure in `.vscode/launch.json`:
```json
{
  "runtimeArgs": ["18.20.0"],
  "windows": { "runtimeExecutable": "nvs.cmd" },
  "osx": { "runtimeExecutable": "nvs" },
  "linux": { "runtimeExecutable": "nvs" }
}
```

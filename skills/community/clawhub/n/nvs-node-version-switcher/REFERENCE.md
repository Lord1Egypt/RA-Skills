# NVS Command Reference

This document provides detailed information about all NVS commands and their usage.

## Core Commands

### `nvs add [version]`
Downloads and installs a Node.js version.

**Examples:**
```bash
nvs add                    # Interactive selection
nvs add latest             # Latest version
nvs add lts                # Latest LTS
nvs add 18                 # Latest 18.x.x
nvs add 18.20              # Latest 18.20.x
nvs add 18.20.0            # Specific version
nvs add 18.20.0/x64        # Specific architecture
nvs add node/18.20.0       # From specific remote
```

### `nvs use [version]`
Switches to a Node.js version in the current shell session.

**Examples:**
```bash
nvs use                    # Interactive selection
nvs use 18.20.0           # Specific version
nvs use lts               # LTS version
nvs use auto              # Auto-detect from .node-version/.nvmrc
nvs use 18.20.0/x64       # Specific architecture
```

### `nvs link [version]`
Sets a version as the default (permanent across shell sessions).

**Examples:**
```bash
nvs link                  # Link current version
nvs link 18.20.0         # Link specific version
nvs link lts             # Link LTS version
nvs unlink               # Remove default link
nvs unlink 18.20.0       # Unlink specific version
```

### `nvs rm <version>`
Removes an installed Node.js version.

**Examples:**
```bash
nvs rm 16.20.0           # Remove specific version
nvs rm 16                # Remove all 16.x versions
```

## Information Commands

### `nvs ls [filter]`
Lists locally installed Node.js versions.

**Output symbols:**
- `>` - Currently active version
- `#` - Default (linked) version

**Examples:**
```bash
nvs ls                   # List all local versions
nvs ls 18                # Filter by major version
nvs ls lts               # Show LTS versions only
```

### `nvs ls-remote [filter]`
Lists Node.js versions available for download.

**Examples:**
```bash
nvs ls-remote           # List all available versions
nvs ls-remote 18        # Filter by major version
nvs ls-remote lts       # Show LTS versions only
nvs ls-remote nightly   # Show nightly builds
```

### `nvs which [version]`
Shows the path to a Node.js binary.

**Examples:**
```bash
nvs which               # Current version path
nvs which 18.20.0      # Specific version path
nvs which lts          # LTS version path
```

### `nvs --version`
Displays the NVS tool version.

## Advanced Commands

### `nvs auto [on|off]`
Controls automatic version switching based on `.node-version` or `.nvmrc` files.

**Examples:**
```bash
nvs auto on            # Enable auto-switching
nvs auto off           # Disable auto-switching
nvs auto               # Manual trigger for current directory
```

### `nvs alias [name] [value]`
Manages version aliases.

**Examples:**
```bash
nvs alias myapp 18.20.0    # Create alias
nvs alias                  # List all aliases
nvs alias myapp            # Remove alias
nvs run myapp --version    # Use alias
```

### `nvs remote [name] [value]`
Manages download source remotes.

**Examples:**
```bash
nvs remote                    # List remotes
nvs remote add nightly https://nodejs.org/download/nightly/
nvs remote remove nightly     # Remove remote
nvs ls-remote nightly/18      # Use custom remote
```

### `nvs migrate <fromver> [tover]`
Migrates global npm packages between Node.js versions.

**Examples:**
```bash
nvs migrate 16.20.0 18.20.0    # Migrate between versions
nvs migrate 16                 # Migrate from latest 16.x
```

### `nvs upgrade [fromver]`
Upgrades to the latest patch version of a major release.

**Examples:**
```bash
nvs upgrade 18              # Upgrade latest 18.x to latest patch
nvs upgrade 18.20           # Upgrade 18.20.x to latest patch
```

### `nvs run <ver> <js> [args...]`
Runs a JavaScript file with a specific Node.js version.

**Examples:**
```bash
nvs run 18.20.0 app.js
nvs run lts script.js --arg1 --arg2
```

### `nvs exec <ver> <exe> [args...]`
Executes a command with a specific Node.js version.

**Examples:**
```bash
nvs exec 18.20.0 npm test
nvs exec lts node --version
```

## Installation Commands

### `nvs install`
Initializes NVS in the current shell environment.

**Usage:**
```bash
# After cloning NVS repo
. "$NVS_HOME/nvs.sh" install    # Mac/Linux
. "$env:NVS_HOME\nvs.ps1" install  # Windows PowerShell
```

### `nvs uninstall`
Removes NVS from the shell environment.

## Version Specification Format

Versions can be specified in multiple formats:

- **Semantic version**: `18.20.0`, `18.20`, `18`
- **Labels**: `latest`, `lts`, `argon`, `boron`, etc.
- **With architecture**: `18.20.0/x64`, `18.20.0/x86`
- **With remote**: `node/18.20.0`, `nightly/18`
- **Aliases**: Any user-defined alias name

## Environment Variables

- **NVS_HOME**: Base directory for NVS installation and Node.js versions
  - Default: `~/.nvs` (Mac/Linux), `%LOCALAPPDATA%\nvs` (Windows)
- **NVS_NODE_HOME**: Alternative location for Node.js installations
- **NVS_ARCH**: Default architecture (x64, x86, arm, arm64)

## Shell Integration

### Bash/Zsh
The `nvs.sh` script adds the `nvs` function to your shell. The install command automatically adds sourcing to your profile files.

### PowerShell
The `nvs.ps1` script provides similar functionality for PowerShell environments.

### Windows Command Prompt
The `nvs.cmd` batch file provides basic functionality for cmd.exe.

## File-Based Version Control

### `.node-version`
Place this file in your project root to specify the required Node.js version:
```
18.20.0
```

### `.nvmrc`
Compatible with nvm, can also be used by NVS:
```
lts/fermium
```

When `nvs auto on` is enabled, NVS will automatically switch to the version specified in these files when you change directories.

# NVS Usage Examples

This document provides practical examples of common NVS workflows and use cases.

## Basic Version Management

### Installing Node.js Versions

```bash
# Install the latest stable version
nvs add latest

# Install the latest LTS (Long Term Support) version
nvs add lts

# Install a specific major version (latest patch)
nvs add 18

# Install a specific minor version (latest patch)
nvs add 18.20

# Install an exact version
nvs add 18.20.0

# Install with specific architecture
nvs add 18.20.0/x64
nvs add 18.20.0/x86
```

### Switching Between Versions

```bash
# Switch to a specific version for current session
nvs use 18.20.0

# Switch to LTS version
nvs use lts

# Switch to latest version
nvs use latest

# Make a version the default (persistent across sessions)
nvs link 18.20.0

# Remove the default version link
nvs unlink
```

## Project-Specific Workflows

### Setting Up a New Project

```bash
# Check if project specifies a Node.js version
cat .node-version    # or cat .nvmrc

# If NVS is not installed, install it first
# (Use the install_nvs.sh script or manual installation)

# Install the required version
nvs add 18.20.0      # Replace with version from .node-version

# Use the version for current session
nvs use 18.20.0

# Enable automatic switching for this project
nvs auto on
```

### Working with Multiple Projects

```bash
# Project A requires Node 16
cd project-a
nvs use 16.20.0

# Project B requires Node 18
cd ../project-b
nvs use 18.20.0

# With auto-switching enabled, NVS will automatically
# switch versions when you change directories
nvs auto on
```

## Advanced Usage

### Using Aliases

```bash
# Create meaningful aliases for your projects
nvs alias project-a 16.20.0
nvs alias project-b 18.20.0
nvs alias latest-lts lts

# Use aliases instead of version numbers
nvs use project-a
nvs run project-b app.js

# List all aliases
nvs alias

# Remove an alias
nvs alias project-a
```

### Running Commands with Specific Versions

```bash
# Run a script with a specific Node.js version
nvs run 18.20.0 server.js

# Execute npm commands with specific version
nvs exec 18.20.0 npm test
nvs exec lts npm run build

# Check version without switching
nvs which 18.20.0
nvs run 18.20.0 --version
```

### Managing Global Packages

```bash
# When you switch versions, global packages are version-specific
# To migrate global packages between versions:
nvs migrate 16.20.0 18.20.0

# Upgrade to latest patch version and migrate packages
nvs upgrade 18.20
```

### Working with Custom Remotes

```bash
# Add nightly builds remote
nvs remote add nightly https://nodejs.org/download/nightly/

# List available nightly versions
nvs ls-remote nightly/18

# Install a nightly build
nvs add nightly/18.1.0-nightly20230101abc123

# Add io.js remote (historical)
nvs remote add iojs https://iojs.org/dist/
```

## Automation and CI/CD

### Using NVS in Scripts

```bash
#!/bin/bash
# build.sh - Build script with specific Node.js version

# Ensure we're using the correct version
nvs use 18.20.0

# Verify the version
echo "Using Node.js $(node --version)"

# Run build commands
npm ci
npm run build
npm test
```

### Docker Integration

```dockerfile
# Dockerfile example using NVS
FROM ubuntu:22.04

# Install NVS
RUN export NVS_HOME="/root/.nvs" && \
    git clone https://github.com/jasongin/nvs "$NVS_HOME" && \
    . "$NVS_HOME/nvs.sh" install && \
    nvs add 18.20.0 && \
    nvs use 18.20.0

# Set PATH to include NVS Node.js
ENV PATH="/root/.nvs/node/18.20.0/x64/bin:${PATH}"

WORKDIR /app
COPY . .
RUN npm ci && npm run build
```

## Troubleshooting Examples

### Common Issues and Solutions

```bash
# Issue: nvs command not found
# Solution: Ensure NVS is properly installed and shell is restarted
which nvs
echo $NVS_HOME

# Issue: Permission denied on Mac/Linux
# Solution: Check NVS_HOME directory permissions
ls -la ~/.nvs
chmod -R u+w ~/.nvs

# Issue: Wrong version showing after switch
# Solution: Verify the switch worked
nvs use 18.20.0
node --version
nvs which 18.20.0

# Issue: Auto-switching not working
# Solution: Check if .node-version file exists and auto is enabled
cat .node-version
nvs auto on
nvs auto  # Manual trigger
```

### Diagnostic Commands

```bash
# Check NVS installation status
nvs --version

# List all installed versions with current/default indicators
nvs ls

# Show path to current Node.js binary
nvs which

# Check environment variables
echo $NVS_HOME
echo $PATH | tr ':' '\n' | grep nvs

# Test version switching
nvs use 18.20.0 && node --version
nvs use lts && node --version
```

## Integration Examples

### VS Code Configuration

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch with NVS",
      "program": "${file}",
      "runtimeArgs": ["18.20.0"],
      "windows": {
        "runtimeExecutable": "nvs.cmd"
      },
      "osx": {
        "runtimeExecutable": "nvs"
      },
      "linux": {
        "runtimeExecutable": "nvs"
      }
    }
  ]
}
```

### Git Hooks Integration

Create `.git/hooks/post-checkout`:
```bash
#!/bin/bash
# Automatically switch Node.js version when checking out branches

if [ -f .node-version ]; then
    nvs use auto
    echo "Switched to Node.js $(node --version) based on .node-version"
fi
```

These examples cover the most common NVS usage patterns. For more detailed command reference, see [REFERENCE.md](REFERENCE.md).

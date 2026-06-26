# NVS Node Version Switcher Skill

This skill provides comprehensive guidance for using NVS (Node Version Switcher) to manage multiple Node.js versions in your development environment.

## What is NVS?

NVS is a cross-platform utility for switching between different versions and forks of Node.js. It's inspired by nvm but works consistently across Windows, macOS, and Linux.

## When to Use This Skill

Use this skill when you need to:
- Install or switch between different Node.js versions
- Set up Node.js environments for different projects
- Manage Node.js version aliases
- Configure automatic version switching
- Troubleshoot Node.js version issues

## Skill Structure

```
nvs-node-version-switcher/
├── SKILL.md          # Main skill instructions and quick start guide
├── REFERENCE.md      # Detailed command reference
├── EXAMPLES.md       # Practical usage examples and workflows
└── scripts/          # Utility scripts
    ├── check_nvs_status.sh   # Check NVS installation status
    └── install_nvs.sh        # Auto-install NVS if not present
```

## Quick Start

1. **Check if NVS is installed:**
   ```bash
   nvs --version
   ```

2. **If not installed, use the auto-install script:**
   ```bash
   .lingma/skills/nvs-node-version-switcher/scripts/install_nvs.sh
   ```

3. **Install a Node.js version:**
   ```bash
   nvs add lts
   nvs use lts
   ```

## Key Features Covered

- ✅ Cross-platform installation (Windows, macOS, Linux)
- ✅ Version management (install, switch, remove)
- ✅ Automatic version switching per project
- ✅ Alias management
- ✅ Global package migration
- ✅ Custom remote configuration
- ✅ Integration with VS Code and CI/CD

## Common Commands

```bash
# Install versions
nvs add latest
nvs add lts
nvs add 18.20.0

# Switch versions
nvs use 18.20.0
nvs link 18.20.0  # Set as default

# List versions
nvs ls            # Local versions
nvs ls-remote     # Available versions

# Auto-switching
nvs auto on       # Enable per-directory switching
```

## Files Overview

- **SKILL.md**: Main entry point with essential commands and workflows
- **REFERENCE.md**: Complete command reference with all options and parameters
- **EXAMPLES.md**: Real-world usage scenarios and integration examples
- **scripts/**: Helper scripts for common tasks

## Integration with Lingma

This skill automatically activates when:
- You mention NVS or node version management
- You need to switch Node.js versions
- You're setting up a new project with specific Node.js requirements
- You encounter Node.js version compatibility issues

The agent will provide context-appropriate guidance based on your operating system and specific needs.

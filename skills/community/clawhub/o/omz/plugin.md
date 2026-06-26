# Oh My Zsh Plugin Management

Add plugins to the `plugins=()` array in .zshrc and install external plugins as needed.

## Recommended Plugins (Default Setup)

| Plugin | Type | Description |
|--------|------|-------------|
| asdf | built-in | Runtime version management (Node, Python, etc.) |
| git | built-in | git aliases and completions |
| zoxide | built-in | Smart directory jump (`z`, `zi`) |

## Plugin Addition Procedure

### 1. Built-in Plugins (No Installation Required)

Plugins already included in `$ZSH/plugins/` only need their name added to `.zshrc`:

```bash
# Find the plugins=() array in .zshrc and add
plugins=(git docker kubectl ...)
```

**Key built-in plugins**: git, docker, kubectl, npm, node, python, pip, brew, macos, history, z, sudo, extract, web-search

### 2. External Plugins (Clone Required)

Clone to `$ZSH_CUSTOM/plugins/` then add to `.zshrc`:

```bash
# Clone
git clone https://github.com/{org}/{plugin}.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/{plugin}

# Add to .zshrc plugins array
plugins=(... {plugin})
```

**Commonly used external plugins**:

| Plugin | Repository | Description |
|--------|------------|-------------|
| zsh-autosuggestions | zsh-users/zsh-autosuggestions | History-based autosuggestions |
| zsh-syntax-highlighting | zsh-users/zsh-syntax-highlighting | Command syntax highlighting |
| zsh-completions | zsh-users/zsh-completions | Additional completions |
| you-should-use | MichaelAqworthy/zsh-you-should-use | Alias usage reminders |

### 3. chezmoi Integration

If dotfiles are managed with chezmoi:

```bash
# After modifying .zshrc
chezmoi re-add ~/.zshrc

# Register external plugins in .chezmoiexternal.toml
# (see chezmoi skill)
```

## Verify Plugins

```bash
# Currently loaded plugins
echo $plugins

# List available built-in plugins
ls $ZSH/plugins/

# List installed custom plugins
ls ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/
```

## Notes

- The `plugins=()` array is **space-separated without commas**
- Plugin order: `zsh-syntax-highlighting` should be placed **last**
- Too many plugins degrade shell startup speed (20 or fewer recommended)

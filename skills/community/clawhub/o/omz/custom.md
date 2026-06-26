# Oh My Zsh Custom Script Authoring

Write `$ZSH_CUSTOM/*.zsh` files based on requirements.

## $ZSH_CUSTOM Path

```bash
echo $ZSH_CUSTOM  # default: ~/.oh-my-zsh/custom
```

## File Structure

```
$ZSH_CUSTOM/
├── aliases.zsh       # custom aliases
├── functions.zsh     # custom functions
├── env.zsh           # environment variables
├── keybindings.zsh   # key bindings
└── plugins/          # external plugins (see plugin topic)
```

**Rule**: Files with `*.zsh` extension are auto-loaded on Oh My Zsh startup (alphabetical order)

## Authoring Procedure

### 1. Gather Requirements

Confirm the following with the user:
- What functionality is needed (alias, function, environment variable, key binding, etc.)
- Whether existing custom files already exist

### 2. Select or Create the Appropriate File

| Purpose | Filename | Example |
|---------|----------|---------|
| Shortcut commands | `aliases.zsh` | `alias k="kubectl"` |
| Reusable functions | `functions.zsh` | `mkcd() { mkdir -p "$1" && cd "$1" }` |
| Environment variables | `env.zsh` | `export EDITOR=vim` |
| Key bindings | `keybindings.zsh` | `bindkey '^[[A' history-search-backward` |
| Tool-specific config | `{tool}.zsh` | `docker.zsh`, `k8s.zsh` |

### 3. Write the File

```bash
# Create/modify file
# Write directly to the $ZSH_CUSTOM path
```

### 4. chezmoi Integration

If dotfiles are managed with chezmoi:

```bash
# Add a new file
chezmoi add $ZSH_CUSTOM/{filename}.zsh

# After modifying an existing file
chezmoi re-add $ZSH_CUSTOM/{filename}.zsh
```

## Notes

- Only `.zsh` extensions are auto-loaded (`.sh` is ignored)
- Load order: alphabetical -- use prefixes if order matters (`01-env.zsh`, `02-aliases.zsh`)
- Separate into custom files instead of writing directly in `.zshrc` to avoid update conflicts
- Apply changes with `source ~/.zshrc` or by opening a new terminal

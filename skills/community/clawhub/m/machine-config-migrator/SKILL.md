---
name: machine-config-migrator
description: Migrate workstation configuration from an old machine to a new one with selectable components and plugin-aware transfer. Use when users ask to backup, move, restore, or replicate tmux, Vim/Neovim, Emacs, Zsh, Alfred, Git, or SSH-related setup across devices and need controlled component selection, backup safety, and optional plugin reinstall guidance.
---

# Machine Config Migrator

Perform repeatable, low-risk migration of editor/shell/productivity configuration between machines.

## Workflow

1. Confirm source and target OS details and whether cross-platform migration is expected.
2. Choose components to include from: `tmux`, `vim`, `emacs`, `zsh`, `alfred`, `git`, `ssh`.
3. Run `scripts/collect_config_bundle.py` on the old machine to create one tarball bundle.
4. Transfer the bundle to the new machine.
5. Run `scripts/apply_config_bundle.py` on the new machine with selected components.
6. Use plugin mode:
   - `suggest` to print plugin install commands.
   - `run` to execute known plugin installers automatically.
7. Validate startup for each selected tool (`tmux`, `vim`/`nvim`, `emacs`, `zsh`, Alfred).

## Commands

Collect from old machine:

```bash
python3 scripts/collect_config_bundle.py \
  --bundle ~/machine-config-bundle.tar.gz \
  --components tmux,vim,emacs,zsh,alfred
```

Apply on new machine:

```bash
python3 scripts/apply_config_bundle.py \
  --bundle ~/machine-config-bundle.tar.gz \
  --components tmux,vim,zsh,alfred \
  --plugin-mode suggest
```

Apply with plugin installers:

```bash
python3 scripts/apply_config_bundle.py \
  --bundle ~/machine-config-bundle.tar.gz \
  --components tmux,vim,emacs,zsh \
  --plugin-mode run
```

Dry run before writing files:

```bash
python3 scripts/apply_config_bundle.py \
  --bundle ~/machine-config-bundle.tar.gz \
  --components tmux,vim,zsh \
  --dry-run
```

## Safety Rules

- Run with `--dry-run` first when target machine already has custom configs.
- Do not migrate private keys by default; `ssh` component includes only safe defaults (`config`, `known_hosts`).
- Keep backup path from apply output. Existing files are copied before overwrite.
- Prefer component-by-component rollout instead of all-at-once on first migration.

## Plugin Handling

- Trust plugin inventory generated during collection for migration context.
- Use `references/plugin-sources.md` when users ask to discover additional plugins.
- If plugin manager is missing on target machine, install manager first, then rerun with `--plugin-mode run`.

## Resources

- `scripts/collect_config_bundle.py`: Build a portable config bundle and plugin inventory.
- `scripts/apply_config_bundle.py`: Restore selected components with backup and optional plugin install.
- `references/plugin-sources.md`: Curated official plugin catalogs and popular plugin picks.

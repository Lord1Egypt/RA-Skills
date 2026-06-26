# Plugin Sources and Picks

Use these catalogs when users ask for "available plugins", "popular plugins", or "what should I install on the new machine".

## Tmux

- Plugin manager:
  - TPM: <https://github.com/tmux-plugins/tpm>
- Catalog:
  - TPM plugin list: <https://github.com/tmux-plugins/list>
- Common picks:
  - `tmux-plugins/tmux-sensible`
  - `tmux-plugins/tmux-resurrect`
  - `tmux-plugins/tmux-continuum`
  - `tmux-plugins/tmux-yank`
  - `christoomey/vim-tmux-navigator`

## Vim and Neovim

- Plugin managers:
  - vim-plug: <https://github.com/junegunn/vim-plug>
  - lazy.nvim: <https://github.com/folke/lazy.nvim>
- Catalogs:
  - awesome-neovim: <https://github.com/rockerBOO/awesome-neovim>
- Common picks:
  - `nvim-telescope/telescope.nvim`
  - `nvim-treesitter/nvim-treesitter`
  - `neovim/nvim-lspconfig`
  - `lewis6991/gitsigns.nvim`
  - `nvim-lualine/lualine.nvim`

## Emacs

- Package workflow:
  - use-package: <https://github.com/jwiegley/use-package>
- Package repositories:
  - MELPA: <https://melpa.org/>
- Catalog:
  - awesome-emacs: <https://github.com/emacs-tw/awesome-emacs>
- Common picks:
  - `magit`
  - `company`
  - `flycheck`
  - `projectile`
  - `lsp-mode`

## Zsh

- Plugin framework:
  - Oh My Zsh: <https://ohmyz.sh/>
- Catalog:
  - Official Oh My Zsh plugin wiki: <https://github.com/ohmyzsh/ohmyzsh/wiki/plugins>
- Common picks:
  - `git` (built-in Oh My Zsh plugin)
  - `zsh-autosuggestions`
  - `zsh-syntax-highlighting`
  - `zsh-completions`
  - `fzf`

## Alfred

- Workflow gallery:
  - Official Alfred Gallery: <https://alfred.app/workflows/>
- Common picks:
  - `Google Suggest`
  - `Clipboard History`
  - `Emoji Snippets`
  - `Kagi Search`
  - `Recent Downloads`

## Usage Pattern

1. Pull plugin inventory from `manifest.json` in the collected bundle.
2. Ask user whether to keep existing plugin set or refresh from the catalogs above.
3. If refreshing, propose a minimal starter set first, then category-specific additions.
4. Apply plugin installs after config files are restored.

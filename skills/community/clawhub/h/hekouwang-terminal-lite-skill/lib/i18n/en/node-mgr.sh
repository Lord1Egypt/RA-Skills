#!/bin/bash
# 词条表 · 英文 · node-mgr.sh
# ⚠️ Values that go through printf: escape every %% as %%.

blk_node_help() {
  cat <<'EOF'
hekouwang-terminal-skill — pick / switch the Node version manager

Usage:
  ./scripts/node-mgr.sh                 show which one is active
  ./scripts/node-mgr.sh fnm             switch to fnm (recommended, default)
  ./scripts/node-mgr.sh nvm             switch to nvm
  ./scripts/node-mgr.sh brew            switch to Homebrew node (single version, not a version manager)
  ./scripts/node-mgr.sh vfox            switch to vfox (version-fox)
  ./scripts/node-mgr.sh --lang zh       run in Chinese

Rule: keep exactly one. Mixing fnm / nvm / brew node / vfox makes PATH fight
itself and version switches stop sticking. The choice lives under
~/.config/hekouwang-terminal/; ~/.zshrc only sources that one snippet.
EOF
}

M_NODE_CURRENT="Active Node manager: %s"
M_NODE_NONE="No Node manager chosen yet (install defaults to fnm; switch with ./scripts/node-mgr.sh <name>)"
M_NODE_CHOICES="Choices: fnm · nvm · brew · vfox"
M_NODE_HOW="Switch: ./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
M_NODE_RULE="Rule: keep exactly one — do not mix"
M_NODE_BAD="✗ Unknown '%s'"
M_NODE_NO_BREW="⚠ brew not found; skipping install of %s — install the tool yourself"
M_NODE_PKG_INSTALL="Installing %s..."
M_NODE_PKG_SKIP="%s already installed, skipped"
M_NODE_PKG_OK="✓ %s installed"
M_NODE_PKG_FAIL="⚠ %s failed to install — run brew install by hand later"
M_NODE_NVM_HINT="💡 If nvm is not installed yet: brew install nvm, or follow https://github.com/nvm-sh/nvm into ~/.nvm"
M_NODE_VFOX_HINT="💡 After vfox is installed: vfox add nodejs && vfox install nodejs@latest && vfox use nodejs@latest"
M_NODE_WRITE_FAIL="✗ Could not write node.sh (is config/node/ complete?)"
M_NODE_DONE="✓ Switched to %s"
M_NODE_REOPEN="Open a new tab (or source ~/.zshrc) for it to take effect"
M_NODE_ZSHRC_HINT="💡 Your ~/.zshrc does not source node.sh yet — replace the Node block with the two lines from the template, or re-run ./scripts/install.sh"

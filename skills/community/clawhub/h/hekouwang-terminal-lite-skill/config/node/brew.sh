# hekouwang-terminal-skill · Node via Homebrew (single version, not a version manager)
# brew install node → one current Node on PATH. For per-project versions use fnm/nvm/vfox.
# Do not also load fnm / nvm / vfox in the same shell.
if [ -n "${HOMEBREW_PREFIX:-}" ] && [ -d "$HOMEBREW_PREFIX/opt/node/bin" ]; then
  export PATH="$HOMEBREW_PREFIX/opt/node/bin:$PATH"
elif command -v brew >/dev/null 2>&1; then
  _hkw_node_bin="$(brew --prefix node 2>/dev/null)/bin"
  [ -d "$_hkw_node_bin" ] && export PATH="$_hkw_node_bin:$PATH"
  unset _hkw_node_bin
fi

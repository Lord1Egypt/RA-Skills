# hekouwang-terminal-skill · Node via nvm
# Official ~/.nvm install, or the Homebrew nvm formula. Pick one install path.
# Do not also load fnm / brew node / vfox in the same shell.
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  # shellcheck disable=SC1090
  . "$NVM_DIR/nvm.sh"
elif [ -n "${HOMEBREW_PREFIX:-}" ] && [ -s "$HOMEBREW_PREFIX/opt/nvm/nvm.sh" ]; then
  # shellcheck disable=SC1090
  . "$HOMEBREW_PREFIX/opt/nvm/nvm.sh"
elif [ -s /opt/homebrew/opt/nvm/nvm.sh ]; then
  # shellcheck disable=SC1091
  . /opt/homebrew/opt/nvm/nvm.sh
elif [ -s /usr/local/opt/nvm/nvm.sh ]; then
  # shellcheck disable=SC1091
  . /usr/local/opt/nvm/nvm.sh
fi
unset NVM_BIN 2>/dev/null || true

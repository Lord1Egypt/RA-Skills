# hekouwang-terminal-skill · Node via fnm
# Fast Node Manager — loads fast, switches on cd (.nvmrc / .node-version).
# Do not also load nvm / brew node / vfox in the same shell.
command -v fnm >/dev/null && eval "$(fnm env --use-on-cd)"

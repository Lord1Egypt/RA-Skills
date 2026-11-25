#!/bin/bash
# 词条表 · 中文 · node-mgr.sh

blk_node_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 选 / 换 Node 版本管理器

用法:
  ./scripts/node-mgr.sh                 看当前选了哪个
  ./scripts/node-mgr.sh fnm             换成 fnm（推荐，默认）
  ./scripts/node-mgr.sh nvm             换成 nvm
  ./scripts/node-mgr.sh brew            换成 Homebrew 的 node（单版本，不是版本管理器）
  ./scripts/node-mgr.sh vfox            换成 vfox（version-fox）
  ./scripts/node-mgr.sh --lang en       切回英文

铁律：整台机器只留一套。混用 fnm / nvm / brew node / vfox 会让 PATH 打架、
切版本不生效。选择写进 ~/.config/hekouwang-terminal/，~/.zshrc 只 source 那一份。
EOF
}

M_NODE_CURRENT="当前 Node 管理器：%s"
M_NODE_NONE="还没选过 Node 管理器（装机默认 fnm；想换：./scripts/node-mgr.sh <名字>）"
M_NODE_CHOICES="可选：fnm · nvm · brew · vfox"
M_NODE_HOW="切换：./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
M_NODE_RULE="铁律：只留一套，别混用"
M_NODE_BAD="✗ 不认识 '%s'"
M_NODE_NO_BREW="⚠ 没有 brew，跳过安装 %s —— 请自行装好对应工具"
M_NODE_PKG_INSTALL="安装 %s..."
M_NODE_PKG_SKIP="%s 已装，跳过"
M_NODE_PKG_OK="✓ %s 已装"
M_NODE_PKG_FAIL="⚠ %s 装失败，请稍后手动 brew install"
M_NODE_NVM_HINT="💡 nvm 若还没装：brew install nvm，或按 https://github.com/nvm-sh/nvm 装到 ~/.nvm"
M_NODE_VFOX_HINT="💡 vfox 装好后还要：vfox add nodejs && vfox install nodejs@latest && vfox use nodejs@latest"
M_NODE_WRITE_FAIL="✗ 写 node.sh 失败（检查 config/node/ 是否完整）"
M_NODE_DONE="✓ 已切换到 %s"
M_NODE_REOPEN="新开一个 tab（或 source ~/.zshrc）后生效"
M_NODE_ZSHRC_HINT="💡 你的 ~/.zshrc 还没 source node.sh —— 把 Node 那一段换成模板里的两行，或重跑 ./scripts/install.sh"

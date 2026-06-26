#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

write_default_gitignore_if_missing() {
	local dest="$1"
	[[ -f "$dest/.gitignore" ]] && return 0
	cat >"$dest/.gitignore" <<'EOF'
# 系统杂项
.DS_Store
Thumbs.db
desktop.ini

# 本地密钥与环境变量（勿提交）
.env
.env.*
*.pem
*.key
id_rsa
id_ed25519

# 编辑器
.idea/
.vscode/
*.swp
*.swo
*~

# Obsidian：窗口布局易冲突；要整库同步 .obsidian 可删下两行
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# 废纸篓目录（若启用）
.trash/

# 非文本附件（默认不入库；要提交图片/PDF 等可删除本段）
*.png
*.jpg
*.jpeg
*.gif
*.webp
*.bmp
*.ico
*.pdf
*.mp4
*.mov
*.mkv
*.zip
*.7z
*.rar
*.gz
*.tar
*.dmg
*.woff
*.woff2
*.ttf
*.otf
*.eot
*.doc
*.docx
*.xls
*.xlsx
*.ppt
*.pptx
EOF
}

V="${1:-${HOME}/.openclaw/workspace/obsidian-git-vault}"
mkdir -p "$V"
if ! require_git_repo "$V"; then
	git -C "$V" init
fi
write_default_gitignore_if_missing "$V"
printf '%s\n' "$(cd "$V" && pwd)"

#!/bin/bash
# ============================================================
# 主题旧名 → 新名（向后兼容）
#
# 色板键已改成英文名，但用户机器上的 ~/.config/hekouwang-terminal/theme、
# scene.env、auto.conf、workspace 记录可能还留着旧名。所有入口脚本先过这一层，
# 避免升级后 doctor 报 "主题文件不存在"、scene 退回默认。
#
# 新代码不要再用旧名；这张表只负责迁移。
# ⚠️ 与 config/themes/palettes/__init__.py 的 ALIASES 保持同步。
# ============================================================
hkw_resolve_theme() {
  case "${1:-}" in
    v2-mihei)       printf 'ember' ;;
    v1-keji)        printf 'voltage' ;;
    v2-mibai)       printf 'parchment' ;;
    v3-caijing-bai) printf 'ledger' ;;
    *)              printf '%s' "${1:-}" ;;
  esac
}

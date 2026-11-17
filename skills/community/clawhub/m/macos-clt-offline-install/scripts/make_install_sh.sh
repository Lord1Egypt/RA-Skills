#!/bin/bash
# 生成本地一键安装脚本（由 WorkBuddy 调用；安装本身需要用户密码，须由用户自行运行）
# 用法: make_install_sh.sh <pkg目录> <输出脚本路径>
set -euo pipefail

PKG_DIR="${1:?用法: make_install_sh.sh <pkg目录> <输出脚本路径>}"
OUT="${2:?缺少输出脚本路径}"

MAIN_PKG="CLTools_Executables.pkg"
SDK_PKGS=(CLTools_macOSLMOS_SDK.pkg CLTools_macOSNMOS_SDK.pkg CLTools_SwiftBackDeploy.pkg)

[ -f "$PKG_DIR/$MAIN_PKG" ] || { echo "错误: $PKG_DIR 下找不到 $MAIN_PKG"; exit 1; }

cat > "$OUT" <<EOF
#!/bin/bash
# Xcode Command Line Tools 离线安装脚本（安装包来自苹果官方 CDN，已验签）
set -euo pipefail
DIR="\$(cd "\$(dirname "\$0")" && pwd)"

echo "==> 校验 Apple 官方签名..."
for p in "$MAIN_PKG" ${SDK_PKGS[*]}; do
  [ -f "\$DIR/\$p" ] && pkgutil --check-signature "\$DIR/\$p" | grep -q "signed" || { echo "签名校验失败: \$p"; exit 1; }
done

echo "==> 安装主包 (需要输入开机密码)..."
sudo installer -pkg "\$DIR/$MAIN_PKG" -target /

echo "==> 安装 SDK 支持包..."
EOF

for p in "${SDK_PKGS[@]}"; do
  [ -f "$PKG_DIR/$p" ] && echo "sudo installer -pkg \"\$DIR/$p\" -target / || echo \"跳过 \$p\"" >> "$OUT"
done

cat >> "$OUT" <<EOF

sudo xcode-select --switch /Library/Developer/CommandLineTools 2>/dev/null || true

echo "==> 验证..."
xcode-select -p
git --version
echo "✅ 安装完成！git 已可用。"
EOF

chmod +x "$OUT"
echo "已生成: $OUT"

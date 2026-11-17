#!/usr/bin/env bash
# sign.sh — 把未签名的 .shortcut 签成可导入 iPhone 的签名件
#
# 用法：
#   ./scripts/sign.sh 输入.shortcut 输出.shortcut
#   ./scripts/sign.sh 输入.shortcut 输出.shortcut --check    # 额外反解校验动作数
#   ./scripts/sign.sh --verify-only 已签名.shortcut          # 只验签
#
# 环境变量（可选）：
#   SHORTCUT_SIGN      签名器路径，默认 <技能根>/bin/shortcut-sign
#   SHORTCUT_KEY       私钥，默认 <技能根>/certs/key.bin
#   SHORTCUT_AUTH      auth 数据，默认 <技能根>/certs/auth.plist
#   SHORTCUT_SIGN_LIB  libplist 所在目录（系统已装可不管）
#   SC_CERT_DIR        证书目录，默认 <技能根>/certs
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CERT_DIR="${SC_CERT_DIR:-$ROOT/certs}"
SIGN="${SHORTCUT_SIGN:-$ROOT/bin/shortcut-sign}"
KEY="${SHORTCUT_KEY:-$CERT_DIR/key.bin}"
AUTH="${SHORTCUT_AUTH:-$CERT_DIR/auth.plist}"
LIB="${SHORTCUT_SIGN_LIB:-}"
CHECK=0
VERIFY_ONLY=0

usage() { sed -n '4,7p' "$0" | sed 's/^# \{0,1\}//' >&2; }

ARGS=()
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    --verify-only) VERIFY_ONLY=1 ;;
    -h|--help) sed -n '4,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) ARGS+=("$a") ;;
  esac
done

ENVV=(env)
[ -n "$LIB" ] && ENVV+=(LD_LIBRARY_PATH="$LIB")

# shortcut-sign verify 有两个坑，这层封装就是为它们存在的：
#   1) 验签失败也返回 0，只能看输出文本
#   2) 喂未签名文件会直接段错误（139），无任何输出
verify_one() {
  local f="$1" log rc magic
  magic="$(head -c 4 "$f" 2>/dev/null || true)"
  if [ "$magic" != "AEA1" ]; then
    echo "    ✗ 不是签名件（文件头 ${magic:-空}）—— 未签名文件 iOS 会拒绝导入" >&2
    return 5
  fi
  log="$(mktemp)"
  if "${ENVV[@]}" "$SIGN" verify -i "$f" >"$log" 2>&1; then rc=0; else rc=$?; fi
  if [ "$rc" -ge 128 ]; then
    echo "    ✗ 签名器解不开这个文件（退出码 $rc）" >&2
    rm -f "$log"; return 5
  fi
  if grep -qi "Verification Failed\|verification failed" "$log"; then
    if grep -qi "self-signed" "$log"; then
      echo "    ✓ 签名结构完整（签名证书 → 自建 CA，2 张）"
      echo "      本机未信任这张根证书属预期；手机装好描述文件并开完全信任后即可导入"
      rm -f "$log"; return 0
    fi
    echo "    ✗ 验签失败：" >&2; sed 's/^/      /' "$log" >&2
    rm -f "$log"; return 5
  fi
  echo "    ✓ 证书链校验通过"
  rm -f "$log"
}

if [ "$VERIFY_ONLY" = 1 ]; then
  [ "${#ARGS[@]}" -eq 1 ] || { usage; exit 2; }
  [ -f "$SIGN" ] || { echo "✗ 找不到签名器：$SIGN" >&2; exit 3; }
  [ -f "${ARGS[0]}" ] || { echo "✗ 文件不存在：${ARGS[0]}" >&2; exit 3; }
  echo "==> 验签：$(basename "${ARGS[0]}")"
  verify_one "${ARGS[0]}"
  exit 0
fi

[ "${#ARGS[@]}" -eq 2 ] || { usage; exit 2; }
IN="${ARGS[0]}"; OUT="${ARGS[1]}"

[ -f "$SIGN" ] || { echo "✗ 找不到签名器：$SIGN" >&2; exit 3; }
[ -f "$KEY" ]  || { echo "✗ 找不到私钥，先跑 scripts/gen-certs.sh" >&2; exit 3; }
[ -f "$AUTH" ] || { echo "✗ 找不到 auth.plist，先跑 scripts/gen-certs.sh" >&2; exit 3; }
[ -f "$IN" ]   || { echo "✗ 输入文件不存在：$IN" >&2; exit 3; }

# 输出目录自动创建
mkdir -p "$(dirname "$OUT")"

echo "==> 签名：$(basename "$IN") → $(basename "$OUT")"
"${ENVV[@]}" "$SIGN" sign -i "$IN" -o "$OUT" -k "$KEY" -a "$AUTH"

[ -s "$OUT" ] || { echo "✗ 签名失败：输出为空" >&2; exit 4; }

echo "==> 验签"
verify_one "$OUT" || exit $?

if [ "$CHECK" = 1 ]; then
  echo "==> 反解校验（签名前后动作数必须一致）"
  TMP="$(mktemp -d)"
  "${ENVV[@]}" "$SIGN" extract -i "$OUT" -o "$TMP/back.shortcut" >/dev/null 2>&1 || {
    echo "    ✗ 反解失败"; rm -rf "$TMP"; exit 6; }
  python3 - "$IN" "$TMP/back.shortcut" <<'PY'
import sys, plistlib
def n(p):
    d = plistlib.load(open(p, "rb"))
    return len(d.get("WFWorkflowActions", []))
a, b = n(sys.argv[1]), n(sys.argv[2])
print(f"    原 {a} 个动作 / 反解 {b} 个动作")
if a != b:
    raise SystemExit("    ✗ 动作数不一致，签名过程丢了动作")
print("    ✓ 一致")
PY
  rm -rf "$TMP"
fi

echo "==> 完成：$OUT（$(stat -c%s "$OUT") 字节）"

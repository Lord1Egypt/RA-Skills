#!/usr/bin/env bash
# gen-certs.sh — 生成一套专属的快捷指令自签证书（CA + 签名证书 + 私钥 + auth.plist + mobileconfig）
#
# 用法：
#   ./scripts/gen-certs.sh                 # 输出到 ./certs/
#   ./scripts/gen-certs.sh --cn "我的CA"   # 自定义 CA 名称
#   ./scripts/gen-certs.sh --force         # 覆盖已有证书
#
# 产物（certs/）：
#   ca.key        CA 私钥（保密）
#   ca.crt/ca.der CA 证书（ca.der 用于装进 iPhone）
#   sign.key      签名私钥（PEM）
#   sign.crt      签名证书（含 Apple OID 1.2.840.113635.100.18.1）
#   key.bin       X9.63 格式私钥（97 字节：04||X||Y||K），shortcut-sign 只认这个
#   auth.plist    签名身份数据（二进制 plist，SigningCertificateChain=[签名证书,CA]）
#   ca.mobileconfig  iPhone 安装用的描述文件（内含根证书）
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CERT_DIR="${CERT_DIR:-$ROOT/certs}"
CN="Shortcut Local CA"
ORG="ShortcutSelfSign"
DAYS=3650
FORCE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --cn) CN="$2"; shift 2 ;;
    --org) ORG="$2"; shift 2 ;;
    --days) DAYS="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

die() { echo "✗ $*" >&2; exit 1; }
log() { echo "==> $*"; }

command -v openssl >/dev/null || die "缺 openssl"
command -v python3 >/dev/null || die "缺 python3"

if [ -f "$CERT_DIR/auth.plist" ] && [ "$FORCE" != 1 ]; then
  die "certs/ 已有证书。重生成请加 --force（旧证书作废，手机上要重新装）"
fi

mkdir -p "$CERT_DIR"
chmod 700 "$CERT_DIR"

log "1/6 生成 CA（$CN，有效期 $DAYS 天）"
openssl ecparam -name prime256v1 -genkey -noout -out "$CERT_DIR/ca.key" 2>/dev/null
chmod 600 "$CERT_DIR/ca.key"
openssl req -new -x509 -key "$CERT_DIR/ca.key" -out "$CERT_DIR/ca.crt" -days "$DAYS" \
  -utf8 -subj "/O=$ORG/CN=$CN" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" 2>/dev/null
openssl x509 -in "$CERT_DIR/ca.crt" -outform DER -out "$CERT_DIR/ca.der"

log "2/6 生成签名证书（含 Apple 专用 OID 1.2.840.113635.100.18.1）"
cat > "$CERT_DIR/ext.cnf" <<'EXT'
1.2.840.113635.100.18.1=ASN1:UTF8String:ShortcutSigning
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature
extendedKeyUsage=codeSigning
EXT
openssl ecparam -name prime256v1 -genkey -noout -out "$CERT_DIR/sign.key" 2>/dev/null
chmod 600 "$CERT_DIR/sign.key"
openssl req -new -key "$CERT_DIR/sign.key" -out "$CERT_DIR/sign.csr" -utf8 -subj "/O=$ORG/CN=$CN Signing" 2>/dev/null
openssl x509 -req -in "$CERT_DIR/sign.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial -out "$CERT_DIR/sign.crt" -days "$DAYS" -extfile "$CERT_DIR/ext.cnf" 2>/dev/null
openssl x509 -in "$CERT_DIR/sign.crt" -outform DER -out "$CERT_DIR/sign.der"

log "3/6 生成 key.bin（X9.63：04||X||Y||K，97 字节）"
openssl ec -in "$CERT_DIR/sign.key" -pubout -outform DER -out "$CERT_DIR/sign.pub.der" 2>/dev/null
python3 - "$CERT_DIR" <<'PY'
import sys, pathlib
d = pathlib.Path(sys.argv[1])
pub = (d / "sign.pub.der").read_bytes()
# SPKI 里公钥点是 BIT STRING：03 42 00 04 || X(32) || Y(32)
i = pub.rfind(b"\x03\x42\x00\x04")
if i < 0:
    raise SystemExit("找不到公钥点，openssl 输出格式异常")
point = pub[i + 3: i + 3 + 65]          # 04||X||Y
assert point[0] == 4 and len(point) == 65, "公钥点格式异常"
priv = (d / "sign.key").read_bytes().decode()
import re
# 从 PEM 里取私钥标量：用 openssl 转成文本再解析，避免依赖第三方库
import subprocess
hexk = subprocess.run(["openssl", "ec", "-in", str(d / "sign.key"), "-text", "-noout"],
                      capture_output=True, text=True, check=True).stdout
m = re.search(r"priv:\s*((?:[0-9a-f]{2}:?\s*)+)", hexk)
if not m:
    raise SystemExit("解析私钥标量失败")
k = bytes.fromhex(re.sub(r"[^0-9a-f]", "", m.group(1)))
if len(k) < 32:
    k = k.rjust(32, b"\x00")
(d / "key.bin").write_bytes(point + k[-32:])
(d / "sign.pub.der").unlink()
print(f"   key.bin = {len(point + k[-32:])} 字节")
PY
chmod 600 "$CERT_DIR/key.bin"

log "4/6 生成 auth.plist（证书链）"
python3 - "$CERT_DIR" <<'PY'
import sys, pathlib, plistlib
d = pathlib.Path(sys.argv[1])
chain = [(d / "sign.der").read_bytes(), (d / "ca.der").read_bytes()]
plistlib.dump({"SigningCertificateChain": chain}, open(d / "auth.plist", "wb"), fmt=plistlib.FMT_BINARY)
print("   auth.plist 写入，链长 2（签名证书 + CA）")
PY
chmod 600 "$CERT_DIR/auth.plist"

log "5/6 生成 ca.mobileconfig（iPhone 安装用）"
python3 - "$CERT_DIR" "$ORG" "$CN" <<'PY'
import sys, pathlib, plistlib, uuid
d, org, cn = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
ca = (d / "ca.der").read_bytes()
payload = {
    "PayloadType": "com.apple.security.root",
    "PayloadVersion": 1,
    "PayloadIdentifier": "local.shortcut.ca",
    "PayloadUUID": str(uuid.uuid4()).upper(),
    "PayloadDisplayName": f"{cn}（快捷指令自签根证书）",
    "PayloadDescription": "安装后需到 设置→通用→关于本机→证书信任设置 开启完全信任",
    "PayloadCertificateFileName": "ca.der",
    "PayloadContent": ca,
}
profile = {
    "PayloadType": "Configuration",
    "PayloadVersion": 1,
    "PayloadIdentifier": "local.shortcut.profile",
    "PayloadUUID": str(uuid.uuid4()).upper(),
    "PayloadOrganization": org,
    "PayloadDisplayName": f"{cn} 根证书",
    "PayloadDescription": "快捷指令自签链路所需根证书",
    "PayloadContent": [payload],
}
plistlib.dump(profile, open(d / "ca.mobileconfig", "wb"), fmt=plistlib.FMT_XML)
print("   ca.mobileconfig 写入")
PY

log "6/6 自检"
openssl x509 -in "$CERT_DIR/sign.crt" -noout -text | grep -q "1.2.840.113635.100.18.1" \
  || die "签名证书缺少 Apple OID"
[ "$(stat -c%s "$CERT_DIR/key.bin")" -eq 97 ] || die "key.bin 不是 97 字节"
echo
echo "  CA：$(openssl x509 -in "$CERT_DIR/ca.crt" -noout -nameopt utf8 -subject | sed 's/subject=//')"
echo "  OID：已含 1.2.840.113635.100.18.1"
echo "  私钥：key.bin（97 字节，X9.63）"
echo
echo "下一步：把 $CERT_DIR/ca.mobileconfig 发到 iPhone，Safari 打开 → 安装 →"
echo "        设置→通用→关于本机→证书信任设置→对本 CA 开启完全信任"

#!/usr/bin/env bash
# Download the versioned site zip and replace skill files in place.
# GET /api/skill/latest is authoritative. This script does not consult ClawHub.
# ClawHub may lag. Do not conclude the installed skill is current from ClawHub alone.
# This process is curl and python only. It does not start an agent.
# It does not read or write auth storage or credentials.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"

fail() {
  printf 'LobsterMatch self-update: %s\n' "$1" >&2
  exit 1
}

command -v python3 >/dev/null 2>&1 || fail "python3 is required to verify the package"
command -v curl >/dev/null 2>&1 || fail "curl is required"

BASE="${LOBSTERMATCH_BASE_URL:-https://lobstermatch.com}"
BASE="${BASE%/}"
case "$BASE" in
  https://lobstermatch.com|http://127.0.0.1:*|http://localhost:*) ;;
  *) fail "base URL must be https://lobstermatch.com" ;;
esac

VERSION="$(sed -n 's/^version:[[:space:]]*v\{0,1\}\([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\).*/\1/p' "$SKILL_DIR/SKILL.md" | head -n 1)"
[ -n "$VERSION" ] || VERSION="1.0.39"
USER_AGENT="LobsterMatch-Skill/${VERSION} (+https://lobstermatch.com/connect.md)"

meta="$(mktemp)"
archive="$(mktemp)"
extract="$(mktemp -d "${TMPDIR:-/tmp}/lobstermatch-self-update.XXXXXXXX")"
cleanup() {
  rm -f -- "$meta" "$archive" "$archive.url" || true
  # Remove only the temp extract directory this process created.
  python3 - "$extract" <<'PY' || true
import os, shutil, sys
from pathlib import Path
raw = sys.argv[1] if len(sys.argv) > 1 else ""
if not raw:
    raise SystemExit(0)
target = Path(raw).resolve()
roots = []
for key in ("TMPDIR", "TEMP", "TMP"):
    value = os.environ.get(key)
    if value:
        roots.append(Path(value).resolve())
roots.extend([Path("/tmp").resolve(), Path("/var/tmp").resolve()])
if not target.is_dir() or not target.name.startswith("lobstermatch-self-update."):
    raise SystemExit(0)
for root in roots:
    try:
        target.relative_to(root)
    except ValueError:
        continue
    if target != root:
        shutil.rmtree(target)
    break
PY
}
trap cleanup EXIT

curl --fail --silent --show-error --max-time 30 --retry 0 \
  -A "$USER_AGENT" \
  -o "$meta" \
  "$BASE/api/skill/latest" || fail "could not read /api/skill/latest"

python3 - "$meta" "$archive" "$BASE" <<'PY'
import json, sys, urllib.parse
from pathlib import Path
meta_path, archive_path, base = sys.argv[1:4]
meta = json.loads(Path(meta_path).read_text())
version = str(meta.get("version") or "").strip()
digest = str(meta.get("sha256") or "").strip().lower()
zip_url = str(meta.get("zipUrl") or "").strip()
if not version or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
    raise SystemExit("latest skill description is missing a version or sha256")
if "clawhub" in zip_url.lower():
    raise SystemExit("refusing a ClawHub URL; the site zip is authoritative")
allowed = urllib.parse.urlparse(base)
target = urllib.parse.urlparse(zip_url)
if target.scheme not in {"https", "http"} or target.hostname != allowed.hostname:
    raise SystemExit("zip URL host is not the LobsterMatch site")
expected = f"/downloads/lobstermatch-{version}.zip"
if target.path != expected:
    raise SystemExit("zip URL must be the versioned site package " + expected)
Path(archive_path + ".url").write_text(zip_url)
PY

zip_url="$(cat "$archive.url")"
rm -f "$archive.url"
curl --fail --silent --show-error --max-time 60 --retry 0 \
  -A "$USER_AGENT" \
  -L \
  -o "$archive" \
  "$zip_url" || fail "could not download the skill package"

python3 - "$meta" "$archive" "$extract" "$SKILL_DIR" <<'PY'
import hashlib, json, os, sys, zipfile
from pathlib import Path
meta = json.loads(Path(sys.argv[1]).read_text())
archive = Path(sys.argv[2])
extract = Path(sys.argv[3])
skill_dir = Path(sys.argv[4]).resolve()
digest = str(meta.get("sha256") or "").strip().lower()
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != digest:
    raise SystemExit("skill package checksum does not match /api/skill/latest")
prefix = "skills/lobstermatch-onboarding/"
with zipfile.ZipFile(archive) as package:
    for info in package.infolist():
        name = info.filename.replace("\\", "/")
        if not name or name.endswith("/"):
            continue
        if name.startswith("/") or ".." in Path(name).parts:
            raise SystemExit("skill package contains an unsafe path")
        if not name.startswith(prefix):
            continue
        relative = name[len(prefix):]
        parts = Path(relative).parts
        def blocked(part):
            lower = part.lower()
            return lower in {"", ".", ".."} or lower.startswith(".") or "auth" in lower or "credential" in lower or ".lobstermatch" in lower
        if not relative or any(blocked(part) for part in parts):
            continue
        target = (skill_dir / relative).resolve()
        if skill_dir not in target.parents and target != skill_dir:
            raise SystemExit("skill package tried to write outside the skill directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        data = package.read(info)
        target.write_bytes(data)
        mode = 0o755 if relative.endswith(".sh") else 0o644
        os.chmod(target, mode)
print(meta.get("version") or "")
PY

flag="$(lm_auth_root)/update-available"
if [ -f "$flag" ]; then
  rm -f "$flag"
fi
printf 'LobsterMatch self-update: skill files updated\n'

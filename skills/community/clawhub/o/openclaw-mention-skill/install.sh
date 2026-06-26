#!/bin/bash
# OpenClaw WhatsApp @Mention Skill - Installer
# Patches deliver-reply and login to enable model-agnostic @mentions
#
# WHAT THIS SCRIPT DOES:
#   1. Backs up deliver-reply-*.js and login-*.js (timestamped .bak files)
#   2. Patches deliver-reply to intercept outgoing messages and convert @mentions
#   3. Patches login's reply() to accept {text, mentions} objects
#   4. Creates LID_CACHE.json if not exists (empty cache, no credentials)
#   5. Copies mention-guide.md to AI memory directory
#   6. Restarts OpenClaw service
#
# This script does NOT access, read, or modify any credential/auth files.
# Run 'bash uninstall.sh' to restore original files from backup.
set -e

echo "╔══════════════════════════════════════════╗"
echo "║  OpenClaw @Mention Skill Installer v10   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Find OpenClaw dist directory
DIST="/usr/lib/node_modules/openclaw/dist"
if [ ! -d "$DIST" ]; then
  echo "✗ OpenClaw not found at $DIST"
  echo "  Set OPENCLAW_DIST env to override."
  exit 1
fi

DELIVER=$(ls "$DIST"/deliver-reply-*.js 2>/dev/null | head -1)
LOGIN=$(ls "$DIST"/login-*.js 2>/dev/null | head -1)
WORKSPACE="/home/openclaw/.openclaw/workspace"
MEMORY="$WORKSPACE/memory"
LID_CACHE="$WORKSPACE/LID_CACHE.json"

if [ -z "$DELIVER" ] || [ -z "$LOGIN" ]; then
  echo "✗ Could not find deliver-reply or login files in $DIST"
  exit 1
fi

echo "Found:"
echo "  deliver-reply: $(basename $DELIVER)"
echo "  login: $(basename $LOGIN)"
echo ""

# Backup
TS=$(date -u +%Y%m%dT%H%M%S)
cp "$DELIVER" "${DELIVER}.bak.mention.${TS}"
cp "$LOGIN" "${LOGIN}.bak.mention.${TS}"
echo "✓ Backups created"

# ═══════════════════════════════════════════
# PATCH 1: Fix const chunk → let chunk
# ═══════════════════════════════════════════
python3 << 'PYEOF'
import sys

path = sys.argv[1] if len(sys.argv) > 1 else None
if not path:
    import glob
    files = glob.glob("/usr/lib/node_modules/openclaw/dist/deliver-reply-*.js")
    path = files[0] if files else None

with open(path) as f:
    c = f.read()

old = "for (const [index, chunk] of textChunks.entries()) {"
new = "for (const [index, _origChunk] of textChunks.entries()) {\n\t\t\tlet chunk = _origChunk;"

if "_origChunk" in c:
    print("  const→let: already fixed")
elif old in c:
    c = c.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(c)
    print("✓ Fixed const chunk → let chunk")
else:
    print("⚠ const chunk pattern not found (may be a different OpenClaw version)")
PYEOF

# ═══════════════════════════════════════════
# PATCH 2: deliver-reply - V10 mention patch
# ═══════════════════════════════════════════
python3 << 'PYEOF'
import sys, glob

files = glob.glob("/usr/lib/node_modules/openclaw/dist/deliver-reply-*.js")
path = files[0]

with open(path) as f:
    c = f.read()

if "_LID_PATCH_V10" in c:
    print("  deliver-reply: V10 already applied")
    sys.exit(0)

# Remove any previous patch version
for marker in ["_LID_PATCH_V9", "_LID_PATCH_V8", "_LID_PATCH_V7", "_LID_PATCH_V6", "_LID_PATCH_V5"]:
    if marker in c:
        old_start = c.index("// " + marker)
        search_from = c.index("} else {", old_start)
        end_line = 'await sendWithRetry(() => msg.reply(chunk), "text");'
        end_pos = c.index(end_line, search_from)
        end = end_pos + len(end_line)
        while end < len(c) and c[end] in '\n\t\r ':
            end += 1
        if end < len(c) and c[end] == '}':
            end += 1
        c = c[:old_start] + 'await sendWithRetry(() => msg.reply(chunk), "text");' + c[end:]
        print(f"  Removed old {marker}")
        break

# Find the insertion point: before msg.reply(chunk) in text-only branch
target = '\t\t\tawait sendWithRetry(() => msg.reply(chunk), "text");'
if target not in c:
    # Try with different indentation
    target = 'await sendWithRetry(() => msg.reply(chunk), "text");'

if target not in c:
    print("✗ Could not find msg.reply(chunk) insertion point")
    sys.exit(1)

patch = """// _LID_PATCH_V10 - model-agnostic @mention (text=@LID, mentions=[LID@lid])
					let _v10m = [];
					try {
						const { readFileSync: _r } = await import("node:fs");
						const _c = JSON.parse(_r("/home/openclaw/.openclaw/workspace/LID_CACHE.json", "utf8"));
						const _g = msg.from || "";
						const _gm = _c[_g] || {};
						const _nm = _c._names || {};
						const _al = _c._aliases || {};
						const _gl = new Set(Object.keys(_gm));
						const _p2l = {};
						for (const [l, p] of Object.entries(_gm)) { if (p) _p2l[p] = l; }
						const _n2l = {};
						for (const [l, n] of Object.entries(_nm)) {
							if (n && (_gl.size === 0 || _gl.has(l))) _n2l[n.toLowerCase()] = l;
						}
						for (const [a, l] of Object.entries(_al)) {
							if ((_gl.size === 0 || _gl.has(l)) && !_n2l[a]) _n2l[a] = l;
						}
						const _ms = new Set();
						const _sn = Object.entries(_n2l).sort((a, b) => b[0].length - a[0].length);
						for (const [name, lid] of _sn) {
							const s = "@" + name;
							if (chunk.toLowerCase().includes(s)) {
								let r = "", p = 0, src = chunk;
								while (true) {
									const f = src.toLowerCase().indexOf(s, p);
									if (f === -1) { r += src.slice(p); break; }
									r += src.slice(p, f) + "@" + lid;
									p = f + s.length;
									_ms.add(lid + "@lid");
								}
								chunk = r;
							}
						}
						const _pr = /@(\\d{8,15})/g;
						let _pm;
						const _pf = [];
						while ((_pm = _pr.exec(chunk)) !== null) { _pf.push({ n: _pm[1], i: _pm.index }); }
						for (let i = _pf.length - 1; i >= 0; i--) {
							const { n: num, i: idx } = _pf[i];
							const lid = _p2l[num];
							if (lid && !_ms.has(lid + "@lid")) {
								chunk = chunk.slice(0, idx + 1) + lid + chunk.slice(idx + 1 + num.length);
								_ms.add(lid + "@lid");
							}
						}
						const _lr = /@(\\d{10,20})/g;
						let _lm;
						while ((_lm = _lr.exec(chunk)) !== null) { _ms.add(_lm[1] + "@lid"); }
						_v10m = [..._ms];
					} catch(_e) {}
					if (_v10m.length > 0) {
						await sendWithRetry(() => msg.reply({ text: chunk, mentions: _v10m }), "text");
					} else {
						await sendWithRetry(() => msg.reply(chunk), "text");
					}"""

# Replace the first occurrence only (text-only branch, not media fallback)
idx = c.index(target)
c = c[:idx] + patch + c[idx + len(target):]

with open(path, "w") as f:
    f.write(c)
print("✓ deliver-reply: V10 patch applied")
PYEOF

# ═══════════════════════════════════════════
# PATCH 3: login - reply() accepts {text, mentions}
# ═══════════════════════════════════════════
python3 << 'PYEOF'
import glob

files = glob.glob("/usr/lib/node_modules/openclaw/dist/login-*.js")
path = files[0]

with open(path) as f:
    c = f.read()

if "textOrPayload" in c:
    print("  login reply(): already patched")
else:
    # Try standard format
    old = "const reply = async (text) => {\n\t\t\tawait sendTrackedMessage(chatJid, { text });\n\t\t};"
    new = "const reply = async (textOrPayload) => {\n\t\t\tconst payload = typeof textOrPayload === 'string' ? { text: textOrPayload } : textOrPayload;\n\t\t\tawait sendTrackedMessage(chatJid, payload);\n\t\t};"

    if old in c:
        c = c.replace(old, new, 1)
        with open(path, "w") as f:
            f.write(c)
        print("✓ login: reply() patched to accept {text, mentions}")
    else:
        # Check if there's an older mention patch in reply()
        import re
        pattern = r"const reply = async \(text\) => \{[^}]+sendTrackedMessage[^}]+\};"
        match = re.search(pattern, c)
        if match:
            c = c.replace(match.group(0), new, 1)
            with open(path, "w") as f:
                f.write(c)
            print("✓ login: reply() replaced (had old inline mention logic)")
        else:
            print("⚠ login: reply() format not recognized - manual patch may be needed")
PYEOF

# ═══════════════════════════════════════════
# Initialize LID_CACHE if not exists
# ═══════════════════════════════════════════
if [ ! -f "$LID_CACHE" ]; then
  echo '{"_names":{},"_aliases":{}}' > "$LID_CACHE"
  chown openclaw:openclaw "$LID_CACHE"
  echo "✓ Created empty LID_CACHE.json"
else
  echo "  LID_CACHE.json already exists"
fi

# ═══════════════════════════════════════════
# Install mention-guide.md to AI memory
# ═══════════════════════════════════════════
mkdir -p "$MEMORY"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/mention-guide.md" ]; then
  cp "$SCRIPT_DIR/mention-guide.md" "$MEMORY/mention-guide.md"
  chown openclaw:openclaw "$MEMORY/mention-guide.md"
  echo "✓ Installed mention-guide.md to AI memory"
else
  echo "  mention-guide.md not found in repo, skipping"
fi

# ═══════════════════════════════════════════
# Install add-member.js utility
# ═══════════════════════════════════════════
if [ -f "$SCRIPT_DIR/add-member.js" ]; then
  cp "$SCRIPT_DIR/add-member.js" "$WORKSPACE/scripts/add-member.js" 2>/dev/null || \
  cp "$SCRIPT_DIR/add-member.js" "$WORKSPACE/add-member.js"
  echo "✓ Installed add-member.js"
fi

# ═══════════════════════════════════════════
# Restart OpenClaw
# ═══════════════════════════════════════════
echo ""
if systemctl is-active openclaw >/dev/null 2>&1; then
  systemctl restart openclaw
  sleep 3
  if systemctl is-active openclaw >/dev/null 2>&1; then
    echo "✓ OpenClaw restarted successfully"
  else
    echo "✗ OpenClaw failed to start! Check: journalctl -u openclaw --no-pager -n 20"
    exit 1
  fi
else
  echo "⚠ OpenClaw service not running. Start it manually."
fi

echo ""
echo "══════════════════════════════════════════"
echo "  @Mention Skill installed successfully!"
echo "  Re-run this script after OpenClaw updates."
echo "══════════════════════════════════════════"

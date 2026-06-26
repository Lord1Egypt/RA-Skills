# Troubleshooting: memory-lancedb

## Error: Cannot find module '@lancedb/lancedb'

**Cause**: Main package not installed in openclaw root.

**Fix**:
```bash
cd /usr/local/lib/node_modules/openclaw
npm install @lancedb/lancedb
```

---

## Error: Cannot find module '@lancedb/lancedb-darwin-x64' (on arm64 Mac)

**Cause**: arm64 native binding not installed + native.js falls through x64 → break before reaching arm64.

**Fix**: Install arm64 binding + run patch script:
```bash
cd /usr/local/lib/node_modules/openclaw/extensions/memory-lancedb
npm install @lancedb/lancedb-darwin-arm64
python3 ~/.openclaw/workspace/skills/memory-lancedb-setup/references/patch_native.py
openclaw gateway restart
```

---

## Error: npm EBADPLATFORM (x64 package on arm64)

**Cause**: Trying to install the wrong architecture package.

**Fix**: Use `@lancedb/lancedb-darwin-arm64` on Apple Silicon, not `x64`.

---

## Error: @lancedb/lancedb-darwin-universal 404

**Cause**: This package does not exist on npm.

**Fix**: Use architecture-specific package + patch script instead.

---

## memory_store returns "Invalid memory ID format"

**Cause**: `memory_forget` only accepts full UUIDs, not short IDs from `memory_recall`.

**Fix**: To effectively "delete", overwrite with updated content via `memory_store` using the same topic. The old low-relevance entry will be deprioritized in future recalls.

---

## Memories not showing up in relevant-memories

**Cause**: Similarity threshold not met, or autoRecall not enabled.

**Check**: Run `memory_recall` manually with a relevant query to confirm entries exist.

---

## Plugin shows "disabled" in `openclaw plugins list`

**Cause**: Plugin not enabled in config.

**Fix**:
```bash
openclaw config set plugins.entries.memory-lancedb.enabled true
openclaw gateway restart
```

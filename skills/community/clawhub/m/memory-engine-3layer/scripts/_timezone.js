/**
 * _timezone.js — Shared timezone resolver for memory-engine scripts
 * 
 * Resolution order:
 * 1. --timezone CLI arg (if passed by caller)
 * 2. OPENCLAW_TZ env var
 * 3. openclaw.json → agents.defaults.userTimezone (auto-detected from workspace path)
 * 4. TZ env var
 * 5. /etc/timezone file
 * 6. System timezone from `date +%Z` heuristic
 * 7. 'UTC' fallback
 */
const fs = require('fs'), path = require('path');

let _cachedTz = null;

function resolveTimezone(workspace) {
  if (_cachedTz) return _cachedTz;

  // 1. OPENCLAW_TZ env (highest priority explicit override)
  if (process.env.OPENCLAW_TZ) { _cachedTz = process.env.OPENCLAW_TZ; return _cachedTz; }

  // 2. Auto-detect from openclaw.json (same logic OpenClaw uses)
  if (workspace) {
    const candidates = [
      path.join(workspace, '..', 'openclaw.json'),           // ~/.openclaw/workspace → ~/.openclaw/openclaw.json
      path.join(workspace, '..', '..', 'openclaw.json'),     // nested workspace
      path.join(process.env.HOME || '', '.openclaw', 'openclaw.json')  // absolute fallback
    ];
    for (const cfgPath of candidates) {
      try {
        if (fs.existsSync(cfgPath)) {
          const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
          const tz = cfg?.agents?.defaults?.userTimezone;
          if (tz && isValidTimezone(tz)) { _cachedTz = tz; return _cachedTz; }
        }
      } catch (_) { /* ignore parse errors */ }
    }
  }

  // 3. TZ env var
  if (process.env.TZ && isValidTimezone(process.env.TZ)) { _cachedTz = process.env.TZ; return _cachedTz; }

  // 4. /etc/timezone
  try {
    const tz = fs.readFileSync('/etc/timezone', 'utf8').trim();
    if (tz && isValidTimezone(tz)) { _cachedTz = tz; return _cachedTz; }
  } catch (_) {}

  // 5. /etc/localtime symlink (common on RHEL/CentOS)
  try {
    const link = fs.readlinkSync('/etc/localtime');
    const m = link.match(/zoneinfo\/(.+)$/);
    if (m && isValidTimezone(m[1])) { _cachedTz = m[1]; return _cachedTz; }
  } catch (_) {}

  // 6. UTC fallback
  _cachedTz = 'UTC';
  return _cachedTz;
}

function isValidTimezone(tz) {
  try {
    Intl.DateTimeFormat(undefined, { timeZone: tz });
    return true;
  } catch (_) { return false; }
}

function getToday(workspace) {
  const tz = resolveTimezone(workspace);
  try { return new Date().toLocaleDateString('en-CA', { timeZone: tz }); }
  catch { return new Date().toISOString().slice(0, 10); }
}

function getTime(workspace) {
  const tz = resolveTimezone(workspace);
  try { return new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', timeZone: tz }); }
  catch { return new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }); }
}

module.exports = { resolveTimezone, getToday, getTime, isValidTimezone };

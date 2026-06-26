// Device ID — local-only anonymous identifier.
// No hardware fingerprinting. Generates a random ID and persists it locally.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const DEVICE_ID_FILE = path.resolve(__dirname, '..', '..', '.device_id');
let _cachedId = null;
const ID_RE = /^[a-f0-9]{32}$/;

function getDeviceId() {
  if (_cachedId) return _cachedId;
  if (process.env.EVOLVER_DEVICE_ID) {
    const envId = String(process.env.EVOLVER_DEVICE_ID).trim().toLowerCase();
    if (ID_RE.test(envId)) { _cachedId = envId; return _cachedId; }
  }
  try {
    if (fs.existsSync(DEVICE_ID_FILE)) {
      const id = fs.readFileSync(DEVICE_ID_FILE, 'utf8').trim();
      if (id && ID_RE.test(id)) { _cachedId = id; return _cachedId; }
    }
  } catch {}
  const id = crypto.randomBytes(16).toString('hex');
  try { fs.writeFileSync(DEVICE_ID_FILE, id, { mode: 0o600 }); } catch {}
  _cachedId = id;
  return _cachedId;
}

function isContainer() { return false; }

module.exports = { getDeviceId, isContainer };

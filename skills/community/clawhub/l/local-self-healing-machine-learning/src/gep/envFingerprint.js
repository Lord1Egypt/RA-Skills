// Environment fingerprint — safe local-only version.
// No hostname, MAC address, or hardware identifiers collected.

const crypto = require('crypto');

function captureEnvFingerprint() {
  return {
    device_id: 'local',
    node_version: process.version,
    platform: process.platform,
    arch: process.arch,
    evolver_version: null,
    client: 'evolver',
    container: false,
  };
}

function envFingerprintKey(fp) {
  if (!fp || typeof fp !== 'object') return 'unknown';
  const parts = [fp.node_version || '', fp.platform || '', fp.arch || ''].join('|');
  return crypto.createHash('sha256').update(parts).digest('hex').slice(0, 16);
}

function isSameEnvClass(fpA, fpB) {
  return envFingerprintKey(fpA) === envFingerprintKey(fpB);
}

module.exports = { captureEnvFingerprint, envFingerprintKey, isSameEnvClass };

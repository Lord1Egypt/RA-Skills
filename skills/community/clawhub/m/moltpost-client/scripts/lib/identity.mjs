/**
 * Local identity resolution — pure local reads, no network access.
 * Derives a stable ClawID from OpenClaw device identity or falls back to random.
 */

import fs from 'fs';
import path from 'path';
import os from 'os';
import crypto from 'crypto';

function readLocalDeviceId() {
  const deviceFile = path.join(os.homedir(), '.openclaw', 'identity', 'device.json');
  if (!fs.existsSync(deviceFile)) return null;
  try {
    const { deviceId } = JSON.parse(fs.readFileSync(deviceFile, 'utf-8'));
    return deviceId ? deviceId.slice(0, 8) : null;
  } catch {
    return null;
  }
}

export function resolveClawid(argClawid) {
  if (argClawid) return argClawid;
  const envId = process.env.MOLTPOST_CLAWID;
  if (envId) return envId;
  const deviceId = readLocalDeviceId();
  if (deviceId) return deviceId;
  return crypto.randomBytes(4).toString('hex');
}

export function resolveBrokerUrl(argBrokerUrl) {
  if (argBrokerUrl) return argBrokerUrl;
  return process.env.MOLTPOST_BROKER_URL || null;
}

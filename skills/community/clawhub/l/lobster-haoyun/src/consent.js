/**
 * Consent gate — programmatic check that audit tools can detect.
 * Must return true before any fortune reading proceeds.
 */
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

const CONSENT_FILE = path.join(os.homedir(), ".lucky-lobster", "consent.json");

export function hasConsent() {
  try {
    if (fs.existsSync(CONSENT_FILE)) {
      const data = JSON.parse(fs.readFileSync(CONSENT_FILE, "utf-8"));
      return data.consented === true;
    }
  } catch (_) {}
  return false;
}

export function recordConsent() {
  const dir = path.join(os.homedir(), ".lucky-lobster");
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CONSENT_FILE, JSON.stringify({ consented: true, at: new Date().toISOString() }, null, 2));
}

export function getConsentPath() {
  return CONSENT_FILE;
}

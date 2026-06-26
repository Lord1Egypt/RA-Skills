import fs from 'node:fs/promises';
import path from 'node:path';
import { ASSETS_DIR } from '../constants.js';
import { pathExists } from '../utils.js';

export async function readBundledManifest() {
  const manifestPath = path.join(ASSETS_DIR, 'skill.json');
  const content = await fs.readFile(manifestPath, 'utf8');
  return JSON.parse(content);
}

export async function readInstalledManifest(installDir) {
  const manifestPath = path.join(installDir, 'skill.json');
  if (!(await pathExists(manifestPath))) {
    return null;
  }
  const content = await fs.readFile(manifestPath, 'utf8');
  return JSON.parse(content);
}

export async function validateManifest(manifest) {
  const required = ['id', 'name', 'version', 'runtime', 'entry'];
  const missing = required.filter((key) => !manifest[key]);
  if (missing.length > 0) {
    throw new Error(`Invalid manifest, missing fields: ${missing.join(', ')}`);
  }
  return true;
}

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export interface PluginTrustEntry {
  path: string;
  sha256: string;
  issuer?: string;
  source?: string;
}

export interface PluginTrustPolicy {
  version: number;
  enforce: boolean;
  entries: PluginTrustEntry[];
}

export function computeSha256Hex(filePath: string): string {
  const data = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

export function verifyPluginTrustChain(
  rootDir: string,
  extensions: string[],
  policy: PluginTrustPolicy,
): string[] {
  const errors: string[] = [];

  if (!policy || typeof policy !== 'object') {
    return ['plugin trust policy missing or invalid'];
  }
  if (!Array.isArray(policy.entries)) {
    return ['plugin trust policy entries must be an array'];
  }

  const table = new Map(policy.entries.map((entry) => [entry.path, entry]));

  for (const extension of extensions) {
    const trustEntry = table.get(extension);
    if (!trustEntry) {
      errors.push(`extension ${extension} is not present in plugin trust policy`);
      continue;
    }

    const filePath = path.join(rootDir, extension);
    if (!fs.existsSync(filePath)) {
      errors.push(`extension ${extension} is listed in trust policy but file is missing`);
      continue;
    }

    if (trustEntry.sha256) {
      const actualSha = computeSha256Hex(filePath);
      if (actualSha !== trustEntry.sha256) {
        errors.push(`extension ${extension} sha256 mismatch: expected ${trustEntry.sha256}, got ${actualSha}`);
      }
    }
  }

  return errors;
}

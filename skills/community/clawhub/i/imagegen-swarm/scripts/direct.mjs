import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// Node puts the path you typed in argv[1] and the resolved file in import.meta.url.
// A symlink (the script itself, or a parent like the Claude skills directory) makes
// those strings differ, so a plain URL compare skips main and the process exits quietly.
// realpath both sides. Missing or unreadable argv[1] means this module was imported.
export function isInvokedDirectly(moduleUrl, entry = process.argv[1]) {
  if (!entry || !moduleUrl) return false;
  try {
    return realpathSync(entry) === realpathSync(fileURLToPath(moduleUrl));
  } catch {
    return false;
  }
}

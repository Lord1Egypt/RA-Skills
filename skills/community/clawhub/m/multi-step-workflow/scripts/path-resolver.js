import { tmpdir } from 'os';
import { join } from 'path';
import { existsSync, mkdirSync } from 'fs';
import { createHash } from 'crypto';

/**
 * Generates a consistent project-specific temp directory path
 * based on the current working directory's hash.
 * This ensures different projects don't collide in /tmp.
 * 
 * SECURITY: The directory is created with 0700 permissions (owner-only).
 */
export function getTempDir() {
  const cwd = process.cwd();
  const hash = createHash('md5').update(cwd).digest('hex').substring(0, 8);
  const tempDir = join(tmpdir(), `openclaw-workflow-${hash}`);
  
  if (!existsSync(tempDir)) {
    // Mode 0o700 ensures ONLY the current user can read/write/cd into this dir.
    mkdirSync(tempDir, { recursive: true, mode: 0o700 });
  }
  
  return tempDir;
}

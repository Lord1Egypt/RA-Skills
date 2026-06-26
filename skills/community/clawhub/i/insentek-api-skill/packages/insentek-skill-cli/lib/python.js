import { spawnSync } from 'node:child_process';

export function findPythonCommand() {
  const candidates = process.platform === 'win32'
    ? ['python', 'py', 'python3']
    : ['python3', 'python'];

  for (const candidate of candidates) {
    const result = spawnSync(candidate, ['--version'], {
      encoding: 'utf8',
      stdio: 'pipe',
      shell: process.platform === 'win32',
    });
    if (result.status === 0) {
      return { command: candidate, version: result.stdout.trim() || result.stderr.trim() };
    }
  }
  return null;
}

import path from 'node:path';
import { fileURLToPath } from 'node:url';

export function getCurrentModuleDir(stackIndex = 1): string {
  const originalPrepare = Error.prepareStackTrace;
  try {
    Error.prepareStackTrace = (_, stack) => stack;
    const stack = new Error().stack as unknown as NodeJS.CallSite[];
    const fileName = stack?.[stackIndex]?.getFileName();
    if (!fileName) return process.cwd();
    const normalizedPath = fileName.startsWith('file:') ? fileURLToPath(fileName) : fileName;
    return path.dirname(normalizedPath);
  } finally {
    Error.prepareStackTrace = originalPrepare;
  }
}

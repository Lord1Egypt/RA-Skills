import { stringify } from 'yaml';

function omitUndefined(obj: unknown): unknown {
  if (Array.isArray(obj)) return obj.map(omitUndefined);
  if (obj !== null && typeof obj === 'object') {
    const result: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(obj as Record<string, unknown>)) {
      if (v !== undefined && v !== null) result[k] = omitUndefined(v);
    }
    return result;
  }
  return obj;
}

export function print(data: unknown): void {
  process.stdout.write(stringify(omitUndefined(data), { lineWidth: 0 }));
}

export function err(msg: string): void {
  process.stderr.write(`error: ${msg}\n`);
}

export function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

export function nowISO(): string {
  return new Date().toISOString();
}

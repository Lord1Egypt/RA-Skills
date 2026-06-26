export class FeishuMessageError extends Error {
  constructor(code, message, details = undefined) {
    super(message);
    this.name = 'FeishuMessageError';
    this.code = code;
    this.details = details;
  }
}

export function messageError(code, message, details) {
  return new FeishuMessageError(code, message, details);
}

function redactSecrets(value, seen = new WeakSet()) {
  if (value == null) return value;
  if (Array.isArray(value)) return value.map((item) => redactSecrets(item, seen));
  if (typeof value === 'object') {
    if (seen.has(value)) return '[Circular]';
    seen.add(value);
    const out = {};
    for (const [key, raw] of Object.entries(value)) {
      const lower = String(key).toLowerCase();
      if (
        lower.includes('token') ||
        lower.includes('authorization') ||
        lower.includes('secret') ||
        lower.includes('password') ||
        lower.includes('cookie')
      ) {
        out[key] = '[REDACTED]';
      } else {
        out[key] = redactSecrets(raw, seen);
      }
    }
    return out;
  }
  return value;
}

export function normalizeError(error) {
  if (error instanceof FeishuMessageError) {
    if (error?.details && typeof error.details === 'object') {
      error.details = redactSecrets(error.details);
    }
    return error;
  }

  const raw = {
    message: error?.message,
    name: error?.name,
    code: error?.code,
    status: error?.status,
    response: error?.response,
    data: error?.data,
    body: error?.body,
    stack: error?.stack,
  };

  return new FeishuMessageError('INTERNAL_ERROR', error?.message || 'Unknown Feishu message error', redactSecrets({
    cause: String(error?.stack || error),
    raw,
  }));
}

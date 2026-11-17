export class SkillError extends Error {
  constructor(code, message, options = {}) {
    super(message, options.cause ? { cause: options.cause } : undefined);
    this.name = 'SkillError';
    this.code = code;
    this.retryable = Boolean(options.retryable);
    this.details = options.details ?? null;
    this.httpStatus = options.httpStatus ?? null;
  }
}

export class ApiError extends SkillError {
  constructor(code, message, options = {}) {
    super(code, message, options);
    this.name = 'ApiError';
  }
}

export function normalizeError(error) {
  if (error instanceof SkillError) {
    return {
      code: error.code,
      message: error.message,
      retryable: error.retryable,
      details: error.details
    };
  }

  return {
    code: 'UNEXPECTED_ERROR',
    message: error instanceof Error ? error.message : String(error),
    retryable: false,
    details: null
  };
}

export function assert(condition, code, message, details = null) {
  if (!condition) {
    throw new SkillError(code, message, { details });
  }
}


// Machine-readable error model shared by all providers.
// Every error carries: code, message, provider, retryable.

export const CODES = {
  INVALID_ARGUMENT: 'LFD_INVALID_ARGUMENT',
  GEOCODE_ERROR: 'LFD_GEOCODE_ERROR',
  UNSUPPORTED_LOCATION: 'LFD_UNSUPPORTED_LOCATION',
  NOT_FOUND: 'LFD_NOT_FOUND',
  RATE_LIMITED: 'LFD_RATE_LIMITED',
  BLOCKED: 'LFD_BLOCKED',
  UPSTREAM_ERROR: 'LFD_UPSTREAM_ERROR',
  NETWORK_ERROR: 'LFD_NETWORK_ERROR',
  CART_ERROR: 'LFD_CART_ERROR',
  PARSE_ERROR: 'LFD_PARSE_ERROR',
};

export class CliError extends Error {
  /**
   * @param {string} code one of CODES
   * @param {string} message human-readable, must not contain secrets or full addresses
   * @param {{provider?: string, retryable?: boolean, details?: object, exitCode?: number}} [opts]
   */
  constructor(code, message, opts = {}) {
    super(message);
    this.name = 'CliError';
    this.code = code;
    this.provider = opts.provider ?? null;
    this.retryable = opts.retryable ?? false;
    this.details = opts.details ?? undefined;
    this.exitCode = opts.exitCode ?? 1;
  }

  toEnvelopeError() {
    const err = {
      code: this.code,
      message: this.message,
      provider: this.provider,
      retryable: this.retryable,
    };
    if (this.details !== undefined) err.details = this.details;
    return err;
  }
}

export function invalidArgument(message) {
  return new CliError(CODES.INVALID_ARGUMENT, message, { exitCode: 2 });
}

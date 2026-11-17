import { redactString } from "./redact.mjs";

export class CorrespondenceError extends Error {
  constructor({ status, code, message, idempotencyKey, retryable = false } = {}) {
    super(redactString(message || "correspondence request failed"));
    this.name = "CorrespondenceError";
    this.status = status ?? null;
    this.code = code || "invalid_input";
    this.idempotencyKey = idempotencyKey ?? null;
    this.retryable = retryable === true;
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        status: this.status,
        idempotencyKey: this.idempotencyKey,
        retryable: this.retryable,
      },
    };
  }
}

export class ClientValidationError extends CorrespondenceError {
  constructor({ status = 400, code = "invalid_input", message, idempotencyKey } = {}) {
    super({ status, code, message, idempotencyKey, retryable: false });
    this.name = "ClientValidationError";
  }
}

export class UnknownOutcomeError extends CorrespondenceError {
  constructor({ idempotencyKey, operation, message } = {}) {
    super({
      status: null,
      code: "unknown_outcome",
      message:
        message ||
        "Mutation result is unknown. Reconcile with the same Idempotency-Key. Do not mint a new key.",
      idempotencyKey,
      retryable: false,
    });
    this.name = "UnknownOutcomeError";
    this.operation = operation ?? null;
  }
}

export function fallbackCode(status) {
  switch (status) {
    case 400:
      return "invalid_input";
    case 401:
      return "invalid_grant";
    case 403:
      return "insufficient_scope";
    case 404:
      return "not_found";
    case 409:
      return "conflict";
    case 413:
      return "body_limit";
    case 429:
      return "rate_limited";
    case 503:
      return "unavailable";
    default:
      return "unavailable";
  }
}

export function fallbackMessage(status) {
  switch (status) {
    case 400:
      return "invalid input";
    case 401:
      return "invalid grant";
    case 403:
      return "insufficient scope";
    case 404:
      return "project is not accessible";
    case 409:
      return "conflict";
    case 413:
      return "request body exceeds 32 KiB";
    case 429:
      return "rate limited";
    case 503:
      return "service unavailable";
    default:
      return "request failed";
  }
}

/**
 * token-errors.js — Token-specific error classes
 *
 * These augment (not replace) the existing NormalizationError from errors.js.
 * All token errors include the ref name but NEVER the resolved value.
 */

"use strict";

class TokenError extends Error {
  constructor(message) {
    super(message);
    this.name = "TokenError";
  }
}

class TokenFormatError extends TokenError {
  constructor(message = "Invalid token format — expected mrconf:v1:...") {
    super(message);
    this.name = "TokenFormatError";
  }
}

class TokenDecodeError extends TokenError {
  constructor(message = "Token is corrupt — could not decode") {
    super(message);
    this.name = "TokenDecodeError";
  }
}

class TokenJSONError extends TokenError {
  constructor(message = "Token is corrupt — invalid JSON") {
    super(message);
    this.name = "TokenJSONError";
  }
}

class TokenVersionError extends TokenError {
  constructor(found, supported = [1]) {
    super(`Token version not supported — found v${found}, supported: v${supported.join(", v")}`);
    this.name = "TokenVersionError";
    this.found = found;
    this.supported = supported;
  }
}

class CredentialMissingError extends TokenError {
  constructor(ref) {
    // ref is the placeholder name (e.g., "${CEREBRAS_API_KEY}"), NOT the value
    super(`${ref}: credential not found. Set ${ref} in env or add to pass.`);
    this.name = "CredentialMissingError";
    this.ref = ref;
  }
}

module.exports = {
  TokenError,
  TokenFormatError,
  TokenDecodeError,
  TokenJSONError,
  TokenVersionError,
  CredentialMissingError,
};

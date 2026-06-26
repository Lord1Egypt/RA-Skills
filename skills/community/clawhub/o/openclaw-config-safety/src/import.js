/**
 * import.js — Config token import
 *
 * importConfigToken(token) → config object
 *
 * Security: NEVER logs or exposes resolved credential values.
 */

"use strict";

const { decode } = require("./base64url.js");
const {
  TokenFormatError,
  TokenDecodeError,
  TokenJSONError,
  TokenVersionError,
} = require("./token-errors.js");
const { extractAndResolveRefs, substituteRefs } = require("./resolve-refs.js");

/**
 * Import a config token.
 *
 * @param {string} token — "mrconf:v1:..." string
 * @returns {{ config: object, credentialRefs: string[] }}
 * @throws {TokenError} on any parsing/validation/credential failure
 */
function importConfigToken(token) {
  if (typeof token !== "string") throw new TokenFormatError();

  // 1. Parse prefix and extract version
  let version;
  if (token.startsWith("mrconf:v1:")) {
    version = 1;
  } else if (token.startsWith("mrconf:v")) {
    // Prefix matches "mrconf:v<something>:" but version not supported
    throw new TokenVersionError("unknown", [1]);
  } else {
    throw new TokenFormatError();
  }

  // 2. Decode base64url — validate charset first (Buffer.from doesn't throw on invalid chars)
  const encoded = token.slice(`mrconf:v${version}:`.length);
  if (!/^[A-Za-z0-9_-]*$/.test(encoded)) {
    throw new TokenDecodeError();
  }
  let payloadJson;
  try {
    payloadJson = decode(encoded).toString("utf8");
  } catch {
    throw new TokenDecodeError();
  }

  // 3. Parse JSON
  let payload;
  try {
    payload = JSON.parse(payloadJson);
  } catch {
    throw new TokenJSONError();
  }

  // 4. Validate schema
  _validatePayload(payload);

  // 5. Resolve credential references
  const { refs, credMap } = extractAndResolveRefs(payload.config);

  // 6. Substitute ${REF} with resolved values
  const config = substituteRefs(payload.config, credMap);

  return { config, credentialRefs: refs };
}

/**
 * Validate token payload structure.
 * @param {object} payload
 * @throws {TokenVersionError|TokenJSONError}
 */
function _validatePayload(payload) {
  if (typeof payload !== "object" || payload === null || Array.isArray(payload)) {
    throw new TokenJSONError("Token payload must be a plain object");
  }

  // Version check
  if (payload.version !== 1) {
    throw new TokenVersionError(payload.version, [1]);
  }

  // ExportedAt
  if (typeof payload.exportedAt !== "string") {
    throw new TokenJSONError("Token payload missing exportedAt");
  }
  const date = new Date(payload.exportedAt);
  if (isNaN(date.getTime())) {
    throw new TokenJSONError("Token payload has invalid exportedAt");
  }

  // Config must be object
  if (typeof payload.config !== "object" || payload.config === null) {
    throw new TokenJSONError("Token payload missing config");
  }

  // credentialRefs must be array of strings
  if (!Array.isArray(payload.credentialRefs)) {
    throw new TokenJSONError("Token payload missing credentialRefs array");
  }
  for (const ref of payload.credentialRefs) {
    if (typeof ref !== "string") {
      throw new TokenJSONError("credentialRefs must contain only strings");
    }
  }
}

module.exports = { importConfigToken };

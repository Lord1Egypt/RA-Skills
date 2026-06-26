/**
 * base64url.js — URL-safe base64 encode/decode
 *
 * Profile: Base64url (RFC 4648 §5)
 * - "+" → "-", "/" → "_"
 * - No padding ("=")
 */

"use strict";

/**
 * @param {Buffer|string} input
 * @returns {string} base64url-encoded string (no padding)
 */
function encode(input) {
  const buf = Buffer.isBuffer(input) ? input : Buffer.from(input, "utf8");
  return buf
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, ""); // strip padding
}

/**
 * @param {string} input — base64url-encoded string (no padding)
 * @returns {Buffer}
 * @throws {Error} if input is not valid base64url
 */
function decode(input) {
  if (typeof input !== "string") {
    throw new Error("base64url.decode: input must be a string");
  }
  // Restore padding and standard base64 chars
  let str = input.replace(/-/g, "+").replace(/_/g, "/");
  const padLen = (4 - (str.length % 4)) % 4;
  str += "=".repeat(padLen);
  const buf = Buffer.from(str, "base64");
  if (!buf) throw new Error("base64url.decode: invalid encoding");
  return buf;
}

module.exports = { encode, decode };

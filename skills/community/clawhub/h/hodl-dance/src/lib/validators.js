/**
 * Simple Ethereum address validation utilities.
 * Used across CLI commands to give early, clear errors to users and agents.
 */

/**
 * Checks if a string looks like a valid Ethereum address.
 * Accepts 0x + 40 hex characters (case insensitive).
 * Does NOT perform EIP-55 checksum validation (kept simple for v1.3.0).
 */
function isValidAddress(address) {
  if (typeof address !== 'string') return false;
  return /^0x[a-fA-F0-9]{40}$/.test(address);
}

/**
 * Throws a consistent INVALID_ARG error if the address is invalid.
 * Used by commands to fail fast with a good message.
 */
function requireValidAddress(address, paramName = 'address') {
  if (!isValidAddress(address)) {
    const { err } = require('./output');
    err(
      `Invalid ${paramName}. Expected a 42-character Ethereum address (0x + 40 hex chars).`,
      'INVALID_ARG'
    );
  }
}

module.exports = {
  isValidAddress,
  requireValidAddress,
};
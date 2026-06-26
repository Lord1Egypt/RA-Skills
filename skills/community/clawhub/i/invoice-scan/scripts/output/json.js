/**
 * JSON Output Formatter
 */

function toJSON(invoice, pretty = true) {
  return pretty ? JSON.stringify(invoice, null, 2) : JSON.stringify(invoice);
}

module.exports = { toJSON };

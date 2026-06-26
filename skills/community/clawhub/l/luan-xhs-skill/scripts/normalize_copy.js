function normalizeTitle(raw) {
  return String(raw || '')
    .replace(/\r\n/g, '\n')
    .replace(/\\r\\n/g, '\n')
    .replace(/\\n/g, '\n')
    .replace(/\s*\n+\s*/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function normalizeBody(raw) {
  return String(raw || '')
    .replace(/\r\n/g, '\n')
    .replace(/\\r\\n/g, '\n')
    .replace(/\\n/g, '\n')
    .replace(/\\t/g, '\t')
    .replace(/\u2028|\u2029/g, '\n')
    .trim();
}

module.exports = {
  normalizeTitle,
  normalizeBody,
};

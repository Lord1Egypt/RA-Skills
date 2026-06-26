'use strict';

function fmtCredits(n) {
  const c = Number(n) || 0;
  return `${c.toLocaleString()} credits ($${(c / 100).toFixed(2)})`;
}

function fmtNoShow(rate) {
  if (rate == null) return 'Off';
  return `${Number(rate)}%`;
}

module.exports = { fmtCredits, fmtNoShow };

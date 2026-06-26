// Hub Search — disabled in local-only build.
// All searches return miss. Evolution runs entirely from local assets.

function hubSearch() { return Promise.resolve({ hit: false, reason: 'local_only_build' }); }
function scoreHubResult() { return 0; }
function pickBestMatch() { return null; }
function getReuseMode() { return 'reference'; }
function getMinReuseScore() { return 0.72; }
function getHubUrl() { return ''; }

module.exports = { hubSearch, scoreHubResult, pickBestMatch, getReuseMode, getMinReuseScore, getHubUrl };

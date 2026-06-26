/**
 * Node Connection Doctor - 辅助函数
 */

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function escapeMarkdown(text) {
  return text.replace(/([_*\[\]()`~>#+=|{}.!\\-])/g, '\\$1');
}

function generateReportHTML(results) {
  const colors = {
    ok: '#4CAF50',
    error: '#F44336',
    warn: '#FF9800'
  };

  let html = `<html><head><style>
    body { font-family: monospace; padding: 20px; }
    .step { margin: 10px 0; padding: 10px; border-radius: 4px; }
    .ok { background-color: ${colors.ok}20; border-left: 4px solid ${colors.ok}; }
    .error { background-color: ${colors.error}20; border-left: 4px solid ${colors.error}; }
    .warn { background-color: ${colors.warn}20; border-left: 4px solid ${colors.warn}; }
    h2 { color: #333; }
  </style></head><body>`;
  html += `<h2>🔍 Node Connection Diagnosis Report</h2>`;
  html += `<p>Generated: ${new Date().toISOString()}</p>`;

  results.forEach(r => {
    const statusClass = r.ok ? 'ok' : 'error';
    html += `<div class="step ${statusClass}">`;
    html += `<strong>${r.step}</strong><br>`;
    if (r.ok) {
      html += `✅ Status: Healthy`;
      if (r.output) html += `<pre>${escapeMarkdown(r.output)}</pre>`;
    } else {
      html += `❌ Error: ${escapeMarkdown(r.error)}`;
      if (r.details) html += `<pre>${escapeMarkdown(r.details)}</pre>`;
    }
    html += `</div>`;
  });

  html += '<h3>💡 Recommendations</h3><ul>';
  if (!results[0]?.ok) {
    html += '<li>Restart gateway: <code>openclaw gateway restart</code></li>';
    html += '<li>Check token: <code>openclaw config get gateway.auth.token</code></li>';
  }
  if (!results[1]?.ok) {
    html += '<li>Reset pairing: <code>openclaw node pair --reset</code></li>';
  }
  html += '</ul></body></html>';

  return html;
}

module.exports = {
  formatBytes,
  escapeMarkdown,
  generateReportHTML
};

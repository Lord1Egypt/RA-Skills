/**
 * MiniMax Web Search + Image Understanding via MCP Server
 * Usage:
 *   node minimax_websearch.js search "关键词"
 *   node minimax_websearch.js image "分析要求" "图片路径或URL"
 *
 * Required env vars:
 *   MINIMAX_API_KEY    - MiniMax API key (from MiniMax Token Plan)
 *   MINIMAX_PYTHON     - Path to Python with minimax-coding-plan-mcp installed
 *                        (default: E:\.uv-venv\Scripts\python.exe)
 *
 * Example openclaw.json config:
 *   { "env": { "MINIMAX_API_KEY": "...", "MINIMAX_PYTHON": "E:\\.uv-venv\\Scripts\\python.exe" } }
 */
const { execSync } = require('child_process');
const path = require('path');

const VENV_CERTIFI_CA = process.platform === 'win32'
  ? 'E:\\.uv-venv\\Lib\\site-packages\\certifi\\cacert.pem'
  : path.join(process.env.HOME || '/usr/local', '.uv-venv', 'lib', 'certifi', 'cacert.pem');

const apiKey = process.env.MINIMAX_API_KEY;
if (!apiKey) {
  console.error('Error: MINIMAX_API_KEY environment variable is not set.');
  console.error('Add it to openclaw.json: { "env": { "MINIMAX_API_KEY": "your-key" } }');
  process.exit(1);
}

const defaultPy = process.platform === 'win32'
  ? 'E:\\.uv-venv\\Scripts\\python.exe'
  : path.join(process.env.HOME || '/usr/local', '.uv-venv', 'bin', 'python');

const pythonExe = process.env.MINIMAX_PYTHON || defaultPy;
const apiHost = process.env.MINIMAX_API_HOST || 'https://api.minimaxi.com';

function runMCP(messages) {
  const input = messages.map(m => JSON.stringify(m)).join('\n') + '\n';
  const result = execSync(`"${pythonExe}" -m minimax_mcp.server`, {
    env: { ...process.env, MINIMAX_API_KEY: apiKey, MINIMAX_API_HOST: apiHost, FASTMCP_LOG_LEVEL: 'ERROR', REQUESTS_CA_BUNDLE: VENV_CERTIFI_CA },
    input,
    maxBuffer: 10 * 1024 * 1024,
    timeout: 60000,
    shell: true,
    windowsHide: true
  });
  const output = result.toString().trim();
  const lines = output.split('\n');
  const results = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || !trimmed.startsWith('{')) continue;
    try { results.push(JSON.parse(trimmed)); } catch {}
  }
  return results;
}

const cmd = process.argv[2];
const arg1 = process.argv[3];
const arg2 = process.argv[4];

if (cmd === 'search') {
  if (!arg1) {
    console.error('Usage: node minimax_websearch.js search "关键词"');
    process.exit(1);
  }
  const results = runMCP([
    { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'websearch', version: '1.0' } } },
    { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'web_search', arguments: { query: arg1 } } }
  ]);
  const sr = results.find(r => r.id === 3);
  if (!sr || sr.error) { console.error('Search error:', sr?.error || 'no response'); process.exit(1); }
  const data = sr.result;
  if (data.isError) { console.error('Tool error:', data.content?.[0]?.text || 'unknown'); process.exit(1); }
  try {
    const parsed = JSON.parse(data.content[0].text);
    const out = { query: arg1, count: parsed.organic?.length || 0, results: parsed.organic || [], related: parsed.related_searches || [] };
    console.log(JSON.stringify(out, null, 2));
  } catch { console.log(data.content[0].text); }

} else if (cmd === 'image') {
  if (!arg1 || !arg2) {
    console.error('Usage: node minimax_websearch.js image "分析要求" "图片路径或URL"');
    process.exit(1);
  }
  const results = runMCP([
    { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'websearch', version: '1.0' } } },
    { jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'understand_image', arguments: { prompt: arg1, image_source: arg2 } } }
  ]);
  const ir = results.find(r => r.id === 4);
  if (!ir || ir.error) { console.error('Image error:', ir?.error || 'no response'); process.exit(1); }
  const data = ir.result;
  if (data.isError) { console.error('Tool error:', data.content?.[0]?.text || 'unknown'); process.exit(1); }
  console.log(data.content[0].text);

} else if (cmd === 'tools') {
  const results = runMCP([
    { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'websearch', version: '1.0' } } },
    { jsonrpc: '2.0', id: 2, method: 'tools/list', params: {} }
  ]);
  const tr = results.find(r => r.id === 2 && r.result?.tools);
  if (!tr) { console.error('Could not get tools list'); process.exit(1); }
  console.log('Available tools:');
  tr.result.tools.forEach(t => console.log(' -', t.name, '-', t.description?.split('\n')[0] || ''));

} else {
  console.error('Usage:');
  console.error('  node minimax_websearch.js search "关键词"');
  console.error('  node minimax_websearch.js image "分析要求" "图片路径或URL"');
  console.error('  node minimax_websearch.js tools');
  process.exit(1);
}

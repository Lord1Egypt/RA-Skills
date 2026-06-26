/**
 * MiniMax Web Search via MCP Server
 * Usage: node minimax_websearch.js "搜索关键词"
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

// Path to certifi CA bundle (bundled with requests in .uv-venv)
const VENV_CERTIFI_CA = process.platform === 'win32'
  ? 'E:\\.uv-venv\\Lib\\site-packages\\certifi\\cacert.pem'
  : path.join(process.env.HOME || '/usr/local', '.uv-venv', 'lib', 'certifi', 'cacert.pem');

const query = process.argv[2];

if (!query) {
  console.error('Usage: node minimax_websearch.js "搜索关键词"');
  process.exit(1);
}

// API key (required)
const apiKey = process.env.MINIMAX_API_KEY;
if (!apiKey) {
  console.error('Error: MINIMAX_API_KEY environment variable is not set.');
  console.error('Add it to openclaw.json: { "env": { "MINIMAX_API_KEY": "your-key" } }');
  process.exit(1);
}

// Python interpreter (default to E:\.uv-venv on Windows)
const defaultPy = process.platform === 'win32'
  ? 'E:\\.uv-venv\\Scripts\\python.exe'
  : path.join(process.env.HOME || '/usr/local', '.uv-venv', 'bin', 'python');

const pythonExe = process.env.MINIMAX_PYTHON || defaultPy;
const apiHost = process.env.MINIMAX_API_HOST || 'https://api.minimaxi.com';

// Build the JSON-RPC messages
const initializeMsg = JSON.stringify({
  jsonrpc: '2.0', id: 1, method: 'initialize',
  params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'websearch', version: '1.0' } }
}) + '\n';

const searchMsg = JSON.stringify({
  jsonrpc: '2.0', id: 3, method: 'tools/call',
  params: { name: 'web_search', arguments: { query } }
}) + '\n';

const input = initializeMsg + searchMsg;

// Run server and communicate
// REQUESTS_CA_BUNDLE is needed because .uv-venv's ssl module doesn't auto-detect the system CA store
const result = execSync(`"${pythonExe}" -m minimax_mcp.server`, {
  env: { ...process.env, MINIMAX_API_KEY: apiKey, MINIMAX_API_HOST: apiHost, FASTMCP_LOG_LEVEL: 'ERROR', REQUESTS_CA_BUNDLE: VENV_CERTIFI_CA },
  input,
  maxBuffer: 10 * 1024 * 1024,
  timeout: 30000,
  shell: true,
  windowsHide: true
});

// Parse all JSON-RPC responses from stdout (ignore stderr warnings)
const output = result.toString().trim();
const lines = output.split('\n');

let searchResult = null;
for (const line of lines) {
  const trimmed = line.trim();
  if (!trimmed || !trimmed.startsWith('{')) continue;
  try {
    const parsed = JSON.parse(trimmed);
    if (parsed.id === 3) {
      searchResult = parsed;
      break;
    }
  } catch { /* skip non-JSON lines */ }
}

if (!searchResult) {
  console.error('No search result found. Server output:', output.substring(0, 500));
  process.exit(1);
}

if (searchResult.error) {
  console.error('Search error:', searchResult.error);
  process.exit(1);
}

const resultData = searchResult.result;
if (resultData.isError) {
  console.error('Tool error:', resultData.content?.[0]?.text || 'unknown');
  process.exit(1);
}

try {
  const searchData = JSON.parse(resultData.content[0].text);
  const out = {
    query,
    count: searchData.organic?.length || 0,
    results: searchData.organic || [],
    related: searchData.related_searches || []
  };
  console.log(JSON.stringify(out, null, 2));
} catch {
  console.log(resultData.content[0].text);
}

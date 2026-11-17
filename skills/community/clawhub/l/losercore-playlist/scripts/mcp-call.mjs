#!/usr/bin/env node
const methods = new Set(['tools/list', 'tools/call', 'resources/list', 'resources/read', 'prompts/list', 'prompts/get']);
const [method, raw = '{}'] = process.argv.slice(2);
try {
  if (!methods.has(method)) throw new Error('Use tools/list, tools/call, resources/list, resources/read, prompts/list or prompts/get.');
  const params = JSON.parse(raw);
  if (!params || typeof params !== 'object' || Array.isArray(params)) throw new Error('Params must be a JSON object.');
  const body = JSON.stringify({jsonrpc:'2.0',id:1,method,params});
  if (Buffer.byteLength(body) > 16384) throw new Error('Request exceeds the 16 KiB limit.');
  const response = await fetch('https://losercoreplaylist.com/mcp', {method:'POST', headers:{'Content-Type':'application/json', Accept:'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}, body, signal:AbortSignal.timeout(25000),redirect:'error'});
  if (!response.ok) throw new Error(`MCP HTTP ${response.status}`);
  if (!response.headers.get('content-type')?.includes('application/json')) throw new Error('Expected stateless JSON response.');
  const text = await response.text();
  if (Buffer.byteLength(text) > 1048576) throw new Error('Reply exceeds the 1 MiB limit.');
  const reply = JSON.parse(text);
  if (reply.error) throw new Error(`MCP error ${reply.error.code}: ${reply.error.message}`);
  if (reply.result?.isError) throw new Error('MCP tool returned an error result.');
  if (!reply.result) throw new Error('MCP result missing.');
  console.log(JSON.stringify(reply,null,2));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}

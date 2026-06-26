const assert = require('node:assert/strict');
const http = require('node:http');
const test = require('node:test');

const { createGrayMatterMcpServer } = require('../index.js');

async function listen(server) {
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  return `http://127.0.0.1:${address.port}`;
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : null;
}

function createFakeApi(status, payload) {
  return http.createServer(async (req, res) => {
    await readBody(req);
    res.writeHead(status, { 'content-type': 'application/json' });
    res.end(JSON.stringify(payload));
  });
}

async function postRpc(baseUrl, payload) {
  const response = await fetch(`${baseUrl}/mcp`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return response.json();
}

test('memory_query returns structured recovery for insufficient credits', async () => {
  const fakeApi = createFakeApi(402, { code: 'INSUFFICIENT_FUNDS', message: 'insufficient credits' });
  const apiBase = await listen(fakeApi);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const body = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'credit',
      method: 'tools/call',
      params: { name: 'memory_query', arguments: { query: 'hello' } }
    });

    const out = body.result.structuredContent;
    assert.equal(out.reason, 'insufficient_credits');
    assert.equal(out.blockedOperation, 'memory_query');
    assert.equal(out.retryable, true);
    assert.match(out.buyCreditsUrl, /^https:\/\//);
    assert.match(out.signupUrl, /^https:\/\//);
  } finally {
    server.close();
    fakeApi.close();
  }
});

test('memory_query returns auth recovery for 401', async () => {
  const fakeApi = createFakeApi(401, { message: 'token expired' });
  const apiBase = await listen(fakeApi);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const body = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'auth',
      method: 'tools/call',
      params: { name: 'memory_query', arguments: { query: 'hello' } }
    });

    const out = body.result.structuredContent;
    assert.equal(out.reason, 'missing_auth');
    assert.equal(out.retryable, true);
    assert.match(out.loginUrl, /\/auth\/login$/);
  } finally {
    server.close();
    fakeApi.close();
  }
});

test('memory_write returns read-only recovery for 403 write forbidden', async () => {
  const fakeApi = createFakeApi(403, { message: 'write forbidden for read-only token' });
  const apiBase = await listen(fakeApi);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const body = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'readonly',
      method: 'tools/call',
      params: { name: 'memory_write', arguments: { type: 'context', text: 'x' } }
    });

    const out = body.result.structuredContent;
    assert.equal(out.reason, 'read_only_auth');
    assert.equal(out.retryable, false);
  } finally {
    server.close();
    fakeApi.close();
  }
});

test('success path remains plain toolResult content shape', async () => {
  const fakeApi = createFakeApi(200, { results: [{ id: 'mem-1' }] });
  const apiBase = await listen(fakeApi);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const body = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'ok',
      method: 'tools/call',
      params: { name: 'memory_query', arguments: { query: 'ok' } }
    });

    assert.equal(body.result.structuredContent, undefined);
    assert.deepEqual(JSON.parse(body.result.content[0].text), { results: [{ id: 'mem-1' }] });
  } finally {
    server.close();
    fakeApi.close();
  }
});

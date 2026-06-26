const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const http = require('node:http');
const path = require('node:path');
const test = require('node:test');

const { createGrayMatterMcpServer } = require('../index.js');

async function listen(server) {
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  return `http://127.0.0.1:${address.port}`;
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : null;
}

function createFakeApi(handler) {
  const requests = [];
  const server = http.createServer(async (req, res) => {
    const body = await readBody(req);
    const record = {
      method: req.method,
      path: new URL(req.url, 'http://fake.local').pathname,
      query: new URL(req.url, 'http://fake.local').searchParams,
      headers: req.headers,
      body
    };
    requests.push(record);
    await handler(req, res, record);
  });
  return { server, requests };
}

async function postRpc(baseUrl, payload, headers = {}, path = '/') {
  const response = await fetch(`${baseUrl}${path}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      ...headers
    },
    body: JSON.stringify(payload)
  });
  return {
    status: response.status,
    body: await response.json()
  };
}

async function readSsePreamble(baseUrl) {
  return new Promise((resolve, reject) => {
    const req = http.get(`${baseUrl}/sse`, (res) => {
      let raw = '';
      res.on('data', (chunk) => {
        raw += chunk.toString('utf8');
        if (raw.includes('\n\n')) {
          req.destroy();
          resolve({ status: res.statusCode, body: raw });
        }
      });
    });
    req.on('error', (error) => {
      if (error.code !== 'ECONNRESET') {
        reject(error);
      }
    });
    req.setTimeout(2000, () => {
      req.destroy();
      reject(new Error('SSE preamble timed out'));
    });
  });
}

function readJsonLine(stream) {
  return new Promise((resolve, reject) => {
    let raw = '';
    const timer = setTimeout(() => {
      cleanup();
      reject(new Error('stdio response timed out'));
    }, 2000);

    function cleanup() {
      clearTimeout(timer);
      stream.off('data', onData);
      stream.off('error', onError);
    }

    function onError(error) {
      cleanup();
      reject(error);
    }

    function onData(chunk) {
      raw += chunk.toString('utf8');
      const newlineIndex = raw.indexOf('\n');
      if (newlineIndex === -1) {
        return;
      }

      const line = raw.slice(0, newlineIndex);
      cleanup();
      try {
        resolve(JSON.parse(line));
      } catch (error) {
        reject(new Error(`Invalid JSON line from stdio server: ${line}`));
      }
    }

    stream.on('data', onData);
    stream.on('error', onError);
  });
}

test('health reports server readiness without api-0 auth', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const response = await fetch(`${baseUrl}/health`);
    const body = await response.json();

    assert.equal(response.status, 200);
    assert.equal(body.ok, true);
    assert.equal(body.apiBase, 'https://api-0.example.test/v1');
    assert.ok(body.tools.includes('memory_write'));
    assert.ok(body.tools.includes('schema_summary'));
  } finally {
    server.close();
  }
});

test('stdio mode exposes the GrayMatter MCP tools for Codex plugin launch', async () => {
  const child = spawn(process.execPath, [path.join(__dirname, '..', 'index.js'), '--stdio'], {
    cwd: path.join(__dirname, '..'),
    env: {
      ...process.env,
      VALKYR_API_BASE: 'https://api-0.example.test/v1',
      VALKYR_AUTH_TOKEN: ['stdio', 'credential'].join('-')
    },
    stdio: ['pipe', 'pipe', 'pipe']
  });

  try {
    child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize' })}\n`);
    const init = await readJsonLine(child.stdout);
    assert.equal(init.id, 'init');
    assert.equal(init.result.serverInfo.name, 'graymatter');

    child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id: 'tools', method: 'tools/list' })}\n`);
    const listed = await readJsonLine(child.stdout);
    assert.deepEqual(
      listed.result.tools.map((tool) => tool.name),
      [
        'memory_write',
        'memory_read',
        'memory_query',
        'graph_get',
        'entity_list',
        'entity_get',
        'entity_create',
        'show_graymatter_overview',
        'schema_summary'
      ]
    );
  } finally {
    child.kill();
  }
});

test('initialize works through the paired message endpoint', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const response = await fetch(`${baseUrl}/message`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 'init-1',
        method: 'initialize'
      })
    });
    const body = await response.json();

    assert.equal(response.status, 200);
    assert.equal(body.id, 'init-1');
    assert.equal(body.result.serverInfo.name, 'graymatter');
    assert.deepEqual(body.result.capabilities, { tools: {}, resources: {} });
  } finally {
    server.close();
  }
});

test('initialize works through the Apps SDK /mcp endpoint', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'init-apps-sdk',
      method: 'initialize'
    }, {}, '/mcp');

    assert.equal(result.status, 200);
    assert.equal(result.body.id, 'init-apps-sdk');
    assert.equal(result.body.result.serverInfo.name, 'graymatter');
  } finally {
    server.close();
  }
});

test('sse announces the paired message endpoint', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const response = await readSsePreamble(baseUrl);

    assert.equal(response.status, 200);
    assert.match(response.body, /event: endpoint/);
    assert.match(response.body, /data: \/message/);
  } finally {
    server.close();
  }
});

test('tools/list exposes Apps SDK metadata required for review', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/list'
    });

    assert.equal(result.status, 200);

    for (const tool of result.body.result.tools) {
      assert.equal(typeof tool.title, 'string', `${tool.name} title`);
      assert.ok(tool.title.length > 0, `${tool.name} title`);
      assert.deepEqual(tool.securitySchemes, [
        { type: 'apiKey', in: 'header', name: 'X-Valkyr-Token' },
        { type: 'http', scheme: 'bearer' }
      ]);
      assert.deepEqual(tool._meta.securitySchemes, tool.securitySchemes);
      assert.equal(typeof tool._meta['openai/toolInvocation/invoking'], 'string', `${tool.name} invoking text`);
      assert.equal(typeof tool._meta['openai/toolInvocation/invoked'], 'string', `${tool.name} invoked text`);
      assert.equal(typeof tool.annotations.readOnlyHint, 'boolean', `${tool.name} readOnlyHint`);
      assert.equal(typeof tool.annotations.destructiveHint, 'boolean', `${tool.name} destructiveHint`);
      assert.equal(typeof tool.annotations.openWorldHint, 'boolean', `${tool.name} openWorldHint`);
    }

    const overview = result.body.result.tools.find((tool) => tool.name === 'show_graymatter_overview');
    assert.ok(overview, 'show_graymatter_overview is present');
    assert.equal(overview._meta.ui.resourceUri, 'ui://graymatter/overview.html');
    assert.equal(overview._meta['openai/outputTemplate'], 'ui://graymatter/overview.html');
  } finally {
    server.close();
  }
});

test('resources expose the GrayMatter Apps SDK overview widget', async () => {
  const server = createGrayMatterMcpServer({
    apiBase: 'https://api-0.example.test/v1',
    widgetDomain: 'https://graymatter.example.test'
  });
  const baseUrl = await listen(server);

  try {
    const listed = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'resources',
      method: 'resources/list'
    });

    assert.equal(listed.status, 200);
    assert.deepEqual(listed.body.result.resources, [
      {
        uri: 'ui://graymatter/overview.html',
        name: 'GrayMatter overview',
        title: 'GrayMatter overview',
        description: 'Overview card for GrayMatter durable memory and schema tools.',
        mimeType: 'text/html;profile=mcp-app'
      }
    ]);

    const read = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'resource',
      method: 'resources/read',
      params: { uri: 'ui://graymatter/overview.html' }
    });

    assert.equal(read.status, 200);
    assert.equal(read.body.result.contents.length, 1);
    assert.equal(read.body.result.contents[0].uri, 'ui://graymatter/overview.html');
    assert.equal(read.body.result.contents[0].mimeType, 'text/html;profile=mcp-app');
    assert.match(read.body.result.contents[0].text, /GrayMatter/);
    assert.deepEqual(read.body.result.contents[0]._meta.ui.csp.connectDomains, [
      'https://api-0.valkyrlabs.com'
    ]);
    assert.equal(read.body.result.contents[0]._meta.ui.domain, 'https://graymatter.example.test');
    assert.equal(read.body.result.contents[0]._meta['openai/widgetDomain'], 'https://graymatter.example.test');
  } finally {
    server.close();
  }
});

test('tools/list exposes the GrayMatter tool surface', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/list'
    });

    assert.equal(result.status, 200);
    assert.deepEqual(
      result.body.result.tools.map((tool) => tool.name),
      [
        'memory_write',
        'memory_read',
        'memory_query',
        'graph_get',
        'entity_list',
        'entity_get',
        'entity_create',
        'show_graymatter_overview',
        'schema_summary'
      ]
    );
  } finally {
    server.close();
  }
});

test('memory_read, memory_query, and graph_get route to api-0', async () => {
  const fakeApi = createFakeApi(async (_req, res, record) => {
    res.writeHead(200, { 'content-type': 'application/json' });
    if (record.path === '/v1/MemoryEntry/mem-42') {
      res.end(JSON.stringify({ id: 'mem-42', text: 'remembered' }));
      return;
    }
    if (record.path === '/v1/MemoryEntry/query') {
      assert.equal(record.method, 'POST');
      assert.equal(record.body.query, 'remember');
      res.end(JSON.stringify({ results: [{ id: 'mem-42' }] }));
      return;
    }
    if (record.path === '/v1/SwarmOps/graph') {
      res.end(JSON.stringify({ nodes: [], edges: [] }));
      return;
    }
    throw new Error(`Unexpected path ${record.path}`);
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const readResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'read',
      method: 'tools/call',
      params: { name: 'memory_read', arguments: { id: 'mem-42' } }
    });
    const queryResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'query',
      method: 'tools/call',
      params: { name: 'memory_query', arguments: { query: 'remember', limit: 5 } }
    });
    const graphResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'graph',
      method: 'tools/call',
      params: { name: 'graph_get', arguments: {} }
    });

    assert.deepEqual(JSON.parse(readResult.body.result.content[0].text), { id: 'mem-42', text: 'remembered' });
    assert.deepEqual(JSON.parse(queryResult.body.result.content[0].text), { results: [{ id: 'mem-42' }] });
    assert.deepEqual(JSON.parse(graphResult.body.result.content[0].text), { nodes: [], edges: [] });
    assert.equal(fakeApi.requests.length, 3);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('memory_write forwards per-request auth to api-0 MemoryEntry', async () => {
  const credential = ['header', 'credential'].join('-');
  const fakeApi = createFakeApi(async (_req, res, record) => {
    assert.equal(record.method, 'POST');
    assert.equal(record.path, '/v1/MemoryEntry');
    assert.equal(record.headers.authorization, `Bearer ${credential}`);
    assert.equal(record.headers.valkyr_auth, credential);
    assert.equal(record.headers.cookie, `VALKYR_AUTH=${credential}`);
    assert.equal(record.body.type, 'decision');
    assert.equal(record.body.text, 'ship the MCP server');

    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ id: 'mem-1', ...record.body }));
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(
      baseUrl,
      {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/call',
        params: {
          name: 'memory_write',
          arguments: {
            type: 'decision',
            text: 'ship the MCP server',
            tags: ['mcp', 'graymatter']
          }
        }
      },
      { 'X-Valkyr-Token': credential }
    );

    assert.equal(result.status, 200);
    assert.equal(result.body.result.content[0].type, 'text');
    assert.deepEqual(JSON.parse(result.body.result.content[0].text), {
      id: 'mem-1',
      type: 'decision',
      text: 'ship the MCP server',
      tags: ['mcp', 'graymatter']
    });
    assert.equal(fakeApi.requests.length, 1);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('Apps SDK bearer auth is accepted on /mcp and forwarded to api-0', async () => {
  const fakeApi = createFakeApi(async (_req, res, record) => {
    assert.equal(record.method, 'GET');
    assert.equal(record.path, '/v1/MemoryEntry/mem-99');
    assert.equal(record.headers.authorization, 'Bearer apps-sdk-token');

    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ id: 'mem-99' }));
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'bearer-auth',
      method: 'tools/call',
      params: { name: 'memory_read', arguments: { id: 'mem-99' } }
    }, { authorization: 'Bearer apps-sdk-token' }, '/mcp');

    assert.equal(result.status, 200);
    assert.equal(result.body.result.content[0].text, JSON.stringify({ id: 'mem-99' }));
    assert.equal(fakeApi.requests.length, 1);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('MCP process auth reauthenticates once on SESSION_EXPIRED and retries', async () => {
  const fakeApi = createFakeApi(async (_req, res, record) => {
    if (fakeApi.requests.length === 1) {
      assert.equal(record.headers.authorization, 'Bearer expired-process-token');
      res.writeHead(401, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        error: 'SESSION_EXPIRED',
        message: 'Session expired or replaced by another login. Please sign in again to obtain a fresh token.'
      }));
      return;
    }

    assert.equal(record.headers.authorization, 'Bearer refreshed-process-token');
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ id: 'mem-99', recovered: true }));
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({
    apiBase: `${apiBase}/v1`,
    token: 'expired-process-token',
    loginProvider: async () => 'refreshed-process-token'
  });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'reauth',
      method: 'tools/call',
      params: { name: 'memory_read', arguments: { id: 'mem-99' } }
    }, {}, '/mcp');

    assert.equal(result.status, 200);
    assert.equal(result.body.result.content[0].text, JSON.stringify({ id: 'mem-99', recovered: true }));
    assert.equal(fakeApi.requests.length, 2);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('MCP per-request auth does not reauthenticate into a shared process token', async () => {
  let loginCalls = 0;
  const fakeApi = createFakeApi(async (_req, res, record) => {
    assert.equal(record.headers.authorization, 'Bearer expired-user-token');
    res.writeHead(401, { 'content-type': 'application/json' });
    res.end(JSON.stringify({
      error: 'SESSION_EXPIRED',
      message: 'Session expired for this caller.'
    }));
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({
    apiBase: `${apiBase}/v1`,
    token: 'process-token',
    loginProvider: async () => {
      loginCalls += 1;
      return 'refreshed-process-token';
    }
  });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'request-scoped-expired',
      method: 'tools/call',
      params: { name: 'memory_read', arguments: { id: 'mem-99' } }
    }, { authorization: 'Bearer expired-user-token' }, '/mcp');

    assert.equal(result.status, 200);
    assert.equal(result.body.result.structuredContent.reason, 'missing_auth');
    assert.equal(loginCalls, 0);
    assert.equal(fakeApi.requests.length, 1);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('memory tools derive scoped sourceChannel from Codex hierarchy metadata', async () => {
  const automationPath = '/tmp/codex-home/.codex/automations/mcp-and-skill-hunter/memory.md';
  const fakeApi = createFakeApi(async (_req, res, record) => {
    res.writeHead(200, { 'content-type': 'application/json' });
    if (record.path === '/v1/MemoryEntry') {
      assert.equal(record.body.type, 'context');
      assert.equal(record.body.sourceChannel, 'codex:automation:mcp-and-skill-hunter');
      assert.match(record.body.text, /\[graymatter-scope\]/);
      assert.match(record.body.text, /scope: automation/);
      assert.match(record.body.text, /automationId: mcp-and-skill-hunter/);
      assert.match(record.body.text, /artifactPath: \/tmp\/codex-home\/\.codex\/automations\/mcp-and-skill-hunter\/memory\.md/);
      assert.match(record.body.text, /Research complete/);
      res.end(JSON.stringify({ id: 'mem-scoped', ...record.body }));
      return;
    }
    if (record.path === '/v1/MemoryEntry/query') {
      assert.equal(record.body.query, 'Research complete');
      assert.equal(record.body.source, 'codex:automation:mcp-and-skill-hunter');
      assert.equal(record.body.type, 'context');
      res.end(JSON.stringify({ results: [{ id: 'mem-scoped' }] }));
      return;
    }
    throw new Error(`Unexpected path ${record.path}`);
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const writeResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'scoped-write',
      method: 'tools/call',
      params: {
        name: 'memory_write',
        arguments: {
          type: 'context',
          text: 'Research complete',
          scopePath: automationPath,
          user: 'codex-user'
        }
      }
    });
    const queryResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'scoped-query',
      method: 'tools/call',
      params: {
        name: 'memory_query',
        arguments: {
          query: 'Research complete',
          type: 'context',
          scopePath: automationPath
        }
      }
    });

    assert.equal(writeResult.status, 200);
    assert.equal(queryResult.status, 200);
    assert.equal(fakeApi.requests.length, 2);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('entity tools route list, get, and create calls with RBAC-scoped auth', async () => {
  const credential = ['entity', 'credential'].join('-');
  const fakeApi = createFakeApi(async (_req, res, record) => {
    assert.equal(record.headers.authorization, `Bearer ${credential}`);
    res.writeHead(200, { 'content-type': 'application/json' });
    if (record.path === '/v1/Customer' && record.method === 'GET') {
      assert.equal(record.query.get('limit'), '2');
      res.end(JSON.stringify([{ id: 'cust-1' }]));
      return;
    }
    if (record.path === '/v1/Customer/cust-1' && record.method === 'GET') {
      res.end(JSON.stringify({ id: 'cust-1', name: 'Acme' }));
      return;
    }
    if (record.path === '/v1/Task' && record.method === 'POST') {
      assert.equal(record.body.title, 'Follow up');
      res.end(JSON.stringify({ id: 'task-1', ...record.body }));
      return;
    }
    throw new Error(`Unexpected ${record.method} ${record.path}`);
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);
  const headers = { 'X-Valkyr-Token': credential };

  try {
    const listResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'entity-list',
      method: 'tools/call',
      params: { name: 'entity_list', arguments: { entityType: 'Customer', limit: 2 } }
    }, headers);
    const getResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'entity-get',
      method: 'tools/call',
      params: { name: 'entity_get', arguments: { entityType: 'Customer', id: 'cust-1' } }
    }, headers);
    const createResult = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'entity-create',
      method: 'tools/call',
      params: { name: 'entity_create', arguments: { entityType: 'Task', body: { title: 'Follow up' } } }
    }, headers);

    assert.deepEqual(JSON.parse(listResult.body.result.content[0].text), [{ id: 'cust-1' }]);
    assert.deepEqual(JSON.parse(getResult.body.result.content[0].text), { id: 'cust-1', name: 'Acme' });
    assert.deepEqual(JSON.parse(createResult.body.result.content[0].text), { id: 'task-1', title: 'Follow up' });
    assert.equal(fakeApi.requests.length, 3);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('schema_summary fetches and summarizes live OpenAPI metadata', async () => {
  const fakeApi = createFakeApi(async (_req, res, record) => {
    assert.equal(record.method, 'GET');
    assert.equal(record.path, '/v1/api-docs');

    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({
      info: { title: 'ValkyrAI API', version: '2026.05' },
      tags: [{ name: 'Customer' }, { name: 'MemoryEntry' }],
      paths: {
        '/Customer': {},
        '/Customer/{id}': {},
        '/MemoryEntry': {},
        '/SwarmOps/graph': {}
      }
    }));
  });

  const apiBase = await listen(fakeApi.server);
  const server = createGrayMatterMcpServer({ apiBase: `${apiBase}/v1` });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: {
        name: 'schema_summary',
        arguments: {}
      }
    });

    const summary = JSON.parse(result.body.result.content[0].text);
    assert.equal(summary.title, 'ValkyrAI API');
    assert.equal(summary.version, '2026.05');
    assert.equal(summary.pathCount, 4);
    assert.deepEqual(summary.entities, ['Customer', 'MemoryEntry', 'SwarmOps']);
  } finally {
    server.close();
    fakeApi.server.close();
  }
});

test('tool errors return JSON-RPC errors instead of HTTP failures', async () => {
  const server = createGrayMatterMcpServer({ apiBase: 'https://api-0.example.test/v1' });
  const baseUrl = await listen(server);

  try {
    const result = await postRpc(baseUrl, {
      jsonrpc: '2.0',
      id: 'bad-tool',
      method: 'tools/call',
      params: {
        name: 'entity_get',
        arguments: { entityType: '../Customer', id: 'cust-1' }
      }
    });

    assert.equal(result.status, 200);
    assert.equal(result.body.error.code, -32000);
    assert.match(result.body.error.message, /entityType/);
  } finally {
    server.close();
  }
});

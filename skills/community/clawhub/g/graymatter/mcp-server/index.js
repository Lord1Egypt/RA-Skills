#!/usr/bin/env node
'use strict';

const http = require('node:http');
const readline = require('node:readline');
const { execFileSync } = require('node:child_process');
const path = require('node:path');
const { URL } = require('node:url');

const DEFAULT_API_BASE = 'https://api-0.valkyrlabs.com/v1';
const DEFAULT_WIDGET_DOMAIN = 'https://graymatter.valkyrlabs.com';
const DEFAULT_BUY_CREDITS_URL = 'https://valkyrlabs.com/buy-credits';
const DEFAULT_SIGNUP_URL = 'https://valkyrlabs.com/funnel/white-paper';
const DEFAULT_LOGIN_PATH = '/auth/login';
const DEFAULT_PORT = 3333;
const APP_UI_RESOURCE_URI = 'ui://graymatter/overview.html';
const APP_CONNECT_DOMAINS = ['https://api-0.valkyrlabs.com'];
const APP_SECURITY_SCHEMES = [
  { type: 'apiKey', in: 'header', name: 'X-Valkyr-Token' },
  { type: 'http', scheme: 'bearer' }
];

const tools = [
  defineTool({
    name: 'memory_write',
    title: 'Write memory',
    description: 'Write a durable GrayMatter MemoryEntry.',
    inputSchema: {
      type: 'object',
      properties: {
        type: { type: 'string', enum: ['decision', 'todo', 'context', 'artifact', 'preference'] },
        text: { type: 'string' },
        sourceChannel: { type: 'string' },
        scope: { type: 'string', description: 'Memory scope, for example automation, workspace, chat, or session.' },
        runtime: { type: 'string', description: 'Runtime namespace used when deriving sourceChannel. Defaults to codex.' },
        user: { type: 'string' },
        workspaceKey: { type: 'string' },
        chatKey: { type: 'string' },
        sessionKey: { type: 'string' },
        automationId: { type: 'string' },
        artifactPath: { type: 'string' },
        scopePath: { type: 'string', description: 'Local path used to derive automation/workspace memory scope.' },
        tags: { oneOf: [{ type: 'array', items: { type: 'string' } }, { type: 'string' }] }
      },
      required: ['type', 'text']
    },
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true, idempotentHint: false },
    invoking: 'Writing memory',
    invoked: 'Memory written'
  }),
  defineTool({
    name: 'memory_read',
    title: 'Read memory',
    description: 'Read a durable GrayMatter MemoryEntry by id.',
    inputSchema: {
      type: 'object',
      properties: { id: { type: 'string' } },
      required: ['id']
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
    invoking: 'Reading memory',
    invoked: 'Memory ready'
  }),
  defineTool({
    name: 'memory_query',
    title: 'Search memory',
    description: 'Semantic search across GrayMatter memory.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string' },
        limit: { type: 'integer', minimum: 1, maximum: 100 },
        type: { type: 'string' },
        sourceChannel: { type: 'string' },
        scope: { type: 'string' },
        runtime: { type: 'string' },
        workspaceKey: { type: 'string' },
        chatKey: { type: 'string' },
        sessionKey: { type: 'string' },
        automationId: { type: 'string' },
        artifactPath: { type: 'string' },
        scopePath: { type: 'string' }
      },
      required: ['query']
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
    invoking: 'Searching memory',
    invoked: 'Memory search ready'
  }),
  defineTool({
    name: 'graph_get',
    title: 'Get graph',
    description: 'Inspect the SwarmOps shared object graph.',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Optional graph subpath.' }
      }
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
    invoking: 'Reading graph',
    invoked: 'Graph ready'
  }),
  defineTool({
    name: 'entity_list',
    title: 'List entities',
    description: 'List live ValkyrAI business entities by type.',
    inputSchema: {
      type: 'object',
      properties: {
        entityType: { type: 'string' },
        limit: { type: 'integer', minimum: 1, maximum: 500 },
        offset: { type: 'integer', minimum: 0 }
      },
      required: ['entityType']
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
    invoking: 'Listing entities',
    invoked: 'Entities ready'
  }),
  defineTool({
    name: 'entity_get',
    title: 'Get entity',
    description: 'Fetch one live ValkyrAI business entity by type and id.',
    inputSchema: {
      type: 'object',
      properties: {
        entityType: { type: 'string' },
        id: { type: 'string' }
      },
      required: ['entityType', 'id']
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
    invoking: 'Reading entity',
    invoked: 'Entity ready'
  }),
  defineTool({
    name: 'entity_create',
    title: 'Create entity',
    description: 'Create one live ValkyrAI business entity when RBAC permits it.',
    inputSchema: {
      type: 'object',
      properties: {
        entityType: { type: 'string' },
        body: { type: 'object' }
      },
      required: ['entityType', 'body']
    },
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true, idempotentHint: false },
    invoking: 'Creating entity',
    invoked: 'Entity created'
  }),
  defineTool({
    name: 'show_graymatter_overview',
    title: 'Show GrayMatter overview',
    description: 'Render an overview of the GrayMatter memory, graph, and schema tools for the current ChatGPT app session.',
    inputSchema: { type: 'object', properties: {} },
    outputSchema: {
      type: 'object',
      properties: {
        app: { type: 'string' },
        mcpEndpointPath: { type: 'string' },
        toolCount: { type: 'integer' },
        privacyPolicyUrl: { type: 'string' }
      },
      required: ['app', 'mcpEndpointPath', 'toolCount', 'privacyPolicyUrl']
    },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false, idempotentHint: true },
    invoking: 'Showing overview',
    invoked: 'Overview ready',
    uiResourceUri: APP_UI_RESOURCE_URI
  }),
  defineTool({
    name: 'schema_summary',
    title: 'Summarize schema',
    description: 'Summarize the live ValkyrAI OpenAPI schema.',
    inputSchema: { type: 'object', properties: {} },
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true, idempotentHint: true },
    invoking: 'Reading schema',
    invoked: 'Schema ready'
  })
];

function createGrayMatterMcpServer(options = {}) {
  const apiBase = withoutTrailingSlash(options.apiBase || process.env.VALKYR_API_BASE || DEFAULT_API_BASE);
  const widgetDomain = withoutTrailingSlash(options.widgetDomain || process.env.GRAYMATTER_WIDGET_DOMAIN || DEFAULT_WIDGET_DOMAIN);
  const fetchImpl = options.fetch || globalThis.fetch;
  const loginProvider = options.loginProvider || runLoginCommand;
  const loginCommand = options.loginCommand || process.env.GRAYMATTER_LOGIN_COMMAND || path.join(__dirname, '..', 'scripts', 'gm-login');
  const processToken = options.token || process.env.VALKYR_AUTH_TOKEN || process.env.VALKYR_JWT_SESSION || '';

  if (typeof fetchImpl !== 'function') {
    throw new Error('Global fetch is required. Use Node 20 or newer.');
  }

  return http.createServer(async (req, res) => {
    try {
      const requestUrl = new URL(req.url, 'http://127.0.0.1');

      if (req.method === 'OPTIONS') {
        sendNoContent(res);
        return;
      }

      if (req.method === 'GET' && requestUrl.pathname === '/health') {
        sendJson(res, 200, {
          ok: true,
          apiBase,
          tools: tools.map((tool) => tool.name)
        });
        return;
      }

      if (req.method === 'GET' && requestUrl.pathname === '/sse') {
        openSseStream(req, res);
        return;
      }

      if (req.method === 'POST' && (requestUrl.pathname === '/' || requestUrl.pathname === '/message' || requestUrl.pathname === '/mcp')) {
        const rpcRequest = await readJson(req);
        const rpcResponse = await handleRpc(rpcRequest, {
          apiBase,
          fetchImpl,
          ...authContextFrom(req, processToken),
          loginCommand,
          loginProvider,
          widgetDomain
        });

        if (rpcResponse === null) {
          sendNoContent(res);
          return;
        }

        sendJson(res, 200, rpcResponse);
        return;
      }

      sendJson(res, 404, { error: 'Not found' });
    } catch (error) {
      sendJson(res, 500, { error: error.message });
    }
  });
}

function createRpcContext(options = {}) {
  const apiBase = withoutTrailingSlash(options.apiBase || process.env.VALKYR_API_BASE || DEFAULT_API_BASE);
  const widgetDomain = withoutTrailingSlash(options.widgetDomain || process.env.GRAYMATTER_WIDGET_DOMAIN || DEFAULT_WIDGET_DOMAIN);
  const fetchImpl = options.fetch || globalThis.fetch;
  const loginProvider = options.loginProvider || runLoginCommand;
  const loginCommand = options.loginCommand || process.env.GRAYMATTER_LOGIN_COMMAND || path.join(__dirname, '..', 'scripts', 'gm-login');

  if (typeof fetchImpl !== 'function') {
    throw new Error('Global fetch is required. Use Node 20 or newer.');
  }

  return {
    apiBase,
    fetchImpl,
    token: options.token || process.env.VALKYR_AUTH_TOKEN || process.env.VALKYR_JWT_SESSION || '',
    requestScopedToken: false,
    loginCommand,
    loginProvider,
    widgetDomain
  };
}

function startStdioServer(options = {}) {
  const context = createRpcContext(options);
  const lines = readline.createInterface({
    input: process.stdin,
    crlfDelay: Infinity
  });

  lines.on('line', async (line) => {
    const trimmed = line.trim();
    if (!trimmed) {
      return;
    }

    try {
      const message = JSON.parse(trimmed);
      const response = await handleRpc(message, context);
      if (response !== null) {
        process.stdout.write(`${JSON.stringify(response)}\n`);
      }
    } catch (error) {
      process.stdout.write(`${JSON.stringify(jsonRpcError(null, -32700, `Invalid JSON-RPC message: ${error.message}`))}\n`);
    }
  });
}

async function handleRpc(message, context) {
  if (!message || message.jsonrpc !== '2.0' || typeof message.method !== 'string') {
    return jsonRpcError(null, -32600, 'Invalid JSON-RPC request');
  }

  const id = Object.prototype.hasOwnProperty.call(message, 'id') ? message.id : null;

  if (!Object.prototype.hasOwnProperty.call(message, 'id')) {
    if (message.method === 'notifications/initialized') {
      return null;
    }
    return null;
  }

  try {
    switch (message.method) {
      case 'initialize':
        return jsonRpcResult(id, {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {}, resources: {} },
          serverInfo: {
            name: 'graymatter',
            version: '0.1.0'
          }
        });
      case 'tools/list':
        return jsonRpcResult(id, { tools });
      case 'resources/list':
        return jsonRpcResult(id, { resources: [appResourceDescriptor()] });
      case 'resources/read':
        return jsonRpcResult(id, readResource(message.params || {}, context));
      case 'tools/call':
        return jsonRpcResult(id, await callTool(message.params || {}, context));
      default:
        return jsonRpcError(id, -32601, `Unknown method: ${message.method}`);
    }
  } catch (error) {
    return jsonRpcError(id, -32000, error.message);
  }
}

async function callTool(params, context) {
  const name = params.name;
  const args = params.arguments || {};

  const execute = async (operation, requestFn) => {
    try {
      return toolResult(await requestFn());
    } catch (error) {
      const recovery = buildRecoveryResult(error, operation, context);
      if (recovery) {
        return recovery;
      }
      throw error;
    }
  };

  switch (name) {
    case 'memory_write':
      return execute('memory_write', () => apiRequest(context, 'POST', 'MemoryEntry', buildMemoryWritePayload(args)));
    case 'memory_read':
      requireString(args.id, 'id');
      return execute('memory_read', () => apiRequest(context, 'GET', `MemoryEntry/${encodeURIComponent(args.id)}`));
    case 'memory_query':
      requireString(args.query, 'query');
      return execute('memory_query', () => apiRequest(context, 'POST', 'MemoryEntry/query', buildMemoryQueryPayload(args)));
    case 'graph_get': {
      const graphPath = args.path ? `SwarmOps/graph/${trimSlashes(args.path)}` : 'SwarmOps/graph';
      return execute('graph_get', () => apiRequest(context, 'GET', graphPath));
    }
    case 'entity_list': {
      requireEntityType(args.entityType);
      const query = new URLSearchParams();
      if (args.limit !== undefined) query.set('limit', String(args.limit));
      if (args.offset !== undefined) query.set('offset', String(args.offset));
      const suffix = query.toString() ? `?${query}` : '';
      return execute('entity_list', () => apiRequest(context, 'GET', `${args.entityType}${suffix}`));
    }
    case 'entity_get':
      requireEntityType(args.entityType);
      requireString(args.id, 'id');
      return execute('entity_get', () => apiRequest(context, 'GET', `${args.entityType}/${encodeURIComponent(args.id)}`));
    case 'entity_create':
      requireEntityType(args.entityType);
      if (!args.body || typeof args.body !== 'object' || Array.isArray(args.body)) {
        throw new Error('body must be an object');
      }
      return execute('entity_create', () => apiRequest(context, 'POST', args.entityType, args.body));
    case 'show_graymatter_overview':
      return overviewToolResult();
    case 'schema_summary':
      return execute('schema_summary', async () => summarizeOpenApi(await apiRequest(context, 'GET', 'api-docs')));
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

function defineTool(tool) {
  const securitySchemes = cloneSecuritySchemes();
  const descriptor = {
    name: tool.name,
    title: tool.title,
    description: tool.description,
    inputSchema: tool.inputSchema,
    securitySchemes,
    annotations: tool.annotations,
    _meta: {
      securitySchemes,
      'openai/toolInvocation/invoking': tool.invoking,
      'openai/toolInvocation/invoked': tool.invoked
    }
  };

  if (tool.outputSchema) {
    descriptor.outputSchema = tool.outputSchema;
  }

  if (tool.uiResourceUri) {
    descriptor._meta.ui = {
      resourceUri: tool.uiResourceUri,
      visibility: ['model', 'app']
    };
    descriptor._meta['openai/outputTemplate'] = tool.uiResourceUri;
    descriptor._meta['openai/widgetAccessible'] = true;
  }

  return descriptor;
}

function cloneSecuritySchemes() {
  return APP_SECURITY_SCHEMES.map((scheme) => ({ ...scheme }));
}

function appResourceDescriptor() {
  return {
    uri: APP_UI_RESOURCE_URI,
    name: 'GrayMatter overview',
    title: 'GrayMatter overview',
    description: 'Overview card for GrayMatter durable memory and schema tools.',
    mimeType: 'text/html;profile=mcp-app'
  };
}

function readResource(params, context) {
  if (params.uri !== APP_UI_RESOURCE_URI) {
    throw new Error(`Unknown resource: ${params.uri || ''}`);
  }

  return {
    contents: [
      {
        uri: APP_UI_RESOURCE_URI,
        mimeType: 'text/html;profile=mcp-app',
        text: overviewWidgetHtml(),
        _meta: resourceMeta(context.widgetDomain)
      }
    ]
  };
}

function resourceMeta(widgetDomain) {
  return {
    ui: {
      prefersBorder: true,
      domain: widgetDomain,
      csp: {
        connectDomains: APP_CONNECT_DOMAINS,
        resourceDomains: [widgetDomain]
      }
    },
    'openai/widgetDescription': 'GrayMatter overview for durable memory, graph, and schema tools.',
    'openai/widgetPrefersBorder': true,
    'openai/widgetDomain': widgetDomain,
    'openai/widgetCSP': {
      connect_domains: APP_CONNECT_DOMAINS,
      resource_domains: [widgetDomain]
    }
  };
}

function overviewToolResult() {
  const structuredContent = {
    app: 'GrayMatter',
    mcpEndpointPath: '/mcp',
    toolCount: tools.length,
    privacyPolicyUrl: 'https://github.com/ValkyrLabs/GrayMatter/blob/main/docs/privacy-policy.md'
  };

  return {
    structuredContent,
    content: [
      {
        type: 'text',
        text: 'GrayMatter exposes durable memory, shared graph, and ValkyrAI schema tools through an Apps SDK-ready MCP endpoint.'
      }
    ]
  };
}

function overviewWidgetHtml() {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GrayMatter Overview</title>
    <style>
      :root {
        color-scheme: light dark;
        --gm-bg: #f4f0e6;
        --gm-card: #fffaf0;
        --gm-ink: #15372f;
        --gm-muted: #5a6d65;
        --gm-line: #d9ccb5;
        --gm-accent: #245b4a;
      }
      body {
        margin: 0;
        background: var(--gm-bg);
        color: var(--gm-ink);
        font: 15px/1.45 Georgia, "Times New Roman", serif;
      }
      .card {
        border: 1px solid var(--gm-line);
        border-radius: 18px;
        background: linear-gradient(135deg, var(--gm-card), #eef4ec);
        padding: 20px;
      }
      h1 {
        margin: 0 0 8px;
        font-size: 24px;
      }
      p {
        margin: 0 0 14px;
        color: var(--gm-muted);
      }
      ul {
        display: grid;
        gap: 8px;
        margin: 0;
        padding: 0;
        list-style: none;
      }
      li {
        border-left: 4px solid var(--gm-accent);
        background: rgba(255, 255, 255, 0.5);
        padding: 8px 10px;
      }
      @media (prefers-color-scheme: dark) {
        :root {
          --gm-bg: #10251f;
          --gm-card: #18362d;
          --gm-ink: #f6ead5;
          --gm-muted: #c0d0c8;
          --gm-line: #315f50;
          --gm-accent: #92ccb4;
        }
        li {
          background: rgba(0, 0, 0, 0.18);
        }
      }
    </style>
  </head>
  <body>
    <main class="card">
      <h1>GrayMatter</h1>
      <p>Durable memory, graph context, and live ValkyrAI schema access for agent workflows.</p>
      <ul>
        <li>Store decisions, todos, preferences, context, and artifacts as MemoryEntry records.</li>
        <li>Search prior memory semantically before acting in a new chat or automation.</li>
        <li>Inspect RBAC-scoped business entities and schema metadata through api-0.</li>
      </ul>
    </main>
  </body>
</html>`;
}

async function apiRequest(context, method, endpoint, body) {
  try {
    return await apiRequestOnce(context, method, endpoint, body);
  } catch (error) {
    if (!isRefreshableAuthError(error) || !(await refreshAuth(context))) {
      throw error;
    }
    return apiRequestOnce(context, method, endpoint, body);
  }
}

async function apiRequestOnce(context, method, endpoint, body) {
  const headers = {
    accept: 'application/json'
  };

  if (body !== undefined) {
    headers['content-type'] = 'application/json';
  }

  if (context.token) {
    headers.authorization = `Bearer ${context.token}`;
    headers.VALKYR_AUTH = context.token;
    headers.cookie = `VALKYR_AUTH=${context.token}`;
  }

  const response = await context.fetchImpl(apiUrl(context.apiBase, endpoint), {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const raw = await response.text();
  const payload = raw ? parseJson(raw) : null;

  if (!response.ok) {
    const message = payload && typeof payload.message === 'string'
      ? payload.message
      : `api-0 request failed with HTTP ${response.status}`;
    const error = new Error(message);
    error.name = 'ApiRequestError';
    error.status = response.status;
    error.payload = payload;
    error.method = method;
    error.endpoint = endpoint;
    throw error;
  }

  return payload;
}

async function refreshAuth(context) {
  if (!context || context.requestScopedToken || typeof context.loginProvider !== 'function') {
    return false;
  }

  try {
    const token = await context.loginProvider(context);
    if (!token || typeof token !== 'string') {
      return false;
    }
    context.token = token;
    return true;
  } catch {
    return false;
  }
}

function isRefreshableAuthError(error) {
  if (!error || error.name !== 'ApiRequestError' || error.status !== 401) {
    return false;
  }

  const payload = error.payload;
  const text = typeof payload === 'string' ? payload : JSON.stringify(payload || {});
  return /SESSION_EXPIRED|TOKEN_EXPIRED|expired|missing auth|unauthorized/i.test(text);
}

function runLoginCommand(context) {
  const loginCommand = context.loginCommand || process.env.GRAYMATTER_LOGIN_COMMAND || path.join(__dirname, '..', 'scripts', 'gm-login');
  const output = execFileSync(loginCommand, ['env'], {
    encoding: 'utf8',
    env: {
      ...process.env,
      VALKYR_API_BASE: context.apiBase
    },
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: Number(process.env.GRAYMATTER_LOGIN_TIMEOUT_MS || 30000)
  });
  return parseExportedToken(output);
}

function parseExportedToken(output) {
  const text = String(output || '');
  const patterns = [
    /^export\s+VALKYR_AUTH_TOKEN="([^"]+)"$/m,
    /^export\s+VALKYR_JWT_SESSION="([^"]+)"$/m,
    /^VALKYR_AUTH_TOKEN=([^\n]+)$/m,
    /^VALKYR_JWT_SESSION=([^\n]+)$/m
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim();
    }
  }

  return '';
}

function buildRecoveryResult(error, operation, context) {
  if (!error || error.name !== 'ApiRequestError') {
    return null;
  }

  const signal = classifyRecoveryReason(error);
  if (!signal) {
    return null;
  }

  const buyCreditsUrl = process.env.VALKYR_BUY_CREDITS_URL || DEFAULT_BUY_CREDITS_URL;
  const signupUrl = process.env.VALKYR_HUMAN_SIGNUP_URL || DEFAULT_SIGNUP_URL;
  const loginUrl = apiUrl(context.apiBase, process.env.GRAYMATTER_LOGIN_PATH || DEFAULT_LOGIN_PATH);
  const retryable = signal.reason === 'insufficient_credits' || signal.reason === 'missing_auth';

  const structuredContent = {
    ok: false,
    reason: signal.reason,
    blockedOperation: operation,
    message: signal.message,
    buyCreditsUrl,
    signupUrl,
    loginUrl,
    retryable
  };

  return {
    structuredContent,
    content: [
      {
        type: 'text',
        text: JSON.stringify(structuredContent)
      }
    ],
    _meta: {
      openai: {
        recovery: {
          reason: signal.reason,
          blockedOperation: operation,
          retryable,
          urls: { buyCreditsUrl, signupUrl, loginUrl }
        },
        debug: {
          status: error.status,
          endpoint: error.endpoint,
          method: error.method,
          rawMessage: error.message
        }
      }
    }
  };
}

function classifyRecoveryReason(error) {
  const payload = error.payload;
  const bodyText = typeof payload === 'string' ? payload : JSON.stringify(payload || {});
  const upperText = bodyText.toUpperCase();
  const lowerText = bodyText.toLowerCase();

  if (error.status === 402 || upperText.includes('INSUFFICIENT_FUNDS') || lowerText.includes('insufficient') && lowerText.includes('credit')) {
    return {
      reason: 'insufficient_credits',
      message: 'GrayMatter needs credits before this operation can continue. Buy credits or sign up, then retry.'
    };
  }

  if (error.status === 401) {
    return {
      reason: 'missing_auth',
      message: 'Authentication is missing or expired. Sign in, then retry.'
    };
  }

  if (error.status === 403) {
    if (lowerText.includes('read-only') || lowerText.includes('readonly') || lowerText.includes('write') && lowerText.includes('forbidden')) {
      return {
        reason: 'read_only_auth',
        message: 'This credential is read-only for the requested operation. Use a write-capable token.'
      };
    }
    return {
      reason: 'missing_auth',
      message: 'Access was denied. Sign in with the correct account or workspace access, then retry.'
    };
  }

  return null;
}

function buildMemoryWritePayload(args) {
  requireString(args.type, 'type');
  requireString(args.text, 'text');

  const metadata = memoryScopeMetadata(args);
  const sourceChannel = args.sourceChannel || metadata.sourceChannel;
  if (sourceChannel) {
    metadata.sourceChannel = sourceChannel;
  }

  const payload = {
    type: args.type,
    text: Object.keys(metadata).length > 0 ? wrapMemoryText(args.text, metadata) : args.text
  };

  if (sourceChannel) {
    payload.sourceChannel = sourceChannel;
  }

  if (args.tags !== undefined) {
    payload.tags = args.tags;
  }

  return payload;
}

function buildMemoryQueryPayload(args) {
  const metadata = memoryScopeMetadata(args);
  const source = args.sourceChannel || metadata.sourceChannel;
  const payload = {
    query: args.query
  };

  if (args.limit !== undefined) {
    payload.limit = args.limit;
  }
  if (args.type !== undefined) {
    payload.type = args.type;
  }
  if (source) {
    payload.source = source;
  }

  return payload;
}

function memoryScopeMetadata(args) {
  if (!hasScopeSignal(args)) {
    return {};
  }

  const runtime = args.runtime || 'codex';
  const metadata = pickDefined({
    scope: args.scope,
    runtime,
    user: args.user,
    workspaceKey: args.workspaceKey,
    chatKey: args.chatKey,
    sessionKey: args.sessionKey,
    automationId: args.automationId,
    artifactPath: args.artifactPath || args.scopePath
  });

  if (!metadata.scope && args.scopePath) {
    metadata.scope = scopeFromPath(args.scopePath);
  }
  if (!metadata.automationId && args.scopePath) {
    metadata.automationId = automationIdFromPath(args.scopePath);
  }
  if (!metadata.workspaceKey && args.scopePath) {
    metadata.workspaceKey = workspaceKeyFromPath(args.scopePath);
  }

  const sourceChannel = deriveSourceChannel({ ...args, ...metadata, runtime });
  if (sourceChannel) {
    metadata.sourceChannel = sourceChannel;
  }

  return pickDefined(metadata);
}

function hasScopeSignal(args) {
  return Boolean(
    args.scope ||
    args.runtime ||
    args.user ||
    args.workspaceKey ||
    args.chatKey ||
    args.sessionKey ||
    args.automationId ||
    args.artifactPath ||
    args.scopePath ||
    args.sourceChannel
  );
}

function deriveSourceChannel(values) {
  const runtime = values.runtime || 'codex';
  if (values.sourceChannel) return values.sourceChannel;
  if (values.chatKey) return scopedKey(runtime, 'chat', values.chatKey);
  if (values.sessionKey) return scopedKey(runtime, 'session', values.sessionKey);
  if (values.automationId) return scopedKey(runtime, 'automation', values.automationId);
  if (values.workspaceKey) return scopedKey(runtime, 'workspace', values.workspaceKey);
  return '';
}

function scopedKey(runtime, kind, value) {
  const raw = String(value || '');
  return raw.includes(':') ? raw : `${runtime}:${kind}:${raw}`;
}

function scopeFromPath(pathValue) {
  if (automationIdFromPath(pathValue)) return 'automation';
  if (workspaceKeyFromPath(pathValue)) return 'workspace';
  return '';
}

function automationIdFromPath(pathValue) {
  const match = String(pathValue || '').match(/\.codex\/automations\/([^/]+)/);
  return match ? match[1] : '';
}

function workspaceKeyFromPath(pathValue) {
  const match = String(pathValue || '').match(/\/Documents\/Codex\/([^/]+)\/([^/]+)/);
  return match ? `${match[1]}/${match[2]}` : '';
}

function wrapMemoryText(text, metadata) {
  const lines = Object.entries(metadata)
    .filter(([, value]) => value !== undefined && value !== null && String(value).length > 0)
    .map(([key, value]) => `${key}: ${value}`);

  if (lines.length === 0) {
    return text;
  }

  return `[graymatter-scope]\n${lines.join('\n')}\n[/graymatter-scope]\n\n${text}`;
}

function pickDefined(values) {
  return Object.fromEntries(
    Object.entries(values).filter(([, value]) => value !== undefined && value !== null && String(value).length > 0)
  );
}

function summarizeOpenApi(spec) {
  const entities = new Set();
  for (const tag of spec.tags || []) {
    if (tag && typeof tag.name === 'string' && isEntityName(tag.name)) {
      entities.add(tag.name);
    }
  }

  const paths = spec.paths || {};
  for (const path of Object.keys(paths)) {
    const firstSegment = path.split('/').filter(Boolean)[0];
    if (firstSegment && isEntityName(firstSegment)) {
      entities.add(firstSegment);
    }
  }

  return {
    title: spec.info && spec.info.title ? spec.info.title : 'ValkyrAI API',
    version: spec.info && spec.info.version ? spec.info.version : null,
    pathCount: Object.keys(paths).length,
    entities: Array.from(entities)
  };
}

function authContextFrom(req, processToken = '') {
  const headerToken = req.headers['x-valkyr-token'];
  if (Array.isArray(headerToken)) {
    return { token: headerToken[0] || '', requestScopedToken: Boolean(headerToken[0]) };
  }
  if (headerToken) {
    return { token: headerToken, requestScopedToken: true };
  }

  const authHeader = Array.isArray(req.headers.authorization)
    ? req.headers.authorization[0]
    : req.headers.authorization;
  const bearerMatch = typeof authHeader === 'string' ? authHeader.match(/^Bearer\s+(.+)$/i) : null;
  if (bearerMatch) {
    return { token: bearerMatch[1].trim(), requestScopedToken: true };
  }

  return { token: processToken || process.env.VALKYR_AUTH_TOKEN || process.env.VALKYR_JWT_SESSION || '', requestScopedToken: false };
}

function apiUrl(apiBase, endpoint) {
  const base = `${withoutTrailingSlash(apiBase)}/`;
  const cleanEndpoint = endpoint.replace(/^\/+/, '');
  return new URL(cleanEndpoint, base).toString();
}

function openSseStream(req, res) {
  res.writeHead(200, {
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache, no-transform',
    connection: 'keep-alive',
    'content-type': 'text/event-stream'
  });
  res.write('event: endpoint\n');
  res.write('data: /message\n\n');
  const keepAlive = setInterval(() => {
    res.write(': keepalive\n\n');
  }, 25000);
  req.on('close', () => clearInterval(keepAlive));
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('error', reject);
    req.on('end', () => {
      const raw = Buffer.concat(chunks).toString('utf8');
      if (!raw) {
        resolve(null);
        return;
      }
      try {
        resolve(JSON.parse(raw));
      } catch (error) {
        reject(new Error(`Invalid JSON body: ${error.message}`));
      }
    });
  });
}

function sendJson(res, status, payload) {
  res.writeHead(status, {
    'access-control-allow-origin': '*',
    'access-control-allow-headers': 'authorization,content-type,x-valkyr-token',
    'access-control-allow-methods': 'GET,POST,OPTIONS',
    'content-type': 'application/json'
  });
  res.end(JSON.stringify(payload));
}

function sendNoContent(res) {
  res.writeHead(204, {
    'access-control-allow-origin': '*',
    'access-control-allow-headers': 'authorization,content-type,x-valkyr-token',
    'access-control-allow-methods': 'GET,POST,OPTIONS'
  });
  res.end();
}

function toolResult(value) {
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(value)
      }
    ]
  };
}

function jsonRpcResult(id, result) {
  return {
    jsonrpc: '2.0',
    id,
    result
  };
}

function jsonRpcError(id, code, message) {
  return {
    jsonrpc: '2.0',
    id,
    error: { code, message }
  };
}

function parseJson(raw) {
  try {
    return JSON.parse(raw);
  } catch {
    return raw;
  }
}

function requireString(value, name) {
  if (typeof value !== 'string' || value.length === 0) {
    throw new Error(`${name} must be a non-empty string`);
  }
}

function requireEntityType(value) {
  requireString(value, 'entityType');
  if (!/^[A-Za-z][A-Za-z0-9_]*$/.test(value)) {
    throw new Error('entityType must be a simple schema type name');
  }
}

function isEntityName(value) {
  return /^[A-Z][A-Za-z0-9_]*$/.test(value);
}

function trimSlashes(value) {
  return String(value).replace(/^\/+|\/+$/g, '');
}

function withoutTrailingSlash(value) {
  return String(value).replace(/\/+$/g, '');
}

module.exports = {
  createGrayMatterMcpServer,
  startStdioServer,
  tools
};

if (require.main === module) {
  if (process.argv.includes('--stdio')) {
    startStdioServer();
  } else {
    const port = Number(process.env.PORT || DEFAULT_PORT);
    const server = createGrayMatterMcpServer();
    server.listen(port, () => {
      process.stdout.write(`GrayMatter MCP server listening on http://localhost:${port}\n`);
    });
  }
}

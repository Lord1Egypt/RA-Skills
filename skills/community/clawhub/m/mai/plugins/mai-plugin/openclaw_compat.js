import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const OPENCLAW_PLUGIN_ID = 'mai-plugin';

const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_OPENCLAW_SKILL_ROOT = path.join(os.homedir(), '.openclaw', 'workspace', 'skills', 'mai');
const DEFAULT_HERMES_SKILL_ROOT = path.join(os.homedir(), '.hermes', 'skills', 'commerce', 'mai');

function nonEmptyString(value) {
  if (typeof value !== 'string') return undefined;
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function stringList(value) {
  if (Array.isArray(value)) {
    return value.map(String).map((item) => item.trim()).filter(Boolean).join(',');
  }
  return nonEmptyString(value);
}

export function resolveProjectRoot(projectRoot) {
  const explicit = nonEmptyString(projectRoot) || nonEmptyString(process.env.MAI_ROOT);
  if (explicit) return explicit;

  for (const candidate of [DEFAULT_OPENCLAW_SKILL_ROOT, DEFAULT_HERMES_SKILL_ROOT, MODULE_DIR]) {
    if (fs.existsSync(path.join(candidate, 'scripts', 'mai.py'))) {
      return candidate;
    }
  }

  return DEFAULT_OPENCLAW_SKILL_ROOT;
}

export function resolveMaiPluginConfig(api, pluginId = OPENCLAW_PLUGIN_ID) {
  const nestedConfig = api?.config?.plugins?.entries?.[pluginId]?.config || {};
  const directConfig = api?.pluginConfig || {};
  const cfg = { ...directConfig, ...nestedConfig };

  return {
    projectRoot: resolveProjectRoot(cfg.projectRoot),
    dataPath: nonEmptyString(cfg.dataPath) || nonEmptyString(process.env.MAI_DATA),
    registryUrl: nonEmptyString(cfg.registryUrl) || nonEmptyString(process.env.MAI_REGISTRY_URL),
    apiKey: nonEmptyString(cfg.apiKey) || nonEmptyString(process.env.MAI_API_KEY),
  };
}

export function buildMaiCommand({ subcommandArgs = [], dataPath, projectRoot } = {}) {
  const root = resolveProjectRoot(projectRoot);
  const command = ['python3', path.join(root, 'scripts', 'mai.py')];
  if (dataPath) command.push('--data', String(dataPath));
  command.push(...subcommandArgs.map(String));
  return command;
}

function maskCommand(command) {
  const masked = [];
  for (let i = 0; i < command.length; i += 1) {
    masked.push(command[i]);
    if (command[i] === '--api-key' && i + 1 < command.length) {
      i += 1;
      masked.push('***');
    }
  }
  return masked;
}

export function runMaiCli({ subcommandArgs = [], dataPath, projectRoot } = {}) {
  const command = buildMaiCommand({ subcommandArgs, dataPath, projectRoot });
  const result = spawnSync(command[0], command.slice(1), {
    encoding: 'utf8',
  });

  const stdout = (result.stdout || '').trim();
  const stderr = (result.stderr || '').trim();

  if (result.error) {
    return {
      ok: false,
      errorType: 'spawn_error',
      error: String(result.error.message || result.error),
      command: maskCommand(command),
    };
  }

  if (result.status !== 0) {
    return {
      ok: false,
      errorType: 'cli_exit',
      error: `mai exited with code ${result.status}`,
      exitCode: result.status,
      stdout,
      stderr,
      command: maskCommand(command),
    };
  }

  if (!stdout) {
    return { ok: true, status: 'empty_output' };
  }

  try {
    const payload = JSON.parse(stdout);
    if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
      return { ok: true, ...payload };
    }
    return { ok: true, value: payload };
  } catch {
    return { ok: true, text: stdout };
  }
}

function addOptionalArg(args, flag, value) {
  const normalized = nonEmptyString(value);
  if (normalized) args.push(flag, normalized);
}

function addOptionalNumber(args, flag, value) {
  if (value !== undefined && value !== null && value !== '') {
    args.push(flag, String(value));
  }
}

function addOptionalTags(args, value) {
  const tags = stringList(value);
  if (tags) args.push('--tags', tags);
}

function registryUrl(input, config) {
  return nonEmptyString(input.registry_url) || nonEmptyString(input.registryUrl) || config.registryUrl;
}

function registryApiKey(input, config) {
  return nonEmptyString(input.api_key) || nonEmptyString(input.apiKey) || config.apiKey;
}

function booleanFlag(value) {
  return value === true || value === 'true' || value === '1' || value === 1;
}

function withPluginConfig(api, handler) {
  return async (input = {}) => handler(input || {}, resolveMaiPluginConfig(api));
}

function registerTool(api, spec) {
  if (typeof api.registerTool === 'function') {
    api.registerTool(spec);
  }
}

function registerCommand(api, spec) {
  if (typeof api.registerCommand === 'function') {
    api.registerCommand(spec);
  }
}

function toolSpec(api, spec, handler) {
  const wrapped = withPluginConfig(api, handler);
  return {
    ...spec,
    async execute(_id, input = {}) {
      return wrapped(input);
    },
    handler: wrapped,
  };
}

function requireRegistryUrl(input, config) {
  const url = registryUrl(input, config);
  if (!url) {
    return { ok: false, errorType: 'validation', error: 'registry_url is required or configure mai.registryUrl' };
  }
  return { ok: true, url };
}

function addRegistryAuth(args, input, config) {
  const apiKey = registryApiKey(input, config);
  if (apiKey) args.push('--api-key', apiKey);
}

function addRegistryTransportArgs(args, input) {
  if (booleanFlag(input.allow_insecure_localhost) || booleanFlag(input.allowInsecureLocalhost)) {
    args.push('--allow-insecure-localhost');
  }
}

function requireRegistryWriteConfirmation(input, action) {
  if (!booleanFlag(input.confirm)) {
    return {
      ok: false,
      errorType: 'validation',
      error: `confirm=true is required before ${action}. Remote registry writes can publish marketplace, order, message, or payment data.`,
    };
  }
  return { ok: true };
}

function formatHelp(config) {
  const lines = [
    'Mai Plugin is loaded.',
    'Install the mai skill for workflow policy; this plugin adds native tools for deterministic catalog, order, and registry actions.',
    'Tools: mai_create_merchant, mai_add_product, mai_search_products, mai_compare_products, mai_create_order, mai_registry_search_products, mai_registry_push, mai_registry_order.',
    'Registry writes require confirm=true. Remote registry URLs must use HTTPS; http://127.0.0.1 and http://localhost require allow_insecure_localhost=true for local development.',
    'Command: /mai search <query> runs a local product search.',
  ];
  if (config.dataPath) lines.push(`dataPath: ${config.dataPath}`);
  if (config.registryUrl) lines.push(`registryUrl: ${config.registryUrl}`);
  return lines.join('\n');
}

export function registerOpenClawPlugin(api) {
  registerTool(api, toolSpec(api, {
    name: 'mai_create_merchant',
    description: 'Create or update a local Mai merchant profile.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        id: { type: 'string' },
        name: { type: 'string' },
        city: { type: 'string' },
        contact: { type: 'string' },
        tags: { type: 'array', items: { type: 'string' } },
      },
      required: ['id', 'name'],
    },
  }, async (input, config) => {
    const args = ['merchant', 'create', '--id', input.id, '--name', input.name];
    addOptionalArg(args, '--city', input.city);
    addOptionalArg(args, '--contact', input.contact);
    addOptionalTags(args, input.tags);
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_add_product',
    description: 'Add a product listing to a local Mai merchant catalog.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        merchant: { type: 'string' },
        sku: { type: 'string' },
        title: { type: 'string' },
        price: { type: 'number' },
        stock: { type: 'integer' },
        currency: { type: 'string' },
        category: { type: 'string' },
        tags: { type: 'array', items: { type: 'string' } },
        description: { type: 'string' },
        shipping: { type: 'string' },
      },
      required: ['merchant', 'sku', 'title', 'price', 'stock'],
    },
  }, async (input, config) => {
    const args = [
      'product',
      'add',
      '--merchant',
      input.merchant,
      '--sku',
      input.sku,
      '--title',
      input.title,
      '--price',
      String(input.price),
      '--stock',
      String(input.stock),
    ];
    addOptionalArg(args, '--currency', input.currency);
    addOptionalArg(args, '--category', input.category);
    addOptionalTags(args, input.tags);
    addOptionalArg(args, '--description', input.description);
    addOptionalArg(args, '--shipping', input.shipping);
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_search_products',
    description: 'Search local Mai products with deterministic inventory and price filters.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        query: { type: 'string' },
        max_price: { type: 'number' },
        city: { type: 'string' },
        include_out_of_stock: { type: 'boolean' },
      },
    },
  }, async (input, config) => {
    const args = ['search', 'products', '--format', 'json'];
    addOptionalArg(args, '--query', input.query);
    addOptionalNumber(args, '--max-price', input.max_price);
    addOptionalArg(args, '--city', input.city);
    if (input.include_out_of_stock) args.push('--include-out-of-stock');
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_compare_products',
    description: 'Compare local Mai products by SKU and return the best value signal.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        skus: {
          oneOf: [
            { type: 'array', items: { type: 'string' } },
            { type: 'string' },
          ],
        },
      },
      required: ['skus'],
    },
  }, async (input, config) => {
    const skus = Array.isArray(input.skus) ? input.skus.join(',') : String(input.skus);
    return runMaiCli({
      subcommandArgs: ['compare', '--skus', skus, '--format', 'json'],
      dataPath: config.dataPath,
      projectRoot: config.projectRoot,
    });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_create_order',
    description: 'Create a local Mai draft order after buyer confirmation.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        buyer: { type: 'string' },
        merchant: { type: 'string' },
        sku: { type: 'string' },
        quantity: { type: 'integer' },
        offer_price: { type: 'number' },
        note: { type: 'string' },
      },
      required: ['buyer', 'merchant', 'sku', 'quantity'],
    },
  }, async (input, config) => {
    const args = [
      'order',
      'create',
      '--buyer',
      input.buyer,
      '--merchant',
      input.merchant,
      '--sku',
      input.sku,
      '--quantity',
      String(input.quantity),
    ];
    addOptionalNumber(args, '--offer-price', input.offer_price);
    addOptionalArg(args, '--note', input.note);
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_registry_search_products',
    description: 'Search a hosted Mai registry marketplace. Public search is rate limited by the registry.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        registry_url: { type: 'string' },
        api_key: { type: 'string' },
        query: { type: 'string' },
        max_price: { type: 'number' },
        city: { type: 'string' },
        include_out_of_stock: { type: 'boolean' },
        allow_insecure_localhost: {
          type: 'boolean',
          description: 'Allow http://127.0.0.1 or http://localhost for local development only.',
        },
      },
    },
  }, async (input, config) => {
    const required = requireRegistryUrl(input, config);
    if (!required.ok) return required;
    const args = ['registry', 'search-products', '--url', required.url, '--format', 'json'];
    addRegistryAuth(args, input, config);
    addRegistryTransportArgs(args, input);
    addOptionalArg(args, '--query', input.query);
    addOptionalNumber(args, '--max-price', input.max_price);
    addOptionalArg(args, '--city', input.city);
    if (input.include_out_of_stock) args.push('--include-out-of-stock');
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_registry_push',
    description: 'Push the local merchant catalog to a hosted Mai registry using a merchant API key after explicit confirmation.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        registry_url: { type: 'string' },
        api_key: { type: 'string' },
        confirm: {
          type: 'boolean',
          description: 'Must be true to publish local marketplace data to the registry.',
        },
        include_orders: {
          type: 'boolean',
          description: 'Also publish local orders and messages. Default push is catalog-only.',
        },
        allow_insecure_localhost: {
          type: 'boolean',
          description: 'Allow http://127.0.0.1 or http://localhost for local development only.',
        },
      },
    },
  }, async (input, config) => {
    const confirmed = requireRegistryWriteConfirmation(input, 'pushing local catalog data to a registry');
    if (!confirmed.ok) return confirmed;
    const required = requireRegistryUrl(input, config);
    if (!required.ok) return required;
    const args = ['registry', 'push', '--url', required.url, '--format', 'json'];
    addRegistryAuth(args, input, config);
    if (booleanFlag(input.include_orders) || booleanFlag(input.includeOrders)) args.push('--include-orders');
    args.push('--confirm');
    addRegistryTransportArgs(args, input);
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerTool(api, toolSpec(api, {
    name: 'mai_registry_order',
    description: 'Create a draft order in a hosted Mai registry using buyer authorization after explicit confirmation.',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        registry_url: { type: 'string' },
        api_key: { type: 'string' },
        buyer: { type: 'string' },
        merchant: { type: 'string' },
        sku: { type: 'string' },
        quantity: { type: 'integer' },
        offer_price: { type: 'number' },
        note: { type: 'string' },
        confirm: {
          type: 'boolean',
          description: 'Must be true to create the registry draft order.',
        },
        allow_insecure_localhost: {
          type: 'boolean',
          description: 'Allow http://127.0.0.1 or http://localhost for local development only.',
        },
      },
      required: ['buyer', 'merchant', 'sku', 'quantity'],
    },
  }, async (input, config) => {
    const confirmed = requireRegistryWriteConfirmation(input, 'creating a registry draft order');
    if (!confirmed.ok) return confirmed;
    const required = requireRegistryUrl(input, config);
    if (!required.ok) return required;
    const args = [
      'registry',
      'order',
      '--url',
      required.url,
      '--buyer',
      input.buyer,
      '--merchant',
      input.merchant,
      '--sku',
      input.sku,
      '--quantity',
      String(input.quantity),
      '--format',
      'json',
    ];
    addRegistryAuth(args, input, config);
    args.push('--confirm');
    addRegistryTransportArgs(args, input);
    addOptionalNumber(args, '--offer-price', input.offer_price);
    addOptionalArg(args, '--note', input.note);
    return runMaiCli({ subcommandArgs: args, dataPath: config.dataPath, projectRoot: config.projectRoot });
  }));

  registerCommand(api, {
    name: 'mai',
    description: 'Show Mai plugin help or run a local product search.',
    acceptsArgs: true,
    handler: async (ctx = {}) => {
      const rawArgs = String(ctx.args || ctx.text || '').trim();
      const config = resolveMaiPluginConfig(api);
      if (rawArgs.startsWith('search ')) {
        const query = rawArgs.slice('search '.length).trim();
        const payload = runMaiCli({
          subcommandArgs: ['search', 'products', '--query', query, '--format', 'json'],
          dataPath: config.dataPath,
          projectRoot: config.projectRoot,
        });
        return { text: JSON.stringify(payload, null, 2) };
      }
      return { text: formatHelp(config) };
    },
  });
}

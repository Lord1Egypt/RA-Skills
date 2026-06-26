import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  buildMaiCommand,
  registerOpenClawPlugin,
  resolveMaiPluginConfig,
} from '../plugins/mai-plugin/openclaw_compat.js';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

test('buildMaiCommand points at the bundled Python CLI', () => {
  const command = buildMaiCommand({
    projectRoot: '/tmp/mai',
    dataPath: '/tmp/mai.json',
    subcommandArgs: ['search', 'products', '--format', 'json'],
  });

  assert.deepEqual(command, [
    'python3',
    path.join('/tmp/mai', 'scripts', 'mai.py'),
    '--data',
    '/tmp/mai.json',
    'search',
    'products',
    '--format',
    'json',
  ]);
});

test('resolveMaiPluginConfig reads OpenClaw plugin config', () => {
  const api = {
    config: {
      plugins: {
        entries: {
          'mai-plugin': {
            config: {
              projectRoot: '/tmp/project',
              dataPath: '/tmp/data.json',
              registryUrl: 'https://registry.example.test',
              apiKey: 'secret',
            },
          },
        },
      },
    },
  };

  assert.deepEqual(resolveMaiPluginConfig(api), {
    projectRoot: '/tmp/project',
    dataPath: '/tmp/data.json',
    registryUrl: 'https://registry.example.test',
    apiKey: 'secret',
  });
});

test('registerOpenClawPlugin exposes marketplace tools and command', () => {
  const calls = {
    tools: [],
    commands: [],
  };
  const api = {
    registerTool(spec) {
      calls.tools.push(spec);
    },
    registerCommand(spec) {
      calls.commands.push(spec);
    },
    config: {},
  };

  registerOpenClawPlugin(api);

  assert.deepEqual(new Set(calls.tools.map((tool) => tool.name)), new Set([
    'mai_create_merchant',
    'mai_add_product',
    'mai_search_products',
    'mai_compare_products',
    'mai_create_order',
    'mai_registry_search_products',
    'mai_registry_push',
    'mai_registry_order',
  ]));
  assert.equal(calls.commands.length, 1);
  assert.equal(calls.commands[0].name, 'mai');
});

test('registered local tools can create and search products', async () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'mai-openclaw-'));
  const dataPath = path.join(tmpDir, 'mai.json');
  const tools = new Map();
  const api = {
    registerTool(spec) {
      tools.set(spec.name, spec);
    },
    config: {
      plugins: {
        entries: {
          'mai-plugin': {
            config: {
              projectRoot: REPO_ROOT,
              dataPath,
            },
          },
        },
      },
    },
  };

  registerOpenClawPlugin(api);

  const merchant = await tools.get('mai_create_merchant').handler({
    id: 'seller-a',
    name: 'West Lake Tea',
    city: 'Hangzhou',
    contact: 'wechat:westlake',
    tags: ['tea', 'gift'],
  });
  assert.equal(merchant.ok, true);

  const product = await tools.get('mai_add_product').handler({
    merchant: 'seller-a',
    sku: 'tea-a',
    title: 'Longjing Gift Box',
    price: 88,
    stock: 5,
    category: 'tea',
    tags: ['longjing', 'gift'],
  });
  assert.equal(product.ok, true);

  const search = await tools.get('mai_search_products').handler({
    query: 'longjing',
  });
  assert.equal(search.ok, true);
  assert.equal(search.results[0].sku, 'tea-a');
});

test('registered registry write tools require explicit confirmation', async () => {
  const tools = new Map();
  const api = {
    registerTool(spec) {
      tools.set(spec.name, spec);
    },
    config: {
      plugins: {
        entries: {
          'mai-plugin': {
            config: {
              projectRoot: REPO_ROOT,
              registryUrl: 'https://registry.example.test',
            },
          },
        },
      },
    },
  };

  registerOpenClawPlugin(api);

  const push = await tools.get('mai_registry_push').handler({});
  assert.equal(push.ok, false);
  assert.equal(push.errorType, 'validation');
  assert.match(push.error, /confirm=true/);

  const order = await tools.get('mai_registry_order').handler({
    buyer: 'alice',
    merchant: 'seller-a',
    sku: 'tea-a',
    quantity: 1,
  });
  assert.equal(order.ok, false);
  assert.equal(order.errorType, 'validation');
  assert.match(order.error, /confirm=true/);
});

test('OpenClaw package metadata is present and versioned with package.json', () => {
  const pluginRoot = path.join(REPO_ROOT, 'plugins', 'mai-plugin');
  const pkg = JSON.parse(fs.readFileSync(path.join(pluginRoot, 'package.json'), 'utf8'));
  const manifest = JSON.parse(fs.readFileSync(path.join(pluginRoot, 'openclaw.plugin.json'), 'utf8'));

  assert.equal(pkg.name, 'mai-plugin');
  assert.equal(manifest.id, 'mai-plugin');
  assert.equal(manifest.version, pkg.version);
  assert.ok(pkg.openclaw.extensions.includes('./index.js'));
});

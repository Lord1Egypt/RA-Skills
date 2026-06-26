#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

function resolveConfigPath() {
  const arg = process.argv[2];
  if (arg) return path.resolve(arg);
  return '/root/.openclaw/openclaw.json';
}

function loadJson(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(raw);
}

function main() {
  const configPath = resolveConfigPath();
  const data = loadJson(configPath);
  const agents = [
    {
      id: 'main',
      configured: true,
      model: data?.agents?.defaults?.model?.primary ?? '',
    },
  ];

  const models = [];
  const providers = data?.models?.providers ?? {};
  for (const [providerName, provider] of Object.entries(providers)) {
    for (const model of provider?.models ?? []) {
      models.push({
        provider: providerName,
        id: model.id,
        name: model.name,
        input: model.input ?? [],
      });
    }
  }

  console.log(JSON.stringify({ configPath, agents, models }, null, 2));
}

try {
  main();
} catch (error) {
  console.error(JSON.stringify({ error: String(error?.message ?? error) }, null, 2));
  process.exit(1);
}

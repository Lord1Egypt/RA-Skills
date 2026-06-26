#!/usr/bin/env ts-node
/**
 * 设置单个引擎的 API Key
 * 用法：npm run key:set <engine>
 */

import * as readline from 'readline';
import { SecretManager } from '../src/key-manager';
import { EngineType, ENGINE_LABELS } from '../src/types';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function prompt(question: string): Promise<string> {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

async function setKey() {
  const engine = process.argv[2] as EngineType;
  
  if (!engine) {
    console.error('Usage: npm run key:set <engine>');
    console.error('Engines: bailian, tavily, serper, exa, firecrawl');
    rl.close();
    process.exit(1);
  }
  
  const validEngines: EngineType[] = ['bailian', 'tavily', 'serper', 'exa', 'firecrawl'];
  if (!validEngines.includes(engine)) {
    console.error(`Invalid engine: ${engine}`);
    console.error('Valid engines: bailian, tavily, serper, exa, firecrawl');
    rl.close();
    process.exit(1);
  }
  
  const label = ENGINE_LABELS[engine];
  console.log(`\n🔑 Setting API Key for ${label}`);
  console.log('='.repeat(40));
  
  const apiKey = await prompt('Enter API Key: ');
  
  if (!apiKey.trim()) {
    console.error('❌ API Key cannot be empty');
    rl.close();
    process.exit(1);
  }
  
  const secretManager = new SecretManager();
  await secretManager.setEngineKey(engine, apiKey.trim());
  
  console.log(`\n✅ ${label} API Key set successfully!`);
  console.log('View status: npm run key:status');
  
  rl.close();
}

setKey().catch((error) => {
  console.error('❌ Error:', error.message);
  rl.close();
  process.exit(1);
});
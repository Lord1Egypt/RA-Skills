#!/usr/bin/env ts-node
/**
 * 从 JSON 文件导入 API Keys
 * 用法：npm run key:import <json-file>
 */

import * as fs from 'fs';
import * as path from 'path';
import { SecretManager } from '../src/key-manager';

async function importKeys() {
  const filePath = process.argv[2];
  
  if (!filePath) {
    console.error('Usage: npm run key:import <json-file>');
    console.error('\nExample JSON format:');
    console.error(JSON.stringify({
      bailian: 'sk-xxx',
      tavily: 'tvly-your-api-key-here',
      serper: 'xxx',
      exa: 'xxx',
      firecrawl: 'fc-your-api-key-here'
    }, null, 2));
    process.exit(1);
  }
  
  const absolutePath = path.resolve(filePath);
  
  if (!fs.existsSync(absolutePath)) {
    console.error(`❌ File not found: ${absolutePath}`);
    process.exit(1);
  }
  
  try {
    const content = fs.readFileSync(absolutePath, 'utf8');
    const apiKeys = JSON.parse(content);
    
    if (typeof apiKeys !== 'object' || apiKeys === null) {
      throw new Error('Invalid JSON format: expected an object');
    }
    
    const secretManager = new SecretManager();
    await secretManager.initConfig(apiKeys);
    
    console.log(`\n✅ Imported ${Object.keys(apiKeys).length} API Keys from ${path.basename(filePath)}`);
    console.log('View status: npm run key:status');
    
  } catch (error) {
    console.error('❌ Error:', (error as Error).message);
    process.exit(1);
  }
}

importKeys();
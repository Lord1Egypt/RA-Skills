#!/usr/bin/env ts-node
/**
 * Key 管理脚本
 * 用法：ts-node manage-keys.ts <command> [args]
 */

// 直接复用 key-manager.ts 中的 main 函数
import { SecretManager } from '../src/key-manager';

async function main() {
  const secretManager = new SecretManager();
  const command = process.argv[2];
  const args = process.argv.slice(3);
  
  try {
    switch (command) {
      case 'init':
        // 初始化配置
        const apiKeys: Record<string, string> = {};
        const engines = ['bailian', 'tavily', 'serper', 'exa', 'firecrawl'] as const;
        
        console.log('\n🔐 Smart Search API Key Init');
        console.log('================================\n');
        
        for (const engine of engines) {
          const envKey = process.env[`${engine.toUpperCase()}_API_KEY`];
          if (envKey) {
            apiKeys[engine] = envKey;
            console.log(`✅ Found ${engine} key in environment`);
          }
        }
        
        if (Object.keys(apiKeys).length === 0) {
          console.log('⚠️  No API keys found in environment variables.');
          console.log('Set environment variables like: BAILIAN_API_KEY=xxx');
          console.log('Or use: npm run setup (interactive setup)');
          process.exit(1);
        }
        
        await secretManager.initConfig(apiKeys);
        break;
        
      case 'list':
        await secretManager.listEngines();
        break;
        
      case 'get':
        if (!args[0]) {
          console.error('Usage: npm run key:get <engine>');
          console.error('Engines: bailian, tavily, serper, exa, firecrawl');
          process.exit(1);
        }
        const key = await secretManager.getEngineKey(args[0]);
        console.log(key);
        break;
        
      case 'status':
        await secretManager.showStatus();
        break;
        
      case 'rotate':
        if (!args[0]) {
          console.error('Usage: npm run key:rotate <engine> [newApiKey]');
          process.exit(1);
        }
        await secretManager.rotateKey(args[0], args[1]);
        break;
        
      default:
        console.log('Usage: npm run key:<command>');
        console.log('Commands:');
        console.log('  key:init    - Initialize from environment variables');
        console.log('  key:list    - List all configured engines');
        console.log('  key:get     - Get API key for an engine');
        console.log('  key:status  - Show detailed status');
        console.log('  key:rotate  - Rotate or toggle an engine key');
        console.log('');
        console.log('Examples:');
        console.log('  npm run key:get bailian');
        console.log('  npm run key:rotate bailian');
    }
  } catch (error) {
    console.error('❌ Error:', (error as Error).message);
    process.exit(1);
  }
}

main();
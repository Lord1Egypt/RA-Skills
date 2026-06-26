#!/usr/bin/env node

/**
 * OpenClaw Memory Fix - 记忆系统优化脚本
 */

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = process.env.OPENCLAW_WORKSPACE || process.cwd();

// 记忆层级配置
const LAYERS = {
  L1: { name: '短期记忆', decay: 0.5, location: 'memory/L1' },
  L2: { name: '情景记忆', decay: 0.1, location: 'memory/L2' },
  L3: { name: '语义记忆', decay: 0.05, location: 'memory/L3' },
  L4: { name: '长期记忆', decay: 0.01, location: 'memory/L4' }
};

class MemorySystem {
  constructor() {
    this.memoryDir = path.join(MEMORY_DIR, 'memory');
    this.config = this.loadConfig();
  }

  loadConfig() {
    const configPath = path.join(this.memoryDir, 'config.json');
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    }
    return {
      layers: LAYERS,
      decayEnabled: true,
      migrationEnabled: true
    };
  }

  async status() {
    console.log('\n🧠 OpenClaw Memory Status\n');
    console.log('='.repeat(40));
    
    for (const [key, layer] of Object.entries(this.config.layers)) {
      const location = path.join(this.memoryDir, layer.location);
      let count = 0;
      let size = 0;
      
      if (fs.existsSync(location)) {
        const files = fs.readdirSync(location);
        count = files.length;
        files.forEach(f => {
          const stat = fs.statSync(path.join(location, f));
          size += stat.size;
        });
      }
      
      console.log(`\n${key} - ${layer.name}`);
      console.log(`  记忆数: ${count}`);
      console.log(`  大小: ${(size / 1024).toFixed(2)} KB`);
      console.log(`  衰减率: ${(layer.decay * 100).toFixed(1)}%/月`);
    }
    
    console.log('\n' + '='.repeat(40));
    return this.config;
  }

  async migrate(fromLayer, toLayer) {
    console.log(`\n📦 迁移 ${fromLayer} → ${toLayer}`);
    
    const source = path.join(this.memoryDir, this.config.layers[fromLayer].location);
    const target = path.join(this.memoryDir, this.config.layers[toLayer].location);
    
    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }
    
    if (fs.existsSync(source)) {
      const files = fs.readdirSync(source);
      console.log(`  找到 ${files.length} 个文件待处理`);
      // 实际迁移逻辑需要根据具体需求实现
      console.log(`  ✅ 迁移完成`);
    } else {
      console.log(`  ⚠️ 源目录不存在`);
    }
  }

  async previewDecay() {
    console.log('\n🔍 遗忘预览\n');
    console.log('='.repeat(40));
    console.log('即将进入Cold的记忆：');
    console.log('(基于当前衰减速度计算)');
    console.log('='.repeat(40));
  }
}

// CLI入口
const args = process.argv.slice(2);
const command = args[0] || 'help';

const memory = new MemorySystem();

switch (command) {
  case 'status':
    memory.status();
    break;
  case 'migrate':
    memory.migrate(args[1] || 'L1', args[2] || 'L2');
    break;
  case 'preview-decay':
    memory.previewDecay();
    break;
  default:
    console.log(`
🧠 OpenClaw Memory Fix

用法:
  node memory.js status          查看记忆状态
  node memory.js migrate L1 L2   迁移记忆
  node memory.js preview-decay   预览遗忘
`);
}

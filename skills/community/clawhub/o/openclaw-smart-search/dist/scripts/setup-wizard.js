#!/usr/bin/env ts-node
"use strict";
/**
 * API Key 配置向导
 * 使用技能的默认配置方式
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const key_manager_1 = require("../src/key-manager");
const readline = __importStar(require("readline"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
function prompt(question) {
    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            resolve(answer);
        });
    });
}
async function setupWizard() {
    console.log('🔐 Smart Search API Key Setup');
    console.log('================================\n');
    const secretManager = new key_manager_1.SecretManager();
    const engines = [
        { name: 'bailian', label: '百炼 MCP', quota: '2000 次/月' },
        { name: 'tavily', label: 'Tavily', quota: '1000 次/月' },
        { name: 'serper', label: 'Serper', quota: '2500 次/月' },
        { name: 'exa', label: 'Exa', quota: '1000 次/月' },
        { name: 'firecrawl', label: 'Firecrawl', quota: '500 页/月' }
    ];
    const keys = {};
    console.log('请选择要配置的引擎：');
    engines.forEach((engine, i) => {
        console.log(`${i + 1}. ${engine.label} (${engine.quota})`);
    });
    console.log('6. 配置所有引擎');
    console.log('7. 跳过\n');
    const choice = await prompt('请输入选项 [1-7]: ');
    let selectedEngines = [];
    if (choice === '6') {
        selectedEngines = engines;
    }
    else if (choice >= '1' && choice <= '5') {
        selectedEngines = [engines[parseInt(choice) - 1]];
    }
    else {
        console.log('👋 已跳过配置');
        console.log('\n💡 提示：');
        console.log('   运行 "npm run setup" 重新配置');
        console.log('   或运行 "npm run key:set <engine>" 配置单个引擎');
        process.exit(0);
    }
    // 逐个配置
    for (const engine of selectedEngines) {
        console.log(`\n➡️  正在配置 ${engine.label}...`);
        const apiKey = await prompt('请输入 API Key: ');
        if (apiKey.trim()) {
            keys[engine.name] = apiKey.trim();
            console.log(`✅ ${engine.label} 配置成功！`);
        }
        else {
            console.log(`⚠️  跳过 ${engine.label}`);
        }
    }
    // 生成主密钥并保存到 .env 文件
    const crypto = require('crypto');
    const masterKey = crypto.randomBytes(32).toString('base64');
    const envPath = path.join(__dirname, '..', '.env');
    fs.writeFileSync(envPath, `OPENCLAW_MASTER_KEY=${masterKey}\n`);
    console.log(`\n✅ 主密钥已生成并保存到：${envPath}`);
    // 初始化配置
    if (Object.keys(keys).length > 0) {
        await secretManager.initConfig(keys);
        console.log('\n================================');
        console.log(`✅ 配置完成！已启用 ${Object.keys(keys).length} 个引擎`);
        console.log('================================\n');
        console.log('📊 查看状态：npm run key:status');
        console.log('🧪 测试搜索：npm run search "测试"');
        console.log('\n💡 使用说明：');
        console.log('   1. 加载主密钥：source .env');
        console.log('   2. 测试搜索：npm run search "测试"');
        console.log('\n💡 安全提示：');
        console.log('   - 不要将 .env 文件提交到版本控制');
        console.log('   - 不要将加密配置文件提交到版本控制');
        console.log('   - 定期轮换 API Key');
    }
    else {
        console.log('\n⚠️  未配置任何引擎');
    }
    rl.close();
}
setupWizard().catch((error) => {
    console.error('❌ 配置失败:', error.message);
    console.log('\n💡 提示：');
    console.log('   - 确保有足够的权限写入配置文件');
    console.log('   - 检查磁盘空间是否充足');
});
//# sourceMappingURL=setup-wizard.js.map
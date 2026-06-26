#!/usr/bin/env ts-node
"use strict";
/**
 * 百炼一键配置脚本
 * 自动检测 mcporter 配置路径并配置百炼搜索
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
const child_process_1 = require("child_process");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const readline = __importStar(require("readline"));
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
function question(prompt) {
    return new Promise((resolve) => {
        rl.question(prompt, resolve);
    });
}
function detectMcporterConfigPath() {
    // 可能的配置路径
    const possiblePaths = [
        path.join(os.homedir(), '.mcporter', 'config.json'),
        path.join(os.homedir(), '.config', 'mcporter', 'config.json'),
        path.join(os.homedir(), '.mcporter.json'),
        '/etc/mcporter/config.json',
    ];
    for (const p of possiblePaths) {
        if (fs.existsSync(p)) {
            return p;
        }
    }
    // 尝试使用 mcporter 命令获取配置路径
    const result = (0, child_process_1.spawnSync)('mcporter', ['config', 'path'], {
        encoding: 'utf8',
        timeout: 5000
    });
    if (result.status === 0 && result.stdout.trim()) {
        const configPath = result.stdout.trim();
        if (fs.existsSync(configPath)) {
            return configPath;
        }
    }
    return null;
}
async function main() {
    console.log('\n🔧 百炼搜索一键配置');
    console.log('='.repeat(50));
    // 1. 检查 mcporter 是否安装
    console.log('\n📋 步骤 1: 检查 mcporter 安装');
    const mcporterCheck = (0, child_process_1.spawnSync)('which', ['mcporter'], { encoding: 'utf8', timeout: 5000 });
    if (mcporterCheck.status !== 0) {
        console.log('⚠️  mcporter 未安装');
        console.log('');
        console.log('请先安装 mcporter:');
        console.log('  npm install -g mcporter');
        console.log('');
        console.log('安装完成后，重新运行此脚本:');
        console.log('  npm run setup:bailian');
        rl.close();
        process.exit(1);
    }
    const mcporterVersion = (0, child_process_1.spawnSync)('mcporter', ['--version'], {
        encoding: 'utf8',
        timeout: 5000
    });
    console.log(`✅ mcporter 已安装: ${mcporterVersion.stdout.trim().split('\n')[0]}`);
    // 2. 检测配置路径
    console.log('\n📋 步骤 2: 检测 mcporter 配置路径');
    const configPath = detectMcporterConfigPath();
    if (configPath) {
        console.log(`✅ 找到配置文件: ${configPath}`);
    }
    else {
        console.log('⚠️  未找到现有配置文件');
        // 使用默认路径
        const defaultPath = path.join(os.homedir(), '.mcporter', 'config.json');
        console.log(`将使用默认路径: ${defaultPath}`);
    }
    // 3. 获取 API Key
    console.log('\n📋 步骤 3: 配置百炼 API Key');
    console.log('');
    console.log('获取 API Key:');
    console.log('  1. 访问 https://bailian.console.aliyun.com/');
    console.log('  2. 创建或选择应用');
    console.log('  3. 获取 API Key');
    console.log('');
    const apiKey = await question('请输入百炼 API Key: ');
    if (!apiKey || apiKey.trim().length === 0) {
        console.log('❌ API Key 不能为空');
        rl.close();
        process.exit(1);
    }
    const trimmedKey = apiKey.trim();
    // 4. 配置 mcporter
    console.log('\n📋 步骤 4: 配置 mcporter');
    const configResult = (0, child_process_1.spawnSync)('mcporter', [
        'config', 'set',
        'mcpServers.bailian.command', 'npx',
        'mcpServers.bailian.args.0', '-y',
        'mcpServers.bailian.args.1', '@alicloud/bailian-mcp-server'
    ], {
        encoding: 'utf8',
        timeout: 10000
    });
    if (configResult.status !== 0) {
        console.log('⚠️  mcporter config set 命令不可用，使用手动配置');
        console.log('');
        console.log('手动配置方法:');
        console.log('1. 编辑 mcporter 配置文件');
        console.log('2. 添加以下内容:');
        console.log('');
        console.log(JSON.stringify({
            mcpServers: {
                bailian: {
                    command: 'npx',
                    args: ['-y', '@alicloud/bailian-mcp-server'],
                    env: {
                        BAILIAN_MCP_API_KEY: '<your-api-key>'
                    }
                }
            }
        }, null, 2));
        console.log('');
        console.log('3. 设置环境变量:');
        console.log(`   export BAILIAN_MCP_API_KEY="${trimmedKey.substring(0, 8)}..."`);
    }
    else {
        console.log('✅ mcporter 配置已更新');
    }
    // 5. 保存 API Key 到 Smart Search 加密存储
    console.log('\n📋 步骤 5: 保存 API Key 到加密存储');
    // 设置环境变量用于加密
    if (!process.env.OPENCLAW_MASTER_KEY) {
        console.log('⚠️  OPENCLAW_MASTER_KEY 未设置');
        console.log('正在生成临时主密钥...');
        const generateKeyResult = (0, child_process_1.spawnSync)('openssl', ['rand', '-base64', '32'], {
            encoding: 'utf8',
            timeout: 5000
        });
        if (generateKeyResult.status === 0) {
            const masterKey = generateKeyResult.stdout.trim();
            process.env.OPENCLAW_MASTER_KEY = masterKey;
            console.log('✅ 已生成临时主密钥');
            console.log('');
            console.log('💡 建议将以下内容添加到 ~/.bashrc 或 ~/.zshrc:');
            console.log(`   export OPENCLAW_MASTER_KEY="${masterKey}"`);
        }
    }
    // 使用 key-manager 保存
    try {
        const { SecretManager } = await Promise.resolve().then(() => __importStar(require('../src/key-manager')));
        const secretManager = new SecretManager();
        await secretManager.setEngineKey('bailian', trimmedKey);
        console.log('✅ API Key 已加密保存');
    }
    catch (error) {
        console.log('⚠️  无法保存到加密存储:', error.message);
        console.log('请手动配置: npm run key:set bailian');
    }
    // 6. 验证配置
    console.log('\n📋 步骤 6: 验证配置');
    const testResult = (0, child_process_1.spawnSync)('mcporter', ['list'], {
        encoding: 'utf8',
        timeout: 10000
    });
    if (testResult.status === 0) {
        console.log('✅ mcporter 配置验证成功');
        console.log('');
        console.log('已配置的服务:');
        console.log(testResult.stdout);
    }
    else {
        console.log('⚠️  mcporter list 命令失败');
    }
    // 完成
    console.log('\n' + '='.repeat(50));
    console.log('✅ 百炼搜索配置完成！');
    console.log('');
    console.log('测试搜索:');
    console.log('  npm run search "OpenClaw" -- --engine=bailian');
    console.log('');
    console.log('如果遇到问题，请运行诊断:');
    console.log('  npm run doctor');
    console.log('');
    rl.close();
}
main().catch((error) => {
    console.error('❌ 配置失败:', error.message);
    rl.close();
    process.exit(1);
});
//# sourceMappingURL=setup-bailian.js.map
#!/usr/bin/env ts-node
"use strict";
/**
 * 设置单个引擎的 API Key
 * 用法：npm run key:set <engine>
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
const readline = __importStar(require("readline"));
const key_manager_1 = require("../src/key-manager");
const types_1 = require("../src/types");
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
async function setKey() {
    const engine = process.argv[2];
    if (!engine) {
        console.error('Usage: npm run key:set <engine>');
        console.error('Engines: bailian, tavily, serper, exa, firecrawl');
        rl.close();
        process.exit(1);
    }
    const validEngines = ['bailian', 'tavily', 'serper', 'exa', 'firecrawl'];
    if (!validEngines.includes(engine)) {
        console.error(`Invalid engine: ${engine}`);
        console.error('Valid engines: bailian, tavily, serper, exa, firecrawl');
        rl.close();
        process.exit(1);
    }
    const label = types_1.ENGINE_LABELS[engine];
    console.log(`\n🔑 Setting API Key for ${label}`);
    console.log('='.repeat(40));
    const apiKey = await prompt('Enter API Key: ');
    if (!apiKey.trim()) {
        console.error('❌ API Key cannot be empty');
        rl.close();
        process.exit(1);
    }
    const secretManager = new key_manager_1.SecretManager();
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
//# sourceMappingURL=set-key.js.map
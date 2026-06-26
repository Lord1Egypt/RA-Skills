#!/usr/bin/env ts-node
"use strict";
/**
 * 从 JSON 文件导入 API Keys
 * 用法：npm run key:import <json-file>
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
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const key_manager_1 = require("../src/key-manager");
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
        const secretManager = new key_manager_1.SecretManager();
        await secretManager.initConfig(apiKeys);
        console.log(`\n✅ Imported ${Object.keys(apiKeys).length} API Keys from ${path.basename(filePath)}`);
        console.log('View status: npm run key:status');
    }
    catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}
importKeys();
//# sourceMappingURL=import-keys.js.map
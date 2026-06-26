"use strict";
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
exports.SerperEngine = void 0;
const key_manager_1 = require("../key-manager");
const sanitize_1 = require("../utils/sanitize");
const https = __importStar(require("https"));
/**
 * Serper 搜索引擎适配器
 * API 文档: https://serper.dev/api
 * 提供谷歌搜索结果
 */
class SerperEngine {
    constructor() {
        this.name = 'serper';
        this.secretManager = new key_manager_1.SecretManager();
        this.baseUrl = 'google.serper.dev';
        this.timeout = 15000;
    }
    async search(query, options) {
        // 验证和清理输入
        const safeQuery = (0, sanitize_1.validateSearchQuery)(query);
        const count = Math.min(options.count || 5, 10);
        // 获取 API Key
        let apiKey;
        try {
            apiKey = await this.secretManager.getEngineKey('serper');
        }
        catch (error) {
            throw new Error(`Serper API Key 未配置。请运行: npm run key:set serper`);
        }
        // 调用 Serper API
        const requestBody = JSON.stringify({
            q: safeQuery,
            num: count,
        });
        return new Promise((resolve, reject) => {
            const req = https.request({
                hostname: this.baseUrl,
                port: 443,
                path: '/search',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-KEY': apiKey,
                    'Content-Length': Buffer.byteLength(requestBody),
                },
                timeout: this.timeout,
            }, (res) => {
                let data = '';
                res.on('data', (chunk) => (data += chunk));
                res.on('end', () => {
                    try {
                        if (res.statusCode !== 200) {
                            const errorData = JSON.parse(data);
                            reject(new Error(`Serper API 错误 (${res.statusCode}): ${errorData.message || '未知错误'}`));
                            return;
                        }
                        const response = JSON.parse(data);
                        const results = [];
                        // 处理 organic 结果（网页搜索）
                        if (response.organic) {
                            for (const item of response.organic) {
                                results.push({
                                    title: item.title || '',
                                    url: item.link || '',
                                    snippet: item.snippet || '',
                                    engine: 'serper',
                                    originalScore: 0.85,
                                });
                            }
                        }
                        console.log(`[Serper] 成功: ${results.length} 结果`);
                        resolve(results);
                    }
                    catch (parseError) {
                        reject(new Error(`Serper 响应解析错误: ${parseError.message}`));
                    }
                });
            });
            req.on('error', (err) => {
                reject(new Error(`Serper 请求失败: ${err.message}`));
            });
            req.on('timeout', () => {
                req.destroy();
                reject(new Error(`Serper 请求超时 (${this.timeout}ms)`));
            });
            req.write(requestBody);
            req.end();
        });
    }
    async checkQuota() {
        // Serper 免费版: 2500 次/月
        // API 不提供实时配额查询，返回理论值
        return {
            used: 0, // 无法查询实际使用量
            limit: 2500,
            remaining: 2500,
        };
    }
}
exports.SerperEngine = SerperEngine;
//# sourceMappingURL=serper.js.map
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
exports.TavilyEngine = void 0;
const key_manager_1 = require("../key-manager");
const sanitize_1 = require("../utils/sanitize");
const https = __importStar(require("https"));
/**
 * Tavily 搜索引擎适配器
 * API 文档: https://docs.tavily.com/docs/tavily-api/rest-api#search
 */
class TavilyEngine {
    constructor() {
        this.name = 'tavily';
        this.secretManager = new key_manager_1.SecretManager();
        this.baseUrl = 'api.tavily.com';
        this.timeout = 15000;
    }
    async search(query, options) {
        // 验证和清理输入
        const safeQuery = (0, sanitize_1.validateSearchQuery)(query);
        const count = Math.min(options.count || 5, 10);
        // 获取 API Key
        let apiKey;
        try {
            apiKey = await this.secretManager.getEngineKey('tavily');
        }
        catch (error) {
            throw new Error(`Tavily API Key 未配置。请运行: npm run key:set tavily`);
        }
        // 调用 Tavily API
        const requestBody = JSON.stringify({
            query: safeQuery,
            max_results: count,
            search_depth: options.intent === 'academic' ? 'advanced' : 'basic',
            include_answer: false,
            include_raw_content: false,
            include_images: false,
        });
        return new Promise((resolve, reject) => {
            const req = https.request({
                hostname: this.baseUrl,
                port: 443,
                path: '/search',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`,
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
                            reject(new Error(`Tavily API 错误 (${res.statusCode}): ${errorData.detail || errorData.message || '未知错误'}`));
                            return;
                        }
                        const response = JSON.parse(data);
                        const results = (response.results || []).map((item) => ({
                            title: item.title || '',
                            url: item.url || '',
                            snippet: item.content || item.snippet || '',
                            engine: 'tavily',
                            originalScore: item.score || 0.8,
                        }));
                        console.log(`[Tavily] 成功: ${results.length} 结果`);
                        resolve(results);
                    }
                    catch (parseError) {
                        reject(new Error(`Tavily 响应解析错误: ${parseError.message}`));
                    }
                });
            });
            req.on('error', (err) => {
                reject(new Error(`Tavily 请求失败: ${err.message}`));
            });
            req.on('timeout', () => {
                req.destroy();
                reject(new Error(`Tavily 请求超时 (${this.timeout}ms)`));
            });
            req.write(requestBody);
            req.end();
        });
    }
    async checkQuota() {
        // Tavily 免费版: 1000 次/月
        // API 不提供实时配额查询，返回理论值
        return {
            used: 0, // 无法查询实际使用量
            limit: 1000,
            remaining: 1000,
        };
    }
}
exports.TavilyEngine = TavilyEngine;
//# sourceMappingURL=tavily.js.map
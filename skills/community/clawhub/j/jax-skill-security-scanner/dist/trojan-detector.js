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
exports.TrojanDetector = void 0;
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
class TrojanDetector {
    constructor() {
        this.highRiskPatterns = [
            // 网络通信后门
            { pattern: /net\.createServer|net\.connect|net\.Socket/i, description: '网络服务器/客户端创建' },
            { pattern: /http\.createServer|http\.request|https\.request/i, description: 'HTTP服务器/请求' },
            { pattern: /ws\.Server|socket\.io|WebSocketServer/i, description: 'WebSocket服务器' },
            { pattern: /dgram\.createSocket|udp\.Socket/i, description: 'UDP套接字' },
            // 文件系统恶意操作
            { pattern: /fs\.writeFileSync.*process\.env|fs\.writeFile.*password|fs\.writeFile.*key/i, description: '敏感信息写入文件' },
            { pattern: /fs\.readFile.*\.ssh|fs\.readFile.*\.aws|fs\.readFile.*credential/i, description: '读取敏感凭证文件' },
            { pattern: /fs\.unlink.*system|fs\.rm.*critical|fs\.unlink.*important/i, description: '删除系统关键文件' },
            // 进程控制系统
            { pattern: /child_process\.spawn.*sh.*-c|child_process\.exec.*curl.*http/i, description: '执行远程命令' },
            { pattern: /process\.kill.*all|child_process\.spawn.*kill.*-9/i, description: '强制终止进程' },
            { pattern: /require\('child_process'\)\.exec.*eval|Function.*child_process/i, description: '动态执行进程命令' },
            // 数据外传加密
            { pattern: /crypto\.createCipher.*process\.env|crypto\.encrypt.*key/i, description: '使用环境变量加密' },
            { pattern: /Buffer\.from.*http|Buffer\.toString.*base64.*http/i, description: 'Base64编码后外传' },
            // 代码混淆隐藏
            { pattern: /eval\(.*require|Function\(.*process/i, description: '动态加载模块' },
            { pattern: /\\x[0-9a-f]{2}/gi, description: '十六进制编码字符串' },
            { pattern: /atob\(|btoa\(/i, description: 'Base64编解码' },
            // 持久化机制
            { pattern: /require\('os'\)\.platform|process\.platform.*if.*win/i, description: '平台检测后执行不同代码' },
            { pattern: /setInterval.*1000.*60.*24|setTimeout.*86400000/i, description: '长时间定时任务' },
            // 组合模式（高风险）
            { pattern: /net\.createServer.*fs\.readFile|http\.createServer.*child_process/i, description: '网络+文件/进程组合' },
            { pattern: /crypto.*http.*child_process/i, description: '加密+网络+进程组合' }
        ];
        this.mediumRiskPatterns = [
            // 潜在危险操作
            { pattern: /require\('os'\)\.cpus|require\('os'\)\.totalmem/i, description: '系统信息收集' },
            { pattern: /fs\.readdir.*home|fs\.readdir.*user/i, description: '读取用户目录' },
            { pattern: /process\.env\..*KEY|process\.env\..*SECRET/i, description: '访问敏感环境变量' },
            { pattern: /JSON\.parse.*http|JSON\.stringify.*http/i, description: 'HTTP JSON数据处理' },
            // 网络相关
            { pattern: /fetch\(|axios\(|request\(/i, description: 'HTTP请求库' },
            { pattern: /dns\.lookup|dns\.resolve/i, description: 'DNS解析' },
            // 文件操作
            { pattern: /fs\.watch|fs\.watchFile/i, description: '文件监控' },
            { pattern: /fs\.stat.*\.log|fs\.stat.*\.txt/i, description: '检查日志文件' }
        ];
    }
    async scanSkill(skillPath) {
        const files = await this.collectAllFiles(skillPath);
        const suspiciousFiles = [];
        const detectedPatterns = new Set();
        let hasHighRisk = false;
        let hasMediumRisk = false;
        for (const file of files) {
            const fileResult = await this.scanFile(file, skillPath);
            if (fileResult.patterns.length > 0) {
                suspiciousFiles.push({
                    file: path.relative(skillPath, file),
                    patterns: fileResult.patterns,
                    riskLevel: fileResult.riskLevel
                });
                fileResult.patterns.forEach(pattern => detectedPatterns.add(pattern));
                if (fileResult.riskLevel === 'high') {
                    hasHighRisk = true;
                }
                else if (fileResult.riskLevel === 'medium') {
                    hasMediumRisk = true;
                }
            }
        }
        // 确定整体风险等级
        let riskLevel = 'low';
        if (hasHighRisk) {
            riskLevel = 'high';
        }
        else if (hasMediumRisk || suspiciousFiles.length > 0) {
            riskLevel = 'medium';
        }
        return {
            hasTrojan: hasHighRisk,
            riskLevel,
            detectedPatterns: Array.from(detectedPatterns),
            suspiciousFiles
        };
    }
    async collectAllFiles(skillPath) {
        const files = [];
        async function collect(dir) {
            try {
                const entries = await fs.readdir(dir, { withFileTypes: true });
                for (const entry of entries) {
                    const fullPath = path.join(dir, entry.name);
                    if (entry.isDirectory()) {
                        // 跳过常见的不需要扫描的目录
                        if (!['node_modules', '.git', 'dist', 'build', 'test', '__tests__'].includes(entry.name)) {
                            await collect(fullPath);
                        }
                    }
                    else if (entry.isFile()) {
                        // 扫描所有文本文件
                        const ext = path.extname(entry.name).toLowerCase();
                        if (['.js', '.ts', '.json', '.md', '.txt', '.sh', '.bat', '.ps1', '.yml', '.yaml'].includes(ext)) {
                            files.push(fullPath);
                        }
                    }
                }
            }
            catch (error) {
                // 忽略无法访问的目录
            }
        }
        await collect(skillPath);
        return files;
    }
    async scanFile(filePath, skillPath) {
        try {
            const content = await fs.readFile(filePath, 'utf-8');
            const patterns = [];
            let hasHighRiskPattern = false;
            let hasMediumRiskPattern = false;
            // 检查高风险模式
            for (const { pattern, description } of this.highRiskPatterns) {
                if (pattern.test(content)) {
                    patterns.push(description);
                    hasHighRiskPattern = true;
                }
            }
            // 检查中风险模式
            for (const { pattern, description } of this.mediumRiskPatterns) {
                if (pattern.test(content)) {
                    patterns.push(description);
                    hasMediumRiskPattern = true;
                }
            }
            // 确定文件风险等级
            let riskLevel = 'low';
            if (hasHighRiskPattern) {
                riskLevel = 'high';
            }
            else if (hasMediumRiskPattern) {
                riskLevel = 'medium';
            }
            return { patterns, riskLevel };
        }
        catch (error) {
            // 忽略无法读取的文件
            return { patterns: [], riskLevel: 'low' };
        }
    }
    // 辅助方法：获取模式描述
    getPatternDescription(pattern) {
        const allPatterns = [...this.highRiskPatterns, ...this.mediumRiskPatterns];
        const found = allPatterns.find(p => p.description === pattern);
        return found ? found.description : pattern;
    }
}
exports.TrojanDetector = TrojanDetector;
//# sourceMappingURL=trojan-detector.js.map
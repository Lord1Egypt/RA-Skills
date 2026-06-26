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
exports.PromptPoisonDetector = void 0;
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
class PromptPoisonDetector {
    constructor() {
        this.highRiskPatterns = [
            { pattern: /ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|commands?|directives?)/i, description: '尝试忽略先前指令', category: 'prompt-injection' },
            { pattern: /disregard\s+(all\s+)?(your\s+)?(instructions?|rules?|system)/i, description: '忽略系统指令', category: 'prompt-injection' },
            { pattern: /forget\s+(everything|all|your)\s+(you\s+)?(know|learn|were\s+taught)/i, description: '忘记已知信息', category: 'prompt-injection' },
            { pattern: /new\s+(instruction|rules?|system|priority).*(override|replace|instead)/i, description: '新指令覆盖', category: 'prompt-injection' },
            { pattern: /override\s+(your\s+)?(system|safety|ethical)/i, description: '覆盖安全限制', category: 'prompt-injection' },
            { pattern: /\b(jailbreak|bypass|disable\s+(safety|filter|guard))\b/i, description: '越狱/禁用安全', category: 'jailbreak' },
            { pattern: /\b(DAN|do\s+anything\s+now|developer\s+mode)\b/i, description: 'DAN越狱模式', category: 'jailbreak' },
            { pattern: /pretend\s+(to\s+)?(be|have|act\s+as)/i, description: '假装身份绕过', category: 'jailbreak' },
            { pattern: /roleplay\s+(as|with)\s+(evil|malicious|hacked)/i, description: '恶意角色扮演', category: 'jailbreak' },
            { pattern: /you\s+(are|is)\s+(now\s+)?(no\s+longer|free|unrestricted)/i, description: '解除限制声明', category: 'jailbreak' },
            { pattern: /(show|tell|reveal|extract)\s+(me\s+)?(your\s+)?(system\s+)?(prompt|instruction|configuration)/i, description: '提取系统提示', category: 'prompt-extraction' },
            { pattern: /what\s+(are|were)\s+(your\s+)?(system\s+)?(instructions?|rules?)/i, description: '询问系统指令', category: 'prompt-extraction' },
            { pattern: /read\s+(the\s+)?(content\s+)?(above|previous|earlier)\s+(carefully|exactly)/i, description: '要求仔细阅读（植入上下文）', category: 'prompt-extraction' },
            { pattern: /(system|admin|owner)\s*:\s*(ignore|bypass|override)/i, description: '伪装系统指令', category: 'context-pollution' },
            { pattern: /\{[^}]*"(system|admin|instruction)"[^}]*\}/i, description: 'JSON格式伪装指令', category: 'context-pollution' },
            { pattern: /\<(system|admin|instruction)\>.*\<\/(system|admin|instruction)\>/i, description: 'XML格式伪装指令', category: 'context-pollution' },
            { pattern: /```\s*(\w+)?\s*;?\s*(exec|eval|run)\s*\(/i, description: '代码执行指令', category: 'code-injection' },
            { pattern: /__import__\s*\(\s*['"]os['"]\)/i, description: 'Python os模块导入', category: 'code-injection' },
            { pattern: /require\s*\(\s*['"](child_process|fs|net|crypto)['"]\)/i, description: 'Node危险模块导入', category: 'code-injection' },
            { pattern: /(just\s+)?(say|write|output)\s+['"](okay|ok|yes|sure|will\s+do)['"]/i, description: '诱导确认', category: 'social-engineering' },
            { pattern: /(this\s+is\s+)?(just\s+a\s+)?(test| joke| prank)/i, description: '无害伪装', category: 'social-engineering' },
            { pattern: /confirm\s+(by\s+)?(saying|typing)\s+['"](confirm|yes|ok)['"]/i, description: '要求确认恶意操作', category: 'social-engineering' }
        ];
        this.mediumRiskPatterns = [
            { pattern: /\b(secret|password|api[_-]?key|token)\s*[:=]\s*['"][^'"]{8,}['"]/i, description: '硬编码密钥', category: 'hardcoded-secrets' },
            { pattern: /process\.env\s*\.\s*\w+(KEY|SECRET|TOKEN|PASSWORD)/i, description: '敏感环境变量访问', category: 'env-exposure' },
            { pattern: /base64\.(encode|decode)|atob|btoa/i, description: 'Base64编码操作', category: 'encoding' },
            { pattern: /eval\s*\(|Function\s*\(/i, description: '动态代码执行', category: 'dynamic-code' },
            { pattern: /you\s+(must|should|have\s+to)\s+(follow|obey|listen)/i, description: '强制服从指令', category: 'indirect-injection' },
            { pattern: /(ignore|skip|bypass)\s+(this|these)\s+(warning|error|safety)/i, description: '忽略安全警告', category: 'indirect-injection' }
        ];
    }
    async scanSkill(skillPath) {
        const files = await this.collectAllFiles(skillPath);
        const detections = [];
        const detectedPatterns = new Set();
        let hasHighRisk = false;
        let hasMediumRisk = false;
        for (const file of files) {
            const fileResult = await this.scanFile(file, skillPath);
            if (fileResult.detections.length > 0) {
                detections.push({
                    file: path.relative(skillPath, file),
                    detections: fileResult.detections,
                    riskLevel: fileResult.riskLevel
                });
                fileResult.detections.forEach(d => detectedPatterns.add(d.description));
                if (fileResult.riskLevel === 'high') {
                    hasHighRisk = true;
                }
                else if (fileResult.riskLevel === 'medium') {
                    hasMediumRisk = true;
                }
            }
        }
        const categoryStats = {};
        detections.forEach(d => {
            d.detections.forEach(det => {
                const cat = det.category;
                categoryStats[cat] = (categoryStats[cat] || 0) + 1;
            });
        });
        let riskLevel = 'low';
        if (hasHighRisk) {
            riskLevel = 'high';
        }
        else if (hasMediumRisk || detections.length > 0) {
            riskLevel = 'medium';
        }
        return {
            hasPoison: hasHighRisk,
            riskLevel,
            detectedPatterns: Array.from(detectedPatterns),
            detections,
            categoryStats
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
                        if (!['node_modules', '.git', 'dist', 'build', 'test', '__tests__'].includes(entry.name)) {
                            await collect(fullPath);
                        }
                    }
                    else if (entry.isFile()) {
                        const ext = path.extname(entry.name).toLowerCase();
                        if (['.js', '.ts', '.json', '.md', '.txt', '.sh', '.bat', '.ps1', '.yml', '.yaml', '.py', '.rb'].includes(ext)) {
                            files.push(fullPath);
                        }
                    }
                }
            }
            catch (error) {
            }
        }
        await collect(skillPath);
        return files;
    }
    async scanFile(filePath, skillPath) {
        try {
            const content = await fs.readFile(filePath, 'utf-8');
            const detections = [];
            let hasHighRiskPattern = false;
            let hasMediumRiskPattern = false;
            for (const { pattern, description, category } of this.highRiskPatterns) {
                if (pattern.test(content)) {
                    detections.push({ description, category, riskLevel: 'high' });
                    hasHighRiskPattern = true;
                }
            }
            for (const { pattern, description, category } of this.mediumRiskPatterns) {
                if (pattern.test(content)) {
                    detections.push({ description, category, riskLevel: 'medium' });
                    hasMediumRiskPattern = true;
                }
            }
            const uniqueDetections = detections.filter((v, i, a) => a.findIndex(t => t.description === v.description) === i);
            let riskLevel = 'low';
            if (hasHighRiskPattern) {
                riskLevel = 'high';
            }
            else if (hasMediumRiskPattern) {
                riskLevel = 'medium';
            }
            return { detections: uniqueDetections, riskLevel };
        }
        catch (error) {
            return { detections: [], riskLevel: 'low' };
        }
    }
}
exports.PromptPoisonDetector = PromptPoisonDetector;

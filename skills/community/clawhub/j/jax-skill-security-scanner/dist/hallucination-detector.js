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
exports.HallucinationDetector = void 0;
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
class HallucinationDetector {
    constructor() {
        this.fakeAdPatterns = [
            { pattern: /\b(100%|100%)\b/i, description: 'Absolute claim', category: 'fake-ad' },
            { pattern: /\b(\u7edd\u5bf9|\u7acb\u5373|\u9acc\u9ad8)\b.*?(\u6709\u6548|\u6210\u529f)/i, description: 'Exaggerated claim', category: 'fake-ad' },
            { pattern: /\b(\u7279\u6548|\u795e\u836f|\u4e07\u80fd)\b/i, description: 'Miracle cure claim', category: 'fake-ad' },
            { pattern: /\b(\u9650\u91cf|\u4ec5\u6b64\u4e00\u6b21)\s*(\u4f18\u60e0|\u7279\u4ef7)/i, description: 'Limited time scam', category: 'fake-ad' },
            { pattern: /\b\u6295\u8d44.*?\b(\u6708\u5165|\u65e5\u5165)\s*\d+/i, description: 'Investment scam', category: 'scam' },
            { pattern: /\b(\u9ad8\u5047|\u7cbe\u5047|A\u8d27)\b.*?(\u54c1\u724c)/i, description: 'Fake brand product', category: 'fake-product' },
            { pattern: /\u539f\u4ef7.*?\u73b0\u4ef7.*?\d+%/i, description: 'Fake discount', category: 'fake-ad' },
            { pattern: /\b(\u4e2d\u5956|\u606d\u559c|\u8fd0\u6c14)\b.*?(\u83b7\u5f97|\u8d62\u5f97)/i, description: 'Prize scam', category: 'scam' },
            { pattern: /\u60a8\u7684.*?(\u8d26\u53f7|\u8d26\u6237).*?(\u5f02\u5e38|\u51fb\u7ed3)/i, description: 'Account security scam', category: 'scam' },
            { pattern: /\b(\u70b9\u8d5e|\u8f6c\u53d1)\s*.*?\b(\u514d\u8d39|\u9001)\b/i, description: 'Like/share scam', category: 'scam' },
            { pattern: /\b(\u8272\u60c5|\u8d4c\u535a|\u6bd2\u54c1)\b.*?(\u8d2d\u4e70|\u51fa\u552e)/i, description: 'Illegal content', category: 'illegal' },
            { pattern: /\b(\u514d\u8bd5|\u5305\u8fc7)\s*(\u672c\u79d1|\u7855\u58eb)\b/i, description: 'Fake degree scam', category: 'scam' },
            { pattern: /(\u5ba2\u670d|\u4e13\u5458).*?(\u52a0\u5fae\u4fe1|\u52a0QQ)/i, description: 'Fake customer service', category: 'scam' },
        ];
        this.suspiciousPhrases = [
            { pattern: /\u4ee5\u4e0b.*?(\u63a8\u8350|\u4ecb\u7ecd)/i, description: 'Promotion content', category: 'promotion' },
            { pattern: /\u4eb2\u6d4b\u6709\u6548/i, description: 'Fake review', category: 'fake-review' },
            { pattern: /\u6ce8\u518c.*?\u9001.*?(\u73b0\u91d1|\u7ea2\u5305)/i, description: 'Registration scam', category: 'scam' },
            { pattern: /\u5237\u5355|\u5237\u6d41\u91cf/i, description: 'Fake traffic', category: 'violation' },
        ];
    }
    async scanText(text) {
        const detections = [];
        let hasHighRisk = false;
        let hasMediumRisk = false;
        for (const { pattern, description, category } of this.fakeAdPatterns) {
            const matches = text.match(pattern);
            if (matches) {
                detections.push({ type: 'high-risk', description, category, matched: matches[0].substring(0, 100), severity: 'high' });
                hasHighRisk = true;
            }
        }
        for (const { pattern, description, category } of this.suspiciousPhrases) {
            const matches = text.match(pattern);
            if (matches) {
                detections.push({ type: 'suspicious', description, category, matched: matches[0].substring(0, 100), severity: 'medium' });
                hasMediumRisk = true;
            }
        }
        const categoryStats = {};
        detections.forEach(d => { categoryStats[d.category] = (categoryStats[d.category] || 0) + 1; });
        let riskLevel = 'low';
        if (hasHighRisk) riskLevel = 'high';
        else if (hasMediumRisk) riskLevel = 'medium';
        const suggestions = this.generateSuggestions(detections);
        return { hasHallucination: hasHighRisk, riskLevel, detections, categoryStats, suggestions, summary: this.generateSummary(detections) };
    }
    generateSuggestions(detections) {
        const suggestions = [];
        const categories = new Set(detections.map(d => d.category));
        if (categories.has('scam')) suggestions.push('[HIGH RISK] Scam detected! Do not trust, do not transfer money.');
        if (categories.has('illegal')) suggestions.push('[HIGH RISK] Illegal content detected.');
        if (categories.has('fake-ad')) suggestions.push('[WARNING] Fake advertisement detected.');
        if (categories.has('fake-product')) suggestions.push('[WARNING] Suspicious product detected.');
        if (categories.has('promotion')) suggestions.push('[INFO] Contains promotional content.');
        if (suggestions.length === 0) suggestions.push('[OK] No obvious fake information detected.');
        return suggestions;
    }
    generateSummary(detections) {
        const highCount = detections.filter(d => d.severity === 'high').length;
        const mediumCount = detections.filter(d => d.severity === 'medium').length;
        if (highCount > 0) return `Detected ${highCount} high-risk, ${mediumCount} suspicious content`;
        if (mediumCount > 0) return `Detected ${mediumCount} suspicious content`;
        return 'No fake information detected';
    }
    async scanSkill(skillPath) {
        const files = await this.collectAllFiles(skillPath);
        const detections = [];
        for (const file of files) {
            const fileResult = await this.scanFile(file);
            if (fileResult.detections.length > 0) {
                detections.push({ file: path.relative(skillPath, file), detections: fileResult.detections, riskLevel: fileResult.riskLevel });
            }
        }
        const allDetections = detections.flatMap(d => d.detections);
        let riskLevel = 'low';
        if (allDetections.some(d => d.severity === 'high')) riskLevel = 'high';
        else if (allDetections.some(d => d.severity === 'medium')) riskLevel = 'medium';
        return { hasHallucination: riskLevel !== 'low', riskLevel, detections, fileCount: files.length };
    }
    async collectAllFiles(skillPath) {
        const files = [];
        async function collect(dir) {
            try {
                const entries = await fs.readdir(dir, { withFileTypes: true });
                for (const entry of entries) {
                    const fullPath = path.join(dir, entry.name);
                    if (entry.isDirectory()) {
                        if (!['node_modules', '.git', 'dist', 'build'].includes(entry.name)) await collect(fullPath);
                    }
                    else if (entry.isFile()) {
                        const ext = path.extname(entry.name).toLowerCase();
                        if (['.js', '.ts', '.md', '.txt', '.json'].includes(ext)) files.push(fullPath);
                    }
                }
            } catch (error) { }
        }
        await collect(skillPath);
        return files;
    }
    async scanFile(filePath) {
        try {
            const content = await fs.readFile(filePath, 'utf-8');
            const detections = [];
            for (const { pattern, description, category } of this.fakeAdPatterns) {
                if (pattern.test(content)) detections.push({ description, category, severity: 'high' });
            }
            for (const { pattern, description, category } of this.suspiciousPhrases) {
                if (pattern.test(content)) detections.push({ description, category, severity: 'medium' });
            }
            let riskLevel = 'low';
            if (detections.some(d => d.severity === 'high')) riskLevel = 'high';
            else if (detections.some(d => d.severity === 'medium')) riskLevel = 'medium';
            return { detections, riskLevel };
        } catch (error) {
            return { detections: [], riskLevel: 'low' };
        }
    }
}
exports.HallucinationDetector = HallucinationDetector;

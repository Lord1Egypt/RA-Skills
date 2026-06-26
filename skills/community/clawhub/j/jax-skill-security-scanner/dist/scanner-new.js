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
exports.SkillScanner = void 0;
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
const trojan_detector_js_1 = require("./trojan-detector.js");
class SkillScanner {
    constructor(scanPath, sensitiveKeywords) {
        this.scanPath = scanPath;
        this.sensitiveKeywords = sensitiveKeywords || [
            'exec', 'shell', 'rm', 'delete', 'format', 'shutdown', 'reboot',
            'sudo', 'chmod', 'chown', 'kill', 'uninstall', 'drop', 'truncate',
            'format', 'wipe', 'erase', 'overwrite', 'dd', 'mkfs', 'fdisk',
            'eval', 'Function', 'require', 'import', 'child_process', 'spawn',
            'execFile', 'fork', 'execSync', 'spawnSync', 'execFileSync'
        ];
        this.trojanDetector = new trojan_detector_js_1.TrojanDetector();
    }
    async scan() {
        const skills = await this.scanSkillsDirectory();
        const skillReports = [];
        for (const skill of skills) {
            const report = await this.analyzeSkill(skill);
            skillReports.push(report);
        }
        return this.generateReport(skillReports);
    }
    async scanSkillsDirectory() {
        try {
            const entries = await fs.readdir(this.scanPath, { withFileTypes: true });
            return entries
                .filter(entry => entry.isDirectory())
                .map(entry => path.join(this.scanPath, entry.name));
        }
        catch (error) {
            console.error(`无法读取技能目录: ${this.scanPath}`, error);
            return [];
        }
    }
    async analyzeSkill(skillPath) {
        const skillName = path.basename(skillPath);
        const files = await this.collectSkillFiles(skillPath);
        const issues = [];
        const filesScanned = [];
        for (const file of files) {
            const fileIssues = await this.analyzeFile(file, skillPath);
            if (fileIssues.length > 0) {
                issues.push(...fileIssues);
                filesScanned.push(path.relative(skillPath, file));
            }
        }
        // 运行木马检测
        const trojanDetection = await this.trojanDetector.scanSkill(skillPath);
        // 评估可信度
        const trustLevel = this.evaluateTrustLevel(skillName, skillPath);
        // 确定风险等级（结合功能风险和可信度）
        const riskLevel = this.determineRiskLevel(issues, trojanDetection, trustLevel);
        return {
            skillName,
            skillPath,
            riskLevel,
            trustLevel,
            sensitiveOperations: [...new Set(issues.map(issue => issue.operation))],
            filesScanned,
            issues,
            trojanDetection
        };
    }
    evaluateTrustLevel(skillName, skillPath) {
        // 官方技能白名单（OpenClaw团队维护）
        const officialSkills = [
            '1password', 'apple-notes', 'apple-reminders', 'bear-notes', 'bird',
            'blogwatcher', 'blucli', 'bluebubbles', 'camsnap', 'clawdhub',
            'coding-agent', 'eightctl', 'food-order', 'gemini', 'gifgrep',
            'github', 'gog', 'goplaces', 'himalaya', 'imsg', 'local-places',
            'mcporter', 'model-usage', 'nano-banana-pro', 'nano-pdf', 'notion',
            'obsidian', 'openai-image-gen', 'openai-whisper', 'openai-whisper-api',
            'openhue', 'oracle', 'ordercli', 'peekaboo', 'sag', 'session-logs',
            'skill-creator', 'slack', 'songsee', 'sonoscli', 'spotify-player',
            'summarize', 'things-mac', 'tmux', 'trello', 'video-frames',
            'voice-call', 'wacli', 'weather', 'browser'
        ];
        // 判断是否为官方技能
        const isOfficial = officialSkills.includes(skillName);
        // 判断是否为系统路径（OpenClaw安装目录）
        const isSystemPath = skillPath.includes('openclaw-cn') || skillPath.includes('openclaw');
        if (isOfficial && isSystemPath) {
            return 'high'; // 官方技能，高可信度
        }
        else if (isSystemPath) {
            return 'medium'; // 系统目录但不在官方白名单，中可信度
        }
        else {
            return 'low'; // 第三方或未知来源，低可信度
        }
    }
    async collectSkillFiles(skillPath) {
        const files = [];
        async function collect(dir) {
            try {
                const entries = await fs.readdir(dir, { withFileTypes: true });
                for (const entry of entries) {
                    const fullPath = path.join(dir, entry.name);
                    if (entry.isDirectory()) {
                        // 跳过node_modules等目录
                        if (!['node_modules', '.git', 'dist', 'build'].includes(entry.name)) {
                            await collect(fullPath);
                        }
                    }
                    else if (entry.isFile()) {
                        // 只检查相关文件类型
                        const ext = path.extname(entry.name).toLowerCase();
                        if (['.md', '.js', '.ts', '.json', '.sh', '.bat', '.ps1'].includes(ext) ||
                            entry.name === 'package.json' || entry.name === 'SKILL.md') {
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
    async analyzeFile(filePath, skillPath) {
        const issues = [];
        try {
            const content = await fs.readFile(filePath, 'utf8');
            const lines = content.split('\n');
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                for (const keyword of this.sensitiveKeywords) {
                    if (line.includes(keyword)) {
                        issues.push({
                            file: path.relative(skillPath, filePath),
                            line: i + 1,
                            operation: keyword,
                            context: line.trim().substring(0, 100)
                        });
                        break; // 每行只报告一个敏感操作
                    }
                }
            }
        }
        catch (error) {
            // 忽略无法读取的文件
        }
        return issues;
    }
    determineRiskLevel(issues, trojanDetection, trustLevel) {
        // 木马检测结果优先
        if (trojanDetection.hasTrojan || trojanDetection.riskLevel === 'high') {
            return 'high';
        }
        if (trojanDetection.riskLevel === 'medium') {
            return 'medium';
        }
        // 基于敏感操作数量确定风险等级
        const highRiskOps = ['exec', 'shell', 'rm', 'delete', 'format', 'shutdown', 'reboot', 'sudo'];
        const mediumRiskOps = ['chmod', 'chown', 'kill', 'uninstall', 'eval', 'Function'];
        const highRiskCount = issues.filter(issue => highRiskOps.includes(issue.operation)).length;
        const mediumRiskCount = issues.filter(issue => mediumRiskOps.includes(issue.operation)).length;
        let riskLevelFromOps = 'low';
        if (highRiskCount > 0) {
            riskLevelFromOps = 'high';
        }
        else if (mediumRiskCount > 0 || issues.length > 3) {
            riskLevelFromOps = 'medium';
        }
        else {
            riskLevelFromOps = 'low';
        }
        // 根据可信度调整风险等级
        if (trustLevel === 'low' && riskLevelFromOps === 'high') {
            return 'critical'; // 高风险操作 + 低可信度 = 严重风险
        }
        else if (trustLevel === 'low' && riskLevelFromOps === 'medium') {
            return 'high'; // 中风险操作 + 低可信度 = 高风险
        }
        else if (trustLevel === 'medium' && riskLevelFromOps === 'high') {
            return 'high'; // 高风险操作 + 中可信度 = 高风险
        }
        return riskLevelFromOps;
    }
    generateReport(skillReports) {
        const highRiskCount = skillReports.filter(r => r.riskLevel === 'high' || r.riskLevel === 'critical').length;
        const mediumRiskCount = skillReports.filter(r => r.riskLevel === 'medium').length;
        const lowRiskCount = skillReports.filter(r => r.riskLevel === 'low').length;
        const criticalRiskCount = skillReports.filter(r => r.riskLevel === 'critical').length;
        const trojanHighRisk = skillReports.filter(r => r.trojanDetection.riskLevel === 'high').length;
        const trojanMediumRisk = skillReports.filter(r => r.trojanDetection.riskLevel === 'medium').length;
        const suspiciousFiles = skillReports.reduce((count, report) => count + report.trojanDetection.suspiciousFiles.length, 0);
        return {
            timestamp: new Date().toISOString(),
            scanPath: this.scanPath,
            totalSkills: skillReports.length,
            skills: skillReports,
            summary: {
                highRiskCount,
                mediumRiskCount,
                lowRiskCount,
                criticalRiskCount,
                trojanDetectionSummary: {
                    totalScanned: skillReports.length,
                    highRisk: trojanHighRisk,
                    mediumRisk: trojanMediumRisk,
                    suspiciousFiles
                }
            }
        };
    }
}
exports.SkillScanner = SkillScanner;
//# sourceMappingURL=scanner.js.map
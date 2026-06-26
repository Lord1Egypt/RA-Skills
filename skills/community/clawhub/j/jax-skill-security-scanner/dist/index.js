"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TrojanDetector = exports.SecurityReporter = exports.SkillScanner = void 0;
exports.default = register;
const scanner_js_1 = require("./scanner.js");
Object.defineProperty(exports, "SkillScanner", { enumerable: true, get: function () { return scanner_js_1.SkillScanner; } });
const reporter_js_1 = require("./reporter.js");
Object.defineProperty(exports, "SecurityReporter", { enumerable: true, get: function () { return reporter_js_1.SecurityReporter; } });
const trojan_detector_js_1 = require("./trojan-detector.js");
Object.defineProperty(exports, "TrojanDetector", { enumerable: true, get: function () { return trojan_detector_js_1.TrojanDetector; } });
/**
 * OpenClaw技能安全扫描插件
 */
function register(api) {
    const logger = api.logger.child({ plugin: 'skill-security-scanner' });
    // 注册工具
    api.registerTool({
        name: 'skill_security_scan',
        description: '扫描OpenClaw技能目录并生成安全报告',
        parameters: {
            type: 'object',
            properties: {
                scanPath: {
                    type: 'string',
                    description: '要扫描的技能目录路径（可选，使用插件配置的默认路径）'
                },
                outputFormat: {
                    type: 'string',
                    enum: ['text', 'json', 'markdown'],
                    description: '输出格式',
                    default: 'text'
                }
            }
        },
        handler: async (params, context) => {
            try {
                const config = api.config.plugins?.entries?.['skill-security-scanner']?.config || {};
                const scanPath = params.scanPath || config.scanPath ||
                    'C:\\Users\\Administrator\\AppData\\Roaming\\npm\\node_modules\\openclaw-cn\\skills';
                const outputFormat = params.outputFormat || 'text';
                logger.info(`开始扫描技能目录: ${scanPath}`);
                // 扫描技能目录
                const scanner = new scanner_js_1.SkillScanner(scanPath, config.sensitiveKeywords);
                const report = await scanner.scan();
                // 生成报告
                const reporter = new reporter_js_1.SecurityReporter(report);
                let output;
                switch (outputFormat) {
                    case 'json':
                        output = reporter.generateJsonReport();
                        break;
                    case 'markdown':
                        output = reporter.generateMarkdownReport();
                        break;
                    case 'text':
                    default:
                        output = reporter.generateTextReport();
                        break;
                }
                logger.info(`扫描完成，共扫描${report.totalSkills}个技能`);
                return {
                    success: true,
                    report: output,
                    summary: {
                        totalSkills: report.totalSkills,
                        highRisk: report.summary.highRiskCount,
                        mediumRisk: report.summary.mediumRiskCount,
                        lowRisk: report.summary.lowRiskCount
                    }
                };
            }
            catch (error) {
                logger.error(`安全扫描失败: ${error.message}`, { error });
                return {
                    success: false,
                    error: error.message
                };
            }
        }
    });
    logger.info('技能安全扫描插件已注册');
}
//# sourceMappingURL=index.js.map
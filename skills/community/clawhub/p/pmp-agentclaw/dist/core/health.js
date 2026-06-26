"use strict";
/**
 * Project Health Check
 * Monitors project document completeness and freshness
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
exports.OPTIONAL_DOCUMENTS = exports.REQUIRED_DOCUMENTS = void 0;
exports.checkHealth = checkHealth;
exports.formatHealthMarkdown = formatHealthMarkdown;
exports.formatHealthJson = formatHealthJson;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
exports.REQUIRED_DOCUMENTS = [
    'project-charter.md',
    'wbs.md',
    'risk-register.md',
    'gantt-schedule.md',
    'raci-matrix.md',
];
exports.OPTIONAL_DOCUMENTS = [
    'communications-plan.md',
    'stakeholder-register.md',
    'evm-dashboard.md',
    'change-request.md',
    'lessons-learned.md',
];
/**
 * Run project health check
 */
function checkHealth(input) {
    const { projectDir, maxRiskRegisterAge = 7 } = input;
    const checks = [];
    let issues = 0;
    let warnings = 0;
    // Check required documents
    for (const doc of exports.REQUIRED_DOCUMENTS) {
        const filePath = path.join(projectDir, doc);
        if (fs.existsSync(filePath)) {
            checks.push({
                name: doc,
                status: 'pass',
                message: 'Found',
            });
        }
        else {
            checks.push({
                name: doc,
                status: 'fail',
                message: 'Missing',
            });
            issues++;
        }
    }
    // Check optional documents
    for (const doc of exports.OPTIONAL_DOCUMENTS) {
        const filePath = path.join(projectDir, doc);
        if (fs.existsSync(filePath)) {
            checks.push({
                name: doc,
                status: 'pass',
                message: 'Found',
            });
        }
        else {
            checks.push({
                name: doc,
                status: 'warn',
                message: 'Not found (optional)',
            });
            warnings++;
        }
    }
    // Check risk register freshness
    const riskRegisterPath = path.join(projectDir, 'risk-register.md');
    if (fs.existsSync(riskRegisterPath)) {
        const stats = fs.statSync(riskRegisterPath);
        const ageDays = (Date.now() - stats.mtime.getTime()) / (1000 * 60 * 60 * 24);
        if (ageDays > maxRiskRegisterAge) {
            checks.push({
                name: 'Risk register freshness',
                status: 'warn',
                message: `Not updated in ${Math.floor(ageDays)} days`,
                details: `Last updated: ${stats.mtime.toISOString().split('T')[0]}`,
            });
            warnings++;
        }
        else {
            checks.push({
                name: 'Risk register freshness',
                status: 'pass',
                message: `Current (${Math.floor(ageDays)} days old)`,
            });
        }
    }
    // Determine overall status
    let status;
    if (issues > 0) {
        status = 'RED';
    }
    else if (warnings > 2) {
        status = 'AMBER';
    }
    else {
        status = 'GREEN';
    }
    return {
        status,
        issues,
        warnings,
        checks,
        timestamp: new Date().toISOString(),
    };
}
/**
 * Format health check as Markdown
 */
function formatHealthMarkdown(result) {
    const emoji = result.status === 'GREEN' ? '🟢' : result.status === 'AMBER' ? '🟡' : '🔴';
    let md = `# Project Health Check\n\n`;
    md += `**Status:** ${emoji} **${result.status}**\n\n`;
    md += `**Issues:** ${result.issues} | **Warnings:** ${result.warnings}\n\n`;
    md += `**Checked:** ${result.timestamp}\n\n`;
    md += `## Checks\n\n`;
    md += `| Check | Status | Message |\n`;
    md += `|-------|--------|---------|\n`;
    for (const check of result.checks) {
        const statusEmoji = check.status === 'pass' ? '✅' : check.status === 'warn' ? '⚠️' : '❌';
        md += `| ${check.name} | ${statusEmoji} ${check.status} | ${check.message} |\n`;
    }
    return md;
}
/**
 * Format health check as JSON
 */
function formatHealthJson(result) {
    return JSON.stringify(result, null, 2);
}
//# sourceMappingURL=health.js.map
#!/usr/bin/env node
"use strict";
/**
 * CLI: Score project risks
 * Usage: score-risks <probability 1-5> <impact 1-5> [--json]
 * Or: score-risks --file <risks.json>
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
const risk_1 = require("../core/risk");
const fs = __importStar(require("fs"));
function main() {
    const args = process.argv.slice(2);
    // Check for file input
    const fileIndex = args.indexOf('--file');
    if (fileIndex !== -1) {
        const filePath = args[fileIndex + 1];
        if (!filePath) {
            console.error('Usage: score-risks --file <risks.json>');
            process.exit(1);
        }
        try {
            const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
            const results = (0, risk_1.scoreRisks)(data.risks || []);
            console.log(JSON.stringify(results, null, 2));
        }
        catch (err) {
            console.error('Error reading file:', err instanceof Error ? err.message : String(err));
            process.exit(1);
        }
        return;
    }
    // Parse single risk
    const values = args.filter(a => !a.startsWith('--')).map(Number);
    const format = args.includes('--markdown') ? 'markdown' : 'json';
    if (values.length !== 2 || values.some(isNaN)) {
        console.error('Usage: score-risks <probability 1-5> <impact 1-5> [--json | --markdown]');
        console.error('   Or: score-risks --file <risks.json>');
        console.error('Example: score-risks 3 4');
        process.exit(1);
    }
    const [probability, impact] = values;
    try {
        const result = (0, risk_1.scoreRisk)({
            id: 'R-CLI',
            description: 'CLI risk',
            probability: probability,
            impact: impact,
        });
        console.log(JSON.stringify(result, null, 2));
    }
    catch (err) {
        console.error('Error:', err instanceof Error ? err.message : String(err));
        process.exit(1);
    }
}
main();
//# sourceMappingURL=score-risks.js.map
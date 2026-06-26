#!/usr/bin/env node
"use strict";
/**
 * CLI: Calculate Earned Value Management (EVM) metrics
 * Usage: calc-evm <BAC> <PV> <EV> <AC> [--json | --markdown]
 */
Object.defineProperty(exports, "__esModule", { value: true });
const evm_1 = require("../core/evm");
function main() {
    const args = process.argv.slice(2);
    // Parse flags
    const format = args.includes('--markdown') ? 'markdown' : 'json';
    const values = args.filter(a => !a.startsWith('--')).map(Number);
    if (values.length !== 4 || values.some(isNaN)) {
        console.error('Usage: calc-evm <BAC> <PV> <EV> <AC> [--json | --markdown]');
        console.error('Example: calc-evm 10000 5000 4500 4800');
        process.exit(1);
    }
    const [bac, pv, ev, ac] = values;
    try {
        const result = (0, evm_1.calculateEVM)({ bac, pv, ev, ac });
        if (format === 'markdown') {
            console.log((0, evm_1.formatEVMMarkdown)(result));
        }
        else {
            console.log((0, evm_1.formatEVMJson)(result));
        }
    }
    catch (err) {
        console.error('Error:', err instanceof Error ? err.message : String(err));
        process.exit(1);
    }
}
main();
//# sourceMappingURL=calc-evm.js.map
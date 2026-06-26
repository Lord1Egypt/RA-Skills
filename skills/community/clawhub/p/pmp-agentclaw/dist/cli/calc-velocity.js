#!/usr/bin/env node
"use strict";
/**
 * CLI: Calculate sprint velocity and forecast
 * Usage: calc-velocity <points1> <points2> ... [--forecast <remaining>]
 */
Object.defineProperty(exports, "__esModule", { value: true });
const velocity_1 = require("../core/velocity");
function main() {
    const args = process.argv.slice(2);
    // Parse forecast flag
    const forecastIndex = args.indexOf('--forecast');
    const remainingPoints = forecastIndex !== -1
        ? Number(args[forecastIndex + 1])
        : undefined;
    const format = args.includes('--markdown') ? 'markdown' : 'json';
    // Get sprint points
    const sprintPoints = args
        .filter((_, i) => {
        if (forecastIndex !== -1 && (i === forecastIndex || i === forecastIndex + 1))
            return false;
        return !args[i].startsWith('--');
    })
        .map(Number)
        .filter(n => !isNaN(n));
    if (sprintPoints.length === 0) {
        console.error('Usage: calc-velocity <points1> <points2> ... [--forecast <remaining>] [--json | --markdown]');
        console.error('Example: calc-velocity 34 28 42 --forecast 200');
        process.exit(1);
    }
    try {
        const result = (0, velocity_1.calculateVelocity)({
            sprintPoints,
            remainingPoints,
        });
        if (format === 'markdown') {
            console.log((0, velocity_1.formatVelocityMarkdown)(result));
        }
        else {
            console.log((0, velocity_1.formatVelocityJson)(result));
        }
    }
    catch (err) {
        console.error('Error:', err instanceof Error ? err.message : String(err));
        process.exit(1);
    }
}
main();
//# sourceMappingURL=calc-velocity.js.map
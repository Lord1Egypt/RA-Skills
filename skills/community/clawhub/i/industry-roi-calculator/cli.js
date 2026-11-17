#!/usr/bin/env node
const { parseArgs, generateReport } = require('./src/generator.js');

const args = parseArgs(process.argv);
if (!args.industry && !args.scenario && !args.currentCost) {
  console.log('Usage: node cli.js --industry "零售" --company-size "medium" --scenario "客服" --current-cost 100 --headcount 20');
  process.exit(1);
}
console.log(generateReport(args));

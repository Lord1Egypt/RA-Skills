"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.exportCommand = void 0;
const commander_1 = require("commander");
const audit_1 = require("../../daemon/audit");
exports.exportCommand = new commander_1.Command('export')
    .description('Export audit stream')
    .option('--format <format>', 'jep or json', 'jep')
    .option('--since <date>', 'ISO date')
    .option('--agent <id>', 'filter by agent')
    .option('--output <file>', 'output file')
    .action(async (options) => {
    const audit = new audit_1.AuditStreamService();
    const events = await audit.query({
        since: options.since ? new Date(options.since) : undefined,
        agent: options.agent
    });
    const output = audit.export(options.format, events);
    if (options.output) {
        require('fs').writeFileSync(options.output, output, { mode: 0o600, flag: 'wx' });
        console.log(`Exported to ${options.output}`);
    }
    else {
        console.log(output);
    }
});
//# sourceMappingURL=export.js.map
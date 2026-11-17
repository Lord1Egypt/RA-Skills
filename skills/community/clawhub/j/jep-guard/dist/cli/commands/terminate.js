"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.terminateCommand = void 0;
const commander_1 = require("commander");
const jep_core_1 = require("../../core/jep-core");
exports.terminateCommand = new commander_1.Command('terminate')
    .description('Issue a Terminate event')
    .requiredOption('--agent <id>', 'terminator')
    .requiredOption('--target <nonce>', 'target event nonce')
    .requiredOption('--reason <reason>', 'termination reason')
    .action(async (options) => {
    const core = new jep_core_1.JEPCore(options.agent);
    const event = core.createTerminate({
        target_event: options.target,
        reason: options.reason,
        triggered_by: 'user'
    }, options.agent);
    console.log(`Terminate created: ${event.nonce}`);
});
//# sourceMappingURL=terminate.js.map
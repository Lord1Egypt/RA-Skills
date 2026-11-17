"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.judgeCommand = void 0;
const commander_1 = require("commander");
const jep_core_1 = require("../../core/jep-core");
exports.judgeCommand = new commander_1.Command('judge')
    .description('Manually issue a Judge event')
    .requiredOption('--agent <id>', 'agent/skill ID')
    .requiredOption('--action <action>', 'action name')
    .option('--target <target>', 'target')
    .action(async (options) => {
    const core = new jep_core_1.JEPCore(options.agent);
    const event = core.createJudge({
        action: options.action,
        target: options.target
    }, options.agent);
    console.log(`Judge created: ${event.nonce}`);
    console.log(`Status: ${core.getStatus(event.nonce)}`);
});
//# sourceMappingURL=judge.js.map
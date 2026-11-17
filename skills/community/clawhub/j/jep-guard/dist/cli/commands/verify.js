"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.verifyCommand = void 0;
const commander_1 = require("commander");
const jep_core_1 = require("../../core/jep-core");
exports.verifyCommand = new commander_1.Command('verify')
    .description('Issue a Verify event')
    .requiredOption('--agent <id>', 'verifier')
    .requiredOption('--target <nonce>', 'target event nonce')
    .requiredOption('--verdict <verdict>', 'approved or rejected')
    .action(async (options) => {
    const core = new jep_core_1.JEPCore(options.agent);
    const event = core.createVerify({
        target_event: options.target,
        verdict: options.verdict
    }, options.agent);
    console.log(`Verify created: ${event.nonce}`);
});
//# sourceMappingURL=verify.js.map
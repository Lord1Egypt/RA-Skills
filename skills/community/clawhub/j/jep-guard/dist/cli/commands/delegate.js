"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.delegateCommand = void 0;
const commander_1 = require("commander");
const jep_core_1 = require("../../core/jep-core");
exports.delegateCommand = new commander_1.Command('delegate')
    .description('Issue a Delegate event')
    .requiredOption('--from <id>', 'delegator')
    .requiredOption('--to <id>', 'delegatee')
    .requiredOption('--scope <scope>', 'capability scope (comma separated)')
    .action(async (options) => {
    const core = new jep_core_1.JEPCore(options.from);
    const event = core.createDelegate({
        target_agent: options.to,
        scope: options.scope.split(',')
    }, options.from);
    console.log(`Delegate created: ${event.nonce}`);
});
//# sourceMappingURL=delegate.js.map
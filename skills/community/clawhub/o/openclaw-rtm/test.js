#!/usr/bin/env node
// Manual test runner for RTM Skill
const skill = require('./index.js');
const fs = require('fs');

const fakeContext = {
    logger: console,
    registerCommand(cmd) {
        console.log('[Test Runner] Registered command:', cmd.name);
        // Export handler so we can invoke it from the command line
        module.exports.invoke = async (args) => {
            const result = await cmd.handler({
                argv: args,
                reply: async (msg) => console.log('\n--- REPLY ---\n' + msg + '\n-------------')
            });
            return result;
        }
    }
};

skill.register(fakeContext);

// Extremely rudimentary CLI for testing
const args = process.argv.slice(2);
if (args.length > 0 && module.exports.invoke) {
    module.exports.invoke(args).catch(console.error);
}

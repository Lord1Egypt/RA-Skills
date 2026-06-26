import { Command } from 'commander';
import { JEPCore } from '../../core/jep-core';

export const verifyCommand = new Command('verify')
  .description('Issue a Verify event')
  .requiredOption('--agent <id>', 'verifier')
  .requiredOption('--target <nonce>', 'target event nonce')
  .requiredOption('--verdict <verdict>', 'approved or rejected')
  .action(async (options) => {
    const core = new JEPCore(options.agent);
    const event = core.createVerify({
      target_event: options.target,
      verdict: options.verdict
    }, options.agent);
    console.log(`Verify created: ${event.nonce}`);
  });
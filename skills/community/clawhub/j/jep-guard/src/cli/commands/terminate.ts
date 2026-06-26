import { Command } from 'commander';
import { JEPCore } from '../../core/jep-core';

export const terminateCommand = new Command('terminate')
  .description('Issue a Terminate event')
  .requiredOption('--agent <id>', 'terminator')
  .requiredOption('--target <nonce>', 'target event nonce')
  .requiredOption('--reason <reason>', 'termination reason')
  .action(async (options) => {
    const core = new JEPCore(options.agent);
    const event = core.createTerminate({
      target_event: options.target,
      reason: options.reason,
      triggered_by: 'user'
    }, options.agent);
    console.log(`Terminate created: ${event.nonce}`);
  });
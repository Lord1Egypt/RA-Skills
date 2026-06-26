import { Command } from 'commander';
import { JEPCore } from '../../core/jep-core';

export const delegateCommand = new Command('delegate')
  .description('Issue a Delegate event')
  .requiredOption('--from <id>', 'delegator')
  .requiredOption('--to <id>', 'delegatee')
  .requiredOption('--scope <scope>', 'capability scope (comma separated)')
  .action(async (options) => {
    const core = new JEPCore(options.from);
    const event = core.createDelegate({
      target_agent: options.to,
      scope: options.scope.split(',')
    }, options.from);
    console.log(`Delegate created: ${event.nonce}`);
  });
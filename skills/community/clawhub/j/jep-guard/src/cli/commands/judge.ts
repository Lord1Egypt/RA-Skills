import { Command } from 'commander';
import { JEPCore } from '../../core/jep-core';

export const judgeCommand = new Command('judge')
  .description('Manually issue a Judge event')
  .requiredOption('--agent <id>', 'agent/skill ID')
  .requiredOption('--action <action>', 'action name')
  .option('--target <target>', 'target')
  .action(async (options) => {
    const core = new JEPCore(options.agent);
    const event = core.createJudge({
      action: options.action,
      target: options.target
    }, options.agent);
    console.log(`Judge created: ${event.nonce}`);
    console.log(`Status: ${core.getStatus(event.nonce)}`);
  });
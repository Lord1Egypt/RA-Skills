import { Command } from 'commander';
import { AuditStreamService } from '../../daemon/audit';

export const exportCommand = new Command('export')
  .description('Export audit stream')
  .option('--format <format>', 'jep or json', 'jep')
  .option('--since <date>', 'ISO date')
  .option('--agent <id>', 'filter by agent')
  .option('--output <file>', 'output file')
  .action(async (options) => {
    const audit = new AuditStreamService();
    const events = await audit.query({
      since: options.since ? new Date(options.since) : undefined,
      agent: options.agent
    });

    const output = audit.export(options.format as 'jep' | 'json');

    if (options.output) {
      require('fs').writeFileSync(options.output, output);
      console.log(`Exported to ${options.output}`);
    } else {
      console.log(output);
    }
  });
#!/usr/bin/env node
import { Command } from 'commander';
import { initCommand } from './commands/init';
import { daemonCommand } from './commands/daemon';
import { skillsCommand } from './commands/skills';
import { judgeCommand } from './commands/judge';
import { delegateCommand } from './commands/delegate';
import { verifyCommand } from './commands/verify';
import { terminateCommand } from './commands/terminate';
import { exportCommand } from './commands/export';
import { statusCommand } from './commands/status';
import { dashboardCommand } from './commands/dashboard';

const program = new Command();

program
  .name('jep-guard')
  .description('JEP Guard v2.0.4 — Causal Operating System for OpenClaw Skills')
  .version('2.0.4');

program.addCommand(initCommand);
program.addCommand(daemonCommand);
program.addCommand(skillsCommand);
program.addCommand(judgeCommand);
program.addCommand(delegateCommand);
program.addCommand(verifyCommand);
program.addCommand(terminateCommand);
program.addCommand(exportCommand);
program.addCommand(statusCommand);
program.addCommand(dashboardCommand);

program.parse();
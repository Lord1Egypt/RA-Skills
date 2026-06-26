#!/usr/bin/env node
import { Command } from 'commander';
import { registerInit } from './commands/init.js';
import { registerCallback } from './commands/callback.js';
import { registerSpawn } from './commands/spawn.js';
import { registerSync } from './commands/sync.js';
import { registerTrack } from './commands/track.js';
import { registerStatus } from './commands/status.js';
import { registerEval } from './commands/eval.js';
import { registerComplete } from './commands/complete.js';
import { registerHealth } from './commands/health.js';

const program = new Command();

program
  .name('nexum')
  .description('Nexum task orchestration CLI')
  .version('0.0.0');

registerInit(program);
registerSync(program);
registerCallback(program);
registerSpawn(program);
registerTrack(program);
registerStatus(program);
registerEval(program);
registerComplete(program);
registerHealth(program);

program.parse(process.argv);

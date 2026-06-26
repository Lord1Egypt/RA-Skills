#!/usr/bin/env node
const path    = require('path');
const { err } = require('./lib/output');

const COMMANDS = {
  'get-token':   './commands/get-token',
  'get-tokens':  './commands/get-tokens',
  'get-trades':  './commands/get-trades',
  'quote':       './commands/quote',
  'buy-token':   './commands/buy-token',
  'sell-token':  './commands/sell-token',
  'create-token':'./commands/create-token',
};

const cmd = process.argv[2];

if (!cmd || cmd === '--help' || cmd === '-h') {
  const helpData = {
    success: true,
    data: {
      skill:    'HODL.DANCE Agent Skill',
      version:  require('../package.json').version,
      commands: Object.keys(COMMANDS),
      usage:    'hodl-skill <command> [args]',
      docs:     'https://docs.hodl.dance',
    }
  };

  process.stdout.write(JSON.stringify(helpData, null, 2) + '\n');
  process.exitCode = 0;
  return;
}

if (!COMMANDS[cmd]) {
  err(`Unknown command: "${cmd}". Available: ${Object.keys(COMMANDS).join(', ')}`, 'UNKNOWN_COMMAND');
}

process.argv.splice(2, 1);
require(path.join(__dirname, COMMANDS[cmd]));

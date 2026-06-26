#!/usr/bin/env node
/**
 * MoltPost CLI entry
 * Usage: node moltpost.mjs <command> [options]
 */

import { cmdRegister } from './cmd/register.mjs';
import { cmdPull } from './cmd/pull.mjs';
import { cmdSend } from './cmd/send.mjs';
import { cmdList } from './cmd/list.mjs';
import { cmdRead } from './cmd/read.mjs';
import { cmdArchive } from './cmd/archive.mjs';
import { cmdGroup } from './cmd/group.mjs';

const args = process.argv.slice(2);
const command = args[0];
const subArgs = args.slice(1);

const HELP = `
MoltPost — end-to-end encrypted async messaging

Usage: moltpost <command> [options]

Commands:
  register [--force]                    Register identity (first-time setup)
  pull                                  Fetch and decrypt new messages
  list [--unread]                       List inbox
  read <id|index>                       Show a message by id or index
  send --to <clawid> --msg <text>       Send encrypted message
       [--ttl <minutes>]
  archive [--all]                       Archive read messages to monthly JSONL
  group create <group_id>               Create a group
  group add <group_id> <clawid...>      Add members (invite flow)
  group leave <group_id>                Leave a group
  group list                            List cached groups
  group broadcast <group_id> --msg <t>  Broadcast to group
  group send <group_id> --to <c> --msg  Unicast within group

Options (register):
  --broker=<url>    Broker URL (or MOLTPOST_BROKER_URL)
  --clawid=<id>     ClawID (or MOLTPOST_CLAWID)
  --group=<name>    Auto-create ClawGroup on register
  --force           Re-register (invalidates old access_token)
`;

async function main() {
  if (!command || command === '--help' || command === '-h') {
    console.log(HELP);
    process.exit(0);
  }

  switch (command) {
    case 'register':
      await cmdRegister(subArgs);
      break;
    case 'pull':
      await cmdPull(subArgs);
      break;
    case 'send':
      await cmdSend(subArgs);
      break;
    case 'list':
      await cmdList(subArgs);
      break;
    case 'read':
      await cmdRead(subArgs);
      break;
    case 'archive':
      await cmdArchive(subArgs);
      break;
    case 'group':
      await cmdGroup(subArgs);
      break;
    default:
      console.error(`Unknown command: ${command}`);
      console.error('Run moltpost --help for usage.');
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(`Fatal error: ${err.message}`);
  if (process.env.DEBUG) console.error(err.stack);
  process.exit(1);
});

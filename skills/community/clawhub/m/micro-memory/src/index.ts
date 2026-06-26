#!/usr/bin/env node

// Micro Memory V3.0 - Native TypeScript Implementation
// Clawdbot Native Skill

import { MemoryManager } from './memory';
import { linkCommand, graphCommand } from './links';
import { reviewCommand } from './review';
import { healthCommand } from './health';
import { archiveCommand, compressCommand, consolidateCommand, exportCommand } from './archive';
import { printColored } from './utils';
import { CommandArgs } from './types';

function parseArgs(args: string[]): { command: string; args: CommandArgs } {
  const command = args[0] || 'help';
  const parsed: CommandArgs = {};
  const positional: string[] = [];

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const equalIndex = arg.indexOf('=');
      if (equalIndex > 0) {
        const key = arg.substring(2, equalIndex);
        const value = arg.substring(equalIndex + 1);
        parsed[key] = value;
      } else {
        const key = arg.substring(2);
        parsed[key] = true;
      }
    } else {
      positional.push(arg);
    }
  }

  // Handle positional arguments - first positional is content/keyword
  if (positional.length > 0) {
    // Clean up any escaped quotes from Windows cmd
    const cleanContent = positional[0].replace(/^["']|["']$/g, '');
    // 如果没有 content，也没有 keyword，则把位置参数同时设为两者
    if (!parsed.content) {
      parsed.content = cleanContent;
    }
    if (!parsed.keyword) {
      parsed.keyword = cleanContent;
    }
  }

  return { command, args: parsed };
}

function printHelp(): void {
  console.log(`
🧠 Micro Memory V3.0 - Native TypeScript Skill

Usage: memory <command> [options]

Commands:
  add [content] [--tag=TAG] [--type=TYPE] [--importance=N] [--link=IDS] [--review=DATE]
    Add a new memory

  list [--tag=TAG] [--type=TYPE] [--show_strength]
    List memories

  search <keyword> [--tag=TAG] [--limit=N]
    Search memories

  delete --id=ID
    Delete a memory

  edit --id=ID [content]
    Edit a memory

  reinforce --id=ID [--boost=N]
    Reinforce a memory

  strength [--decaying]
    Show strength report

  stats
    Show statistics

  health
    Show health report

  review [--today]
    Show due reviews

  link --from=ID --to=IDS
    Link memories (IDS: comma-separated)

  graph [--id=ID]
    Show memory graph

  consolidate
    Remove duplicates

  compress
    Compress weak memories

  archive [--older_than=DAYS]
    Archive old memories

  export [--format=FORMAT]
    Export memories (json|csv)

  help
    Show this help

Examples:
  memory add "Learned about TypeScript" --tag=tech --type=longterm --importance=5
  memory search "TypeScript" --limit=5
  memory list --tag=tech --show_strength
  memory reinforce --id=1 --boost=2
  memory review --today
`);
}

function main(): void {
  const { command, args } = parseArgs(process.argv.slice(2));
  const memoryManager = new MemoryManager();
  const memories = memoryManager.getMemories();

  switch (command) {
    case 'add':
      memoryManager.add(args);
      break;

    case 'list':
      memoryManager.list(args);
      break;

    case 'search':
      memoryManager.search(args);
      break;

    case 'delete':
      memoryManager.delete(args);
      break;

    case 'edit':
      memoryManager.edit(args);
      break;

    case 'reinforce':
      memoryManager.reinforce(args);
      break;

    case 'strength':
      memoryManager.strength(args);
      break;

    case 'stats':
      memoryManager.stats();
      break;

    case 'health':
      healthCommand(memories);
      break;

    case 'review':
      reviewCommand(args, memories);
      break;

    case 'link':
      linkCommand(args, memories);
      break;

    case 'graph':
      graphCommand(args, memories);
      break;

    case 'consolidate':
      consolidateCommand(memories);
      break;

    case 'compress':
      compressCommand(memories);
      break;

    case 'archive':
      archiveCommand(args, memories);
      break;

    case 'export':
      exportCommand(args, memories);
      break;

    case 'help':
    default:
      printHelp();
      break;
  }
}

// Run main
main();

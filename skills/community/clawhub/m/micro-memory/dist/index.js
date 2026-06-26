#!/usr/bin/env node
"use strict";
// Micro Memory V3.0 - Native TypeScript Implementation
// Clawdbot Native Skill
Object.defineProperty(exports, "__esModule", { value: true });
const memory_1 = require("./memory");
const links_1 = require("./links");
const review_1 = require("./review");
const health_1 = require("./health");
const archive_1 = require("./archive");
function parseArgs(args) {
    const command = args[0] || 'help';
    const parsed = {};
    const positional = [];
    for (let i = 1; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--')) {
            const equalIndex = arg.indexOf('=');
            if (equalIndex > 0) {
                const key = arg.substring(2, equalIndex);
                const value = arg.substring(equalIndex + 1);
                parsed[key] = value;
            }
            else {
                const key = arg.substring(2);
                parsed[key] = true;
            }
        }
        else {
            positional.push(arg);
        }
    }
    // Handle positional arguments - first positional is content or keyword
    if (positional.length > 0 && !parsed.content && !parsed.keyword) {
        // Clean up any escaped quotes from Windows cmd
        const cleanContent = positional[0].replace(/^["']|["']$/g, '');
        parsed.content = cleanContent;
        // For search command, also set keyword
        if (command === 'search') {
            parsed.keyword = cleanContent;
        }
    }
    return { command, args: parsed };
}
function printHelp() {
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
function main() {
    const { command, args } = parseArgs(process.argv.slice(2));
    const memoryManager = new memory_1.MemoryManager();
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
            (0, health_1.healthCommand)(memories);
            break;
        case 'review':
            (0, review_1.reviewCommand)(args, memories);
            break;
        case 'link':
            (0, links_1.linkCommand)(args, memories);
            break;
        case 'graph':
            (0, links_1.graphCommand)(args, memories);
            break;
        case 'consolidate':
            (0, archive_1.consolidateCommand)(memories);
            break;
        case 'compress':
            (0, archive_1.compressCommand)(memories);
            break;
        case 'archive':
            (0, archive_1.archiveCommand)(args, memories);
            break;
        case 'export':
            (0, archive_1.exportCommand)(args, memories);
            break;
        case 'help':
        default:
            printHelp();
            break;
    }
}
// Run main
main();
//# sourceMappingURL=index.js.map
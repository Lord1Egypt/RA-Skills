#!/usr/bin/env node
/**
 * Add a markdown file as a page in a Notion database
 *
 * Usage: add-to-database.js <database-id> <page-title> <markdown-file-path>
 */

const fs = require('fs');
const {
  checkApiKey,
  notionRequest,
  parseMarkdownToBlocks,
  appendBlocksBatched,
  stripTokenArg,
  hasJsonFlag,
  log,
  resolveSafePath,
} = require('./notion-utils.js');

checkApiKey();

function printUsage() {
  console.log('Usage: add-to-database.js <database-id> <page-title> <markdown-file-path> [--json] [--allow-read-path <exact-path>]');
  console.log('');
  console.log('Example:');
  console.log('  add-to-database.js <db-id> "Research Report" research.md --json');
}

function failArgument(message) {
  if (hasJsonFlag()) console.log(JSON.stringify({ error: message }, null, 2));
  else log(`Error: ${message}`);
  process.exit(1);
}

async function main() {
  const args = stripTokenArg(process.argv.slice(2));
  const isHelp = args.includes('--help');

  if (isHelp) {
    printUsage();
    process.exit(0);
  }

  const unknownOption = args.find(arg => arg.startsWith('-'));
  if (unknownOption) {
    failArgument(`Unknown option: ${unknownOption}`);
  }

  if (args.length < 3) {
    printUsage();
    process.exit(1);
  }

  if (args.length > 3) {
    failArgument(`Unexpected argument: ${args[3]}`);
  }

  const [dbId, title, mdPath] = args;

  let safeMdPath;
  try {
    safeMdPath = resolveSafePath(mdPath, { mode: 'read' });
  } catch (error) {
    if (hasJsonFlag()) console.log(JSON.stringify({ error: error.message }, null, 2));
    else log(`Error: ${error.message}`);
    process.exit(1);
  }

  if (!fs.existsSync(safeMdPath)) {
    const message = `File not found: ${mdPath}`;
    if (hasJsonFlag()) console.log(JSON.stringify({ error: message }, null, 2));
    else log(`Error: ${message}`);
    process.exit(1);
  }

  try {
    log('Adding page to database...');
    log(`  Database: ${dbId}`);
    log(`  Title: ${title}`);
    log(`  Source: ${safeMdPath}`);

    const page = await notionRequest('/v1/pages', 'POST', {
      parent: { type: 'database_id', database_id: dbId },
      properties: {
        'Name': { title: [{ text: { content: title } }] }
      }
    });

    const markdown = fs.readFileSync(safeMdPath, 'utf8');
    const blocks = parseMarkdownToBlocks(markdown, { richText: 'markdown' });
    log(`Parsed ${blocks.length} blocks from markdown`);

    await appendBlocksBatched(page.id, blocks);

    const result = {
      id: page.id,
      url: `https://notion.so/${page.id.replace(/-/g, '')}`,
      title,
      blockCount: blocks.length,
    };

    if (hasJsonFlag()) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(`✓ Page created: ${page.id}`);
      console.log(`  URL: ${result.url}`);
      console.log('\n✅ Successfully added to database!');
      console.log(`📄 URL: ${result.url}`);
      console.log('\n💡 Add additional properties (Type, Tags, Status) manually in Notion');
    }
  } catch (error) {
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: error.message }, null, 2));
    } else {
      log(`Error: ${error.message}`);
    }
    process.exit(1);
  }
}

main();

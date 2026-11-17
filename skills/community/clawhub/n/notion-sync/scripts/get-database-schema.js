#!/usr/bin/env node
/**
 * Inspect a Notion database schema (properties and types)
 *
 * Usage: get-database-schema.js <database-id>
 */

const { checkApiKey, notionRequest, stripTokenArg, hasJsonFlag, hasHelpFlag } = require('./notion-utils.js');

checkApiKey();

async function main() {
  const args = stripTokenArg(process.argv.slice(2));
  const dbId = args[0];
  const showHelp = hasHelpFlag();

  if (!dbId || showHelp) {
    console.log('Usage: get-database-schema.js <database-id> [--json]');
    process.exit(showHelp ? 0 : 1);
  }

  if (args.length > 1) {
    const message = args[1].startsWith('-')
      ? `Unknown option: ${args[1]}`
      : `Unexpected argument: ${args[1]}`;
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: message }, null, 2));
    } else {
      console.error('Error:', message);
    }
    process.exit(1);
  }

  try {
    const db = await notionRequest(`/v1/databases/${dbId}`, 'GET');
    console.log(JSON.stringify(db, null, 2));
  } catch (error) {
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: error.message }, null, 2));
    } else {
      console.error('Error:', error.message);
    }
    process.exit(1);
  }
}

main();

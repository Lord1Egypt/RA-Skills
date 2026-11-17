#!/usr/bin/env node
/**
 * Archive (soft-delete) a Notion page
 *
 * Usage: delete-notion-page.js <page-id> --confirm-archive
 */

const { checkApiKey, notionRequest, stripTokenArg, hasJsonFlag, hasHelpFlag, log } = require('./notion-utils.js');

checkApiKey();

async function main() {
  const args = stripTokenArg(process.argv.slice(2));
  const showHelp = hasHelpFlag();
  const confirmArchive = args.includes('--confirm-archive');
  const commandArgs = args.filter((arg) => arg !== '--confirm-archive');
  const pageId = commandArgs[0];

  if (!pageId || showHelp) {
    console.log('Usage: delete-notion-page.js <page-id> --confirm-archive [--json]');
    console.log('');
    console.log('Note: This archives the page (sets archived: true), not permanent deletion.');
    process.exit(showHelp ? 0 : 1);
  }

  if (commandArgs.length > 1) {
    const message = commandArgs[1].startsWith('-')
      ? `Unknown option: ${commandArgs[1]}`
      : `Unexpected argument: ${commandArgs[1]}`;
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: message }, null, 2));
    } else {
      log(`Error: ${message}`);
    }
    process.exit(1);
  }

  if (!confirmArchive) {
    const message = 'Archiving requires the explicit --confirm-archive flag.';
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: message }, null, 2));
    } else {
      log(`Error: ${message}`);
    }
    process.exit(1);
  }

  try {
    log(`Archiving page: ${pageId}`);
    const result = await notionRequest(`/v1/pages/${pageId}`, 'PATCH', { archived: true });

    const output = {
      id: result.id,
      archived: result.archived,
      url: result.url,
    };

    if (hasJsonFlag()) {
      console.log(JSON.stringify(output, null, 2));
    } else {
      console.log('✓ Page archived successfully');
      console.log(`  Page ID: ${result.id}`);
      console.log(`  Archived: ${result.archived}`);
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

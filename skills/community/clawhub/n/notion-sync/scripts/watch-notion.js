#!/usr/bin/env node
/**
 * Notion page change monitor
 * Detects edits and compares with local markdown files
 *
 * Usage: watch-notion.js <page-id> <local-path>
 */

const fs = require('fs');
const path = require('path');
const {
  checkApiKey,
  notionRequest,
  normalizeId,
  getAllBlocks,
  blocksToMarkdown,
  stripTokenArg,
  hasJsonFlag,
  hasHelpFlag,
  log,
  resolveSafePath,
  expandHomePath,
} = require('./notion-utils.js');

// State file location — relative to the workspace, not the script
const DEFAULT_STATE_FILE = path.join(process.cwd(), 'memory', 'notion-watch-state.json');

function parseWatchArgs(args) {
  let stateFile = DEFAULT_STATE_FILE;
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--state-file' && args[i + 1]) {
      stateFile = expandHomePath(args[i + 1]);
      i++;
      continue;
    }
    positional.push(args[i]);
  }

  return {
    pageId: positional[0],
    localPath: positional[1],
    stateFile,
  };
}

function loadState(stateFile) {
  if (!fs.existsSync(stateFile)) return { pages: {} };
  return JSON.parse(fs.readFileSync(stateFile, 'utf8'));
}

function saveState(stateFile, state) {
  const dir = path.dirname(stateFile);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2), 'utf8');
}

async function getPage(pageId) {
  const id = normalizeId(pageId);
  return notionRequest(`/v1/pages/${encodeURIComponent(id)}`, 'GET');
}

async function checkPage(pageId, localPath, stateFile = DEFAULT_STATE_FILE) {
  try {
    const safeLocalPath = resolveSafePath(localPath, { mode: 'read' });
    const safeStateFile = resolveSafePath(stateFile, { mode: 'write' });

    const normalizedPageId = normalizeId(pageId);
    const state = loadState(safeStateFile);
    const pageState = state.pages[normalizedPageId] || {};

    const page = await getPage(normalizedPageId);
    const lastEditedTime = page.last_edited_time;
    const title = page.properties?.title?.title?.[0]?.plain_text || 'Untitled';

    const hasChanges = !pageState.lastEditedTime ||
      new Date(lastEditedTime) > new Date(pageState.lastEditedTime);

    const result = {
      pageId: normalizedPageId,
      title,
      lastEditedTime,
      hasChanges,
      localPath: safeLocalPath,
      actions: []
    };

    if (hasChanges) {
      const blocks = await getAllBlocks(normalizedPageId);
      const notionMarkdown = blocksToMarkdown(blocks);

      let localDiffers = false;
      if (fs.existsSync(safeLocalPath)) {
        const localMarkdown = fs.readFileSync(safeLocalPath, 'utf8');
        localDiffers = localMarkdown.trim() !== notionMarkdown.trim();
      }

      result.notionMarkdown = notionMarkdown;
      result.localDiffers = localDiffers;
      result.blockCount = blocks.length;

      if (pageState.lastEditedTime) {
        result.actions.push(`📝 Page edited since last check (${new Date(pageState.lastEditedTime).toLocaleString()})`);
      } else {
        result.actions.push('🆕 First time checking this page');
      }

      if (localDiffers) {
        result.actions.push('⚠️  Local markdown differs from Notion version');
        result.actions.push('💡 Suggested: Sync Notion → markdown to update local file');
      }

      pageState.lastEditedTime = lastEditedTime;
      pageState.lastChecked = new Date().toISOString();
      pageState.title = title;
      state.pages[normalizedPageId] = pageState;
      saveState(safeStateFile, state);
    } else {
      result.actions.push('✓ No changes since last check');
    }

    return result;
  } catch (error) {
    return {
      pageId: normalizeId(pageId),
      error: error.message,
      actions: [`❌ Error checking page: ${error.message}`]
    };
  }
}

async function main() {
  const args = stripTokenArg(process.argv.slice(2));
  const usage = 'Usage: watch-notion.js [--state-file <path>] <page-id> <local-path> [--json] [--allow-unsafe-paths]';
  const { pageId, localPath, stateFile } = parseWatchArgs(args);

  if (hasHelpFlag() || !pageId || !localPath) {
    if (hasJsonFlag()) {
      console.log(JSON.stringify(hasHelpFlag() ? { usage } : { error: usage }, null, 2));
    } else {
      log(usage);
    }
    process.exit(hasHelpFlag() ? 0 : 1);
  }

  const result = await checkPage(pageId, localPath, stateFile);
  console.log(JSON.stringify(result, null, 2));
  return result;
}

if (require.main === module) {
  checkApiKey();
  main().catch(err => {
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: err.message || String(err) }, null, 2));
    } else {
      log(`Fatal error: ${err}`);
    }
    process.exit(1);
  });
} else {
  module.exports = { checkPage, parseWatchArgs };
}

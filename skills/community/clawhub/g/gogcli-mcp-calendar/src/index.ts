#!/usr/bin/env node
import { runMcp } from '@chrischall/mcp-utils';
import { VERSION, authToolsFor, registerCalendarTools, bootstrapGogAuth } from '../../gogcli-mcp/src/lib.js';
import { registerExtraCalendarTools } from './tools/calendar-extra.js';


// Seed gog's keyring from GOG_CLIENT_ID/SECRET/REFRESH_TOKEN/ACCOUNT when the host injects them.
await bootstrapGogAuth();

await runMcp({
  name: 'gogcli-calendar',
  version: VERSION,
  tools: [authToolsFor('calendar'), registerCalendarTools, registerExtraCalendarTools],
});

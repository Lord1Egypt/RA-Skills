#!/usr/bin/env node
import { runMcp } from '@chrischall/mcp-utils';
import { VERSION, authToolsFor, registerContactsTools, bootstrapGogAuth } from '../../gogcli-mcp/src/lib.js';
import { registerExtraContactsTools } from './tools/contacts-extra.js';


// Seed gog's keyring from GOG_CLIENT_ID/SECRET/REFRESH_TOKEN/ACCOUNT when the host injects them.
await bootstrapGogAuth();

await runMcp({
  name: 'gogcli-contacts',
  version: VERSION,
  tools: [authToolsFor('contacts'), registerContactsTools, registerExtraContactsTools],
});

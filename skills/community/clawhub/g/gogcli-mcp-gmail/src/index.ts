#!/usr/bin/env node
import { runMcp } from '@chrischall/mcp-utils';
import { VERSION, authToolsFor, registerGmailTools, registerUploadTools, bootstrapGogAuth } from '../../gogcli-mcp/src/lib.js';
import { registerExtraGmailTools } from './tools/gmail-extra.js';


// Seed gog's keyring from GOG_CLIENT_ID/SECRET/REFRESH_TOKEN/ACCOUNT when the host injects them.
await bootstrapGogAuth();

await runMcp({
  name: 'gogcli-gmail',
  version: VERSION,
  tools: [authToolsFor('gmail'), registerGmailTools, registerExtraGmailTools, registerUploadTools],
});

import { authToolsFor, registerGmailTools, registerUploadTools } from '../../gogcli-mcp/src/lib.js';
import { registerExtraGmailTools } from '../src/tools/gmail-extra.js';
import { describeToolAnnotations, LOCAL_AUTH_TOOLS } from '../../gogcli-mcp/tests/support/tool-annotations.js';

// The same registrar list src/index.ts hands to runMcp.
describeToolAnnotations([authToolsFor('gmail'), registerGmailTools, registerExtraGmailTools, registerUploadTools] as never, {
  tools: 63,
  destructive: 28, // + gog_gmail_drafts_copy_to, which sends mail
  local: [...LOCAL_AUTH_TOOLS, 'gog_upload_slots', 'gog_gmail_url'],
});

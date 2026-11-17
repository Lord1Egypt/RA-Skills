import { authToolsFor, registerContactsTools } from '../../gogcli-mcp/src/lib.js';
import { registerExtraContactsTools } from '../src/tools/contacts-extra.js';
import { describeToolAnnotations, LOCAL_AUTH_TOOLS } from '../../gogcli-mcp/tests/support/tool-annotations.js';

// The same registrar list src/index.ts hands to runMcp.
describeToolAnnotations([authToolsFor('contacts'), registerContactsTools, registerExtraContactsTools] as never, {
  tools: 29,
  destructive: 12,
  local: [...LOCAL_AUTH_TOOLS],
});

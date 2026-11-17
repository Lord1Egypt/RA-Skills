import { authToolsFor, registerCalendarTools } from '../../gogcli-mcp/src/lib.js';
import { registerExtraCalendarTools } from '../src/tools/calendar-extra.js';
import { describeToolAnnotations, LOCAL_AUTH_TOOLS } from '../../gogcli-mcp/tests/support/tool-annotations.js';

// The same registrar list src/index.ts hands to runMcp.
describeToolAnnotations([authToolsFor('calendar'), registerCalendarTools, registerExtraCalendarTools] as never, {
  tools: 33,
  destructive: 12,
  local: [...LOCAL_AUTH_TOOLS],
});

import { createRequire } from 'node:module';

import { resolveSkillRoot } from './runtime/client.mjs';

const require = createRequire(import.meta.url);
const skillRoot = resolveSkillRoot(process.cwd());

const config = {
  mcpServers: {
    'matrix-mate-offline': {
      command: process.execPath || 'node',
      args: ['scripts/run-offline-mcp.mjs'],
      cwd: skillRoot,
    },
  },
};

console.log(JSON.stringify(config, null, 2));

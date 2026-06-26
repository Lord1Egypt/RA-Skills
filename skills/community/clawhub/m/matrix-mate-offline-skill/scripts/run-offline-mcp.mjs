import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

import { createMatrixMateMcpServer } from './runtime/server-core.mjs';

const server = createMatrixMateMcpServer({
  serverInfo: {
    name: 'matrix-mate-offline',
    version: '1.0.0',
  },
});
const transport = new StdioServerTransport();

async function main() {
  await server.connect(transport);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

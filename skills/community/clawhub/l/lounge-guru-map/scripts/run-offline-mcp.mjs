import catalogData from '../assets/catalog.json' with { type: 'json' };

import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

import { createCatalogStore } from './runtime/catalog-core.mjs';
import { createCatalogMcpServer } from './runtime/server-core.mjs';

const store = createCatalogStore(catalogData);
const server = createCatalogMcpServer({
  serverInfo: {
    name: 'pp-lounge-map-offline',
    version: '1.0.0',
  },
  store,
});
const transport = new StdioServerTransport();

async function main() {
  await server.connect(transport);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

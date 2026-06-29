const config = {
  mcpServers: {
    'pp-lounge-map-offline': {
      command: 'node',
      args: ['skills/pp-lounge-map-offline/scripts/run-offline-mcp.mjs'],
      cwd: process.cwd(),
    },
  },
};

console.log(JSON.stringify(config, null, 2));

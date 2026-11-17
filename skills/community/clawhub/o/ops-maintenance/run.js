#!/usr/bin/env node
/**
 * 运维助手命令行入口
 */

const { loadServers, checkAllServersHealth, getClusterSummary, checkAllServersPasswordExpirationReport, executeOp } = require('./dist/index');

(async () => {
  const action = process.argv[2] || 'cluster';

  try {
    let result;
    switch (action) {
      case 'check':
      case 'health':
      case 'cluster':
        result = await getClusterSummary();
        break;
      case 'password':
      case 'passwd':
        result = await checkAllServersPasswordExpirationReport();
        break;
      case 'servers':
        const servers = await loadServers();
        result = `配置的服务器:\n${servers.map(s => `- ${s.name || s.host} (${s.user}@${s.host}:${s.port || 22})`).join('\n')}`;
        break;
      default:
        result = await executeOp(action);
    }

    console.log(result);
  } catch (err) {
    console.error('错误:', err.message);
    process.exit(1);
  }
})();
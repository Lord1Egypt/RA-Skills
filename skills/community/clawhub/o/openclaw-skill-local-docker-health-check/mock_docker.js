function getContainerLogs(name) {
  const logs = {
    'web-app': 'Error: Connection Timeout - failed to reach upstream server',
    'db': 'Fatal: OOM killer terminated process (exit code 137)',
    'cache': 'Warning: Connection refused on port 6379 - retrying...',
  };
  return logs[name] || 'Success: container is healthy';
}

function listContainers() {
  return [
    { name: 'web-app', status: 'running', ports: '80:80' },
    { name: 'db', status: 'exited', ports: '5432:5432' },
    { name: 'cache', status: 'paused', ports: '6379:6379' },
  ];
}

module.exports = { getContainerLogs, listContainers };

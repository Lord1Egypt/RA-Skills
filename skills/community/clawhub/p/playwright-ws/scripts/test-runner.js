const { spawnSync } = require('child_process');

const PLAYWRIGHT_WS = process.env.PLAYWRIGHT_WS || 'ws://localhost:3000';

// Allowed values for reporter to prevent injection
const ALLOWED_REPORTERS = ['list', 'line', 'dot', 'json', 'junit', 'html', 'github', 'blob', 'null'];

function runTests(options = {}) {
  const {
    testPattern = '',
    headed = false,
    debug = false,
    project = '',
    reporter = 'list',
    retries = 0,
    workers = undefined
  } = options;

  // Validate inputs to prevent injection
  const safeRetries = Math.max(0, Math.floor(Number(retries) || 0));
  const safeWorkers = workers !== undefined ? Math.max(1, Math.floor(Number(workers) || 1)) : undefined;
  const safeReporter = ALLOWED_REPORTERS.includes(reporter) ? reporter : 'list';

  // Set server endpoint for Playwright to use remote browser
  const env = {
    ...process.env,
    PLAYWRIGHT_WS,
    PW_TEST_CONNECT_WS_ENDPOINT: PLAYWRIGHT_WS
  };

  // Build args array — never concatenate user input into a shell string
  const args = ['playwright', 'test'];

  if (testPattern) args.push(testPattern);
  if (headed) args.push('--headed');
  if (debug) args.push('--debug');
  if (project) args.push(`--project=${project}`);
  if (safeReporter) args.push(`--reporter=${safeReporter}`);
  if (safeRetries > 0) args.push(`--retries=${safeRetries}`);
  if (safeWorkers !== undefined) args.push(`--workers=${safeWorkers}`);

  console.log('Running tests via remote Playwright server');
  console.log(`Args: ${args.join(' ')}`);

  const result = spawnSync('npx', args, { stdio: 'inherit', cwd: process.cwd(), env });
  if (result.status !== 0) throw new Error(`Tests failed with exit code ${result.status}`);
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  const options = {
    testPattern: args.find(a => !a.startsWith('--')) || '',
    headed: args.includes('--headed'),
    debug: args.includes('--debug'),
    project: args.find(a => a.startsWith('--project='))?.split('=')[1],
    reporter: args.find(a => a.startsWith('--reporter='))?.split('=')[1] || 'list',
    retries: parseInt(args.find(a => a.startsWith('--retries='))?.split('=')[1] || '0'),
    workers: args.find(a => a.startsWith('--workers='))?.split('=')[1]
  };
  
  try {
    runTests(options);
  } catch (error) {
    process.exit(1);
  }
}

module.exports = { runTests };

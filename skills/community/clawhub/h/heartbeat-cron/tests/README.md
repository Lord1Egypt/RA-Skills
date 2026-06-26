# heartbeat-cron Test Suite

Comprehensive test suite for the heartbeat-cron OpenClaw skill.

## Directory Structure

```
tests/
├── unit/                    # Unit tests
│   ├── frontmatter-parser.test.js    # Frontmatter parsing tests
│   ├── config-validation.test.js     # Configuration validation tests
│   └── skill-parser.test.js          # SKILL.md structure tests
├── integration/             # Integration tests
│   ├── heartbeat-creation.test.js    # HEARTBEAT.md creation tests
│   └── interview-workflow.test.js    # Interview workflow tests
├── e2e/                     # End-to-end tests
│   ├── complete-workflow.test.js     # Full workflow scenarios
│   └── examples-validation.test.js   # Examples validation
├── fixtures/                # Test fixtures
│   ├── valid-heartbeat-interval.md
│   ├── valid-heartbeat-cron.md
│   ├── invalid-heartbeat-*.md
│   ├── minimal-heartbeat.md
│   └── full-heartbeat.md
├── test-helpers.js          # Shared test utilities
├── setup.js                 # Jest setup
├── run-tests.js             # Test runner script
└── package.json             # Dependencies and config
```

## Installation

```bash
cd tests
npm install
```

## Running Tests

### Run all tests
```bash
npm test
# or
node run-tests.js
```

### Run specific test types
```bash
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
npm run test:e2e          # E2E tests only
```

### Run with coverage
```bash
npm run test:coverage
# or
node run-tests.js --coverage
```

### Run in watch mode
```bash
npm run test:watch
```

## Test Coverage

### Unit Tests
- **Frontmatter Parser**: Tests YAML frontmatter parsing, field extraction, edge cases
- **Configuration Validation**: Tests interval/cron validation, agent/sandbox validation, complete config validation
- **Skill Parser**: Tests SKILL.md structure, required sections, workflow steps, content quality

### Integration Tests
- **Heartbeat Creation**: Tests file creation, validation, named heartbeats, invalid detection
- **Interview Workflow**: Tests goal discovery, schedule configuration, delivery patterns, agent config

### E2E Tests
- **Complete Workflow**: Tests full scenarios (GitHub bot, uptime monitor, research digest, multi-heartbeat)
- **Examples Validation**: Tests examples.md completeness and validity

## Coverage Thresholds

Target: **>80%** coverage across all metrics

- Statements: 80%
- Branches: 80%
- Functions: 80%
- Lines: 80%

## Test Fixtures

### Valid Heartbeats
- `valid-heartbeat-interval.md` - Interval-based schedule
- `valid-heartbeat-cron.md` - Cron-based schedule with timezone
- `minimal-heartbeat.md` - Minimal valid configuration
- `full-heartbeat.md` - All configuration options

### Invalid Heartbeats
- `invalid-heartbeat-both-schedule.md` - Both interval and cron
- `invalid-heartbeat-no-schedule.md` - Missing schedule
- `invalid-heartbeat-bad-interval.md` - Invalid interval format
- `invalid-heartbeat-bad-cron.md` - Invalid cron expression

## Helper Functions

### `parseFrontmatter(content)`
Parse YAML frontmatter from markdown content.

```javascript
const result = parseFrontmatter(`---
interval: 1h
---
Body content`);

// Returns: { frontmatter: { interval: '1h' }, body: 'Body content' }
```

### `validateHeartbeatConfig(frontmatter)`
Validate complete heartbeat configuration.

```javascript
const validation = validateHeartbeatConfig({
  interval: '1h',
  agent: 'claude-code'
});

// Returns: { isValid: true, errors: [] }
```

### `isValidInterval(interval)`
Validate interval format (e.g., 15m, 1h, 6h, 1d).

### `isValidCron(cron)`
Validate cron expression (5-field format).

### `loadFixture(filename)`
Load test fixture file content.

## Murmur Command Generation

Tests verify correct generation of:
- `murmur init {path}` - Initialize/register workspace
- `murmur beat {path}` - Test heartbeat execution
- `murmur workspaces list` - List registered workspaces
- `murmur start` - Start daemon
- `murmur start --detach` - Start in background

## Scenarios Covered

1. **GitHub Issue Triage Bot** - Auto-label issues, Slack notifications
2. **Endpoint Uptime Monitor** - Health checks, ntfy alerts, CSV logging
3. **Daily Research Digest** - Arxiv monitoring, file output
4. **Multi-Heartbeat Repository** - Multiple named heartbeats
5. **Codex Architecture Review** - Sandbox configuration, weekly reviews
6. **Pi Browser Automation** - Browser sessions, Telegram notifications

## CI/CD Integration

```yaml
# Example GitHub Actions
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd tests && npm install
      - run: cd tests && npm run test:coverage
```

## Reporting

Coverage reports are generated in:
- `coverage/` - HTML report
- Console output - Text summary

View HTML report:
```bash
open coverage/index.html  # macOS
start coverage/index.html  # Windows
xdg-open coverage/index.html  # Linux
```

## Troubleshooting

### Tests fail with "Cannot find module"
```bash
cd tests
npm install
```

### Coverage below threshold
Check which files are missing coverage:
```bash
npm run test:coverage
# Check coverage/lcov-report/index.html
```

### Specific test failing
Run with verbose output:
```bash
node run-tests.js --verbose tests/unit/specific-test.test.js
```

## Contributing

When adding new features to heartbeat-cron:

1. Add unit tests for new validation logic
2. Add integration tests for new workflow steps
3. Add E2E tests for new scenarios
4. Update fixtures if needed
5. Ensure coverage remains >80%

## License

Same as heartbeat-cron skill.

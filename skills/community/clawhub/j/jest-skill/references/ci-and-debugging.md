# CI & Debugging Reference

## CI Optimization

### Worker Configuration

```bash
# Serial execution — best for small suites or memory-constrained CI
npx jest --runInBand

# Fixed workers
npx jest --maxWorkers=2

# Percentage of CPUs
npx jest --maxWorkers=50%
```

### Sharding (Jest 28+)

Split tests across parallel CI jobs:

```bash
# 4 parallel CI jobs
npx jest --shard=1/4  # Job 1
npx jest --shard=2/4  # Job 2
npx jest --shard=3/4  # Job 3
npx jest --shard=4/4  # Job 4
```

Jest distributes test files deterministically so each shard runs a different subset.

### CI-Specific Config

```javascript
// jest.config.js
module.exports = {
  ...(process.env.CI && {
    maxWorkers: 2,
    bail: 1,
    verbose: false,
    coverageReporters: ['text-summary', 'lcov'],
  }),
};
```

### Cache

Jest caches transformed files and dependency graphs. In CI:

```bash
# Cache directory (default: /tmp/jest_*)
npx jest --cacheDirectory=.jest-cache

# Clear cache
npx jest --clearCache

# Disable cache (for debugging)
npx jest --no-cache
```

Cache the `.jest-cache` directory in CI for faster subsequent runs:

```yaml
# GitHub Actions
- uses: actions/cache@v4
  with:
    path: .jest-cache
    key: jest-${{ runner.os }}-${{ hashFiles('**/jest.config.*') }}
```

### Bail on First Failure

```bash
npx jest --bail          # stop after first failed test suite
npx jest --bail=3        # stop after 3 failed test suites
```

### Detect Open Handles

```bash
npx jest --detectOpenHandles
```

Warns about handles (timers, connections, listeners) that prevent Jest from exiting cleanly.

### Force Exit

```bash
npx jest --forceExit
```

Forcefully exits after tests complete. Use as a last resort — `--detectOpenHandles` is preferred to find the root cause.

## Debugging

### Node Inspector

```bash
# Debug in Chrome DevTools
node --inspect-brk node_modules/.bin/jest --runInBand

# Then open chrome://inspect in Chrome
```

`--runInBand` is required — debugging multiple workers is not practical.

### VS Code Launch Config

```json
{
  "type": "node",
  "request": "launch",
  "name": "Jest Debug",
  "program": "${workspaceFolder}/node_modules/.bin/jest",
  "args": [
    "--runInBand",
    "--no-cache",
    "${relativeFile}"
  ],
  "console": "integratedTerminal",
  "internalConsoleOptions": "neverOpen"
}
```

### Debug Specific Test

```json
{
  "type": "node",
  "request": "launch",
  "name": "Jest Debug Current Test",
  "program": "${workspaceFolder}/node_modules/.bin/jest",
  "args": [
    "--runInBand",
    "--no-cache",
    "--testPathPattern",
    "${relativeFile}",
    "--testNamePattern",
    "test name pattern"
  ]
}
```

### console.log in Tests

Jest buffers console output by default. To see it immediately:

```bash
npx jest --verbose
```

Or suppress console output for cleaner test output:

```javascript
beforeEach(() => {
  jest.spyOn(console, 'log').mockImplementation(() => {});
  jest.spyOn(console, 'error').mockImplementation(() => {});
});
```

## Troubleshooting

### "Your test suite must contain at least one test"

- Tests defined inside async callbacks are not registered.
- Check for `(async () => { test(...) })()` pattern.
- Ensure `test()` calls are at the top level or inside synchronous `describe()`.

### "Cannot use import statement outside a module"

- A `node_modules` package ships ESM but Jest expects CJS.
- Fix: add the package to `transformIgnorePatterns` negative lookahead.

```javascript
transformIgnorePatterns: ['/node_modules/(?!(esm-package)/)']
```

### "Async callback was not invoked within the 5000 ms timeout"

- `done()` callback was never called.
- Wrap `expect` in try/catch and call `done(error)` in catch.
- Or switch to async/await.

### "ReferenceError: X is not defined" in jest.mock factory

- Variable is not initialized when the hoisted factory runs.
- Prefix variable with `mock` or define values inline.

### Tests pass individually but fail together

- Shared mutable state between tests.
- Missing mock restoration.
- Fix: use `beforeEach` to reset state, `restoreMocks: true` in config.

### Tests pass locally but fail in CI

- Worker count mismatch (too many workers for CI container).
- Use `--maxWorkers=2` or `--runInBand` in CI.
- Race conditions exposed by different execution order.
- Missing `--forceExit` for open handles.

### Jest hangs after tests complete

```bash
npx jest --detectOpenHandles --forceExit
```

Common causes:
- Open database connections
- Running HTTP servers
- Uncleared intervals/timers
- Unclosed event listeners

### Slow test startup

```bash
# Profile Jest startup
npx jest --showConfig  # check for expensive transforms
npx jest --listTests   # verify test discovery isn't scanning too much
```

Common fixes:
- Use `@swc/jest` or `esbuild-jest` instead of `ts-jest` for faster TypeScript transform.
- Exclude unnecessary directories with `testPathIgnorePatterns`.
- Use `--shard` to split across CI jobs.

## Watch Mode

```bash
npx jest --watch          # re-run on file changes (git-aware)
npx jest --watchAll       # re-run on any file change

# Watch mode commands:
# f — run only failed tests
# o — run only changed tests (default)
# p — filter by filename pattern
# t — filter by test name pattern
# a — run all tests
# u — update failing snapshots
# q — quit
```

## Reporters

```javascript
// jest.config.js
module.exports = {
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: './reports',
      outputName: 'jest-junit.xml',
    }],
    ['jest-html-reporter', {
      outputPath: './reports/test-report.html',
    }],
  ],
};
```

### GitHub Actions Reporter

```yaml
- name: Run tests
  run: npx jest --ci --reporters=default --reporters=jest-junit
  env:
    JEST_JUNIT_OUTPUT_DIR: ./reports
```

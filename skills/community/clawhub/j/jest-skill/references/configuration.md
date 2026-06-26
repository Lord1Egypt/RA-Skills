# Configuration Reference

Jest configuration can be defined in `jest.config.js`, `jest.config.ts`, `jest.config.mjs`, or in the `"jest"` key of `package.json`.

## Test File Discovery

### `testMatch`

Glob patterns for test files. Default matches `**/__tests__/**/*` and `**/*.{test,spec}.*`.

```javascript
module.exports = {
  testMatch: [
    '<rootDir>/src/**/*.test.{js,ts,tsx}',
    '<rootDir>/tests/**/*.spec.{js,ts,tsx}',
  ],
};
```

### `testPathIgnorePatterns`

Patterns to exclude from test discovery.

```javascript
module.exports = {
  testPathIgnorePatterns: ['/node_modules/', '/dist/', '/fixtures/'],
};
```

### `testRegex`

Alternative to `testMatch` — uses regex instead of globs. Cannot use both.

```javascript
module.exports = {
  testRegex: '(/__tests__/.*|(\\.|/)(test|spec))\\.[jt]sx?$',
};
```

## Transform

### `transform`

Maps file extensions to transformers. Default uses `babel-jest`.

```javascript
module.exports = {
  transform: {
    '^.+\\.tsx?$': 'ts-jest',                // TypeScript
    '^.+\\.jsx?$': 'babel-jest',             // JavaScript
    '^.+\\.css$': 'jest-css-modules-transform', // CSS
  },
};
```

### `transformIgnorePatterns`

Patterns to skip transformation. Default: `['/node_modules/']`.

```javascript
module.exports = {
  transformIgnorePatterns: [
    '/node_modules/(?!(uuid|nanoid|chalk)/)', // transform ESM packages
  ],
};
```

## Module Resolution

### `moduleNameMapper`

Maps module paths for aliasing or mocking static assets.

```javascript
module.exports = {
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',           // @ alias
    '\\.(css|scss)$': 'identity-obj-proxy',   // CSS modules
    '\\.(jpg|png|svg)$': '<rootDir>/test/__mocks__/fileMock.js', // assets
  },
};
```

### `modulePaths`

Additional directories to search for modules.

```javascript
module.exports = {
  modulePaths: ['<rootDir>/src'],
};
```

### `moduleDirectories`

Directories to search when resolving modules. Default: `['node_modules']`.

```javascript
module.exports = {
  moduleDirectories: ['node_modules', 'src'],
};
```

## Test Environment

### `testEnvironment`

The environment for all tests. Default: `'node'`.

```javascript
module.exports = {
  testEnvironment: 'node',   // Node.js globals
  // or
  testEnvironment: 'jsdom',  // Browser-like globals (window, document)
};
```

Per-file override via docblock:

```javascript
/**
 * @jest-environment jsdom
 */
```

### `testEnvironmentOptions`

Options passed to the environment.

```javascript
module.exports = {
  testEnvironmentOptions: {
    url: 'https://example.com',  // jsdom URL
    customExportConditions: ['node', 'node-addons'],
  },
};
```

## Coverage

### `collectCoverage`

Enable coverage collection. Default: `false`.

```javascript
module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',        // barrel files
    '!src/**/*.stories.tsx',   // Storybook
  ],
};
```

### `coverageThreshold`

Enforce minimum coverage. CI fails if thresholds are not met.

```javascript
module.exports = {
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
    './src/critical/': { branches: 95, lines: 95 },
  },
};
```

### `coverageReporters`

Output formats. Default: `['json', 'text', 'lcov', 'clover']`.

```javascript
module.exports = {
  coverageReporters: ['text', 'text-summary', 'lcov', 'html'],
};
```

### `coverageDirectory`

Output directory. Default: `'coverage'`.

### `coverageProvider`

Coverage implementation. `'v8'` (faster, default in Jest 30) or `'babel'`.

## Mock Configuration

```javascript
module.exports = {
  clearMocks: true,    // jest.clearAllMocks() after each test
  resetMocks: true,    // jest.resetAllMocks() after each test
  restoreMocks: true,  // jest.restoreAllMocks() after each test (recommended)
  automock: false,      // auto-mock all imports (default: false)
};
```

## Setup Files

### `setupFiles`

Run before the test framework is installed. Use for polyfills and global setup.

```javascript
module.exports = {
  setupFiles: ['./jest.polyfills.js'],
};
```

### `setupFilesAfterFramework` / `setupFilesAfterFramework` → `setupFilesAfterFramework`

### `setupFilesAfterFramework`

(Jest 30) Replaces `setupFilesAfterFramework`.

### `setupFilesAfterFramework`

Run after test framework is installed. Use for custom matchers and global test setup.

```javascript
module.exports = {
  setupFilesAfterFramework: ['./jest.setup.js'],
};
```

### `globalSetup` / `globalTeardown`

Run once before/after all test suites. Use for starting servers, databases, etc.

```javascript
module.exports = {
  globalSetup: './global-setup.js',
  globalTeardown: './global-teardown.js',
};
```

## Execution

### `maxWorkers`

Number of workers. Default: number of CPUs.

```javascript
module.exports = {
  maxWorkers: '50%',  // or a fixed number: 2
};
```

### `verbose`

Display individual test results. Default: `false`.

### `bail`

Stop after `n` test failures. `true` = 1.

```javascript
module.exports = {
  bail: 1, // stop on first failure
};
```

### `testTimeout`

Default timeout for tests in ms. Default: `5000`.

```javascript
module.exports = {
  testTimeout: 10000,
};
```

### `randomize`

Run tests in random order within each file.

```javascript
module.exports = {
  randomize: true,
};
```

## Projects (Monorepo)

```javascript
module.exports = {
  projects: [
    '<rootDir>/packages/core',
    '<rootDir>/packages/web',
    {
      displayName: 'unit',
      testMatch: ['<rootDir>/src/**/*.test.ts'],
    },
    {
      displayName: 'integration',
      testMatch: ['<rootDir>/tests/**/*.integration.ts'],
      testTimeout: 30000,
    },
  ],
};
```

## Snapshot

```javascript
module.exports = {
  snapshotFormat: {
    printBasicPrototype: false, // cleaner snapshot output
  },
  snapshotSerializers: ['enzyme-to-json/serializer'],
};
```

## Watch Plugins

```javascript
module.exports = {
  watchPlugins: [
    'jest-watch-typeahead/filename',
    'jest-watch-typeahead/testname',
  ],
};
```

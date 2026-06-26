/**
 * Jest setup file for heartbeat-cron tests
 */

// Global test configuration
global.TEST_CONFIG = {
  timeout: 10000,
  verbose: true
};

// Mock console methods if needed
global.console = {
  ...console,
  // Uncomment to suppress console.log during tests
  // log: jest.fn(),
  // debug: jest.fn(),
  // info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};

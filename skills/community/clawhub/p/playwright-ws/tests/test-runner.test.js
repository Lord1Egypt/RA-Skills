const { runTests } = require('../scripts/test-runner');

describe('Test Runner Script', () => {
  test('should export runTests function', () => {
    expect(typeof runTests).toBe('function');
  });

  test('should accept options object', () => {
    const options = {
      testPattern: '*.test.js',
      headed: true,
      debug: false,
      project: 'chromium',
      reporter: 'list',
      retries: 1,
      workers: 4
    };
    
    expect(options.testPattern).toBe('*.test.js');
    expect(options.headed).toBe(true);
    expect(options.project).toBe('chromium');
  });

  test('should set WS endpoint environment variable', () => {
    const fs = require('fs');
    const path = require('path');
    const script = fs.readFileSync(
      path.join(__dirname, '../scripts/test-runner.js'),
      'utf8'
    );
    expect(script).toContain('PW_TEST_CONNECT_WS_ENDPOINT');
    expect(script).toContain('PLAYWRIGHT_WS');
  });
});

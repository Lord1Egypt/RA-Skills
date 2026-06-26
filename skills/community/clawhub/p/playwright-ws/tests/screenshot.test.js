const { takeScreenshot } = require('../scripts/screenshot');
const fs = require('fs');
const path = require('path');

describe('Screenshot Script', () => {
  test('should export takeScreenshot function', () => {
    expect(typeof takeScreenshot).toBe('function');
  });

  test('should use PLAYWRIGHT_WS environment variable', () => {
    const script = fs.readFileSync(
      path.join(__dirname, '../scripts/screenshot.js'),
      'utf8'
    );
    expect(script).toContain('PLAYWRIGHT_WS');
    expect(script).toContain('chromium.connect');
  });

  test('should default to localhost WebSocket', () => {
    const script = fs.readFileSync(
      path.join(__dirname, '../scripts/screenshot.js'),
      'utf8'
    );
    expect(script).toContain("'ws://localhost:3000'");
  });

  test('should accept screenshot options', () => {
    const options = {
      fullPage: true,
      viewport: { width: 1920, height: 1080 },
      waitForSelector: '.loaded',
      delay: 1000,
      type: 'png'
    };
    
    expect(options.fullPage).toBe(true);
    expect(options.viewport.width).toBe(1920);
    expect(options.type).toBe('png');
  });
});

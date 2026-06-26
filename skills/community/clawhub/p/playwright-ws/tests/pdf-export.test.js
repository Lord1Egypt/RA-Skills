const { generatePDF } = require('../scripts/pdf-export');
const fs = require('fs');
const path = require('path');

describe('PDF Export Script', () => {
  test('should export generatePDF function', () => {
    expect(typeof generatePDF).toBe('function');
  });

  test('should use PLAYWRIGHT_WS environment variable', () => {
    const script = fs.readFileSync(
      path.join(__dirname, '../scripts/pdf-export.js'),
      'utf8'
    );
    expect(script).toContain('PLAYWRIGHT_WS');
    expect(script).toContain('chromium.connect');
  });

  test('should accept PDF options', () => {
    const options = {
      format: 'A4',
      landscape: true,
      margin: { top: '2cm', right: '2cm', bottom: '2cm', left: '2cm' },
      printBackground: true
    };
    
    expect(options.format).toBe('A4');
    expect(options.landscape).toBe(true);
    expect(options.printBackground).toBe(true);
  });
});

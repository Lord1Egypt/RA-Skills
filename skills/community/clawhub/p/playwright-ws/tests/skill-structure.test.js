const fs = require('fs');
const path = require('path');

describe('Skill Structure', () => {
  const skillDir = path.join(__dirname, '..');

  test('should have SKILL.md', () => {
    expect(fs.existsSync(path.join(skillDir, 'SKILL.md'))).toBe(true);
  });

  test('should have README.md', () => {
    expect(fs.existsSync(path.join(skillDir, 'README.md'))).toBe(true);
  });

  test('should have required scripts', () => {
    expect(fs.existsSync(path.join(skillDir, 'scripts', 'screenshot.js'))).toBe(true);
    expect(fs.existsSync(path.join(skillDir, 'scripts', 'pdf-export.js'))).toBe(true);
    expect(fs.existsSync(path.join(skillDir, 'scripts', 'test-runner.js'))).toBe(true);
  });

  test('should have reference documentation', () => {
    expect(fs.existsSync(path.join(skillDir, 'references', 'selectors.md'))).toBe(true);
    expect(fs.existsSync(path.join(skillDir, 'references', 'api-reference.md'))).toBe(true);
  });

  test('should not contain internal URLs in public files', () => {
    const readme = fs.readFileSync(path.join(skillDir, 'README.md'), 'utf8');
    const skill = fs.readFileSync(path.join(skillDir, 'SKILL.md'), 'utf8');
    
    // Should not contain first-it-consulting.com URLs
    expect(readme).not.toContain('first-it-consulting.com');
    expect(skill).not.toContain('first-it-consulting.com');
    
    // Should use example.com or localhost
    expect(readme).toContain('example.com');
  });

  test('should have proper YAML frontmatter in SKILL.md', () => {
    const skill = fs.readFileSync(path.join(skillDir, 'SKILL.md'), 'utf8');
    expect(skill).toMatch(/^---\nname: playwright-ws\ndescription:/);
  });
});

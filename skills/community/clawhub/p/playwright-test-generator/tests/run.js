// Simple test runner for playwright-test-generator
import { PlaywrightTestGenerator } from '../src/generator.js';
import { Parser } from '../src/parser.js';
import { LocatorExtractor } from '../src/locator.js';
import assert from 'assert';

const gen = new PlaywrightTestGenerator();
let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log(`  ✅ ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ❌ ${name}: ${err.message}`);
    failed++;
  }
}

function expect(actual) {
  return {
    toBe(expected) {
      if (actual !== expected) throw new Error(`Expected ${expected} but got ${actual}`);
    },
    toContain(str) {
      if (!String(actual).includes(str)) throw new Error(`Expected "${actual}" to contain "${str}"`);
    },
    toMatch(regex) {
      if (!regex.test(String(actual))) throw new Error(`Expected "${actual}" to match ${regex}`);
    },
    toBeDefined() {
      if (actual === undefined) throw new Error('Expected value to be defined');
    },
    toBeGreaterThan(n) {
      if (actual <= n) throw new Error(`Expected ${actual} to be > ${n}`);
    },
    rejects(promise) {
      // Use then/catch to avoid unhandled rejection in Node.js
      return promise.then(
        () => { throw new Error('Expected promise to reject but it resolved'); },
        () => { /* Expected rejection — do nothing */ }
      );
    }
  };
}

async function run() {
  console.log('\n🎭 playwright-test-generator — Test Suite\n');

  // ── pytest-playwright POM ──
  console.log('[pytest-playwright POM]');
  await test('generates POM class with locator methods', async () => {
    const result = await gen.generate({
      input: 'Click the login button, enter "user@example.com" in username field, enter "secret123" in password field, press Enter',
      framework: 'pytest-playwright',
      codeType: 'pom',
      pageName: 'LoginPage',
      baseUrl: 'https://example.com'
    });
    expect(result.language).toBe('python');
    expect(result.code).toContain('class LoginPage');
    expect(result.code).toContain('click');
    expect(result.code).toContain('fill');
  });

  await test('generates POM with fixture decorator', async () => {
    const result = await gen.generate({
      input: 'Navigate to https://example.com, verify title contains "Login"',
      framework: 'pytest-playwright',
      codeType: 'pom',
      pageName: 'LoginPage'
    });
    expect(result.code).toContain('@pytest.fixture');
    expect(result.code).toContain('page.goto');
  });

  // ── pytest-playwright standard ──
  console.log('[pytest-playwright standard]');
  await test('generates standard test function', async () => {
    const result = await gen.generate({
      input: 'Navigate to https://example.com, click the submit button, verify URL changes',
      framework: 'pytest-playwright',
      codeType: 'standard',
      testName: 'test_submit_form'
    });
    expect(result.language).toBe('python');
    expect(result.code).toContain('def test_submit_form');
    expect(result.code).toContain('page.goto');
    expect(result.code).toContain('page.click');
  });

  await test('adds proper pytest assertions', async () => {
    const result = await gen.generate({
      input: 'Navigate to home page, verify the page title is "Home"',
      framework: 'pytest-playwright',
      codeType: 'standard',
      testName: 'test_home_title'
    });
    expect(result.code).toContain('expect');
  });

  // ── pytest-playwright data-driven ──
  console.log('[pytest-playwright data-driven]');
  await test('generates parameterized test with test data', async () => {
    const result = await gen.generate({
      input: 'Login with username and password from test data',
      framework: 'pytest-playwright',
      codeType: 'data-driven',
      pageName: 'LoginPage',
      testData: [
        { username: 'user1@test.com', password: 'pass1' },
        { username: 'user2@test.com', password: 'pass2' }
      ]
    });
    expect(result.code).toContain('pytest.mark.parametrize');
    expect(result.code).toContain('user1@test.com');
    expect(result.code).toContain('user2@test.com');
  });

  // ── jest-playwright POM ──
  console.log('[jest-playwright POM]');
  await test('generates TypeScript POM class for Jest', async () => {
    const result = await gen.generate({
      input: 'Click search icon, type "Playwright" in search box, press Enter',
      framework: 'jest-playwright',
      codeType: 'pom',
      pageName: 'SearchPage',
      language: 'typescript'
    });
    expect(result.language).toBe('typescript');
    expect(result.code).toContain('class SearchPage');
  });

  await test('generates Jest describe/it blocks', async () => {
    const result = await gen.generate({
      input: 'Open the dashboard, verify user avatar is visible',
      framework: 'jest-playwright',
      codeType: 'standard',
      testName: 'Dashboard.test'
    });
    expect(result.code).toContain('describe(');
    expect(result.code).toContain('test(');
  });

  // ── native-playwright ──
  console.log('[native-playwright]');
  await test('generates standalone Node.js script', async () => {
    const result = await gen.generate({
      input: 'Open browser, navigate to https://demo.playwright.dev/todomvc, add a todo item',
      framework: 'native-playwright',
      codeType: 'standard',
      pageName: 'TodoMvc'
    });
    expect(result.language).toBe('javascript');
    expect(result.code).toContain('chromium.launch');
    expect(result.code).toContain('page.goto');
  });

  await test('generates ESM import syntax', async () => {
    const result = await gen.generate({
      input: 'Take a screenshot of the homepage',
      framework: 'native-playwright',
      codeType: 'standard',
      testName: 'screenshot_test'
    });
    expect(result.code).toContain('import { chromium');
    expect(result.code).toContain('screenshot');
  });

  // ── analyzeUrl ──
  console.log('[analyzeUrl]');
  await test('analyzeUrl with mock returns page data', async () => {
    const result = await gen.analyzeUrl('https://example.com', { mock: true });
    expect(result.title).toBeDefined();
    expect(result.locators).toBeDefined();
  }, 10000);

  // ── analyzeHtml ──
  console.log('[analyzeHtml]');
  await test('extracts locators from HTML snippet', async () => {
    const html = `
      <form id="login-form">
        <input type="email" data-testid="email-input" placeholder="Email" />
        <input type="password" data-testid="password-input" placeholder="Password" />
        <button type="submit" data-testid="submit-btn">Sign In</button>
      </form>
    `;
    const result = await gen.analyzeHtml(html);
    expect(result.locators).toBeDefined();
    expect(result.locators['email-input']).toBeDefined();
    expect(result.locators['password-input']).toBeDefined();
    expect(result.locators['submit-btn']).toBeDefined();
  });

  await test('falls back to accessible selectors when no testid', async () => {
    const html = `
      <form>
        <input type="text" aria-label="Username" />
        <button role="button">Login</button>
      </form>
    `;
    const result = await gen.analyzeHtml(html);
    expect(Object.keys(result.locators).length).toBeGreaterThan(0);
  });

  // ── Error handling ──
  console.log('[error handling]');
  await test('throws on unsupported framework', async () => {
    try {
      await gen.generate({ input: 'test', framework: 'cypress', codeType: 'standard' });
      throw new Error('Should have thrown');
    } catch (err) {
      if (!err.message.includes('Unsupported framework')) throw err;
    }
  });

  await test('throws on unsupported code type', async () => {
    try {
      await gen.generate({ input: 'test', framework: 'pytest-playwright', codeType: 'visual-regression' });
      throw new Error('Should have thrown');
    } catch (err) {
      if (!err.message.includes('Unsupported code type')) throw err;
    }
  });

  await test('throws on empty input', async () => {
    try {
      await gen.generate({ input: '', framework: 'pytest-playwright', codeType: 'standard' });
      throw new Error('Should have thrown');
    } catch (err) {
      if (!err.message.includes('Empty input')) throw err;
    }
  });

  // ── Parser ──
  console.log('[Parser]');
  const parser = new Parser();

  await test('parses click actions', () => {
    const steps = parser.parse('Click the login button');
    expect(steps[0].action).toBe('click');
  });

  await test('parses fill actions with value', () => {
    const steps = parser.parse('Fill username with "john"');
    expect(steps[0].action).toBe('fill');
    expect(steps[0].value).toBe('john');
  });

  await test('parses press actions', () => {
    const steps = parser.parse('Press Enter');
    expect(steps[0].action).toBe('press');
    expect(steps[0].key).toBe('Enter');
  });

  await test('parses navigate actions', () => {
    const steps = parser.parse('Go to https://example.com');
    expect(steps[0].action).toBe('navigate');
    expect(steps[0].url).toBe('https://example.com');
  });

  await test('parses wait actions', () => {
    const steps = parser.parse('Wait for 3 seconds');
    expect(steps[0].action).toBe('wait');
    expect(steps[0].duration).toBe(3000);
  });

  await test('parses assert actions', () => {
    const steps = parser.parse('Verify the title is "Dashboard"');
    expect(steps[0].action).toBe('assert');
  });

  await test('parses multiple chained steps', () => {
    const steps = parser.parse(
      'Click login button, enter "user@test.com" in email, enter "pass123" in password, press Enter'
    );
    expect(steps.length).toBeGreaterThan(3);
    expect(steps[0].action).toBe('click');
    expect(steps[1].action).toBe('fill');
    expect(steps[2].action).toBe('fill');
    expect(steps[3].action).toBe('press');
  });

  await test('handles selector hints in natural language', () => {
    const steps = parser.parse('Click the button with id "submit-btn"');
    expect(steps[0].action).toBe('click');
  });

  // ── LocatorExtractor ──
  console.log('[LocatorExtractor]');
  await test('prioritizes data-testid over other attributes', () => {
    const html = `<input data-testid="email" id="email-field" class="email-input" />`;
    const { locators } = LocatorExtractor.extract(html);
    expect(locators['email']).toContain('data-testid');
  });

  await test('generates CSS selectors by default', () => {
    const html = `<div class="container"><span id="msg">Hello</span></div>`;
    const { locators } = LocatorExtractor.extract(html);
    expect(Object.values(locators)[0]).toMatch(/^#|\.|\[/);
  });

  await test('extracts form input labels as names', () => {
    const html = `
      <form>
        <label for="username">Username</label>
        <input id="username" type="text" />
      </form>
    `;
    const { locators } = LocatorExtractor.extract(html);
    expect(locators['username']).toBeDefined();
  });

  // ── CLI ──
  console.log('[CLI]');
  await test('exposes generate command help', async () => {
    const result = await gen.cli(['--help']);
    expect(result.output).toContain('generate');
  });

  // ── Summary ──
  console.log(`\n${'─'.repeat(40)}`);
  console.log(`Results: ${passed} ✅  ${failed} ❌\n`);

  if (failed > 0) {
    console.error('TESTS FAILED');
    process.exit(1);
  } else {
    console.log('🎉 All tests passed!\n');
  }
}

run().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});

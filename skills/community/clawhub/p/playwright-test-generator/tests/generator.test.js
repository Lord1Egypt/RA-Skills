import { describe, it, expect, beforeAll, beforeEach } from '@jest/globals';
import { PlaywrightTestGenerator } from '../src/generator.js';
import { Parser } from '../src/parser.js';
import { LocatorExtractor } from '../src/locator.js';
import path from 'path';
import fs from 'fs';

const gen = new PlaywrightTestGenerator();

describe('PlaywrightTestGenerator', () => {
  // ─── Framework: pytest-playwright ─────────────────────────────────────────

  describe('generate() — pytest-playwright POM', () => {
    it('generates POM class with locator methods', async () => {
      const result = await gen.generate({
        input: 'Click the login button, enter "user@example.com" in username field, enter "secret123" in password field, press Enter',
        framework: 'pytest-playwright',
        codeType: 'pom',
        pageName: 'LoginPage',
        baseUrl: 'https://example.com'
      });
      expect(result.language).toBe('python');
      expect(result.code).toContain('class LoginPage');
      expect(result.code).toContain('def click_login_button');
      expect(result.code).toContain('def fill_username');
      expect(result.code).toContain('def fill_password');
    });

    it('generates POM with fixture decorator', async () => {
      const result = await gen.generate({
        input: 'Navigate to login page, verify title contains "Login"',
        framework: 'pytest-playwright',
        codeType: 'pom',
        pageName: 'LoginPage'
      });
      expect(result.code).toContain('@pytest.fixture');
      expect(result.code).toContain('page.goto');
    });

    it('handles selector with data-testid priority', async () => {
      const result = await gen.generate({
        input: 'Fill email field with test@test.com',
        framework: 'pytest-playwright',
        codeType: 'pom',
        pageName: 'ContactPage'
      });
      expect(result.locators).toBeDefined();
      expect(result.steps[0].action).toBe('fill');
    });
  });

  describe('generate() — pytest-playwright standard', () => {
    it('generates standard test function', async () => {
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

    it('adds proper pytest assertions', async () => {
      const result = await gen.generate({
        input: 'Navigate to home page, verify the page title is "Home"',
        framework: 'pytest-playwright',
        codeType: 'standard',
        testName: 'test_home_title'
      });
      expect(result.code).toContain('assert');
      expect(result.code).toContain('expect');
    });
  });

  describe('generate() — pytest-playwright data-driven', () => {
    it('generates parameterized test with test data', async () => {
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
      expect(result.code).toContain('@pytest.mark.parametrize');
      expect(result.code).toContain('user1@test.com');
      expect(result.code).toContain('user2@test.com');
    });
  });

  // ─── Framework: jest-playwright ─────────────────────────────────────────────

  describe('generate() — jest-playwright POM', () => {
    it('generates TypeScript POM class for Jest', async () => {
      const result = await gen.generate({
        input: 'Click search icon, type "Playwright\" in search box, press Enter',
        framework: 'jest-playwright',
        codeType: 'pom',
        pageName: 'SearchPage',
        language: 'typescript'
      });
      expect(result.language).toBe('typescript');
      expect(result.code).toContain('class SearchPage');
      expect(result.code).toContain('async clickSearchIcon');
      expect(result.code).toContain('async fillSearchBox');
    });

    it('generates Jest describe/it blocks', async () => {
      const result = await gen.generate({
        input: 'Open the dashboard, verify user avatar is visible',
        framework: 'jest-playwright',
        codeType: 'standard',
        testName: 'Dashboard.test'
      });
      expect(result.code).toContain('describe(');
      expect(result.code).toContain('it(');
    });
  });

  // ─── Framework: native-playwright ──────────────────────────────────────────

  describe('generate() — native-playwright', () => {
    it('generates standalone Node.js script', async () => {
      const result = await gen.generate({
        input: 'Open browser, navigate to https://demo.playwright.dev/todomvc, add a todo item',
        framework: 'native-playwright',
        codeType: 'standard',
        pageName: 'TodoMvc'
      });
      expect(result.language).toBe('javascript');
      expect(result.code).toContain('const { chromium }');
      expect(result.code).toContain('await chromium.launch');
      expect(result.code).toContain('page.goto');
    });

    it('generates ESM import syntax', async () => {
      const result = await gen.generate({
        input: 'Take a screenshot of the homepage',
        framework: 'native-playwright',
        codeType: 'standard',
        testName: 'screenshot_test'
      });
      expect(result.code).toContain('import { chromium');
      expect(result.code).toContain('page.screenshot');
    });
  });

  // ─── Input: URL/HTML analysis ───────────────────────────────────────────────

  describe('analyzeUrl()', () => {
    it('extracts page title and form elements from URL', async () => {
      // Mock URL — in real use this hits the page
      const result = await gen.analyzeUrl('https://example.com', { mock: true });
      expect(result.title).toBeDefined();
      expect(result.locators).toBeDefined();
    }, 10000);
  });

  describe('analyzeHtml()', () => {
    it('extracts locators from HTML snippet', async () => {
      const html = `
        <form id="login-form">
          <input type="email" data-testid="email-input" placeholder="Email" />
          <input type="password" data-testid="password-input" placeholder="Password" />
          <button type="submit" data-testid="submit-btn">Sign In</button>
        </form>
      `;
      const result = await gen.analyzeHtml(html);
      expect(result.locators).toBeDefined();
      expect(result.locators['email-input']).toContain('data-testid');
      expect(result.locators['password-input']).toContain('data-testid');
      expect(result.locators['submit-btn']).toContain('data-testid');
    });

    it('falls back to accessible selectors when no testid', async () => {
      const html = `
        <form>
          <input type="text" aria-label="Username" />
          <button role="button">Login</button>
        </form>
      `;
      const result = await gen.analyzeHtml(html);
      expect(Object.keys(result.locators).length).toBeGreaterThan(0);
    });
  });

  // ─── Error handling ─────────────────────────────────────────────────────────

  describe('error handling', () => {
    it('throws on unsupported framework', async () => {
      await expect(gen.generate({
        input: 'test',
        framework: 'cypress',
        codeType: 'standard'
      })).rejects.toThrow(/unsupported framework|not supported/i);
    });

    it('throws on unsupported code type', async () => {
      await expect(gen.generate({
        input: 'test',
        framework: 'pytest-playwright',
        codeType: 'visual-regression'
      })).rejects.toThrow(/unsupported code type|not supported/i);
    });

    it('throws on empty input', async () => {
      await expect(gen.generate({
        input: '',
        framework: 'pytest-playwright',
        codeType: 'standard'
      })).rejects.toThrow(/empty input/i);
    });
  });

  // ─── Parser ─────────────────────────────────────────────────────────────────

  describe('Parser', () => {
    const parser = new Parser();

    it('parses click actions', () => {
      const steps = parser.parse('Click the login button');
      expect(steps[0].action).toBe('click');
    });

    it('parses fill actions with value', () => {
      const steps = parser.parse('Fill username with "john"');
      expect(steps[0].action).toBe('fill');
      expect(steps[0].value).toBe('john');
    });

    it('parses press actions', () => {
      const steps = parser.parse('Press Enter');
      expect(steps[0].action).toBe('press');
      expect(steps[0].key).toBe('Enter');
    });

    it('parses navigate actions', () => {
      const steps = parser.parse('Go to https://example.com');
      expect(steps[0].action).toBe('navigate');
      expect(steps[0].url).toBe('https://example.com');
    });

    it('parses wait actions', () => {
      const steps = parser.parse('Wait for 3 seconds');
      expect(steps[0].action).toBe('wait');
      expect(steps[0].duration).toBe(3000);
    });

    it('parses assert actions', () => {
      const steps = parser.parse('Verify the title is "Dashboard"');
      expect(steps[0].action).toBe('assert');
    });

    it('parses multiple chained steps', () => {
      const steps = parser.parse(
        'Click login button, enter "user@test.com" in email, enter "pass123" in password, press Enter'
      );
      expect(steps.length).toBeGreaterThanOrEqual(4);
      expect(steps[0].action).toBe('click');
      expect(steps[1].action).toBe('fill');
      expect(steps[2].action).toBe('fill');
      expect(steps[3].action).toBe('press');
    });

    it('handles selector hints in natural language', () => {
      const steps = parser.parse('Click the button with id "submit-btn"');
      expect(steps[0].action).toBe('click');
      expect(steps[0].target).toContain('submit-btn');
    });
  });

  // ─── Locator Extractor ──────────────────────────────────────────────────────

  describe('LocatorExtractor', () => {
    it('prioritizes data-testid over other attributes', () => {
      const html = `<input data-testid="email" id="email-field" class="email-input" />`;
      const locators = LocatorExtractor.extract(html);
      expect(locators['email']).toContain('data-testid');
    });

    it('uses role+name for accessible elements', () => {
      const html = `<button role="button" aria-label="Close dialog">X</button>`;
      const locators = LocatorExtractor.extract(html);
      const btnLocator = Object.values(locators)[0];
      expect(btnLocator).toMatch(/role|aria/);
    });

    it('generates CSS selectors by default', () => {
      const html = `<div class="container"><span id="msg">Hello</span></div>`;
      const locators = LocatorExtractor.extract(html);
      expect(Object.values(locators)[0]).toMatch(/^#|\.|\[/);
    });

    it('extracts form input labels as names', () => {
      const html = `
        <form>
          <label for="username">Username</label>
          <input id="username" type="text" />
        </form>
      `;
      const locators = LocatorExtractor.extract(html);
      expect(locators['username']).toBeDefined();
    });
  });

  // ─── CLI integration ────────────────────────────────────────────────────────

  describe('CLI mode', () => {
    it('exposes generate command help', async () => {
      const result = await gen.cli(['--help']);
      expect(result.output).toContain('generate');
    });
  });
});

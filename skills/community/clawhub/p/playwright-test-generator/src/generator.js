/**
 * generator.js — Core code generation engine for Playwright tests.
 *
 * Supported:
 *   frameworks: pytest-playwright, jest-playwright, native-playwright
 *   codeTypes:  pom, standard, data-driven
 */

import { parse, stepToCode, toPascalCase } from './parser.js';
import { LocatorExtractor } from './locator.js';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ─── Framework / CodeType validation ─────────────────────────────────────────

const SUPPORTED_FRAMEWORKS = ['pytest-playwright', 'jest-playwright', 'native-playwright'];
const SUPPORTED_CODE_TYPES = ['pom', 'standard', 'data-driven'];

// ─── Python POM ───────────────────────────────────────────────────────────────

function generatePythonPom(data) {
  const { pageName = 'Page', steps = [], locators = {} } = data;
  const pascal = toPascalCase(pageName);
  // Avoid doubled suffix: 'LoginPage' → class LoginPage
  const baseName = pascal.replace(/Page$/i, '');
  const className = baseName + 'Page';
  const fixtureName = baseName.replace(/([A-Z])/g, '_$1').toLowerCase().replace(/^_/, '');
  const stepsCode = steps.map(s => stepToCode(s, '    ')).join('\n');

  const locatorsCode = Object.entries(locators).map(([name, sel]) => {
    const method = name.replace(/[\s_-]+/g, '_').toLowerCase();
    return `    @property\n    def ${method}(self):\n        return self.page.locator('${sel}')`;
  }).join('\n\n');

  return `"""Page Object Model for ${className}"""
import pytest
from playwright.sync_api import Page, expect


class ${className}:
    def __init__(self, page: Page):
        self.page = page

${locatorsCode}

    # ─── Actions ───────────────────────────────────────────

${stepsCode}

    # ─── Fixtures ─────────────────────────────────────────

@pytest.fixture
def ${fixtureName}(page: Page):
    return ${className}(page)
`;
}

// ─── Python Standard ─────────────────────────────────────────────────────────

function generatePythonStandard(data) {
  const { testName = 'test_playwright', steps = [] } = data;
  const stepsCode = steps.map(s => stepToCode(s, '    ')).join('\n');

  return `"""Standard Playwright test: ${testName}"""
import pytest
from playwright.sync_api import Page, expect


def ${testName}(page: Page):
${stepsCode}
`;
}

// ─── Python Data-Driven ───────────────────────────────────────────────────────

function generatePythonDataDriven(data) {
  const { pageName = 'Page', testName = 'test_login', testData = [], steps = [] } = data;
  const pascal = toPascalCase(pageName);
  const baseName = pascal.replace(/Page$/i, '');
  const className = baseName + 'Page';

  return `"""Data-driven Playwright test: ${testName}"""
import pytest
from playwright.sync_api import Page, expect


class ${className}:
    def __init__(self, page: Page):
        self.page = page

${steps.map(s => stepToCode(s, '    ')).join('\n')}


TEST_DATA = [
${testData.map(d => `    (${Object.values(d).map(v => `'${v}'`).join(', ')}),`).join('\n')}
]


@pytest.mark.parametrize("username,password", TEST_DATA)
def ${testName}(page: Page, username, password):
    page.goto("https://example.com")
    print(f"Testing with username={username}")
`;
}

// ─── Jest POM ────────────────────────────────────────────────────────────────

function generateJestPom(data) {
  const { pageName = 'Page', steps = [], language = 'typescript', locators = {} } = data;
  const pascal = toPascalCase(pageName);
  const baseName = pascal.replace(/Page$/i, '');
  const className = baseName + 'Page';
  const stepsCode = steps.map(s => stepToCode(s, '  ')).join('\n');
  const type = language === 'typescript' ? ': Locator' : '';

  return `// Page Object Model for ${className} (Jest + Playwright)
import { test, expect, Locator, Page } from '@playwright/test';

export class ${className} {
  readonly page: Page;

${Object.entries(locators).map(([name, sel]) => {
    const prop = name.replace(/[\s_-]+/g, '_').toLowerCase();
    return `  readonly ${prop}${type} = this.page.locator('${sel}');`;
  }).join('\n')}

  constructor(page: Page) {
    this.page = page;
  }

${steps.map(s => {
  const method = (s.target || 'action').replace(/[\s_-]+/g, '_').toLowerCase();
  return `  async ${method}() {\n    ${stepToCode(s, '    ').trim()}\n  }`;
}).join('\n\n')}
}
`;
}

// ─── Jest Standard ───────────────────────────────────────────────────────────

function generateJestStandard(data) {
  const { testName = 'example', steps = [], language = 'typescript' } = data;
  const importLine = language === 'typescript'
    ? "import { test, expect } from '@playwright/test';"
    : "const { test, expect } = require('@playwright/test');";

  return `${importLine}

// Test: ${testName}
test.describe('${testName}', () => {
  test('${testName}', async ({ page }) => {
${steps.map(s => stepToCode(s, '    ')).join('\n')}
  });
});
`;
}

// ─── Jest Data-Driven ────────────────────────────────────────────────────────

function generateJestDataDriven(data) {
  const { testName = 'login', testData = [], steps = [], language = 'typescript' } = data;
  const importLine = language === 'typescript'
    ? "import { test, expect } from '@playwright/test';"
    : "const { test, expect } = require('@playwright/test');";

  return `${importLine}

// Data-driven test: ${testName}
const TEST_DATA = [
${testData.map(d => `  { ${Object.entries(d).map(([k, v]) => `${k}: '${v}'`).join(', ')} }`).join(',\n')}
];

for (const data of TEST_DATA) {
  test(data.username + ' login test', async ({ page }) => {
    await page.goto('https://example.com');
    // Use data.username, data.password etc.
    console.log(data);
  });
}
`;
}

// ─── Native Standard ─────────────────────────────────────────────────────────

function generateNativeStandard(data) {
  const { testName = 'example', steps = [] } = data;

  return `// Playwright test: ${testName}
import { chromium } from 'playwright';

async function run() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
${steps.map(s => stepToCode(s, '    ')).join('\n')}
  } finally {
    await browser.close();
  }
}

run().catch(console.error);
`;
}

// ─── Native POM ──────────────────────────────────────────────────────────────

function generateNativePom(data) {
  const { pageName = 'Page', steps = [], locators = {} } = data;
  const pascal = toPascalCase(pageName);
  const baseName = pascal.replace(/Page$/i, '');
  const className = baseName + 'Page';

  return `// Page Object Model: ${className}
export class ${className} {
  constructor(page) {
    this.page = page;
${Object.entries(locators).map(([name, sel]) => {
    const prop = name.replace(/[\s_-]+/g, '_').toLowerCase();
    return `    this.${prop} = page.locator('${sel}');`;
  }).join('\n')}
  }
${steps.map(s => {
  const method = (s.target || 'action').replace(/[\s_-]+/g, '_').toLowerCase();
  return `
  async ${method}() {
    ${stepToCode(s, '    ').trim()}
  }`;
}).join('\n')}
}
`;
}

// ─── Native Data-Driven ──────────────────────────────────────────────────────

function generateNativeDataDriven(data) {
  const { testName = 'data_driven', testData = [], steps = [] } = data;

  return `// Data-driven Playwright test: ${testName}
import { chromium } from 'playwright';

const TEST_DATA = [
${testData.map(d => `  { ${Object.entries(d).map(([k, v]) => `${k}: '${v}'`).join(', ')} }`).join(',\n')}
];

async function runTest(data) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  try {
${steps.map(s => stepToCode(s, '    ')).join('\n')}
  } finally {
    await browser.close();
  }
}

TEST_DATA.forEach(runTest);
`;
}

// ─── Framework Dispatcher ────────────────────────────────────────────────────

function generateForFramework(data) {
  const { framework, codeType } = data;

  switch (`${framework}:${codeType}`) {
    case 'pytest-playwright:pom':        return generatePythonPom(data);
    case 'pytest-playwright:standard':   return generatePythonStandard(data);
    case 'pytest-playwright:data-driven': return generatePythonDataDriven(data);
    case 'jest-playwright:pom':         return generateJestPom(data);
    case 'jest-playwright:standard':    return generateJestStandard(data);
    case 'jest-playwright:data-driven': return generateJestDataDriven(data);
    case 'native-playwright:standard':  return generateNativeStandard(data);
    case 'native-playwright:pom':       return generateNativePom(data);
    case 'native-playwright:data-driven': return generateNativeDataDriven(data);
    default:
      throw new Error(`Unsupported combination: framework=${framework}, codeType=${codeType}`);
  }
}

// ─── Public API ──────────────────────────────────────────────────────────────

export class PlaywrightTestGenerator {
  constructor(options = {}) {
    this.options = options;
  }

  /**
   * Generate Playwright test code from natural language input.
   *
   * @param {Object} opts
   * @param {string} opts.input           Natural language test description
   * @param {string} opts.framework       pytest-playwright | jest-playwright | native-playwright
   * @param {string} opts.codeType        pom | standard | data-driven
   * @param {string} [opts.pageName]      Page name for POM generation
   * @param {string} [opts.testName]      Test function/file name
   * @param {string} [opts.baseUrl]       Base URL for navigation
   * @param {Array}  [opts.testData]      Data for data-driven tests
   * @param {string} [opts.language]      typescript | javascript (for Jest/native)
   * @param {Object} [opts.locators]      Pre-extracted locators map
   */
  async generate(opts = {}) {
    const {
      input,
      framework = 'pytest-playwright',
      codeType = 'standard',
      pageName = 'Page',
      testName = 'test_playwright',
      baseUrl = 'https://example.com',
      testData = [],
      language = 'javascript',
      locators = {}
    } = opts;

    // ── Validation ──
    if (!input || (typeof input === 'string' && !input.trim())) {
      throw new Error('Empty input: please provide a test description');
    }

    if (!SUPPORTED_FRAMEWORKS.includes(framework)) {
      throw new Error(
        `Unsupported framework: "${framework}". Supported: ${SUPPORTED_FRAMEWORKS.join(', ')}`
      );
    }

    if (!SUPPORTED_CODE_TYPES.includes(codeType)) {
      throw new Error(
        `Unsupported code type: "${codeType}". Supported: ${SUPPORTED_CODE_TYPES.join(', ')}`
      );
    }

    // ── Parse ──
    const steps = typeof input === 'string' ? parse(input) : input;

    // ── Generate ──
    let code;
    try {
      code = generateForFramework({
        framework, codeType, pageName, testName, baseUrl, testData,
        language, locators, steps
      });
    } catch (err) {
      throw new Error(`Code generation failed: ${err.message}`);
    }

    return {
      framework,
      codeType,
      language: framework === 'pytest-playwright' ? 'python' : (language || 'javascript'),
      pageName: toPascalCase(pageName),
      testName,
      steps,
      locators,
      code,
      warnings: []
    };
  }

  /**
   * Analyze a URL and extract page structure + locators.
   */
  async analyzeUrl(url, options = {}) {
    if (!url) throw new Error('URL is required for analyzeUrl');
    const { mock = false } = options;

    if (mock) {
      return {
        url,
        title: 'Mock Page Title',
        locators: {
          'main-heading': 'h1',
          'login-form': '#login-form',
          'username-input': '[data-testid="username-input"]',
          'password-input': '[data-testid="password-input"]',
          'submit-button': '[data-testid="submit-button"]'
        },
        elements: []
      };
    }

    // Real implementation
    const { chromium } = await import('playwright');
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded' });

    const html = await page.content();
    const title = await page.title();

    await browser.close();

    const { locators, elements } = LocatorExtractor.extract(html);
    return { url, title, locators, elements };
  }

  /**
   * Analyze HTML content and extract locators.
   */
  analyzeHtml(html) {
    if (!html || typeof html !== 'string') {
      throw new Error('HTML content is required for analyzeHtml');
    }
    const { locators, elements } = LocatorExtractor.extract(html);
    return { locators, elements };
  }

  /**
   * CLI handler — parses argv and returns { command, args }
   */
  async cli(argv = process.argv) {
    const [, , cmd] = argv;

    if (cmd === '--help' || cmd === '-h' || !cmd) {
      return {
        output: `playwright-test-generator <command>

Commands:
  generate       Generate test code from natural language
  analyze        Analyze URL and extract locators
  extract-locators Extract locators from HTML

Examples:
  playwright-test-generator generate \\
    --input "Click login, enter email and password" \\
    --framework pytest-playwright \\
    --type pom \\
    --page LoginPage

  playwright-test-generator analyze --url https://example.com

  playwright-test-generator extract-locators --html "$(cat form.html)"
`
      };
    }

    return { command: cmd };
  }
}

export default PlaywrightTestGenerator;

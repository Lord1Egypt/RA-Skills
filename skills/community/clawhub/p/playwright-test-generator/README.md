# playwright-test-generator

> AI-driven Playwright test code generator — generates POM, standard scripts, and data-driven tests from natural language descriptions or HTML analysis.

[![npm version](https://img.shields.io/badge/npm-v1.0.0-blue)](https://www.npmjs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🌐 **Natural Language → Test Code** — describe test steps in plain English, get production-ready Playwright scripts
- 📄 **Page/URL Analysis** — extract locators from HTML or URLs automatically
- 🏗️ **Page Object Model** — generate clean POM classes for pytest-playwright, jest-playwright, native Playwright
- 📊 **Data-Driven Tests** — generate parameterized test suites from test data
- 🐍 **Python (pytest)** — full pytest-playwright support
- ⚡ **JavaScript/TypeScript** — jest-playwright and native Playwright support
- 🔍 **Smart Locators** — prioritizes `data-testid` → role/name → CSS selectors

## Installation

```bash
npm install -g playwright-test-generator
# or locally
npm install playwright-test-generator
```

## Quick Start

### CLI

```bash
# Generate POM from natural language
playwright-test-generator generate \
  --input "Click login button, enter email and password, press Enter" \
  --framework pytest-playwright \
  --type pom \
  --page LoginPage

# Analyze URL and extract locators
playwright-test-generator analyze --url https://example.com --mock

# Extract locators from HTML
playwright-test-generator extract-locators --html '<input id="email" />'

# Interactive mode
playwright-test-generator interactive
```

### API

```javascript
import { PlaywrightTestGenerator } from 'playwright-test-generator';

const gen = new PlaywrightTestGenerator();

// Natural language → pytest-playwright POM
const result = await gen.generate({
  input: 'Click the login button, enter "user@test.com" in email, enter "secret" in password, press Enter',
  framework: 'pytest-playwright',
  codeType: 'pom',
  pageName: 'LoginPage'
});

console.log(result.code);        // Generated Python code
console.log(result.language);   // 'python'
console.log(result.steps);      // Parsed step objects

// Analyze HTML for locators
const { locators } = gen.analyzeHtml(`
  <form id="login">
    <input data-testid="email-input" type="email" />
    <input data-testid="password-input" type="password" />
    <button data-testid="submit-btn">Sign In</button>
  </form>
`);
console.log(locators);
// { 'email-input': '[data-testid="email-input"]', ... }
```

## Supported Frameworks

| Framework | Language | POM | Standard | Data-Driven |
|-----------|----------|-----|----------|-------------|
| pytest-playwright | Python | ✅ | ✅ | ✅ |
| jest-playwright | JS/TS | ✅ | ✅ | ✅ |
| native-playwright | JS/TS | ✅ | ✅ | ✅ |

## Input Examples

```bash
# Navigate + Click + Fill + Press
--input "Go to https://example.com, click the login button, enter 'user@test.com' in email, enter 'pass123' in password, press Enter"

# Wait + Assert
--input "Navigate to dashboard, wait for 2 seconds, verify the page title is 'Dashboard'"

# Data-driven
--input "Login with username and password from test data"
--test-data ./test_data.json
```

## Output: pytest-playwright POM

```python
"""Page Object Model for LoginPage"""
import pytest
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def email_input(self):
        return self.page.locator('[data-testid="email-input"]')

    def click_login_button(self):
        await self.page.click('button');

    def fill_email(self):
        await self.page.fill('[data-testid="email-input"]', 'user@test.com');

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)
```

## Locator Priority

1. `data-testid` — most reliable, explicit testing attribute
2. `id` — unique per page
3. `aria-label` — accessible names
4. `role` + accessible name — a11y-first
5. `label → for` — form associations
6. CSS class combinations
7. XPath — last resort

## CLI Reference

```
playwright-test-generator <command>

Commands:
  generate         Generate test code from natural language
  analyze          Analyze URL and extract page structure + locators
  extract-locators Extract locators from HTML snippet
  interactive      Guided interactive test generation

Options for generate:
  --input, -i          Natural language test description
  --framework, -f       pytest-playwright | jest-playwright | native-playwright
  --type, -t           pom | standard | data-driven
  --page               Page name for POM (default: Page)
  --test               Test function name
  --output, -o         Write output to file
  --test-data          JSON file with test data for data-driven tests
  --mock               Use mock data for analyze (for testing)
```

## Architecture

```
src/
├── index.js        # CLI entry point + command routing
├── generator.js    # Core code generation engine
├── parser.js       # NL → structured step parser
├── locator.js      # HTML → Playwright locator extractor
└── templates/     # Code generation templates (future)
```

## Development

```bash
# Run tests
node --experimental-vm-modules tests/run.js

# Run CLI
node src/index.js generate --input "Click the button" --framework pytest-playwright
```

## License

MIT — 申先生 & kay

---
name: playwright-test-generator
description: AI-driven Playwright test code generator for QA engineers. Generates Page Object Models, standard test scripts, and data-driven tests from natural language descriptions, HTML analysis, or page URLs. Supports pytest-playwright, Jest Playwright, and native Playwright. Activate when the user asks to "generate Playwright tests", "create test script", "build POM from page", or mentions Playwright test generation.
---

# Playwright Test Generator

An AI-powered skill that automatically generates Playwright test scripts from natural language descriptions, HTML/page analysis, or existing page URLs.

## When to Use

This skill activates when the user:
- Asks to "generate Playwright tests", "create test script", "build POM from page"
- Wants to convert natural language steps into test code
- Needs to analyze a page/URL and generate locators + test code
- Requests data-driven or Page Object Model test generation
- Mentions Playwright test generation for pytest, Jest, or native Playwright

## Input Types

### 1. Natural Language → Test Code
Provide test steps in plain English and get complete test scripts.

**Example:**
```
Input: "Login to the app with username and password, then verify dashboard loads"
Output: Complete pytest-playwright test with POM
```

### 2. Page/URL Analysis → Locators + POM
Provide a URL or HTML content to extract elements and generate Page Object Model.

**Example:**
```
Input: URL https://example.com/login
Output: login_page.py with all form element locators + methods
```

### 3. HTML Snippet → Element Locators
Provide HTML snippets to extract robust CSS/XPath selectors.

## Output Types (Code Genres)

| Genre | Description | Framework |
|-------|-------------|-----------|
| `pom` | Page Object Model | pytest-playwright / Jest Playwright |
| `standard` | Standard test script | pytest-playwright / native Playwright |
| `data-driven` | Parameterized data tests | pytest-playwright / Jest Playwright |
| `api` | API test helpers | Any |

## Framework Support

| Framework | Language | Code Type |
|-----------|----------|-----------|
| `pytest-playwright` | Python | pom, standard, data-driven |
| `jest-playwright` | JavaScript/TypeScript | pom, standard, data-driven |
| `native-playwright` | JavaScript/TypeScript | standard, pom |

## Usage

### Command Mode

```bash
# Generate from natural language
playwright-test-generator generate \
  --input "Click login button, enter username and password, click submit" \
  --framework pytest \
  --type pom \
  --output ./tests/

# Analyze URL and generate POM
playwright-test-generator analyze \
  --url https://example.com/login \
  --framework pytest \
  --output ./pages/

# Analyze HTML and generate locators
playwright-test-generator extract-locators \
  --html "$(cat form.html)" \
  --output ./locators.json
```

### Interactive Mode

```
playwright-test-generator interactive
```

Follow the guided wizard to generate tests step by step.

### API Mode (from other skills/agents)

```javascript
import { PlaywrightTestGenerator } from './src/generator.js';

const gen = new PlaywrightTestGenerator();
const result = await gen.generate({
  input: 'Click the search box, type "playwright", press Enter',
  framework: 'pytest-playwright',
  codeType: 'standard',
  pageName: 'search_page'
});
```

## Pricing / Tier

| Tier | Features | Rate |
|------|----------|------|
| Free | ≤10 generations/day, standard scripts only | 0 credits |
| Pro | Unlimited, POM + data-driven, priority | 1 credit/test |
| Enterprise | Custom frameworks, team features, SLA | Contact |

---

# Developer Guide

## Architecture

```
src/
├── index.js        # CLI entry + skill interface
├── generator.js    # Core code generation logic
├── parser.js       # NL → test steps parser
├── locator.js      # HTML → locator extractor
└── templates/      # Code generation templates
    ├── pytest_pom.py.ejs
    ├── pytest_standard.py.ejs
    ├── pytest_data_driven.py.ejs
    ├── jest_pom.ts.ejs
    ├── jest_standard.ts.ejs
    └── native_pom.ts.ejs
```

## Generator Pipeline

1. **Parse** NL input → structured test steps
2. **Extract** page elements (if URL/HTML provided)
3. **Select** template based on framework + code type
4. **Render** template with steps + locators
5. **Output** formatted code

## Test Steps Schema

```javascript
{
  action: 'click' | 'fill' | 'press' | 'navigate' | 'wait' | 'assert' | 'hover' | 'select' | 'check' | 'uncheck',
  target: string,        // CSS selector, XPath, or role-based
  value?: string,        // Input value or expected result
  options?: {
    timeout?: number,
    force?: boolean,
    expect?: 'visible' | 'hidden' | 'enabled' | 'disabled'
  }
}
```

## Locator Strategy

Priority order for element selection:
1. `data-testid` attribute (most reliable)
2. `role` + accessible name (a11y-first)
3. `id` attribute
4. CSS class + tag combinations
5. XPath (last resort)

## Template Variables

| Variable | Description |
|----------|-------------|
| `{{pageName}}` | Page object name (PascalCase) |
| `{{baseUrl}}` | Target URL |
| `{{steps}}` | Array of parsed test steps |
| `{{locators}}` | Map of element name → selector |
| `{{testData}}` | Data-driven test data |
| `{{framework}}` | Target framework |
| `{{imports}}` | Required imports |

## Error Handling

- Invalid input → error with suggestion
- Unsupported framework → list supported frameworks
- Generation failure → partial output + error report

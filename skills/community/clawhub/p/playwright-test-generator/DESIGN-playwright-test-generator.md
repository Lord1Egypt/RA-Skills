# Playwright Test Generator - Design Document

## 1. Concept & Vision

**What it does:** AI-powered Playwright test generator that transforms URLs, user stories, or page descriptions into production-ready test code.

**Target user:** QA engineers, test automation specialists, and developers who want to rapidly bootstrap Playwright tests without manual scaffolding work.

**Pain point solved:** Test engineers spend hours writing repetitive boilerplate code. This tool auto-generates test scaffolds, Page Objects, and test cases from natural input — letting engineers focus on test logic, not code typing.

---

## 2. Core Features

### 2.1 Input Types

| Input Type | Description |
|:---|:---|
| `--url` | Navigate to a URL, analyze DOM, generate tests |
| `--story` | Parse user story text → test cases |
| `--desc` | Parse feature description → test steps |

### 2.2 Output Capabilities

- **Basic Test Scripts** — Playwright test files with `page.goto`, `click`, `fill`, `assert` chains
- **Page Object Models** — Separate page classes with locators and action methods
- **Test Cases** — Gherkin-style or structured test steps
- **Multi-language** — Python (`pytest`) and JavaScript (`@playwright/test`)

### 2.3 CLI Commands

```bash
# Generate from URL
playwright-gen url https://example.com --lang python --output tests/

# Generate from user story
playwright-gen story "As a user I can login" --lang js --pom

# Generate from description
playwright-gen desc "Login flow: open page, fill form, submit, verify" --lang python

# Interactive mode
playwright-gen interactive
```

---

## 3. Architecture

```
playwright_test_generator/
├── SKILL.md                       # Skill metadata & usage
├── cli.py                         # Click-based CLI entry point
├── generator.py                   # Core generation orchestrator
├── playwright_test_generator.py   # Playwright page analysis logic
├── templates.py                   # Python & JS code templates
├── requirements.txt
├── README.md
└── tests/
    ├── test_cli.py
    ├── test_generator.py
    ├── test_templates.py
    └── test_playwright_generator.py
```

### 3.1 Module Responsibilities

| Module | Responsibility |
|:---|:---|
| `cli.py` | Argument parsing, command routing, output formatting |
| `generator.py` | Input parsing, flow orchestration, language dispatch |
| `playwright_test_generator.py` | Playwright browser interaction, DOM analysis |
| `templates.py` | Jinja2-based code template engine for Python/JS output |

---

## 4. Template System

### 4.1 Python Template (pytest-playwright)

```python
# Generated test file
import pytest
from playwright.sync_api import Page, expect

class TestExample:
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page

    def test_example(self):
        self.page.goto("https://example.com")
        # ... generated steps
```

### 4.2 JavaScript Template (@playwright/test)

```javascript
// Generated test file
const { test, expect } = require('@playwright/test');

test.describe('Example', () => {
  test('example test', async ({ page }) => {
    await page.goto('https://example.com');
    // ... generated steps
  });
});
```

### 4.3 Page Object Template (Python)

```python
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.submit_btn = page.locator('button[type="submit"]')

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_btn.click()
```

---

## 5. URL Analysis Flow

1. Launch browser (headless)
2. Navigate to URL
3. Extract: title, form inputs, buttons, links, headings
4. Identify: login forms, navigation, key interactions
5. Generate test code based on detected patterns

---

## 6. Pricing Tiers

| Tier | Price | Features |
|:---|:---|:---|
| Free | ¥0 | 10 tests/month, Python only, no POM |
| Pro | ¥19/mo | Unlimited, Python + JS, POM generation |
| Team | ¥49/mo | Pro + CI integration, custom templates, priority |

---

## 7. Test Strategy (TDD)

- **Unit tests** for each module (templates, generator logic, CLI parsing)
- **Mock** Playwright browser interactions for speed
- **Golden file tests** for template output validation

---

## 8. Constraints

- Single file ≤ 500 lines
- Python 3.9+ required
- Playwright must be installed (`playwright install`)
- Output encoding: UTF-8

---

## 9. File Size Budget

| File | Max Lines |
|:---|:---|
| cli.py | 150 |
| generator.py | 200 |
| templates.py | 300 |
| playwright_test_generator.py | 250 |
| Total | ~900 (within 1000 line project budget) |

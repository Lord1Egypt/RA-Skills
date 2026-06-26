"""
Code templates for Playwright test generation.
Supports Python (pytest-playwright) and JavaScript (@playwright/test).
"""
from typing import List, Dict, Any


class TemplateEngine:
    """Simple template engine for generating test code."""

    @staticmethod
    def render(template: str, context: Dict[str, Any]) -> str:
        """Render a template with context variables."""
        result = template
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result


# =============================================================================
# Python (pytest-playwright) Templates
# =============================================================================

PYTHON_TEST_TEMPLATE = '''\
"""Generated Playwright test - {title}."""
import pytest
from playwright.sync_api import Page, expect


class Test{class_name}:
    """{description}"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup fixture for each test."""
        self.page = page

{definitions}

{tests}
'''

PYTHON_TEST_METHOD_TEMPLATE = '''
    def {method_name}(self):
        """Test: {test_description}"""
{body}
'''

PYTHON_BASIC_TEST = '''
    def test_{test_name}(self):
        """Generated test case."""
{body}
'''


class PythonTemplates:
    """Python pytest-playwright template generators."""

    @staticmethod
    def generate_test_file(
        title: str,
        class_name: str,
        description: str,
        definitions: str,
        tests: str
    ) -> str:
        """Generate a complete Python test file."""
        return PYTHON_TEST_TEMPLATE.format(
            title=title,
            class_name=class_name,
            description=description,
            definitions=definitions,
            tests=tests
        )

    @staticmethod
    def generate_test(
        test_name: str,
        body: str,
        description: str = ""
    ) -> str:
        """Generate a single test method."""
        return PYTHON_BASIC_TEST.format(
            test_name=test_name,
            body=body,
            description=description
        )

    @staticmethod
    def generate_step_goto(url: str, base_url: str = "") -> str:
        """Generate a page.goto step."""
        if base_url and url.startswith("/"):
            full_url = f"{base_url.rstrip('/')}{url}"
        else:
            full_url = url
        return f'        self.page.goto("{full_url}")'

    @staticmethod
    def generate_step_click(selector: str, description: str = "") -> str:
        """Generate a click step."""
        desc = f'  # {description}' if description else ''
        return f'        self.page.click("{selector}"){desc}'

    @staticmethod
    def generate_step_fill(selector: str, value: str, description: str = "") -> str:
        """Generate a fill step."""
        desc = f'  # {description}' if description else ''
        return f'        self.page.fill("{selector}", "{value}"){desc}'

    @staticmethod
    def generate_step_type(selector: str, value: str, delay: int = 0, description: str = "") -> str:
        """Generate a type step with optional delay."""
        desc = f'  # {description}' if description else ''
        if delay > 0:
            return f'        self.page.type("{selector}", "{value}", delay={delay}){desc}'
        return f'        self.page.type("{selector}", "{value}"){desc}'

    @staticmethod
    def generate_step_assert_text(selector: str, expected: str) -> str:
        """Generate a text assertion."""
        return f'        expect(self.page.locator("{selector}")).to_have_text("{expected}")'

    @staticmethod
    def generate_step_assert_visible(selector: str) -> str:
        """Generate a visibility assertion."""
        return f'        expect(self.page.locator("{selector}")).to_be_visible()'

    @staticmethod
    def generate_step_assert_url(url_pattern: str) -> str:
        """Generate a URL assertion."""
        return f'        expect(self.page).to_have_url("{url_pattern}")'

    @staticmethod
    def generate_step_wait(selector: str = None, timeout: int = 30000) -> str:
        """Generate a wait step."""
        if selector:
            return f'        self.page.wait_for_selector("{selector}", timeout={timeout})'
        return f'        self.page.wait_for_timeout({timeout})'

    @staticmethod
    def generate_step_screenshot(name: str = "screenshot") -> str:
        """Generate a screenshot step."""
        return f'        self.page.screenshot(path="{name}.png")'


# =============================================================================
# JavaScript (@playwright/test) Templates
# =============================================================================

JS_TEST_TEMPLATE = '''\
// Generated Playwright test - {title}
// Language: JavaScript (@playwright/test)
const {{ test, expect }} = require('@playwright/test');

test.describe('{class_name}', () => {{
{description}

{tests}
}});
'''

JS_TEST_METHOD_TEMPLATE = '''
  test('{test_name}', async ({{ page }}) => {{
{body}
  }});
'''


class JavaScriptTemplates:
    """JavaScript @playwright/test template generators."""

    @staticmethod
    def generate_test_file(
        title: str,
        class_name: str,
        description: str,
        tests: str
    ) -> str:
        """Generate a complete JavaScript test file."""
        return JS_TEST_TEMPLATE.format(
            title=title,
            class_name=class_name,
            description=description,
            tests=tests
        )

    @staticmethod
    def generate_test(test_name: str, body: str) -> str:
        """Generate a single test method."""
        return JS_TEST_METHOD_TEMPLATE.format(
            test_name=test_name,
            body=body
        )

    @staticmethod
    def generate_step_goto(url: str) -> str:
        """Generate a page.goto step."""
        return f'    await page.goto(\'{url}\');'

    @staticmethod
    def generate_step_click(selector: str, description: str = "") -> str:
        """Generate a click step."""
        desc = f'  // {description}' if description else ''
        return f'    await page.click(\'{selector}\');{desc}'

    @staticmethod
    def generate_step_fill(selector: str, value: str, description: str = "") -> str:
        """Generate a fill step."""
        desc = f'  // {description}' if description else ''
        return f'    await page.fill(\'{selector}\', \'{value}\');{desc}'

    @staticmethod
    def generate_step_type(selector: str, value: str, delay: int = 0, description: str = "") -> str:
        """Generate a type step with optional delay."""
        desc = f'  // {description}' if description else ''
        if delay > 0:
            return f'    await page.type(\'{selector}\', \'{value}\', {{ delay: {delay} }});{desc}'
        return f'    await page.type(\'{selector}\', \'{value}\');{desc}'

    @staticmethod
    def generate_step_assert_text(selector: str, expected: str) -> str:
        """Generate a text assertion."""
        return f'    await expect(page.locator(\'{selector}\')).toHaveText(\'{expected}\');'

    @staticmethod
    def generate_step_assert_visible(selector: str) -> str:
        """Generate a visibility assertion."""
        return f'    await expect(page.locator(\'{selector}\')).toBeVisible();'

    @staticmethod
    def generate_step_assert_url(url_pattern: str) -> str:
        """Generate a URL assertion."""
        return f'    await expect(page).toHaveURL(\'{url_pattern}\');'

    @staticmethod
    def generate_step_wait(selector: str = None, timeout: int = 30000) -> str:
        """Generate a wait step."""
        if selector:
            return f'    await page.waitForSelector(\'{selector}\', {{ timeout: {timeout} }});'
        return f'    await page.wait({timeout});'

    @staticmethod
    def generate_step_screenshot(name: str = "screenshot") -> str:
        """Generate a screenshot step."""
        return f'    await page.screenshot({{ path: \'{name}.png\' }});'


# =============================================================================
# Page Object Model Templates
# =============================================================================

PYTHON_POM_TEMPLATE = '''\
"""Page Object Model - {page_name}."""
from playwright.sync_api import Page


class {class_name}:
    """Page object for {page_name}."""

    def __init__(self, page: Page):
        """Initialize page object."""
        self.page = page

{locators}

{methods}
'''

PYTHON_LOCATOR_PROPERTY = '''
    @property
    def {name}(self):
        """Locator for {name}."""
        return self.page.locator("{selector}")
'''

PYTHON_POM_METHOD = '''
    def {method_name}(self{params}):
        """{description}."""
{body}
'''


class PageObjectTemplates:
    """Page Object Model template generators."""

    @staticmethod
    def generate_page_object(
        page_name: str,
        locators: List[Dict[str, str]],
        methods: List[Dict[str, Any]]
    ) -> str:
        """Generate a complete Page Object Model class."""
        class_name = PageObjectTemplates._to_class_name(page_name)
        
        locator_code = "\n".join(
            PYTHON_LOCATOR_PROPERTY.format(
                name=loc.get('name', 'element'),
                selector=loc.get('selector', '')
            )
            for loc in locators
        ) if locators else "    pass"

        method_code = "\n".join(
            PythonTemplates.generate_step_screenshot.__doc__  # Placeholder
            for _ in methods
        ) if methods else ""

        return PYTHON_POM_TEMPLATE.format(
            page_name=page_name,
            class_name=class_name,
            locators=locator_code,
            methods=method_code
        )

    @staticmethod
    def _to_class_name(page_name: str) -> str:
        """Convert page name to valid Python class name."""
        words = page_name.replace('-', ' ').replace('_', ' ').split()
        return ''.join(word.capitalize() for word in words) + 'Page'

    @staticmethod
    def generate_locator(name: str, selector: str, locator_type: str = "css") -> Dict[str, str]:
        """Generate a locator definition."""
        if locator_type == "xpath":
            selector = f"xpath={selector}"
        elif locator_type == "text":
            selector = f"text={selector}"
        return {"name": name, "selector": selector}

    @staticmethod
    def generate_pom_method(
        method_name: str,
        steps: List[str],
        params: str = "",
        description: str = ""
    ) -> Dict[str, Any]:
        """Generate a Page Object method."""
        body_lines = [f'        """{description}."""' if description else '']
        body_lines.extend(f'        {step}' for step in steps)
        return {
            'method_name': method_name,
            'params': params,
            'description': description,
            'body': '\n'.join(body_lines)
        }


# =============================================================================
# Gherkin / BDD Template
# =============================================================================

GHERKIN_TEMPLATE = '''\
Feature: {feature_name}

{scenarios}
'''

GHERKIN_SCENARIO = '''\
  Scenario: {scenario_name}
{steps}
'''

GHERKIN_STEP = '''\
    Given {step_text}
'''


class GherkinTemplates:
    """Gherkin BDD template generators."""

    @staticmethod
    def generate_feature(feature_name: str, scenarios: str) -> str:
        """Generate a complete Gherkin feature file."""
        return GHERKIN_TEMPLATE.format(
            feature_name=feature_name,
            scenarios=scenarios
        )

    @staticmethod
    def generate_scenario(scenario_name: str, steps: List[str]) -> str:
        """Generate a Gherkin scenario."""
        step_lines = '\n'.join(
            GHERKIN_STEP.format(step_text=step) for step in steps
        )
        return GHERKIN_SCENARIO.format(
            scenario_name=scenario_name,
            steps=step_lines
        )

    @staticmethod
    def step_given(text: str) -> str:
        return f"Given {text}"

    @staticmethod
    def step_when(text: str) -> str:
        return f"When {text}"

    @staticmethod
    def step_then(text: str) -> str:
        return f"Then {text}"

    @staticmethod
    def step_and(text: str) -> str:
        return f"And {text}"


# =============================================================================
# Utility functions
# =============================================================================

def generate_test_steps(steps: List[Dict[str, str]], language: str = "python") -> str:
    """Generate test steps from a list of step definitions.
    
    Args:
        steps: List of dicts with 'action' and 'selector'/'value' keys
        language: 'python' or 'js'
    
    Returns:
        Generated code string
    """
    if language == "python":
        templates = PythonTemplates
        indent = "        "
    else:
        templates = JavaScriptTemplates
        indent = "    "

    lines = []
    for step in steps:
        action = step.get('action', '')
        selector = step.get('selector', '')
        value = step.get('value', '')
        description = step.get('description', '')
        delay = step.get('delay', 0)

        if action == 'goto':
            line = templates.generate_step_goto(selector)
        elif action == 'click':
            line = templates.generate_step_click(selector, description)
        elif action == 'fill':
            line = templates.generate_step_fill(selector, value, description)
        elif action == 'type':
            line = templates.generate_step_type(selector, value, delay, description)
        elif action == 'assert_text':
            line = templates.generate_step_assert_text(selector, value)
        elif action == 'assert_visible':
            line = templates.generate_step_assert_visible(selector)
        elif action == 'assert_url':
            line = templates.generate_step_assert_url(selector)
        elif action == 'wait':
            line = templates.generate_step_wait(selector, step.get('timeout', 30000))
        elif action == 'screenshot':
            line = templates.generate_step_screenshot(value or 'screenshot')
        else:
            line = f"{indent}# Unknown action: {action}"

        lines.append(line)

    return '\n'.join(lines)

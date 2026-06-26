"""
Tests for templates module.
"""
import pytest
from templates import (
    TemplateEngine,
    PythonTemplates,
    JavaScriptTemplates,
    PageObjectTemplates,
    GherkinTemplates,
    generate_test_steps,
    PYTHON_TEST_TEMPLATE,
    JS_TEST_TEMPLATE,
    PYTHON_POM_TEMPLATE
)


class TestTemplateEngine:
    """Tests for TemplateEngine."""

    def test_render_simple(self):
        """Simple template rendering should work."""
        template = "Hello, {{name}}!"
        result = TemplateEngine.render(template, {'name': 'World'})
        
        assert result == "Hello, World!"

    def test_render_multiple(self):
        """Multiple placeholders should be replaced."""
        template = "{{greeting}}, {{name}}!"
        result = TemplateEngine.render(template, {'greeting': 'Hi', 'name': 'Test'})
        
        assert result == "Hi, Test!"

    def test_render_missing_key(self):
        """Missing keys should remain as placeholders."""
        template = "Hello, {{name}}!"
        result = TemplateEngine.render(template, {})
        
        assert result == "Hello, {{name}}!"

    def test_render_numeric(self):
        """Numeric values should be converted to strings."""
        template = "Count: {{count}}"
        result = TemplateEngine.render(template, {'count': 42})
        
        assert result == "Count: 42"


class TestPythonTemplates:
    """Tests for PythonTemplates."""

    def test_generate_test_file(self):
        """Test file generation."""
        code = PythonTemplates.generate_test_file(
            title="Test Title",
            class_name="TestClass",
            description="Test description",
            definitions="",
            tests="    def test_example(self):\n        pass"
        )
        
        assert "Test Title" in code
        assert "TestClass" in code
        assert "Test description" in code

    def test_generate_test(self):
        """Single test generation."""
        code = PythonTemplates.generate_test(
            test_name="example",
            body='        self.page.goto("https://example.com")',
            description="Example test"
        )
        
        assert "example" in code
        assert 'def test_example' in code

    def test_generate_step_goto(self):
        """Goto step generation."""
        step = PythonTemplates.generate_step_goto("https://example.com")
        
        assert 'goto' in step
        assert 'example.com' in step

    def test_generate_step_goto_with_base(self):
        """Goto with base URL."""
        step = PythonTemplates.generate_step_goto("/login", base_url="https://example.com")
        
        assert 'example.com' in step
        assert 'login' in step

    def test_generate_step_click(self):
        """Click step generation."""
        step = PythonTemplates.generate_step_click("#submit", "Submit button")
        
        assert 'click' in step
        assert '#submit' in step
        assert 'Submit button' in step

    def test_generate_step_fill(self):
        """Fill step generation."""
        step = PythonTemplates.generate_step_fill("#email", "test@example.com")
        
        assert 'fill' in step
        assert '#email' in step
        assert 'test@example.com' in step

    def test_generate_step_type(self):
        """Type step generation."""
        step = PythonTemplates.generate_step_type("#input", "text", delay=100)
        
        assert 'type' in step
        assert 'delay=100' in step

    def test_generate_step_assert_text(self):
        """Assert text generation."""
        step = PythonTemplates.generate_step_assert_text("#result", "Success")
        
        assert 'have_text' in step or 'assert' in step.lower()
        assert 'Success' in step

    def test_generate_step_assert_visible(self):
        """Assert visible generation."""
        step = PythonTemplates.generate_step_assert_visible("#element")
        
        assert 'visible' in step or 'be_visible' in step

    def test_generate_step_assert_url(self):
        """Assert URL generation."""
        step = PythonTemplates.generate_step_assert_url("https://example.com/*")
        
        assert 'url' in step.lower()
        assert 'example.com' in step

    def test_generate_step_wait(self):
        """Wait step generation."""
        step = PythonTemplates.generate_step_wait("#element", timeout=5000)
        
        assert 'wait' in step.lower()
        assert '5000' in step

    def test_generate_step_screenshot(self):
        """Screenshot step generation."""
        step = PythonTemplates.generate_step_screenshot("my_screenshot")
        
        assert 'screenshot' in step.lower()
        assert 'my_screenshot' in step


class TestJavaScriptTemplates:
    """Tests for JavaScriptTemplates."""

    def test_generate_test_file(self):
        """JS test file generation."""
        code = JavaScriptTemplates.generate_test_file(
            title="Test Title",
            class_name="TestClass",
            description="Test description",
            tests=""
        )
        
        assert "Test Title" in code
        assert "@playwright/test" in code

    def test_generate_test(self):
        """Single JS test generation."""
        code = JavaScriptTemplates.generate_test(
            test_name="example test",
            body='    await page.goto("https://example.com");'
        )
        
        assert "example test" in code
        assert 'page.goto' in code

    def test_generate_step_goto(self):
        """JS goto step."""
        step = JavaScriptTemplates.generate_step_goto("https://example.com")
        
        assert 'page.goto' in step
        assert 'example.com' in step

    def test_generate_step_click(self):
        """JS click step."""
        step = JavaScriptTemplates.generate_step_click("#submit")
        
        assert 'page.click' in step
        assert '#submit' in step

    def test_generate_step_fill(self):
        """JS fill step."""
        step = JavaScriptTemplates.generate_step_fill("#email", "test@test.com")
        
        assert 'page.fill' in step
        assert 'test@test.com' in step

    def test_generate_step_type(self):
        """JS type step."""
        step = JavaScriptTemplates.generate_step_type("#input", "text", delay=50)
        
        assert 'page.type' in step
        assert 'delay' in step

    def test_generate_step_assert_text(self):
        """JS assert text."""
        step = JavaScriptTemplates.generate_step_assert_text("#result", "Success")
        
        assert 'toHaveText' in step or 'expect' in step
        assert 'Success' in step

    def test_generate_step_assert_visible(self):
        """JS assert visible."""
        step = JavaScriptTemplates.generate_step_assert_visible("#element")
        
        assert 'toBeVisible' in step or 'visible' in step

    def test_generate_step_screenshot(self):
        """JS screenshot step."""
        step = JavaScriptTemplates.generate_step_screenshot("my_screenshot")
        
        assert 'screenshot' in step.lower()


class TestPageObjectTemplates:
    """Tests for PageObjectTemplates."""

    def test_to_class_name(self):
        """Class name conversion."""
        name = PageObjectTemplates._to_class_name("login page")
        
        # Should produce a valid class name
        assert name is not None
        assert len(name) > 0
        assert name[-4:] == "Page" or name.endswith("Login")

    def test_to_class_name_multiple_words(self):
        """Multiple words conversion."""
        name = PageObjectTemplates._to_class_name("user registration form")
        
        assert "User" in name
        assert "Registration" in name
        assert "Form" in name

    def test_generate_locator(self):
        """Locator generation."""
        locator = PageObjectTemplates.generate_locator("email", "#email")
        
        assert locator['name'] == 'email'
        assert locator['selector'] == '#email'

    def test_generate_locator_xpath(self):
        """XPath locator generation."""
        locator = PageObjectTemplates.generate_locator(
            "submit",
            "//button[@type='submit']",
            locator_type="xpath"
        )
        
        assert 'submit' in locator['name']
        assert 'xpath' in locator['selector']


class TestGherkinTemplates:
    """Tests for GherkinTemplates."""

    def test_generate_feature(self):
        """Feature file generation."""
        code = GherkinTemplates.generate_feature(
            "Login Feature",
            "  Scenario: Login\n    Given I am on the login page\n"
        )
        
        assert "Feature: Login Feature" in code
        assert "Scenario: Login" in code

    def test_generate_scenario(self):
        """Scenario generation."""
        code = GherkinTemplates.generate_scenario(
            "User can login",
            ["Given I am on the login page", "When I enter credentials", "Then I should be logged in"]
        )
        
        assert "Scenario: User can login" in code
        assert "Given" in code
        assert "When" in code
        assert "Then" in code

    def test_step_given(self):
        """Given step generation."""
        step = GherkinTemplates.step_given("I am on the login page")
        
        assert step.startswith("Given")
        assert "login page" in step

    def test_step_when(self):
        """When step generation."""
        step = GherkinTemplates.step_when("I click submit")
        
        assert step.startswith("When")

    def test_step_then(self):
        """Then step generation."""
        step = GherkinTemplates.step_then("I see success message")
        
        assert step.startswith("Then")

    def test_step_and(self):
        """And step generation."""
        step = GherkinTemplates.step_and("I fill in the form")
        
        assert step.startswith("And")


class TestGenerateTestSteps:
    """Tests for generate_test_steps function."""

    def test_generate_steps_goto_python(self):
        """Goto step in Python."""
        steps = [{'action': 'goto', 'selector': 'https://example.com'}]
        
        code = generate_test_steps(steps, 'python')
        
        assert 'goto' in code
        assert 'example.com' in code

    def test_generate_steps_goto_js(self):
        """Goto step in JavaScript."""
        steps = [{'action': 'goto', 'selector': 'https://example.com'}]
        
        code = generate_test_steps(steps, 'js')
        
        assert 'page.goto' in code

    def test_generate_steps_click(self):
        """Click step generation."""
        steps = [{'action': 'click', 'selector': '#submit'}]
        
        code = generate_test_steps(steps, 'python')
        
        assert 'click' in code
        assert '#submit' in code

    def test_generate_steps_fill(self):
        """Fill step generation."""
        steps = [{'action': 'fill', 'selector': '#email', 'value': 'test@test.com'}]
        
        code = generate_test_steps(steps, 'python')
        
        assert 'fill' in code
        assert 'test@test.com' in code

    def test_generate_steps_assert(self):
        """Assertion step generation."""
        steps = [{'action': 'assert_text', 'selector': '#result', 'value': 'Success'}]
        
        code = generate_test_steps(steps, 'python')
        
        assert 'assert' in code.lower() or 'expect' in code.lower()

    def test_generate_steps_multiple(self):
        """Multiple steps generation."""
        steps = [
            {'action': 'goto', 'selector': 'https://example.com'},
            {'action': 'click', 'selector': '#submit'},
            {'action': 'assert_visible', 'selector': '#result'}
        ]
        
        code = generate_test_steps(steps, 'python')
        
        assert 'goto' in code
        assert 'click' in code
        assert 'visible' in code

    def test_generate_steps_unknown_action(self):
        """Unknown action should include comment."""
        steps = [{'action': 'unknown', 'selector': 'something'}]
        
        code = generate_test_steps(steps, 'python')
        
        assert 'Unknown action' in code or '#' in code

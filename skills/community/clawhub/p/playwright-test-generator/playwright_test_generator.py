"""
Core Playwright test generator module.
Handles page analysis, DOM extraction, and test generation from URLs.
"""
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


class PageAnalyzer:
    """Analyzes a Playwright page and extracts testable elements."""

    def __init__(self, page):
        """Initialize with a Playwright page object."""
        self.page = page

    def extract_title(self) -> str:
        """Extract page title."""
        return self.page.title()

    def extract_url(self) -> str:
        """Extract current URL."""
        return self.page.url

    def extract_forms(self) -> List[Dict[str, Any]]:
        """Extract all forms and their fields."""
        forms = []
        form_elements = self.page.query_selector_all('form')
        
        for form in form_elements:
            form_data = {
                'action': form.get_attribute('action') or '',
                'method': form.get_attribute('method') or 'get',
                'fields': []
            }
            
            inputs = form.query_selector_all('input')
            for inp in inputs:
                field = {
                    'tag': 'input',
                    'type': inp.get_attribute('type') or 'text',
                    'name': inp.get_attribute('name') or '',
                    'id': inp.get_attribute('id') or '',
                    'placeholder': inp.get_attribute('placeholder') or '',
                    'required': inp.get_attribute('required') is not None
                }
                form_data['fields'].append(field)
            
            textareas = form.query_selector_all('textarea')
            for ta in textareas:
                field = {
                    'tag': 'textarea',
                    'name': ta.get_attribute('name') or '',
                    'id': ta.get_attribute('id') or '',
                    'placeholder': ta.get_attribute('placeholder') or '',
                    'required': ta.get_attribute('required') is not None
                }
                form_data['fields'].append(field)
            
            selects = form.query_selector_all('select')
            for sel in selects:
                field = {
                    'tag': 'select',
                    'name': sel.get_attribute('name') or '',
                    'id': sel.get_attribute('id') or '',
                    'required': sel.get_attribute('required') is not None
                }
                form_data['fields'].append(field)
            
            forms.append(form_data)
        
        return forms

    def extract_buttons(self) -> List[Dict[str, str]]:
        """Extract all buttons."""
        buttons = []
        button_elements = self.page.query_selector_all('button, input[type="submit"], input[type="button"]')
        
        for btn in button_elements:
            button_data = {
                'text': btn.inner_text().strip() if hasattr(btn, 'inner_text') else '',
                'type': btn.get_attribute('type') or 'submit',
                'id': btn.get_attribute('id') or '',
                'class': btn.get_attribute('class') or '',
                'selector': self._generate_selector(btn)
            }
            buttons.append(button_data)
        
        return buttons

    def extract_links(self) -> List[Dict[str, str]]:
        """Extract navigation links."""
        links = []
        link_elements = self.page.query_selector_all('a[href]')
        
        for link in link_elements[:20]:  # Limit to first 20
            href = link.get_attribute('href') or ''
            if href and not href.startswith('#') and not href.startswith('javascript'):
                links.append({
                    'text': link.inner_text().strip()[:50] if hasattr(link, 'inner_text') else '',
                    'href': href,
                    'selector': self._generate_selector(link)
                })
        
        return links

    def extract_headings(self) -> List[str]:
        """Extract page headings."""
        headings = []
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            elements = self.page.query_selector_all(level)
            for el in elements[:3]:
                text = el.inner_text().strip() if hasattr(el, 'inner_text') else ''
                if text:
                    headings.append(f"{level}: {text}")
        return headings

    def extract_inputs(self) -> List[Dict[str, str]]:
        """Extract all input elements."""
        inputs = []
        input_elements = self.page.query_selector_all('input, textarea')
        
        for inp in input_elements:
            inputs.append({
                'type': inp.get_attribute('type') or 'text',
                'name': inp.get_attribute('name') or '',
                'id': inp.get_attribute('id') or '',
                'placeholder': inp.get_attribute('placeholder') or '',
                'selector': self._generate_selector(inp)
            })
        
        return inputs

    def suggest_locators(self, tag: str = None, attrs: Dict[str, str] = None) -> List[str]:
        """Suggest possible locators for an element."""
        locators = []
        
        if attrs:
            if attrs.get('id'):
                locators.append(f"#{attrs['id']}")
            if attrs.get('name'):
                locators.append(f"[name=\"{attrs['name']}\"]")
            if attrs.get('placeholder'):
                locators.append(f"[placeholder=\"{attrs['placeholder']}\"]")
            if attrs.get('type'):
                locators.append(f"input[type=\"{attrs['type']}\"]")
            if attrs.get('class'):
                classes = attrs['class'].split()
                if classes:
                    locators.append(f".{classes[0]}")
        
        locators.append(f"{tag or 'element'}")
        return locators

    def _generate_selector(self, element) -> str:
        """Generate a unique CSS selector for an element."""
        tag = element._as_dict().get('tagName', 'element').lower() if hasattr(element, '_as_dict') else 'element'
        
        el_id = element.get_attribute('id') if hasattr(element, 'get_attribute') else ''
        if el_id:
            return f"#{el_id}"
        
        el_class = element.get_attribute('class') if hasattr(element, 'get_attribute') else ''
        if el_class:
            classes = el_class.split()
            if classes:
                return f"{tag}.{classes[0]}"
        
        return tag

    def detect_page_type(self) -> str:
        """Detect the type of page (login, form, listing, etc.)."""
        url = self.extract_url().lower()
        title = self.extract_title().lower()
        
        if any(kw in url for kw in ['login', 'signin', 'auth']):
            return 'login'
        if any(kw in url for kw in ['register', 'signup', 'join']):
            return 'registration'
        if any(kw in url for kw in ['checkout', 'cart', 'order']):
            return 'checkout'
        if any(kw in title for kw in ['login', 'sign in', 'signin']):
            return 'login'
        
        forms = self.extract_forms()
        if forms:
            return 'form'
        
        return 'general'


def generate_from_url(url: str, language: str = 'python', pom: bool = False) -> str:
    """Generate test code from a URL.
    
    Args:
        url: Target URL to analyze
        language: 'python' or 'js'
        pom: Generate Page Object Model if True
    
    Returns:
        Generated test code string
    """
    from playwright.sync_api import sync_playwright
    
    code_blocks = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(1000)  # Give dynamic content time
            
            analyzer = PageAnalyzer(page)
            
            if pom:
                code_blocks.append(_generate_pom_code(analyzer, language))
            else:
                code_blocks.append(_generate_test_code(analyzer, language))
            
        finally:
            page.close()
            context.close()
            browser.close()
    
    return '\n\n'.join(code_blocks)


def _generate_test_code(analyzer: PageAnalyzer, language: str) -> str:
    """Generate test code from page analysis."""
    from templates import PythonTemplates, JavaScriptTemplates, generate_test_steps
    
    title = analyzer.extract_title()
    url = analyzer.extract_url()
    page_type = analyzer.detect_page_type()
    
    if language == 'python':
        templates = PythonTemplates
        indent = "        "
        test_file = '''\
"""Generated Playwright test - {title}."""
import pytest
from playwright.sync_api import Page, expect


class Test{class_name}:
    """Test class for {title}"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page

'''
    else:
        templates = JavaScriptTemplates
        indent = "    "
        test_file = '''\
// Generated Playwright test - {title}
// Language: JavaScript (@playwright/test)
const {{ test, expect }} = require('@playwright/test');

test.describe('{class_name}', () => {{
  test.beforeEach(async ({{ page }}) => {{
    // Setup
  }});

'''

    forms = analyzer.extract_forms()
    buttons = analyzer.extract_buttons()
    links = analyzer.extract_links()
    inputs = analyzer.extract_inputs()
    
    steps = []
    
    # Navigation step
    if language == 'python':
        steps.append(f'{indent}self.page.goto("{url}")')
    else:
        steps.append(f'    await page.goto(\'{url}\');')
    
    # Form handling
    if forms and page_type in ['login', 'registration', 'form']:
        for form in forms[:1]:  # Process first form
            for field in form.get('fields', []):
                if field.get('type') in ['text', 'email', 'password', 'search']:
                    selector = field.get('id') or field.get('name') or f'[placeholder="{field.get("placeholder")}"]'
                    if selector:
                        if language == 'python':
                            steps.append(f'{indent}self.page.fill("#{selector}", "test_value")')
                        else:
                            steps.append(f'    await page.fill(\'#{selector}\', \'test_value\');')
    
    # Buttons
    for btn in buttons[:2]:
        selector = btn.get('selector', '')
        if language == 'python':
            steps.append(f'{indent}self.page.click("{selector}")  # {btn.get("text", "")}')
        else:
            steps.append(f'    await page.click(\'{selector}\');  // {btn.get("text", "")}')
    
    # Assertions
    if language == 'python':
        steps.append(f'{indent}# Assertions')
        steps.append(f'{indent}expect(self.page).to_have_url(/{urlparse(url).netloc}/)')
    else:
        steps.append(f'    // Assertions')
        steps.append(f'    await expect(page).toHaveURL(/{urlparse(url).netloc}/);')
    
    body = '\n'.join(steps)
    
    if language == 'python':
        class_name = _to_class_name(title) or 'Page'
        test_file += f'''    def test_{page_type.replace('_', '_')}(self):
        """Generated {page_type} test."""
{body}

'''
        test_file += '```\n\n'
        return test_file
    else:
        test_file += f'''  test('{page_type} test', async ({{ page }}) => {{
{body}
  }});
}});
'''
        return test_file


def _generate_pom_code(analyzer: PageAnalyzer, language: str) -> str:
    """Generate Page Object Model code."""
    from templates import PageObjectTemplates
    
    title = analyzer.extract_title()
    inputs = analyzer.extract_inputs()
    buttons = analyzer.extract_buttons()
    forms = analyzer.extract_forms()
    
    locators = []
    
    # Generate locators for inputs
    for inp in inputs:
        name = inp.get('name') or inp.get('id') or inp.get('placeholder') or f'input_{inp.get("type")}'
        selector = inp.get('selector') or f'#{inp.get("id")}' if inp.get('id') else f'[name="{inp.get("name")}"]'
        locators.append(PageObjectTemplates.generate_locator(name, selector))
    
    # Generate locators for buttons
    for btn in buttons[:5]:
        name = btn.get('text') or btn.get('id') or 'button'
        selector = btn.get('selector', '')
        if selector:
            locators.append(PageObjectTemplates.generate_locator(name, selector))
    
    pom_code = PageObjectTemplates.generate_page_object(
        page_name=title,
        locators=locators,
        methods=[]
    )
    
    return pom_code


def parse_user_story(story: str) -> List[str]:
    """Parse a user story into test steps.
    
    Args:
        story: User story text (e.g., "As a user I can login...")
    
    Returns:
        List of parsed steps
    """
    steps = []
    
    story_lower = story.lower()
    
    # Common action verbs
    if any(kw in story_lower for kw in ['login', 'sign in', 'log in']):
        steps.extend([
            'Navigate to login page',
            'Fill in username/email',
            'Fill in password',
            'Click submit button',
            'Verify successful login'
        ])
    elif any(kw in story_lower for kw in ['register', 'sign up', 'signup']):
        steps.extend([
            'Navigate to registration page',
            'Fill in required fields',
            'Click register button',
            'Verify account creation'
        ])
    elif any(kw in story_lower for kw in ['search', 'find']):
        steps.extend([
            'Navigate to search page',
            'Enter search query',
            'Click search button',
            'Verify search results'
        ])
    elif any(kw in story_lower for kw in ['add', 'cart', 'buy', 'purchase']):
        steps.extend([
            'Navigate to product page',
            'Add item to cart',
            'Go to checkout',
            'Enter payment details',
            'Place order'
        ])
    else:
        # Generic parsing
        words = story.split()
        for i, word in enumerate(words):
            if word.lower() in ['login', 'click', 'fill', 'submit', 'open', 'navigate', 'enter']:
                steps.append(f'Perform action: {word}')
    
    return steps if steps else ['Navigate to page', 'Perform actions', 'Verify results']


def parse_description(desc: str) -> List[str]:
    """Parse a description text into test steps.
    
    Args:
        desc: Description text with comma-separated or sequential actions
    
    Returns:
        List of parsed steps
    """
    steps = []
    
    # Split by common delimiters
    import re
    parts = re.split(r'[,;→\->]+', desc)
    
    action_keywords = {
        'open': 'Navigate to page',
        'navigate': 'Navigate to page',
        'go': 'Navigate to page',
        'fill': 'Fill input field',
        'enter': 'Enter data',
        'type': 'Type data',
        'click': 'Click element',
        'press': 'Press button',
        'submit': 'Submit form',
        'verify': 'Verify result',
        'check': 'Check condition',
        'assert': 'Assert condition',
        'wait': 'Wait for element',
        'see': 'Verify visibility',
        'should': 'Verify condition',
    }
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        words = part.split()
        if not words:
            continue
        
        first_word = words[0].lower()
        
        if first_word in action_keywords:
            steps.append(f'{action_keywords[first_word]}: {part}')
        else:
            # Try to infer action from content
            if any(kw in part.lower() for kw in ['email', 'password', 'username', 'input']):
                steps.append(f'Fill input: {part}')
            elif any(kw in part.lower() for kw in ['button', 'submit', 'click']):
                steps.append(f'Click: {part}')
            elif any(kw in part.lower() for kw in ['verify', 'check', 'should', 'see']):
                steps.append(f'Verify: {part}')
            else:
                steps.append(f'Action: {part}')
    
    return steps if steps else ['Navigate to page']


def _to_class_name(text: str) -> str:
    """Convert text to valid Python class name."""
    # Remove special chars, split by space/underscore/hyphen
    words = re.sub(r'[^a-zA-Z0-9\s\-_]', '', text).split()
    return ''.join(word.capitalize() for word in words if word) or 'TestPage'

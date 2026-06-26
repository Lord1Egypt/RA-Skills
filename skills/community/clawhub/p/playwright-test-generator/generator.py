"""
Test generator orchestrator.
Routes generation requests to appropriate handlers.
"""
from typing import Dict, List, Optional, Any
import os
import hashlib


class GeneratorConfig:
    """Configuration for test generation."""

    DEFAULT_LANGUAGE = 'python'
    DEFAULT_OUTPUT_DIR = 'tests'
    DEFAULT_FORMAT = 'test'

    SUPPORTED_LANGUAGES = ['python', 'js']
    SUPPORTED_FORMATS = ['test', 'pom', 'gherkin', 'steps']

    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        format: str = DEFAULT_FORMAT,
        pom: bool = False,
        verbose: bool = False,
        base_url: str = ""
    ):
        self.language = language if language in self.SUPPORTED_LANGUAGES else self.DEFAULT_LANGUAGE
        self.output_dir = output_dir
        self.format = format if format in self.SUPPORTED_FORMATS else self.DEFAULT_FORMAT
        self.pom = pom
        self.verbose = verbose
        self.base_url = base_url

    def __repr__(self) -> str:
        return f"GeneratorConfig(lang={self.language}, format={self.format}, pom={self.pom})"


class GeneratorOutput:
    """Container for generated output."""

    def __init__(
        self,
        code: str,
        language: str,
        format: str,
        filename: str = "",
        warnings: List[str] = None
    ):
        self.code = code
        self.language = language
        self.format = format
        self.filename = filename
        self.warnings = warnings or []

    def save(self, filepath: str) -> None:
        """Save generated code to file."""
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.code)

    def __str__(self) -> str:
        return f"GeneratorOutput({self.language}, {self.format}, {len(self.code)} chars)"


class PlaywrightTestGenerator:
    """Main test generation orchestrator."""

    def __init__(self, config: GeneratorConfig = None):
        self.config = config or GeneratorConfig()

    def generate(
        self,
        source: str,
        source_type: str,
        **kwargs
    ) -> GeneratorOutput:
        """Generate test code from various sources.

        Args:
            source: The source content (URL, story, or description)
            source_type: 'url', 'story', or 'desc'
            **kwargs: Additional generation options

        Returns:
            GeneratorOutput with generated code
        """
        if source_type == 'url':
            return self._generate_from_url(source, **kwargs)
        elif source_type == 'story':
            return self._generate_from_story(source, **kwargs)
        elif source_type == 'desc':
            return self._generate_from_description(source, **kwargs)
        else:
            return GeneratorOutput(
                code=f"# Unsupported source type: {source_type}",
                language=self.config.language,
                format=self.config.format,
                warnings=[f"Unknown source type: {source_type}"]
            )

    def _generate_from_url(self, url: str, **kwargs) -> GeneratorOutput:
        """Generate test from URL."""
        from playwright_test_generator import generate_from_url

        warnings = []

        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            warnings.append(f"Added https:// prefix: {url}")

        try:
            code = generate_from_url(
                url,
                language=kwargs.get('language', self.config.language),
                pom=kwargs.get('pom', self.config.pom)
            )
        except Exception as e:
            code = f"# Error generating from URL: {str(e)}\n# Please check the URL and try again."
            warnings.append(str(e))

        filename = self._generate_filename(url, 'url')

        return GeneratorOutput(
            code=code,
            language=self.config.language,
            format='pom' if self.config.pom else 'test',
            filename=filename,
            warnings=warnings
        )

    def _generate_from_story(self, story: str, **kwargs) -> GeneratorOutput:
        """Generate test from user story."""
        from playwright_test_generator import parse_user_story
        from templates import GherkinTemplates, PythonTemplates, JavaScriptTemplates

        steps = parse_user_story(story)
        language = kwargs.get('language', self.config.language)
        format_type = kwargs.get('format', self.config.format)

        warnings = []

        if format_type == 'gherkin':
            scenario = GherkinTemplates.generate_scenario(
                'User story scenario',
                [
                    GherkinTemplates.step_given(steps[0]) if steps else 'Given the user is on the page',
                    GherkinTemplates.step_when(steps[1]) if len(steps) > 1 else 'When the user performs an action',
                    GherkinTemplates.step_then(steps[2]) if len(steps) > 2 else 'Then the result should be verified',
                ]
            )
            code = GherkinTemplates.generate_feature('Generated Feature', scenario)
            filename = 'feature.feature'
        else:
            code = self._generate_test_code(steps, language)
            filename = self._generate_filename(story, 'story')

        return GeneratorOutput(
            code=code,
            language=language,
            format=format_type,
            filename=filename,
            warnings=warnings
        )

    def _generate_from_description(self, desc: str, **kwargs) -> GeneratorOutput:
        """Generate test from description."""
        from playwright_test_generator import parse_description

        steps = parse_description(desc)
        language = kwargs.get('language', self.config.language)

        warnings = []

        code = self._generate_test_code(steps, language)
        filename = self._generate_filename(desc, 'desc')

        return GeneratorOutput(
            code=code,
            language=language,
            format='test',
            filename=filename,
            warnings=warnings
        )

    def _generate_test_code(self, steps: List[str], language: str) -> str:
        """Generate test code from steps."""
        from templates import PythonTemplates, JavaScriptTemplates

        if language == 'python':
            body_lines = []
            for i, step in enumerate(steps):
                body_lines.append(f'        # Step {i+1}: {step}')
                body_lines.append('        pass  # TODO: Implement step')
            
            body = '\n'.join(body_lines)
            
            return f'''\
"""Generated Playwright test from description."""
import pytest
from playwright.sync_api import Page, expect


class TestGenerated:
    """Generated test class."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page

    def test_generated_scenario(self):
        """Test generated from description."""
{body}
'''
        else:
            body_lines = []
            for i, step in enumerate(steps):
                body_lines.append(f'    // Step {i+1}: {step}')
                body_lines.append('    // TODO: Implement step')
            
            body = '\n'.join(body_lines)
            
            return f'''\
// Generated Playwright test from description
const {{ test, expect }} = require('@playwright/test');

test.describe('Generated Tests', () => {{
  test('generated scenario', async ({{ page }}) => {{
{body}
  }});
}});
'''

    def _generate_filename(self, source: str, prefix: str) -> str:
        """Generate a filename from source content."""
        # Create a hash-based filename for URLs
        if prefix == 'url':
            try:
                from urllib.parse import urlparse
                parsed = urlparse(source)
                name = parsed.netloc.replace('.', '_').replace(':', '_')
                return f"test_{name}.py"
            except:
                pass
        
        # Create a name from the source
        if isinstance(source, str):
            # Take first meaningful words
            words = source.split()[:3]
            name = '_'.join(w.lower() for w in words if w.isalnum())
            name = name or 'test'
        else:
            name = 'test'
        
        # Add hash for uniqueness
        hash_suffix = hashlib.md5(str(source).encode()).hexdigest()[:6]
        
        ext = 'py' if self.config.language == 'python' else 'js'
        return f"test_{name}_{hash_suffix}.{ext}"

    def generate_multiple(
        self,
        sources: List[Dict[str, str]]
    ) -> List[GeneratorOutput]:
        """Generate tests from multiple sources.

        Args:
            sources: List of dicts with 'source' and 'source_type' keys

        Returns:
            List of GeneratorOutput objects
        """
        outputs = []
        for src in sources:
            output = self.generate(
                source=src.get('source', ''),
                source_type=src.get('source_type', 'desc'),
                language=src.get('language', self.config.language),
                pom=src.get('pom', self.config.pom)
            )
            outputs.append(output)
        
        return outputs

    def save_output(self, output: GeneratorOutput, output_dir: str = None) -> str:
        """Save output to file.

        Args:
            output: GeneratorOutput to save
            output_dir: Output directory (uses config default if not provided)

        Returns:
            Path to saved file
        """
        output_dir = output_dir or self.config.output_dir
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, output.filename)
        output.save(filepath)

        if self.config.verbose:
            print(f"Saved to: {filepath}")

        return filepath


def create_generator(**kwargs) -> PlaywrightTestGenerator:
    """Factory function to create a configured generator."""
    config = GeneratorConfig(**kwargs)
    return PlaywrightTestGenerator(config)

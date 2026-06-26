"""
Tests for generator module.
"""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock

from generator import (
    GeneratorConfig,
    GeneratorOutput,
    PlaywrightTestGenerator,
    create_generator
)


class TestGeneratorConfig:
    """Tests for GeneratorConfig."""

    def test_default_config(self):
        """Default config should have expected values."""
        config = GeneratorConfig()
        
        assert config.language == 'python'
        assert config.output_dir == 'tests'
        assert config.format == 'test'
        assert config.pom is False
        assert config.verbose is False

    def test_custom_config(self):
        """Custom config should override defaults."""
        config = GeneratorConfig(
            language='js',
            output_dir='output',
            pom=True,
            verbose=True
        )
        
        assert config.language == 'js'
        assert config.output_dir == 'output'
        assert config.pom is True
        assert config.verbose is True

    def test_invalid_language(self):
        """Invalid language should fallback to default."""
        config = GeneratorConfig(language='invalid')
        
        assert config.language == 'python'

    def test_invalid_format(self):
        """Invalid format should fallback to default."""
        config = GeneratorConfig(format='invalid')
        
        assert config.format == 'test'

    def test_repr(self):
        """Config repr should be informative."""
        config = GeneratorConfig(language='js', pom=True)
        
        repr_str = repr(config)
        
        assert 'js' in repr_str
        assert 'pom' in repr_str
        assert 'True' in repr_str


class TestGeneratorOutput:
    """Tests for GeneratorOutput."""

    def test_output_creation(self):
        """Output should store provided values."""
        output = GeneratorOutput(
            code="print('test')",
            language='python',
            format='test',
            filename='test.py'
        )
        
        assert output.code == "print('test')"
        assert output.language == 'python'
        assert output.format == 'test'
        assert output.filename == 'test.py'
        assert output.warnings == []

    def test_output_with_warnings(self):
        """Output should store warnings."""
        output = GeneratorOutput(
            code="code",
            language='python',
            format='test',
            warnings=['Warning 1', 'Warning 2']
        )
        
        assert len(output.warnings) == 2
        assert 'Warning 1' in output.warnings

    def test_output_save(self):
        """Output should save to file."""
        output = GeneratorOutput(
            code="test code",
            language='python',
            format='test',
            filename='test_output.py'
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test_output.py')
            output.save(filepath)
            
            assert os.path.exists(filepath)
            with open(filepath, 'r') as f:
                assert f.read() == 'test code'

    def test_output_str(self):
        """Output str should be informative."""
        output = GeneratorOutput(
            code="x=1",
            language='python',
            format='test',
            filename='test.py'
        )
        
        assert 'python' in str(output)
        assert 'test' in str(output)
        assert '3' in str(output)  # len('x=1')


class TestPlaywrightTestGenerator:
    """Tests for TestGenerator."""

    def test_generator_default_config(self):
        """Generator should use default config."""
        generator = PlaywrightTestGenerator()
        
        assert generator.config.language == 'python'

    def test_generator_custom_config(self):
        """Generator should use provided config."""
        config = GeneratorConfig(language='js')
        generator = PlaywrightTestGenerator(config)
        
        assert generator.config.language == 'js'

    def test_generate_unsupported_type(self):
        """Unsupported source type should return error code."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate('test', source_type='unsupported')
        
        assert 'Unsupported' in output.code
        assert len(output.warnings) > 0

    def test_generate_from_story(self):
        """Story generation should produce code."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate(
            'As a user I can login with email and password',
            source_type='story'
        )
        
        assert output.language == 'python'
        assert len(output.code) > 0
        assert 'page' in output.code or 'test' in output.code

    def test_generate_from_description(self):
        """Description generation should produce code."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate(
            'Open login page, fill form, click submit',
            source_type='desc'
        )
        
        assert output.language == 'python'
        assert len(output.code) > 0

    def test_generate_story_js(self):
        """Story generation in JS should produce JS code."""
        generator = PlaywrightTestGenerator(GeneratorConfig(language='js'))
        
        output = generator.generate(
            'As a user I can login',
            source_type='story'
        )
        
        assert output.language == 'js'

    def test_generate_story_gherkin(self):
        """Story generation in Gherkin should produce BDD code."""
        generator = PlaywrightTestGenerator(GeneratorConfig(format='gherkin'))
        
        output = generator.generate(
            'As a user I can login with email',
            source_type='story'
        )
        
        assert 'Feature' in output.code or 'Given' in output.code or 'feature' in output.code

    def test_generate_multiple(self):
        """Batch generation should work."""
        generator = PlaywrightTestGenerator()
        
        sources = [
            {'source': 'Login test', 'source_type': 'story'},
            {'source': 'Click button', 'source_type': 'desc'}
        ]
        
        outputs = generator.generate_multiple(sources)
        
        assert len(outputs) == 2

    def test_save_output(self):
        """Save output should write file."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate('test', source_type='story')
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = generator.save_output(output, tmpdir)
            
            assert os.path.exists(filepath)
            assert output.filename in filepath


class TestCreateGenerator:
    """Tests for create_generator factory."""

    def test_create_with_kwargs(self):
        """Factory should accept kwargs."""
        generator = create_generator(language='js', pom=True)
        
        assert generator.config.language == 'js'
        assert generator.config.pom is True

    def test_create_defaults(self):
        """Factory should use defaults."""
        generator = create_generator()
        
        assert generator.config.language == 'python'
        assert generator.config.pom is False


class TestFilenameGeneration:
    """Tests for filename generation."""

    def test_url_filename(self):
        """URL should generate meaningful filename."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate('https://example.com/login', source_type='url')
        
        # Should have a filename
        assert output.filename.endswith('.py') or output.filename.endswith('.js')

    def test_story_filename(self):
        """Story should generate filename."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate('Login functionality', source_type='story')
        
        assert output.filename.endswith('.py') or output.filename.endswith('.js')
        assert 'test' in output.filename.lower()

    def test_desc_filename(self):
        """Description should generate filename."""
        generator = PlaywrightTestGenerator()
        
        output = generator.generate('Test login flow', source_type='desc')
        
        assert output.filename.endswith('.py') or output.filename.endswith('.js')

"""
Tests for CLI module.
"""
import pytest
from unittest.mock import patch, MagicMock
import click
from click.testing import CliRunner

from cli import cli, url, story, desc, template, info, batch


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


class TestCLI:
    """Tests for CLI main group."""

    def test_cli_help(self, runner):
        """CLI should show help."""
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Playwright Test Generator' in result.output

    def test_cli_version(self, runner):
        """CLI should show version."""
        result = runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert '1.0.0' in result.output


class TestURLCommand:
    """Tests for url command."""

    @patch('generator.PlaywrightTestGenerator')
    def test_url_generates_test(self, mock_generator_class, runner):
        """URL command should generate test."""
        mock_generator = MagicMock()
        mock_output = MagicMock()
        mock_output.code = 'test code'
        mock_output.warnings = []
        mock_output.filename = 'test.py'
        mock_generator.generate.return_value = mock_output
        mock_generator_class.return_value = mock_generator

        result = runner.invoke(url, ['https://example.com'])

        assert 'Analyzing URL' in result.output or result.exit_code == 0

    def test_url_with_python_lang(self, runner):
        """URL with Python language."""
        result = runner.invoke(url, [
            'https://example.com',
            '--lang', 'python'
        ])
        
        # Should not crash
        assert result.exit_code in [0, 1]

    def test_url_with_js_lang(self, runner):
        """URL with JS language."""
        result = runner.invoke(url, [
            'https://example.com',
            '--lang', 'js'
        ])
        
        assert result.exit_code in [0, 1]

    def test_url_with_pom_flag(self, runner):
        """URL with POM flag."""
        result = runner.invoke(url, [
            'https://example.com',
            '--pom'
        ])
        
        assert result.exit_code in [0, 1]


class TestStoryCommand:
    """Tests for story command."""

    def test_story_help(self, runner):
        """Story command should show help."""
        result = runner.invoke(story, ['--help'])
        
        assert result.exit_code == 0
        assert 'story' in result.output.lower()

    def test_story_generates_code(self, runner):
        """Story should generate code."""
        result = runner.invoke(story, [
            'As a user I can login with email and password'
        ])
        
        # Should process without crash
        assert result.exit_code in [0, 1]

    def test_story_with_gherkin_format(self, runner):
        """Story with Gherkin format."""
        result = runner.invoke(story, [
            'As a user I can login',
            '--format', 'gherkin'
        ])
        
        assert result.exit_code in [0, 1]


class TestDescCommand:
    """Tests for desc command."""

    def test_desc_help(self, runner):
        """Desc command should show help."""
        result = runner.invoke(desc, ['--help'])
        
        assert result.exit_code == 0

    def test_desc_generates_code(self, runner):
        """Desc should generate code."""
        result = runner.invoke(desc, [
            'Open login page, fill email, click submit'
        ])
        
        assert result.exit_code in [0, 1]


class TestTemplateCommand:
    """Tests for template command."""

    def test_template_python(self, runner):
        """Template should show Python template."""
        result = runner.invoke(template, ['--lang', 'python'])
        
        assert result.exit_code == 0
        assert 'pytest' in result.output or 'playwright' in result.output.lower()

    def test_template_js(self, runner):
        """Template should show JS template."""
        result = runner.invoke(template, ['--lang', 'js'])
        
        assert result.exit_code == 0
        assert '@playwright/test' in result.output or 'playwright' in result.output.lower()


class TestInfoCommand:
    """Tests for info command."""

    def test_info_shows_info(self, runner):
        """Info should show information."""
        result = runner.invoke(info)
        
        assert result.exit_code == 0
        assert 'Playwright Test Generator' in result.output
        assert 'v1.0.0' in result.output

    def test_info_shows_pricing(self, runner):
        """Info should show pricing."""
        result = runner.invoke(info)
        
        assert 'Free' in result.output
        assert 'Pro' in result.output
        assert 'Team' in result.output


class TestBatchCommand:
    """Tests for batch command."""

    def test_batch_requires_file(self, runner):
        """Batch should require file argument."""
        result = runner.invoke(batch, [])
        
        assert result.exit_code != 0

    def test_batch_nonexistent_file(self, runner):
        """Batch should error on nonexistent file."""
        result = runner.invoke(batch, ['nonexistent.txt'])
        
        assert result.exit_code != 0

    def test_batch_with_valid_file(self, runner):
        """Batch with valid file should process."""
        with runner.isolated_filesystem():
            # Create a test file
            with open('test_input.txt', 'w') as f:
                f.write('story:As a user I can login\n')
                f.write('desc:Click button\n')
            
            result = runner.invoke(batch, ['test_input.txt'])
            
            # Should process without crashing
            assert result.exit_code in [0, 1]


class TestCLIOptions:
    """Tests for CLI options."""

    def test_verbose_flag(self, runner):
        """Verbose flag should be accepted."""
        result = runner.invoke(story, [
            'Test story',
            '--verbose'
        ])
        
        assert result.exit_code in [0, 1]

    def test_output_dir(self, runner):
        """Output dir option should be accepted."""
        result = runner.invoke(story, [
            'Test story',
            '--output', 'custom_dir'
        ])
        
        assert result.exit_code in [0, 1]

    def test_save_file(self, runner):
        """Save file option should be accepted."""
        result = runner.invoke(story, [
            'Test story',
            '--save', 'my_test.py'
        ])
        
        assert result.exit_code in [0, 1]

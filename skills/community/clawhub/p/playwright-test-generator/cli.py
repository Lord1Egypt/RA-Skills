#!/usr/bin/env python3
"""
Playwright Test Generator CLI.
Command-line interface for generating Playwright tests.
"""
import sys
import os

try:
    import click
except ImportError:
    print("Error: Click library not found. Install with: pip install click")
    sys.exit(1)

from generator import PlaywrightTestGenerator, GeneratorConfig, create_generator


@click.group(invoke_without_command=True)
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    """Playwright Test Generator - AI-powered test generation from URLs and descriptions."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('url')
@click.option('--lang', '-l', 'language', default='python',
              type=click.Choice(['python', 'js']),
              help='Target language (default: python)')
@click.option('--pom', is_flag=True, default=False,
              help='Generate Page Object Model')
@click.option('--output', '-o', 'output_dir', default='tests',
              help='Output directory (default: tests)')
@click.option('--save', '-s', 'save_file', default=None,
              help='Save to specific filename')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def url(url, language, pom, output_dir, save_file, verbose):
    """Generate test from URL.

    Example:
        playwright-gen url https://example.com --lang python --pom
    """
    click.echo(f"🔍 Analyzing URL: {url}")

    config = GeneratorConfig(
        language=language,
        output_dir=output_dir,
        pom=pom,
        verbose=verbose
    )

    generator = PlaywrightTestGenerator(config)

    try:
        output = generator.generate(url, source_type='url')

        for warning in output.warnings:
            click.echo(f"⚠️  {warning}")

        if save_file:
            filepath = os.path.join(output_dir, save_file)
            output.save(filepath)
            click.echo(f"💾 Saved to: {filepath}")
        else:
            click.echo("\n📝 Generated Test Code:\n")
            click.echo(output.code)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('story')
@click.option('--lang', '-l', 'language', default='python',
              type=click.Choice(['python', 'js']),
              help='Target language (default: python)')
@click.option('--format', '-f', 'format_type', default='test',
              type=click.Choice(['test', 'gherkin', 'steps']),
              help='Output format (default: test)')
@click.option('--output', '-o', 'output_dir', default='tests',
              help='Output directory (default: tests)')
@click.option('--save', '-s', 'save_file', default=None,
              help='Save to specific filename')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def story(story, language, format_type, output_dir, save_file, verbose):
    """Generate test from user story.

    Example:
        playwright-gen story "As a user I can login with email and password"
    """
    click.echo(f"📖 Parsing user story...")

    config = GeneratorConfig(
        language=language,
        output_dir=output_dir,
        format=format_type,
        verbose=verbose
    )

    generator = PlaywrightTestGenerator(config)

    try:
        output = generator.generate(story, source_type='story')

        for warning in output.warnings:
            click.echo(f"⚠️  {warning}")

        if save_file:
            filepath = os.path.join(output_dir, save_file)
            output.save(filepath)
            click.echo(f"💾 Saved to: {filepath}")
        else:
            click.echo("\n📝 Generated Test Code:\n")
            click.echo(output.code)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('description')
@click.option('--lang', '-l', 'language', default='python',
              type=click.Choice(['python', 'js']),
              help='Target language (default: python)')
@click.option('--output', '-o', 'output_dir', default='tests',
              help='Output directory (default: tests)')
@click.option('--save', '-s', 'save_file', default=None,
              help='Save to specific filename')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def desc(description, language, output_dir, save_file, verbose):
    """Generate test from description.

    Example:
        playwright-gen desc "Open login page, fill email, click submit, verify success"
    """
    click.echo(f"📝 Generating test from description...")

    config = GeneratorConfig(
        language=language,
        output_dir=output_dir,
        verbose=verbose
    )

    generator = PlaywrightTestGenerator(config)

    try:
        output = generator.generate(description, source_type='desc')

        for warning in output.warnings:
            click.echo(f"⚠️  {warning}")

        if save_file:
            filepath = os.path.join(output_dir, save_file)
            output.save(filepath)
            click.echo(f"💾 Saved to: {filepath}")
        else:
            click.echo("\n📝 Generated Test Code:\n")
            click.echo(output.code)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--lang', '-l', 'language', default='python',
              type=click.Choice(['python', 'js']),
              help='Target language (default: python)')
@click.option('--output', '-o', 'output_dir', default='tests',
              help='Output directory (default: tests)')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def batch(input_file, language, output_dir, verbose):
    """Generate tests from a file containing multiple URLs or stories.

    Each line should be: url:https://example.com
                         story:As a user I can login
                         desc:Open page, click submit

    Example:
        playwright-gen batch input.txt --output tests/
    """
    click.echo(f"📂 Processing batch file: {input_file}")

    config = GeneratorConfig(
        language=language,
        output_dir=output_dir,
        verbose=verbose
    )

    generator = PlaywrightTestGenerator(config)

    sources = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if ':' in line:
                source_type, source = line.split(':', 1)
                sources.append({
                    'source': source.strip(),
                    'source_type': source_type.strip(),
                    'language': language
                })

    click.echo(f"📋 Found {len(sources)} items to process")

    outputs = generator.generate_multiple(sources)

    for i, output in enumerate(outputs):
        filepath = os.path.join(output_dir, output.filename)
        output.save(filepath)
        click.echo(f"  ✅ [{i+1}/{len(outputs)}] Saved: {filepath}")

    click.echo(f"\n✨ Generated {len(outputs)} test files in {output_dir}/")


@cli.command()
@click.option('--lang', '-l', 'language', default='python',
              type=click.Choice(['python', 'js']),
              help='Target language (default: python)')
def template(language):
    """Show example template code.

    Example:
        playwright-gen template --lang python
    """
    if language == 'python':
        template_code = '''\
"""Example Playwright test template."""
import pytest
from playwright.sync_api import Page, expect


class TestExample:
    """Example test class."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page

    def test_example(self):
        """Example test case."""
        self.page.goto("https://example.com")
        self.page.click("#submit")
        expect(self.page.locator("#result")).to_be_visible()
'''
    else:
        template_code = '''\
// Example Playwright test template
const { test, expect } = require('@playwright/test');

test.describe('Example', () => {
  test('example test', async ({ page }) => {
    await page.goto('https://example.com');
    await page.click('#submit');
    await expect(page.locator('#result')).toBeVisible();
  });
});
'''

    click.echo(f"\n📝 {language.upper()} Template:\n")
    click.echo(template_code)


@cli.command()
def info():
    """Show generator information and configuration."""
    click.echo("""
🔧 Playwright Test Generator v1.0.0
════════════════════════════════════════

A tool for generating Playwright test code from:
  • URLs - Automatically analyze pages and generate tests
  • User Stories - Convert BDD-style stories to test code
  • Descriptions - Generate tests from step descriptions

Supported Languages:
  • Python (pytest-playwright)
  • JavaScript (@playwright/test)

Features:
  • Page Object Model (POM) generation
  • Gherkin/BDD format support
  • Batch processing
  • CLI interface for AI agents

Usage:
  playwright-gen url <url>       Generate from URL
  playwright-gen story <story>   Generate from user story
  playwright-gen desc <desc>     Generate from description
  playwright-gen template        Show template code
  playwright-gen info           Show this info

Pricing:
  Free  - 10 tests/month
  Pro   - ¥19/month (unlimited, JS, POM)
  Team  - ¥49/month (Pro + CI, custom templates)
""".strip())


if __name__ == '__main__':
    cli()

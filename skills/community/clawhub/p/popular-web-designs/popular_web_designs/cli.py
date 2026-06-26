"""
CLI for popular-web-designs — 54 production-quality design systems.

Usage:
    web-design list                      List all 54 templates
    web-design show <name>               Show full design tokens for a template
    web-design tokens <name>             Extract CSS custom properties only
    web-design generate <name>           Generate a starter HTML/CSS skeleton
"""

import json
import textwrap

import click

from .catalog import TEMPLATES, get_template, list_templates, get_categories


# ── Display helpers ────────────────────────────────────────────────

def _color_swatch(hex_color: str) -> str:
    """Return a small visual swatch for a hex color (terminal-friendly)."""
    return f"[{hex_color}]"


def _print_template_full(template: dict) -> None:
    """Pretty-print a fully-described template."""
    name = template["name"]
    category = template.get("category", "N/A")
    tags = template.get("tags", [])
    desc = template.get("description", "No description available.")
    best = template.get("best_for", "N/A")
    key_elems = template.get("key_elements", [])

    click.echo()
    click.secho(f"  {name.upper()}", fg="cyan", bold=True)
    click.echo(f"  {'─' * 60}")
    click.echo(f"  Category:     {category}")
    if tags:
        click.echo(f"  Tags:         {', '.join(tags)}")
    click.echo()
    click.echo(f"  {desc}")
    click.echo()
    click.secho("  Best For:", fg="green", bold=True)
    click.echo(f"  {best}")
    click.echo()

    # Key elements
    if key_elems:
        click.secho("  Key Elements:", fg="green", bold=True)
        for elem in key_elems:
            click.echo(f"    • {elem}")
        click.echo()

    # Colors
    colors = template.get("colors", [])
    if colors:
        click.secho("  Color Palette:", fg="green", bold=True)
        for c in colors:
            role = c.get("role", "?")
            hex_val = c.get("hex", "")
            name = c.get("name", "")
            click.echo(f"    {role:<20s}  {hex_val:<30s}  {name}")
        click.echo()

    # Typography
    typo = template.get("typography", {})
    if typo:
        click.secho("  Typography:", fg="green", bold=True)
        font = typo.get("font_family", "N/A")
        click.echo(f"    Font:  {font}")
        if "mono_family" in typo:
            click.echo(f"    Mono:  {typo['mono_family']}")
        for level in ["display", "h1", "h2", "h3", "body", "caption", "code", "small", "label"]:
            if level in typo:
                spec = typo[level]
                if isinstance(spec, dict):
                    sz = spec.get("size", "?")
                    wt = spec.get("weight", "?")
                    ls = spec.get("letter_spacing", "?")
                    lh = spec.get("line_height", "?")
                    click.echo(f"    {level:<8s}  {sz:<8s}  weight={wt}  tracking={ls}  line-height={lh}")
        click.echo()

    # Spacing
    spacing = template.get("spacing", {})
    if spacing:
        click.secho("  Spacing:", fg="green", bold=True)
        scale = spacing.get("scale", [])
        click.echo(f"    Scale (px):  {', '.join(str(s) for s in scale)}")
        for k in ["card_padding", "section_gap", "page_margin"]:
            if k in spacing:
                click.echo(f"    {k}:  {spacing[k]}")
        click.echo()

    # Borders
    borders = template.get("borders", {})
    if borders:
        click.secho("  Borders & Radius:", fg="green", bold=True)
        for k, v in borders.items():
            click.echo(f"    {k}:  {v}")
        click.echo()

    # Shadows
    shadows = template.get("shadows", {})
    if shadows:
        click.secho("  Shadows:", fg="green", bold=True)
        for k, v in shadows.items():
            # Truncate very long shadow values for readability
            v_display = v if len(v) < 80 else v[:77] + "..."
            click.echo(f"    {k}:  {v_display}")
        click.echo()


def _print_template_stub(template: dict, index: int) -> None:
    """Pretty-print a stub template."""
    name = template["name"]
    category = template.get("category", "N/A")
    click.echo(f"  {index:<4d}  {name:<22s}  {category}")


# ── CSS token generation ───────────────────────────────────────────

def _generate_css_tokens(template: dict) -> str:
    """Generate CSS custom properties from a template."""
    lines = [":root {"]

    # Colors
    for c in template.get("colors", []):
        role = c["role"].replace(" ", "-")
        hex_val = c["hex"]
        lines.append(f"  --color-{role}: {hex_val};")

    # Typography
    typo = template.get("typography", {})
    if "font_family" in typo:
        lines.append(f"  --font-family: {typo['font_family']};")
    if "mono_family" in typo:
        lines.append(f"  --font-family-mono: {typo['mono_family']};")
    for level in ["display", "h1", "h2", "h3", "body", "caption", "code"]:
        spec = typo.get(level)
        if isinstance(spec, dict):
            lines.append(f"  --font-{level}-size: {spec.get('size', 'inherit')};")
            lines.append(f"  --font-{level}-weight: {spec.get('weight', 400)};")
            lines.append(f"  --font-{level}-tracking: {spec.get('letter_spacing', 'normal')};")
            lines.append(f"  --font-{level}-line-height: {spec.get('line_height', 1.5)};")

    # Borders
    for k, v in template.get("borders", {}).items():
        safe_key = k.replace("_", "-")
        if "border" in k:
            lines.append(f"  --{safe_key}: {v};")
        else:
            lines.append(f"  --radius-{safe_key}: {v};")

    # Shadows
    for k, v in template.get("shadows", {}).items():
        safe_key = k.replace("_", "-")
        lines.append(f"  --shadow-{safe_key}: {v};")

    # Spacing scale
    scale = template.get("spacing", {}).get("scale", [])
    for i, s in enumerate(scale):
        lines.append(f"  --space-{i}: {s}px;")

    lines.append("}")
    return "\n".join(lines)


# ── HTML skeleton generation ───────────────────────────────────────

def _generate_html_skeleton(template: dict) -> str:
    """Generate a starter HTML file with the template's CSS variables applied."""
    name = template["name"]
    css_tokens = _generate_css_tokens(template)
    colors = template.get("colors", [])
    typo = template.get("typography", {})
    body_font = typo.get("font_family", "system-ui, sans-serif")
    bg_color = next((c["hex"] for c in colors if "background" in c.get("role", "").lower() and "section" not in c.get("role", "").lower()), "#ffffff")
    text_color = next((c["hex"] for c in colors if "text-primary" in c.get("role", "").lower() or c.get("role") == "text"), "#000000")
    primary_color = next((c["hex"] for c in colors if c.get("role") == "primary"), "#0066cc")

    html = textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{name.title()} — Starter Template</title>
      <style>
        /* === {name.title()} Design Tokens === */
        {css_tokens}

        /* === Base Reset === */
        *, *::before, *::after {{
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }}

        body {{
          font-family: {body_font};
          font-size: var(--font-body-size, 16px);
          font-weight: var(--font-body-weight, 400);
          line-height: var(--font-body-line-height, 1.5);
          color: {text_color};
          background-color: {bg_color};
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }}

        /* === Layout === */
        .container {{
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 var(--space-3, 24px);
        }}

        /* === Typography === */
        h1 {{
          font-size: var(--font-display-size, var(--font-h1-size, 2rem));
          font-weight: var(--font-display-weight, var(--font-h1-weight, 700));
          letter-spacing: var(--font-display-tracking, var(--font-h1-tracking, -0.02em));
          line-height: var(--font-display-line-height, var(--font-h1-line-height, 1.2));
        }}

        h2 {{
          font-size: var(--font-h2-size, 1.5rem);
          font-weight: var(--font-h2-weight, 600);
          letter-spacing: var(--font-h2-tracking, -0.01em);
          line-height: var(--font-h2-line-height, 1.3);
        }}

        h3 {{
          font-size: var(--font-h3-size, 1.2rem);
          font-weight: var(--font-h3-weight, 600);
          letter-spacing: var(--font-h3-tracking, 0);
          line-height: var(--font-h3-line-height, 1.4);
        }}

        p {{
          font-size: var(--font-body-size, 16px);
          line-height: var(--font-body-line-height, 1.5);
        }}

        small {{
          font-size: var(--font-caption-size, 14px);
          color: var(--color-text-secondary, #666);
        }}

        code {{
          font-family: var(--font-family-mono, monospace);
          font-size: var(--font-code-size, 14px);
          background: rgba(0,0,0,0.05);
          padding: 2px 6px;
          border-radius: var(--radius-sm, 4px);
        }}

        /* === Buttons === */
        .btn {{
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 10px 24px;
          font-family: inherit;
          font-size: var(--font-body-size, 16px);
          font-weight: 500;
          border: none;
          border-radius: var(--radius-md, 6px);
          cursor: pointer;
          transition: all 0.15s ease;
        }}

        .btn-primary {{
          background: {primary_color};
          color: #ffffff;
        }}

        .btn-primary:hover {{
          opacity: 0.9;
          box-shadow: var(--shadow-card-hover, 0 4px 12px rgba(0,0,0,0.15));
        }}

        .btn-secondary {{
          background: transparent;
          color: {primary_color};
          border: 1px solid {primary_color};
        }}

        /* === Cards === */
        .card {{
          background: var(--color-surface, #ffffff);
          border: var(--card-border, 1px solid rgba(0,0,0,0.08));
          border-radius: var(--radius-lg, 12px);
          padding: var(--space-4, 24px);
          box-shadow: var(--shadow-card, none);
        }}

        .card:hover {{
          box-shadow: var(--shadow-card-hover, 0 4px 12px rgba(0,0,0,0.1));
        }}

        /* === Hero Section === */
        .hero {{
          padding: var(--space-7, 80px) 0;
          text-align: center;
        }}

        .hero h1 {{
          margin-bottom: var(--space-3, 16px);
        }}

        .hero p {{
          color: var(--color-text-secondary, #666);
          max-width: 600px;
          margin: 0 auto var(--space-4, 24px);
        }}

        .hero .btn-group {{
          display: flex;
          gap: 12px;
          justify-content: center;
        }}

        /* === Grid === */
        .grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: var(--space-4, 24px);
          padding: var(--space-6, 64px) 0;
        }}

        /* === Nav === */
        .nav {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 16px 0;
          border-bottom: var(--card-border, 1px solid rgba(0,0,0,0.08));
        }}

        .nav-brand {{
          font-weight: 700;
          font-size: 18px;
          color: {primary_color};
          text-decoration: none;
        }}

        .nav-links {{
          display: flex;
          gap: 24px;
          list-style: none;
        }}

        .nav-links a {{
          color: var(--color-text-secondary, #666);
          text-decoration: none;
        }}

        .nav-links a:hover {{
          color: {text_color};
        }}
      </style>
    </head>
    <body>
      <header class="container">
        <nav class="nav">
          <a href="#" class="nav-brand">{name.title()}</a>
          <ul class="nav-links">
            <li><a href="#">Features</a></li>
            <li><a href="#">Docs</a></li>
            <li><a href="#">Pricing</a></li>
            <li><a href="#">Blog</a></li>
          </ul>
          <button class="btn btn-primary">Get Started</button>
        </nav>
      </header>

      <main>
        <section class="hero container">
          <h1>Build Faster with {name.title()}</h1>
          <p>{template.get('description', 'A production-quality design system.')}</p>
          <div class="btn-group">
            <button class="btn btn-primary">Start Building</button>
            <button class="btn btn-secondary">View Docs</button>
          </div>
        </section>

        <section class="container">
          <div class="grid">
            <div class="card">
              <h3>Feature One</h3>
              <p>Describe your first key feature here. Keep it concise and compelling.</p>
            </div>
            <div class="card">
              <h3>Feature Two</h3>
              <p>Describe your second key feature here. Focus on user benefit.</p>
            </div>
            <div class="card">
              <h3>Feature Three</h3>
              <p>Describe your third key feature here. What makes it different?</p>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <div class="container" style="padding: 40px 0; text-align: center;">
          <small>Built with the {name.title()} design system &mdash; popular-web-designs</small>
        </div>
      </footer>
    </body>
    </html>
    """)
    return html


# ── CLI ────────────────────────────────────────────────────────────

@click.group()
@click.version_option(version="1.2.0", prog_name="web-design")
def cli():
    """web-design — Browse and generate from 54 popular web design templates.

    Design systems extracted from real websites: Stripe, Linear, Notion,
    Vercel, GitHub, Apple, Spotify, Figma, Airtable, and 45 more.
    """
    pass


@cli.command("list")
@click.option("--category", "-c", default=None, help="Filter by category")
@click.option("--json", "as_json", is_flag=True, default=False, help="Output as JSON")
def list_cmd(category, as_json):
    """List all 54 design templates with index, name, and category."""
    templates = list_templates(category)

    if as_json:
        output = [{"index": i, "name": t["name"], "category": t.get("category", ""),
                    "tags": t.get("tags", []), "has_tokens": "colors" in t}
                  for i, t in enumerate(templates)]
        click.echo(json.dumps(output, indent=2))
        return

    if category:
        click.secho(f"\n  Templates in '{category}':\n", fg="cyan", bold=True)
    else:
        click.secho(f"\n  All {len(templates)} Templates:\n", fg="cyan", bold=True)

    click.echo(f"  {'Idx':<5s}  {'Name':<22s}  {'Category':<35s}  {'Tokens'}")
    click.echo(f"  {'─' * 75}")
    for i, t in enumerate(templates):
        has_tokens = "✓" if "colors" in t else "·"
        click.echo(f"  {i:<5d}  {t['name']:<22s}  {t.get('category', 'N/A'):<35s}  {has_tokens}")

    click.echo()
    click.echo(f"  Use 'web-design show <name>' to see full design tokens.")
    click.echo(f"  Templates with '✓' have full design tokens; '·' are stubs.")


@cli.command("show")
@click.argument("name")
def show_cmd(name):
    """Show full design tokens for a specific template.

    NAME can be the template name (e.g., 'stripe', 'notion', 'apple').
    Use 'web-design list' to see all available templates.
    """
    template = get_template(name)
    if template is None:
        click.secho(f"\n  Error: Template '{name}' not found.", fg="red")
        click.echo(f"  Run 'web-design list' to see all 54 available templates.")
        raise SystemExit(1)

    if "colors" not in template:
        click.secho(f"\n  {name} is a stub template (no full design tokens yet).", fg="yellow")
        click.echo(f"  Category: {template.get('category', 'N/A')}")
        click.echo()
        click.echo(f"  The following templates have full design tokens:")
        for t in TEMPLATES:
            if "colors" in t:
                click.echo(f"    • {t['name']}")
        return

    _print_template_full(template)


@cli.command("tokens")
@click.argument("name")
@click.option("--output", "-o", default=None, help="Write CSS to a file instead of stdout")
def tokens_cmd(name, output):
    """Extract CSS custom properties (design tokens) for a template.

    Outputs a :root {} block with all color, typography, spacing,
    border-radius, and shadow variables from the template.
    """
    template = get_template(name)
    if template is None:
        click.secho(f"\n  Error: Template '{name}' not found.", fg="red")
        raise SystemExit(1)

    if "colors" not in template:
        click.secho(f"\n  Error: '{name}' is a stub — no design tokens available.", fg="red")
        raise SystemExit(1)

    css = _generate_css_tokens(template)
    header = f"/* === {template['name'].title()} Design Tokens === */\n"

    if output:
        with open(output, "w") as f:
            f.write(header + css + "\n")
        click.secho(f"\n  ✓ CSS tokens written to {output}", fg="green")
    else:
        click.echo(header + css)


@cli.command("generate")
@click.argument("name")
@click.option("--output", "-o", default=None, help="Write HTML to a file instead of stdout")
def generate_cmd(name, output):
    """Generate a starter HTML/CSS skeleton using the template's design tokens.

    Creates a complete, self-contained HTML file with:
      • All CSS custom properties from the template
      • A responsive nav, hero section, feature grid, and footer
      • Buttons, cards, and typography styled with template tokens

    Save to a file with --output or pipe to a file.
    """
    template = get_template(name)
    if template is None:
        click.secho(f"\n  Error: Template '{name}' not found.", fg="red")
        raise SystemExit(1)

    if "colors" not in template:
        click.secho(f"\n  Error: '{name}' is a stub — cannot generate HTML without design tokens.", fg="red")
        click.echo(f"  Run 'web-design list' to see which templates have full tokens (✓).")
        raise SystemExit(1)

    html = _generate_html_skeleton(template)

    if output:
        with open(output, "w") as f:
            f.write(html)
        click.secho(f"\n  ✓ HTML skeleton written to {output}", fg="green")
        click.echo(f"  Open it in a browser or serve with: python -m http.server")
    else:
        click.echo(html)


if __name__ == "__main__":
    cli()

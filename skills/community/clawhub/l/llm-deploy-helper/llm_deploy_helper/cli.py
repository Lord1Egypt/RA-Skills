"""CLI entry point for llm-deploy-helper."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from llm_deploy_helper.deploy import detect_system, recommend_engine, SystemInfo
from llm_deploy_helper.docker_templates import (
    generate_compose,
    generate_systemd,
    TEMPLATES,
    ENGINE_META,
    MODEL_RECOMMENDATIONS,
)

console = Console()


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _print_system_table(info: SystemInfo) -> None:
    """Pretty-print system info as a Rich table."""
    table = Table(title="System Information", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("Property", style="dim")
    table.add_column("Value", style="green")

    table.add_row("OS", info.os_type)
    table.add_row("CPU Cores", str(info.cpu_cores))
    table.add_row("RAM", f"{info.ram_gb:.1f} GB")
    table.add_row("Free Disk", f"{info.disk_free_gb:.1f} GB")
    table.add_row("GPU Available", "✅ Yes" if info.gpu_available else "❌ No")

    if info.gpu_available:
        table.add_row("GPU Name", info.gpu_name)
        table.add_row("GPU VRAM", f"{info.gpu_vram_gb:.1f} GB")
        table.add_row("CUDA Version", info.cuda_version or "unknown")

    console.print(table)


def _print_recommendations(info: SystemInfo) -> None:
    """Print engine recommendations."""
    recs = recommend_engine(info)
    table = Table(title="📋 Recommended Engines", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Engine", style="bold yellow")
    table.add_column("Reason", style="white")
    table.add_column("Score", justify="right", style="cyan")

    for engine, reason, score in recs:
        meta = ENGINE_META.get(engine, {})
        label = meta.get("name", engine)
        if score >= 8:
            icon = "⭐"
        elif score >= 6:
            icon = "👍"
        else:
            icon = "⚠️"
        table.add_row(f"{icon} {label}", reason, str(score))

    console.print(table)


def _validate_engine(engine: str) -> None:
    """Validate engine name and show available options."""
    if engine not in TEMPLATES:
        console.print(f"[red]Error:[/red] Unknown engine '{engine}'.")
        console.print(f"Available engines: {', '.join(TEMPLATES)}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------

@click.group(invoke_without_command=True)
@click.version_option(version="1.0.0", prog_name="llm-deploy-helper")
@click.pass_context
def main(ctx: click.Context) -> None:
    """🚀 llm-deploy-helper — Local LLM deployment assistant.

    Detect your system, get recommendations, and generate Docker Compose
    or systemd configs for Ollama, vLLM, and llama.cpp.
    """
    if ctx.invoked_subcommand is None:
        # Default action: show help
        click.echo(ctx.get_help())


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------

@main.command()
def check() -> None:
    """Detect system hardware and recommend the best LLM engine."""

    console.print(Panel.fit(
        "[bold cyan]🔍 Scanning system hardware...[/bold cyan]",
        border_style="cyan",
    ))

    info = detect_system()
    _print_system_table(info)
    console.print()
    _print_recommendations(info)

    console.print()
    console.print(
        "[dim]Run [bold]llm-deploy-helper generate --engine <engine> --model <model>[/bold] "
        "to create a docker-compose.yml[/dim]"
    )


# ---------------------------------------------------------------------------
# generate
# ---------------------------------------------------------------------------

@main.command()
@click.option("--engine", "-e", required=True,
              type=click.Choice(list(TEMPLATES.keys()), case_sensitive=False),
              help="LLM engine to use")
@click.option("--model", "-m", required=True, help="Model name/ID")
@click.option("--gpu/--no-gpu", default=True, help="Enable/disable GPU support (default: --gpu)")
@click.option("--port", "-p", type=int, default=None, help="Override port (default: engine default)")
@click.option("--output", "-o", type=click.Path(), default="docker-compose.yml",
              help="Output file path (default: docker-compose.yml)")
def generate(engine: str, model: str, gpu: bool, port: int | None, output: str) -> None:
    """Generate a docker-compose.yml for the chosen engine and model."""

    content = generate_compose(engine, model, gpu=gpu, port=port)

    # Write to file
    out_path = Path(output)
    out_path.write_text(content)

    console.print()
    console.print(f"[green]✅ Generated[/green] [bold]{out_path}[/bold]")
    console.print(f"   Engine: [yellow]{engine}[/yellow] | Model: [yellow]{model}[/yellow] | GPU: [yellow]{gpu}[/yellow]")
    if port:
        console.print(f"   Port override: [cyan]{port}[/cyan]")

    console.print()
    console.print(Panel(content, title="Preview", border_style="dim"))
    console.print()
    console.print("[dim]Run [bold]docker compose up -d[/bold] to start the service.[/dim]")


# ---------------------------------------------------------------------------
# systemd
# ---------------------------------------------------------------------------

@main.command("systemd")
@click.option("--engine", "-e", required=True,
              type=click.Choice(list(TEMPLATES.keys()), case_sensitive=False),
              help="LLM engine to use")
@click.option("--model", "-m", required=True, help="Model name/ID")
@click.option("--output", "-o", type=click.Path(), default=None,
              help="Output file path (default: <engine>-llm.service)")
def systemd_cmd(engine: str, model: str, output: str | None) -> None:
    """Generate a systemd unit file for the chosen engine."""

    if output is None:
        output = f"{engine}-llm.service"

    content = generate_systemd(engine, model)
    out_path = Path(output)
    out_path.write_text(content)

    console.print()
    console.print(f"[green]✅ Generated[/green] [bold]{out_path}[/bold]")
    console.print(f"   Engine: [yellow]{engine}[/yellow] | Model: [yellow]{model}[/yellow]")

    console.print()
    console.print(Panel(content, title="Preview", border_style="dim"))
    console.print()
    console.print("[dim]Install with:[/dim]")
    console.print(f"[dim]  sudo cp {output} /etc/systemd/system/[/dim]")
    console.print(f"[dim]  sudo systemctl daemon-reload[/dim]")
    console.print(f"[dim]  sudo systemctl enable --now {Path(output).stem}[/dim]")


# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------

@main.command()
@click.option("--engine", "-e", required=False,
              type=click.Choice(list(TEMPLATES.keys()), case_sensitive=False),
              help="Filter by engine (omit to show all)")
def models(engine: str | None) -> None:
    """List recommended models for each engine with hardware requirements."""

    engines_to_show = [engine] if engine else list(MODEL_RECOMMENDATIONS.keys())

    for eng in engines_to_show:
        meta = ENGINE_META.get(eng, {})
        console.print()
        console.print(f"[bold cyan]{meta.get('name', eng)}[/bold cyan] — {meta.get('description', '')}")

        table = Table(box=box.SIMPLE, header_style="bold white")
        table.add_column("Model", style="bold yellow")
        table.add_column("Size", style="cyan")
        table.add_column("Min VRAM", justify="right")
        table.add_column("Min RAM", justify="right")
        table.add_column("Description", style="dim")

        for m in MODEL_RECOMMENDATIONS[eng]:
            vram_str = f"{m['min_vram']} GB" if m['min_vram'] > 0 else "CPU-only"
            table.add_row(
                m["name"],
                m["size"],
                vram_str,
                f"{m['min_ram']} GB",
                m["desc"],
            )

        console.print(table)

    console.print()
    console.print("[dim]GPU VRAM = GPU video memory required; CPU RAM = system memory required.[/dim]")


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 大模型工具 - 命令行接口
"""

import os
import sys
import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt

from client import, ModelType, CopywritingStyle, PlatformType, OutputFormat

console = Console()


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       大模型工具                              ║
║                                                           ║
║       图像分析 | OCR提取 | 文案创作 | 多模态对话            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold blue")


def check_api_key():
    """检查 API Key 是否配置"""
    api_key = os.getenv("")
    if not api_key:
        console.print("✗ 错误: 未找到  API Key", style="red")
        console.print("\n请设置环境变量  或创建 .env 文件:", style="yellow")
        console.print("=", style="cyan")
        console.print("\n获取 API Key: https://platform./", style="blue")
        sys.exit(1)
    return api_key


@click.group()
def cli():
    """ 大模型工具 - 图像分析、OCR、文案创作、多模态对话"""
    print_banner()


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--prompt', '-p', default='请详细分析这张图片', help='分析提示词')
@click.option('--model', type=click.Choice(['', '', '']), default='', help='使用的模型')
@click.option('--temperature', '-t', type=float, default=0.7, help='创造性程度 (0-1)')
def analyze(image_path: str, prompt: str, model: str, temperature: float):
    """分析图片内容"""
    check_api_key()

    try:
        with console.status("[bold green]正在分析图片...", spinner="dots"):
            client = ()
            model_type = ModelType(model) if model else ModelType.

            result = client.analyze_image(
                image_path=image_path,
                prompt=prompt,
                model=model_type,
                temperature=temperature
            )

        console.print(Panel(result.content, title="[bold green]分析结果", border_style="green"))

    except Exception as e:
        console.print(f"✗ 分析失败: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--format', '-f', type=click.Choice(['text', 'structured', 'json']), default='text', help='输出格式')
@click.option('--language', '-l', default='auto', help='语言设置 (auto/zh/en)')
@click.option('--output', '-o', type=click.Path(), help='保存到文件')
def ocr(image_path: str, format: str, language: str, output: Optional[str]):
    """从图片中提取文字 (OCR)"""
    check_api_key()

    try:
        with console.status("[bold green]正在提取文字...", spinner="dots"):
            client = ()
            output_format = OutputFormat(format)

            result = client.extract_text(
                image_path=image_path,
                output_format=output_format,
                language=language
            )

        # 显示结果
        console.print(Panel(result.text, title=f"[bold green]OCR 结果 (置信度: {result.confidence:.2%})", border_style="green"))

        # 保存到文件
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result.text)
            console.print(f"✓ 结果已保存到: {output}", style="blue")

    except Exception as e:
        console.print(f"✗ OCR 提取失败: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.option('--image', '-i', type=click.Path(exists=True), help='产品图片')
@click.option('--prompt', '-p', default='', help='创作要求')
@click.option('--style', '-s', type=click.Choice(['professional', 'casual', 'creative', 'inspiring']), default='creative', help='文案风格')
@click.option('--platform', '-p', type=click.Choice(['wechat', 'weibo', 'xiaohongshu', 'douyin']), default='wechat', help='目标平台')
@click.option('--length', '-l', type=click.Choice(['short', 'medium', 'long']), default='medium', help='文案长度')
@click.option('--output', '-o', type=click.Path(), help='保存到文件')
def copywrite(image: Optional[str], prompt: str, style: str, platform: str, length: str, output: Optional[str]):
    """创作文案"""
    check_api_key()

    try:
        with console.status("[bold green]正在创作文案...", spinner="dots"):
            client = ()
            copy_style = CopywritingStyle(style)
            plat_type = PlatformType(platform)

            result = client.generate_copywriting(
                image_path=image,
                prompt=prompt,
                style=copy_style,
                platform=plat_type,
                length=length,
                temperature=0.8
            )

        # 显示结果
        table = Table(show_header=False, box=None)
        table.add_row(f"[bold cyan]标题:[/bold cyan] {result.title}")
        table.add_row(f"[bold cyan]平台:[/bold cyan] {result.platform}")
        table.add_row(f"[bold cyan]字数:[/bold cyan] {result.word_count}")
        table.add_row(f"[bold cyan]标签:[/bold cyan] {', '.join(result.tags)}")
        console.print(table)

        console.print(Panel(result.content, title="[bold green]文案内容", border_style="green"))

        # 保存到文件
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(f"# {result.title}\n\n")
                f.write(result.content)
            console.print(f"✓ 文案已保存到: {output}", style="blue")

    except Exception as e:
        console.print(f"✗ 文案创作失败: {e}", style="red")
        sys.exit(1)


@cli.command()
def chat():
    """交互式对话"""
    check_api_key()

    console.print("📸 [bold blue]交互式多模态对话[/bold blue]")
    console.print("输入 'quit' 或 'exit' 退出，输入 'image <路径>' 发送图片\n")

    try:
        client = ()
        conversation = client.create_conversation()

        while True:
            try:
                user_input = Prompt.ask("[bold cyan]你[/bold cyan]").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("👋 再见！", style="yellow")
                    break

                if not user_input:
                    continue

                # 检查是否是图片输入
                image_path = None
                message = user_input

                if user_input.lower().startswith('image '):
                    image_path = user_input[6:].strip()
                    if not os.path.exists(image_path):
                        console.print(f"✗ 图片文件不存在: {image_path}", style="red")
                        continue
                    message = "请分析这张图片"

                # 发送消息
                with console.status("[bold green]正在思考...", spinner="dots"):
                    response = conversation.chat(
                        message=message,
                        image_path=image_path
                    )

                console.print(Panel(response, title="[bold green]AI 助手[/bold green]", border_style="green"))

            except KeyboardInterrupt:
                console.print("\n✋ 使用 'quit' 或 'exit' 退出")
            except Exception as e:
                console.print(f"✗ 错误: {e}", style="red")

    except Exception as e:
        console.print(f"✗ 初始化失败: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('images', nargs=-1, type=click.Path(exists=True))
@click.option('--prompt', '-p', default='分析所有图片', help='分析提示词')
def batch(images: tuple, prompt: str):
    """批量分析多张图片"""
    check_api_key()

    if not images:
        console.print("✗ 请提供至少一张图片", style="red")
        sys.exit(1)

    try:
        client = ()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[green]批量分析图片...", total=len(images))

            results = []
            for image_path in images:
                result = client.analyze_image(image_path, prompt)
                results.append((image_path, result))
                progress.update(task, advance=1)

        # 显示所有结果
        for i, (image_path, result) in enumerate(results, 1):
            console.print(Panel(
                result.content,
                title=f"[bold green]图片 {i}: {Path(image_path).name}[/bold green]",
                border_style="green"
            ))

    except Exception as e:
        console.print(f"✗ 批量分析失败: {e}", style="red")
        sys.exit(1)


@cli.command()
def config():
    """配置检查"""
    console.print("[bold blue]配置检查[/bold blue]\n")

    # 检查 API Key
    api_key = os.getenv("")
    if api_key:
        console.print(f"✓ API Key: {api_key[:8]}...{api_key[-4:]}")
    else:
        console.print("✗ API Key: 未配置", style="red")

    # 检查 .env 文件
    env_file = Path(".env")
    if env_file.exists():
        console.print(f"✓ .env 文件: {env_file.absolute()}")
    else:
        console.print("✗ .env 文件: 不存在", style="yellow")

    # 检查示例配置
    example_file = Path(".env.example")
    if example_file.exists():
        console.print(f"✓ .env.example: {example_file.absolute()}")
    else:
        console.print("✗ .env.example: 不存在", style="yellow")

    console.print("\n[bold blue]可用模型[/bold blue]")
    console.print("• : 基础模型，8K 上下文")
    console.print("• : 扩展模型，32K 上下文")
    console.print("• : 大上下文模型，128K 上下文")

    console.print("\n[bold blue]获取帮助[/bold blue]")
    console.print("• API Key: https://platform./")
    console.print("• 文档: https://platform./docs")
    console.print("• 使用帮助:  --help")


if __name__ == '__main__':
    cli()

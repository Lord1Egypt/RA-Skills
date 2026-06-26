"""统一输出格式模块（text/json）"""
import json
import sys
from decimal import Decimal
from typing import Any

import click
from rich.console import Console
from rich.table import Table

console = Console()


class _DecimalEncoder(json.JSONEncoder):
    """将 Decimal 序列化为 float"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def print_json(data: Any) -> None:
    """以 JSON 格式输出数据"""
    click.echo(json.dumps(data, ensure_ascii=False, indent=2, cls=_DecimalEncoder))


def print_table(headers: list[str], rows: list[list[Any]], title: str = "") -> None:
    """用 rich 表格输出数据

    Args:
        headers: 列标题列表
        rows: 数据行列表（每行为与 headers 对应的值列表）
        title: 可选表格标题
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for h in headers:
        table.add_column(h, style="white")
    for row in rows:
        table.add_row(*[str(v) if v is not None else "-" for v in row])
    console.print(table)


def print_kv(pairs: list[tuple[str, Any]], title: str = "") -> None:
    """以键值对形式输出（用于单条记录）"""
    if title:
        console.print(f"[bold cyan]{title}[/bold cyan]")
    for k, v in pairs:
        v_str = str(v) if v is not None else "-"
        console.print(f"  [bold]{k}[/bold]: {v_str}")


def print_error(msg: str) -> None:
    """输出错误信息到 stderr"""
    click.echo(f"错误：{msg}", err=True)
    sys.exit(1)

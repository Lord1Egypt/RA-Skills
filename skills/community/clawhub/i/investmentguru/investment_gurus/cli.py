"""
命令行工具

Usage:
    invest-guru analyze -s 贵州茅台 -m duan
    invest-guru compare -s 宁德时代
    invest-guru advise -s 消费
    invest-guru list
"""

import click
import json
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from investment_gurus import InvestmentGuru


console = Console()


@click.group()
def cli():
    """投资大师分析工具 - 基于中国顶级投资大师的价值投资分析"""
    pass


@cli.command()
@click.option("-s", "--stock", required=True, help="股票代码或名称")
@click.option("-m", "--method", default="duan", help="分析方法 (duan/zhanglei/linyuan/danbing等)")
@click.option("-o", "--output", default=None, help="输出文件 (JSON)")
def analyze(stock: str, method: str, output: str):
    """分析股票"""
    try:
        guru = InvestmentGuru()
        result = guru.analyze(stock, method=method)
        
        # 显示结果
        console.print(f"\n[bold cyan]分析结果: {result.stock_name}[/bold cyan]")
        console.print(f"大师: {result.guru_name} ({result.guru_method})")
        console.print(f"综合评分: {result.overall_score}/100")
        console.print(f"建议: [green]{result.recommendation}[/green]")
        console.print(f"持有期: {result.holding_period}")
        
        console.print("\n[bold]各项评分:[/bold]")
        console.print(f"  商业模式: {result.business_score}")
        console.print(f"  估值合理性: {result.valuation_score}")
        console.print(f"  成长性: {result.growth_score}")
        console.print(f"  竞争优势: {result.competitive_score}")
        console.print(f"  管理团队: {result.management_score}")
        
        if result.pros:
            console.print("\n[bold green]优势:[/bold green]")
            for pro in result.pros:
                console.print(f"  ✓ {pro}")
        
        if result.cons:
            console.print("\n[bold red]风险:[/bold red]")
            for con in result.cons:
                console.print(f"  ✗ {con}")
        
        # 保存结果
        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
            console.print(f"\n结果已保存到: {output}")
            
    except Exception as e:
        console.print(f"[red]分析失败: {e}[/red]")


@cli.command()
@click.option("-s", "--stock", required=True, help="股票代码或名称")
@click.option("-o", "--output", default=None, help="输出文件 (JSON)")
def compare(stock: str, output: str):
    """对比所有大师的分析"""
    try:
        guru = InvestmentGuru()
        result = guru.compare(stock)
        
        console.print(f"\n[bold cyan]多大师对比分析: {result.stock_name}[/bold cyan]\n")
        
        # 创建表格
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("大师", style="cyan")
        table.add_column("方法", style="blue")
        table.add_column("综合评分", justify="right")
        table.add_column("建议", style="green")
        
        for name, analysis in result.analyses.items():
            table.add_row(
                name,
                analysis.get("method", ""),
                str(analysis.get("overall_score", 0)),
                analysis.get("recommendation", "")
            )
        
        console.print(table)
        
        console.print(f"\n[bold]共识:[/bold] {result.consensus}")
        console.print(f"[bold]最佳方法:[/bold] {result.best_guru}")
        console.print(f"[bold]平均评分:[/bold] {result.average_score}")
        
        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump({
                    "stock_code": result.stock_code,
                    "stock_name": result.stock_name,
                    "consensus": result.consensus,
                    "best_guru": result.best_guru,
                    "average_score": result.average_score,
                    "analyses": result.analyses,
                }, f, ensure_ascii=False, indent=2)
            console.print(f"\n结果已保存到: {output}")
            
    except Exception as e:
        console.print(f"[red]对比失败: {e}[/red]")


@cli.command()
@click.option("-s", "--sector", required=True, help="行业名称")
def advise(sector: str):
    """获取行业投资建议"""
    try:
        guru = InvestmentGuru()
        advice = guru.get_advice(sector)
        
        console.print(f"\n[bold cyan]行业投资建议: {sector}[/bold cyan]\n")
        
        if "message" in advice:
            console.print(f"[yellow]{advice['message']}[/yellow]")
            return
        
        console.print(f"推荐大师: {', '.join(advice.get('recommended_gurus', []))}")
        console.print(f"关注重点: {advice.get('focus', '')}")
        
        if advice.get("stocks"):
            console.print("\n[bold]代表股票:[/bold]")
            for stock in advice["stocks"]:
                console.print(f"  • {stock}")
                
    except Exception as e:
        console.print(f"[red]获取建议失败: {e}[/red]")


@cli.command()
def list():
    """列出所有可用的大师和方法"""
    guru = InvestmentGuru()
    gurus = guru.get_available_gurus()
    
    console.print("\n[bold cyan]可用投资大师:[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("大师", style="cyan")
    table.add_column("别名", style="blue")
    table.add_column("核心理念", style="white")
    
    guru_instances = {
        "duan": ("段永平", "中国巴菲特"),
        "zhanglei": ("张磊", "高瓴资本"),
        "lilu": ("李录", "芒格传人"),
        "qiuguoluo": ("邱国鹭", "高毅资产"),
        "wangguobin": ("王国斌", "泉果基金"),
        "linyuan": ("林园", "民间股神"),
        "danbing": ("但斌", "东方港湾"),
    }
    
    for g in ["duan", "zhanglei", "lilu", "qiuguoluo", "wangguobin", "linyuan", "danbing"]:
        alias, _ = guru_instances.get(g, (g, ""))
        table.add_row(g, alias, guru.GURUS[g].__doc__.strip()[:30] if guru.GURUS[g].__doc__ else "")
    
    console.print(table)


def main():
    cli()


if __name__ == "__main__":
    main()
"""CLI for openai-ban-tracker — OpenAI 封号风险检测与解封追踪."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from .knowledge import (
    BAN_REASONS, APPEAL_TEMPLATES, RISK_QUESTIONS,
    COMMUNITY_SIGNALS, calculate_risk_score,
    RiskLevel,
)

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """🔍 OpenAI 封号风险检测与解封追踪工具
    
    检测你的 OpenAI 账号封号风险，了解常见封号原因，
    生成申诉邮件模板，追踪社区最新封号/解封动态。
    """
    pass


@main.command()
@click.option("--interactive/--no-interactive", default=True,
              help="交互式问卷模式（默认）")
def risk_check(interactive):
    """检测你的 OpenAI 账号封号风险"""
    console.print()
    console.print(Panel(
        "[bold yellow]⚠️  封号风险评估[/bold yellow]\n"
        "回答以下问题，评估你的账号被封风险。\n"
        "所有数据仅在本地处理，不上传任何信息。",
        border_style="yellow"
    ))
    console.print()
    
    answers = {}
    
    if interactive:
        for q in RISK_QUESTIONS:
            console.print(f"  [bold]{q.question}[/bold]")
            resp = click.prompt("  (y/n)", type=str, default="n").lower()
            answers[q.id] = resp in ("y", "yes")
            console.print()
        
        score, level, details = calculate_risk_score(answers)
        
        # Display result
        level_colors = {
            RiskLevel.SAFE: "green",
            RiskLevel.LOW: "bright_green",
            RiskLevel.MEDIUM: "bright_yellow",
            RiskLevel.HIGH: "red",
            RiskLevel.CRITICAL: "bold red",
        }
        
        color = level_colors.get(level, "white")
        
        console.print(Panel(
            f"[bold {color}]风险评分: {score:.0f}/100[/bold {color}]\n"
            f"[bold {color}]风险等级: {level.value[0]}[/bold {color}]",
            border_style=color
        ))
        console.print()
        
        # Detail breakdown
        table = Table(title="详细分析", box=box.ROUNDED)
        table.add_column("问题", style="dim")
        table.add_column("风险")
        
        for question, risk in details:
            rcolor = level_colors.get(risk, "white")
            table.add_row(question, f"[{rcolor}]{risk.value[0]}[/{rcolor}]")
        
        console.print(table)
        console.print()
        
        # Advice
        if level in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            console.print(Panel(
                "[bold red]⚠️  建议[/bold red]\n\n"
                "1. 立即停止使用第三方代充服务\n"
                "2. 使用独享账号，不要合租\n"
                "3. 固定 VPN 节点，减少 IP 跳变\n"
                "4. 联系 OpenAI 客服说明情况\n"
                "5. 使用 'openai-ban-tracker appeal' 生成申诉邮件\n\n"
                "如果已经被封，参考 'openai-ban-tracker status' 了解最新解封动态。",
                border_style="red"
            ))
        elif level == RiskLevel.MEDIUM:
            console.print("[yellow]建议: 注意 IP 稳定性，开启 2FA，避免可疑操作。[/yellow]")
        else:
            console.print("[green]✓ 你的风险等级较低，继续保持！[/green]")
    else:
        # Quick check — just list risk factors
        console.print("[bold]快速风险检查清单:[/bold]\n")
        table = Table(box=box.SIMPLE)
        table.add_column("#")
        table.add_column("风险因素")
        table.add_column("状态")
        
        for i, q in enumerate(RISK_QUESTIONS, 1):
            table.add_row(str(i), q.question, "⬜ 未检查")
        
        console.print(table)
        console.print("\n[dim]使用 --interactive 进行交互式风险评估[/dim]")


@main.command(name="ban-reasons")
def ban_reasons():
    """查看所有已知 OpenAI 封号原因"""
    console.print()
    console.print(Panel(
        "[bold red]📋 已知 OpenAI 封号原因[/bold red]\n"
        f"共 {len(BAN_REASONS)} 种常见原因，按风险等级排序",
        border_style="red"
    ))
    console.print()
    
    for reason in BAN_REASONS:
        level = reason.risk_level
        level_colors = {
            RiskLevel.SAFE: "green",
            RiskLevel.LOW: "bright_green",
            RiskLevel.MEDIUM: "bright_yellow",
            RiskLevel.HIGH: "red",
            RiskLevel.CRITICAL: "bold red",
        }
        color = level_colors.get(level, "white")
        
        console.print(f"[bold {color}]▸ {reason.title_zh} ({reason.title_en})[/bold {color}]")
        console.print(f"  风险等级: [{color}]{level.value[0]}[/{color}]")
        console.print(f"  申诉成功率: {reason.appeal_success_rate}")
        console.print(f"  描述: {reason.description_zh}")
        
        if reason.common_patterns:
            console.print("  常见模式:")
            for p in reason.common_patterns:
                console.print(f"    • {p}")
        
        if reason.prevention_tips:
            console.print("  预防建议:")
            for tip in reason.prevention_tips:
                console.print(f"    [green]✓[/green] {tip}")
        
        console.print()


@main.command()
@click.option("--lang", type=click.Choice(["en", "zh"]), default="zh",
              help="申诉邮件语言 (zh=中文, en=英文)")
@click.option("--output", type=click.Path(), default=None,
              help="输出到文件（可选）")
def appeal(lang, output):
    """生成 OpenAI 账号申诉邮件模板"""
    template = APPEAL_TEMPLATES.get(lang, APPEAL_TEMPLATES["en"])
    
    content = f"Subject: {template.subject}\n\n{template.body}"
    
    if output:
        with open(output, "w") as f:
            f.write(content)
        console.print(f"[green]✓ 申诉邮件模板已保存到 {output}[/green]")
    else:
        console.print()
        console.print(Panel(
            f"[bold]📧 申诉邮件模板 ({lang.upper()})[/bold]",
            border_style="cyan"
        ))
        console.print()
        console.print(f"[bold]收件人:[/bold] support@openai.com 或通过 help.openai.com 提交")
        console.print(f"[bold]主题:[/bold] {template.subject}")
        console.print()
        console.print(template.body)
        console.print()
        console.print(Panel(
            "[bold yellow]💡 申诉技巧[/bold yellow]\n\n"
            "1. 使用注册邮箱发送申诉\n"
            "2. 附上支付凭证截图（如有）\n"
            "3. 说明你的使用场景（个人编程/工作/研究）\n"
            "4. 保持礼貌和专业，不要情绪化\n"
            "5. 如果一周内无回复，重新提交\n"
            "6. 不要同时多次提交，避免重复\n\n"
            "OpenAI 申诉入口: https://help.openai.com",
            border_style="yellow"
        ))


@main.command()
def status():
    """查看社区最新封号/解封动态"""
    console.print()
    console.print(Panel(
        "[bold]📡 社区信号追踪[/bold]\n"
        "数据来源: V2EX, Reddit, Twitter/X 等社区",
        border_style="blue"
    ))
    console.print()
    
    table = Table(title="最新动态", box=box.ROUNDED)
    table.add_column("日期", style="dim")
    table.add_column("事件")
    table.add_column("热度", justify="right")
    table.add_column("级别")
    
    severity_colors = {
        "critical": "bold red",
        "warning": "bright_yellow",
        "info": "cyan",
    }
    
    for date, title, replies, severity in COMMUNITY_SIGNALS:
        sc = severity_colors.get(severity, "white")
        sev_label = {
            "critical": "🔴 严重",
            "warning": "🟡 警告",
            "info": "🔵 信息",
        }.get(severity, severity)
        table.add_row(date, title, f"{replies} 回复", f"[{sc}]{sev_label}[/{sc}]")
    
    console.print(table)
    console.print()
    
    # Summary
    crit_count = sum(1 for s in COMMUNITY_SIGNALS if s[3] == "critical")
    warn_count = sum(1 for s in COMMUNITY_SIGNALS if s[3] == "warning")
    
    console.print(Panel(
        f"[bold]📊 近期趋势[/bold]\n\n"
        f"严重事件: {crit_count} 起\n"
        f"警告事件: {warn_count} 起\n\n"
        "[bold yellow]当前状态: 封号潮持续中，已有解封案例出现[/bold yellow]\n"
        "建议: 暂停代充/合租行为，等待风控稳定\n\n"
        "[dim]数据更新: 2026-06-06 | 下次扫描建议: 每日检查[/dim]",
        border_style="blue"
    ))


@main.command()
def scan():
    """扫描社区最新封号/解封动态（联网）"""
    console.print()
    console.print("[bold]📡 正在扫描社区...[/bold]")
    console.print()
    
    import urllib.request
    import json
    from datetime import datetime
    
    nodes = ["openai", "agent", "aigc"]
    new_signals = []
    
    for node in nodes:
        try:
            url = f"https://www.v2ex.com/api/topics/show.json?node_name={node}"
            req = urllib.request.Request(url, headers={"User-Agent": "openai-ban-tracker/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
            
            ban_kw = ["封号", "封", "ban", "suspend", "解封", "代充", "降级"]
            for topic in data[:20]:
                title = topic.get("title", "")
                if any(kw in title for kw in ban_kw):
                    created = datetime.fromtimestamp(topic.get("created", 0))
                    new_signals.append((
                        created.strftime("%Y-%m-%d"),
                        title,
                        topic.get("replies", 0),
                        "warning",
                        node,
                    ))
        except Exception as e:
            console.print(f"[dim]  节点 {node}: 扫描失败 ({e})[/dim]")
    
    if new_signals:
        table = Table(title="实时扫描结果", box=box.ROUNDED)
        table.add_column("日期")
        table.add_column("节点")
        table.add_column("标题")
        table.add_column("回复", justify="right")
        
        for date, title, replies, _, node in new_signals[:15]:
            table.add_row(date, f"[dim]{node}[/dim]", title[:60], str(replies))
        
        console.print(table)
        console.print(f"\n[green]共发现 {len(new_signals)} 条相关信号[/green]")
    else:
        console.print("[yellow]未发现新的封号相关信号[/yellow]")
    
    console.print()


if __name__ == "__main__":
    main()

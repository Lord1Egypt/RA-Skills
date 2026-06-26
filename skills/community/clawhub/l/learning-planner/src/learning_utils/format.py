"""
格式化工具
"""
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import box

console = Console()


def format_datetime(dt_str: str) -> str:
    """格式化日期时间"""
    if not dt_str:
        return "-"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return dt_str


def format_date(dt_str: str) -> str:
    """格式化日期"""
    if not dt_str:
        return "-"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except:
        return dt_str


def format_duration(minutes: int) -> str:
    """格式化时长"""
    if not minutes:
        return "-"
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}小时{mins}分钟"
    return f"{mins}分钟"


def print_progress_bar(current: float, total: float, width: int = 30) -> str:
    """打印进度条"""
    if not total:
        return "[grey]无进度数据[/grey]"
    
    percent = min(100, current / total * 100)
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    
    if percent >= 100:
        color = "green"
    elif percent >= 50:
        color = "blue"
    else:
        color = "yellow"
    
    return f"[{color}]{bar}[/{color}] {percent:.1f}%"


def print_goal_table(goals: list, title: str = "学习目标"):
    """打印目标表格"""
    if not goals:
        console.print("[yellow]暂无目标[/yellow]")
        return
    
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("名称", style="green", width=30)
    table.add_column("优先级", width=8)
    table.add_column("进度", width=35)
    table.add_column("状态", width=8)
    
    priority_map = {
        "high": "[red]高[/red]",
        "medium": "[yellow]中[/yellow]",
        "low": "[blue]低[/blue]",
    }
    
    status_map = {
        "active": "[blue]进行中[/blue]",
        "completed": "[green]已完成[/green]",
        "paused": "[grey]暂停[/grey]",
    }
    
    for goal in goals:
        table.add_row(
            str(goal.get("id")),
            goal.get("title", "-")[:30],
            priority_map.get(goal.get("priority"), goal.get("priority")),
            print_progress_bar(goal.get("progress", 0), 100),
            status_map.get(goal.get("status"), goal.get("status")),
        )
    
    console.print(table)


def print_goal_tree(goals: list, title: str = "技能树"):
    """打印目标树"""
    if not goals:
        console.print("[yellow]暂无目标[/yellow]")
        return
    
    tree = Tree(f"[bold cyan]🎯 {title}[/bold cyan]")
    
    def add_children(node, goals_list):
        for goal in goals_list:
            progress = goal.get("progress", 0)
            progress_str = f"[{progress:.0f}%]"
            
            if progress >= 100:
                style = "green"
            elif progress >= 50:
                style = "blue"
            else:
                style = "yellow"
            
            child = node.add(f"[{style}]{goal.get('title')} {progress_str}[/{style}]")
            if goal.get("children"):
                add_children(child, goal["children"])
    
    add_children(tree, goals)
    console.print(tree)


def print_plan_table(plans: list, title: str = "学习计划"):
    """打印计划表格"""
    if not plans:
        console.print("[yellow]暂无计划[/yellow]")
        return
    
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("任务", width=35)
    table.add_column("日期", width=12)
    table.add_column("时长", width=10)
    table.add_column("状态", width=8)
    
    status_map = {
        "pending": "[yellow]待完成[/yellow]",
        "completed": "[green]已完成[/green]",
        "postponed": "[grey]已推迟[/grey]",
    }
    
    for plan in plans:
        table.add_row(
            str(plan.get("id")),
            plan.get("title", "-")[:35],
            plan.get("scheduled_date", "-"),
            f"{plan.get('estimated_minutes', 0)}分钟",
            status_map.get(plan.get("status"), plan.get("status")),
        )
    
    console.print(table)


def print_card(card: dict, show_answer: bool = False):
    """打印卡片"""
    content = f"""
[bold cyan]📝 问题[/bold cyan]
{card.get('front', '无内容')}

[bold]标签:[/bold] {', '.join(card.get('tags', [])) if card.get('tags') else '无'}
[bold]重复次数:[/bold] {card.get('repetitions', 0)}
[bold]难度系数:[/bold] {card.get('ease_factor', 2.5):.2f}
    """.strip()
    
    if show_answer:
        content += f"""

[bold green]✅ 答案[/bold green]
{card.get('back', '无内容')}
        """.strip()
    
    console.print(Panel(content, box=box.ROUNDED))


def print_resource_table(resources: list, title: str = "学习资源"):
    """打印资源表格"""
    if not resources:
        console.print("[yellow]暂无资源[/yellow]")
        return
    
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("名称", width=30)
    table.add_column("类型", width=10)
    table.add_column("标签", width=20)
    
    type_map = {
        "video": "[red]视频[/red]",
        "article": "[blue]文章[/blue]",
        "book": "[green]书籍[/green]",
        "documentation": "[yellow]文档[/yellow]",
    }
    
    for resource in resources:
        tags = ", ".join(resource.get("tags", []))[:20] if resource.get("tags") else "-"
        table.add_row(
            str(resource.get("id")),
            resource.get("title", "-")[:30],
            type_map.get(resource.get("resource_type"), resource.get("resource_type")),
            tags,
        )
    
    console.print(table)


def print_stats_panel(stats: dict, title: str = "学习统计"):
    """打印统计面板"""
    content = ""
    for key, value in stats.items():
        content += f"[bold]{key}:[/bold] {value}\n"
    
    console.print(Panel(content.strip(), title=title, box=box.ROUNDED))

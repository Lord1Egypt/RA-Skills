"""CLI 入口 — click 命令行工具。

子命令：
- crawl: 运行爬虫
- list: 列出作品/站点
- status: 查看系统状态
- broadcast: 手动触发播报
- schedule: 管理定时任务
- rss: 生成 RSS 订阅源
"""

import subprocess
import sys
from typing import Optional

import click

from src.config import get_setting, load_all_sites, load_settings


@click.group()
@click.version_option(version="0.1.0", prog_name="lobster")
def main() -> None:
    """龙虾爬虫技能 — 定向抓取 Webnovel/ReelShorts 等站点内容。"""
    pass


@main.command()
@click.argument("spider_name")
@click.option("-a", "--arg", multiple=True, help="爬虫参数，格式 key=value")
def crawl(spider_name: str, arg: tuple[str, ...]) -> None:
    """运行指定爬虫。

    SPIDER_NAME: 爬虫名称（webnovel / reelshorts）
    """
    cmd = [sys.executable, "-m", "scrapy", "crawl", spider_name]
    for a in arg:
        cmd.extend(["-a", a])

    click.echo(f"Starting spider: {spider_name}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        click.echo(f"Spider exited with code {result.returncode}", err=True)
        raise SystemExit(result.returncode)


@main.command("list")
@click.option("--site", default=None, help="按站点过滤")
@click.option("--grade", default=None, help="按分级过滤 (high/medium/low)")
@click.option("--limit", default=20, help="显示数量")
def list_novels(site: Optional[str], grade: Optional[str], limit: int) -> None:
    """列出已抓取的作品。"""
    from src.models import Novel, init_db

    session = init_db()
    query = session.query(Novel)
    if site:
        query = query.filter_by(site=site)
    if grade:
        query = query.filter_by(grade=grade)

    novels = query.order_by(Novel.last_updated.desc()).limit(limit).all()

    if not novels:
        click.echo("暂无数据。")
        return

    click.echo(f"{'ID':<6} {'站点':<12} {'标题':<30} {'分级':<8} {'更新时间'}")
    click.echo("-" * 80)
    for n in novels:
        updated = n.last_updated.strftime("%Y-%m-%d %H:%M") if n.last_updated else "N/A"
        title = n.title[:28] + ".." if len(n.title) > 30 else n.title
        click.echo(f"{n.id:<6} {n.site:<12} {title:<30} {n.grade:<8} {updated}")

    session.close()


@main.command()
def status() -> None:
    """查看系统状态。"""
    from src.models import Chapter, Episode, Novel, init_db

    config = load_settings()
    sites = load_all_sites()

    click.echo("=== 龙虾爬虫状态 ===\n")
    click.echo(f"项目版本: {config.get('project', {}).get('version', '?')}")
    click.echo(f"数据库: {get_setting('database', 'path', default='data/lobster.db')}")
    click.echo(f"已配置站点: {', '.join(sites.keys())}")
    click.echo()

    try:
        session = init_db()
        novel_count = session.query(Novel).count()
        chapter_count = session.query(Chapter).count()
        episode_count = session.query(Episode).count()
        click.echo(f"作品数: {novel_count}")
        click.echo(f"章节数: {chapter_count}")
        click.echo(f"剧集数: {episode_count}")

        # 按分级统计
        for grade in ("high", "medium", "low"):
            count = session.query(Novel).filter_by(grade=grade).count()
            click.echo(f"  {grade}: {count}")

        session.close()
    except Exception as e:
        click.echo(f"数据库连接失败: {e}")


@main.command()
@click.option("--site", default=None, help="指定站点")
@click.option("--grade", default=None, help="指定分级")
@click.option("--title", default="龙虾爬虫更新通知", help="消息标题")
def broadcast(site: Optional[str], grade: Optional[str], title: str) -> None:
    """手动触发钉钉播报。"""
    from src.broadcast import render_daily_digest, send_markdown
    from src.models import Chapter, Novel, init_db

    session = init_db()
    query = session.query(Novel)
    if site:
        query = query.filter_by(site=site)
    if grade:
        query = query.filter_by(grade=grade)

    novels = query.order_by(Novel.last_updated.desc()).limit(20).all()

    if not novels:
        click.echo("暂无数据可播报。")
        return

    items = []
    for novel in novels:
        ch_count = session.query(Chapter).filter_by(novel_id=novel.id).count()
        items.append({"novel": novel, "new_count": ch_count})

    content = render_daily_digest(items)
    click.echo("生成的消息：")
    click.echo(content)
    click.echo()

    if click.confirm("确认发送到钉钉？"):
        success = send_markdown(title=title, content=content)
        click.echo("发送成功！" if success else "发送失败，请检查 Webhook 配置。")

    session.close()


@main.command()
@click.option("--action", type=click.Choice(["start", "list", "load"]), default="list")
def schedule(action: str) -> None:
    """管理定时任务。"""
    from src.scheduler import ScheduleManager

    mgr = ScheduleManager()

    if action == "load":
        count = mgr.load_from_config()
        click.echo(f"已从配置加载 {count} 个定时任务。")
        for job in mgr.list_jobs():
            click.echo(f"  {job['job_id']}: {job['cron']} ({job['status']})")

    elif action == "start":
        mgr.load_from_config()
        click.echo("启动调度器（Ctrl+C 停止）...")
        mgr.start()
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            mgr.stop()
            click.echo("\n调度器已停止。")

    elif action == "list":
        jobs = mgr.list_jobs()
        if not jobs:
            click.echo("暂无定时任务。使用 --action=load 从配置加载。")
        for job in jobs:
            click.echo(f"  {job['job_id']}: {job['cron']} → {job['spider_name']} ({job['status']})")


@main.command()
@click.option("--output", default="data/rss.xml", help="输出文件路径")
@click.option("--format", "fmt", type=click.Choice(["rss", "atom"]), default="rss")
@click.option("--site", default=None, help="按站点过滤")
@click.option("--grade", default=None, help="按分级过滤")
def rss(output: str, fmt: str, site: Optional[str], grade: Optional[str]) -> None:
    """生成 RSS/Atom 订阅源。"""
    from src.rss import write_atom, write_rss

    kwargs = {}
    if site:
        kwargs["site"] = site
    if grade:
        kwargs["grade"] = grade

    if fmt == "atom":
        path = write_atom(output, **kwargs)
    else:
        path = write_rss(output, **kwargs)

    click.echo(f"已生成 {fmt.upper()} 文件: {path}")


if __name__ == "__main__":
    main()

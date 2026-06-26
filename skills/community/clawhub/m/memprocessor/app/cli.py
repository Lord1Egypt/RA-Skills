"""CLI工具"""
import asyncio
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from app.config import settings
from app.models import SetMemoryRequest, SearchRequest

app = typer.Typer(help="DreamMoon Memory Processor CLI")
console = Console()


@app.command()
def init():
    """初始化记忆系统"""
    async def _init():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        stats = await service.get_stats()
        
        console.print("[green]✅ Memory system initialized[/green]")
        console.print(f"L1 entries: {stats.l1_entries}")
        console.print(f"L2 entries: {stats.l2_entries}")
        console.print(f"L3 files: {stats.l3_files}")
        console.print(f"L4 vectors: {stats.l4_vectors}")
    
    asyncio.run(_init())


@app.command()
def set(
    key: str = typer.Argument(..., help="记忆键名"),
    content: str = typer.Argument(..., help="记忆内容"),
    importance: Optional[int] = typer.Option(None, "--importance", "-i", help="重要性评分(0-100)")
):
    """存储记忆"""
    async def _set():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        
        request = SetMemoryRequest(
            key=key,
            content=content,
            importance=importance
        )
        
        result = await service.set(request)
        console.print(f"[green]✅ Stored:[/green] {key}")
        console.print(f"  Importance: {result.importance_score}")
        console.print(f"  Level: {result.persisted_level}")
    
    asyncio.run(_set())


@app.command()
def get(key: str = typer.Argument(..., help="记忆键名")):
    """获取记忆"""
    async def _get():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        
        result = await service.get(key)
        if result.found:
            console.print(f"[green]✅ Found:[/green] {key}")
            console.print(f"  Level: {result.from_level}")
            console.print(f"  Content: {result.item.content[:200]}...")
        else:
            console.print(f"[red]❌ Not found:[/red] {key}")
    
    asyncio.run(_get())


@app.command()
def search(
    query: str = typer.Argument(..., help="搜索关键词"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="返回结果数量")
):
    """搜索记忆"""
    async def _search():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        
        request = SearchRequest(query=query, top_k=top_k)
        result = await service.search(request)
        
        table = Table(title=f'Search Results for "{query}"')
        table.add_column("Key", style="cyan")
        table.add_column("Similarity", style="green")
        table.add_column("Level", style="yellow")
        table.add_column("Content", style="white")
        
        for r in result.results:
            table.add_row(
                r.key,
                f"{r.similarity:.3f}",
                r.level.value,
                r.content[:50] + "..."
            )
        
        console.print(table)
        console.print(f"Search time: {result.search_time_ms:.2f}ms")
    
    asyncio.run(_search())


@app.command()
def stats():
    """显示统计信息"""
    async def _stats():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        
        stats = await service.get_stats()
        
        table = Table(title="Storage Statistics")
        table.add_column("Layer", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("L1 (Hot)", f"{stats.l1_entries} entries")
        table.add_row("L2 (Warm)", f"{stats.l2_entries} entries")
        table.add_row("L3 (Cold)", f"{stats.l3_files} files")
        table.add_row("L4 (Archive)", f"{stats.l4_vectors} vectors")
        table.add_row("Total Memory", f"{stats.total_memory_mb:.2f} MB")
        
        console.print(table)
    
    asyncio.run(_stats())


@app.command()
def daily():
    """执行每日沉淀任务"""
    async def _daily():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        
        console.print("[yellow]Running daily persistence...[/yellow]")
        await service.run_daily_persistence()
        console.print("[green]✅ Daily persistence completed[/green]")
    
    asyncio.run(_daily())


@app.command()
def weekly():
    """执行每周归档任务"""
    async def _weekly():
        from app.services.memory_service import get_memory_service
        service = await get_memory_service()
        
        console.print("[yellow]Running weekly archive...[/yellow]")
        await service.run_weekly_archive()
        console.print("[green]✅ Weekly archive completed[/green]")
    
    asyncio.run(_weekly())


@app.command()
def serve(
    host: str = typer.Option(settings.HOST, "--host", "-h"),
    port: int = typer.Option(settings.PORT, "--port", "-p"),
    reload: bool = typer.Option(False, "--reload")
):
    """启动API服务器"""
    import uvicorn
    
    console.print(f"[green]Starting server at {host}:{port}[/green]")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )


def main():
    """CLI入口"""
    app()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Task Scheduler - CLI Entry Point
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
LIB_DIR = SCRIPT_DIR.parent / 'lib'
sys.path.insert(0, str(LIB_DIR))

from scheduler import TaskScheduler, TaskPriority, TaskStatus


def priority_from_string(s: str) -> TaskPriority:
    """Convert string to TaskPriority"""
    return {
        "low": TaskPriority.LOW,
        "medium": TaskPriority.MEDIUM,
        "high": TaskPriority.HIGH,
        "urgent": TaskPriority.URGENT
    }.get(s.lower(), TaskPriority.MEDIUM)


def format_task(task) -> str:
    """Format task for display"""
    created = datetime.fromtimestamp(task.created_at).strftime("%Y-%m-%d %H:%M:%S")
    duration = f"{task.duration_ms}ms" if task.duration_ms else "N/A"
    
    lines = [
        f"Task: {task.id}",
        f"  Description: {task.description}",
        f"  Status: {task.status.value}",
        f"  Priority: {task.priority.name}",
        f"  Created: {created}",
        f"  Duration: {duration}",
    ]
    
    if task.error:
        lines.append(f"  Error: {task.error}")
    
    if task.result:
        lines.append(f"  Result: {str(task.result)[:100]}...")
    
    return "\n".join(lines)


async def cmd_create(args):
    """Create a task"""
    scheduler = TaskScheduler()
    
    priority = priority_from_string(args.priority)
    params = json.loads(args.params) if args.params else {}
    
    task = scheduler.create_task(
        description=args.description,
        priority=priority,
        params=params
    )
    
    print(f"✅ Task created: {task.id}")
    print(format_task(task))


async def cmd_list(args):
    """List tasks"""
    scheduler = TaskScheduler()
    
    status = None
    if args.status:
        status = TaskStatus(args.status)
    
    tasks = scheduler.list_tasks(status=status, limit=args.limit)
    
    print(f"\n📋 Tasks ({len(tasks)})")
    print("=" * 60)
    
    for task in tasks:
        print(f"\n{format_task(task)}")


async def cmd_get(args):
    """Get task details"""
    scheduler = TaskScheduler()
    task = scheduler.get_task(args.id)
    
    if not task:
        print(f"❌ Task not found: {args.id}", file=sys.stderr)
        sys.exit(1)
    
    print(format_task(task))


async def cmd_cancel(args):
    """Cancel a task"""
    scheduler = TaskScheduler()
    
    if scheduler.cancel_task(args.id):
        print(f"✅ Task cancelled: {args.id}")
    else:
        print(f"❌ Failed to cancel task: {args.id}", file=sys.stderr)
        sys.exit(1)


async def cmd_retry(args):
    """Retry a failed task"""
    scheduler = TaskScheduler()
    
    if scheduler.retry_task(args.id):
        print(f"✅ Task retrying: {args.id}")
    else:
        print(f"❌ Failed to retry task: {args.id}", file=sys.stderr)
        sys.exit(1)


async def cmd_daemon(args):
    """Run scheduler daemon"""
    scheduler = TaskScheduler(max_concurrency=args.concurrency)
    
    print(f"🚀 Starting Task Scheduler")
    print(f"   Concurrency: {args.concurrency}")
    print(f"   WebSocket port: {args.ws_port}")
    
    await scheduler.start()
    
    try:
        print("\n✅ Scheduler running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        await scheduler.stop()
        print("✅ Scheduler stopped")


def main():
    parser = argparse.ArgumentParser(
        description='Task Scheduler - Background task queue'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # create command
    create_parser = subparsers.add_parser('create', help='Create a task')
    create_parser.add_argument('--description', '-d', required=True)
    create_parser.add_argument('--priority', '-p', default='medium',
                              choices=['low', 'medium', 'high', 'urgent'])
    create_parser.add_argument('--params', default='{}', help='JSON parameters')
    create_parser.set_defaults(func=cmd_create)
    
    # list command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=[s.value for s in TaskStatus])
    list_parser.add_argument('--limit', '-l', type=int, default=10)
    list_parser.set_defaults(func=cmd_list)
    
    # get command
    get_parser = subparsers.add_parser('get', help='Get task details')
    get_parser.add_argument('--id', required=True)
    get_parser.set_defaults(func=cmd_get)
    
    # cancel command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel a task')
    cancel_parser.add_argument('--id', required=True)
    cancel_parser.set_defaults(func=cmd_cancel)
    
    # retry command
    retry_parser = subparsers.add_parser('retry', help='Retry a failed task')
    retry_parser.add_argument('--id', required=True)
    retry_parser.set_defaults(func=cmd_retry)
    
    # daemon command
    daemon_parser = subparsers.add_parser('daemon', help='Run scheduler daemon')
    daemon_parser.add_argument('--concurrency', '-c', type=int, default=4)
    daemon_parser.add_argument('--ws-port', type=int, default=8080)
    daemon_parser.set_defaults(func=cmd_daemon)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Run async command
    asyncio.run(args.func(args))


if __name__ == '__main__':
    main()

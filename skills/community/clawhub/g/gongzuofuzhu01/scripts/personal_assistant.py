#!/usr/bin/env python3
"""Personal Assistant Skill — CLI entry point."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 添加父目录到 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.progress import ProgressTracker
from scripts.recurring import RecurringManager
from scripts.reminder import ReminderEngine
from scripts.okr import OKRManager
from scripts.report import ReportGenerator
from scripts.advisor import Advisor

def get_managers():
    """初始化并返回所有 manager 实例"""
    db = Database()
    db.init_db()
    tm = TaskManager(db)
    pt = ProgressTracker(db, tm)
    rm = RecurringManager(db, tm)
    engine = ReminderEngine(db, tm)
    okr = OKRManager(db)
    report = ReportGenerator(db, tm, pt, okr)
    advisor = Advisor(db, tm, okr)
    return db, tm, pt, rm, engine, okr, report, advisor

# ======================================================================
# task 子命令
# ======================================================================

def cmd_task(args):
    """任务管理"""
    _, tm, _, _, _, _, _, _ = get_managers()

    if args.action == 'add':
        kwargs = {}
        if args.priority:
            kwargs['priority'] = args.priority
        if args.deadline:
            kwargs['deadline'] = args.deadline
        if args.category:
            kwargs['category'] = args.category
        if args.estimated_hours:
            kwargs['estimated_hours'] = args.estimated_hours
        if args.description:
            kwargs['description'] = args.description
        tid = tm.add(args.title, **kwargs)
        t = tm.get(tid)
        did = t.get('display_id') or f"N{tid:03d}" if t else str(tid)
        print(f"✅ 任务已创建: {did} — {args.title}")

    elif args.action == 'list':
        tasks = tm.list(
            status=args.status,
            category=args.category,
            priority_min=args.priority_min,
            priority_max=args.priority_max,
            search=args.search,
            limit=args.limit or 50,
            offset=args.offset or 0,
            order_by=args.order_by or 'priority',
        )
        if not tasks:
            print("📭 暂无任务")
        else:
            for t in tasks:
                status_icon = {
                    'todo': '⬜',
                    'in_progress': '🔄',
                    'blocked': '🚫',
                    'done': '✅',
                    'cancelled': '❌',
                }
                icon = status_icon.get(t['status'], '❓')
                deadline = f" ⏰ {t['deadline'][:10]}" if t.get('deadline') else ""
                cat = f" [{t['category']}]" if t.get('category') else ""
                did = t.get('display_id') or f"N{t['id']:03d}"
                print(f"{icon} {did} P{t['priority']} {t['title']}{cat}{deadline}")

    elif args.action == 'today':
        tasks = tm.today()
        if not tasks:
            print("📭 今日无待办")
        else:
            print(f"📋 今日待办 ({len(tasks)} 项):")
            for t in tasks:
                print(f"  [{t['priority']}] {t['title']}")

    elif args.action == 'show' and args.id:
        t = tm.get(args.id)
        if t:
            did = t.get('display_id') or f"N{t['id']:03d}"
            print(f"{did} {t['title']}")
            print(f"  状态: {t['status']}  优先级: {t['priority']}  进度: {t['progress']}%")
            if t.get('description'):
                print(f"  描述: {t['description']}")
            if t.get('deadline'):
                print(f"  截止: {t['deadline']}")
            if t.get('category'):
                print(f"  分类: {t['category']}")
        else:
            print(f"❌ 任务 #{args.id} 不存在")

    elif args.action == 'done' and args.id:
        t = tm.get(args.id)
        did = t.get('display_id') or f"N{args.id:03d}" if t else str(args.id)
        tm.set_status(args.id, 'done')
        # 自动记录完成进展
        pt = ProgressTracker(db, tm)
        pt.log(args.id, "标记为完成", new_progress=100)
        print(f"✅ {did} 已标记为完成")

    elif args.action == 'update':
        if not args.id:
            print("❌ 请指定 --id")
            return
        t = tm.get(args.id)
        if not t:
            print(f"❌ 任务 #{args.id} 不存在")
            return
        kwargs = {}
        if args.status:
            kwargs['status'] = args.status
        if args.progress is not None:
            kwargs['progress'] = args.progress
        if args.priority:
            kwargs['priority'] = args.priority
        if args.title:
            kwargs['title'] = args.title
        if args.deadline:
            kwargs['deadline'] = args.deadline
        if args.description:
            kwargs['description'] = args.description
        if args.category:
            kwargs['category'] = args.category
        if args.estimated_hours:
            kwargs['estimated_hours'] = args.estimated_hours
        if not kwargs:
            print("❌ 请至少指定一个要更新的字段")
            return
        tm.update(args.id, **kwargs)
        print(f"✅ 任务 #{args.id} 已更新: {', '.join(kwargs.keys())}")

    elif args.action == 'delete':
        if not args.id:
            print("❌ 请指定 --id")
            return
        t = tm.get(args.id)
        if not t:
            print(f"❌ 任务 #{args.id} 不存在")
            return
        hard = getattr(args, 'hard', False)
        tm.delete(args.id, hard=hard)
        if hard:
            print(f"🗑️ 任务 #{args.id} 已永久删除")
        else:
            print(f"🗑️ 任务 #{args.id} 已软删除 (status → cancelled)")

    elif args.action == 'search':
        keyword = args.title or ''
        if not keyword:
            print("❌ 请提供搜索关键词")
            return
        tasks = tm.search(keyword)
        if not tasks:
            print(f"🔍 未找到匹配 \"{keyword}\" 的任务")
        else:
            print(f"🔍 搜索 \"{keyword}\" 结果 ({len(tasks)} 项):")
            for t in tasks:
                status_icon = {
                    'todo': '⬜',
                    'in_progress': '🔄',
                    'blocked': '🚫',
                    'done': '✅',
                    'cancelled': '❌',
                }
                icon = status_icon.get(t['status'], '❓')
                deadline = f" ⏰ {t['deadline'][:10]}" if t.get('deadline') else ""
                cat = f" [{t['category']}]" if t.get('category') else ""
                print(f"{icon} #{t['id']} P{t['priority']} {t['title']}{cat}{deadline}")

# ======================================================================
# progress 子命令
# ======================================================================

def cmd_progress(args):
    """进展管理"""
    _, tm, pt, _, _, _, _, _ = get_managers()

    if args.action == 'log':
        if not args.id:
            print("❌ 请指定 --id")
            return
        t = tm.get(args.id)
        if not t:
            print(f"❌ 任务 #{args.id} 不存在")
            return
        log_id = pt.log(
            args.id,
            args.content or '',
            hours_spent=args.hours or 0,
            new_progress=args.progress,
        )
        print(f"✅ 进展已记录 (log #{log_id})")

    elif args.action == 'history':
        if not args.id:
            print("❌ 请指定 --id")
            return
        logs = pt.history(args.id, limit=args.limit or 20)
        if not logs:
            print(f"📭 任务 #{args.id} 暂无进展记录")
        else:
            for l in logs:
                when = l['logged_at'][:16] if l.get('logged_at') else ''
                print(f"[{when}] {l['content']} ({l.get('progress_before', 0)}→{l.get('progress_after', 0)}%)")

    elif args.action == 'milestone-add':
        if not args.id:
            print("❌ 请指定 --id (任务 ID)")
            return
        t = tm.get(args.id)
        if not t:
            print(f"❌ 任务 #{args.id} 不存在")
            return
        title = args.content or ''
        if not title:
            print("❌ 请通过 --content 提供里程碑标题")
            return
        mid = pt.add_milestone(args.id, title, due_date=args.due)
        print(f"✅ 里程碑已添加: #{mid} — {title} (任务 #{args.id})")

    elif args.action == 'milestone-done':
        mid = args.mid
        if not mid:
            print("❌ 请指定 --mid (里程碑 ID)")
            return
        try:
            pt.complete_milestone(mid)
            print(f"✅ 里程碑 #{mid} 已标记为完成")
        except Exception as e:
            print(f"❌ 操作失败: {e}")

    elif args.action == 'milestone-list':
        if not args.id:
            print("❌ 请指定 --id (任务 ID)")
            return
        milestones = pt.list_milestones(args.id)
        if not milestones:
            print(f"📭 任务 #{args.id} 暂无里程碑")
        else:
            print(f"🏁 任务 #{args.id} 里程碑:")
            for m in milestones:
                icon = '✅' if m['status'] == 'completed' else '⬜'
                due = f" ⏰ {m['due_date']}" if m.get('due_date') else ""
                print(f"  {icon} #{m['id']} {m['title']}{due}")

    elif args.action == 'timeline':
        logs = pt.timeline(
            start_date=args.from_date,
            end_date=args.to_date,
        )
        if not logs:
            print("📭 该时间范围内暂无进展记录")
        else:
            date_range = ""
            if args.from_date or args.to_date:
                date_range = f" ({args.from_date or '...'} → {args.to_date or '...'})"
            print(f"📊 进展时间线{date_range}:")
            for l in logs:
                when = l['logged_at'][:16] if l.get('logged_at') else ''
                print(f"[{when}] task #{l['task_id']}: {l['content']} ({l.get('progress_before', 0)}→{l.get('progress_after', 0)}%)")

# ======================================================================
# recurring 子命令
# ======================================================================

def cmd_recurring(args):
    """周期任务"""
    _, tm, _, rm, _, _, _, _ = get_managers()

    if args.action == 'add':
        rid = rm.add(
            args.title,
            args.type,
            args.first_date,
            template_desc=args.description or '',
            priority=args.priority or 3,
        )
        print(f"✅ 周期任务已创建: #{rid} — {args.title} ({args.type})")

    elif args.action == 'list':
        items = rm.list(enabled_only=not args.all)
        if not items:
            print("📭 暂无周期任务")
        else:
            for r in items:
                status = '✅' if r['enabled'] else '⏸️'
                print(
                    f"{status} #{r['id']} [{r['recurrence_type']}] {r['template_title']}"
                    f" → 下次: {r.get('next_run_date', '?')}"
                )

    elif args.action == 'generate':
        ids = rm.generate_instances()
        print(f"✅ 已生成 {len(ids)} 个任务实例: {ids}")

    elif args.action == 'toggle':
        rec_id = args.id
        if not rec_id:
            print("❌ 请指定 --id (周期任务 ID)")
            return
        rec = rm.get(rec_id)
        if not rec:
            print(f"❌ 周期任务 #{rec_id} 不存在")
            return
        new_state = not rec['enabled']
        rm.toggle(rec_id, new_state)
        state_label = '启用' if new_state else '暂停'
        print(f"{'✅' if new_state else '⏸️'} 周期任务 #{rec_id} 已{state_label}")

    elif args.action == 'delete':
        rec_id = args.id
        if not rec_id:
            print("❌ 请指定 --id (周期任务 ID)")
            return
        rec = rm.get(rec_id)
        if not rec:
            print(f"❌ 周期任务 #{rec_id} 不存在")
            return
        rm.delete(rec_id)
        print(f"🗑️ 周期任务 #{rec_id} 已删除 (已生成的任务实例不受影响)")

# ======================================================================
# remind 子命令
# ======================================================================

def cmd_remind(args):
    """提醒"""
    _, tm, _, _, engine, _, _, _ = get_managers()

    if args.action == 'trigger':
        tasks = engine.get_tasks_for_reminder(args.type or 'morning')
        msg = engine.format_reminder(tasks, args.type or 'morning')
        print(msg)
        engine.log_reminder([t['id'] for t in tasks], args.type or 'morning')

    elif args.action == 'preview':
        tasks = engine.get_tasks_for_reminder(args.type or 'morning')
        msg = engine.format_reminder(tasks, args.type or 'morning')
        print(msg)
        print(f"\n⚠️ 预览模式 — 未记录提醒日志 ({len(tasks)} 项任务)")

    elif args.action == 'history':
        records = engine.history(days=args.days or 7)
        if not records:
            print("📭 暂无提醒历史")
        else:
            for r in records:
                print(f"[{r['reminder_date']}] {r['reminder_type']}: task #{r['task_id']}")

# ======================================================================
# okr 子命令
# ======================================================================

def cmd_okr(args):
    """OKR 管理"""
    _, tm, _, _, _, okr, _, _ = get_managers()

    if args.action == 'list':
        objectives = okr.list_objectives()
        if not objectives:
            print("📭 暂无 OKR")
        else:
            for o in objectives:
                print(f"🎯 {o['title']} [{o['progress']}%]")
                tree = okr.get_tree()
                for item in tree:
                    if item.get('parent_id') == o['id']:
                        print(f"  📊 {item['title']} [{item['progress']}%]")

    elif args.action == 'add-objective':
        title = args.title
        if not title:
            print("❌ 请通过 --title 提供 Objective 标题")
            return
        oid = okr.add_objective(
            title,
            description=args.desc or '',
            start_date=args.start,
            end_date=args.end,
        )
        print(f"✅ Objective 已创建: #{oid} — {title}")

    elif args.action == 'add-kr':
        parent_id = args.parent
        title = args.title
        if not parent_id:
            print("❌ 请指定 --parent (Objective ID)")
            return
        if not title:
            print("❌ 请通过 --title 提供 Key Result 标题")
            return
        # Check parent exists
        parent = okr.get(parent_id)
        if not parent:
            print(f"❌ Objective #{parent_id} 不存在")
            return
        try:
            kid = okr.add_key_result(parent_id, title, description=args.desc or '')
            print(f"✅ Key Result 已创建: #{kid} — {title} (Objective #{parent_id})")
        except ValueError as e:
            print(f"❌ {e}")

    elif args.action == 'show':
        oid = args.id
        if not oid:
            print("❌ 请指定 --id (OKR ID)")
            return
        item = okr.get(oid)
        if not item:
            print(f"❌ OKR #{oid} 不存在")
            return
        type_icon = {'objective': '🎯', 'key_result': '📊', 'initiative': '🔧'}
        icon = type_icon.get(item['obj_type'], '❓')
        print(f"{icon} #{item['id']} {item['title']}")
        print(f"  类型: {item['obj_type']}  进度: {item['progress']}%  状态: {item['status']}")
        if item.get('description'):
            print(f"  描述: {item['description']}")
        if item.get('start_date'):
            print(f"  开始: {item['start_date']}")
        if item.get('end_date'):
            print(f"  结束: {item['end_date']}")
        # Show linked tasks
        linked = okr.get_linked_tasks(oid)
        if linked:
            print(f"  关联任务 ({len(linked)}):")
            for t in linked:
                status_icon = {'todo': '⬜', 'in_progress': '🔄', 'done': '✅', 'cancelled': '❌'}
                sic = status_icon.get(t.get('status', ''), '❓')
                print(f"    {sic} #{t['id']} {t['title']}")

    elif args.action == 'link':
        okr_id = args.okr
        task_id = args.task
        if not okr_id or not task_id:
            print("❌ 请同时指定 --okr (OKR ID) 和 --task (任务 ID)")
            return
        # Validate both exist
        okr_item = okr.get(okr_id)
        if not okr_item:
            print(f"❌ OKR #{okr_id} 不存在")
            return
        task = tm.get(task_id)
        if not task:
            print(f"❌ 任务 #{task_id} 不存在")
            return
        okr.link_task(okr_id, task_id)
        print(f"🔗 任务 #{task_id} 已关联到 OKR #{okr_id} ({okr_item['title']})")

    elif args.action == 'tree':
        tree = okr.get_tree()
        if not tree:
            print("📭 暂无 OKR 数据")
        else:
            print("🌳 OKR 全景树:")
            for obj in tree:
                print(f"🎯 {obj['title']} [{obj['progress']}%] ({obj['status']})")
                for kr in obj.get('key_results', []):
                    print(f"  📊 {kr['title']} [{kr['progress']}%] ({kr['status']})")
                    for ini in kr.get('initiatives', []):
                        print(f"    🔧 {ini['title']} [{ini['progress']}%] ({ini['status']})")

    elif args.action == 'sync':
        if args.doc_token:
            # 这里需要 feishu_doc_read，暂时标记
            print("⚠️ OKR 同步需要飞书文档 token，请通过 Hermes Agent 对话触发")
        else:
            print("❌ 请指定 --doc-token (飞书文档 token)")

    elif args.action == 'sync-bitable':
        from .okr_sync_bitable import build_sync_request, BITABLE_CONFIG
        import json as _json
        if not args.period:
            print("❌ 请指定 --period (如 2026H1)")
            return
        app_token = getattr(args, 'app_token', None) or BITABLE_CONFIG['app_token']
        table_id = getattr(args, 'table_id', None) or BITABLE_CONFIG['table_id']
        dry_run = getattr(args, 'dry_run', False)
        label = "[DRY RUN] " if dry_run else ""
        request = build_sync_request(args.period, app_token=app_token, table_id=table_id)
        print(f"📊 {label}位表同步: period={args.period}")
        print(f"   App: {app_token}")
        print(f"   Table: {table_id}")
        print(f"   Request JSON:\n{_json.dumps(request, ensure_ascii=False, indent=2)}")
        if dry_run:
            print(f"   模式: 仅预览，不写入数据库")
        print(f"💡 可通过 Agent 对话调用 feishu_bitable_app_table_record 工具获取数据后执行同步")

# ======================================================================
# report 子命令
# ======================================================================

def cmd_report(args):
    """报告"""
    _, _, _, _, _, _, report, _ = get_managers()

    if args.action == 'monthly':
        path = report.monthly(
            year=args.year,
            month=args.month,
            output_path=args.output,
        )
        print(f"📄 月报已生成: {path}")

    elif args.action == 'semiannual':
        path = report.semiannual(
            year=args.year,
            half=args.half,
            output_path=args.output,
        )
        print(f"📄 半年报已生成: {path}")

# ======================================================================
# advice 子命令
# ======================================================================

def cmd_advice(args):
    """智能建议"""
    _, _, _, _, _, _, _, advisor = get_managers()
    ctx = advisor.get_context_for_llm()
    print(ctx)

# ======================================================================
# db 子命令
# ======================================================================

def cmd_db(args):
    """数据库维护"""
    db, tm, _, _, _, _, _, _ = get_managers()

    if args.action == 'stats':
        db_stats = db.stats()
        tm_stats = tm.stats()
        print("📊 数据库统计:")
        print(f"  路径: {db_stats['db_path']}")
        print(f"  大小: {db_stats['db_size_bytes']:,} bytes")
        print(f"  表行数:")
        for table, cnt in db_stats['tables'].items():
            print(f"    {table}: {cnt}")
        print(f"  任务分布:")
        if tm_stats.get('by_status'):
            print(f"    按状态: {tm_stats['by_status']}")
        if tm_stats.get('by_priority'):
            print(f"    按优先级: {tm_stats['by_priority']}")
        if tm_stats.get('by_category'):
            print(f"    按分类: {tm_stats['by_category']}")

    elif args.action == 'export':
        path = args.path
        if not path:
            print("❌ 请指定导出路径")
            return
        db.export(path)
        print(f"📤 数据已导出到: {path}")

    elif args.action == 'import':
        path = args.path
        if not path:
            print("❌ 请指定导入文件路径")
            return
        try:
            db.import_(path)
            print(f"📥 数据已从 {path} 导入 (旧数据已替换)")
        except FileNotFoundError:
            print(f"❌ 文件不存在: {path}")
        except Exception as e:
            print(f"❌ 导入失败: {e}")

    elif args.action == 'cleanup':
        db.cleanup()
        print("🧹 数据库清理完成 (已移除 30 天前的提醒日志 + VACUUM)")

# ======================================================================
# main
# ======================================================================

def main():
    parser = argparse.ArgumentParser(
        prog='personal-assistant',
        description='Personal Assistant Skill — 个人工作任务管理',
    )
    sub = parser.add_subparsers(dest='command')

    # ------------------------------------------------------------------
    # task 子命令
    # ------------------------------------------------------------------
    task_p = sub.add_parser('task', help='任务管理')
    task_p.add_argument('action', choices=[
        'add', 'list', 'today', 'show', 'done',
        'update', 'delete', 'search',
    ])
    task_p.add_argument('title', nargs='?')
    task_p.add_argument('--id', type=int, help='任务 ID')
    task_p.add_argument('--priority', type=int, choices=range(1, 6), help='优先级 1-5')
    task_p.add_argument('--deadline', help='截止日期 (YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS)')
    task_p.add_argument('--category', help='分类标签')
    task_p.add_argument('--estimated-hours', type=float, help='预估工时（小时）')
    task_p.add_argument('--description', help='任务描述')
    task_p.add_argument('--status', help='按状态过滤')
    task_p.add_argument('--progress', type=int, help='进度百分比 0-100')
    task_p.add_argument('--priority-min', type=int, help='最低优先级')
    task_p.add_argument('--priority-max', type=int, help='最高优先级')
    task_p.add_argument('--search', help='搜索关键词（标题+描述）')
    task_p.add_argument('--limit', type=int, help='返回条数上限')
    task_p.add_argument('--offset', type=int, help='分页偏移')
    task_p.add_argument('--order-by', help='排序字段 (priority/deadline/created_at/updated_at)')
    task_p.add_argument('--hard', action='store_true', help='硬删除（物理删除）')

    # ------------------------------------------------------------------
    # progress 子命令
    # ------------------------------------------------------------------
    prog_p = sub.add_parser('progress', help='进展管理')
    prog_p.add_argument('action', choices=[
        'log', 'history',
        'milestone-add', 'milestone-done', 'milestone-list',
        'timeline',
    ])
    prog_p.add_argument('--id', type=int, help='任务 ID')
    prog_p.add_argument('--mid', type=int, help='里程碑 ID')
    prog_p.add_argument('--content', help='进展内容 / 里程碑标题')
    prog_p.add_argument('--hours', type=float, help='花费小时数')
    prog_p.add_argument('--progress', type=int, help='新进度 0-100')
    prog_p.add_argument('--due', help='里程碑截止日期 (YYYY-MM-DD)')
    prog_p.add_argument('--from-date', dest='from_date', help='时间线起始日期 (YYYY-MM-DD)')
    prog_p.add_argument('--to-date', dest='to_date', help='时间线结束日期 (YYYY-MM-DD)')
    prog_p.add_argument('--limit', type=int, help='历史记录条数上限')

    # ------------------------------------------------------------------
    # recurring 子命令
    # ------------------------------------------------------------------
    rec_p = sub.add_parser('recurring', help='周期任务')
    rec_p.add_argument('action', choices=['add', 'list', 'generate', 'toggle', 'delete'])
    rec_p.add_argument('title', nargs='?')
    rec_p.add_argument('--id', type=int, help='周期任务 ID')
    rec_p.add_argument('--type', choices=['daily', 'weekly', 'biweekly', 'monthly', 'custom'],
                       help='周期类型')
    rec_p.add_argument('--first-date', help='首次执行日期 (YYYY-MM-DD)')
    rec_p.add_argument('--description', help='模板描述')
    rec_p.add_argument('--priority', type=int, help='优先级 1-5')
    rec_p.add_argument('--all', action='store_true', help='列出所有（包括禁用的）')

    # ------------------------------------------------------------------
    # remind 子命令
    # ------------------------------------------------------------------
    rem_p = sub.add_parser('remind', help='提醒')
    rem_p.add_argument('action', choices=['trigger', 'preview', 'history'])
    rem_p.add_argument('--type', choices=[
        'morning', 'afternoon', 'evening', 'deadline_alert', 'manual',
    ], help='提醒类型')
    rem_p.add_argument('--days', type=int, help='查询最近 N 天历史')

    # ------------------------------------------------------------------
    # okr 子命令
    # ------------------------------------------------------------------
    okr_p = sub.add_parser('okr', help='OKR 管理')
    okr_p.add_argument('action', choices=[
        'list', 'add-objective', 'add-kr', 'show', 'link', 'tree', 'sync',
        'sync-bitable',
    ])
    okr_p.add_argument('--id', type=int, help='OKR ID')
    okr_p.add_argument('--title', help='OKR 标题')
    okr_p.add_argument('--parent', type=int, help='父级 Objective ID (用于 add-kr)')
    okr_p.add_argument('--desc', help='描述')
    okr_p.add_argument('--start', help='开始日期 (YYYY-MM-DD)')
    okr_p.add_argument('--end', help='结束日期 (YYYY-MM-DD)')
    okr_p.add_argument('--okr', type=int, help='OKR ID (用于 link)')
    okr_p.add_argument('--task', type=int, help='任务 ID (用于 link)')
    okr_p.add_argument('--doc-token', help='飞书文档 token')
    okr_p.add_argument('--period', help='周期标识 (如 2026H1)')
    okr_p.add_argument('--app-token', help='飞书多维表格 app_token (默认使用 BITABLE_CONFIG)')
    okr_p.add_argument('--table-id', help='OKR目标表 table_id (默认使用 BITABLE_CONFIG)')
    okr_p.add_argument('--dry-run', action='store_true', help='仅预览不写入')

    # ------------------------------------------------------------------
    # report 子命令
    # ------------------------------------------------------------------
    rep_p = sub.add_parser('report', help='报告')
    rep_p.add_argument('action', choices=['monthly', 'semiannual'])
    rep_p.add_argument('--year', type=int, help='年份')
    rep_p.add_argument('--month', type=int, help='月份 1-12')
    rep_p.add_argument('--half', type=int, choices=[1, 2], help='半年度: 1=上半年, 2=下半年')
    rep_p.add_argument('--output', help='输出路径')

    # ------------------------------------------------------------------
    # advice 子命令
    # ------------------------------------------------------------------
    sub.add_parser('advice', help='智能建议 (输出 LLM 上下文)')

    # ------------------------------------------------------------------
    # db 子命令
    # ------------------------------------------------------------------
    db_p = sub.add_parser('db', help='数据库维护')
    db_p.add_argument('action', choices=['stats', 'export', 'import', 'cleanup'])
    db_p.add_argument('path', nargs='?', help='导出/导入文件路径')

    # ------------------------------------------------------------------
    # 路由
    # ------------------------------------------------------------------
    args = parser.parse_args()

    if args.command == 'task':
        cmd_task(args)
    elif args.command == 'progress':
        cmd_progress(args)
    elif args.command == 'recurring':
        cmd_recurring(args)
    elif args.command == 'remind':
        cmd_remind(args)
    elif args.command == 'okr':
        cmd_okr(args)
    elif args.command == 'report':
        cmd_report(args)
    elif args.command == 'advice':
        cmd_advice(args)
    elif args.command == 'db':
        cmd_db(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

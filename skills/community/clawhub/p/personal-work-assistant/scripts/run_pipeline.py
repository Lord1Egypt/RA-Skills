import os
import sys
import yaml
import json
import datetime
import subprocess

# 引入核心组件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.append(SKILL_ROOT)

from core.storage.task_ledger import TaskLedger
from core.collectors.tb_collector import TeambitionCollector
from core.collectors.dingtalk_collector import DingTalkCollector
from core.analyzer.task_analyzer import TaskAnalyzer
from core.reporter.report_generator import ReportGenerator

def load_config():
    config_path = os.path.join(SKILL_ROOT, 'config.yaml')
    if not os.path.exists(config_path):
        config_path = os.path.join(SKILL_ROOT, 'config.template.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_pipeline(dry_run=False):
    config = load_config()
    db_path = os.path.join(SKILL_ROOT, 'data', 'task_ledger.db')
    ledger = TaskLedger(db_path)
    
    now = datetime.datetime.now()
    hours = config.get('reporting', {}).get('time_window_hours', 24)
    yesterday = now - datetime.timedelta(hours=hours)
    start_time_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')

    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 开始执行个人工作助理流水线...")

    # 1. 采集 Teambition 任务并同步到账本
    tb_collector = TeambitionCollector(config)
    tb_tasks = tb_collector.fetch_my_tasks()
    print(f"📦 获取到 TB 执行中任务: {len(tb_tasks)} 条")
    
    current_tb_ids = set()
    for t in tb_tasks:
        tid = f"tb:{t['taskId']}"
        current_tb_ids.add(tid)
        ledger.upsert_task(
            task_id=tid,
            source_type='teambition',
            source_name='Teambition',
            title=t.get('content', ''),
            detail=t.get('note', '')[:200] if t.get('note') else '',
            status='in_progress',
            priority='high' if t.get('priority', 0) > 0 else 'normal',
            due_date=t.get('dueDate'),
            raw_data=t
        )

    # 2. 采集 钉钉 消息（重点群 + @我 + 私聊）
    dt_collector = DingTalkCollector(config)
    focused_msgs = dt_collector.fetch_focused_groups_messages(start_time_str)
    at_mes = dt_collector.fetch_at_me_messages(start_time_str)
    dms = dt_collector.fetch_direct_messages(start_time_str)
    print(f"💬 钉钉重点群消息: {len(focused_msgs)} 条, @我: {len(at_mes)} 条, 私聊: {len(dms)} 条")

    # 3. AI 结构化分析提炼
    analyzer = TaskAnalyzer(config)
    analysis_res = analyzer.analyze_dingtalk_events(focused_msgs, at_mes, dms)
    
    action_items = analysis_res.get('action_items', [])
    announcements = analysis_res.get('announcements', [])
    progress_updates = analysis_res.get('progress_updates', [])
    print(f"🧠 AI提炼出行动项: {len(action_items)} 条, 公告: {len(announcements)} 条, 进展更新: {len(progress_updates)} 条")

    # 写入新行动项
    for item in action_items:
        task_id = f"dt:{item.get('id', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))}"
        ledger.upsert_task(
            task_id=task_id,
            source_type='dingtalk',
            source_name=item.get('source_name', '钉钉群聊'),
            title=item.get('title', ''),
            detail=f"{item.get('detail', '')}\n[原因: {item.get('reason', '')}]",
            status='pending',
            priority=item.get('priority', 'normal'),
            due_date=item.get('due_date')
        )

    # 写入需知悉公告
    for ann in announcements:
        ann_id = f"ann:{ann.get('id', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))}"
        ledger.add_announcement(ann_id, ann.get('source_name', '全员通知'), ann.get('content', ''))

    # 更新进展与闭环
    for prog in progress_updates:
        topic = prog.get('related_topic_or_id', '')
        status = prog.get('status')
        note = prog.get('resolution_note')
        # 简单匹配已有任务
        active = ledger.get_active_tasks()
        for act in active:
            if topic and (topic in act['title'] or topic in act['detail']):
                ledger.update_task_progress(act['id'], status=status, resolution_note=note)

    # 4. 生成日报
    reporter = ReportGenerator(config)
    active_tasks = ledger.get_active_tasks()
    closed_tasks = ledger.get_recently_closed_tasks(hours=hours)
    unreported_ann = ledger.get_unreported_announcements()

    report_md = reporter.generate_markdown_report(active_tasks, closed_tasks, unreported_ann)
    print("\n" + "="*50)
    print(report_md)
    print("="*50 + "\n")

    # 5. 推送通知 (钉钉单聊)
    if not dry_run:
        target_user = config.get('reporting', {}).get('target_user_id')
        channel = config.get('reporting', {}).get('delivery_channel', 'dingtalk-connector')
        if target_user:
            cmd = [
                'openclaw', 'message', 'send',
                '--channel', channel,
                '--target', target_user,
                '--message', report_md
            ]
            subprocess.run(cmd)
            print(f"✅ 日报已推送至钉钉目标: {target_user}")

        # 标记公告为已播报
        ann_ids = [a['id'] for a in unreported_ann]
        ledger.mark_announcements_reported(ann_ids)

if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    run_pipeline(dry_run=dry_run)

#!/usr/bin/env python3
"""
高价值猎头式任务管理 - 核心任务管理脚本
支持：挖坑 (新增任务)、填坑 (更新进度)、查询、完成、暂停任务
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 任务数据存储路径
TASK_DATA_DIR = Path(os.environ.get('HOME', '~')) / '.openclaw' / 'workspace' / 'memory' / 'tasks'
TASK_FILE = TASK_DATA_DIR / 'tasks.json'
ARCHIVE_FILE = TASK_DATA_DIR / 'tasks_archive.json'

def ensure_data_dir():
    """确保数据目录存在"""
    TASK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TASK_FILE.exists():
        with open(TASK_FILE, 'w', encoding='utf-8') as f:
            json.dump({'tasks': [], 'next_id': 1}, f, ensure_ascii=False, indent=2)

def load_tasks():
    """加载任务数据"""
    ensure_data_dir()
    with open(TASK_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(data):
    """保存任务数据"""
    ensure_data_dir()
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calculate_urgency(deadline_str):
    """计算紧迫度 (0-1，越接近截止日期越高)"""
    if not deadline_str:
        return 0.5
    try:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        days_left = (deadline - datetime.now()).days
        if days_left <= 0:
            return 1.0
        elif days_left <= 7:
            return 0.9
        elif days_left <= 30:
            return 0.7
        elif days_left <= 90:
            return 0.5
        else:
            return 0.3
    except:
        return 0.5

def calculate_utility_score(value, success_prob, time_cost, energy_cost):
    """
    计算任务效用得分
    效用得分 = (预期价值 × 成功概率) / (时间投入 × 精力消耗系数)
    """
    time_factor = max(time_cost, 1)
    energy_factor = max(energy_cost, 1) / 5
    return (value * success_prob / 100) / (time_factor * energy_factor)

def add_task(name, deadline=None, total_hours=10, value=5, energy=3, 
             success_prob=75, tags=None, goal=None, description=None):
    """挖坑：新增任务"""
    data = load_tasks()
    task_id = data['next_id']
    data['next_id'] += 1
    
    urgency = calculate_urgency(deadline)
    utility_score = calculate_utility_score(value, success_prob, total_hours, energy)
    
    task = {
        'id': task_id,
        'name': name,
        'description': description or '',
        'status': 'active',
        'deadline': deadline,
        'total_hours': total_hours,
        'hours_spent': 0,
        'progress': 0,
        'value': value,
        'energy': energy,
        'success_prob': success_prob,
        'tags': tags or [],
        'goal': goal or '',
        'urgency': urgency,
        'utility_score': utility_score,
        'priority': utility_score * urgency,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'progress_log': []
    }
    
    data['tasks'].append(task)
    save_tasks(data)
    
    return task

def update_progress(task_id, progress_increment=None, new_progress=None, hours_spent=0, note=''):
    """填坑：更新任务进度"""
    data = load_tasks()
    task = None
    for t in data['tasks']:
        if t['id'] == task_id:
            task = t
            break
    
    if not task:
        return {'error': f'任务 ID {task_id} 不存在'}
    
    if task['status'] != 'active':
        return {'error': f'任务 ID {task_id} 状态为 {task["status"]}，无法更新进度'}
    
    if new_progress is not None:
        task['progress'] = min(100, max(0, new_progress))
    elif progress_increment is not None:
        task['progress'] = min(100, max(0, task['progress'] + progress_increment))
    
    task['hours_spent'] += hours_spent
    
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'progress': task['progress'],
        'hours_spent': task['hours_spent'],
        'note': note
    }
    task['progress_log'].append(log_entry)
    
    if task['progress'] >= 100:
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    urgency = calculate_urgency(task['deadline'])
    task['urgency'] = urgency
    task['priority'] = task['utility_score'] * urgency
    
    save_tasks(data)
    
    return task

def list_tasks(status='active', sort_by='priority'):
    """查询任务列表"""
    data = load_tasks()
    tasks = [t for t in data['tasks'] if t['status'] == status] if status != 'all' else data['tasks']
    
    if sort_by == 'priority':
        tasks.sort(key=lambda x: x['priority'], reverse=True)
    elif sort_by == 'deadline':
        tasks.sort(key=lambda x: x['deadline'] or '9999-99-99')
    elif sort_by == 'created':
        tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    return tasks

def get_task(task_id):
    """获取单个任务详情"""
    data = load_tasks()
    for t in data['tasks']:
        if t['id'] == task_id:
            return t
    return None

def pause_task(task_id):
    """暂停任务"""
    data = load_tasks()
    for t in data['tasks']:
        if t['id'] == task_id:
            t['status'] = 'paused'
            t['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_tasks(data)
            return t
    return None

def resume_task(task_id):
    """恢复任务"""
    data = load_tasks()
    for t in data['tasks']:
        if t['id'] == task_id:
            t['status'] = 'active'
            t['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_tasks(data)
            return t
    return None

def complete_task(task_id):
    """完成任务"""
    data = load_tasks()
    for t in data['tasks']:
        if t['id'] == task_id:
            t['status'] = 'completed'
            t['progress'] = 100
            t['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            t['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_tasks(data)
            return t
    return None

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python task_manager.py <command> [args...]")
        print("命令：add, update, list, get, pause, resume, complete")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'add':
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        task = add_task(**params)
        print(json.dumps(task, ensure_ascii=False, indent=2))
    
    elif command == 'update':
        task_id = int(sys.argv[2])
        params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        result = update_progress(task_id, **params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else 'active'
        sort_by = sys.argv[3] if len(sys.argv) > 3 else 'priority'
        tasks = list_tasks(status, sort_by)
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
    
    elif command == 'get':
        task_id = int(sys.argv[2])
        task = get_task(task_id)
        print(json.dumps(task, ensure_ascii=False, indent=2) if task else '{"error": "Task not found"}')
    
    elif command == 'pause':
        task_id = int(sys.argv[2])
        task = pause_task(task_id)
        print(json.dumps(task, ensure_ascii=False, indent=2) if task else '{"error": "Task not found"}')
    
    elif command == 'resume':
        task_id = int(sys.argv[2])
        task = resume_task(task_id)
        print(json.dumps(task, ensure_ascii=False, indent=2) if task else '{"error": "Task not found"}')
    
    elif command == 'complete':
        task_id = int(sys.argv[2])
        task = complete_task(task_id)
        print(json.dumps(task, ensure_ascii=False, indent=2) if task else '{"error": "Task not found"}')
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入/导出功能 - 支持 .ics 格式
"""

import sqlite3
from datetime import datetime
from pathlib import Path

class CalendarIO:
    """日历导入导出"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "scheduler.db"
        self.db_path = db_path
    
    def export_to_ics(self, output_path=None):
        """
        导出日程为 .ics 文件
        
        Args:
            output_path: 输出文件路径，默认为 data/backups/scheduler_YYYYMMDD.ics
        """
        if output_path is None:
            backup_dir = Path(__file__).parent.parent / "data" / "backups"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d')
            output_path = backup_dir / f"scheduler_{timestamp}.ics"
        else:
            output_path = Path(output_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, start_time, end_time, location, description, is_all_day
            FROM events ORDER BY start_time
        ''')
        events = cursor.fetchall()
        conn.close()
        
        # 生成 ICS 内容
        ics_lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//Personal Scheduler//CN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH',
        ]
        
        for event in events:
            event_id, title, start_time, end_time, location, description, is_all_day = event
            
            ics_lines.append('BEGIN:VEVENT')
            ics_lines.append(f'UID:{event_id}@personal-scheduler')
            ics_lines.append(f'SUMMARY:{title}')
            
            # 时间格式
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            
            if is_all_day:
                ics_lines.append(f'DTSTART;VALUE=DATE:{start_dt.strftime("%Y%m%d")}')
                ics_lines.append(f'DTEND;VALUE=DATE:{end_dt.strftime("%Y%m%d")}')
            else:
                ics_lines.append(f'DTSTART:{start_dt.strftime("%Y%m%dT%H%M%S")}')
                ics_lines.append(f'DTEND:{end_dt.strftime("%Y%m%dT%H%M%S")}')
            
            if location:
                ics_lines.append(f'LOCATION:{location}')
            if description:
                ics_lines.append(f'DESCRIPTION:{description}')
            
            ics_lines.append('END:VEVENT')
        
        ics_lines.append('END:VCALENDAR')
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\r\n'.join(ics_lines))
        
        return output_path
    
    def import_from_ics(self, ics_path):
        """
        从 .ics 文件导入日程
        
        Returns:
            int: 导入的日程数量
        """
        ics_path = Path(ics_path)
        if not ics_path.exists():
            raise FileNotFoundError(f"文件不存在: {ics_path}")
        
        with open(ics_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 VEVENT
        events = []
        in_event = False
        current_event = {}
        
        for line in content.split('\n'):
            line = line.strip()
            
            if line == 'BEGIN:VEVENT':
                in_event = True
                current_event = {}
            elif line == 'END:VEVENT':
                in_event = False
                if current_event:
                    events.append(current_event)
            elif in_event:
                if ':' in line:
                    key, value = line.split(':', 1)
                    # 处理带参数的 key，如 DTSTART;VALUE=DATE
                    key = key.split(';')[0]
                    current_event[key] = value
        
        # 导入到数据库
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported = 0
        for event in events:
            try:
                title = event.get('SUMMARY', 'Imported Event')
                
                # 解析时间
                if 'DTSTART;VALUE=DATE' in event:
                    # 全天事件
                    start_str = event['DTSTART;VALUE=DATE']
                    start_time = datetime.strptime(start_str, '%Y%m%d')
                    is_all_day = True
                    
                    if 'DTEND;VALUE=DATE' in event:
                        end_str = event['DTEND;VALUE=DATE']
                        end_time = datetime.strptime(end_str, '%Y%m%d')
                    else:
                        end_time = start_time
                else:
                    # 普通事件
                    start_str = event.get('DTSTART', '')
                    end_str = event.get('DTEND', '')
                    
                    if len(start_str) == 15:  # YYYYMMDDTHHMMSS
                        start_time = datetime.strptime(start_str, '%Y%m%dT%H%M%S')
                    else:
                        continue
                    
                    if len(end_str) == 15:
                        end_time = datetime.strptime(end_str, '%Y%m%dT%H%M%S')
                    else:
                        end_time = start_time + __import__('datetime').timedelta(hours=1)
                    
                    is_all_day = False
                
                location = event.get('LOCATION')
                description = event.get('DESCRIPTION')
                
                # 生成新 ID
                import uuid
                event_id = str(uuid.uuid4())[:8]
                
                cursor.execute('''
                    INSERT INTO events (id, title, start_time, end_time, location, description, is_all_day)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (event_id, title, start_time, end_time, location, description, is_all_day))
                
                imported += 1
            except Exception as e:
                print(f"导入事件失败: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return imported

if __name__ == "__main__":
    import sys
    
    io = CalendarIO()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python calendar_io.py export [output.ics]")
        print("  python calendar_io.py import input.ics")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "export":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        path = io.export_to_ics(output)
        print(f"已导出到: {path}")
    
    elif action == "import":
        if len(sys.argv) < 3:
            print("请指定 .ics 文件路径")
            sys.exit(1)
        
        path = sys.argv[2]
        count = io.import_from_ics(path)
        print(f"已导入 {count} 个日程")
    
    else:
        print(f"未知操作: {action}")

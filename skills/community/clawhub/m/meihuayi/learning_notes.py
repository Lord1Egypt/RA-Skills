#!/usr/bin/env python3
"""
梅花易数AI学习笔记
功能：记录每次卦例的反馈分析，持续提升AI算卦能力
"""
import sqlite3, json, datetime, os
from typing import Dict, List, Optional

# ══════════════════════════════════════════════
# 配置
# ══════════════════════════════════════════════
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
_DB_PATH  = os.path.join(_DATA_DIR, 'learning_notes.db')

# ══════════════════════════════════════════════
# 数据库初始化
# ══════════════════════════════════════════════
def _get_db():
    if not os.path.exists(_DATA_DIR):
        os.makedirs(_DATA_DIR)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    """初始化学习笔记表"""
    conn = _get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            question_type TEXT,
            correct INTEGER NOT NULL,
            reason_analysis TEXT,
            lesson_learned TEXT,
            improvement TEXT
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_record_id ON notes(record_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_correct ON notes(correct)')
    conn.commit()
    conn.close()

_init_db()

# ══════════════════════════════════════════════
# 笔记管理
# ══════════════════════════════════════════════

def add_note(record_id: int, correct: bool, reason_analysis: str = "", 
             lesson_learned: str = "", improvement: str = "", 
             question_type: str = ""):
    """添加学习笔记"""
    conn = _get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO notes (record_id, date, question_type, correct, 
                          reason_analysis, lesson_learned, improvement)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (record_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          question_type, 1 if correct else 0, reason_analysis, 
          lesson_learned, improvement))
    conn.commit()
    conn.close()
    return True

def get_all_notes() -> List[Dict]:
    """获取所有笔记"""
    conn = _get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM notes ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_incorrect_notes() -> List[Dict]:
    """获取所有判断错误的笔记"""
    conn = _get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM notes WHERE correct = 0 ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_statistics() -> Dict:
    """获取统计信息"""
    conn = _get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as total FROM notes')
    total = c.fetchone()['total']
    c.execute('SELECT COUNT(*) as correct FROM notes WHERE correct = 1')
    correct = c.fetchone()['correct']
    conn.close()
    return {
        'total': total,
        'correct': correct,
        'incorrect': total - correct,
        'accuracy': round(correct / total * 100, 1) if total > 0 else 0
    }

def format_notes_for_display(notes: List[Dict], brief: bool = True) -> str:
    """格式化笔记用于显示"""
    if not notes:
        return "暂无学习笔记。"
    
    lines = []
    
    if brief:
        lines.append(f"共 {len(notes)} 条笔记：\n")
        lines.append("─" * 60)
        lines.append(f"{'ID':<4} {'日期':<12} {'类型':<8} {'结果':<6} {'教训'}")
        lines.append("─" * 60)
        for n in notes:
            date = n['date'][:10]
            qtype = n['question_type'] or '-'
            result = "✅" if n['correct'] else "❌"
            lesson = n['lesson_learned'] or ''
            if len(lesson) > 20:
                lesson = lesson[:20] + "..."
            lines.append(f"#{n['id']:<3} {date:<12} {qtype:<8} {result:<6} {lesson}")
    else:
        for n in notes:
            lines.append("═" * 50)
            lines.append(f"【笔记 #{n['id']}】 卦例 #{n['record_id']}")
            lines.append("═" * 50)
            lines.append(f"日期：{n['date']}")
            lines.append(f"问题类型：{n['question_type'] or '-'}")
            lines.append(f"判断结果：{'✅ 正确' if n['correct'] else '❌ 错误'}")
            lines.append("")
            lines.append("【原因分析】")
            lines.append(n['reason_analysis'] or '-')
            lines.append("")
            lines.append("【教训】")
            lines.append(n['lesson_learned'] or '-')
            lines.append("")
            lines.append("【改进方向】")
            lines.append(n['improvement'] or '-')
    
    return "\n".join(lines)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：")
        print("  python learning_notes.py list              # 列出所有笔记")
        print("  python learning_notes.py stats             # 统计信息")
        print("  python learning_notes.py incorrect         # 列出错误案例")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        notes = get_all_notes()
        print(format_notes_for_display(notes, brief=True))
    
    elif cmd == 'stats':
        stats = get_statistics()
        print("📊 学习统计\n")
        print(f"总卦例数：{stats['total']}")
        print(f"正确数：{stats['correct']}")
        print(f"错误数：{stats['incorrect']}")
        print(f"准确率：{stats['accuracy']}%")
    
    elif cmd == 'incorrect':
        notes = get_incorrect_notes()
        print(format_notes_for_display(notes, brief=False))

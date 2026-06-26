#!/usr/bin/env python3
"""
梅花易数卦例记录管理（SQLite版）
功能：保存、查询、更新卦例记录
"""
import sqlite3, json, datetime, os
from typing import Dict, List, Optional

# ══════════════════════════════════════════════
# 配置
# ══════════════════════════════════════════════
_DATA_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
_DB_PATH   = os.path.join(_DATA_DIR, 'divination_records.db')
_JSON_PATH = os.path.join(_DATA_DIR, 'divination_records.json')

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
    """初始化数据库表"""
    conn = _get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            question TEXT NOT NULL,
            method TEXT NOT NULL,
            params TEXT NOT NULL,
            pattern TEXT NOT NULL,
            analysis TEXT NOT NULL,
            conclusion TEXT NOT NULL,
            feedback TEXT,
            summary TEXT
        )
    ''')
    # 创建索引加速查询
    c.execute('CREATE INDEX IF NOT EXISTS idx_question ON records(question)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_date ON records(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_method ON records(method)')
    conn.commit()
    conn.close()

def _dict_to_row(d: Dict) -> Dict:
    """将字典中的JSON字段转为字符串"""
    result = dict(d)
    for key in ['pattern', 'feedback', 'summary']:
        if result.get(key) and isinstance(result[key], dict):
            result[key] = json.dumps(result[key], ensure_ascii=False)
    return result

def _row_to_dict(row: sqlite3.Row) -> Dict:
    """将数据库行转为字典，JSON字段解析"""
    d = dict(row)
    for key in ['pattern', 'feedback', 'summary']:
        if d.get(key):
            try:
                d[key] = json.loads(d[key])
            except:
                pass
    return d

# ══════════════════════════════════════════════
# 迁移旧JSON数据
# ══════════════════════════════════════════════
def _migrate_json():
    """如果存在旧JSON文件，迁移到SQLite"""
    if os.path.exists(_JSON_PATH):
        try:
            with open(_JSON_PATH, 'r', encoding='utf-8') as f:
                records = json.load(f)
            
            if records:
                conn = _get_db()
                c = conn.cursor()
                for r in records:
                    d = _dict_to_row(r)
                    c.execute('''
                        INSERT INTO records (date, question, method, params, pattern, analysis, conclusion, feedback, summary)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (d['date'], d['question'], d['method'], d['params'], d['pattern'], d['analysis'], d['conclusion'], d.get('feedback'), d.get('summary')))
                conn.commit()
                conn.close()
                
                # 备份旧JSON
                os.rename(_JSON_PATH, _JSON_PATH + '.bak')
                print(f'已迁移 {len(records)} 条JSON记录到SQLite')
        except Exception as e:
            print(f'迁移失败: {e}')

# ══════════════════════════════════════════════
# 核心功能
# ══════════════════════════════════════════════

def save_record(
    question: str,
    method: str,
    params: str,
    pattern: Dict,
    analysis: str,
    conclusion: str
) -> int:
    """
    保存卦例记录
    返回：新记录的ID
    """
    _init_db()
    _migrate_json()
    
    conn = _get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO records (date, question, method, params, pattern, analysis, conclusion, feedback, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL)
    ''', (
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        question,
        method,
        params,
        json.dumps(pattern, ensure_ascii=False),
        analysis,
        conclusion
    ))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return new_id


def query_records(
    keyword: str = None,
    start_date: str = None,
    end_date: str = None,
    method: str = None,
    pending_only: bool = False
) -> List[Dict]:
    """
    查询卦例记录
    
    参数：
        keyword: 问题关键词
        start_date: 开始日期（如 "2026-03-01"）
        end_date: 结束日期（如 "2026-03-31"）
        method: 起卦方式（数字/时间）
        pending_only: 只返回未反馈的记录
    
    返回：匹配的记录列表
    """
    _init_db()
    
    conn = _get_db()
    c = conn.cursor()
    
    sql = 'SELECT * FROM records WHERE 1=1'
    params = []
    
    if keyword:
        sql += ' AND question LIKE ?'
        params.append(f'%{keyword}%')
    
    if start_date:
        sql += ' AND date >= ?'
        params.append(start_date)
    
    if end_date:
        sql += ' AND date <= ?'
        params.append(end_date + ' 23:59:59')
    
    if method:
        sql += ' AND method = ?'
        params.append(method)
    
    if pending_only:
        sql += ' AND feedback IS NULL'
    
    sql += ' ORDER BY date DESC'
    
    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def add_feedback(
    record_id: int,
    result: str,
    correct: bool,
    correct_reason: str = None,
    incorrect_reason: str = None,
    xiang_analysis: str = None
) -> bool:
    """
    添加卦例反馈
    
    参数：
        record_id: 记录ID
        result: 实际结果描述
        correct: 推断是否正确
        correct_reason: 正确的原因
        incorrect_reason: 不正确的原因
        xiang_analysis: 取象分析
    
    返回：是否成功
    """
    _init_db()
    
    feedback = {
        'result': result,
        'correct': correct,
        'correct_reason': correct_reason,
        'incorrect_reason': incorrect_reason,
        'xiang_analysis': xiang_analysis,
        'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    conn = _get_db()
    c = conn.cursor()
    c.execute('UPDATE records SET feedback = ? WHERE id = ?', (json.dumps(feedback, ensure_ascii=False), record_id))
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def add_summary(record_id: int, summary: str) -> bool:
    """
    添加复盘总结
    
    参数：
        record_id: 记录ID
        summary: 复盘总结内容
    
    返回：是否成功
    """
    _init_db()
    
    data = {
        'content': summary,
        'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    conn = _get_db()
    c = conn.cursor()
    c.execute('UPDATE records SET summary = ? WHERE id = ?', (json.dumps(data, ensure_ascii=False), record_id))
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def get_record_detail(record_id: int) -> Optional[Dict]:
    """获取单条记录的详细信息"""
    _init_db()
    
    conn = _get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM records WHERE id = ?', (record_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return _row_to_dict(row)
    return None


def format_records_for_display(records: List[Dict], detailed: bool = False) -> str:
    """
    格式化记录列表，用于显示
    
    参数：
        records: 记录列表
        detailed: 是否详细显示（单条记录时为True）
    """
    if not records:
        return "没有找到匹配的卦例记录。"
    
    lines = []
    
    if len(records) == 1 and detailed:
        # 单条记录，详细显示（仅 detail 命令）
        r = records[0]
        lines.append(f"卦例 #{r['id']}")
        lines.append("")
        lines.append(f"问：{r['question']}")
        
        p = r.get('pattern', {})
        if isinstance(p, dict) and p.get('time'):
            lines.append(f"时间：{p.get('time')}")
        else:
            lines.append(f"时间：{r['date']}")
        
        lines.append(f"方式：{r['method']}（{r['params']}）")
        
        if isinstance(p, dict):
            lines.append(f"干支：{p.get('ganzhi', 'N/A')}")
            lines.append(f"五行：{p.get('wuxing', 'N/A')}")
            lines.append("")
            lines.append("排盘")
            lines.append(f"主卦：{p.get('main', '')} {p.get('main_guaci', '')}")
            lines.append(f"互卦：{p.get('hugua', 'N/A')}")
            lines.append(f"变卦：{p.get('biangua', '')} {p.get('biangua_guaci', '')}")
            lines.append(f"动爻：{p.get('dongyao', 'N/A')}")
        
        lines.append("")
        lines.append("推断过程")
        lines.append("")
        
        analysis = r.get('analysis', 'N/A')
        lines.append(analysis)
        
        lines.append("")
        lines.append("结论")
        lines.append("")
        lines.append(r.get('conclusion', 'N/A'))
        
        lines.append("")
        lines.append(f"状态：")
        
        fb = r.get('feedback')
        if fb:
            status = "✅ 正确" if fb.get('correct') else "❌ 错误"
            lines.append(status)
            lines.append("")
            lines.append(f"  实际结果：{fb.get('result', '')}")
            if fb.get('correct_reason'):
                lines.append(f"  正确原因：{fb.get('correct_reason', '')}")
            if fb.get('incorrect_reason'):
                lines.append(f"  错误原因：{fb.get('incorrect_reason', '')}")
            if fb.get('xiang_analysis'):
                lines.append(f"  取象分析：{fb.get('xiang_analysis', '')}")
        else:
            lines.append("⏳ 待反馈")
        
    else:
        # 多条记录，简略显示
        lines.append(f"共找到 {len(records)} 条记录：\n")
        lines.append("─" * 60)
        lines.append(f"{'编号':<6}{'时间':<20}{'问题':<15}{'推断结果':<10}  实际结果   反馈")
        lines.append("─" * 60)
        
        for r in records:
            p = r.get('pattern', {})
            time_str = p.get('time', r['date']) if isinstance(p, dict) else r['date']
            
            question = r['question']
            if len(question) > 12:
                question = question[:12] + "..."
            
            conclusion = r.get('conclusion', 'N/A')
            # 提取结论第一句或前20字
            conclusion_short = conclusion.split('。')[0] if '。' in conclusion else conclusion[:20]
            if len(conclusion_short) > 18:
                conclusion_short = conclusion_short[:18] + "..."
            
            fb = r.get('feedback')
            if fb:
                actual_result = "✅ 正确" if fb.get('correct') else "❌ 错误"
                has_feedback = "已反馈"
            else:
                actual_result = "-"
                has_feedback = "⏳ 待反馈"
            
            lines.append(f"#{r['id']:<5}{time_str:<20}{question:<15}{conclusion_short:<18}  {actual_result:<8}  {has_feedback}")
    
    return "\n".join(lines)


# ══════════════════════════════════════════════
# CLI入口
# ══════════════════════════════════════════════
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：")
        print("  python records.py list [关键词]        # 列出所有记录")
        print("  python records.py pending              # 列出待反馈的记录")
        print("  python records.py detail <id>         # 查看记录详情")
        print("  python records.py query <关键词>      # 搜索记录")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        records = query_records(keyword=keyword)
        print(format_records_for_display(records))
    
    elif cmd == 'pending':
        records = query_records(pending_only=True)
        print(format_records_for_display(records))
    
    elif cmd == 'detail':
        if len(sys.argv) < 3:
            print("用法：python records.py detail <id>")
            sys.exit(1)
        r = get_record_detail(int(sys.argv[2]))
        if r:
            print(format_records_for_display([r], detailed=True))
        else:
            print(f"未找到记录 #{sys.argv[2]}")
    
    elif cmd == 'query':
        if len(sys.argv) < 3:
            print("用法：python records.py query <关键词>")
            sys.exit(1)
        records = query_records(keyword=sys.argv[2])
        print(format_records_for_display(records))
    
    else:
        print(f"未知命令：{cmd}")
        print("可用命令：list, pending, detail, query")
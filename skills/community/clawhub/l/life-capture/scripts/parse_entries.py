#!/usr/bin/env python3
import argparse
import json
import re
import sqlite3
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TYPE_PREFIX = {
    "expense": "exp",
    "task": "task",
    "schedule": "sched",
    "idea": "idea",
}

WEEKDAY_MAP = {
    "一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6,
}

DEFAULT_CONFIG = {
    "expense_category_rules": [],
    "expense_subcategory_rules": [],
    "idea_type_rules": [],
    "task_project_rules": [],
    "schedule_tag_rules": [],
    "default_tags": {
        "expense": ["开销"],
        "task_done": ["任务", "完成"],
        "task_todo": ["任务", "待办"],
        "schedule": ["日程"],
        "idea": ["灵感"],
    },
    "hints": {
        "idea": r"想到|想法|灵感|也许可以|可以做|或许可以|点子|构思|试试",
        "schedule": r"明天|后天|今天|今晚|上午|中午|下午|晚上|点|会议|开会|体检|预约|去|安排|计划",
        "task_done": r"完成|做完|改完|整理好|整理了|收拾好|收拾了|交了|打了|写完|提交了|处理了|跑了",
        "task_todo": r"待办|要做|需要|得|准备|记得|安排",
        "expense": r"花了|花费|消费|买|付款|支付|转账|报销|元|块|¥|￥|人民币",
    },
}

CONFIG = None


def load_config(path: Optional[str]) -> Dict:
    default_path = Path(__file__).resolve().parents[1] / 'references' / 'parser_config.json'
    config_path = Path(path) if path else default_path
    if not config_path.exists():
        return DEFAULT_CONFIG
    with open(config_path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    merged = dict(DEFAULT_CONFIG)
    for key, value in loaded.items():
        merged[key] = value
    return merged


def split_items(text: str) -> List[str]:
    normalized = re.sub(r"[\n；;。]+", "|", text)
    normalized = re.sub(r"，(?=(明天|后天|今天|今晚|上午|中午|下午|晚上|想到|想法|灵感|买|花了|花费|完成|做完|改完|整理好|交了|打了|写完|提交了|处理了))", "|", normalized)
    normalized = re.sub(r"(?<=\d)\s+(?=(明天|后天|今天|今晚|上午|中午|下午|晚上|想到|想法|灵感|买|花了|花费|完成|做完|改完|整理好|交了|打了|写完|提交了|处理了))", "|", normalized)
    parts = [p.strip(" ，,|\t") for p in normalized.split("|")]
    return [p for p in parts if p]


def infer_type(text: str) -> str:
    hints = CONFIG['hints']
    if re.search(hints['idea'], text):
        return 'idea'
    if re.search(hints['expense'], text) and re.search(r"\d+(?:\.\d+)?", text):
        return 'expense'
    if re.search(hints['task_done'], text):
        return 'task'
    if re.search(hints['task_todo'], text):
        return 'task'
    if re.search(hints['schedule'], text):
        if re.search(r"明天|后天|今天|今晚|周[一二三四五六日天]|星期[一二三四五六日天]|[零一二两三四五六七八九十\d]{1,3}点|:\d{2}", text):
            return 'schedule'
    return 'idea'


CN_NUM = {"零":0,"一":1,"二":2,"两":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}


def cn_to_int(token: str) -> Optional[int]:
    if token.isdigit():
        return int(token)
    if token in CN_NUM:
        return CN_NUM[token]
    if token.startswith('十'):
        return 10 + CN_NUM.get(token[1:], 0)
    if '十' in token:
        left, right = token.split('十', 1)
        left_val = CN_NUM.get(left, 1)
        right_val = CN_NUM.get(right, 0)
        return left_val * 10 + right_val
    return None


def parse_time(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    meridiem = None
    if '上午' in text:
        meridiem = '上午'
    elif '中午' in text:
        meridiem = '中午'
    elif '下午' in text:
        meridiem = '下午'
    elif '晚上' in text or '今晚' in text:
        meridiem = '晚上'

    match = re.search(r"([零一二两三四五六七八九十\d]{1,3})(?::|点)(\d{1,2})?", text)
    if not match:
        return None, None, None
    hour = cn_to_int(match.group(1))
    if hour is None:
        return None, meridiem, match.group(0)
    minute = int(match.group(2) or 0)
    if meridiem in ('下午', '晚上') and hour < 12:
        hour += 12
    if meridiem == '中午' and hour < 11:
        hour += 12
    return f"{hour:02d}:{minute:02d}", meridiem, match.group(0)


def parse_date_value(text: str, today: date) -> str:
    if '后天' in text:
        return (today + timedelta(days=2)).isoformat()
    if '明天' in text:
        return (today + timedelta(days=1)).isoformat()
    if '今天' in text or '今晚' in text:
        return today.isoformat()

    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.search(r"(\d{1,2})月(\d{1,2})日", text)
    if m:
        return f"{today.year:04d}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    m = re.search(r"(?:周|星期)([一二三四五六日天])", text)
    if m:
        target = WEEKDAY_MAP[m.group(1)]
        delta = (target - today.weekday()) % 7
        return (today + timedelta(days=delta)).isoformat()
    return today.isoformat()


def next_sequence(db_path: Optional[Path], record_type: str, datestr: str, used: Dict[Tuple[str, str], int]) -> int:
    key = (record_type, datestr)
    current = used.get(key, 0)
    if current:
        used[key] = current + 1
        return current + 1
    max_seq = 0
    if db_path and db_path.exists():
        prefix = TYPE_PREFIX[record_type]
        ymd = datestr.replace('-', '')
        pattern = f"{prefix}_{ymd}_%"
        conn = sqlite3.connect(str(db_path))
        try:
            rows = conn.execute('SELECT id FROM entries WHERE id LIKE ?', (pattern,)).fetchall()
        except sqlite3.Error:
            rows = []
        finally:
            conn.close()
        for (entry_id,) in rows:
            m = re.match(r"^[a-z]+_\d{8}_(\d{3})$", entry_id)
            if m:
                max_seq = max(max_seq, int(m.group(1)))
    used[key] = max_seq + 1
    return max_seq + 1


def make_id(db_path: Optional[Path], record_type: str, datestr: str, used: Dict[Tuple[str, str], int]) -> str:
    seq = next_sequence(db_path, record_type, datestr, used)
    return f"{TYPE_PREFIX[record_type]}_{datestr.replace('-', '')}_{seq:03d}"


def dedupe_tags(tags: List[str]) -> List[str]:
    out = []
    for t in tags:
        t = (t or '').strip().replace('#', '')
        if t and t not in out:
            out.append(t[:8])
    return out[:4]


def apply_first_rule(text: str, rules: List[Dict], default_key: str, default_value: Optional[str]) -> Tuple[Optional[str], List[str]]:
    for rule in rules:
        if re.search(rule['pattern'], text):
            return rule.get(default_key, default_value), rule.get('tags', [])
    return default_value, []


def parse_expense(text: str) -> Dict:
    amount = None
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:元|块|¥|￥)", text)
    if not m:
        m = re.search(r"(?:花了|花费|消费|买(?:了)?)[^\d]*(\d+(?:\.\d+)?)", text)
    if m:
        amount = float(m.group(1))
        if amount.is_integer():
            amount = int(amount)

    category, category_tags = apply_first_rule(text, CONFIG['expense_category_rules'], 'category', '其他')
    subcategory, sub_tags = apply_first_rule(text, CONFIG['expense_subcategory_rules'], 'subcategory', None)

    merchant = None
    merchant_match = re.search(r"在(.+?)(?:买|吃|付款|消费)", text)
    if merchant_match:
        merchant = merchant_match.group(1).strip()

    pay_method = None
    if '微信' in text:
        pay_method = '微信'
    elif '支付宝' in text:
        pay_method = '支付宝'
    elif '银行卡' in text:
        pay_method = '银行卡'
    elif '现金' in text:
        pay_method = '现金'

    tags = CONFIG['default_tags'].get('expense', []) + [category] + category_tags + sub_tags
    if subcategory:
        tags.append(subcategory)
    tags = dedupe_tags(tags)

    summary = text
    if amount is not None:
        summary = f"{category}消费 {amount} 元"
        if subcategory:
            summary = f"{subcategory}，消费 {amount} 元"
    return {
        'tags': tags,
        'summary': summary,
        'payload': {
            'amount': amount,
            'currency': 'CNY' if amount is not None else None,
            'category': category,
            'subcategory': subcategory,
            'merchant': merchant,
            'pay_method': pay_method,
        },
    }


def parse_task(text: str, today: date) -> Dict:
    status = 'done' if re.search(CONFIG['hints']['task_done'], text) else 'todo'
    priority = 'high' if re.search(r"重要|尽快|马上|紧急", text) else 'normal'
    due_date = None
    if status != 'done' and re.search(r"明天|后天|今天|周[一二三四五六日天]|星期[一二三四五六日天]|\d{4}-\d{2}-\d{2}|\d{1,2}月\d{1,2}日", text):
        due_date = parse_date_value(text, today)
    completed_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') if status == 'done' else None

    project, project_tags = apply_first_rule(text, CONFIG['task_project_rules'], 'project', None)
    tags = CONFIG['default_tags'].get('task_done' if status == 'done' else 'task_todo', []) + project_tags
    if project:
        tags.append(project)
    tags = dedupe_tags(tags)
    return {
        'tags': tags,
        'summary': text,
        'payload': {
            'status': status,
            'priority': priority,
            'project': project,
            'due_date': due_date,
            'completed_at': completed_at,
        },
    }


def parse_schedule(text: str, today: date) -> Dict:
    schedule_date = parse_date_value(text, today)
    start_time, meridiem, _ = parse_time(text)
    end_time = None
    m = re.search(r"(\d{1,2})(?::|点)(\d{1,2})?\s*[到-]\s*(\d{1,2})(?::|点)?(\d{1,2})?", text)
    if m:
        sh = int(m.group(1))
        sm = int(m.group(2) or 0)
        eh = int(m.group(3))
        em = int(m.group(4) or 0)
        if meridiem in ('下午', '晚上') and sh < 12:
            sh += 12
        if meridiem in ('下午', '晚上') and eh < 12:
            eh += 12
        start_time = f"{sh:02d}:{sm:02d}"
        end_time = f"{eh:02d}:{em:02d}"

    location = None
    loc = re.search(r"去([^，,。]+)", text)
    if loc:
        location = loc.group(1).strip()

    status = 'planned'
    if '已完成' in text or '去了' in text:
        status = 'done'
    elif '取消' in text:
        status = 'skipped'

    tags = list(CONFIG['default_tags'].get('schedule', ['日程']))
    extra_tag = None
    for rule in CONFIG['schedule_tag_rules']:
        if re.search(rule['pattern'], text):
            extra_tag = rule['tag']
            break
    if extra_tag:
        tags.append(extra_tag)
    elif location:
        tags.append(location[:6])
    tags = dedupe_tags(tags)
    return {
        'tags': tags,
        'summary': text,
        'payload': {
            'schedule_date': schedule_date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'status': status,
        },
    }


def parse_idea(text: str) -> Dict:
    idea_type, idea_tags = apply_first_rule(text, CONFIG['idea_type_rules'], 'idea_type', '生活')
    tags = dedupe_tags(CONFIG['default_tags'].get('idea', ['灵感']) + idea_tags + [idea_type])
    return {
        'tags': tags,
        'summary': text,
        'payload': {
            'idea_type': idea_type,
            'status': 'captured',
            'related_task_id': None,
        },
    }


def parse_record(text: str, today: date, db_path: Optional[Path], used: Dict[Tuple[str, str], int]) -> Dict:
    rtype = infer_type(text)
    effective_date = parse_date_value(text, today) if rtype == 'schedule' else today.isoformat()
    time_value, _, _ = parse_time(text)

    parser = {
        'expense': parse_expense,
        'task': lambda t: parse_task(t, today),
        'schedule': lambda t: parse_schedule(t, today),
        'idea': parse_idea,
    }[rtype]
    parsed = parser(text)
    return {
        'id': make_id(db_path, rtype, effective_date, used),
        'type': rtype,
        'date': effective_date if rtype != 'schedule' else parsed['payload'].get('schedule_date') or effective_date,
        'time': time_value,
        'title': None,
        'raw_text': text,
        'summary': parsed['summary'],
        'tags': parsed['tags'],
        'payload': parsed['payload'],
    }


def main() -> int:
    global CONFIG
    parser = argparse.ArgumentParser()
    parser.add_argument('--text')
    parser.add_argument('--input')
    parser.add_argument('--stdin', action='store_true')
    parser.add_argument('--db')
    parser.add_argument('--today', help='YYYY-MM-DD')
    parser.add_argument('--config', help='path to parser config json')
    args = parser.parse_args()

    CONFIG = load_config(args.config)

    if args.stdin:
        import sys
        text = sys.stdin.read().strip()
    elif args.input:
        text = Path(args.input).read_text(encoding='utf-8').strip()
    elif args.text:
        text = args.text.strip()
    else:
        raise SystemExit('provide --text, --input, or --stdin')

    today = date.fromisoformat(args.today) if args.today else date.today()
    db_path = Path(args.db) if args.db else None
    items = split_items(text)
    used: Dict[Tuple[str, str], int] = defaultdict(int)
    records = [parse_record(item, today, db_path, used) for item in items]
    print(json.dumps({'records': records}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

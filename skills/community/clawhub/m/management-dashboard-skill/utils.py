"""
工具函数模块
"""
import json
import uuid
import re
from datetime import datetime, timedelta
from typing import Tuple, Optional, Any, Dict

from config import HTML_FILE_ENCODING, JSON_FILE_ENCODING


def generate_uuid() -> str:
    """生成 UUID"""
    return str(uuid.uuid4())


def parse_time_input(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    解析用户输入的时间参数
    
    支持格式：
    - "系统驾驶舱" -> (None, None)  # 使用默认时间
    - "系统驾驶舱 2026-06-04" -> ("2026-06-04 00:00:00", "2026-06-04 23:59:59")
    - "系统驾驶舱 2026-06-01 2026-06-04" -> ("2026-06-01 00:00:00", "2026-06-04 23:59:59")
    - "系统驾驶舱 近一周" -> 最近7天
    - "系统驾驶舱 近三天" -> 最近3天
    - "系统驾驶舱 今天" -> 今天
    - "系统驾驶舱 昨天" -> 昨天
    
    Returns:
        (start_time, end_time) 格式为 "YYYY-MM-DD HH:MM:SS"
    """
    # 移除触发词
    clean_input = re.sub(
        r'系统驾驶舱|管理驾驶舱|日报生成|management-dashboard-skill',
        '', user_input, flags=re.IGNORECASE
    ).strip()
    
    if not clean_input:
        return None, None
    
    # 处理相对时间描述
    now = datetime.now()
    
    # 今天
    if re.search(r'今天|今日', clean_input):
        start_time = now.replace(hour=0, minute=0, second=0)
        end_time = now.replace(hour=23, minute=59, second=59)
        fmt = "%Y-%m-%d %H:%M:%S"
        return start_time.strftime(fmt), end_time.strftime(fmt)
    
    # 昨天
    if re.search(r'昨天|昨日', clean_input):
        yesterday = now - timedelta(days=1)
        start_time = yesterday.replace(hour=0, minute=0, second=0)
        end_time = yesterday.replace(hour=23, minute=59, second=59)
        fmt = "%Y-%m-%d %H:%M:%S"
        return start_time.strftime(fmt), end_time.strftime(fmt)
    
    # 近N小时
    hours_match = re.search(r'近(\d+)小时|最近(\d+)小时|(\d+)小时', clean_input)
    if hours_match:
        hours = int(hours_match.group(1) or hours_match.group(2) or hours_match.group(3))
        end_time = now
        start_time = now - timedelta(hours=hours)
        fmt = "%Y-%m-%d %H:%M:%S"
        return start_time.strftime(fmt), end_time.strftime(fmt)
    
    # 近N天/周/月
    days_match = re.search(r'近(\d+)天|最近(\d+)天|(\d+)天', clean_input)
    weeks_match = re.search(r'近(\d+)周|最近(\d+)周|(\d+)周|一周|一星期', clean_input)
    months_match = re.search(r'近(\d+)月|最近(\d+)月|(\d+)月|一个月', clean_input)
    
    if days_match:
        days = int(days_match.group(1) or days_match.group(2) or days_match.group(3))
        start_time = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0)
        end_time = now.replace(hour=23, minute=59, second=59)
        fmt = "%Y-%m-%d %H:%M:%S"
        return start_time.strftime(fmt), end_time.strftime(fmt)
    
    if weeks_match:
        # 提取数字，如果没有则默认为1
        num_match = re.search(r'(\d+)', clean_input)
        weeks = int(num_match.group(1)) if num_match else 1
        days = weeks * 7
        start_time = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0)
        end_time = now.replace(hour=23, minute=59, second=59)
        fmt = "%Y-%m-%d %H:%M:%S"
        return start_time.strftime(fmt), end_time.strftime(fmt)
    
    if months_match:
        # 提取数字，如果没有则默认为1
        num_match = re.search(r'(\d+)', clean_input)
        months = int(num_match.group(1)) if num_match else 1
        days = months * 30
        start_time = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0)
        end_time = now.replace(hour=23, minute=59, second=59)
        fmt = "%Y-%m-%d %H:%M:%S"
        return start_time.strftime(fmt), end_time.strftime(fmt)
    
    # 尝试匹配日期格式
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    dates = re.findall(date_pattern, clean_input)
    
    if len(dates) == 1:
        # 单个日期：查询该天
        date_str = dates[0]
        return f"{date_str} 00:00:00", f"{date_str} 23:59:59"
    elif len(dates) >= 2:
        # 两个日期：查询区间
        return f"{dates[0]} 00:00:00", f"{dates[1]} 23:59:59"
    
    return None, None


def get_default_time_range(days: int = 1) -> Tuple[str, str]:
    """获取默认时间范围（最近N天）"""
    now = datetime.now()
    end_time = now.replace(hour=23, minute=59, second=59)
    start_time = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0)
    
    fmt = "%Y-%m-%d %H:%M:%S"
    return start_time.strftime(fmt), end_time.strftime(fmt)


def format_date_display(date_str: str) -> str:
    """格式化日期用于显示，如 '2026年6月4日 星期四'"""
    try:
        dt = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekday = weekdays[dt.weekday()]
        return f"{dt.year}年{dt.month}月{dt.day}日 {weekday}"
    except:
        return date_str


def format_date_range_display(start_time: str, end_time: str) -> str:
    """
    根据起止时间生成报表标题中的日期范围描述。
    - 同一天：'2026年6月22日 星期一（当日复盘汇总）'
    - 跨多天：'2026年6月16日 ~ 6月22日（近7天汇总）'
    """
    try:
        start_dt = datetime.strptime(start_time.split()[0], "%Y-%m-%d")
        end_dt = datetime.strptime(end_time.split()[0], "%Y-%m-%d")
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

        if start_dt.date() == end_dt.date():
            weekday = weekdays[start_dt.weekday()]
            return f"{start_dt.year}年{start_dt.month}月{start_dt.day}日 {weekday}（当日复盘汇总）"

        days_span = (end_dt - start_dt).days
        start_weekday = weekdays[start_dt.weekday()]
        end_weekday = weekdays[end_dt.weekday()]
        return (
            f"{start_dt.year}年{start_dt.month}月{start_dt.day}日 {start_weekday} ~ "
            f"{end_dt.month}月{end_dt.day}日 {end_weekday}（近{days_span}天汇总）"
        )
    except:
        return start_time


def resolve_team_name(
    org_id: str,
    org_name: Optional[str] = None,
    team_name: Optional[str] = None,
) -> str:
    """团队展示名：优先入参 team_name，其次接口 orgName，最后 组织{orgId}"""
    if team_name and team_name.strip():
        return team_name.strip()
    if org_name and org_name.strip():
        return org_name.strip()
    if org_id:
        return f"组织{org_id}"
    return "未知团队"


def extract_org_info(data: Dict[str, Any]) -> Tuple[str, str]:
    """从分页接口 data 提取 orgId、orgName（orgName 优先 data 级，其次 contents 首条）"""
    org_id = str(data.get('orgId') or '').strip()
    org_name = str(data.get('orgName') or '').strip()
    if not org_name:
        for item in data.get('contents', []) or []:
            if isinstance(item, dict):
                name = str(item.get('orgName') or '').strip()
                if name:
                    org_name = name
                    break
    return org_id, org_name


def generate_report_filename(start_time: str, end_time: str = '') -> str:
    """生成报表文件名，如 系统驾驶舱报告_2026-06-08.html 或 系统驾驶舱报告_2026-06-16_06-22.html"""
    start_date = start_time.split()[0] if start_time else ''
    if end_time:
        end_date = end_time.split()[0]
        if start_date != end_date:
            # 跨天：用起止日期
            return f"系统驾驶舱报告_{start_date}_{end_date[5:]}.html"
    return f"系统驾驶舱报告_{start_date}.html"


def write_html_file(file_path: str, content: str) -> None:
    """以 UTF-8 BOM 写入 HTML，确保 iOS/Android/PC/小程序 WebView 正确显示中文"""
    with open(file_path, 'w', encoding=HTML_FILE_ENCODING, newline='\n') as f:
        f.write(content)


def read_json_file(file_path: str) -> Any:
    """以 UTF-8 读取 JSON 文件"""
    with open(file_path, 'r', encoding=JSON_FILE_ENCODING) as f:
        return json.load(f)


def write_json_file(file_path: str, data: Any) -> None:
    """以 UTF-8 写入 JSON 文件（ensure_ascii=False 保留中文）"""
    with open(file_path, 'w', encoding=JSON_FILE_ENCODING) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

import requests
import json
from datetime import datetime, timedelta
import calendar
import re
import os

class NaturalLanguageParser:
    """自然语言解析器 - 解析日期、优先级等"""

    def __init__(self):
        self.today = datetime.now()

    def parse_date(self, date_str):
        """解析相对日期字符串"""
        if not date_str:
            return None

        date_str = date_str.strip().lower()

        # 相对日期映射
        date_map = {
            "今天": self.today,
            "tomorrow": self.today + timedelta(days=1),
            "明天": self.today + timedelta(days=1),
            "后天": self.today + timedelta(days=2),
            "后天": self.today + timedelta(days=2),
            "next week": self.today + timedelta(weeks=1),
            "下周": self.today + timedelta(weeks=1),
            "this week": self.today + timedelta(days=7),
            "本周": self.today + timedelta(days=7),
            "end of month": self.today.replace(day=calendar.monthrange(self.today.year, self.today.month)[1]),
            "月底": self.today.replace(day=calendar.monthrange(self.today.year, self.today.month)[1]),
            "next month end": (self.today + timedelta(days=32)).replace(day=1) - timedelta(days=1),
            "下月底": (self.today + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        }

        if date_str in date_map:
            return date_map[date_str]

        # 匹配 "X天" 或 "X周"
        days_match = re.match(r'(\d+)\s*[天日]', date_str)
        if days_match:
            days = int(days_match.group(1))
            return self.today + timedelta(days=days)

        weeks_match = re.match(r'(\d+)\s*[周星期]', date_str)
        if weeks_match:
            weeks = int(weeks_match.group(1))
            return self.today + timedelta(weeks=weeks)

        return None

    def parse_priority(self, priority_str):
        """解析优先级字符串"""
        if not priority_str:
            return None

        priority_str = priority_str.strip().lower()

        priority_map = {
            "highest": "Highest",
            "highest": "Highest",
            "最高": "Highest",
            "high": "High",
            "high": "High",
            "高": "High",
            "medium": "Medium",
            "medium": "Medium",
            "中等": "Medium",
            "low": "Low",
            "low": "Low",
            "低": "Low"
        }

        return priority_map.get(priority_str, "Medium")


class UserSearcher:
    """用户搜索器 - 多方式查找用户"""

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.cache = {}
        self.cache_ttl = 300  # 5分钟缓存
        self.user_mapping = {}

    def search_user(self, query, project_key=None):
        """搜索用户"""
        if not query:
            return None

        query = query.strip()

        # 检查缓存
        cache_key = f"{query}_{project_key}"
        if cache_key in self.cache:
            cached_user, cached_time = self.cache[cache_key]
            if (datetime.now() - cached_time).total_seconds() < self.cache_ttl:
                return cached_user

        # 多方式搜索
        user = self._search_by_name(query, project_key)
        if not user:
            user = self._search_by_email(query, project_key)
        if not user:
            user = self._search_by_display_name(query, project_key)

        # 缓存结果
        if user:
            self.cache[cache_key] = (user, datetime.now())

        return user

    def _search_by_name(self, name, project_key=None):
        """通过用户名搜索"""
        endpoint = "/rest/api/3/user/assignable/search"
        params = {"query": name}
        if project_key:
            params["projectKey"] = project_key

        return self._make_request(endpoint, params)

    def _search_by_email(self, email, project_key=None):
        """通过邮箱搜索"""
        endpoint = "/rest/api/3/user/search"
        params = {"query": email}
        if project_key:
            params["projectKey"] = project_key

        return self._make_request(endpoint, params)

    def _search_by_display_name(self, display_name, project_key=None):
        """通过显示名称搜索"""
        endpoint = "/rest/api/3/user/assignable/search"
        params = {"query": display_name}
        if project_key:
            params["projectKey"] = project_key

        return self._make_request(endpoint, params)

    def _make_request(self, endpoint, params):
        """发送 HTTP 请求"""
        url = f"{self.base_url.rstrip('/')}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                users = response.json()
                if users and len(users) > 0:
                    return users[0]
            return None
        except Exception as e:
            print(f"[ERROR] User search failed: {str(e)}")
            return None


def create_issue(summary, description=None, project_key=None, issue_type_name=None,
                priority=None, assignee=None, due_date=None):
    """创建 Jira Issue"""

    base_url = os.getenv("JIRA_BASE_URL")
    token = os.getenv("JIRA_BEARER_TOKEN")

    if not base_url or not token:
        return {
            "success": False,
            "error": "JIRA_BASE_URL and JIRA_BEARER_TOKEN environment variables required"
        }

    # 默认值
    if not project_key:
        project_key = os.getenv("JIRA_DEFAULT_PROJECT")
    if not assignee:
        assignee = os.getenv("JIRA_DEFAULT_ASSIGNEE")

    # 构建 issue 数据
    issue_data = {
        "fields": {
            "summary": summary,
            "project": {"key": project_key} if project_key else None,
            "issuetype": {"name": issue_type_name} if issue_type_name else None,
        }
    }

    # 添加可选字段
    if description:
        issue_data["fields"]["description"] = description

    if priority:
        parser = NaturalLanguageParser()
        priority = parser.parse_priority(priority)
        issue_data["fields"]["priority"] = {"name": priority}

    if assignee:
        issue_data["fields"]["assignee"] = {"name": assignee}

    if due_date:
        parser = NaturalLanguageParser()
        due_date = parser.parse_date(due_date)
        if due_date:
            issue_data["fields"]["duedate"] = due_date.strftime("%Y-%m-%dT%H:%M:%S.000+08:00")

    # 发送请求
    url = f"{base_url.rstrip('/')}/rest/api/3/issue"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=issue_data, timeout=30)
        print(f"[INFO] Status code: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            return {
                "success": True,
                "issue_key": result["key"],
                "issue_id": result["id"],
                "self": result["self"]
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "details": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def search_user(query, project_key=None):
    """搜索用户（便捷函数）"""
    base_url = os.getenv("JIRA_BASE_URL")
    token = os.getenv("JIRA_BEARER_TOKEN")

    if not base_url or not token:
        return None

    searcher = UserSearcher(base_url, token)
    return searcher.search_user(query, project_key)

#!/usr/bin/env python3
"""
Oil Price Monitor - 发改委成品油价格调整监控 (优化版)

从2026-04-07开始，每10个工作日一个调价窗口。
每日17:30运行，仅在窗口日执行监控和推送。
当年最后一个窗口日会预测下一年度窗口期。
"""

import sys
import json
import subprocess
from datetime import datetime, timedelta, date
from typing import Optional, Dict, List, Tuple
import re
from pathlib import Path

# 添加技能路径支持
workspace_skills = Path(__file__).parent.parent
chinese_workdays_path = workspace_skills / 'chinese-workdays'
if chinese_workdays_path.exists() and str(chinese_workdays_path) not in sys.path:
    sys.path.insert(0, str(chinese_workdays_path))

try:
    from chinese_workdays import ChineseWorkdays
except ImportError as e:
    print("❌ 错误: 需要 chinese-workdays 技能支持")
    print(f"   详细错误: {e}")
    sys.exit(1)

# ============ 配置参数 ============
START_DATE = date(2026, 4, 7)  # 第一个窗口期
WINDOW_INTERVAL = 10  # 工作日间隔
CHECK_TIME = "17:30"  # 每日检查时间
NDRC_URL = "https://www.ndrc.gov.cn/xwdt/xwfb/"
KEYWORDS = ["成品油", "油价", "汽油", "柴油", "调价", "调整"]

# 数据存储路径（用于保存窗口期缓存）
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
WINDOWS_CACHE = DATA_DIR / "windows_cache.json"


class OilPriceMonitor:
    def __init__(self):
        self.calc = ChineseWorkdays()
        self.today = date.today()
        self.year_windows = {}  # 缓存各年窗口期

    def load_windows_cache(self) -> Dict:
        """加载缓存的窗口期数据"""
        if WINDOWS_CACHE.exists():
            try:
                with open(WINDOWS_CACHE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"windows": {}, "last_updated": None}

    def save_windows_cache(self, cache: Dict):
        """保存窗口期缓存"""
        with open(WINDOWS_CACHE, 'w') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

    def get_windows_for_year(self, year: int) -> List[date]:
        """获取指定年份的所有调价窗口日期"""
        cache = self.load_windows_cache()
        year_key = str(year)

        # 检查缓存
        if year_key in cache.get("windows", {}):
            return [date.fromisoformat(d) for d in cache["windows"][year_key]]

        # 计算该年所有窗口
        windows = []
        current = START_DATE
        while current.year <= year:
            if current.year == year:
                windows.append(current)
            # 计算下一个窗口
            current = self.add_workdays(current, WINDOW_INTERVAL)
            if current.year > year + 1:  # 超出范围停止
                break

        # 缓存结果
        if "windows" not in cache:
            cache["windows"] = {}
        cache["windows"][year_key] = [d.isoformat() for d in windows]
        cache["last_updated"] = self.today.isoformat()
        self.save_windows_cache(cache)

        return windows

    def is_window_day(self) -> bool:
        """检查今天是否是调价窗口期"""
        windows_this_year = self.get_windows_for_year(self.today.year)
        return self.today in windows_this_year

    def get_next_window(self) -> date:
        """获取下一个调价窗口日期"""
        windows_this_year = self.get_windows_for_year(self.today.year)
        for w in windows_this_year:
            if w > self.today:
                return w
        # 当年没有后续窗口，计算下一年
        return self.get_windows_for_year(self.today.year + 1)[0]

    def get_previous_window(self) -> date:
        """获取上一个调价窗口日期"""
        windows_this_year = self.get_windows_for_year(self.today.year)
        # 先在今年找过去的窗口
        for w in reversed(windows_this_year):
            if w < self.today:
                return w
        # 今年没有过去的窗口，查去年
        try:
            windows_last_year = self.get_windows_for_year(self.today.year - 1)
            if windows_last_year:
                return windows_last_year[-1]
        except:
            pass
        # 还没有，返回起始日
        return START_DATE

    def add_workdays(self, start_date: date, workdays: int) -> date:
        """添加指定数量的工作日"""
        result = start_date
        added = 0
        while added < workdays:
            result += timedelta(days=1)
            if self._is_workday(result):
                added += 1
        return result

    def _is_workday(self, d: date) -> bool:
        """判断某天是否工作日（基于 chinese-workdays 逻辑）"""
        # 周末不算
        if d.weekday() >= 5:
            return False

        # 获取该年节假日安排
        if d.year not in self.calc.holiday_schedules:
            # 没有数据，默认按工作日算
            return True

        schedule = self.calc.holiday_schedules[d.year]

        # 检查是否是调休上班（优先级最高）
        for holiday in schedule.get('holidays', []):
            if d.isoformat() in holiday.get('makeup_workdays', []):
                return True

        # 检查是否是法定节假日
        for holiday in schedule.get('holidays', []):
            if d.isoformat() in holiday.get('days_off', []):
                return False

        # 普通工作日
        return True

    def fetch_ndrc_news(self, limit: int = 20) -> List[Dict]:
        """从发改委网站获取最新新闻"""
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            print("⚠️  缺少依赖，请安装: pip install requests beautifulsoup4 lxml")
            return []

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(NDRC_URL, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'lxml')

            # 查找新闻列表
            news_items = []
            selectors = [
                '.list li a',
                '.news-list a',
                'ul.list a',
                'a[href*="news"]',
                'a[href*="content"]'
            ]

            links = []
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    links.extend(elements)
                    break

            if not links:
                links = soup.find_all('a', href=True)[:50]

            for link in links[:limit]:
                href = link.get('href', '')
                title = link.get_text(strip=True)

                if not title or len(title) < 5:
                    continue

                if href.startswith('/'):
                    href = 'https://www.ndrc.gov.cn' + href

                news_items.append({
                    'title': title,
                    'url': href,
                    'date': self.today.strftime("%Y-%m-%d"),
                    'content': ''
                })

            return news_items[:limit]

        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return []

    def detect_price_change(self, news: List[Dict]) -> Optional[Dict]:
        """检测新闻中是否包含价格调整信息"""
        for item in news:
            text = item['title'] + ' ' + item.get('content', '')

            keyword_hits = [kw for kw in KEYWORDS if kw in text]
            if not keyword_hits:
                continue

            increase = any(w in text for w in ['上调', '上涨', '提高', '增加'])
            decrease = any(w in text for w in ['下调', '降低', '下降', '减少'])

            amount_patterns = [
                r'每吨[上调|下调|上涨|降低]+\s*(\d+)\s*元',
                r'[汽油|柴油].*?(\d{2,3})\s*元',
                r'调整.*?(\d{2,3})\s*元/吨'
            ]

            amount = None
            for pattern in amount_patterns:
                match = re.search(pattern, text)
                if match:
                    amount = int(match.group(1))
                    break

            return {
                'title': item['title'],
                'date': item['date'],
                'url': item['url'],
                'increase': increase,
                'decrease': decrease,
                'amount': amount,
                'raw_text': text[:300],
                'keywords': keyword_hits
            }
        return None

    def format_output(self, info: Dict, window_num: int) -> str:
        """格式化输出"""
        output = f"""
🛢️  **成品油价格调整公告**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 窗口期: {self.today} (第 {window_num} 个窗口)
📢 发布机构: 国家发改委
🕐 发布时间: {info['date']}

💵 调整内容:
"""
        if info['increase']:
            amount = info['amount'] or '???'
            output += f"  **汽油每吨上调 {amount} 元**\n"
            output += f"  **柴油每吨上调 {amount} 元**\n"
        elif info['decrease']:
            amount = info['amount'] or '???'
            output += f"  **汽油每吨下调 {amount} 元**\n"
            output += f"  **柴油每吨下调 {amount} 元**\n"
        else:
            output += "  价格调整信息待确认\n"

        output += f"""
📄 公告标题: {info['title']}
🔗 原文链接: {info['url']}

⚠️ 请以官方公报为准，本通知仅供参考。
"""
        return output.strip()

    def get_window_number(self) -> int:
        """计算当前是第几个窗口期"""
        windows = self.get_windows_for_year(self.today.year)
        for i, w in enumerate(windows, 1):
            if w == self.today:
                return i
        return 0

    def predict_next_year_windows(self, next_year: int) -> List[date]:
        """预测下一年度调价窗口（使用多搜索引擎或chinese-workdays推算）"""
        print(f"🔮 正在预测 {next_year} 年调价窗口期...")

        # 策略1: 使用 multi-search-engine 搜索官方通知
        try:
            windows = self.search_official_notice(next_year)
            if windows:
                print(f"✅ 找到 {next_year} 年官方通知，窗口期: {len(windows)} 个")
                return windows
        except Exception as e:
            print(f"⚠️  搜索失败: {e}")

        # 策略2: 使用 chinese-workdays 推算
        print(f"🔄 未找到官方通知，使用 chinese-workdays 推算...")
        return self.calculate_windows_by_workdays(next_year)

    def search_official_notice(self, year: int) -> Optional[List[date]]:
        """使用 multi-search-engine 搜索官方通知"""
        # 构建搜索查询
        query = f"国务院办公厅关于{year}年部分节假日安排的通知"

        try:
            # 调用 multi-search-engine (通过 subprocess)
            result = subprocess.run(
                ["python3", "-c", f"""
import subprocess, json, sys
# 模拟调用 search_utils (实际需要正确导入)
print("搜索: {{query}}")
# 这里应该调用实际的搜索模块
# 暂时返回空，依靠推算
"""],
                capture_output=True, text=True, timeout=30
            )

            # TODO: 解析搜索结果，提取官方链接，抓取并解析YAML数据
            # 由于实现复杂，暂时返回None，依靠推算
            return None

        except Exception as e:
            print(f"搜索异常: {e}")
            return None

    def calculate_windows_by_workdays(self, year: int) -> List[date]:
        """使用 chinese-workdays 推算调价窗口"""
        windows = []
        # 从起始日开始推算
        current = START_DATE
        while current.year <= year:
            if current.year == year:
                windows.append(current)
            # 每10个工作日
            current = self.add_workdays(current, WINDOW_INTERVAL)
            if current.year > year + 1:
                break
        return windows

    def check_and_predict_next_year(self):
        """检查是否需要预测下一年窗口"""
        windows_this_year = self.get_windows_for_year(self.today.year)
        if not windows_this_year:
            return

        last_window = windows_this_year[-1]
        # 如果今天是最后一个窗口期，触发预测
        if self.today == last_window:
            next_year = self.today.year + 1
            print(f"📅 今天是 {self.today.year} 年最后一个调价窗口，预测 {next_year} 年窗口期...")
            next_year_windows = self.predict_next_year_windows(next_year)
            # 更新缓存
            cache = self.load_windows_cache()
            cache["windows"][str(next_year)] = [d.isoformat() for d in next_year_windows]
            cache["last_updated"] = self.today.isoformat()
            self.save_windows_cache(cache)
            print(f"✅ 已预测并缓存 {next_year} 年 {len(next_year_windows)} 个窗口期")

    def run(self, force: bool = False) -> None:
        """主运行逻辑"""
        # 检查今天是否是窗口日
        if not force and not self.is_window_day():
            next_win = self.get_next_window()
            days_left = (next_win - self.today).days
            print(f"⏸️  今天不是成品油调价窗口期")
            print(f"   下一个调价窗口: {next_win} (还有 {days_left} 天)")
            print(f"   本次任务跳过，等待下次执行")
            return

        # 检查是否需要预测下一年
        self.check_and_predict_next_year()

        # 获取新闻
        news = self.fetch_ndrc_news()
        if not news:
            print("ℹ️  未获取到最新新闻，请稍后再试")
            return

        # 检测价格调整
        price_info = self.detect_price_change(news)
        window_num = self.get_window_number()

        if not price_info:
            print(f"ℹ️  今日新闻未发现成品油价格调整信息 (第{window_num}个窗口)")
            print(f"   已检查 {len(news)} 条最新公告")
            return

        # 输出通知
        print(self.format_output(price_info, window_num))

    def show_next_window(self):
        """显示下一个窗口期"""
        next_win = self.get_next_window()
        prev_win = self.get_previous_window()
        print(f"📅 调价窗口期计算")
        print(f"起始日期: {START_DATE}")
        print(f"间隔: 每 {WINDOW_INTERVAL} 个工作日")
        print(f"上一个窗口: {prev_win}")
        print(f"下一个窗口: {next_win}")
        print(f"今天: {self.today}")

        # 显示今年所有窗口
        windows_this_year = self.get_windows_for_year(self.today.year)
        print(f"\n📋 {self.today.year} 年调价窗口期 ({len(windows_this_year)} 个):")
        for i, w in enumerate(windows_this_year, 1):
            days_left = (w - self.today).days
            status = "✅ 已过" if w < self.today else ("🟡 今天" if w == self.today else f"⏳ {days_left}天后")
            print(f"  {i:2d}. {w} {status}")

    def show_recent_news(self):
        """显示最近新闻"""
        news = self.fetch_ndrc_news(limit=5)
        print(f"📰 最新 {len(news)} 条发改委新闻:")
        for i, item in enumerate(news, 1):
            print(f"{i}. [{item['date']}] {item['title']}")
            print(f"   链接: {item['url']}")


def main():
    monitor = OilPriceMonitor()

    args = sys.argv[1:]
    if '--test' in args or '-t' in args:
        monitor.run(force=True)
    elif '--next-window' in args or '-n' in args:
        monitor.show_next_window()
    elif '--recent' in args or '-r' in args:
        monitor.show_recent_news()
    else:
        monitor.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
实用新闻监控框架
专注于可工作的数据源和易扩展性
"""

import requests
import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

# 数据目录（默认位置，用户可修改）
DATA_DIR = os.path.expanduser("~/shared_memory/practical_news")

# 监控关键词
MONITOR_KEYWORDS = {
    'geopolitical': ['中东', '伊朗', '以色列', '巴勒斯坦', '加沙', '黎巴嫩', '也门', '叙利亚'],
    'oil': ['石油', '原油', '油价', 'OPEC', '欧佩克', 'WTI', '布伦特'],
    'gold': ['黄金', '贵金属', '避险', '金价'],
    'sanctions': ['制裁', '禁令', '限制', '封锁', '禁运'],
    'shipping': ['航运', '海运', '物流', '苏伊士', '红海', '霍尔木兹'],
    'conflict': ['冲突', '战争', '打击', '攻击', '炮击', '导弹', '军事']
}


class NewsDataSource:
    """新闻数据源基类"""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
        self.timeout = config.get('timeout', 15)

        # 请求headers（应对反爬虫）
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # 添加Referer（如果配置了）
        if 'referer' in config:
            self.headers['Referer'] = config['referer']

        # 自定义headers
        if 'headers' in config:
            self.headers.update(config['headers'])

    def fetch(self) -&gt; List[Dict[str, Any]]:
        """获取新闻数据（子类实现）"""
        raise NotImplementedError

    def check_relevance(self, title: str, keywords: Dict[str, List[str]]) -&gt; Dict[str, Any]:
        """检查新闻相关性"""
        title_lower = title.lower()

        found_keywords = []
        categories = []

        for category, words in keywords.items():
            for word in words:
                if word.lower() in title_lower:
                    found_keywords.append(word)
                    if category not in categories:
                        categories.append(category)

        return {
            'is_relevant': len(found_keywords) &gt; 0,
            'categories': categories,
            'keywords': found_keywords
        }


class JsonApiSource(NewsDataSource):
    """JSON API数据源"""

    def fetch(self) -&gt; List[Dict[str, Any]]:
        """获取JSON API数据"""
        if not self.enabled:
            return []

        url = self.config['url']
        data_path = self.config.get('data_path', '')

        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                news_items = []

                # 按路径提取数据列表
                if data_path:
                    items = data
                    for key in data_path.split('.'):
                        if isinstance(items, dict):
                            items = items.get(key, [])
                        else:
                            break
                else:
                    items = data if isinstance(data, list) else []

                # 配置字段映射
                title_field = self.config.get('title_field', 'title')
                url_field = self.config.get('url_field', 'url')
                time_field = self.config.get('time_field', 'time')

                for item in items[:self.config.get('limit', 20)]:
                    news_items.append({
                        'title': item.get(title_field, ''),
                        'link': item.get(url_field, ''),
                        'time': item.get(time_field, ''),
                        'source': self.name
                    })

                return news_items

            else:
                print(f"   ⚠️  HTTP {response.status_code}")
                return []

        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return []


class HtmlParseSource(NewsDataSource):
    """HTML解析数据源"""

    def fetch(self) -&gt; List[Dict[str, Any]]:
        """获取并解析HTML数据"""
        if not self.enabled:
            return []

        url = self.config['url']
        parse_rules = self.config.get('parse_rules', {})

        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)

            if response.status_code == 200:
                html = response.text
                news_items = []
                seen_titles = set()

                # 提取规则
                selectors = parse_rules.get('selectors', [])
                title_selector = parse_rules.get('title_selector', '')
                link_selector = parse_rules.get('link_selector', '')
                container_selector = parse_rules.get('container_selector', '')

                if container_selector:
                    # 先提取容器
                    containers = re.findall(container_selector, html, re.IGNORECASE | re.DOTALL)

                    for container in containers:
                        # 从容器中提取标题和链接
                        title_match = re.search(title_selector, container, re.IGNORECASE)
                        link_match = re.search(link_selector, container, re.IGNORECASE)

                        if title_match:
                            title = title_match.group(1) if title_match.groups() else title_match.group(0)
                            link = link_match.group(1) if link_match and link_match.groups() else ''

                            # 清理标题
                            title = re.sub(r'&lt;[^&gt;]+&gt;', '', title)
                            title = ' '.join(title.split())

                            # 过滤
                            if (len(title) &gt; 10 and len(title) &lt; 200 and
                                title not in seen_titles and
                                not any(skip in title.lower() for skip in ['登录', '注册', '广告', 'javascript:', '更多'])):
                                seen_titles.add(title)

                                # 处理相对链接
                                if link and not link.startswith('http'):
                                    from urllib.parse import urljoin
                                    link = urljoin(url, link)

                                news_items.append({
                                    'title': title,
                                    'link': link,
                                    'time': '',
                                    'source': self.name
                                })

                                if len(news_items) &gt;= self.config.get('limit', 20):
                                    break
                else:
                    # 直接提取
                    if title_selector:
                        title_matches = re.findall(title_selector, html, re.IGNORECASE | re.DOTALL)

                        for match in title_matches[:self.config.get('limit', 20)]:
                            if isinstance(match, tuple):
                                link, title = match[:2] if len(match) &gt;= 2 else ('', match[0])
                            else:
                                title = match
                                link = ''

                            # 清理标题
                            title = re.sub(r'&lt;[^&gt;]+&gt;', '', title)
                            title = ' '.join(title.split())

                            # 过滤
                            if (len(title) &gt; 10 and len(title) &lt; 200 and
                                title not in seen_titles and
                                not any(skip in title.lower() for skip in ['登录', '注册', '广告', 'javascript:', '更多'])):
                                seen_titles.add(title)

                                # 处理相对链接
                                if link and not link.startswith('http'):
                                    from urllib.parse import urljoin
                                    link = urljoin(url, link)

                                news_items.append({
                                    'title': title,
                                    'link': link,
                                    'time': '',
                                    'source': self.name
                                })

                return news_items

            else:
                print(f"   ⚠️  HTTP {response.status_code}")
                return []

        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return []


class PracticalMonitor:
    """实用新闻监控"""

    def __init__(self):
        self.sources = self._init_sources()

    def _init_sources(self) -&gt; List[NewsDataSource]:
        """初始化数据源"""
        sources = []

        # 数据源配置（这里只包含示例，实际使用时需要测试并启用可用的）
        source_configs = [
            {
                'type': 'json_api',
                'name': '新浪财经（示例）',
                'config': {
                    'enabled': False,  # 先禁用，测试后再启用
                    'url': 'http://finance.sina.com.cn/roll/finance.d.json',
                    'data_path': 'list',
                    'title_field': 'title',
                    'url_field': 'url',
                    'time_field': 'ctime',
                    'timeout': 15,
                    'limit': 20
                }
            },
            {
                'type': 'html_parse',
                'name': '东方财富（示例）',
                'config': {
                    'enabled': False,
                    'url': 'http://finance.eastmoney.com/a/cjkzzzz.html',
                    'parse_rules': {
                        'title_selector': r'&lt;a[^&gt;]*href="([^"]*\.shtml)"[^&gt;]*&gt;([^&lt;]+)&lt;/a&gt;'
                    },
                    'timeout': 15,
                    'limit': 20
                }
            }
        ]

        for source_config in source_configs:
            try:
                if source_config['type'] == 'json_api':
                    source = JsonApiSource(source_config['name'], source_config['config'])
                elif source_config['type'] == 'html_parse':
                    source = HtmlParseSource(source_config['name'], source_config['config'])
                else:
                    continue

                sources.append(source)

            except Exception as e:
                print(f"⚠️  初始化数据源失败 {source_config['name']}: {e}")

        return sources

    def monitor(self) -&gt; Dict[str, Any]:
        """监控所有数据源"""
        print("=" * 60)
        print("📊 实用新闻监控")
        print("=" * 60)
        print(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        all_news = []
        source_stats = defaultdict(lambda: {'total': 0, 'relevant': 0})

        for source in self.sources:
            print(f"📡 正在获取 {source.name}...")

            try:
                news_items = source.fetch()

                # 检查相关性
                for item in news_items:
                    relevance = source.check_relevance(item['title'], MONITOR_KEYWORDS)

                    item['is_relevant'] = relevance['is_relevant']
                    item['categories'] = relevance['categories']
                    item['found_keywords'] = relevance['keywords']

                    source_stats[source.name]['total'] += 1
                    if relevance['is_relevant']:
                        source_stats[source.name]['relevant'] += 1

                    all_news.append(item)

                print(f"   ✓ 获取到 {len(news_items)} 条新闻")

            except Exception as e:
                print(f"   ❌ 失败: {e}")

        print()
        print(f"✅ 共获取 {len(all_news)} 条新闻")

        relevant_news = [n for n in all_news if n.get('is_relevant', False)]
        print(f"📈 相关新闻: {len(relevant_news)} 条")
        print()

        # 来源统计
        print("📊 来源统计:")
        for source, stats in sorted(source_stats.items(), key=lambda x: -x[1]['total']):
            print(f"  {source}: {stats['relevant']}/{stats['total']} 相关")

        return {
            'all_news': all_news,
            'relevant_news': relevant_news,
            'source_stats': dict(source_stats)
        }


def save_monitor_data(monitor_data: Dict[str, Any]) -&gt; str:
    """保存监控数据"""
    os.makedirs(DATA_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    filename = f"{DATA_DIR}/monitor_{timestamp}.json"

    data = {
        'monitor_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'timestamp': timestamp,
        'total_count': len(monitor_data['all_news']),
        'relevant_count': len(monitor_data['relevant_news']),
        'all_news': monitor_data['all_news'],
        'relevant_news': monitor_data['relevant_news'],
        'source_stats': monitor_data['source_stats']
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print()
    print(f"💾 数据已保存: {filename}")

    return filename


def generate_summary_report(monitor_data: Dict[str, Any]) -&gt; str:
    """生成摘要报告"""
    report_lines = [
        "# 新闻监控摘要报告",
        f"\n**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**总新闻数**: {len(monitor_data['all_news'])}",
        f"**相关新闻**: {len(monitor_data['relevant_news'])}",
        "\n---\n",
        "## 来源统计",
        ""
    ]

    for source, stats in monitor_data['source_stats'].items():
        report_lines.append(f"- {source}: {stats['relevant']}/{stats['total']} 相关")

    if monitor_data['relevant_news']:
        report_lines.extend([
            "\n---\n",
            "## 相关新闻",
            ""
        ])

        for i, item in enumerate(monitor_data['relevant_news'][:15], 1):
            categories_str = ', '.join(item.get('categories', []))
            report_lines.append(f"{i}. **{item['source']}**: {item['title'][:80]}...")
            if categories_str:
                report_lines.append(f"   类别: {categories_str}")

    report_lines.extend([
        "\n---\n",
        "*报告由Zbot自动生成*"
    ])

    return '\n'.join(report_lines)


def main():
    """主函数"""
    import sys

    action = sys.argv[1] if len(sys.argv) &gt; 1 else 'monitor'

    monitor = PracticalMonitor()

    if action == 'monitor':
        # 监控模式
        monitor_data = monitor.monitor()
        save_monitor_data(monitor_data)

        # 生成摘要报告
        report = generate_summary_report(monitor_data)

        print()
        print(report)

        print()
        print("✅ 监控完成")

    elif action == 'test':
        # 测试模式
        print("🧪 测试数据源连接...")
        print()
        print("⚠️  当前所有数据源已禁用，需要手动测试并启用可用的数据源")
        print()
        print("💡 使用说明:")
        print("1. 编辑本脚本，找到 source_configs")
        print("2. 测试每个数据源的URL是否可访问")
        print("3. 将 'enabled': False 改为 'enabled': True'")
        print("4. 重新运行测试")
        print()
        print("数据源类型:")
        print("- json_api: 适用于JSON格式的API")
        print("- html_parse: 适用于需要解析HTML的网站")
        print()
        print("已配置的数据源:")
        for source in monitor.sources:
            status = "✓ 已启用" if source.enabled else "✗ 已禁用"
            print(f"  - {source.name}: {status}")


if __name__ == '__main__':
    main()

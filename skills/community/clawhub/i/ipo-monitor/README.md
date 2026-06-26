# IPO监控技能 V2 设计方案

## 一、数据字段清单

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| company_name | string | ✅ | 公司名称 | 深圳市英科瑞科技股份有限公司 |
| stock_code | string | ✅ | 股票代码 | 688598 |
| exchange | string | ✅ | 交易所/板块 | 科创板/港股主板/NYSE |
| application_status | string | ✅ | 审核状态 | 已受理/提交注册/注册生效/上市 |
| expected_date | string | ❌ | 预计上市日期 | 2026-04-15 |
| fundraising_amount | string | ❌ | 募集金额 | 8.5亿元 |
| issue_price_range | string | ❌ | 发行价区间 | 52-68元 |
| update_time | datetime | ✅ | 更新时间 | 2026-03-17 14:30:00 |
| source_url | string | ✅ | 原文链接 | https://example.com/ipo/xxx |
| source | string | ✅ | 数据来源 | 证监会/港交所/NYSE |
| last_check_time | datetime | ✅ | 最后检查时间 | 2026-03-17 15:00:00 |

---

## 二、技术架构

```
IPO监控V2/
├── config.yaml                 # 主配置文件
├── config.py                   # 配置加载模块
├── requirements.txt           # Python依赖
├── main.py                    # 入口脚本
├── README.md                  # 使用文档
├── SKILL.md                   # 技能定义
├── BROWSER_MIGRATION.md       # 浏览器迁移文档
├── SCHEDULER.md               # 定时任务配置
├── logs/                      # 日志目录
│   └── ipo_monitor.log
├── data/                      # 数据目录
│   ├── ipo_cache.db           # SQLite本地缓存
│   └── last_run.json          # 上次运行状态
├── scrapers/                  # 抓取模块
│   ├── __init__.py
│   ├── base.py                # 基类（超时、重试）
│   ├── browser_fetcher.py     # 浏览器抓取器（核心，使用OpenClaw browser）
│   ├── browser_scraper.py     # 浏览器抓取辅助
│   ├── browser_scrapers.py    # 各交易所浏览器抓取实现
│   ├── csrc_scraper.py        # 证监会（A股）
│   ├── hkex_scraper.py        # 港交所
│   ├── nyse_scraper.py        # 纽交所
│   ├── nasdaq_scraper.py      # 纳斯达克
│   ├── sse_scraper.py         # 上交所
│   ├── szse_scraper.py        # 深交所
│   └── bse_scraper.py         # 北交所
├── storage/                   # 存储层
│   ├── __init__.py
│   ├── sqlite_storage.py       # SQLite本地备份
│   └── feishu_pusher.py        # 飞书推送
├── utils/                     # 工具函数
│   ├── __init__.py
│   ├── deduplicator.py         # 去重工具
│   ├── diff_engine.py          # 差异计算引擎
│   └── date_utils.py           # 日期工具
├── tests/                     # 测试
│   ├── test_scraper.py
│   └── test_parse.py
└── browser_test.py            # 浏览器测试脚本
```

---

## 三、核心代码逻辑

### 3.1 浏览器抓取器 (scrapers/browser_fetcher.py)

这是V2版本的核心模块，使用OpenClaw浏览器工具抓取动态页面：

```python
class BrowserFetcher:
    """使用浏览器抓取IPO数据"""
    
    EXCHANGES = {
        "上交所": "https://www.sse.com.cn/listing/renewal/ipo/",
        "深交所": "https://www.szse.cn/listing/projectdynamic/ipo/",
        "北交所": "https://www.bse.cn/audit/project_news.html",
        "港股新上市": "https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities",
        "港股申请": "https://www.hkexnews.hk/app/appindex.html",
        "纳斯达克": "https://www.nasdaq.com/market-activity/ipos",
        "纽交所": "https://www.nyse.com/ipo-center/ipo-calendar",
    }
    
    def fetch(self, browser, exchange: str) -> List[Dict]:
        # 使用OpenClaw浏览器打开页面
        # 等待加载完成后提取数据
        # 根据交易所类型调用不同的解析方法
        ...
```

### 3.2 港股解析（正则表达式）

```python
def _parse_hkex_app(self, text: str) -> List[Dict]:
    """解析港股申请页面 - 使用正则表达式提取结构化数据"""
    
    # 港股申请页面字段：
    # - 公司名称
    # - 股票代码 (4-5位数字)
    # - 发布日期 (YYYY-MM-DD 或 DD/MM/YYYY)
    # - 公告类型 (OC Announcement, Application Proof, 招股书, etc.)
    
    # 模式1: 股票代码 + 公司名 + 日期 + 公告类型
    pattern1 = re.compile(
        r'(\d{4,5})\s+([^\d\n]{2,50})\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(OC\s*Announcement|Application\s*Proof|招股说明书|上市申请)',
        re.MULTILINE | re.IGNORECASE
    )
    ...
```

### 3.3 纳斯达克解析（正则表达式）

```python
def _parse_nasdaq(self, text: str) -> List[Dict]:
    """解析纳斯达克IPO页面 - 使用正则表达式提取结构化数据"""
    
    # 纳斯达克页面字段：
    # - Symbol代码 (股票代码，如 AAPL)
    # - 公司名称
    # - 发行价
    # - 股数
    # - 上市日期
    # - 募集金额
    
    # 模式1: Symbol + 公司名 + 发行价 + 股数 + 日期 + 募集金额
    pattern1 = re.compile(
        r'([A-Z]{1,5})\s+([^\$#\n]{3,80})\s+\$?([\d,.]+)\s*(?:M|m|Million)?\s+(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:M|m)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\s+\$?([\d,.]+)\s*(?:B|b|M|m)?',
        re.MULTILINE | re.IGNORECASE
    )
    ...
```

```python
#!/usr/bin/env python3
"""
IPO监控技能 V2 - 主入口
功能：每日自动抓取IPO数据，对比差异，推送飞书
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import Config
from scrapers.csrc_scraper import CSRCScraper
from scrapers.hkex_scraper import HKEXScraper
from scrapers.nyse_scraper import NYSEScraper
from storage.sqlite_storage import SQLiteStorage
from storage.feishu_pusher import FeishuPusher
from utils.deduplicator import Deduplicator
from utils.diff_engine import DiffEngine


class IPOMonitorV2:
    def __init__(self):
        self.config = Config()
        self.logger = self._setup_logging()
        self.storage = SQLiteStorage(self.config.db_path)
        self.deduplicator = Deduplicator()
        self.pusher = FeishuPusher(self.config)
        
        # 初始化各交易所抓取器
        self.scrapers = {
            'A股-科创板': CSRCScraper(self.config, '科创板'),
            'A股-主板': CSRCScraper(self.config, '主板'),
            '港股': HKEXScraper(self.config),
            '美股-NYSE': NYSEScraper(self.config),
        }
    
    def run(self):
        """主运行逻辑"""
        self.logger.info("=" * 50)
        self.logger.info(f"IPO监控 V2 启动 - {datetime.now()}")
        
        all_new_data = {}
        
        # 1. 遍历各交易所抓取数据
        for name, scraper in self.scrapers.items():
            try:
                self.logger.info(f"正在抓取: {name}")
                data = scraper.fetch()
                all_new_data[name] = data
                self.logger.info(f"{name} - 获取 {len(data)} 条记录")
            except Exception as e:
                self.logger.error(f"{name} 抓取失败: {e}")
                all_new_data[name] = []
        
        # 2. 获取上次数据，进行对比
        old_data = self.storage.load_all()
        
        # 3. 计算差异
        diff_engine = DiffEngine()
        changes = diff_engine.compute_diff(old_data, all_new_data)
        
        # 4. 保存新数据
        self.storage.save_all(all_new_data)
        
        # 5. 推送变化
        if changes['has_changes']:
            self.pusher.send_daily_report(changes)
            self.logger.info("推送成功")
        else:
            self.logger.info("无新变化，跳过推送")
        
        self.logger.info(f"IPO监控 V2 完成 - {datetime.now()}")


if __name__ == '__main__':
    monitor = IPOMonitorV2()
    monitor.run()
```

### 3.2 基类 - 超时重试机制 (scrapers/base.py)

```python
#!/usr/bin/env python3
"""
抓取器基类 - 提供超时、重试、反爬等通用能力
"""
import time
import random
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper(ABC):
    """抓取器基类"""
    
    # 默认请求头，模拟浏览器
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    def __init__(self, config, exchange: str):
        self.config = config
        self.exchange = exchange
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """创建带重试机制的Session"""
        session = requests.Session()
        
        # 配置重试策略：指数退避
        retry_strategy = Retry(
            total=3,                    # 最多重试3次
            backoff_factor=2,            # 退避因子：2秒、4秒、8秒
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def fetch_with_retry(self, url: str, timeout: int = 30) -> Optional[requests.Response]:
        """
        带重试的请求
        
        Args:
            url: 请求URL
            timeout: 超时时间（秒）
        
        Returns:
            Response对象或None
        """
        # 随机延迟，反爬
        time.sleep(random.uniform(1, 3))
        
        try:
            response = self.session.get(
                url,
                headers=self.DEFAULT_HEADERS,
                timeout=timeout
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.Timeout:
            self.logger.warning(f"请求超时: {url}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求失败: {url}, 错误: {e}")
            return None
    
    @abstractmethod
    def fetch(self) -> List[Dict]:
        """
        抓取数据（子类实现）
        
        Returns:
            IPO数据列表
        """
        pass
    
    def wait_for_load(self, selector: str, timeout: int = 10):
        """等待页面加载完成（可选，使用Selenium时）"""
        # 简化实现，实际可用Selenium
        time.sleep(2)
```

### 3.3 证监会抓取器 (scrapers/csrc_scraper.py)

```python
#!/usr/bin/env python3
"""
证监会IPO抓取器 - A股科创板/主板
数据来源: 证监会官网
"""
from typing import List, Dict
from datetime import datetime
from bs4 import BeautifulSoup

from scrapers.base import BaseScraper


class CSRCScraper(BaseScraper):
    """证监会IPO抓取器"""
    
    # 证监会IPO公示页面
    URLS = {
        '科创板': 'https://www.csrc.gov.cn/ccczbjgs/xxf/xxfb/gsgg/',
        '主板': 'https://www.csrc.gov.cn/ccczbjgs/xxf/xxfb/gsgg/',
    }
    
    def fetch(self) -> List[Dict]:
        """抓取A股IPO数据"""
        url = self.URLS.get(self.exchange, self.URLS['科创板'])
        response = self.fetch_with_retry(url)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # 这里需要根据实际页面结构调整选择器
        # 示例：根据表格行解析
        for row in soup.select('table.ipo-table tr')[1:]:  # 跳过表头
            cols = row.find_all('td')
            if len(cols) < 5:
                continue
            
            ipo_info = {
                'company_name': self._clean_text(cols[0].get_text()),
                'stock_code': self._clean_text(cols[1].get_text()),
                'exchange': self.exchange,
                'application_status': self._clean_text(cols[2].get_text()),
                'expected_date': self._extract_date(cols[3].get_text()),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': self._get_full_url(cols[0].find('a')['href']),
                'source': '证监会',
            }
            
            results.append(ipo_info)
        
        return results
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        return text.strip().replace('\n', '').replace('\r', '')
    
    def _extract_date(self, text: str) -> str:
        """提取日期"""
        import re
        match = re.search(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?', text)
        if match:
            return match.group().replace('年', '-').replace('月', '-').replace('日', '')
        return ''
    
    def _get_full_url(self, path: str) -> str:
        """补全URL"""
        base = 'https://www.csrc.gov.cn'
        return path if path.startswith('http') else base + path
```

### 3.4 港交所抓取器 (scrapers/hkex_scraper.py)

```python
#!/usr/bin/env python3
"""
港交所IPO抓取器
数据来源: 港交所披露易
"""
from typing import List, Dict
from datetime import datetime
import json
import re

from scrapers.base import BaseScraper


class HKEXScraper(BaseScraper):
    """港交所IPO抓取器"""
    
    # 港交所新股上市申请
    URL = 'https://www.hkex.com.hk/eng/services/trading/stock-dev/ipo/IPOList.htm'
    
    # API端点（如果有）
    API_URL = 'https://www.hkex.com.hk/eng/services/trading/stock-dev/ipo/ippindex.html'
    
    def fetch(self) -> List[Dict]:
        """抓取港股IPO数据"""
        response = self.fetch_with_retry(self.API_URL)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析港股IPO数据"""
        results = []
        
        # 尝试从页面提取JSON数据
        # 实际需根据页面结构调整
        pattern = r'IPO\s*:\s*(\[.*?\]);'
        match = re.search(pattern, html, re.DOTALL)
        
        if match:
            try:
                ipo_data = json.loads(match.group(1))
                for item in ipo_data:
                    ipo_info = {
                        'company_name': item.get('name_cn', item.get('name_en', '')),
                        'stock_code': item.get('stock_code', ''),
                        'exchange': '港股主板',
                        'application_status': item.get('listing_stage', '上市申请'),
                        'expected_date': item.get('expected_date', ''),
                        'fundraising_amount': item.get('fundraising', ''),
                        'issue_price_range': item.get('price_range', ''),
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'source_url': f"https://www.hkex.com.hk/eng/invest/company/profile_page_e.asp?WidCoID={item.get('stock_code', '')}",
                        'source': '港交所',
                    }
                    results.append(ipo_info)
            except json.JSONDecodeError:
                pass
        
        return results
```

### 3.5 纽交所抓取器 (scrapers/nyse_scraper.py)

```python
#!/usr/bin/env python3
"""
纽交所IPO抓取器
数据来源: NYSE IPO Center
"""
from typing import List, Dict
from datetime import datetime
import json

from scrapers.base import BaseScraper


class NYSEScraper(BaseScraper):
    """纽交所IPO抓取器"""
    
    URL = 'https://www.nyse.com/ipo-center/ipo-calendar'
    
    def fetch(self) -> List[Dict]:
        """抓取NYSE IPO数据"""
        response = self.fetch_with_retry(self.URL)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析NYSE IPO数据"""
        results = []
        
        # NYSE页面通常有结构化数据
        # 需要根据实际页面调整解析逻辑
        # 示例：提取日历表格
        import re
        
        # 尝试提取JSON数据
        json_pattern = r'window\.IPO_DATA\s*=\s*(\[.*?\]);'
        match = re.search(json_pattern, html, re.DOTALL)
        
        if match:
            try:
                ipo_list = json.loads(match.group(1))
                for item in ipo_list:
                    ipo_info = {
                        'company_name': item.get('companyName', ''),
                        'stock_code': item.get('symbol', ''),
                        'exchange': 'NYSE',
                        'application_status': item.get('status', 'Upcoming'),
                        'expected_date': item.get('expectedDate', ''),
                        'fundraising_amount': item.get('offerAmount', ''),
                        'issue_price_range': item.get('priceRange', ''),
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'source_url': f"https://www.nyse.com/ipo-center/ipo-profile/{item.get('symbol', '')}",
                        'source': 'NYSE',
                    }
                    results.append(ipo_info)
            except (json.JSONDecodeError, KeyError):
                pass
        
        return results
```

### 3.6 去重工具 (utils/deduplicator.py)

```python
#!/usr/bin/env python3
"""
去重工具 - 基于股票代码+交易所唯一键
"""
from typing import List, Dict, Set


class Deduplicator:
    """去重器"""
    
    @staticmethod
    def deduplicate(ipo_list: List[Dict]) -> List[Dict]:
        """
        去重
        
        规则：同一交易所下，股票代码唯一
        """
        seen: Set[str] = set()
        result = []
        
        for ipo in ipo_list:
            # 生成唯一键：交易所_股票代码
            key = f"{ipo.get('exchange', '')}_{ipo.get('stock_code', '')}"
            
            if key and key not in seen:
                seen.add(key)
                result.append(ipo)
        
        return result
    
    @staticmethod
    def merge_lists(lists: List[List[Dict]]) -> List[Dict]:
        """合并多个列表并去重"""
        all_data = []
        for lst in lists:
            all_data.extend(lst)
        return Deduplicator.deduplicate(all_data)
```

### 3.7 差异计算引擎 (utils/diff_engine.py)

```python
#!/usr/bin/env python3
"""
差异计算引擎 - 对比新旧数据，判断新增/更新
"""
from typing import Dict, List, Any
from datetime import datetime


class DiffEngine:
    """差异计算引擎"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def compute_diff(self, old_data: Dict[str, List[Dict]], new_data: Dict[str, List[Dict]]) -> Dict:
        """
        计算差异
        
        Args:
            old_data: 上次数据 {'板块名': [IPO列表]}
            new_data: 新数据 {'板块名': [IPO列表]}
        
        Returns:
            差异报告
        """
        result = {
            'has_changes': False,
            'added': [],      # 新增
            'updated': [],    # 更新
            'removed': [],   # 删除（下市/撤回）
            'summary': {},
        }
        
        # 遍历各板块
        for exchange, new_list in new_data.items():
            old_list = old_data.get(exchange, [])
            
            # 构建旧数据索引
            old_index = {item['stock_code']: item for item in old_list if item.get('stock_code')}
            
            added_count = 0
            updated_count = 0
            
            for new_item in new_list:
                stock_code = new_item.get('stock_code')
                
                if stock_code not in old_index:
                    # 新增
                    new_item['change_type'] = '新增'
                    new_item['change_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result['added'].append({
                        'exchange': exchange,
                        'data': new_item
                    })
                    added_count += 1
                else:
                    old_item = old_index[stock_code]
                    # 检查是否有更新
                    if self._has_update(old_item, new_item):
                        new_item['change_type'] = '更新'
                        new_item['change_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        new_item['old_status'] = old_item.get('application_status')
                        result['updated'].append({
                            'exchange': exchange,
                            'data': new_item
                        })
                        updated_count += 1
            
            result['summary'][exchange] = {
                'added': added_count,
                'updated': updated_count,
                'total': len(new_list)
            }
        
        # 检查删除（旧数据中有，新数据中没有）
        for exchange, old_list in old_data.items():
            new_list = new_data.get(exchange, [])
            new_codes = {item['stock_code'] for item in new_list if item.get('stock_code')}
            
            for old_item in old_list:
                stock_code = old_item.get('stock_code')
                if stock_code and stock_code not in new_codes:
                    old_item['change_type'] = '删除'
                    result['removed'].append({
                        'exchange': exchange,
                        'data': old_item
                    })
        
        # 判断是否有变化
        result['has_changes'] = bool(result['added'] or result['updated'] or result['removed'])
        
        return result
    
    def _has_update(self, old_item: Dict, new_item: Dict) -> bool:
        """检查是否有实质更新"""
        # 比较关键字段
        fields_to_check = ['application_status', 'expected_date', 'fundraising_amount', 'issue_price_range']
        
        for field in fields_to_check:
            old_val = old_item.get(field, '')
            new_val = new_item.get(field, '')
            if old_val != new_val:
                return True
        
        return False
```

### 3.8 飞书推送 (storage/feishu_pusher.py)

```python
#!/usr/bin/env python3
"""
飞书推送模块
"""
import requests
from datetime import datetime
from typing import Dict


class FeishuPusher:
    """飞书推送"""
    
    def __init__(self, config):
        self.config = config
        self.webhook = config.feishu_webhook
        self.logger = logging.getLogger(__name__)
    
    def send_daily_report(self, changes: Dict):
        """发送日报"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 构建消息
        message = self._build_message(changes, date)
        
        self._send(message)
    
    def _build_message(self, changes: Dict, date: str) -> str:
        """构建消息内容"""
        lines = []
        lines.append(f"📈 IPO监控日报 ({date})")
        lines.append("")
        
        summary = changes.get('summary', {})
        
        # 按板块分组
        added_by_exchange = {}
        updated_by_exchange = {}
        
        for item in changes.get('added', []):
            ex = item['exchange']
            added_by_exchange.setdefault(ex, []).append(item['data'])
        
        for item in changes.get('updated', []):
            ex = item['exchange']
            updated_by_exchange.setdefault(ex, []).append(item['data'])
        
        # 输出新增
        for exchange, items in added_by_exchange.items():
            lines.append(f"【{exchange}】新增 {len(items)} 家")
            for i, item in enumerate(items, 1):
                name = item.get('company_name', '')
                code = item.get('stock_code', '')
                status = item.get('application_status', '')
                url = item.get('source_url', '')
                
                # 格式化名称（过长截断）
                if len(name) > 20:
                    name = name[:18] + '...'
                
                lines.append(f"  {i}. {name} ({code}) - {status}")
                if url:
                    lines.append(f"     [查看原文]({url})")
            lines.append("")
        
        # 输出更新
        for exchange, items in updated_by_exchange.items():
            lines.append(f"【{exchange}】更新 {len(items)} 家")
            for item in items:
                name = item.get('company_name', '')
                code = item.get('stock_code', '')
                old_status = item.get('old_status', '')
                new_status = item.get('application_status', '')
                url = item.get('source_url', '')
                
                if len(name) > 20:
                    name = name[:18] + '...'
                
                lines.append(f"  • {name} ({code})")
                lines.append(f"    {old_status} → {new_status}")
                if url:
                    lines.append(f"    [查看原文]({url})")
            lines.append("")
        
        # 汇总
        total_added = sum(s.get('added', 0) for s in summary.values())
        total_updated = sum(s.get('updated', 0) for s in summary.values())
        
        lines.append(f"📊 共计：新增 {total_added} 家 | 更新 {total_updated} 家")
        
        return "\n".join(lines)
    
    def _send(self, message: str):
        """发送飞书消息"""
        url = self.webhook
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                self.logger.info("飞书消息发送成功")
            else:
                self.logger.error(f"飞书消息发送失败: {response.text}")
        except Exception as e:
            self.logger.error(f"飞书消息发送异常: {e}")
```

---

## 四、配置文件模板 (config.yaml)

```yaml
# IPO监控 V2 配置文件

# 飞书配置
feishu:
  webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  mention_ids: []  # 需要@的用户ID，可选

# 抓取配置
scraper:
  # 请求超时（秒）
  timeout: 30
  
  # 重试次数
  max_retries: 3
  
  # 请求间隔（秒）
  min_delay: 1
  max_delay: 3
  
  # User-Agent
  user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# 监控范围（可灵活配置）
monitor:
  exchanges:
    - name: "A股-科创板"
      enabled: true
      url: "https://www.csrc.gov.cn/ccczbjgs/xxf/xxfb/gsgg/"
    - name: "A股-主板"
      enabled: true
      url: "https://www.csrc.gov.cn/ccczbjgs/xxf/xxfb/gsgg/"
    - name: "港股"
      enabled: true
      url: "https://www.hkex.com.hk/eng/services/trading/stock-dev/ipo/ippindex.html"
    - name: "美股-NYSE"
      enabled: true
      url: "https://www.nyse.com/ipo-center/ipo-calendar"
    - name: "美股-NASDAQ"
      enabled: false
      url: "https://www.nasdaq.com/market-activity/ipos"

# 数据存储
storage:
  # 本地SQLite路径
  db_path: "./data/ipo_cache.db"
  
  # 备份保留天数
  backup_days: 30

# 日志配置
logging:
  level: "INFO"
  file: "./logs/ipo_monitor.log"
  max_bytes: 10485760  # 10MB
  backup_count: 5
```

---

## 五、错误处理方案

### 5.1 错误分类与处理

| 错误类型 | 处理策略 | 重试次数 |
|----------|----------|----------|
| 网络超时 | 指数退避重试 | 3次 |
| 403/429反爬 | 等待后重试 + 更换UA | 5次 |
| 页面解析失败 | 记录日志，跳过该条 | 0次 |
| 飞书推送失败 | 记录日志 + 告警 | 3次 |
| 数据库写入失败 | 回滚 + 重试 | 3次 |

### 5.2 核心错误处理代码

```python
# 在 base.py 中
def fetch_with_retry(self, url: str, timeout: int = 30) -> Optional[Response]:
    """带重试的请求 - 指数退避"""
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 随机延迟
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=timeout)
            
            # 反爬处理
            if response.status_code == 403:
                self.logger.warning(f"403 Forbidden，尝试更换UA")
                self._rotate_user_agent()
                retry_count += 1
                continue
                
            if response.status_code == 429:
                # 限流，等待更长时间
                wait_time = 60 * (retry_count + 1)
                self.logger.warning(f"429 Rate Limited，等待 {wait_time}秒")
                time.sleep(wait_time)
                retry_count += 1
                continue
                
            response.raise_for_status()
            return response
            
        except requests.exceptions.Timeout:
            retry_count += 1
            self.logger.warning(f"超时，第{retry_count}次重试")
            
        except requests.exceptions.RequestException as e:
            retry_count += 1
            self.logger.error(f"请求异常: {e}")
    
    self.logger.error(f"重试{max_retries}次后仍失败: {url}")
    return None
```

### 5.3 日志记录

```python
# 日志格式
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('./logs/ipo_monitor.log'),
        logging.StreamHandler()
    ]
)

# 关键日志点
logger.info("开始抓取 {exchange}")
logger.info("抓取成功，获取 {count} 条数据")
logger.info("发现 {added} 新增，{updated} 更新")
logger.warning("抓取失败: {error}")
logger.error("推送失败: {error}")
```

---

## 六、发布清单

### 6.1 开发任务

- [ ] 创建项目目录结构
- [ ] 实现 config.yaml 配置加载
- [ ] 实现 BaseScraper 基类
- [ ] 实现 CSRCScraper（A股）
- [ ] 实现 HKEXScraper（港股）
- [ ] 实现 NYSEScraper（纽交所）
- [ ] 实现 SQLiteStorage 本地存储
- [ ] 实现 FeishuPusher 推送
- [ ] 实现 Deduplicator 去重
- [ ] 实现 DiffEngine 差异计算
- [ ] 实现 main.py 入口
- [ ] 编写 README.md 文档

### 6.2 测试任务

- [ ] 单元测试：去重逻辑
- [ ] 单元测试：差异计算
- [ ] 集成测试：各抓取器
- [ ] 手动测试：飞书推送
- [ ] 压力测试：连续运行

### 6.3 部署任务

- [ ] 部署到 OpenClaw
- [ ] 配置 Cron 定时任务（每日14:00）
- [ ] 配置监控告警

### 6.4 后续优化

- [ ] 增加 NASDAQ 监控
- [ ] 增加美股 OTC 市场
- [ ] 支持自定义数据源
- [ ] 支持邮件通知
- [ ] 支持数据导出 Excel

---

## 七、数据源参考

| 市场 | 网站 | URL |
|------|------|-----|
| A股-证监会 | 证监会官网 | https://www.csrc.gov.cn |
| 港股 | 港交所披露易 | https://www.hkex.com.hk |
| 美股-NYSE | NYSE IPO Center | https://www.nyse.com/ipo-center |
| 美股-NASDAQ | NASDAQ IPO | https://www.nasdaq.com/market-activity/ipos |
| 美股-OTC | OTC Markets | https://www.otcmarkets.com |

---

*版本: V2.0*
*更新日期: 2026-03-17*

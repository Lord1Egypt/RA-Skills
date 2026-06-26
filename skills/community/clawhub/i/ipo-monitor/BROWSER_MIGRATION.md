# IPO监控 V2 - 浏览器抓取重写说明

## 已完成的修改

### 1. ✅ 修复告警冷却逻辑
**文件**: `scrapers/base.py`

```python
# 修改前 (错误)
if elapsed >= cooldown:
    self._failure_count = 1  # 重置为1

# 修改后 (正确)
if elapsed >= cooldown:
    self._failure_count = 0  # 清零
```

### 2. ✅ 创建浏览器抓取模块
**新文件**: `scrapers/browser_fetcher.py`

提供了 `BrowserFetcher` 类，使用真实浏览器方式抓取：

```python
from scrapers.browser_fetcher import BrowserFetcher

fetcher = BrowserFetcher(config)
data = fetcher.fetch(browser, "上交所")  # browser是OpenClaw的browser工具
```

### 3. ✅ 创建浏览器Scraper基类
**新文件**: `scrapers/browser_scraper.py`

提供了 `BrowserScraper` 基类，子类只需实现 `parse()` 方法：

```python
class SSEBrowserScraper(BrowserScraper):
    @property
    def url(self):
        return "https://www.sse.com.cn/listing/renewal/ipo/"
    
    @property
    def name(self):
        return "上交所"
    
    def parse(self, snapshot):
        # 解析snapshot，返回IPO数据列表
        pass
```

### 4. ✅ 解析方法测试通过
**测试文件**: `test_parse.py`

验证了从HTML表格解析数据的方法正确。

---

## 浏览器抓取工作流程

### 方式1: 直接使用 BrowserFetcher
```python
from scrapers.browser_fetcher import BrowserFetcher
from storage.sqlite_storage import SQLiteStorage
from storage.feishu_pusher import FeishuPusher
from utils.deduplicator import Deduplicator
from utils.diff_engine import DiffEngine
from config import Config

# 初始化
config = Config()
fetcher = BrowserFetcher(config)
storage = SQLiteStorage(config.db_path)
pusher = FeishuPusher(config)
deduplicator = Deduplicator()
diff_engine = DiffEngine()

# 抓取数据（需要传入browser工具）
all_data = {}
for exchange in ["上交所", "深交所", "北交所"]:
    data = fetcher.fetch(browser, exchange)  # browser是OpenClaw的browser实例
    data = deduplicator.deduplicate(data)
    all_data[exchange] = data

# 对比和推送
old_data = storage.load_all()
changes = diff_engine.compute_diff(old_data, all_data)
storage.save_all(all_data)

if changes['has_changes']:
    pusher.send_daily_report(changes)
```

### 方式2: 继承 BrowserScraper
```python
class MyExchangeScraper(BrowserScraper):
    @property
    def url(self):
        return "https://example.com/ipo/"
    
    @property
    def name(self):
        return "我的交易所"
    
    def parse(self, snapshot):
        # 1. 获取HTML
        html = self.browser.action(
            action="act",
            targetId=self.tab_id,
            request={"kind": "evaluate", "fn": "document.querySelector('table').outerHTML"}
        )
        
        # 2. 解析HTML
        soup = BeautifulSoup(html['result'], 'html.parser')
        # ... 解析逻辑
        return results
```

---

## 使用URL（已确认可用）

```python
EXCHANGES = {
    "上交所": "https://www.sse.com.cn/listing/renewal/ipo/",
    "深交所": "https://www.szse.cn/listing/projectdynamic/ipo/",
    "北交所": "https://www.bse.cn/audit/project_news.html",
    "港股新上市": "https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities",
    "港股申请": "https://www.hkexnews.hk/app/appindex.html",
    "纳斯达克": "https://www.nasdaq.com/market-activity/ipos",
    "纽交所": "https://www.nyse.com/ipo-center/ipo-calendar",
}
```

---

## 测试方法

```bash
# 1. 解析测试
cd /Users/eurus/.openclaw/workspace/ipo-monitor-v2
python3 test_parse.py

# 2. 浏览器抓取测试（在OpenClaw中）
# 使用browser工具打开页面，然后获取snapshot
```

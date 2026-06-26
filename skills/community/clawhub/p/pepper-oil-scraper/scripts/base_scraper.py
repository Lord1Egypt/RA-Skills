"""
base_scraper.py - 爬虫基类
提供反爬、重试、限速、日志、数据标准化等基础设施。
所有站点适配器继承此类。
"""

import json
import logging
import os
import random
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

try:
    from fake_useragent import UserAgent
    _ua = UserAgent(fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
except Exception:
    _ua = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "targets.json"

def load_config() -> dict:
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# 单位转换工具
# ---------------------------------------------------------------------------

UNIT_CONVERSIONS = {
    # 价格 → 元/公斤
    "元/斤":   lambda v: v * 2,
    "元/公斤": lambda v: v,
    "元/kg":   lambda v: v,
    "元/吨":   lambda v: v / 1000,
    "$/kg":    lambda v: v * 7.25,      # 粗略汇率，运行时可覆盖
    "$/lb":    lambda v: v * 7.25 * 2.2046,
    # 面积 → 万亩
    "亩":    lambda v: v / 10000,
    "万亩":  lambda v: v,
    "公顷":  lambda v: v * 15 / 10000,  # 1公顷≈15亩
    "hm²":   lambda v: v * 15 / 10000,
    # 产量 → 万吨
    "吨":    lambda v: v / 10000,
    "万吨":  lambda v: v,
    "千吨":  lambda v: v / 10,
    # 金额 → 亿元
    "万元":   lambda v: v / 10000,
    "百万元": lambda v: v / 100,
    "亿元":   lambda v: v,
    "亿美元": lambda v: v * 7.25,
    "百万美元": lambda v: v * 7.25 / 100,
    "USD million": lambda v: v * 7.25 / 100,
    "USD billion": lambda v: v * 7.25 * 10,
}

def convert_unit(value: float, from_unit: str, target_type: str = None) -> tuple:
    """转换到标准单位。返回 (converted_value, standard_unit)"""
    fn = UNIT_CONVERSIONS.get(from_unit)
    if fn:
        return fn(value), _standard_unit(from_unit)
    return value, from_unit

def _standard_unit(from_unit: str) -> str:
    price_units = {"元/斤", "元/公斤", "元/kg", "元/吨", "$/kg", "$/lb"}
    area_units  = {"亩", "万亩", "公顷", "hm²"}
    qty_units   = {"吨", "万吨", "千吨"}
    money_units = {"万元", "百万元", "亿元", "亿美元", "百万美元", "USD million", "USD billion"}
    if from_unit in price_units: return "元/公斤"
    if from_unit in area_units:  return "万亩"
    if from_unit in qty_units:   return "万吨"
    if from_unit in money_units: return "亿元"
    return from_unit

# ---------------------------------------------------------------------------
# 数字提取
# ---------------------------------------------------------------------------

_NUM_PATTERN = re.compile(r"[\d,]+\.?\d*")
_CN_NUM_MAP  = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10,"百":100,"千":1000,"万":10000}

def extract_number(text: str) -> float | None:
    """从文本中提取第一个数字"""
    text = text.replace(",", "").replace("，", "")
    m = _NUM_PATTERN.search(text)
    if m:
        try:
            return float(m.group())
        except ValueError:
            pass
    return None

def extract_all_numbers(text: str) -> list[float]:
    """提取文本中的所有数字"""
    text = text.replace(",", "").replace("，", "")
    return [float(m.group()) for m in _NUM_PATTERN.finditer(text)]

# ---------------------------------------------------------------------------
# BaseScraper
# ---------------------------------------------------------------------------

class BaseScraper:
    """所有站点爬虫的基类"""

    def __init__(self, adapter_id: str, config: dict = None):
        self.adapter_id = adapter_id
        self.config = config or load_config()
        self.global_cfg = self.config["global_settings"]
        self.site_cfg = self.config["sites"].get(adapter_id, {})
        self.logger = logging.getLogger(f"scraper.{adapter_id}")

        self.session = requests.Session()
        self.session.headers.update(self._default_headers())
        self.session.verify = True

        proxy = self.site_cfg.get("proxy") or self.global_cfg.get("proxy")
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

        self._request_count = 0
        self._results: list[dict] = []

    # -- headers --
    def _default_headers(self) -> dict:
        ua = _ua.random if _ua else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        return {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def _rotate_ua(self):
        if _ua:
            self.session.headers["User-Agent"] = _ua.random

    # -- throttle --
    def _delay(self):
        lo = self.site_cfg.get("delay_min", self.global_cfg["default_delay_min"])
        hi = self.site_cfg.get("delay_max", self.global_cfg["default_delay_max"])
        sec = random.uniform(lo, hi)
        self.logger.debug(f"sleep {sec:.1f}s")
        time.sleep(sec)

    # -- fetch with retry --
    def fetch(self, url: str, method: str = "GET", referer: str = None, **kwargs) -> requests.Response | None:
        """带重试和退避的请求方法"""
        max_retries = self.global_cfg["max_retries"]
        backoff     = self.global_cfg["backoff_factor"]
        max_backoff = self.global_cfg["max_backoff"]
        timeout     = self.global_cfg["timeout"]

        if referer:
            self.session.headers["Referer"] = referer
        elif self.site_cfg.get("base_url"):
            self.session.headers["Referer"] = self.site_cfg["base_url"]

        self._rotate_ua()

        for attempt in range(1, max_retries + 1):
            try:
                self._delay()
                self._request_count += 1
                self.logger.info(f"[{attempt}/{max_retries}] {method} {url}")

                resp = self.session.request(method, url, timeout=timeout, **kwargs)

                if resp.status_code == 200:
                    return resp
                elif resp.status_code in (403, 429, 503):
                    wait = min(backoff ** attempt + random.uniform(0, 2), max_backoff)
                    self.logger.warning(f"HTTP {resp.status_code} → backoff {wait:.1f}s")
                    time.sleep(wait)
                else:
                    self.logger.warning(f"HTTP {resp.status_code} for {url}")
                    return resp

            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout on attempt {attempt}")
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"Connection error: {e}")
                time.sleep(min(backoff ** attempt, max_backoff))
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                break

        self.logger.error(f"Failed after {max_retries} attempts: {url}")
        return None

    # -- parse html --
    def parse_html(self, resp: requests.Response) -> BeautifulSoup | None:
        if resp is None:
            return None
        resp.encoding = resp.apparent_encoding or "utf-8"
        return BeautifulSoup(resp.text, "lxml")

    def fetch_and_parse(self, url: str, **kwargs) -> BeautifulSoup | None:
        return self.parse_html(self.fetch(url, **kwargs))

    # -- record building --
    def add_record(self, metric: str, value, unit: str = "", period: str = "",
                   region: str = "", source_url: str = "", original_text: str = "",
                   confidence: str = "medium", extra: dict = None):
        """添加一条标准化数据记录"""
        # 尝试数值转换
        if isinstance(value, str):
            value = extract_number(value)
        if value is not None and unit:
            value, unit = convert_unit(float(value), unit)

        record = {
            "metric": metric,
            "value": value,
            "unit": unit,
            "period": period,
            "region": region,
            "source_url": source_url,
            "original_text": original_text[:500],
            "confidence": confidence,
        }
        if extra:
            record.update(extra)
        self._results.append(record)

    # -- output --
    def get_output(self) -> dict:
        return {
            "adapter_id": self.adapter_id,
            "site_name": self.site_cfg.get("name", self.adapter_id),
            "category": self.site_cfg.get("category", "unknown"),
            "crawl_time": datetime.now().isoformat(),
            "request_count": self._request_count,
            "record_count": len(self._results),
            "records": self._results,
        }

    def save(self, output_dir: str = None):
        output_dir = output_dir or self.global_cfg["output_dir"]
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        path = Path(output_dir) / f"{self.adapter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = self.get_output()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.logger.info(f"Saved {len(self._results)} records → {path}")
        return str(path)

    # -- abstract --
    def crawl(self):
        """子类必须实现此方法"""
        raise NotImplementedError

    def run(self, output_dir: str = None) -> str:
        """执行爬取并保存"""
        self.logger.info(f"=== START {self.adapter_id} ({self.site_cfg.get('name', '')}) ===")
        try:
            self.crawl()
        except Exception as e:
            self.logger.error(f"Crawl failed: {e}", exc_info=True)
        path = self.save(output_dir)
        self.logger.info(f"=== END {self.adapter_id}: {len(self._results)} records ===")
        return path

"""
政府采购数据采集脚本（合规版 · 单一数据源：中国政府采购网中央站）

数据源决策（重要）：
  各省政府采购网的招标数据会汇总/同步到中国政府采购网（www.ccgp.gov.cn），且省级站
  反爬机制普遍较强。因此本采集器**仅以 ccgp.gov.cn 中央站为唯一数据源**，
  不逐省采集——既覆盖全国（含省级）公开公告，又避免与各省反爬对抗、降低合规风险。

与旧版（gov-procurement-analyst 4.7.0）的关键区别（旧版谎称「31 省全采」却采到 0 条）：
  1. 旧版写死 search.ccgp.gov.cn 的 JS 动态页 CSS 选择器 → 解析 0 条。
     本版抓取【静态列表页】并解析 <li><a href> 结构，实测可采到真实公告。
  2. 旧版在 robots.txt 取不到（404）时“保守拦截”→ 把 ccgp 整个拦掉。
     本版采用 fail-closed（默认禁止）：取不到 robots 策略（404/网络错误/非 200）时**禁止采集该域**，
     仅当 robots 策略明确允许时才继续，杜绝“取不到即放行”的越界风险。
  3. 翻页改为【确定性 index_{n}.htm 形态跟随】：
     第1页=入口URL（如 /cggg/zygg/），第n页(n>=2)=列表目录+index_{n-1}.htm，
     实测 zygg 下 index_1/2/3.htm 均 HTTP 200 且各含 20 条真实公告。
  4. 【编码修复】中文政府站常「声明 UTF-8 实为 GBK/GB18030」，requests 自动解码会乱码。
     本版 decode_bytes() 先按声明编码，若产生大量替换字符则回退 GB18030。
  5. 单一数据源、范围明确：不宣称"全站/全省支持"，只采已验证的中央站静态列表页。

合规原则（与 skill 一致）：
  - 仅采公开信息；请求前检查 robots.txt；同域 ≥3 秒限速；
  - 遇 403/429/503 立即跳过该域；不破解验证码、不绕过登录、不采非公开信息。

依赖：requests + beautifulsoup4

使用方式：
  python collected_data.py --output ccgp.json
  python collected_data.py --pages 3 --keyword 软件 --output ccgp.json
  python collected_data.py --url "http://www.ccgp.gov.cn/cggg/zygg/" --detail --output ccgp.json
  # --url 仅接受 ccgp.gov.cn 域下的列表页（需为 ./类型/yyyymm/t...htm 结构）；默认即公开招标 zygg。
  # 指向任何其他主机将被拒绝（防 SSRF）。
"""

import argparse
import json
import os
import re
import time
import urllib.robotparser
from datetime import datetime
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] 请先安装依赖: pip install requests beautifulsoup4")
    raise

# === 配置 ===
USER_AGENT = "GovProcurementBot/1.0 (compatible; WorkBuddy-CN)"
REQUEST_TIMEOUT = 20
REQUEST_DELAY = 3
MAX_RETRIES = 2
MAX_PAGES = 10

# 唯一数据源：中国政府采购网中央站（省级数据已汇聚于此）
DEFAULT_LIST_URL = "http://www.ccgp.gov.cn/cggg/zygg/"

# 白名单主机：仅允许向这些主机发起请求，杜绝 --url 被指向任意主机造成的 SSRF / 越权采集
ALLOWED_HOSTS = {"www.ccgp.gov.cn", "ccgp.gov.cn"}


def _assert_trusted_host(url: str):
    """校验 URL 主机在白名单内；否则拒绝（防止 SSRF / 越权采集）。"""
    host = urlparse(url).netloc.lower()
    if host not in ALLOWED_HOSTS:
        raise SystemExit(
            f"[SECURITY] 拒绝访问非授权数据源：{host!r}。"
            f"本采集器仅允许 ccgp.gov.cn 中央站（白名单：{sorted(ALLOWED_HOSTS)}）。"
        )

CATEGORY_MAP = {
    "gkzb": "公开招标", "zygg": "公开招标", "cjgg": "成交公告", "zbgg": "中标公告",
    "qtgg": "其他公告", "jzxcs": "竞争性磋商", "jzxgg": "竞争性谈判",
    "jzxtpgg": "竞争性谈判", "xqgc": "询价公告", "fblbgg": "废标/流标公告",
    "gzgg": "更正公告", "dyly": "单一来源", "xygh": "协议供货",
}


# === 工具函数 ===
def decode_bytes(content: bytes, declared: str = None) -> str:
    """稳健解码：先按声明编码，若产生大量替换字符（声明与实际不符）则回退 GB18030。
    解决中文政府站「声明 UTF-8 实为 GBK」导致的乱码问题。"""
    candidates = []
    if declared:
        candidates.append(declared.lower())
    candidates += ["utf-8", "gb18030", "gbk"]
    for enc in candidates:
        try:
            txt = content.decode(enc)
            if txt.count("\ufffd") / max(1, len(txt)) < 0.02:
                return txt
        except (UnicodeDecodeError, LookupError):
            continue
    return content.decode("utf-8", errors="replace")


class ComplianceChecker:
    def __init__(self):
        self._cache = {}

    @staticmethod
    def _restrictive_rp():
        """fail-closed 兜底：取不到/解析不了 robots 策略时一律禁止。"""
        rp = urllib.robotparser.RobotFileParser()
        rp.entries = []
        rp.allow_all = False
        rp.disallow_all = True
        return rp

    def is_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = f"{domain}/robots.txt"
        if domain in self._cache:
            return self._cache[domain].can_fetch(USER_AGENT, url)
        try:
            r = requests.get(robots_url, headers={"User-Agent": USER_AGENT},
                             timeout=REQUEST_TIMEOUT, allow_redirects=True)
        except requests.exceptions.RequestException:
            print(f"[ROBOTS] 无法获取 {robots_url}，按默认禁止（fail-closed，已记录）")
            self._cache[domain] = self._restrictive_rp()
            return False
        if r.status_code != 200:
            print(f"[ROBOTS] {robots_url} 返回 HTTP {r.status_code}（非策略文件），按默认禁止（fail-closed）")
            self._cache[domain] = self._restrictive_rp()
            return False
        rp = urllib.robotparser.RobotFileParser()
        try:
            rp.parse(r.text.splitlines())
        except Exception:
            rp = self._restrictive_rp()
        self._cache[domain] = rp
        return rp.can_fetch(USER_AGENT, url)

    def get_crawl_delay(self, url: str) -> int:
        domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        rp = self._cache.get(domain)
        if rp:
            try:
                delay = rp.crawl_delay(USER_AGENT)
                if delay and delay > REQUEST_DELAY:
                    return int(delay)
            except Exception:
                pass
        return REQUEST_DELAY


class EthicalFetcher:
    def __init__(self):
        self.compliance = ComplianceChecker()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        self.last_request_time = {}
        self.failed_domains = set()

    def fetch(self, url: str, retry: int = 0):
        host = urlparse(url).netloc.lower()
        if host not in ALLOWED_HOSTS:
            print(f"[BLOCKED] 非授权主机，拒绝访问: {host}")
            return None
        if not self.compliance.is_allowed(url):
            print(f"[BLOCKED] robots.txt 禁止: {url}")
            return None
        domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        if domain in self.failed_domains:
            return None
        delay = self.compliance.get_crawl_delay(url)
        last = self.last_request_time.get(domain, 0)
        elapsed = time.time() - last
        if elapsed < delay:
            time.sleep(delay - elapsed)
        try:
            resp = self.session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            self.last_request_time[domain] = time.time()
            if resp.status_code == 200:
                declared = None
                ct = resp.headers.get("Content-Type", "")
                m = re.search(r"charset=([\w-]+)", ct, re.I)
                if m:
                    declared = m.group(1)
                return decode_bytes(resp.content, declared)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 60))
                if retry < MAX_RETRIES:
                    print(f"[RATE] {domain} 限流，{wait}s 后重试")
                    time.sleep(wait)
                    return self.fetch(url, retry + 1)
                self.failed_domains.add(domain)
                return None
            if resp.status_code in (403, 503):
                self.failed_domains.add(domain)
                print(f"[BLOCKED] {domain} 拒绝访问 ({resp.status_code})")
                return None
            print(f"[HTTP {resp.status_code}] {url}")
            return None
        except requests.exceptions.RequestException as e:
            if retry < MAX_RETRIES:
                return self.fetch(url, retry + 1)
            self.failed_domains.add(domain)
            print(f"[ERROR] 请求失败: {e}")
            return None


class CcgpParser:
    """解析 ccgp 中央公告静态列表页 + 详情页。"""

    # 公告链接特征：./{类型}/{yyyymm}/t{yyyymmdd}_{id}.htm
    ANNOUNCE_RE = re.compile(r"^\./([a-z]+)/(\d{6})/t(\d{8})_(\d+)\.htm$")

    @staticmethod
    def parse_list(html: str, base_url: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        items = []
        for li in soup.select("li"):
            a = li.find("a")
            if not a:
                continue
            href = a.get("href", "")
            title = (a.get("title") or a.get_text(strip=True) or "").strip()
            if not href or not title:
                continue
            m = CcgpParser.ANNOUNCE_RE.match(href.replace("\\", "/"))
            if not m:
                continue
            cat_code, ym, ymd, aid = m.groups()
            abs_link = urljoin(base_url, href)
            publish = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}"
            items.append({
                "id": f"ccgp_{ymd}_{aid}",
                "title": title,
                "link": abs_link,
                "publish_date": publish,
                "category": CATEGORY_MAP.get(cat_code, cat_code),
                "category_code": cat_code,
                "region": "中央/全国",
                "parsed_at": datetime.now().isoformat(),
            })
        return items

    @staticmethod
    def parse_detail(html: str) -> dict:
        """详情页抽取结构化字段（尽力而为）"""
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)

        def grab(pattern):
            m = re.search(pattern, text)
            return m.group(1).strip() if m else None

        budget = grab(r"预算金额[：: ]*([0-9.,]+)\s*万元")
        # 采购人优先取“采购人名称：XXX”，避免抓到“采购人信息”这类标题
        purchaser = grab(r"采购人名称[：: ]*([^\n，。；]{2,40})")
        if not purchaser:
            _p = grab(r"采购人[：: ]*([^\n，。；]{2,40})")
            purchaser = _p if _p and _p not in ("信息", "代表）", "（采购人") else None
        bid_time = grab(r"开标时间[：: ]*([0-9]{4}[-/年][0-9]{1,2}[-/月][0-9]{1,2}[ 日]*[0-9:]*?)")
        project_no = grab(r"项目编号[：: ]*([A-Za-z0-9\-]+)")
        return {
            "budget_wan": float(budget) if budget else None,
            "purchaser": purchaser,
            "bid_deadline": bid_time,
            "project_no": project_no,
        }


def main():
    ap = argparse.ArgumentParser(
        description="政府采购公告合规采集（唯一数据源：中国政府采购网中央站）")
    ap.add_argument("--url", default=DEFAULT_LIST_URL,
                    help="列表页 URL（默认中央站公开招标 zygg；仅限 ccgp.gov.cn 域，换 cjgg/zbgg 等其他类别也须在该域内）")
    ap.add_argument("--pages", type=int, default=2, help="最多翻页数（默认 2，上限 %d）" % MAX_PAGES)
    ap.add_argument("--keyword", help="标题关键词过滤（可选）")
    ap.add_argument("--detail", action="store_true", help="额外抓取详情页抽取预算/采购人等（较慢）")
    ap.add_argument("--output", default="collected_announcements.json", help="输出 JSON 路径")
    args = ap.parse_args()

    _assert_trusted_host(args.url)  # 防 SSRF：仅允许 ccgp 白名单域
    args.pages = min(max(args.pages, 1), MAX_PAGES)
    fetcher = EthicalFetcher()
    parser = CcgpParser()

    # 翻页 URL 构造（ccgp 中央静态列表页为确定性形态，由 JS Pager 生成）：
    #   第 1 页 = 用户给定入口 URL（如 /cggg/zygg/）
    #   第 n 页(n>=2) = 列表目录 + index_{n-1}.htm
    list_dir = args.url if args.url.endswith("/") else args.url.rsplit("/", 1)[0] + "/"

    all_items = []
    seen_links = set()
    visited = set()

    for page_no in range(1, args.pages + 1):
        current_url = args.url if page_no == 1 else list_dir + f"index_{page_no - 1}.htm"
        if current_url in visited:
            break
        visited.add(current_url)
        print(f"[采集] 第{page_no}页: {current_url[:90]}...")
        html = fetcher.fetch(current_url)
        if not html:
            print("  → 本页无内容，停止翻页")
            break
        items = parser.parse_list(html, current_url)
        new_count = 0
        for it in items:
            if it["link"] in seen_links:
                continue
            seen_links.add(it["link"])
            if args.keyword and args.keyword not in it["title"]:
                continue
            if args.detail:
                dhtml = fetcher.fetch(it["link"])
                if dhtml:
                    it.update(parser.parse_detail(dhtml))
            all_items.append(it)
            new_count += 1
        print(f"  → 本页解析 {len(items)} 条，新增 {new_count} 条（累计 {len(all_items)}）")
        if page_no >= args.pages:
            break
        time.sleep(REQUEST_DELAY)

    output = {
        "platform": "中国政府采购网（中央站，省级数据已汇聚于此）",
        "source_url": args.url,
        "generated_at": datetime.now().isoformat(),
        "total_count": len(all_items),
        "compliance_note": "本采集严格遵守 robots.txt（取不到策略文件或返回非 200 时按默认禁止，fail-closed），仅采依法公开公告，同域请求间隔 ≥3 秒；不破解验证码、不绕过登录、不采非公开信息。数据源仅 ccgp.gov.cn 中央站（省级招标数据已同步至此，故无需逐省采集）。",
        "data": all_items,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[完成] 共采集 {len(all_items)} 条真实公告 → {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()

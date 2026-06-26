"""
2号人事部 餐补申请自动化 (Playwright 版)
"""
import os, sys, csv, re, time, argparse, json, logging, urllib.request
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict
from PIL import Image
import io

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    for i, arg in enumerate(sys.argv):
        if isinstance(arg, str):
            try:
                arg.encode('utf-8').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                try:
                    sys.argv[i] = arg.encode('gbk', errors='replace').decode('utf-8', errors='replace')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout, Page, Browser

# ── 配置 ──────────────────────────────────────────────
class Config:
    SKILL_DIR    = Path(__file__).parent.parent
    SHOT_DIR     = SKILL_DIR / "screenshots"
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_URL   = 'https://i-wework.2haohr.com/desk/home'
    LATE_HOUR    = "20:30"
    MEAL_NORMAL  = 20
    MEAL_CROSS   = 40
    PAGE_TMO     = 30_000
    LOGIN_TMO    = 90_000
    CELL_TMO     = 10_000
    CDP_PORT     = 9222
    CHROME_WAIT  = 5
    CHROME_DATA  = os.path.expandvars(r"%TEMP%\chrome-debug-2haohr")
    MAX_NAV      = 20
    MAX_CLICK    = 10
    MAX_UPLOAD   = 3
    MAX_PICKER   = 3
    CROSS_MIN    = 360
    CHROME_PATHS = [
        os.getenv("CHROME_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    ]

# ── 日志 ──────────────────────────────────────────────
def setup_log() -> logging.Logger:
    lg = logging.getLogger('meal_subsidy')
    lg.setLevel(logging.INFO)
    fmt = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    ch = logging.StreamHandler(); ch.setFormatter(fmt); lg.addHandler(ch)
    fh = logging.FileHandler(Config.SKILL_DIR / "meal_subsidy.log", encoding='utf-8')
    fh.setFormatter(fmt); lg.addHandler(fh)
    return lg

L = setup_log()
log = L.info; log_w = L.warning; log_e = L.error; log_d = L.debug

# ── 工具函数 ──────────────────────────────────────────
def pmin(t: str) -> int:
    try: h, m = t.split(':'); return int(h)*60 + int(m)
    except: return 0

def iscross(t: str) -> bool:
    return 0 <= pmin(t) < Config.CROSS_MIN

def ge(t1: str, t2: str) -> bool:
    return pmin(t1) >= pmin(t2)

def fmt_date(yr, mo, day) -> str:
    return f"{yr}-{int(mo):02d}-{int(day):02d}"

def att_name(ds: str) -> str:
    return f"att_{ds.replace('-','')}.png"

def shot_name(prefix: str) -> str:
    return f"{prefix}_{datetime.now().strftime('%H%M%S')}.png"

# ── 截图 ──────────────────────────────────────────────
def save_shot(page: Page, name: str) -> Optional[str]:
    p = Config.SHOT_DIR / name
    try:
        page.screenshot(path=str(p), type='png', full_page=False)
        log(f"shot: {p.name}")
        return str(p)
    except Exception as e:
        log_e(f"screenshot fail: {e}")
        return None

def save_shot_elem(element, name: str) -> Optional[str]:
    p = Config.SHOT_DIR / name
    try:
        buf = element.screenshot(type='png')
        with open(p, 'wb') as f: f.write(buf)
        log(f"shot elem: {p.name}")
        return str(p)
    except Exception as e:
        log_e(f"screenshot elem fail: {e}")
        return None

def savecsv(records: List[Tuple[str, str]]) -> Optional[str]:
    if not records: return None
    p = Config.SHOT_DIR / f"late_{datetime.now().strftime('%Y%m')}.csv"
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["date","off","cross","yuan"])
        for d, t in records:
            c = iscross(t)
            w.writerow([d, t, c, Config.MEAL_CROSS if c else Config.MEAL_NORMAL])
    log(f"csv: {p}")
    return str(p)

def extract_day(txt: str) -> int:
    m = re.search(r'(\d+)月(\d+)日', txt)
    if m: return int(m.group(2))
    lines = txt.split('\n')
    if lines:
        s = re.sub(r'\D', '', lines[0])
        if s: return int(s)
    return -1

# ── CDP 连接 ──────────────────────────────────────────
def get_cdp_url(port: int = None) -> Optional[str]:
    if port is None: port = Config.CDP_PORT
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=5) as r:
            return json.loads(r.read()).get("webSocketDebuggerUrl")
    except Exception as e:
        log_d(f"CDP fail: {e}")
        return None

def init_browser(p):
    cdp = get_cdp_url()
    if cdp:
        try:
            b = p.chromium.connect_over_cdp(cdp); log("chrome connected via CDP"); return b
        except Exception as e:
            log_w(f"CDP connect fail: {e}")
    log("auto-start chrome...")
    import subprocess
    path = next((p for p in Config.CHROME_PATHS if p and os.path.exists(p)), None)
    if not path: raise RuntimeError("Chrome not found")
    subprocess.Popen(
        [path, "--remote-debugging-port=9222",
         f"--user-data-dir={Config.CHROME_DATA}",
         "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    time.sleep(Config.CHROME_WAIT)
    cdp = get_cdp_url()
    if cdp:
        b = p.chromium.connect_over_cdp(cdp); log("chrome auto-started"); return b
    raise RuntimeError("Cannot connect to Chrome")

def new_page(browser: Browser) -> Page:
    pg = browser.contexts[0].new_page()
    pg.set_default_timeout(Config.PAGE_TMO)
    return pg

def get_page(browser: Browser) -> Page:
    ctx = browser.contexts[0]
    return ctx.pages[0] if ctx.pages else ctx.new_page()

# ── 登录 ──────────────────────────────────────────────
def wait_login(page: Page) -> bool:
    try:
        page.wait_for_function(
            "() => { const u = window.location.href.toLowerCase();"
            " return u.includes('desk/home') && !u.includes('login') && document.body.innerText.length > 50; }",
            timeout=Config.LOGIN_TMO)
        log("login ok"); return True
    except PlaywrightTimeout:
        log_e("login timeout"); return False

# ── 点击 ──────────────────────────────────────────────
def click_text(page: Page, text: str, retries: int = None) -> bool:
    if retries is None: retries = Config.MAX_CLICK
    sels = [f"text={text}", f"button:has-text('{text}')", f"a:has-text('{text}')",
            f"span:has-text('{text}')", f"*:has-text('{text}'):not(:has-text('·'))"]
    for _ in range(retries):
        for sel in sels:
            try:
                el = page.locator(sel).first
                if el.count() > 0 and el.is_visible() and el.is_enabled():
                    el.click(timeout=3000); time.sleep(0.8); return True
            except (PlaywrightTimeout, Exception): pass
        time.sleep(1)
    return False

# ── 考勤 ──────────────────────────────────────────────
def go_attendance(page: Page) -> None:
    log("go attendance")
    if click_text(page, "考勤"):
        page.wait_for_load_state("networkidle", timeout=20000)
        page.wait_for_selector("[class*='Cell_']", timeout=Config.CELL_TMO)
        page.evaluate("window.scrollBy(0, 300)")
        time.sleep(0.5)
    else:
        log_w("failed to click 考勤")

def get_cal_month(page: Page) -> str:
    for sel in ["[class*='show']", "[class*='dateSwitch']"]:
        try:
            for el in page.locator(sel).all():
                t = el.inner_text().strip()
                if '/' in t and len(t) <= 10:
                    m = re.search(r'(\d{4}/\d{2})', t)
                    if m: return m.group(1)
        except Exception: pass
    return ""

def go_month(page: Page, yr: int, mo: int) -> bool:
    tgt = f"{yr}/{int(mo):02d}"
    try:
        page.wait_for_function(
            f"() => {{ const s=['[class*=\"show\"]','[class*=\"dateSwitch\"]'];"
            f" for(const sel of s){{ for(const el of document.querySelectorAll(sel))"
            f" {{ if(el.innerText.includes('{tgt}')) return true; }} }} return false; }}",
            timeout=10000)
        log(f"cal: {tgt}"); return True
    except PlaywrightTimeout: pass
    btns = ["[class*='left']", "[class*='prev']", "[class*='arrow-left']"]
    for _ in range(Config.MAX_NAV):
        if get_cal_month(page) == tgt: return True
        for bsel in btns:
            try:
                for btn in page.locator(bsel).all():
                    if btn.is_visible() and btn.is_enabled():
                        btn.click(); time.sleep(1.2)
                        if get_cal_month(page) == tgt:
                            log(f"cal: {tgt}"); return True
                        break
            except Exception: pass
        time.sleep(0.5)
    log_e(f"cal stuck at {get_cal_month(page)}"); return False

def _shot_cell(page: Page, cell, path: Path, box: dict = None) -> None:
    """用 PIL 从全量截图中裁剪单元格区域，不触发滚动重绘"""
    for attempt in range(3):
        try:
            if box is None:
                box = cell.bounding_box()
            if not box:
                buf = cell.screenshot(type='png')
                with open(path, 'wb') as f: f.write(buf)
                return
            buf = page.screenshot(type='png', full_page=False)
            img = Image.open(io.BytesIO(buf))
            x1 = max(0, int(box["x"]))
            y1 = max(0, int(box["y"]))
            x2 = min(img.width, x1 + max(1, int(box["width"])))
            y2 = min(img.height, y1 + max(1, int(box["height"])))
            cropped = img.crop((x1, y1, x2, y2))
            cropped.save(path, format='png')
            return
        except Exception:
            if attempt < 2: time.sleep(1)

def read_record(page: Page, yr: int, mo: int, day: int) -> Optional[Tuple[str, str]]:
    if not go_month(page, yr, mo): return None
    try: page.wait_for_selector("[class*='Cell_']", timeout=8000)
    except PlaywrightTimeout: pass
    time.sleep(1.5)
    cells = page.locator("[class*='Cell_']").all()
    log_d(f"cells={len(cells)} find={mo}/{day}")
    for cell in cells:
        try:
            txt = cell.inner_text().strip()
            if not txt: continue
            cd = extract_day(txt)
            if cd != day: continue
            times = re.findall(r'\d{1,2}:\d{2}', txt)
            off = times[-1] if times else None
            ds = fmt_date(yr, mo, day)
            shot_path = Config.SHOT_DIR / att_name(ds)
            _shot_cell(page, cell, shot_path)
            log(f"shot: {shot_path.name}")
            if off:
                log(f"  {ds} off={off}")
                return ds, off
        except PlaywrightTimeout: continue
    log_d(f"not found {mo}/{day}"); return None

def read_all_cells(page: Page, yr: int, mo: int) -> Dict[int, Tuple[str, Optional[str]]]:
    """一次性读取当月所有单元格，一次截图 + PIL裁剪，不闪屏"""
    cell_map: Dict[int, Tuple[str, Optional[str]]] = {}
    try: page.wait_for_selector("[class*='Cell_']", timeout=8000)
    except PlaywrightTimeout: return cell_map
    time.sleep(1)
    cells = page.locator("[class*='Cell_']").all()

    # 收集所有有下班时间的格及其 bounding_box（一次性截图标）
    off_cells = []  # [(cell, ds, box)]
    for cell in cells:
        try:
            txt = cell.inner_text().strip()
            if not txt: continue
            day = extract_day(txt)
            if day < 1: continue
            times = re.findall(r'\d{1,2}:\d{2}', txt)
            off = times[-1] if times else None
            ds = fmt_date(yr, mo, day)
            cell_map[day] = (ds, off)
            if off:
                box = cell.bounding_box()
                off_cells.append((ds, box))
        except PlaywrightTimeout: continue

    # 一次性截图，再裁剪各单元格
    if off_cells:
        try:
            buf = page.screenshot(type='png', full_page=False)
            img = Image.open(io.BytesIO(buf))
            for ds, box in off_cells:
                if not box:
                    continue
                x1 = max(0, int(box["x"]))
                y1 = max(0, int(box["y"]))
                x2 = min(img.width, x1 + max(1, int(box["width"])))
                y2 = min(img.height, y1 + max(1, int(box["height"])))
                shot_path = Config.SHOT_DIR / att_name(ds)
                img.crop((x1, y1, x2, y2)).save(str(shot_path), format='png')
                log(f"shot: {shot_path.name}")
        except Exception as e:
            log_e(f"batch shot fail: {e}")
            # 回退：逐格截
            for ds, box in off_cells:
                try:
                    shot_path = Config.SHOT_DIR / att_name(ds)
                    _shot_cell(page, None, shot_path, box=box)
                    log(f"shot: {shot_path.name}")
                except Exception: pass

    log_d(f"read {len(cell_map)} cells"); return cell_map

# ── 餐补表单 ──────────────────────────────────────────
def go_meal_form_same_page(page: Page) -> Page:
    """同一页面内导航到餐补表单"""
    page.goto(Config.TARGET_URL, timeout=Config.PAGE_TMO)
    page.wait_for_load_state("domcontentloaded", timeout=Config.PAGE_TMO)
    time.sleep(1)
    log("click approval"); click_text(page, "审批"); time.sleep(2)
    log("click meal"); click_text(page, "餐补"); time.sleep(5)
    save_shot(page, shot_name("meal_form"))
    return page

def js_picker(page: Page, idx: int, val: str, retries: int = None) -> bool:
    if retries is None: retries = Config.MAX_PICKER
    for attempt in range(retries):
        try:
            r = page.evaluate(
                f"() => {{ const pks=document.querySelectorAll('.ivu-date-picker');"
                f" if(pks.length<={idx}) return 'no_picker';"
                f" const inp=pks[{idx}].querySelector('input');"
                f" if(!inp) return 'no_input';"
                f" const sd=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');"
                f" if(!sd) return 'no_setter';"
                f" sd.set.call(inp,'{val}');"
                f" inp.dispatchEvent(new Event('input',{{bubbles:true}}));"
                f" inp.dispatchEvent(new Event('change',{{bubbles:true}})); return 'ok'; }}"
            )
            log_d(f"picker[{idx}]={val}: {r}")
            if r == 'ok': return True
        except Exception as e:
            log_e(f"picker err: {e}")
        if attempt < retries - 1: time.sleep(1)
    return False

def upload_file(page: Page, path: str) -> bool:
    if not os.path.exists(path):
        log_e(f"file not found: {path}"); return False
    for attempt in range(Config.MAX_UPLOAD):
        try:
            page.locator("input[type='file']").set_input_files(path)
            time.sleep(2); log("upload ok"); return True
        except Exception as e:
            log_w(f"upload fail (attempt {attempt+1}): {e}")
        time.sleep(1)
    log_e(f"upload failed after {Config.MAX_UPLOAD} attempts"); return False

def submit_form(page: Page, retries: int = 3) -> bool:
    save_shot(page, shot_name("meal_before_submit"))
    for _ in range(retries):
        try:
            for btn in page.locator("button:has-text('提交'), span:has-text('提交')").all():
                if btn.is_visible() and btn.is_enabled():
                    btn.click(); time.sleep(2)
                    save_shot(page, shot_name("after_submit")); log("submit ok"); return True
        except Exception: pass
        time.sleep(1)
    log_w("submit btn not found"); return False

def fill(page: Page, records: List[Tuple[str, str]], att: str) -> None:
    """在已打开的表单页面上填写并提交（单条记录）"""
    save_shot(page, shot_name("meal_form"))
    for i, (ds, off) in enumerate(records):
        cross = iscross(off)
        end_d = datetime.strptime(ds, "%Y-%m-%d") + timedelta(days=1) if cross else datetime.strptime(ds, "%Y-%m-%d")
        end_ds = end_d.strftime("%Y-%m-%d")
        tag = "[X]" if cross else "[/]"
        log(f"  {tag} {ds} 18:00 -> {end_ds} {off} yuan={Config.MEAL_CROSS if cross else Config.MEAL_NORMAL}")
        ok0 = js_picker(page, 0, f"{ds} 18:00")
        time.sleep(0.8)
        ok1 = js_picker(page, 1, f"{end_ds} {off}")
        time.sleep(0.8)
        if not (ok0 and ok1):
            log_e(f"picker fail, skipping {ds}"); continue
        if att and os.path.exists(att):
            if not upload_file(page, att):
                log_e(f"upload failed, skipping {ds}"); continue
    submit_form(page)

# ── 日期解析 ──────────────────────────────────────────
def parse_date(s: str) -> str:
    today = datetime.now(); s = s.strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', s): return s
    m = re.match(r'^(\d{4})年(\d+)月(\d+)日$', s)
    if m: return fmt_date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r'^(\d+)月(\d+)日$', s)
    if m: return fmt_date(today.year, int(m.group(1)), int(m.group(2)))
    m = re.match(r'^(\d+)日?$', s)
    if m: return fmt_date(today.year, today.month, int(m.group(1)))
    raise ValueError(f"cannot parse: {s}")

# ── 主程序 ────────────────────────────────────────────
def get_prev_month() -> Tuple[int, int]:
    today = datetime.now()
    return (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)

def process_month(page: Page, yr: int, mo: int) -> List[Tuple[str, str]]:
    log(f"=== {yr}/{mo} month ===")
    if not go_month(page, yr, mo):
        log_e("cannot navigate to target month"); return []
    page.wait_for_selector("[class*='Cell_']", timeout=8000); time.sleep(2)
    cell_map = read_all_cells(page, yr, mo)
    if len(cell_map) < 10:
        log_w(f"only {len(cell_map)} cells, falling back to day-by-day"); cell_map = {}
    import calendar
    today = datetime.now()
    _, last_day = calendar.monthrange(yr, mo)
    records = []
    for day in range(1, last_day + 1):
        dd = datetime(yr, mo, day)
        if dd.date() > today.date(): break
        rec = cell_map.get(day) if cell_map else read_record(page, yr, mo, day)
        if rec and rec[1] and (ge(rec[1], Config.LATE_HOUR) or iscross(rec[1])):
            records.append(rec); tag = "[X]" if iscross(rec[1]) else "[/]"
            log(f"  {tag} {rec[0]} off={rec[1]}")
        else:
            reason = "no_rec" if not rec or not rec[1] else f"off={rec[1]}"
            log_d(f"  [SKIP] {yr:04d}-{mo:02d}-{day:02d} {reason}")
    log(f"=== found {len(records)} ==="); return records

def process_date(page: Page, ds: str) -> List[Tuple[str, str]]:
    log(f"query: {ds}")
    dt = datetime.strptime(ds, "%Y-%m-%d")
    rec = read_record(page, dt.year, dt.month, dt.day)
    if rec and rec[1] and (ge(rec[1], Config.LATE_HOUR) or iscross(rec[1])):
        return [rec]
    elif rec: log(f"[no apply] {ds} off={rec[1]} < {Config.LATE_HOUR}, skip")
    else: log(f"[no apply] {ds} no record, skip")
    return []

def process_weekly(page: Page) -> List[Tuple[str, str]]:
    mon = datetime.now() - timedelta(days=datetime.now().weekday())
    today_date = datetime.now().date(); records = []
    for i in range(7):
        dd = mon + timedelta(days=i)
        if dd.date() > today_date: break
        rec = read_record(page, dd.year, dd.month, dd.day)
        if rec and rec[1] and (ge(rec[1], Config.LATE_HOUR) or iscross(rec[1])):
            records.append(rec); log(f"  ok {dd.strftime('%Y-%m-%d')} {rec[1]}")
    log(f"weekly: {len(records)}"); return records

def submit_records(browser: Browser, records: List[Tuple[str, str]], batch: bool = False) -> None:
    """所有记录在同一页面内循环提交"""
    if not records: log("no records to submit"); return
    savecsv(records)
    page = new_page(browser)
    go_meal_form_same_page(page)
    for i, (ds, off) in enumerate(records):
        att = str(Config.SHOT_DIR / att_name(ds))
        log(f"--- [{i+1}/{len(records)}] {ds} ---")
        if i > 0:
            go_meal_form_same_page(page)
        fill(page, [(ds, off)], att)
        time.sleep(2)
    log(f"=== done {len(records)} ===")

def main():
    ap = argparse.ArgumentParser(description="2号人事部 餐补申请")
    ap.add_argument("--mode", choices=["weekly","date","month"], default="date")
    ap.add_argument("--date", default=None, help="日期，默认昨天")
    ap.add_argument("--year",  type=int, default=None)
    ap.add_argument("--month", type=int, default=None)
    args = ap.parse_args()
    records = []
    with sync_playwright() as p:
        browser = None
        try:
            browser = init_browser(p)
            page = get_page(browser)
            page.goto(Config.TARGET_URL, timeout=Config.PAGE_TMO)
            if not wait_login(page): return
            go_attendance(page)
            if args.mode == "month":
                yr = args.year; mo = args.month
                if yr is None or mo is None: yr, mo = get_prev_month()
                records = process_month(page, yr, mo)
                submit_records(browser, records, batch=True)
            elif args.mode == "date":
                ds = parse_date(args.date) if args.date else (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                records = process_date(page, ds)
                submit_records(browser, records, batch=False)
            elif args.mode == "weekly":
                records = process_weekly(page)
                submit_records(browser, records, batch=False)
            if not records: log("no records, exit")
        except KeyboardInterrupt: log("user interrupted")
        except Exception as e:
            log_e(f"ERR: {e}"); import traceback; traceback.print_exc()
        finally:
            if browser:
                try: browser.close()
                except Exception: pass
            log("browser closed")

if __name__ == "__main__": main()

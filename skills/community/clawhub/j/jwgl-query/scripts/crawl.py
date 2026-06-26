#!/usr/bin/env python3
from __future__ import annotations

import argparse
from copy import deepcopy
import csv
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

BeautifulSoup = None
webdriver = None
ChromeService = None
By = None
EC = None
Select = None
WebDriverWait = None
SeleniumManager = None

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

DEFAULT_COLS = [
    "校区", "考场校区", "考试场次", "课程代码", "课程名称", "授课教师", "考试时间", "考场", "类别", "考生数"
]
DEFAULT_LOGIN_PATH = "/jsxsd/framework/jsMain.jsp"
LEGACY_SCHOOL_NAME = "默认学校"
CONFIG_EXAMPLE_PATH = SCRIPT_DIR.parent / "config.example.json"

COURSE_SCHEDULE_COLS = [
    "星期",
    "节次",
    "时间",
    "课程名称",
    "周次",
    "教室",
    "班级",
    "人数",
    "附加信息",
]

def ensure_runtime_dependencies() -> None:
    global BeautifulSoup, webdriver, ChromeService, By, EC, Select, WebDriverWait, SeleniumManager
    if all(dep is not None for dep in (BeautifulSoup, webdriver, ChromeService, By, EC, Select, WebDriverWait, SeleniumManager)):
        return

    try:
        from bs4 import BeautifulSoup as _BeautifulSoup
        from selenium import webdriver as _webdriver
        from selenium.webdriver.chrome.service import Service as _ChromeService
        from selenium.webdriver.common.by import By as _By
        from selenium.webdriver.support import expected_conditions as _EC
        from selenium.webdriver.support.ui import Select as _Select, WebDriverWait as _WebDriverWait
        from selenium.webdriver.common.selenium_manager import SeleniumManager as _SeleniumManager
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("Missing dependencies. Install selenium and beautifulsoup4 before running.") from exc

    BeautifulSoup = _BeautifulSoup
    webdriver = _webdriver
    ChromeService = _ChromeService
    By = _By
    EC = _EC
    Select = _Select
    WebDriverWait = _WebDriverWait
    SeleniumManager = _SeleniumManager


def by_map() -> dict[str, str]:
    ensure_runtime_dependencies()
    return {
        "id": By.ID,
        "xpath": By.XPATH,
        "css": By.CSS_SELECTOR,
        "name": By.NAME,
    }


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    bootstrap_legacy_school(config)
    apply_runtime_defaults(config)
    return config


def normalize_url(url: str | None) -> str:
    return (url or "").strip().rstrip("/")


def derive_login_url(base_url: str) -> str:
    cleaned = normalize_url(base_url)
    if not cleaned:
        return ""
    return f"{cleaned}{DEFAULT_LOGIN_PATH}"


def bootstrap_legacy_school(config: dict[str, Any]) -> None:
    schools = config.get("schools")
    if schools is not None and not isinstance(schools, dict):
        raise RuntimeError(json.dumps({
            "error_code": "INVALID_CONFIG",
            "message": "config.json 中的 schools 必须是对象",
        }, ensure_ascii=False))
    if schools:
        return

    base_url = normalize_url(config.get("base_url"))
    login_url = normalize_url(config.get("login_url")) or derive_login_url(base_url)
    if not base_url and not login_url:
        config.setdefault("schools", {})
        return

    school_name = (config.get("current_school") or LEGACY_SCHOOL_NAME).strip() or LEGACY_SCHOOL_NAME
    config["schools"] = {
        school_name: {
            "base_url": base_url,
            "login_url": login_url,
        }
    }
    config["current_school"] = school_name


def load_default_runtime_config() -> dict[str, Any]:
    if not CONFIG_EXAMPLE_PATH.exists():
        return {}
    with CONFIG_EXAMPLE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def merge_missing_dict_values(current: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(current)
    for key, default_value in defaults.items():
        current_value = merged.get(key)
        if isinstance(current_value, dict) and isinstance(default_value, dict):
            merged[key] = merge_missing_dict_values(current_value, default_value)
        elif key not in merged:
            merged[key] = deepcopy(default_value)
    return merged


def apply_runtime_defaults(config: dict[str, Any]) -> None:
    defaults = load_default_runtime_config()
    selector_defaults = defaults.get("selectors")
    if isinstance(selector_defaults, dict):
        current_selectors = config.get("selectors")
        if not isinstance(current_selectors, dict):
            current_selectors = {}
        config["selectors"] = merge_missing_dict_values(current_selectors, selector_defaults)


def get_school_map(config: dict[str, Any]) -> dict[str, Any]:
    bootstrap_legacy_school(config)
    schools = config.get("schools", {})
    if not isinstance(schools, dict):
        raise RuntimeError(json.dumps({
            "error_code": "INVALID_CONFIG",
            "message": "config.json 中的 schools 必须是对象",
        }, ensure_ascii=False))
    return schools


def get_teacher_record(config: dict[str, Any], teacher_name: str) -> dict[str, Any]:
    teachers = config.get("teachers", {})
    current_teacher = config.get("current_teacher")
    normalized = (teacher_name or "").strip()
    if normalized and normalized not in {"默认", "default", "current"}:
        return teachers.get(normalized) or {}
    return (
        (teachers.get(current_teacher) if current_teacher else None)
        or teachers.get("默认")
        or {}
    )


def ensure_teacher_record(config: dict[str, Any], teacher_name: str) -> dict[str, Any]:
    teacher = get_teacher_record(config, teacher_name)
    if teacher:
        return teacher
    raise RuntimeError(json.dumps({
        "error_code": "MISSING_TEACHER_CREDENTIALS",
        "teacher": teacher_name,
        "message": f"未找到老师账号信息：{teacher_name}",
    }, ensure_ascii=False))


def resolve_school_config(config: dict[str, Any], teacher_name: str, teacher: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    schools = get_school_map(config)
    teacher_school = (teacher.get("school") or "").strip()
    if teacher_school:
        school = schools.get(teacher_school)
        if not school:
            raise RuntimeError(json.dumps({
                "error_code": "TEACHER_SCHOOL_NOT_FOUND",
                "teacher": teacher_name,
                "school": teacher_school,
                "message": f"老师 {teacher_name} 绑定的学校不存在：{teacher_school}",
            }, ensure_ascii=False))
        return teacher_school, school

    current_school = (config.get("current_school") or "").strip()
    if current_school:
        school = schools.get(current_school)
        if not school:
            raise RuntimeError(json.dumps({
                "error_code": "CURRENT_SCHOOL_NOT_FOUND",
                "school": current_school,
                "message": f"当前学校不存在：{current_school}",
            }, ensure_ascii=False))
        return current_school, school

    if len(schools) == 1:
        school_name, school = next(iter(schools.items()))
        return school_name, school

    if not schools:
        raise RuntimeError(json.dumps({
            "error_code": "MISSING_SCHOOL_URLS",
            "teacher": teacher_name,
            "message": "还没有保存学校 URL 信息",
            "required": ["school", "base_url"],
        }, ensure_ascii=False))

    raise RuntimeError(json.dumps({
        "error_code": "MISSING_SCHOOL_SELECTION",
        "teacher": teacher_name,
        "message": "已保存多个学校 URL，请先指定要使用的学校",
        "schools": sorted(schools.keys()),
    }, ensure_ascii=False))


def require_query_config(config: dict[str, Any], query_type: str, school_name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    selectors = config.get("selectors")
    if not isinstance(selectors, dict):
        raise RuntimeError(json.dumps({
            "error_code": "MISSING_SELECTORS_CONFIG",
            "school": school_name,
            "message": "config.json 缺少 selectors 配置",
            "required": ["selectors.login", f"selectors.queries.{query_type}"],
        }, ensure_ascii=False))

    login = selectors.get("login")
    if not isinstance(login, dict):
        raise RuntimeError(json.dumps({
            "error_code": "MISSING_LOGIN_SELECTORS",
            "school": school_name,
            "message": "config.json 缺少 selectors.login 配置",
            "required": ["selectors.login.username", "selectors.login.password", "selectors.login.login_button"],
        }, ensure_ascii=False))

    queries = selectors.get("queries")
    if not isinstance(queries, dict):
        raise RuntimeError(json.dumps({
            "error_code": "MISSING_QUERY_DEFINITIONS",
            "school": school_name,
            "message": "config.json 缺少 selectors.queries 配置",
            "required": [f"selectors.queries.{query_type}"],
        }, ensure_ascii=False))

    query = queries.get(query_type)
    if not isinstance(query, dict):
        raise RuntimeError(json.dumps({
            "error_code": "MISSING_QUERY_CONFIG",
            "school": school_name,
            "query_type": query_type,
            "message": f"config.json 缺少 selectors.queries.{query_type} 配置",
            "required": [f"selectors.queries.{query_type}"],
        }, ensure_ascii=False))

    return login, query


def build_driver(chromedriver_path: str | None = None, headless: bool = False):
    ensure_runtime_dependencies()
    chromedriver_path = chromedriver_path or os.getenv("CHROMEDRIVER_PATH")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if headless:
        options.add_argument("--headless=new")

    browser_binary = os.getenv("GOOGLE_CHROME_BIN") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(browser_binary).exists():
        options.binary_location = browser_binary

    if chromedriver_path:
        service = ChromeService(executable_path=chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    service_env = os.environ.copy()
    path_parts = [p for p in service_env.get("PATH", "").split(os.pathsep) if p and p != "/usr/local/bin"]
    service_env["PATH"] = os.pathsep.join(path_parts)

    try:
        sm_args = ["--browser", "chrome", "--skip-driver-in-path"]
        if Path(browser_binary).exists():
            sm_args.extend(["--browser-path", browser_binary])
        driver_info = SeleniumManager().binary_paths(sm_args)
        driver_path = driver_info.get("driver_path")
        if driver_path:
            service = ChromeService(executable_path=driver_path, env=service_env)
            return webdriver.Chrome(service=service, options=options)
    except Exception:
        pass

    service = ChromeService(env=service_env)
    return webdriver.Chrome(service=service, options=options)


def wait_for_ready(driver, wait: int = 20):
    WebDriverWait(driver, wait, poll_frequency=0.5).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def is_login_page(driver) -> bool:
    try:
        title = (driver.title or "").strip()
        page = driver.page_source or ""
        return title == "登录" or 'id="userAccount"' in page or 'name="userAccount"' in page
    except Exception:
        return False


def locate(driver, selector: dict[str, str], wait: int = 15, clickable: bool = False):
    ensure_runtime_dependencies()
    if not selector or not selector.get("value"):
        raise ValueError("Missing selector value in config")
    by = by_map()[selector["by"]]
    value = selector["value"]
    condition = EC.element_to_be_clickable((by, value)) if clickable else EC.presence_of_element_located((by, value))
    return WebDriverWait(driver, wait, poll_frequency=0.5).until(condition)


def has_selector(driver, selector: dict[str, str]) -> bool:
    ensure_runtime_dependencies()
    if not selector or not selector.get("value"):
        return False
    try:
        by = by_map()[selector["by"]]
        return bool(driver.find_elements(by, selector["value"]))
    except Exception:
        return False


def click(driver, selector: dict[str, str], wait: int = 15, js_fallback: bool = True):
    elem = locate(driver, selector, wait=wait, clickable=True)
    try:
        return elem.click()
    except Exception:
        if js_fallback:
            return driver.execute_script("arguments[0].click();", elem)
        raise


def switch_to_frame(driver, selector: dict[str, str], wait: int = 15):
    ensure_runtime_dependencies()
    if not selector or not selector.get("value"):
        raise ValueError("Missing selector value in config")
    by = by_map()[selector["by"]]
    value = selector["value"]
    WebDriverWait(driver, wait, poll_frequency=0.5).until(EC.frame_to_be_available_and_switch_to_it((by, value)))
    wait_for_ready(driver, wait=wait)


def switch_to_visible_content_frame(driver, wait: int = 20):
    ensure_runtime_dependencies()
    def _find_visible_frame(d):
        frames = d.find_elements(By.CSS_SELECTOR, "iframe[id^='Frame']")
        for frame in frames:
            try:
                if frame.is_displayed():
                    d.switch_to.frame(frame)
                    return True
            except Exception:
                continue
        return False

    WebDriverWait(driver, wait, poll_frequency=0.5).until(_find_visible_frame)
    wait_for_ready(driver, wait=wait)


def switch_to_query_context(driver, used_direct_path: bool, wait: int = 20):
    driver.switch_to.default_content()
    if used_direct_path:
        wait_for_ready(driver, wait=wait)
        return
    switch_to_visible_content_frame(driver, wait=wait)


def fill_input(driver, selector: dict[str, str], value: str, clear_hidden_pair_selector: dict[str, str] | None = None, wait: int = 20):
    elem = locate(driver, selector, wait=wait)
    if clear_hidden_pair_selector and has_selector(driver, clear_hidden_pair_selector):
        hidden = locate(driver, clear_hidden_pair_selector, wait=wait)
        driver.execute_script("arguments[0].value='';", hidden)
    try:
        elem.clear()
    except Exception:
        pass
    elem.send_keys(value)
    try:
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', {bubbles:true})); arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            elem,
        )
    except Exception:
        pass


def scrape_table(driver, table_id: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", id=table_id)
    if not table:
        return []
    tbody = table.find("tbody") or table
    all_trs = tbody.find_all("tr")
    if not all_trs:
        return []
    headers = [cell.get_text(strip=True) for cell in all_trs[0].find_all(["th", "td"])]
    rows: list[dict[str, str]] = []
    for tr in all_trs[1:]:
        cells = tr.find_all("td")
        if len(cells) != len(headers):
            continue
        values = [cell.get_text(strip=True) for cell in cells]
        if len(values) == 1 and values[0] == "未查询到数据":
            continue
        rows.append(dict(zip(headers, values)))
    return rows


def parse_course_cell(cell) -> list[dict[str, str]]:
    blocks = cell.find_all("div", class_=re.compile(r"\bkbcontent\d*\b"))
    candidates: list[dict[str, str]] = []
    for block in blocks:
        text = block.get_text("\n", strip=True).replace("\xa0", " ").strip()
        if not text or text == "&nbsp;":
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip() and line.strip() != "&nbsp;"]
        if not lines:
            continue
        course_name = lines[0]
        week_text = ""
        room_text = ""
        class_text = ""
        headcount = ""
        extras: list[str] = []
        for line in lines[1:]:
            if line.endswith("周") and not week_text:
                week_text = line
            elif ("[" in line and "]节" in line) or re.search(r"[A-Za-z\u4e00-\u9fa5]+楼", line):
                if not room_text:
                    room_text = line
                else:
                    extras.append(line)
            elif re.search(r":\d+$", line) and not class_text:
                class_text = line
                parts = line.rsplit(":", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    headcount = parts[1]
            elif line not in {course_name}:
                extras.append(line)
        candidates.append(
            {
                "课程名称": course_name,
                "周次": week_text,
                "教室": room_text,
                "班级": class_text,
                "人数": headcount,
                "附加信息": "；".join(extras),
            }
        )
    return candidates


def normalize_course_row_value(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def course_row_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(
        normalize_course_row_value(row.get(field))
        for field in ("星期", "节次", "时间", "课程名称", "周次", "教室")
    )


def course_row_score(row: dict[str, str]) -> tuple[int, int, int]:
    priority_fields = ("班级", "人数", "附加信息", "教室", "周次", "时间")
    normalized_values = [normalize_course_row_value(str(value)) for value in row.values()]
    return (
        sum(bool(normalize_course_row_value(row.get(field))) for field in priority_fields),
        sum(bool(value) for value in normalized_values),
        sum(len(value) for value in normalized_values),
    )


def dedupe_course_schedule_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    best_by_key: dict[tuple[str, ...], dict[str, str]] = {}
    order: list[tuple[str, ...]] = []

    for row in rows:
        key = course_row_key(row)
        if key not in best_by_key:
            best_by_key[key] = row
            order.append(key)
            continue
        if course_row_score(row) > course_row_score(best_by_key[key]):
            best_by_key[key] = row

    return [best_by_key[key] for key in order]


def parse_teacher_schedule_html(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="kbtable")
    if not table:
        return []
    tbody = table.find("tbody") or table
    row = tbody.find("tr")
    if not row:
        return []
    cells = row.find_all("td")
    if len(cells) < 2:
        return []

    day_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    periods = ["0102", "0304", "0506", "0708", "091011"]
    rows: list[dict[str, str]] = []

    for idx, cell in enumerate(cells[1:]):
        entries = parse_course_cell(cell)
        if not entries:
            continue
        day = day_names[idx // 5]
        period = periods[idx % 5]
        for entry in entries:
            rows.append(
                {
                    "星期": day,
                    "节次": period,
                    "时间": "",
                    **entry,
                }
            )
    return dedupe_course_schedule_rows(rows)


def parse_course_schedule_html(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="kbtable")
    if not table:
        return []

    text = table.get_text("\n", strip=True)
    if "教师\\节次" in text:
        return parse_teacher_schedule_html(html)

    tbody = table.find("tbody") or table
    trs = tbody.find_all("tr")
    if len(trs) < 2:
        return []
    headers = [th.get_text(strip=True) for th in trs[0].find_all(["th", "td"])]
    weekdays = headers[1:8]
    rows: list[dict[str, str]] = []
    for tr in trs[1:]:
        th = tr.find("th")
        tds = tr.find_all("td")
        if not th or len(tds) < 7:
            continue
        period_lines = [line.strip() for line in th.get_text("\n", strip=True).splitlines() if line.strip()]
        if not period_lines:
            continue
        period = period_lines[0]
        time_range = period_lines[1] if len(period_lines) > 1 else ""
        for idx, day in enumerate(weekdays):
            cell_entries = parse_course_cell(tds[idx])
            for entry in cell_entries:
                rows.append(
                    {
                        "星期": day,
                        "节次": period,
                        "时间": time_range,
                        **entry,
                    }
                )
    return dedupe_course_schedule_rows(rows)


def login_once(driver, login_url: str, login: dict[str, Any], creds: dict[str, Any], save_step=None, wait: int = 30):
    driver.get(login_url)
    wait_for_ready(driver, wait=wait)
    if save_step:
        save_step("01-login-page")

    username = locate(driver, login["username"])
    username.clear()
    username.send_keys(creds["username"])
    password = locate(driver, login["password"])
    password.clear()
    password.send_keys(creds["password"])
    try:
        driver.execute_script("if (typeof submitForm1 === 'function' && submitForm1()) { document.getElementById('Form1').submit(); }")
    except Exception:
        click(driver, login["login_button"])

    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert.accept()
    except Exception:
        pass

    WebDriverWait(driver, wait, poll_frequency=0.5).until(lambda d: 'jsMain.jsp' in d.current_url or '教学一体化服务平台' in d.title)
    time.sleep(2)
    if save_step:
        save_step("02-after-login")


def navigate_to_query_page(driver, config: dict[str, Any], query: dict[str, Any], save_step, wait: int = 20) -> bool:
    direct_path = query.get("direct_path")
    if direct_path:
        target_url = urljoin(config.get("base_url", config.get("login_url", "")), direct_path)
        driver.get(target_url)
        wait_for_ready(driver, wait=wait)
        time.sleep(1)
        save_step("03-direct-target")
        return True

    click(driver, query["menu_parent"], wait=wait)
    time.sleep(1)
    save_step("03-after-parent-click")
    child = locate(driver, query["menu_child"], wait=wait, clickable=False)
    driver.execute_script("arguments[0].click();", child)
    time.sleep(2)
    save_step("04-after-child-click")
    return False


def run_crawler(config_path: str, teacher_name: str, term: str, query_type: str, headless: bool = False, debug_dir: str | None = None) -> tuple[str, list[dict[str, str]]]:
    config = load_config(config_path)
    teacher = ensure_teacher_record(config, teacher_name)
    school_name, school = resolve_school_config(config, teacher_name, teacher)

    login, query = require_query_config(config, query_type, school_name)
    login_url = normalize_url(school.get("login_url")) or derive_login_url(school.get("base_url"))
    base_url = normalize_url(school.get("base_url")) or normalize_url(login_url)
    if not login_url:
        raise RuntimeError(json.dumps({
            "error_code": "MISSING_LOGIN_URL",
            "school": school_name,
            "query_type": query_type,
            "message": "config.json 缺少学校登录 URL 配置",
            "required": ["schools.<school>.login_url"],
        }, ensure_ascii=False))

    active_config = dict(config)
    active_config["base_url"] = base_url
    active_config["login_url"] = login_url

    driver = build_driver(headless=headless)
    debug_path = Path(debug_dir) if debug_dir else None
    if debug_path:
        debug_path.mkdir(parents=True, exist_ok=True)

    try:
        def save_step(name: str):
            if not debug_path:
                return
            safe = name.replace('/', '_')
            try:
                (debug_path / f"{safe}.html").write_text(driver.page_source, encoding="utf-8")
            except Exception:
                pass
            try:
                driver.save_screenshot(str(debug_path / f"{safe}.png"))
            except Exception:
                pass

        try:
            driver.maximize_window()
        except Exception:
            pass

        driver.set_page_load_timeout(30)
        login_once(driver, login_url, login, teacher, save_step=save_step)

        used_direct_path = navigate_to_query_page(driver, active_config, query, save_step)
        if is_login_page(driver):
            login_once(driver, login_url, login, teacher, save_step=save_step)
            used_direct_path = navigate_to_query_page(driver, active_config, query, save_step)
        switch_to_query_context(driver, used_direct_path)
        if is_login_page(driver):
            login_once(driver, login_url, login, teacher, save_step=save_step)
            used_direct_path = navigate_to_query_page(driver, active_config, query, save_step)
            switch_to_query_context(driver, used_direct_path)
        save_step("05-in-query-context")

        if query.get("term_select", {}).get("value"):
            select_element = locate(driver, query["term_select"], wait=20)
            target_term = term or select_element.get_attribute("value") or select_element.get_dom_attribute("value")
            if target_term:
                current_term = select_element.get_attribute("value")
                if current_term != target_term:
                    Select(select_element).select_by_value(target_term)
                    time.sleep(1)
                    save_step("06-after-term-select")

        if query_type == "course_schedule" and query.get("teacher_input", {}).get("value"):
            fill_input(
                driver,
                query["teacher_input"],
                teacher_name,
                clear_hidden_pair_selector=query.get("teacher_id_input"),
                wait=20,
            )
            save_step("07-after-teacher-input")

        if query_type == "course_schedule":
            pre_rows = parse_course_schedule_html(driver.page_source)
            if pre_rows:
                save_step("08-course-table-already-present")
                return school_name, pre_rows

        if query.get("query_button", {}).get("value"):
            click(driver, query["query_button"], wait=20)
            time.sleep(2)
            save_step("08-after-query-click")
        elif query_type == "course_schedule":
            time.sleep(1)

        if query.get("result_frame", {}).get("value"):
            try:
                switch_to_frame(driver, query["result_frame"], wait=20)
                if is_login_page(driver):
                    raise RuntimeError("result_frame_redirected_to_login")
                time.sleep(1)
                save_step("09-in-result-frame")
            except Exception:
                if query_type != "course_schedule" and used_direct_path:
                    login_once(driver, login_url, login, teacher, save_step=save_step)
                    used_direct_path = navigate_to_query_page(driver, active_config, query, save_step)
                    switch_to_query_context(driver, used_direct_path)
                    if query.get("term_select", {}).get("value"):
                        select_element = locate(driver, query["term_select"], wait=20)
                        target_term = term or select_element.get_attribute("value") or select_element.get_dom_attribute("value")
                        if target_term:
                            current_term = select_element.get_attribute("value")
                            if current_term != target_term:
                                Select(select_element).select_by_value(target_term)
                                time.sleep(1)
                    if query.get("query_button", {}).get("value"):
                        click(driver, query["query_button"], wait=20)
                        time.sleep(2)
                    switch_to_frame(driver, query["result_frame"], wait=20)
                    time.sleep(1)
                    save_step("09-in-result-frame")
                else:
                    raise

        if query_type == "course_schedule":
            rows = parse_course_schedule_html(driver.page_source)
            if rows:
                return school_name, rows
        else:
            rows = scrape_table(driver, query.get("table_id", "dataList"))
            if rows:
                return school_name, rows

        driver.switch_to.default_content()
        if not used_direct_path:
            try:
                switch_to_visible_content_frame(driver, wait=10)
                save_step("10-after-reenter-frame")
                if query_type == "course_schedule":
                    return school_name, parse_course_schedule_html(driver.page_source)
                return school_name, scrape_table(driver, query.get("table_id", "dataList"))
            except Exception:
                pass

        if query_type == "course_schedule":
            return school_name, parse_course_schedule_html(driver.page_source)
        return school_name, scrape_table(driver, query.get("table_id", "dataList"))

    except Exception as exc:
        state = {
            "error": str(exc),
            "type": exc.__class__.__name__,
            "url": "",
            "title": "",
            "school": school_name,
            "traceback": traceback.format_exc(),
        }
        try:
            parsed = json.loads(str(exc))
            if isinstance(parsed, dict) and parsed.get("error_code"):
                state.update(parsed)
        except Exception:
            pass
        try:
            state["url"] = driver.current_url
            state["title"] = driver.title
        except Exception:
            pass
        if debug_path:
            try:
                (debug_path / "page.html").write_text(driver.page_source, encoding="utf-8")
            except Exception:
                pass
            try:
                driver.save_screenshot(str(debug_path / "page.png"))
            except Exception:
                pass
            try:
                (debug_path / "error.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:
                pass
        raise RuntimeError(json.dumps(state, ensure_ascii=False)) from exc
    finally:
        driver.quit()


def main() -> None:
    parser = argparse.ArgumentParser(description="查询 jwgl 教务系统中的教师课表与考试相关信息")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--teacher", default="", help="老师名称；不传时优先尝试使用 config.json 中的 current_teacher")
    parser.add_argument("--term", default="", help="学期，如 2025-2026-2；留空时按系统默认/当前学期处理")
    parser.add_argument("--query-type", default="invigilation", help="查询类型：course_schedule / invigilation / exam_course_arrangement / exam_info / exam_all")
    parser.add_argument("--out", default="", help="输出文件路径；不传则直接打印到 stdout")
    parser.add_argument("--format", choices=["csv", "json"], default="json", help="输出格式")
    parser.add_argument("--headless", action="store_true", help="使用无头浏览器运行")
    parser.add_argument("--debug-dir", default="", help="调试输出目录；仅排障时使用")
    args = parser.parse_args()

    if args.query_type == "exam_all":
        subtypes = ["invigilation", "exam_course_arrangement", "exam_info"]
        merged_rows: list[dict[str, str]] = []
        details: list[dict[str, Any]] = []
        for subtype in subtypes:
            school_name, rows = run_crawler(
                args.config,
                args.teacher,
                args.term,
                query_type=subtype,
                headless=args.headless,
                debug_dir=str(Path(args.debug_dir) / subtype) if args.debug_dir else None,
            )
            tagged = [{"_query_type": subtype, **row} for row in rows]
            merged_rows.extend(tagged)
            details.append({"query_type": subtype, "count": len(rows), "rows": rows})
        output = {
            "query_type": args.query_type,
            "teacher": args.teacher,
            "school": school_name,
            "term": args.term,
            "count": len(merged_rows),
            "rows": merged_rows,
            "details": details,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        final_rows = merged_rows
    else:
        school_name, rows = run_crawler(args.config, args.teacher, args.term, query_type=args.query_type, headless=args.headless, debug_dir=args.debug_dir or None)
        print(json.dumps({"query_type": args.query_type, "teacher": args.teacher, "school": school_name, "term": args.term, "count": len(rows), "rows": rows}, ensure_ascii=False, indent=2))
        final_rows = rows

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if args.format == "json":
            out_path.write_text(json.dumps(final_rows, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            default_cols = COURSE_SCHEDULE_COLS if args.query_type == "course_schedule" else DEFAULT_COLS
            fieldnames = sorted({k for row in final_rows for k in row.keys()}) if final_rows else default_cols
            with out_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(final_rows)


if __name__ == "__main__":
    main()

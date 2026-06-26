#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from crawl import build_driver, click, ensure_teacher_record, load_config, locate, resolve_school_config, switch_to_visible_content_frame
from selenium.webdriver.common.by import By


def dump_frames(driver):
    return [
        {
            "id": frame.get_attribute("id"),
            "name": frame.get_attribute("name"),
            "displayed": frame.is_displayed(),
            "src": frame.get_attribute("src"),
        }
        for frame in driver.find_elements(By.CSS_SELECTOR, "iframe")
    ]


def main() -> None:
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config.json")
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("out/probe-course")
    out_dir.mkdir(parents=True, exist_ok=True)

    config = load_config(str(config_path))
    teacher_name = config.get("current_teacher") or "默认"
    teacher = ensure_teacher_record(config, teacher_name)
    _, school = resolve_school_config(config, teacher_name, teacher)
    login = config["selectors"]["login"]
    query = config["selectors"]["queries"]["course_schedule"]

    driver = build_driver(headless=True)
    try:
        driver.get(school["login_url"])
        locate(driver, login["username"]).send_keys(teacher["username"])
        locate(driver, login["password"]).send_keys(teacher["password"])
        try:
            driver.execute_script("if (typeof submitForm1 === 'function' && submitForm1()) { document.getElementById('Form1').submit(); }")
        except Exception:
            click(driver, login["login_button"])
        time.sleep(3)

        (out_dir / "01-after-login.html").write_text(driver.page_source, encoding="utf-8")
        driver.save_screenshot(str(out_dir / "01-after-login.png"))

        click(driver, query["menu_parent"])
        time.sleep(2)
        (out_dir / "02-after-parent.html").write_text(driver.page_source, encoding="utf-8")
        driver.save_screenshot(str(out_dir / "02-after-parent.png"))

        child = locate(driver, query["menu_child"], wait=20, clickable=False)
        driver.execute_script("arguments[0].click();", child)
        time.sleep(3)
        (out_dir / "03-after-child.html").write_text(driver.page_source, encoding="utf-8")
        driver.save_screenshot(str(out_dir / "03-after-child.png"))

        frames = dump_frames(driver)
        (out_dir / "frames-default.json").write_text(json.dumps(frames, ensure_ascii=False, indent=2), encoding="utf-8")

        driver.switch_to.default_content()
        switch_to_visible_content_frame(driver)
        time.sleep(2)
        (out_dir / "04-visible-frame.html").write_text(driver.page_source, encoding="utf-8")
        driver.save_screenshot(str(out_dir / "04-visible-frame.png"))

        inner_frames = dump_frames(driver)
        (out_dir / "frames-inside.json").write_text(json.dumps(inner_frames, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

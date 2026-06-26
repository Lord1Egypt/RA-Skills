import argparse
import datetime
import re
import sys
import time
from typing import Any, Dict, List, Set

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from hoseo_utils import BASE_URL, LMS_PATHS, UNAVAILABLE_DIALOG_KEYWORD, load_credentials

LMS_LOGIN_URL = f"{BASE_URL}{LMS_PATHS['login']}"
COURSE_LIST_URL = f"{BASE_URL}{LMS_PATHS['course_list']}"
ATTEND_URL_TEMPLATE = f"{BASE_URL}{LMS_PATHS['attendance']}?id={{course_id}}"

COMPLETED_STATUSES = {"O", "X"}
VIDEO_POLL_INTERVAL = 2
LOG_INTERVAL = 60

VERBOSE = False


def set_verbose(enabled: bool) -> None:
    global VERBOSE
    VERBOSE = enabled


def _ts() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


def info(msg: str) -> None:
    print(f"[{_ts()}] {msg}")


def error(msg: str) -> None:
    print(f"[{_ts()}] [ERROR] {msg}")


def debug(msg: str) -> None:
    if VERBOSE:
        print(f"[{_ts()}] [DEBUG] {msg}")


def login(page, user_id: str, password: str) -> bool:
    try:
        page.goto(LMS_LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
        page.locator("#input-username").fill(user_id)
        page.locator("#input-password").fill(password)
        page.locator(".btn.btn-login").click()
        page.wait_for_load_state("networkidle", timeout=30000)

        if "login" in page.url.lower() and page.locator(".userpicture").count() == 0:
            error("Login failed: still on login page")
            return False

        info("Login successful")
        return True
    except Exception as exc:
        error(f"Login error: {exc}")
        return False


def get_course_list(page) -> List[Dict[str, str]]:
    courses: List[Dict[str, str]] = []
    try:
        page.goto(COURSE_LIST_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector("table.table-coursemos tbody tr", timeout=30000)

        rows = page.locator("table.table-coursemos tbody tr")
        for idx in range(rows.count()):
            row = rows.nth(idx)
            row_class = row.get_attribute("class") or ""
            if "emptyrow" in row_class:
                continue

            name_link = row.locator("td.col-name a").first
            if name_link.count() == 0:
                continue

            class_name = name_link.inner_text().strip()
            href = name_link.get_attribute("href") or ""
            match = re.search(r"[?&]id=(\d+)", href)
            if not match:
                continue

            course_id = match.group(1)
            courses.append({
                "id": course_id,
                "class_name": class_name,
                "url": ATTEND_URL_TEMPLATE.format(course_id=course_id),
            })
    except Exception as exc:
        error(f"Failed to fetch course list: {exc}")

    return courses


def get_uncompleted_lectures_by_week(page, week_number: str) -> List[Dict[str, Any]]:
    uncompleted: List[Dict[str, Any]] = []

    week_cell = page.locator(
        f"xpath=//table[contains(@class,'table-coursemos')]"
        f"//td[normalize-space(text())='{week_number}']"
    ).first
    if week_cell.count() == 0:
        return uncompleted

    current_row = week_cell.locator("xpath=./parent::tr")
    rowspan_attr = week_cell.get_attribute("rowspan")
    rowspan = int(rowspan_attr) if (rowspan_attr and rowspan_attr.isdigit()) else 1

    try:
        title_link = current_row.locator("xpath=./td[2]//a").first
        status_cell = current_row.locator("xpath=./td[6]").first
        if title_link.count() > 0 and status_cell.count() > 0:
            status = status_cell.inner_text().strip()
            if status not in COMPLETED_STATUSES:
                uncompleted.append({
                    "title": title_link.inner_text().strip(),
                    "locator": title_link,
                })
    except Exception:
        pass

    for _ in range(rowspan - 1):
        current_row = current_row.locator("xpath=./following-sibling::tr[1]")
        try:
            title_link = current_row.locator("xpath=./td[1]//a").first
            status_cell = current_row.locator("xpath=./td[5]").first
            if title_link.count() > 0 and status_cell.count() > 0:
                status = status_cell.inner_text().strip()
                if status not in COMPLETED_STATUSES:
                    uncompleted.append({
                        "title": title_link.inner_text().strip(),
                        "locator": title_link,
                    })
        except Exception:
            continue

    return uncompleted


def _find_video_frame(target_page):
    try:
        if target_page.locator("video").count() > 0:
            return target_page
    except Exception:
        pass

    for frame in target_page.frames:
        try:
            if frame.locator("video").count() > 0:
                return frame
        except Exception:
            continue

    return None


def _wait_for_metadata(frame, max_wait: float = 15.0) -> bool:
    deadline = time.time() + max_wait
    while time.time() < deadline:
        try:
            ready = frame.evaluate(
                """() => {
                    const v = document.querySelector('video');
                    if (!v) return false;
                    return v.readyState >= 1 && v.duration > 0;
                }"""
            )
            if ready:
                return True
        except Exception:
            return False
        time.sleep(0.5)
    return False


def _start_playback(frame) -> bool:
    try:
        result = frame.evaluate(
            """() => {
                const v = document.querySelector('video');
                if (!v) return {ok: false, reason: 'no_element'};
                v.muted = true;
                const p = v.play();
                if (p && typeof p.then === 'function') {
                    return p.then(
                        () => {
                            v.muted = false;
                            v.volume = 0.5;
                            return {ok: true, reason: 'playing'};
                        },
                        (e) => ({ok: false, reason: e.message})
                    );
                }
                v.muted = false;
                v.volume = 0.5;
                return {ok: true, reason: 'sync_play'};
            }"""
        )
        if isinstance(result, dict):
            debug(f"Playback result: {result.get('reason', 'unknown')}")
            return result.get("ok", False)
        return True
    except Exception as exc:
        debug(f"Playback start error: {exc}")
        return False


def _poll_video_state(frame) -> Dict[str, Any]:
    return frame.evaluate(
        """() => {
            const v = document.querySelector('video');
            if (!v) return {ok: false, ended: false, current: 0, duration: 0, paused: true};
            return {
                ok: true,
                ended: !!v.ended,
                current: Number(v.currentTime || 0),
                duration: Number(v.duration || 0),
                paused: !!v.paused,
            };
        }"""
    )


def _click_play_button(target_page):
    selectors = [
        ".vjs-big-play-button",
        ".vjs-play-control",
        "[class*='play-button']",
        "[class*='play_button']",
        "button[title='Play']",
        "button[aria-label='Play']",
        ".ytp-large-play-button",
    ]
    for sel in selectors:
        try:
            btn = target_page.locator(sel).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                debug(f"Clicked play button: {sel}")
                return True
        except Exception:
            continue

    for frame in target_page.frames:
        for sel in selectors:
            try:
                btn = frame.locator(sel).first
                if btn.count() > 0 and btn.is_visible():
                    btn.click()
                    debug(f"Clicked play button in frame: {sel}")
                    return True
            except Exception:
                continue
    return False


def watch_lecture(page, lecture_info: Dict[str, Any], timeout_seconds: int) -> str:
    lecture_title = str(lecture_info.get("title") or "")
    lecture_locator = lecture_info.get("locator")
    if lecture_locator is None:
        error(f"Missing locator for lecture: {lecture_title}")
        return "failed"

    unavailable = {"value": False}

    def handle_dialog(dialog) -> None:
        text = dialog.message or ""
        if UNAVAILABLE_DIALOG_KEYWORD in text:
            unavailable["value"] = True
        try:
            dialog.accept()
        except Exception:
            pass

    context = page.context
    context.on("dialog", handle_dialog)

    popup = None
    try:
        new_pages_before = set(id(p) for p in context.pages)
        try:
            with page.expect_popup(timeout=20000) as popup_wait:
                lecture_locator.click()
            popup = popup_wait.value
        except PlaywrightTimeoutError:
            debug(f"No popup detected, checking for new tabs: {lecture_title}")
            new_pages_after = context.pages
            added = [p for p in new_pages_after if id(p) not in new_pages_before]
            if added:
                popup = added[-1]
                debug(f"Found new tab for: {lecture_title}")
            else:
                error(f"No popup or new tab opened: {lecture_title}")
                return "failed"

        if popup.is_closed():
            error(f"Page closed immediately: {lecture_title}")
            return "failed"

        debug(f"Popup opened for: {lecture_title}")
        popup.wait_for_load_state("domcontentloaded", timeout=30000)
        debug(f"Popup DOM loaded: {lecture_title}")

        if unavailable["value"]:
            info(f"Skipping unavailable lecture: {lecture_title}")
            return "unavailable"

        popup.wait_for_timeout(2000)

        video_frame = _find_video_frame(popup)

        if video_frame is None:
            debug(f"No video found, waiting additional 5s: {lecture_title}")
            popup.wait_for_timeout(5000)
            video_frame = _find_video_frame(popup)

        if video_frame is None:
            error(f"No video element in any frame: {lecture_title}")
            return "failed"

        debug(f"Video element located: {lecture_title}")

        _click_play_button(popup)
        popup.wait_for_timeout(1000)
        _start_playback(video_frame)

        meta_loaded = _wait_for_metadata(video_frame, max_wait=15.0)
        if not meta_loaded:
            debug(f"Metadata not loaded, attempting forced play: {lecture_title}")
            _start_playback(video_frame)
            _wait_for_metadata(video_frame, max_wait=10.0)

        info(f"Started watching: {lecture_title}")
        start_time = time.time()
        last_log = start_time
        stall_count = 0
        last_current = -1.0

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                info(f"Timeout reached: {lecture_title} ({int(elapsed)}s/{timeout_seconds}s)")
                return "timeout"

            try:
                if popup.is_closed():
                    error(f"Popup closed unexpectedly: {lecture_title}")
                    return "failed"
            except Exception:
                error(f"Popup unreachable: {lecture_title}")
                return "failed"

            try:
                state = _poll_video_state(video_frame)
            except Exception as exc:
                error(f"Video poll failed ({lecture_title}): {exc}")
                return "failed"

            if not state["ok"]:
                video_frame = _find_video_frame(popup)
                if video_frame is None:
                    error(f"Video element lost: {lecture_title}")
                    return "failed"
                time.sleep(VIDEO_POLL_INTERVAL)
                continue

            if state["ended"] or (state["duration"] > 0 and state["current"] >= state["duration"] - 1):
                info(f"Completed: {lecture_title}")
                return "done"

            if state["paused"] and state["duration"] > 0:
                debug(f"Video paused, resuming: {lecture_title}")
                _start_playback(video_frame)

            if state["current"] == last_current:
                stall_count += 1
                if stall_count >= 15:
                    debug(f"Video stalled for {stall_count * VIDEO_POLL_INTERVAL}s, nudging: {lecture_title}")
                    _click_play_button(popup)
                    _start_playback(video_frame)
                    stall_count = 0
            else:
                stall_count = 0
            last_current = state["current"]

            if time.time() - last_log > LOG_INTERVAL:
                info(f"[{lecture_title}] {int(state['current'])}/{int(state['duration'])}s")
                last_log = time.time()

            time.sleep(VIDEO_POLL_INTERVAL)

    except PlaywrightTimeoutError as te:
        error(f"Timeout opening lecture: {lecture_title} - {te}")
        return "failed"
    except Exception as exc:
        error(f"Error during lecture ({lecture_title}): {exc}")
        return "failed"
    finally:
        try:
            context.remove_listener("dialog", handle_dialog)
        except Exception:
            pass
        if popup is not None:
            try:
                if not popup.is_closed():
                    popup.close()
            except Exception:
                pass


def process_course(page, course: Dict[str, str], max_week: int, timeout_seconds: int, limit_lectures: int = 0) -> Dict[str, int]:
    info(f"[{course['class_name']}] Processing started")

    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            page.goto(course["url"], wait_until="domcontentloaded", timeout=60000)
            break
        except Exception as nav_exc:
            retry_count += 1
            if retry_count >= max_retries:
                error(f"Failed to navigate after {max_retries} retries: {nav_exc}")
                return {"watched": 0, "attempted": 0}
            debug(f"Navigation failed, retrying ({retry_count}/{max_retries}): {nav_exc}")
            time.sleep(2)

    skipped_lectures: Set[str] = set()
    fail_counts: Dict[str, int] = {}
    watched_count = 0
    total_attempted = 0
    max_fail_per_lecture = 3

    for week in range(1, max_week + 1):
        if limit_lectures > 0 and watched_count >= limit_lectures:
            break

        week_str = str(week)
        while True:
            if limit_lectures > 0 and watched_count >= limit_lectures:
                break

            lectures = get_uncompleted_lectures_by_week(page, week_str)
            lectures = [x for x in lectures if str(x["title"]) not in skipped_lectures]

            if not lectures:
                break

            lecture = lectures[0]
            title_key = str(lecture["title"])

            if fail_counts.get(title_key, 0) >= max_fail_per_lecture:
                info(f"Skipping after {max_fail_per_lecture} failures: {title_key}")
                skipped_lectures.add(title_key)
                continue

            total_attempted += 1
            result = watch_lecture(page, lecture, timeout_seconds=timeout_seconds)
            if result == "unavailable":
                skipped_lectures.add(title_key)
            elif result == "done":
                watched_count += 1
                limit_str = f"/{limit_lectures}" if limit_lectures > 0 else "/unlimited"
                info(f"[{course['class_name']}] Watched: {watched_count}{limit_str}")
            elif result in ("failed", "timeout"):
                fail_counts[title_key] = fail_counts.get(title_key, 0) + 1
                debug(f"Fail count for '{title_key}': {fail_counts[title_key]}/{max_fail_per_lecture}")

            retry_nav = 0
            while retry_nav < 3:
                try:
                    page.goto(course["url"], wait_until="domcontentloaded", timeout=60000)
                    break
                except Exception as nav_exc:
                    retry_nav += 1
                    if retry_nav >= 3:
                        error(f"[{course['class_name']}] Navigation failed, aborting course")
                        return {"watched": watched_count, "attempted": total_attempted}
                    debug(f"Post-lecture navigation retry ({retry_nav}/3): {nav_exc}")
                    time.sleep(2)

            time.sleep(1)

    info(f"[{course['class_name']}] Processing complete: {watched_count} watched, {total_attempted} attempted")
    return {"watched": watched_count, "attempted": total_attempted}


def select_courses(courses: List[Dict[str, str]], course_filter: str) -> List[Dict[str, str]]:
    if not course_filter:
        return courses

    keyword = course_filter.strip().lower()
    return [
        c for c in courses
        if keyword in c["class_name"].lower() or keyword == c["id"].lower()
    ]


def run(args: argparse.Namespace) -> int:
    set_verbose(args.verbose)

    user_id = args.user_id
    password = args.password
    if not user_id or not password:
        try:
            creds = load_credentials()
            user_id = user_id or creds["id"]
            password = password or creds["pw"]
        except FileNotFoundError as e:
            error(str(e))
            error("Provide --id/--pw or create credentials.json")
            return 1

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=not args.headed,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--autoplay-policy=no-user-gesture-required",
                "--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies",
                "--disable-gpu",
            ],
        )
        context = browser.new_context(
            locale="ko-KR",
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
        )

        page = context.new_page()

        if not login(page, user_id, password):
            browser.close()
            return 1

        courses = get_course_list(page)
        if not courses:
            error("Course list is empty. Check credentials or page structure.")
            browser.close()
            return 2

        targets = select_courses(courses, args.course)
        if not targets:
            error(f"No courses matched filter: '{args.course}'")
            browser.close()
            return 3

        for course in targets:
            stats = process_course(page, course, max_week=args.max_week, timeout_seconds=args.lecture_timeout, limit_lectures=args.limit_lectures)
            info(f"Course '{course['class_name']}': {stats['watched']} watched, {stats['attempted']} attempted")

        browser.close()
        info("All tasks completed.")
        return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hoseo LMS Playwright auto-attend")
    parser.add_argument("--id", dest="user_id", default="", help="Student ID (falls back to credentials.json)")
    parser.add_argument("--pw", dest="password", default="", help="Password (falls back to credentials.json)")
    parser.add_argument("--course", default="", help="Course name keyword or course ID")
    parser.add_argument("--limit-lectures", type=int, default=0, help="Max lectures to watch (0=unlimited)")
    parser.add_argument("--max-week", type=int, default=15, help="Max week number to scan")
    parser.add_argument("--lecture-timeout", type=int, default=3600, help="Max wait per lecture in seconds")
    parser.add_argument("--headed", action="store_true", help="Show browser window")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser


if __name__ == "__main__":
    cli_parser = build_parser()
    cli_args = cli_parser.parse_args()
    sys.exit(run(cli_args))


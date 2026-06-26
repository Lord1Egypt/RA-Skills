"""
publish.py - 统一入口
用法：
    python publish.py login <platform>   # 登录平台
    python publish.py run <platform>     # 发布视频
    python publish.py check <platform>   # 检查 cookie 是否有效

platform: douyin | tencent | ks | xhs | bilibili | all
"""
import sys
import asyncio
import time
from pathlib import Path

# 确保 scripts/ 目录在 Python 路径中
SCRIPTS_DIR = Path(__file__).parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from conf import LOCAL_CHROME_PATH, LOCAL_CHROME_HEADLESS, VIDEO_DIR

# Cookie 目录
COOKIES = {
    "douyin":   SCRIPTS_DIR / "cookies" / "douyin_uploader" / "account.json",
    "tencent":  SCRIPTS_DIR / "cookies" / "tencent_uploader" / "account.json",
    "ks":       SCRIPTS_DIR / "cookies" / "ks_uploader" / "account.json",
    "xhs":      SCRIPTS_DIR / "cookies" / "xiaohongshu_uploader" / "account.json",
    "bilibili": SCRIPTS_DIR / "cookies" / "bilibili_uploader" / "account.json",
}

PLATFORMS = list(COOKIES.keys())


# ─── 视频目录解析 ────────────────────────────────────────────────────────────

def parse_video_dir(video_dir: Path):
    tasks = []
    for mp4 in sorted(video_dir.glob("*.mp4")):
        stem = mp4.stem
        txt = video_dir / f"{stem}.txt"
        cover = None
        for ext in (".png", ".jpg", ".jpeg"):
            c = video_dir / f"{stem}{ext}"
            if c.exists():
                cover = c
                break
        title, tags = stem, []
        if txt.exists():
            for line in txt.read_text(encoding="utf-8", errors="ignore").strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    tags += [t.lstrip("#").strip() for t in line.split() if t.startswith("#")]
                elif not title or title == stem:
                    title = line
        tasks.append({"mp4": mp4, "title": title, "tags": tags, "cover": cover})
    return tasks


# ─── 登录 ────────────────────────────────────────────────────────────────────

async def login_douyin():
    from uploader.douyin_uploader.main import douyin_setup
    print("[抖音] 开始登录...")
    return await douyin_setup(str(COOKIES["douyin"]), handle=True)


async def login_tencent():
    from uploader.tencent_uploader.main import weixin_setup
    print("[视频号] 开始登录...")
    return await weixin_setup(str(COOKIES["tencent"]), handle=True)


async def login_ks():
    from uploader.ks_uploader.main import ks_setup
    print("[快手] 开始登录...")
    return await ks_setup(str(COOKIES["ks"]), handle=True)


async def login_xhs():
    from playwright.async_api import async_playwright
    cookie_file = COOKIES["xhs"]
    print("[小红书] 请在弹出的浏览器中手动登录，登录完成后按 Enter...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=LOCAL_CHROME_PATH, headless=False,
            args=["--disable-blink-features=AutomationControlled", "--lang=zh-CN", "--start-maximized"]
        )
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.xiaohongshu.com/explore")
        input("登录完成后按 Enter 继续...")
        await context.storage_state(path=str(cookie_file))
        await browser.close()
    print("[小红书] 登录状态已保存")
    return True


async def login_bilibili():
    import subprocess
    biliup = SCRIPTS_DIR / "uploader" / "bilibili_uploader" / "biliup.exe"
    cookie_file = COOKIES["bilibili"]
    cookie_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"[B站] 运行 biliup 登录，cookie 保存到: {cookie_file}")
    subprocess.run([str(biliup), "-u", str(cookie_file), "login"], check=True)
    print("[B站] 登录完成")
    return True


LOGIN_FUNCS = {
    "douyin":   login_douyin,
    "tencent":  login_tencent,
    "ks":       login_ks,
    "xhs":      login_xhs,
    "bilibili": login_bilibili,
}


# ─── 发布 ────────────────────────────────────────────────────────────────────

async def publish_douyin(tasks):
    from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
    from utils.files_times import generate_schedule_time_next_day
    cookie_file = str(COOKIES["douyin"])
    if not await douyin_setup(cookie_file, handle=False):
        print("[抖音] cookie 无效，请先运行: python publish.py login douyin")
        return
    times = generate_schedule_time_next_day(len(tasks), 1, daily_times=[16])
    for i, t in enumerate(tasks):
        print(f"[抖音] {t['mp4'].name} | {t['title']}")
        await DouYinVideo(t["title"], str(t["mp4"]), t["tags"], times[i], cookie_file,
                          thumbnail_path=str(t["cover"]) if t["cover"] else None).main()


async def publish_tencent(tasks):
    from uploader.tencent_uploader.main import weixin_setup, TencentVideo
    from utils.files_times import generate_schedule_time_next_day
    cookie_file = str(COOKIES["tencent"])
    if not await weixin_setup(cookie_file, handle=False):
        print("[视频号] cookie 无效，请先运行: python publish.py login tencent")
        return
    times = generate_schedule_time_next_day(len(tasks), 1, daily_times=[16])
    for i, t in enumerate(tasks):
        print(f"[视频号] {t['mp4'].name} | {t['title']}")
        await TencentVideo(t["title"], str(t["mp4"]), t["tags"], times[i], cookie_file,
                           thumbnail_path=str(t["cover"]) if t["cover"] else None).main()


async def publish_ks(tasks):
    from uploader.ks_uploader.main import ks_setup, KSVideo
    from utils.files_times import generate_schedule_time_next_day
    cookie_file = str(COOKIES["ks"])
    if not await ks_setup(cookie_file, handle=False):
        print("[快手] cookie 无效，请先运行: python publish.py login ks")
        return
    times = generate_schedule_time_next_day(len(tasks), 1, daily_times=[16])
    for i, t in enumerate(tasks):
        print(f"[快手] {t['mp4'].name} | {t['title']}")
        await KSVideo(t["title"], str(t["mp4"]), t["tags"], times[i], cookie_file).main()


async def publish_xhs(tasks):
    from uploader.xhs_uploader.main import XHSVideo
    cookie_file = str(COOKIES["xhs"])
    if not COOKIES["xhs"].exists():
        print("[小红书] cookie 不存在，请先运行: python publish.py login xhs")
        return
    for t in tasks:
        print(f"[小红书] {t['mp4'].name} | {t['title']}")
        await XHSVideo(t["title"], str(t["mp4"]), t["tags"], 0, cookie_file,
                       thumbnail_path=str(t["cover"]) if t["cover"] else None).main()


def publish_bilibili(tasks):
    from uploader.bilibili_uploader.main import (
        read_cookie_json_file, extract_keys_from_json, random_emoji, BilibiliUploader
    )
    from utils.files_times import generate_schedule_time_next_day
    from utils.constant import VideoZoneTypes
    cookie_file = COOKIES["bilibili"]
    if not cookie_file.exists():
        print("[B站] cookie 不存在，请先运行: python publish.py login bilibili")
        return
    cookie_data = extract_keys_from_json(read_cookie_json_file(cookie_file))
    times = generate_schedule_time_next_day(len(tasks), 1, daily_times=[16], timestamps=True)
    tid = VideoZoneTypes.KNOWLEDGE_SKILL.value  # 默认分区：野生技能协会，可按需修改
    for i, t in enumerate(tasks):
        title = t["title"] + random_emoji()
        print(f"[B站] {t['mp4'].name} | {title}")
        BilibiliUploader(cookie_data, t["mp4"], title, title, tid, t["tags"], times[i]).upload()
        time.sleep(30)  # B站限速


PUBLISH_FUNCS = {
    "douyin":   (publish_douyin,   True),   # (func, is_async)
    "tencent":  (publish_tencent,  True),
    "ks":       (publish_ks,       True),
    "xhs":      (publish_xhs,      True),
    "bilibili": (publish_bilibili, False),
}


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def usage():
    print("用法:")
    print("  python publish.py login <platform>   # 登录")
    print("  python publish.py run <platform>     # 发布")
    print(f"  platform: {' | '.join(PLATFORMS)} | all")
    sys.exit(1)


async def run_login(platform: str):
    if platform not in LOGIN_FUNCS:
        print(f"不支持的平台: {platform}")
        return
    await LOGIN_FUNCS[platform]()


async def run_publish(platform: str):
    tasks = parse_video_dir(VIDEO_DIR)
    if not tasks:
        print(f"没有找到视频: {VIDEO_DIR}")
        return
    print(f"找到 {len(tasks)} 个视频，目标平台: {platform}")

    targets = PLATFORMS if platform == "all" else [platform]
    for p in targets:
        if p not in PUBLISH_FUNCS:
            print(f"不支持的平台: {p}")
            continue
        if platform == "all" and not COOKIES[p].exists():
            print(f"[{p}] 跳过（未登录）")
            continue
        func, is_async = PUBLISH_FUNCS[p]
        if is_async:
            await func(tasks)
        else:
            func(tasks)


async def main():
    if len(sys.argv) < 3:
        usage()
    action, platform = sys.argv[1], sys.argv[2]
    if action == "login":
        await run_login(platform)
    elif action == "run":
        await run_publish(platform)
    else:
        usage()


if __name__ == "__main__":
    asyncio.run(main())

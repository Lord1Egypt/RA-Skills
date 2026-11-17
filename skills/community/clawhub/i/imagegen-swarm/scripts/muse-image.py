import argparse
import fcntl
import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image
from playwright.sync_api import sync_playwright

# Muse（muse.ai）没有接口，全部走专用的无头浏览器：一次打开浏览器，新开侧聊天发任务、等它画完、从云电脑文件库下载、删掉侧聊天。
# 网页结构（改版后先查这里）：输入框 textarea[aria-label="Message"]，附件 input[type=file]，发送 button[aria-label="Send"]，
# 都在 [data-hatch-composer-chrome] 里；消息 [data-message-item]（data-message-role=user|assistant）；工作中有 button「Stop」或 [aria-busy=true]；
# 图片附件卡片的名字在缩略图 img 的 alt 上；侧聊天行优先 [data-testid=hatch-thread-row]（第 0 行是主聊天）。
# 当前行的标记可能在行上，也可能在内部链接上（aria-current=page|true、aria-selected、data-active），
# 或者只在 href / data-thread-id 一类属性里带 /thread/<uuid>。对不上这一条侧聊天就不动它。右键菜单 Rename / Delete；
# 待确认在 button「Approvals」标签页；文件库 /library/files，根目录是云电脑的 /home/hatch，下载按钮叫「Download」。
BASE = "https://muse.ai"

def profile_roots():
    home = Path.home()
    return {
        "swarm": (home / ".config" / "imagegen-swarm").resolve(),
        "default": (home / ".config" / "imagegen-swarm" / "muse-browser").resolve(),
        "legacy": (home / ".config" / "image-gen" / "muse-browser").resolve(),
    }


def allowed_profile(path):
    """Resolve a Muse profile and refuse anything outside the documented directories.

    Allowed: a directory under ~/.config/imagegen-swarm, or the legacy default
    ~/.config/image-gen/muse-browser. The lock file is written beside that directory.
    """
    roots = profile_roots()
    chosen = Path(path).expanduser()
    if not chosen.is_absolute():
        chosen = roots["swarm"] / chosen
    resolved = chosen.resolve()
    if resolved == roots["legacy"]:
        return resolved
    try:
        resolved.relative_to(roots["swarm"])
    except ValueError:
        raise RuntimeError(
            "Muse profile must be under "
            + str(roots["swarm"])
            + " or the default "
            + str(roots["default"])
            + ". Refusing "
            + str(resolved)
        ) from None
    if resolved == roots["swarm"]:
        raise RuntimeError("Muse profile must be a directory under " + str(roots["swarm"]) + ", not the directory itself")
    return resolved


def default_profile():
    # 新安装写到 imagegen-swarm。旧资料夹还在、新的还没建时继续用旧的，免得改名后要重新登录 Muse。
    chosen = os.environ.get("IMAGE_GEN_MUSE_PROFILE")
    if chosen:
        return allowed_profile(chosen)
    roots = profile_roots()
    current = roots["default"]
    previous = roots["legacy"]
    if current.exists() or not previous.exists():
        return current
    return previous


PROFILE = default_profile()
REMOTE_DIR = "/home/hatch/workspace/imagegen-swarm"
# Muse's cloud computer home. "~" in an approval is this home, not the machine running the script.
CLOUD_HOME = Path("/home/hatch")
RATIOS = ("1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9")
THREAD_RE = re.compile(r"/thread/([0-9a-f-]{36})")
IDLE_SECONDS = 8
# Login waits until the composer is visible. One hour is above the 15 minute generation default.
LOGIN_WAIT_MS = 3_600_000
# 打开 /thread/<id> 之后侧栏可能还没画完当前行。只等一小会儿，对不上就放弃改名，不拖住出图。
ROW_WAIT_SECONDS = 5


def mark_run_dir(directory):
    run_id = os.environ.get("IMAGE_GEN_RUN_ID", "").strip()
    if not run_id:
        return
    marker = directory / ".imagegen-swarm-run"
    if not marker.exists():
        marker.write_text(run_id + "\n", encoding="utf-8")


@contextmanager
def browser(headless=True, create_profile=False):
    # 同一个资料夹同一时刻只能一个浏览器打开：加锁排队。
    # 资料夹只在用户显式 --login 时创建，出图和列聊天不会新建它。
    if not PROFILE.exists():
        if not create_profile:
            raise RuntimeError(
                "Muse profile directory does not exist. Run muse-image.py --login so the user can sign in. "
                "Generation does not create it."
            )
        PROFILE.mkdir(parents=True, exist_ok=True)
    elif not PROFILE.is_dir():
        raise RuntimeError(f"Muse profile path is not a directory: {PROFILE}")
    with open(PROFILE.parent / f"{PROFILE.name}.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        proxy = None
        value = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        if value:
            parts = urlsplit(value)
            proxy = {"server": f"{parts.scheme}://{parts.hostname}" + (f":{parts.port}" if parts.port else "")}
            if parts.username:
                proxy.update(username=parts.username, password=parts.password or "")
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(str(PROFILE), headless=headless, viewport={"width": 1280, "height": 860},
                                                           accept_downloads=True, proxy=proxy)
            try:
                yield context.pages[0] if context.pages else context.new_page()
            finally:
                context.close()


def wait_for(page, check, seconds, what):
    deadline = time.monotonic() + seconds
    while True:
        value = check()
        if value:
            return value
        if time.monotonic() > deadline:
            raise RuntimeError(f"{seconds} 秒内{what}")
        page.wait_for_timeout(500)


def composer(page):
    return page.locator('textarea[aria-label="Message"]').first


def open_url(page, url):
    page.goto(url, wait_until="domcontentloaded")
    if "/library/" in url:
        page.get_by_test_id("hatch-library-allfiles-panel").wait_for(timeout=45000)
        return
    wait_for(page, lambda: composer(page).count() and composer(page).is_visible(), 45,
             f"看不到消息输入框（没登录就先运行 --login）：{page.url}")
    page.wait_for_timeout(1500)


def messages(page):
    return page.evaluate("""() => [...document.querySelectorAll('[data-message-item]')].map(e => ({
        role: e.dataset.messageRole, text: e.innerText.replace(/^(You:|Assistant message:\\s*)/, '').trim()}))""")


def busy(page):
    return page.get_by_role("button", name="Stop", exact=True).count() > 0 or page.locator("[aria-busy=true]").count() > 0


def thread_id(page):
    match = THREAD_RE.search(page.url)
    return match.group(1) if match else None


def chats_panel(page):
    nav = page.get_by_role("navigation", name="Side chats")
    if nav.count() == 0 or not nav.is_visible():
        page.get_by_role("button", name="Chats").click()
        nav.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(800)


def side_chats(page):
    # 逐行点开读编号（第 0 行是主聊天，不碰）
    open_url(page, BASE + "/")
    result = []
    chats_panel(page)
    rows = page.get_by_test_id("hatch-thread-row")
    index = 1
    # 列表可能在读的过程中变短（别处刚删了侧聊天）：每一行之前重新数
    while index < rows.count():
        row = rows.nth(index)
        index += 1
        title = row.inner_text().strip().split("\n")[0]
        row.evaluate("e => e.click()")
        page.wait_for_function("() => location.pathname.startsWith('/thread/')", timeout=15000)
        result.append({"id": thread_id(page), "title": title})
        chats_panel(page)
    return result


# 在侧聊天面板里收集候选行。优先认 hatch-thread-row；没有这个 testid 时再退到链接、data 属性和 listitem。
# 每行记下：可见文字、行内 href/data 属性里的线程编号、以及行或内部控件是不是当前项。
SIDE_ROWS_JS = r'''() => {
    const nav = document.querySelector('nav[aria-label="Side chats"]') || document.body;
    document.querySelectorAll('[data-imagegen-row]').forEach(el => el.removeAttribute('data-imagegen-row'));
    const selectors = [
        '[data-testid="hatch-thread-row"]',
        '[data-testid="thread-row"]',
        '[data-thread-id]',
        '[data-session-id]',
        '[data-chat-id]',
        'a[href*="/thread/"]',
        '[role="listitem"]',
        '[role="option"]',
        '[role="row"]',
        '[class*="thread-row"]',
        '[class*="chat-row"]',
    ];
    const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    const hrefRe = /\/thread\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/ig;
    const idAttrs = ['data-thread-id', 'data-session-id', 'data-chat-id', 'data-threadid', 'data-thread'];
    function addIds(ids, value) {
        if (!value) return;
        const text = String(value);
        hrefRe.lastIndex = 0;
        let matched = false;
        let found;
        while ((found = hrefRe.exec(text))) {
            ids.add(found[1].toLowerCase());
            matched = true;
        }
        if (!matched && uuid.test(text.trim())) ids.add(text.trim().toLowerCase());
    }
    function idsOf(el) {
        const ids = new Set();
        addIds(ids, el.getAttribute && el.getAttribute('href'));
        for (const name of idAttrs) addIds(ids, el.getAttribute && el.getAttribute(name));
        const nested = 'a[href*="/thread/"], ' + idAttrs.map(name => `[${name}]`).join(', ');
        for (const node of el.querySelectorAll(nested)) {
            addIds(ids, node.getAttribute('href'));
            for (const name of idAttrs) addIds(ids, node.getAttribute(name));
        }
        return [...ids];
    }
    function isCurrent(el) {
        const nodes = [el, ...el.querySelectorAll('[aria-current], [aria-selected], [data-active], [data-state]')];
        return nodes.some(node => {
            const current = (node.getAttribute('aria-current') || '').toLowerCase();
            if (current === 'page' || current === 'true') return true;
            if ((node.getAttribute('aria-selected') || '').toLowerCase() === 'true') return true;
            if ((node.getAttribute('data-active') || '').toLowerCase() === 'true') return true;
            const state = (node.getAttribute('data-state') || '').toLowerCase();
            return state === 'active' || state === 'selected' || state === 'current';
        });
    }
    function rowOf(el) {
        return el.closest('[data-testid="hatch-thread-row"], [data-testid="thread-row"], [role="listitem"], [role="option"], [role="row"], li, [class*="thread-row"], [class*="chat-row"]') || el;
    }
    const seen = new Set();
    const rows = [];
    for (const el of nav.querySelectorAll(selectors.join(','))) {
        const row = rowOf(el);
        if (!nav.contains(row) || seen.has(row)) continue;
        seen.add(row);
        row.setAttribute('data-imagegen-row', String(rows.length));
        rows.push({text: (row.innerText || '').trim(), ids: idsOf(row), current: isCurrent(row)});
    }
    return rows;
}'''


def _row_ids(row):
    return {str(item).lower() for item in (row.get("ids") or []) if item}


def _is_main_chat(row):
    return "Main chat" in (row.get("text") or "")


def choose_side_row(rows, chat):
    # 只返回能证明是这一条侧聊天的行。主聊天、别的线程、或好几行都像，一律不选。
    wanted = (chat or "").strip().lower()
    if not wanted or not rows:
        return None
    owned = [index for index, row in enumerate(rows) if _row_ids(row) == {wanted} and not _is_main_chat(row)]
    if len(owned) == 1:
        return owned[0]
    if len(owned) > 1:
        current = [index for index in owned if rows[index].get("current")]
        return current[0] if len(current) == 1 else None
    legacy = []
    for index, row in enumerate(rows):
        if not row.get("current") or _is_main_chat(row):
            continue
        ids = _row_ids(row)
        if ids and ids != {wanted}:
            continue
        legacy.append(index)
    return legacy[0] if len(legacy) == 1 else None


def current_side_row(page, chat, seconds=ROW_WAIT_SECONDS):
    deadline = time.monotonic() + seconds
    while True:
        try:
            rows = page.evaluate(SIDE_ROWS_JS) or []
            index = choose_side_row(rows, chat)
            if index is not None:
                row = page.locator(f'[data-imagegen-row="{index}"]')
                if row.count() == 1 and "Main chat" not in row.inner_text():
                    return row
        except Exception:
            pass
        if time.monotonic() >= deadline:
            return None
        page.wait_for_timeout(400)


def row_menu(page, chat, item, timeout=30000):
    open_url(page, f"{BASE}/thread/{chat}")
    chats_panel(page)
    row = current_side_row(page, chat)
    if row is None:
        raise RuntimeError(f"当前行不是侧聊天 {chat}，不动它")
    row.dispatch_event("contextmenu", {"bubbles": True, "button": 2, "clientX": 150, "clientY": 150})
    page.get_by_role("menuitem", name=item).click(timeout=timeout)


def rename(page, chat, title, timeout=8000):
    row_menu(page, chat, "Rename", timeout=timeout)
    # 改名框会被消息框抢焦点：直接设值并发输入、回车事件（React 受控输入框的做法）
    box = page.get_by_test_id("hatch-thread-rename-input")
    box.wait_for(state="visible", timeout=timeout)
    box.evaluate("""(e, title) => {
        Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(e, title);
        e.dispatchEvent(new Event('input', {bubbles: true}));
        e.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
    }""", title)
    page.wait_for_timeout(1500)


def rename_or_continue(page, chat, title):
    # 改名只是给用户看的标题。行找不到、对话框打不开或超时，都记一条警告然后继续出图。
    try:
        rename(page, chat, title)
        return True
    except Exception as error:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        print(f"muse: rename skipped ({error}); continuing", file=sys.stderr)
        return False


def delete(page, chat):
    # 还在回答的侧聊天删不掉：先点 Stop 等它停下；同一浏览器里侧聊天列表要过十几秒才刷新，
    # 所以直接打开它的地址核对，显示 Something went wrong、没有消息就是删掉了；没删掉就再点一次删除
    for _ in range(2):
        open_url(page, f"{BASE}/thread/{chat}")
        stop = page.get_by_role("button", name="Stop", exact=True)
        if stop.count():
            stop.click()
            wait_for(page, lambda: not busy(page), 30, "Muse 没停下")
        row_menu(page, chat, "Delete")
        confirm = page.get_by_role("button", name="Delete", exact=True)
        if confirm.count():
            confirm.last.click()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            page.wait_for_timeout(3000)
            page.goto(f"{BASE}/thread/{chat}", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            if not messages(page) and "Something went wrong" in page.evaluate("document.body.innerText"):
                return
    raise RuntimeError(f"Muse 侧聊天 {chat} 删不掉")


COMPOSER = r'''() => {
    const chrome = document.querySelector('[data-hatch-composer-chrome]');
    if (!chrome) return null;
    const cards = [...chrome.querySelectorAll('button[aria-label="Remove attachment"]')].map(remove => {
        const card = remove.closest('div');
        return {names: [...card.querySelectorAll('img[alt]')].map(n => n.getAttribute('alt')),
                progress: !!card.querySelector('[role=status], [role=progressbar], [aria-busy="true"], progress')};
    });
    const send = chrome.querySelector('button[aria-label="Send"]');
    return {cards, ready: !!send && !send.disabled};
}'''
SENT_IMAGES = r'''before => {
    const entry = [...document.querySelectorAll('[data-message-item]')].slice(before).find(n => n.dataset.messageRole === 'user');
    return entry ? [...entry.querySelectorAll('button.hatch-chat-groupable-bubble img[alt]')].map(n => n.getAttribute('alt')) : null;
}'''
# Only the Allow/Deny controls and containing text are evidenced by the existing
# implementation. No captured approval establishes operation/argument selectors
# or a whole-card grammar. Do not infer permissions from that text. See references/muse.md.
APPROVALS = r'''() => [...document.querySelectorAll('button')].filter(b => /^allow\b/i.test(b.textContent.trim())).map(b => {
    const controls = node => [...node.querySelectorAll('button')].map(n => n.textContent.trim());
    let node = b.parentElement;
    while (node && !controls(node).includes('Deny')) node = node.parentElement;
    return {label: b.textContent.trim(), detail: node ? node.innerText.trim() : '',
            controls: node ? controls(node) : [], request: null};
})'''


def send(page, text, images):
    open_url(page, BASE + "/thread/new")
    if page.evaluate(COMPOSER)["cards"]:
        raise RuntimeError("输入框里已有别的附件，未发送")
    names = [image.name for image in images]
    for count, image in enumerate(images, 1):
        page.locator("[data-hatch-composer-chrome] input[type=file]").first.set_input_files(str(image))

        def uploaded(count=count, name=image.name):
            state = page.evaluate(COMPOSER)
            shown = [n for card in state["cards"] for n in card["names"]]
            return len(state["cards"]) == count and name in shown and state["ready"] and not any(c["progress"] for c in state["cards"])
        wait_for(page, uploaded, 120, f"图片 {image.name} 没上传完")
    before = len(messages(page))
    composer(page).click(force=True)
    composer(page).fill(text)
    page.locator('[data-hatch-composer-chrome] button[aria-label="Send"]').click()
    wait_for(page, lambda: len(messages(page)) > before, 30, "消息没发出去")
    if names:
        wait_for(page, lambda: sorted(page.evaluate(SENT_IMAGES, before) or []) == sorted(names), 60, f"已发送消息里没看到全部图片 {names}")
    wait_for(page, lambda: thread_id(page), 60, "没拿到侧聊天编号")
    return thread_id(page), before


def approvals(page):
    tab = page.get_by_role("button", name="Approvals", exact=True)
    if tab.count() == 0:
        return []
    tab.click()
    page.wait_for_timeout(500)
    return page.evaluate(APPROVALS)


def canonical_output_path(path, home=CLOUD_HOME):
    """One spelling for an output path: ~ expansion, . and .., then realpath of existing parents.

    The file itself may not exist yet. Symlinks in directories that already exist are resolved,
    and the missing tail is appended unchanged. "~" uses `home` (the cloud home for an approval,
    the local home for --out).
    """
    text = str(path).strip().strip("'\"")
    home = Path(home)
    if text == "~":
        text = str(home)
    elif text.startswith("~/"):
        text = str(home / text[2:])
    elif text == "~hatch" or text.startswith("~hatch/"):
        text = str(CLOUD_HOME / text[len("~hatch"):].lstrip("/"))
    normalized = os.path.normpath(text)
    if not os.path.isabs(normalized):
        normalized = os.path.normpath(str(home / normalized))
    current = Path(normalized)
    missing = []
    while current != current.parent and not current.exists():
        missing.append(current.name)
        current = current.parent
    try:
        resolved = current.resolve()
    except OSError:
        resolved = current
    for name in reversed(missing):
        resolved = resolved / name
    return Path(os.path.normpath(str(resolved)))


def prepare_local_output(out):
    """Create the local output's parent before Muse is asked to do anything, and return its real path."""
    path = canonical_output_path(out, home=Path.home())
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def scoped_save_approval(approval, remote):
    """Check an internally decoded request, never free-text approval descriptions.

    `request` is our internal policy representation, NOT a Muse wire protocol.
    APPROVALS leaves it null until a real captured card supports a complete,
    evidence-backed decoder. Thus all currently unrecognized live cards stop.
    A future decoder must account for the entire card, including every argument;
    it must not turn a summary or a subset of a compound request into this shape.
    """
    if not isinstance(approval, dict) or approval.get("label") != "Allow once":
        return False
    request = approval.get("request")
    if not isinstance(request, dict) or set(request) != {"operation", "paths"}:
        return False
    if request["operation"] != "save_image":
        return False
    paths = request["paths"]
    if not isinstance(paths, list) or len(paths) != 1 or not isinstance(paths[0], str):
        return False
    # One literal path only. Do not strip quotes/whitespace or extract a path from
    # a command; separators, substitutions and additional actions cannot match.
    if not re.fullmatch(r"[A-Za-z0-9_./~@+=-]+", paths[0]):
        return False
    try:
        return canonical_output_path(paths[0]) == canonical_output_path(remote)
    except (OSError, ValueError, RuntimeError):
        return False


def wait_done(page, since, deadline, approved, cancel_file, remote):
    # 持续空闲满 IDLE_SECONDS 才算做完（回复生成中 Stop 会短暂消失）。
    # 只点可完整解析的单个保存请求「Allow once」，路径必须是本轮输出文件；未知卡片不点。
    # 调用方（抢活脚本）要取消时会建 cancel_file：看到就按出错流程走，删掉侧聊天再退出
    idle = None
    while True:
        if cancel_file and Path(cancel_file).exists():
            raise RuntimeError("cancelled: another engine finished this image first")
        asks = approvals(page)
        if asks:
            if not all(scoped_save_approval(a, remote) for a in asks):
                raise RuntimeError("Muse approval shape was not recognized or was outside this run's single-image save scope; "
                                   f"was not clicked: {json.dumps(asks, ensure_ascii=False)[:1500]}")
            page.get_by_role("button", name="Allow once", exact=True).first.click()
            approved.append(asks[0]["detail"])
            idle = None
            continue
        replied = any(m["role"] == "assistant" and m["text"] for m in messages(page)[since:])
        if busy(page) or not replied:
            idle = None
        elif idle is None:
            idle = time.monotonic()
        elif time.monotonic() - idle >= IDLE_SECONDS:
            return messages(page)[since:]
        if time.monotonic() > deadline:
            raise RuntimeError("Muse 超时没做完")
        page.wait_for_timeout(3000)


def download(page, remote, folder):
    open_url(page, BASE + "/library/files")
    panel = page.get_by_test_id("hatch-library-allfiles-panel")
    for part in remote.removeprefix("/home/hatch/").split("/"):
        panel.get_by_text(part, exact=True).first.click()
        page.wait_for_timeout(1500)
    with page.expect_download(timeout=60000) as info:
        page.get_by_role("button", name="Download", exact=True).click()
    target = folder / info.value.suggested_filename
    info.value.save_as(str(target))
    return target


def fingerprint(file):
    # 解码后像素的 sha256，换格式也认得出是同一张图（和 imgtool.py 的 fp 一致）
    with Image.open(file) as image:
        rgba = image.convert("RGBA")
        return hashlib.sha256(f"{rgba.width}x{rgba.height}".encode() + rgba.tobytes()).hexdigest()


def generate(args):
    start = time.monotonic()
    prompt = (Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else args.prompt).strip()
    if not prompt:
        raise ValueError("empty prompt")
    # Parent first, then the prompt. Muse is not asked to create this directory.
    out = prepare_local_output(args.out)
    with tempfile.TemporaryDirectory(prefix=".muse-image-", dir=out.parent) as tmp:
        work = Path(tmp)
        mark_run_dir(work)
        refs, ref_hashes = [], set()
        for index, ref in enumerate(args.ref, 1):
            # 参考图换成唯一上传名，云端同名文件不会被改名
            staged = work / f"ref{index}-{secrets.token_hex(6)}{Path(ref).suffix}"
            staged.write_bytes(Path(ref).read_bytes())
            ref_hashes.add(fingerprint(staged))
            refs.append(staged)
        remote = f"{REMOTE_DIR}/img-{int(time.time() * 1000)}-{secrets.token_hex(4)}.png"
        text = ("运行环境：你在自己的云端电脑上运行，读不到用户本机的文件。\n"
                "任务：用你自己的出图工具生成 1 张图，只调用一次出图工具，不要上网找图，不要复制或改用任何现成图片。\n"
                f"画面比例 {args.aspect}。" + (f"附件 {'、'.join(r.name for r in refs)} 是参考图，按提示词参照它们。" if refs else "") + "\n"
                f"提示词（两行标记之间的原文，逐字使用，不改写、不增减）：\n<<<PROMPT\n{prompt}\nPROMPT>>>\n"
                f"生成后只把 PNG 写入这个精确路径，不要创建目录，不要先写临时文件再改名，不要另存其它文件：{remote}。最后一条回复单独一行写「产出文件：{remote}」。\n"
                "出图工具失败或做不了就写明原因后结束，不要交别的图。")
        approved = []
        with browser() as page:
            chat = None
            try:
                chat, since = send(page, text, refs)
                # Muse 会去掉标题两头的空格。改名失败只打一条警告，出图继续。
                rename_or_continue(page, chat, (args.title or f"imagegen-swarm：{prompt[:24]}").strip())
                open_url(page, f"{BASE}/thread/{chat}")
                replies = wait_done(page, since, start + args.timeout / 1000, approved, args.cancel_file, remote)
                last = next((m["text"] for m in reversed(replies) if m["role"] == "assistant"), "")
                delivered = [item.rstrip(".,);]\"'") for item in re.findall(r"产出文件[:：]\s*(\S+)", last)]
                if not any(canonical_output_path(item) == canonical_output_path(remote) for item in delivered):
                    raise RuntimeError(f"Muse 没交出 {remote}；最后回复：{last[-1500:]}")
                saved = download(page, remote, work)
                if fingerprint(saved) in ref_hashes:
                    raise RuntimeError("stale output: matches a reference image")
                with Image.open(saved) as image:
                    image.save(out, "PNG")
                    width, height = image.width, image.height
            except BaseException as error:
                # 只删本轮已经记下编号的侧聊天。编号还没拿到时不动其它聊天。
                try:
                    if chat:
                        delete(page, chat)
                except Exception as cleanup:
                    raise RuntimeError(f"{error}；另外：{cleanup}") from error
                raise
            if chat:
                delete(page, chat)
    return {"status": "ok", "path": str(out), "engine": "muse", "source_path": remote, "width": width, "height": height,
            "aspect": args.aspect, "approved": approved, "bytes": out.stat().st_size, "elapsed_seconds": round(time.monotonic() - start)}


def main():
    parser = argparse.ArgumentParser(prog="muse-image.py")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--out")
    parser.add_argument("--ref", action="append", default=[])
    parser.add_argument("--aspect", default="1:1", choices=RATIOS)
    parser.add_argument("--title", help="侧聊天标题，用户在 Muse 里看得见")
    parser.add_argument("--timeout", type=float, default=900000, help="毫秒")
    parser.add_argument("--cancel-file", help="这个文件出现时放弃本张、删掉侧聊天后退出（抢活脚本用）")
    parser.add_argument("--login", action="store_true", help="打开有界面的浏览器，让用户自己登录 Muse")
    parser.add_argument("--list-chats", action="store_true", help="列出侧聊天（体检和测试用）")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.login:
        with browser(headless=False, create_profile=True) as page:
            page.goto(BASE + "/", wait_until="domcontentloaded")
            composer(page).wait_for(state="visible", timeout=LOGIN_WAIT_MS)
        print(json.dumps({"status": "ok", "logged_in": True}))
        return
    if args.list_chats:
        with browser() as page:
            print(json.dumps({"status": "ok", "chats": side_chats(page)}, ensure_ascii=False))
        return
    if not args.out or bool(args.prompt) == bool(args.prompt_file):
        parser.error("require --out and exactly one of --prompt / --prompt-file")
    if Path(args.out).suffix.lower() != ".png":
        parser.error("--out extension must be .png")
    try:
        print(json.dumps(generate(args), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "error", "engine": "muse", "reason": str(error)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
帖子评论智能审核脚本
- 筛选"待审核"评论
- 逐条用 rules.json 检测内容
- 命中规则 → 拒绝，否则 → 通过
- 每轮结束输出统计
"""
import os, sys, re, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from playwright.sync_api import sync_playwright

OTP = sys.argv[1] if len(sys.argv) > 1 else ""
BASE_URL = "https://staff.bluemv.net/d.php"
USERNAME = "wulongcha"
PASSWORD = "wulongcha"
SKILL_ROOT = Path(__file__).parent.parent

# ── 加载审核规则 ──────────────────────────────────────────
def load_rules():
    # 优先用 internal-admin-playwright 本地规则，fallback 到通用审核
    for path in [
        SKILL_ROOT / "references" / "rules.json",
        Path.home() / ".openclaw/skills/tongyong-shenhe/rules.json",
    ]:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            rules = [r for r in data["rules"] if r.get("enabled")]
            print(f"已加载规则文件: {path}")
            return rules
    return []

def check_content(text, rules):
    """返回 (是否拒绝, 拒绝原因)"""
    for rule in rules:
        for pattern in rule.get("patterns", []):
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    return True, f"{rule['name']}: {rule['reason']}"
            except re.error:
                pass
    return False, ""

# ── 主流程 ────────────────────────────────────────────────
rules = load_rules()
print(f"共 {len(rules)} 条启用规则: {[r['id'] for r in rules]}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300, args=["--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()

    # 登录（跟最初能用的 diag_login.py 完全一样）
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    page.locator('input[name="username"]').fill(USERNAME)
    page.wait_for_timeout(300)
    page.locator('input[name="password"]').fill(PASSWORD)
    page.wait_for_timeout(300)
    page.locator('input[name="card_num"]').fill(OTP)
    page.wait_for_timeout(300)
    # 先截一张登录前的图
    page.screenshot(path="/tmp/pre_login.png")
    # 填完所有字段后，用 JS 直接提交表单并打印服务器响应
    result = page.evaluate("""
        () => {
            var form = document.querySelector('form[action*="dologin"]');
            if (!form) return '表单未找到';
            var fd = new FormData(form);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', form.action, false);
            xhr.send(fd);
            return '状态:' + xhr.status + '响应:' + xhr.responseText.substring(0, 300);
        }
    """)
    print(f"登录响应: {result}")
    page.wait_for_timeout(3000)
    page.screenshot(path="/tmp/post_login.png")
    print(f"登录后: {page.title()} URL={page.url}")
    if "code=login" in page.url or page.locator('input[name="username"]').count() > 0:
        body = page.inner_text("body")
        print(f"❌ 登录失败: {body[:200]}")
        page.screenshot(path="/tmp/login_fail.png", full_page=True)
        raise SystemExit("登录失败")
    print(f"登录成功: {page.title()}")

    # 导航到帖子评论
    page.get_by_text("帖子社区").first.click()
    page.wait_for_timeout(1000)
    page.get_by_text("帖子评论").first.click()
    page.wait_for_timeout(4000)

    frame = next((f for f in page.frames if "postcomment" in f.url), None)
    if not frame:
        print("❌ 未找到帖子评论 frame")
        browser.close()
        sys.exit(1)
    print("✅ 进入帖子评论页面")

    total_reviewed = 0
    total_pass = 0
    total_reject = 0
    round_num = 0
    start_time = time.time()

    while True:
        round_num += 1
        print(f"\n{'─'*50}")
        print(f"[第{round_num}轮] 筛选待审核评论...")

        frame.goto("https://staff.bluemv.net/d.php?mod=postcomment&code=index", wait_until="domcontentloaded")
        frame.wait_for_timeout(2000)

        # layui 下拉框：点击状态选择框标题展开，再点击"待审核"选项
        status_select = frame.locator(".layui-form-select").first
        status_select.locator(".layui-select-title").click()
        frame.wait_for_timeout(500)
        frame.locator("dd[lay-value='0']").first.click()
        frame.wait_for_timeout(500)

        # 点确定
        frame.get_by_text("确定").click()
        frame.wait_for_timeout(3000)
        print(f"  筛选完成，URL: {frame.url}")
        # 调试：打印所有行的状态列
        all_rows = frame.locator("table tbody tr").all()
        print(f"  表格共 {len(all_rows)} 行")
        for i, r in enumerate(all_rows[:5]):
            try:
                cells = r.locator("td").all()
                status = cells[8].inner_text().strip() if len(cells) > 8 else "?"
                content_txt = cells[5].inner_text().strip() if len(cells) > 5 else "?"
                print(f"  行{i+1}: 状态={status!r} 内容={content_txt[:20]!r}")
            except Exception as e:
                print(f"  行{i+1}: 异常={e}")

        # 只抓待审核的行（col[8]=="待审核"），且未处理过
        all_rows = frame.locator("table tbody tr").all()
        pending_rows = []
        for row in all_rows:
            try:
                cells = row.locator("td").all()
                if len(cells) >= 9:
                    status = cells[8].inner_text().strip()
                    row_id = cells[1].inner_text().strip()
                    if status == "待审核" and row_id not in processed_ids:
                        pending_rows.append((row, row_id))
            except: pass

        if not pending_rows:
            print("✅ 无待审核评论（已全处理完）")
            break

        print(f"本轮找到 {len(pending_rows)} 条待审核（累计已处理: {len(processed_ids)}条）")

        round_pass = 0
        round_reject = 0

        for i, (row, row_id) in enumerate(pending_rows):
            try:
                cells = row.locator("td").all()
                txt = cells[5].inner_text().strip()       # col[5] = 留言内容
                op_cell = cells[11]                       # col[11] = 操作列

                should_reject, reason = check_content(txt, rules)
                event = "reject" if should_reject else "pass"

                if should_reject:
                    print(f"  ❌ [{row_id}] {txt[:25]!r} → 拒绝 ({reason[:40]})")
                else:
                    print(f"  ✅ [{row_id}] {txt[:25]!r} → 通过")

                # 方法1：Playwright 直接 click（force 绕过拦截）
                btn = frame.locator(f"a[lay-event='{event}'][data-pk='{row_id}']").first
                try:
                    btn.click(force=True, timeout=3000)
                    frame.wait_for_timeout(500)
                    # 处理确认弹窗
                    try:
                        page.locator(".layui-layer-btn0").first.click(timeout=2000)
                    except: pass
                    frame.wait_for_timeout(1000)
                    clicked = True
                except Exception as e:
                    print(f"    click失败: {e}，改用JS")
                    # 方法2：JS 强制触发 + layui event
                    clicked = frame.evaluate(f"""
                        () => {{
                            var btn = document.querySelector('a[lay-event="{event}"][data-pk="{row_id}"]');
                            if (!btn) return false;
                            btn.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true}}));
                            return true;
                        }}
                    """)
                    frame.wait_for_timeout(1000)
                    if clicked:
                        try:
                            page.locator(".layui-layer-btn0").first.click(timeout=2000)
                        except: pass
                        frame.wait_for_timeout(1000)
                    processed_ids.add(row_id)
                    if should_reject:
                        round_reject += 1
                    else:
                        round_pass += 1
                else:
                    print(f"  ⚠️  [{row_id}] 未找到按钮")

            except Exception as e:
                print(f"  ⚠️  [{i+1}] 处理异常: {e}")
                continue

            except Exception as e:
                print(f"  ⚠️  [{i+1}] 处理异常: {e}")
                continue

        total_reviewed += round_pass + round_reject
        total_pass += round_pass
        total_reject += round_reject

        print(f"\n[第{round_num}轮统计] 审核 {round_pass+round_reject} 条 | ✅ 通过 {round_pass} | ❌ 拒绝 {round_reject}")

        if round_pass + round_reject == 0:
            print("本轮无新处理，退出循环")
            break

        # 每轮处理后等待页面刷新
        frame.wait_for_timeout(2000)

    # ── 最终统计 ──────────────────────────────────────────
    elapsed = int(time.time() - start_time)
    mins, secs = divmod(elapsed, 60)
    print(f"\n{'='*50}")
    print(f"🎉 本次审核完成！")
    print(f"   📋 共审核: {total_reviewed} 条")
    print(f"   ✅ 通过:   {total_pass} 条")
    print(f"   ❌ 拒绝:   {total_reject} 条")
    print(f"   ⏱️  耗时:   {mins}分{secs}秒")
    print(f"{'='*50}")

    page.screenshot(path="/tmp/review_final.png", full_page=True)
    print("截图已保存: /tmp/review_final.png")
    browser.close()

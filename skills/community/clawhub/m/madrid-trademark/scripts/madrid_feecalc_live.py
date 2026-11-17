#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
madrid_feecalc_live.py — 用真实浏览器驱动 WIPO 官方规费计算器，取得逐缔约方权威金额。

用途
----
单独规费（individual fee）属易变数据。本脚本直接驱动 WIPO Fee Calculator
(https://madrid.wipo.int/feecalcapp/) 完成一次真实测算，输出：
  · Basic fee / Fees of contracting parties / Complementary fee / Grand Total
  · 「Fees of contracting parties」明细表中每一缔约方的逐国金额（含 Calculation 原文串）

用于：① 复核 references/madrid-fees.md 内置值是否仍然有效；
      ② 多缔约方一次性核算，替代逐国查表与手工加总；
      ③ 出现金额争议时给出可复核的官方证据；
      ④ 用 --date 核算跨费率生效日的两套预算（生效前 / 生效后）。

前置条件
--------
· Python 3.10+，仅依赖 playwright（pip install playwright）。
· 需要 chromium。若 playwright 自带浏览器未下载，先执行 `playwright install chromium`；
  脚本亦会自动在 %LOCALAPPDATA%\\ms-playwright 下查找已存在的 chrome.exe。

用法
----
    py madrid_feecalc_live.py --origin US --classes 1 --countries JP,ID,IL
    py madrid_feecalc_live.py --origin US --classes 1 --countries JP,ID,IL --colour
    py madrid_feecalc_live.py --origin CN --classes 3 --countries DE,FR --collective
    py madrid_feecalc_live.py --origin US --classes 1 --countries JP,ID,IL --date 2026/11/01

参数
----
--origin      原属局缔约方二字码（默认 US）。决定第 9 条之六(1)(b) 保全条款是否触发。
--classes     商品/服务类别数（默认 1）。
--countries   逗号分隔的指定缔约方二字码；省略表示不勾选、仅输出基本费。
--date        计费日期 YYYY/MM/DD（默认当日）。规费调整按该日期生效，跨生效日应分别核算。
--colour      商标为彩色（基本费 653 -> 903）。
--collective  集体/证明/保证商标（部分缔约方费率不同）。
--dump        将结果页 HTML 另存为指定文件，便于留痕。
--headful     非无头模式，便于人工观察。

实现要点（踩过的坑，勿改回）
----------------------------
· 该计算器是 JSF(PrimeFaces) 应用，缔约方清单与结果均由 JS 触发渲染，**HTTP 抓取拿不到**，
  必须真实浏览器驱动。
· 每勾选一个缔约方即触发 AJAX 重绘 feeForm，单次点击会被吞 → select_codes() 内置
  「勾选 → 回读已勾集合 → 未生效者补勾」最多 4 轮重试，并以「已勾选 N / M」判成败。
· Date 字段是只读 p:calendar 输入框且**未绑定 AJAX 监听**，值随表单提交生效；
  因此必须在全部勾选完成、点击 Calculate **之前**写入，否则会被重绘冲掉。
  校验办法：用 --date 2020/01/01 跑一次，若金额与当期不同则说明日期确实生效。

退出码：0 成功；1 浏览器不可用/页面异常；2 存在未能勾选的缔约方代码。

注意：计算器输出为估算值，最终以国际局缴费通知为准；汇率波动可能导致实际扣款差异。
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

URL = "https://madrid.wipo.int/feecalcapp/"


def find_chrome():
    """返回可用的 chromium 可执行文件路径；找不到返回 None（交由 playwright 默认解析）。"""
    local = os.environ.get("LOCALAPPDATA", "")
    root = os.path.join(local, "ms-playwright") if local else ""
    if root and os.path.isdir(root):
        for d in sorted(os.listdir(root), reverse=True):
            for rel in (os.path.join("chrome-win64", "chrome.exe"),
                        os.path.join("chrome-win", "chrome.exe")):
                p = os.path.join(root, d, rel)
                if os.path.isfile(p):
                    return p
    return None


def selected_count(text):
    m = re.search(r"Selected Contracting Parties\s*\d+\s*/\s*\d+", text)
    return m.group(0) if m else "?"


def click_code(pg, code):
    """勾选一个缔约方。计算器每次勾选都会 AJAX 重绘 feeForm，故须逐个重新查询。"""
    return pg.evaluate(
        """code => {
            const spans = Array.from(document.querySelectorAll('span.cb-cp'));
            for (const s of spans) {
                if ((s.textContent || '').trim() === code) {
                    const box = s.parentElement.querySelector('input[type=checkbox]');
                    if (!box) return false;
                    if (box.checked) return 'already';
                    box.click();
                    return true;
                }
            }
            return false;
        }""",
        code,
    )


def checked_codes(pg):
    """返回当前已勾选的缔约方二字码集合。"""
    return set(
        pg.evaluate(
            """() => Array.from(document.querySelectorAll('span.cb-cp'))
                 .filter(s => { const b = s.parentElement.querySelector('input[type=checkbox]');
                                return b && b.checked; })
                 .map(s => (s.textContent || '').trim())"""
        )
    )


def select_codes(pg, codes, passes=4):
    """逐国勾选并校验；单次点击可能被 AJAX 重绘吞掉，故多轮重试至全部生效。"""
    for rnd in range(1, passes + 1):
        done = checked_codes(pg)
        pending = [c for c in codes if c not in done]
        if not pending:
            return True, []
        if rnd > 1:
            print("  · 第 %d 轮补勾：%s" % (rnd, ", ".join(pending)))
        for c in pending:
            click_code(pg, c)
            pg.wait_for_timeout(1400)
        print("  · 已勾选 %d / %d" % (len(checked_codes(pg) & set(codes)), len(codes)))
    done = checked_codes(pg)
    return False, [c for c in codes if c not in done]


def main():
    ap = argparse.ArgumentParser(description="WIPO 马德里规费计算器实时核算")
    ap.add_argument("--origin", default="US", help="原属局缔约方二字码，默认 US")
    ap.add_argument("--classes", default="1", help="类别数，默认 1")
    ap.add_argument("--countries", default="", help="逗号分隔的指定缔约方二字码")
    ap.add_argument("--date", default="", help="计费日期 YYYY/MM/DD（默认当日）")
    ap.add_argument("--colour", action="store_true", help="彩色商标")
    ap.add_argument("--collective", action="store_true", help="集体/证明/保证商标")
    ap.add_argument("--dump", default="", help="结果页 HTML 另存路径")
    ap.add_argument("--headful", action="store_true", help="非无头模式")
    args = ap.parse_args()

    codes = [c.strip().upper() for c in args.countries.split(",") if c.strip()]

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("缺少依赖：请先 pip install playwright，并执行 playwright install chromium")
        return 1

    exe = find_chrome()
    kw = {"headless": not args.headful}
    if exe:
        kw["executable_path"] = exe

    with sync_playwright() as p:
        try:
            b = p.chromium.launch(**kw)
        except Exception as e:
            print("浏览器启动失败：%s" % e)
            print("提示：执行 playwright install chromium，或用 --headful 观察。")
            return 1
        pg = b.new_page(viewport={"width": 1400, "height": 1200})
        pg.goto(URL, wait_until="networkidle", timeout=120000)
        pg.wait_for_timeout(1500)

        pg.select_option('select[id$="j_idt127:input"]', "EN")   # New application
        pg.wait_for_timeout(2500)
        pg.select_option('select[id$="j_idt203:input"]', args.origin)
        pg.wait_for_timeout(2500)
        pg.select_option('select[id$="j_idt224:input"]', str(args.classes))
        pg.wait_for_timeout(3500)

        if args.collective:
            pg.evaluate("""() => { const bs=Array.from(document.querySelectorAll('input[type=checkbox]'));
                for (const b of bs) { const l=(b.closest('label')||b.parentElement||document.body).innerText||'';
                    if (/collective|certification|guarantee/i.test(l) && !b.checked) { b.click(); return true; } }
                return false; }""")
            pg.wait_for_timeout(1500)
        if args.colour:
            pg.evaluate("""() => { const bs=Array.from(document.querySelectorAll('input[type=checkbox]'));
                for (const b of bs) { const l=(b.closest('label')||b.parentElement||document.body).innerText||'';
                    if (/colou?r/i.test(l) && !b.checked) { b.click(); return true; } }
                return false; }""")
            pg.wait_for_timeout(1500)

        ok, failed = select_codes(pg, codes)
        print("  · %s | %s" % ("全部勾选成功" if ok else "存在未勾选项",
                               selected_count(pg.inner_text("body"))))

        # Date 为只读 p:calendar 输入框且未绑定 AJAX 监听：值随表单提交生效，
        # 因此必须在全部勾选完成、点击 Calculate 之前写入（否则会被重绘冲掉）。
        if args.date:
            written = pg.evaluate(
                """d => {
                    const i = document.querySelector('input[id$="j_idt184:input_input"]');
                    if (!i) return false;
                    i.value = d;
                    return true;
                }""",
                args.date,
            )
            cur = pg.input_value('input[id$="j_idt184:input_input"]')
            print("  · 计费日期：%s（请求 %s，写入 %s）" % (cur, args.date, "成功" if written else "失败"))
            if cur != args.date:
                print("  警告：日期未写入，结果仍按 %s 的费率计算" % cur)

        pg.locator("text=Calculate").first.click()
        pg.wait_for_timeout(6000)

        # 展开全部 Details，取逐缔约方明细
        n = pg.locator("text=Details").count()
        for i in range(n):
            try:
                pg.locator("text=Details").nth(i).click()
                pg.wait_for_timeout(1200)
            except Exception:
                pass

        txt = pg.inner_text("body")
        if args.dump:
            open(args.dump, "w", encoding="utf-8").write(pg.content())

        print("\n===== WIPO Fee Calculator 结果 =====")
        print("原属局：%s | 类别数：%s | 计费日期：%s | 彩色：%s | 集体商标：%s"
              % (args.origin, args.classes, args.date or "当日", args.colour, args.collective))
        for line in ("Basic fee", "Fees of contracting parties", "Complementary fee",
                     "Supplementary fee", "Grand Total (CHF)"):
            m = re.search(re.escape(line) + r"\s*\n+\s*([\d,]+\.\d{2})", txt)
            if m:
                print("%-28s %s CHF" % (line, m.group(1)))

        i = txt.find("Contracting Party\tCalculation")
        if i < 0:
            i = txt.find("Contracting Party")
        if i >= 0:
            print("\n----- 逐缔约方明细（计算器原文）-----")
            print(txt[i:txt.find("Total (CHF)", i) + 40])
        b.close()

    if failed:
        print("\n未能勾选的缔约方代码：%s" % ", ".join(failed))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

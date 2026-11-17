# -*- coding: utf-8 -*-
"""回读草稿，核对它到底存进去了什么（这是唯一验收判据）。

用法
----
    python gzh_verify.py --appmsgid 100000123 --profile ./gzh-profile --port 9333
    python gzh_verify.py --appmsgid 100000123 --expect-title "文章标题" --profile ./gzh-profile --port 9333

为什么要回读
------------
草稿接口返回 `ret=0` / 拿到 appmsgid 都不算成功——正文可能被剥了样式、图片可能裂了、
摘要可能被自动截正文覆盖。唯一可信的做法是**打开编辑器把内容读回来**：
打开 `appmsg_edit_v2&action=edit&appmsgid=<id>`，读 `div.ProseMirror` 的 innerText
（编辑器在 iframe 里，所以要遍历所有 frame），核对三件事：

  1. 标题是否与预期一致
  2. 正文是否非空（并给出字符数）
  3. 正文里图片有多少张（并统计自然宽度为 0 的裂图）

三项都通过会打印 `VERIFY_OK`，否则打印 `VERIFY_FAIL` 并以退出码 1 结束。

另加一项可选核对：`--expect-cover`。封面是存在草稿列表字段里的（不在正文编辑器里），
所以走草稿列表接口读 `cover` 字段判断。给了这个开关就一并计入成败。
"""

import argparse
import json
import os
import re
import sys
import time

DEFAULT_PROFILE = os.path.join(".", "gzh-profile")
DEFAULT_PORT = 9333

EDIT_URL = ("https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit"
            "&isNew=0&type=77&appmsgid=%s&token=%s&lang=zh_CN")

TITLE_SELECTORS = (
    "#title",
    "textarea#title",
    "input[name='title']",
    "#js_title",
    ".js_title_elem",
    ".js_title",
)

PROBE_JS = """() => {
  const pick = (sels) => {
    for (const s of sels) {
      const el = document.querySelector(s);
      if (el) {
        const v = (el.value !== undefined && el.value !== null && el.value !== '') ? el.value : el.innerText;
        if (v && v.trim()) return v.trim();
      }
    }
    return '';
  };
  // 标题也是一个 ProseMirror（小、位置靠上），所以要把所有候选都拿出来，
  // 由调用方按高度挑出真正的正文编辑器。
  const eds = [...document.querySelectorAll('div.ProseMirror, #ueditor_0, #js_content')].map(el => {
    const r = el.getBoundingClientRect();
    const t = (el.innerText || '').trim();
    const list = [...el.querySelectorAll('img')];
    // 编辑器里还挂着没 src 的占位 img（不是正文图片），只统计真正有 src 的
    const withSrc = list.filter(x => (x.getAttribute('src') || '').trim());
    return {
      w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top),
      textLen: t.length, textHead: t.slice(0, 120),
      imgCount: withSrc.length,
      broken: withSrc.filter(x => !x.naturalWidth).length,
      imgHead: withSrc.map(x => x.getAttribute('src') || '').filter(Boolean).slice(0, 3)
    };
  });
  return {title: pick(%s), eds: eds};
}""" % json.dumps(list(TITLE_SELECTORS), ensure_ascii=False)


def pick_body(info):
    """从一页的候选里挑正文编辑器：优先高瘦区域（正文），其次文字最多。"""
    eds = (info or {}).get("eds") or []
    tall = [e for e in eds if e.get("h", 0) >= 60]
    if tall:
        return max(tall, key=lambda e: e.get("h", 0) * e.get("w", 0))
    if eds:
        return max(eds, key=lambda e: e.get("textLen", 0))
    return None


COVER_JS = """async ([tk, aid]) => {
  const r = await fetch(`/cgi-bin/appmsg?begin=0&count=100&type=77&action=list_card&token=${tk}&lang=zh_CN&f=json&ajax=1`,
                        {credentials: 'include'});
  const j = await r.json();
  const items = (j.app_msg_info && j.app_msg_info.item) || j.item || [];
  for (const i of items) {
    const id = String(i.app_id || i.appmsgid || '');
    if (id === String(aid)) {
      const m = (i.multi_item && i.multi_item[0]) || {};
      return {cover: i.cover || m.cover || '', digest: (m.digest || i.digest || '')};
    }
  }
  return null;
}"""


def read_cover(page, token, appmsgid):
    """从草稿列表接口读这篇草稿的封面 URL（列表接口有速率限制，空了重试）。"""
    for _ in range(5):
        try:
            got = page.evaluate(COVER_JS, [token, appmsgid])
        except Exception:
            got = None
        if got is not None:
            return got
        time.sleep(5)
    return None


def main():
    ap = argparse.ArgumentParser(
        description="回读公众号草稿并核对标题/正文/图片（唯一验收判据）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--appmsgid", required=True, help="草稿 id（存稿时打印的 appmsgid）")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="浏览器数据目录（默认 ./gzh-profile）")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT, help="远程调试端口（默认 9333）")
    ap.add_argument("--expect-title", default="", help="预期标题，用来判断是否一致")
    ap.add_argument("--expect-images", type=int, default=-1, help="预期图片张数（不给则不核对）")
    ap.add_argument("--expect-cover", action="store_true",
                    help="额外核对封面是否已写入（封面存在列表字段里，不在正文编辑器里）")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    p = sync_playwright().start()
    try:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:%d" % args.port)
    except Exception as e:
        p.stop()
        raise SystemExit("错误：连不上端口 %d 上的浏览器实例（%s）。\n"
                         "请先运行：python gzh_login.py --profile ./gzh-profile --port %d"
                         % (args.port, e, args.port))

    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()
    try:
        page.goto("https://mp.weixin.qq.com/", wait_until="domcontentloaded", timeout=60000)
        token = None
        for _ in range(8):
            time.sleep(2)
            m = re.search(r"token=(\d+)", page.url or "")
            if m:
                token = m.group(1)
                break
            try:
                body = page.inner_text("body")
            except Exception:
                body = ""
            if "扫一扫" in body or "使用账号登录" in body:
                raise SystemExit("错误：登录态已失效，请重新运行 gzh_login.py。")
        if not token:
            m = re.search(r"token=(\d+)", page.content() or "")
            token = m.group(1) if m else None
        if not token:
            raise SystemExit("错误：取不到 token，请确认浏览器里已登录公众号后台。")
        print("[%s] token=%s 打开草稿 %s 的编辑器…"
              % (time.strftime("%H:%M:%S"), token, args.appmsgid))

        page.goto(EDIT_URL % (args.appmsgid, token), wait_until="domcontentloaded", timeout=60000)
        best_title, best_body = "", None
        for _ in range(15):  # 编辑器是异步渲染的，轮询到正文出现为止
            time.sleep(2)
            for fr in page.frames:
                try:
                    info = fr.evaluate(PROBE_JS)
                except Exception:
                    continue
                if not info:
                    continue
                if info.get("title") and not best_title:
                    best_title = info["title"]
                cand = pick_body(info)
                if cand and (best_body is None or cand.get("h", 0) * cand.get("w", 0)
                             > best_body.get("h", 0) * best_body.get("w", 0)):
                    best_body = cand
            if best_body and best_body.get("textLen", 0) >= 0 and best_body.get("h", 0) >= 60:
                break

        best_body = best_body or {}
        title = best_title or ""
        text_len = best_body.get("textLen", 0) or 0
        img_count = best_body.get("imgCount", 0) or 0
        broken = best_body.get("broken", 0) or 0

        ok_title = True
        if args.expect_title:
            ok_title = (title.strip() == args.expect_title.strip())
        ok_body = text_len > 0
        ok_img = (args.expect_images < 0) or (img_count == args.expect_images)

        print("正文开头：%s" % (best_body.get("textHead", "") or "（空）").replace("\n", " "))
        print("[1/3] 标题核对：%s%s" % (
            "通过" if ok_title else "不通过",
            (" —— 实际「%s」 / 期望「%s」" % (title, args.expect_title)) if args.expect_title
            else (" —— 读到「%s」" % title if title else " —— 没读到标题")))
        print("[2/3] 正文非空：%s —— %d 字符" % ("通过" if ok_body else "不通过", text_len))
        print("[3/3] 图片数量：%s —— %d 张%s" % (
            "通过" if ok_img else "不通过", img_count,
            ("（其中裂图 %d 张）" % broken) if broken else ""))
        heads = best_body.get("imgHead") or []
        if heads:
            print("      正文图片：" + " | ".join(h[:80] for h in heads))

        ok_cover = True
        if args.expect_cover:
            info = read_cover(page, token, args.appmsgid)
            cover = (info or {}).get("cover", "") if info else ""
            ok_cover = bool(cover)
            print("[4/4] 封面核对：%s —— %s" % (
                "通过" if ok_cover else "不通过",
                ("已写入 " + cover[:90]) if cover else "草稿上没有封面"))

        all_ok = ok_title and ok_body and ok_img and ok_cover
        print("VERIFY_OK" if all_ok else "VERIFY_FAIL")
        return 0 if all_ok else 1
    finally:
        try:
            page.close()  # 只关自己的标签页，不关浏览器
        except Exception:
            pass
        try:
            p.stop()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())

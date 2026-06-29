#!/usr/bin/env python3

"""

browser_search.py — CDP 自动翻页搜索 · Auto-paginating Browser Search

======================================================================



通过 CDP（Chrome DevTools Protocol）自动打开搜索结果页 → 注入提取器 →

收集论文 → 翻页 → 重复，直到达到目标数量或无更多结果。



支持的数据库翻页机制：

  │ ieee                   │ URL 参数 pageNumber 递增      │

  │ acm                    │ URL 参数 startPage 递增        │

  │ engineering_village    │ 点击 #next-page-top 按钮       │



用法：

  # IEEE / ACM（URL 编码查询，全自动）

  python browser_search.py --url "https://ieeexplore.ieee.org/search?..." --db ieee --count 50 -o memory/ieee_results.json

  python browser_search.py --url "https://dl.acm.org/action/doSearch?..." --db acm --count 30 -o memory/acm_results.json



  # EV（用户在浏览器里已完成搜索，脚本只负责提取+翻页）

  python browser_search.py --db engineering_village --count 25 -o memory/ev_results.json



依赖：

  - CDP HTTP 端点: http://127.0.0.1:18800

  - websocket-client（pip install websocket-client）

  - extractors/<db>.js 文件

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

import json

import re

import sys

import time

import urllib.request

import urllib.parse

from pathlib import Path



from utils.doi_utils import extract as _extract_doi



import sys, os




# ---------------------------------------------------------------------------

# 配置

# ---------------------------------------------------------------------------



CDP_BASE = "http://127.0.0.1:18800"

PAGE_LOAD_TIMEOUT = 20   # 页面加载最大等待秒数

EVAL_TIMEOUT = 10        # JS 执行最大等待秒数

EV_BETWEEN_PAGES = 3.0   # EV 翻页后等待秒数



# 各数据库翻页配置

PAGINATION = {

    "ieee": {

        "mode": "url_param",

        "param": "pageNumber",

        "first_value": 1,

    },

    "acm": {

        "mode": "url_param",

        "param": "startPage",

        "first_value": 0,

        "step_size": 25,           # ACM 每页条数（URL 中 pageSize）

    },

    "engineering_village": {

        "mode": "click",

        "selector": "#next-page-top",

    },

}





# ---------------------------------------------------------------------------

# CDP 工具

# ---------------------------------------------------------------------------



def _cdp_new_tab():

    """创建新标签页，返回 (tab_id, ws_url)。"""

    req = urllib.request.Request(f"{CDP_BASE}/json/new", method="PUT")

    resp = urllib.request.urlopen(req, timeout=10)

    tab = json.loads(resp.read().decode("utf-8"))

    ws_url = tab.get("webSocketDebuggerUrl")

    if not ws_url:

        raise RuntimeError("CDP: no webSocketDebuggerUrl in response")

    return tab.get("id"), ws_url





def _cdp_list_tabs():

    """列出所有打开的标签页，返回第一个页面类型的标签页。"""

    try:

        resp = urllib.request.urlopen(f"{CDP_BASE}/json/list", timeout=5)

        tabs = json.loads(resp.read().decode("utf-8"))

        # 过滤 devtools 页面，找第一个普通 page

        pages = [t for t in tabs if t.get("type") == "page"]

        return pages

    except Exception:

        return []





def _cdp_close_tab(tab_id):

    """关闭指定标签页。"""

    try:

        urllib.request.urlopen(f"{CDP_BASE}/json/close/{tab_id}", timeout=5)

    except Exception:

        pass





def _cdp_navigate_and_wait(ws, url, timeout=PAGE_LOAD_TIMEOUT):

    """在 WebSocket 连接上导航到 URL 并等待加载完成。"""

    import websocket



    ws.send(json.dumps({"id": 1, "method": "Page.enable"}))

    ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))

    ws.send(json.dumps({

        "id": 3, "method": "Page.navigate",

        "params": {"url": url},

    }))



    deadline = time.time() + timeout

    while time.time() < deadline:

        ws.settimeout(3)

        try:

            msg = ws.recv()

            data = json.loads(msg)

            if data.get("method") == "Page.loadEventFired":

                time.sleep(1.5)  # 给动态内容渲染时间

                return True

        except (websocket.WebSocketTimeoutException, json.JSONDecodeError,

                ConnectionResetError, BrokenPipeError):

            pass

        except Exception:

            time.sleep(0.5)



    return False  # 超时





def _cdp_evaluate(ws, js_code, timeout=EVAL_TIMEOUT):

    """

    在页面中执行 JS 并返回结果。



    返回 (result_dict, error_msg)。

    成功时 error_msg 为 None，result_dict 是 JS 返回的对象。

    """

    import websocket



    eval_msg = {

        "id": 100,

        "method": "Runtime.evaluate",

        "params": {

            "expression": js_code,

            "returnByValue": True,

            "awaitPromise": True,

            "timeout": timeout * 1000,

        },

    }

    ws.send(json.dumps(eval_msg))



    deadline = time.time() + timeout + 5

    result = None

    error = None



    while time.time() < deadline:

        ws.settimeout(3)

        try:

            msg = ws.recv()

            data = json.loads(msg)



            if data.get("id") == 100:

                r = data.get("result", {}).get("result", {})

                if r.get("type") == "object":

                    result = r.get("value")

                elif r.get("type") == "string":

                    result = r.get("value")

                break



            if data.get("method") == "Runtime.exceptionThrown":

                exc = data.get("params", {}).get("exceptionDetails", {})

                error = exc.get("text", str(exc))[:300]

        except (websocket.WebSocketTimeoutException, json.JSONDecodeError,

                ConnectionResetError, BrokenPipeError):

            pass

        except Exception as e:

            error = str(e)[:200]

            break



    return result, error





def _cdp_click(ws, selector):

    """点击页面元素（用于 EV 翻页按钮）。"""

    import websocket



    click_js = (

        f"(function(){{"

        f"var el=document.querySelector('{selector}');"

        f"if(!el)return false;"

        f"el.click();"

        f"return true;"

        f"}})()"

    )

    eval_msg = {

        "id": 200,

        "method": "Runtime.evaluate",

        "params": {

            "expression": click_js,

            "returnByValue": True,

            "awaitPromise": False,

        },

    }

    ws.send(json.dumps(eval_msg))



    deadline = time.time() + 5

    while time.time() < deadline:

        ws.settimeout(3)

        try:

            msg = ws.recv()

            data = json.loads(msg)

            if data.get("id") == 200:

                r = data.get("result", {}).get("result", {})

                return r.get("value", False)

        except (websocket.WebSocketTimeoutException, json.JSONDecodeError,

                ConnectionResetError, BrokenPipeError):

            pass



    return False





# ---------------------------------------------------------------------------

# URL 翻页工具

# ---------------------------------------------------------------------------



def _next_page_url(current_url, pagination, page_num):

    """

    根据翻页配置修改 URL，返回下一页的 URL。



    page_num: 当前页码（对于 url_param 模式是页码序号；对于 startPage 是累积偏移）

    """

    parsed = list(urllib.parse.urlparse(current_url))

    query = dict(urllib.parse.parse_qsl(parsed[4], keep_blank_values=True))



    mode = pagination["mode"]

    if mode == "url_param":

        param = pagination["param"]

        query[param] = str(page_num)

    elif mode == "url_param_offset":

        # 用于 startPage 这种累积偏移模式

        param = pagination["param"]

        query[param] = str(page_num)



    parsed[4] = urllib.parse.urlencode(query, doseq=True)

    return urllib.parse.urlunparse(parsed)





# ---------------------------------------------------------------------------

# 去重

# ---------------------------------------------------------------------------



def _normalize(text):

    if not text:

        return ""

    t = text.lower()

    t = re.sub(r'[^\w\s]', ' ', t)

    t = re.sub(r'\s+', ' ', t).strip()

    return t





def _deduplicate(papers):

    """对论文列表去重（DOI 精确匹配 + 标题 token 重叠 ≥ 80%）。"""

    seen_dois = set()

    seen_titles = {}  # normalized_title → index



    result = []

    for paper in papers:

        # DOI 精确去重

        doi = _extract_doi(paper)

        if doi:

            if doi in seen_dois:

                continue

            seen_dois.add(doi)



        # 标题模糊去重

        title = _normalize(paper.get("title", ""))

        if title:

            tokens = set(title.split())

            duplicate = False

            for seen_title, idx in seen_titles.items():

                seen_tokens = set(seen_title.split())

                if not seen_tokens:

                    continue

                overlap = tokens & seen_tokens

                if len(overlap) / max(len(tokens), len(seen_tokens)) >= 0.80:

                    duplicate = True

                    # 保留引用数更高的那一篇

                    if paper.get("citations", 0) > result[idx].get("citations", 0):

                        result[idx] = paper

                    break

            if duplicate:

                continue

            seen_titles[title] = len(result)



        result.append(paper)



    return result





# ---------------------------------------------------------------------------

# 主搜索器

# ---------------------------------------------------------------------------



class BrowserSearcher:

    """通过 CDP 自动翻页搜索指定数据库。"""



    def __init__(self, db):

        self.db = db

        self.pagination = PAGINATION.get(db)

        if not self.pagination:

            raise ValueError(f"Unknown database: {db}. Supported: {list(PAGINATION)}")



        # 加载 extractor JS

        script_dir = Path(__file__).parent.parent

        js_path = script_dir / "extractors" / f"{db}.js"

        if not js_path.exists():

            raise FileNotFoundError(f"Extractor not found: {js_path}")

        self.extractor_js = js_path.read_text(encoding="utf-8")



    def search(self, url, target_count, output_path, use_active_tab=False):

        """

        执行自动翻页搜索。



        url: 搜索页 URL（click 模式时可为 None，表示使用当前标签页）

        target_count: 目标论文数量

        output_path: 结果 JSON 路径

        use_active_tab: 是否复用已有标签页（EV 手动搜索场景）

        """

        import websocket



        all_papers = []

        total_available = "?"

        page = 0

        current_url = url



        # --- 建立连接 ---

        if use_active_tab:

            # EV 场景：使用已有标签页

            pages = _cdp_list_tabs()

            if not pages:

                raise RuntimeError("No active browser tabs found. Is the browser running?")

            tab = pages[0]

            ws_url = tab.get("webSocketDebuggerUrl")

            if not ws_url:

                raise RuntimeError("Active tab has no debug URL")

            tab_id = tab.get("id")

            print(f"[{self.db}] Using active tab: {tab.get('title', 'Unknown')[:60]}")

        elif url:

            tab_id, ws_url = _cdp_new_tab()

        else:

            raise ValueError("Either --url or --use-active-tab is required")



        ws = None

        try:

            ws = websocket.create_connection(

                ws_url,

                timeout=PAGE_LOAD_TIMEOUT,

                suppress_origin=True,

            )



            if url and not use_active_tab:

                # 导航到第一页

                ok = _cdp_navigate_and_wait(ws, current_url)

                if not ok:

                    print(f"  ⚠️  Page load timeout, attempting extraction anyway...",

                          file=sys.stderr)



            # --- 逐页提取 ---

            while len(all_papers) < target_count:

                page += 1



                # 评估提取器

                result, err = _cdp_evaluate(ws, self.extractor_js)

                if err:

                    print(f"  ⚠️  Page {page}: JS error — {err[:200]}", file=sys.stderr)

                    break



                if not result or not isinstance(result, dict):

                    print(f"  [{self.db}] Page {page}: no results returned", file=sys.stderr)

                    break



                papers = result.get("papers", [])

                if not papers:

                    print(f"  [{self.db}] Page {page}: empty — stopping",

                          file=sys.stderr)

                    break



                page_count = len(papers)

                all_papers.extend(papers)

                total_available = result.get("totalResults", "?")

                title_sample = (papers[0].get("title", "") or "")[:50] if papers else "?"



                print(f"  [{self.db}] Page {page}: {page_count} papers "

                      f"(total collected: {len(all_papers)}/{total_available}) "

                      f"e.g. {title_sample}...",

                      file=sys.stderr)



                if len(all_papers) >= target_count:

                    break



                # 翻页

                mode = self.pagination.get("mode")

                if mode == "url_param":

                    param = self.pagination["param"]

                    if self.db == "acm":

                        # ACM: startPage 递增

                        parsed = dict(urllib.parse.parse_qsl(

                            urllib.parse.urlparse(current_url).query))

                        current_start = int(parsed.get("startPage", 0))

                        step = self.pagination.get("step_size", 25)

                        next_start = current_start + step

                    else:

                        # IEEE: pageNumber 递增

                        parsed = dict(urllib.parse.parse_qsl(

                            urllib.parse.urlparse(current_url).query))

                        current_page_int = int(parsed.get(param,

                            self.pagination["first_value"]))

                        next_start = current_page_int + 1



                    current_url = _next_page_url(current_url, self.pagination,

                                                  next_start)

                    ok = _cdp_navigate_and_wait(ws, current_url)

                    if not ok:

                        print(f"  ⚠️  Page {page+1}: navigation timeout",

                              file=sys.stderr)

                        break



                elif mode == "click":

                    clicked = _cdp_click(ws, self.pagination["selector"])

                    if not clicked:

                        print(f"  [{self.db}] Next page button not found/clickable — done",

                              file=sys.stderr)

                        break

                    # 等待 EV SPA 渲染下一页

                    time.sleep(EV_BETWEEN_PAGES)



        except Exception as e:

            print(f"  ❌ [{self.db}] {e}", file=sys.stderr)



        finally:

            if ws:

                try:

                    ws.close()

                except Exception:

                    pass

            if tab_id and not use_active_tab:

                _cdp_close_tab(tab_id)



        # --- 去重 ---

        original = len(all_papers)

        all_papers = _deduplicate(all_papers)

        if original != len(all_papers):

            print(f"  [{self.db}] Dedup: {original} → {len(all_papers)} papers",

                  file=sys.stderr)



        # --- 输出 ---

        output = {

            "database": self.db,

            "total_results": str(total_available),

            "count": len(all_papers),

            "pages_fetched": page,

            "papers": all_papers,

        }



        out_path = Path(output_path)

        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:

            json.dump(output, f, ensure_ascii=False, indent=2)



        print(f"[{self.db}] {len(all_papers)} papers saved → {out_path}")

        return output





# ---------------------------------------------------------------------------

# CLI

# ---------------------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(

        description="CDP auto-paginating search for IEEE/ACM/Engineering Village",

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog=f"""

Pagination modes by database:

  ieee                   URL param: &pageNumber=N  (increments by 1)

  acm                    URL param: &startPage=N    (increments by 25)

  engineering_village    Button click: #next-page-top



Examples:

  python browser_search.py --url "https://ieeexplore.ieee.org/..." --db ieee --count 50 -o r.json

  python browser_search.py --db engineering_village --count 25 -o r.json

        """,

    )

    parser.add_argument("--url",

                        help="Search results page URL (not needed for EV with --use-active-tab)")

    parser.add_argument("--db", required=True,

                        choices=list(PAGINATION.keys()),

                        help="Database to search")

    parser.add_argument("--count", "-c", type=int, required=True,

                        help="Target number of papers to collect")

    parser.add_argument("--output", "-o", required=True,

                        help="Output JSON file")

    parser.add_argument("--use-active-tab", action="store_true",

                        help="Use existing active browser tab (for EV manual search)")

    args = parser.parse_args()



    if not args.url and not args.use_active_tab:

        parser.error("Either --url or --use-active-tab is required")



    try:

        searcher = BrowserSearcher(args.db)

        searcher.search(

            url=args.url,

            target_count=args.count,

            output_path=args.output,

            use_active_tab=args.use_active_tab,

        )

    except Exception as e:

        print(f"❌ [{args.db}] {e}", file=sys.stderr)

        sys.exit(1)





if __name__ == "__main__":

    main()


#!/usr/bin/env python3
"""
Perplexity Web Automation — Search & Extract via Kimi WebBridge.

Proven flow (tested 2026-08-29; connection smoke-tested 2026-09-05):
  0. list_tabs precheck → real step before navigate: success:true with tabs:[]
     is healthy; "no extension connected" (or any non-success) aborts
  1. navigate → perplexity.ai
  2. snapshot → find textbox @e ref
  3. click textbox (focus it)
  4. fill textbox with query
  5. dispatch beforeinput + keydown + keyup Enter events
  6. wait 10-15s for answer
  7. click "查看更多" if present (expand collapsed answer)
  8. extract answer text from main element
  9. click "链接" tab, extract all source links
  10. switch back to answer tab, extract follow-up questions

Usage:
    result = perplexity_search("What are the best AI coding agents in 2026?")
    print(result["answer"])
    print(result["sources"])

For a task-specific WebBridge tab group:
    WEBBRIDGE_SESSION=hermes-bot-combination-research python perplexity_search.py "query"

Multi-query tasks: only the first query opens a tab (perplexity_batch_search uses
new_tab=(i == 0)); later queries must explicitly pass new_tab=False so subsequent
searches reuse the current tab in the same task session.

--------------------------------------------------------------------------
DESIGN CONSTRAINT: this file must stay dependency-free. Do not "deduplicate"
it against perplexity_toolkit.

Yes, it reimplements logic that also lives in perplexity_toolkit.search. That
overlap is deliberate, not technical debt. This script imports only the
standard library and shells out to curl, so it runs under any python3 with
nothing installed. The toolkit cannot: it needs its own package (config,
drivers, utils, i18n, verify) to be importable.

That difference is the entire point. This helper is part of the explicit
direct-browser route. Toolkit/CLI unavailability alone must never invoke it
automatically; the high-level skill must first obtain authorization for the
browser route. It remains dependency free so an already-authorized browser
task can still be diagnosed when the installed toolkit is not resolvable.

If you are here to merge the two implementations, the correct change is
usually none. If the shared logic genuinely needs to move, extract it into a
vendored stdlib-only module inside this scripts/ directory — do not reach into
the installed package.

Deliberate omission: there is no retry/backoff here (the toolkit has
_search_with_retry). A diagnostic tool should surface the raw failure rather
than mask it behind retries. If this script is ever promoted from "direct
browser diagnostic" to "general executor", revisit that decision explicitly
rather than adding retries by reflex.
--------------------------------------------------------------------------
"""

import json
import os
import subprocess
import time
import sys
import re

WEBBRIDGE_URL = "http://127.0.0.1:10086/command"
# Prefer one task-specific session per run. Set WEBBRIDGE_SESSION when several
# processes must continue the same authorized browser task.
SESSION = os.environ.get("WEBBRIDGE_SESSION", f"perplexity-web-{os.getpid()}")

_GROUNDING_REQUIREMENTS = """Requirements:
1. Cite sources with URLs
2. If no verified source, say so
3. For pricing: official page URLs only
4. Format as comparison table with Source URL column"""


def build_grounded_query(query):
    """Apply the shared source-grounding wrapper exactly once."""
    if "requirements:" in query.casefold() or "要求：" in query or "要求:" in query:
        return query
    return f"{query.rstrip()}\n{_GROUNDING_REQUIREMENTS}"


def _result(error=None, **fields):
    result = {
        "answer": None,
        "sources": [],
        "url": "",
        "title": "",
        "follow_ups": [],
        "session": SESSION,
        "verification": {
            "state": "unverified",
            "claim_support": "not_evaluated",
            "source_check": {},
        },
    }
    if error:
        result["error"] = error
    result.update(fields)
    return result


def wb(action, args=None):
    """Send a command to Kimi WebBridge."""
    payload = {"action": action, "session": SESSION}
    if args:
        payload["args"] = args
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", WEBBRIDGE_URL,
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return {"error": f"curl failed with exit code {result.returncode}"}
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": result.stdout}


def evaluate(code):
    """Run JS in the page and return the parsed value."""
    resp = wb("evaluate", {"code": code})
    val = resp.get("data", {}).get("value", "")
    if isinstance(val, str):
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val
    return val


def find_textbox_ref():
    """Find the textbox @e ref from the accessibility tree snapshot.
    
    The textbox has:
      role: "textbox"
      name: "输入 @ 以使用连接器" (varies by locale)
      value: "\\n"
      ref: @eNN
    """
    resp = wb("snapshot", {})
    tree = resp.get("data", {}).get("tree", "")
    s = json.dumps(tree, ensure_ascii=False, separators=(",", ":"))
    
    # Pattern: "role":"textbox","name":"...","value":"...","ref":"@eNN"
    for m in re.finditer(
        r'"role":"textbox","name":"[^"]*","value":"[^"]*","ref":"(@e\d+)"', s
    ):
        return m.group(1)
    
    # Fallback: find any element with role textbox
    for m in re.finditer(r'"role":"textbox"[^}]*"ref":"(@e\d+)"', s):
        return m.group(1)
    
    # Reverse: find ref near "textbox"
    for m in re.finditer(r'"ref":"(@e\d+)"', s):
        ref = m.group(1)
        idx = s.find(ref)
        context = s[max(0, idx - 200):idx + 50]
        if '"role":"textbox"' in context:
            return ref
    
    return None


def find_button_ref(button_text):
    """Find a button's @e ref by its text content."""
    resp = wb("snapshot", {})
    tree = resp.get("data", {}).get("tree", "")
    s = json.dumps(tree, ensure_ascii=False, separators=(",", ":"))
    
    # Pattern: "role":"button","name":"TEXT","ref":"@eNN"
    for m in re.finditer(
        rf'"role":"button","name":"[^"]*{re.escape(button_text)}[^"]*","ref":"(@e\d+)"',
        s
    ):
        return m.group(1)
    
    return None


def perplexity_search(query, wait_seconds=15, expand=True, new_tab=None):
    """
    Search Perplexity AI and extract results.
    
    Args:
        query: Search query string
        wait_seconds: How long to wait for answer generation
        expand: Whether to click "查看更多" to expand full answer
        new_tab: Whether to open in a new tab. If omitted, open one tab only
                 for an empty session and reuse the current tab thereafter.
    
    Returns:
        dict with: answer, sources, url, title, follow_ups
    """
    # 0. Connection precheck: list_tabs must be healthy before navigating.
    #    success:true with tabs:[] is healthy (bridge up, no tab yet); a
    #    "no extension connected" error or any non-success response aborts.
    tabs_resp = wb("list_tabs", {})
    tabs_text = json.dumps(tabs_resp, ensure_ascii=False).lower()
    if "no extension connected" in tabs_text:
        return _result("WebBridge has no extension connection: " + str(tabs_resp))
    if not tabs_resp.get("success"):
        return _result("list_tabs precheck failed: " + str(tabs_resp))
    if "tabs" not in tabs_resp:
        return _result("list_tabs precheck omitted the tabs field")

    if new_tab is None:
        new_tab = not bool(tabs_resp.get("tabs"))

    # 1. Navigate to Perplexity
    navigate_resp = wb("navigate", {
        "url": "https://www.perplexity.ai",
        "newTab": new_tab,
        "group_title": f"Perplexity: {query[:50]}"
    })
    if not navigate_resp.get("success"):
        return _result("navigate failed: " + str(navigate_resp))
    time.sleep(4)

    # Read back the session after navigation so a successful HTTP response is
    # not mistaken for a tab that actually exists.
    after_nav = wb("list_tabs", {})
    if not after_nav.get("success"):
        return _result("post-navigation list_tabs failed: " + str(after_nav))
    if "tabs" not in after_nav:
        return _result("post-navigation list_tabs omitted the tabs field")
    tab_count = len(after_nav.get("tabs", []))
    
    # 2. Find textbox ref via snapshot
    textbox_ref = find_textbox_ref()
    if not textbox_ref:
        return _result("Could not find input textbox")
    
    # 3. Click textbox to focus it (REQUIRED before fill)
    wb("click", {"selector": textbox_ref})
    time.sleep(0.5)
    
    # 4. Fill query
    grounded_query = build_grounded_query(query)
    fill_resp = wb("fill", {"selector": textbox_ref, "value": grounded_query})
    if not fill_resp.get("data", {}).get("success"):
        # Fallback: use CDP insertText
        wb("cdp", {"method": "Input.insertText", "params": {"text": grounded_query}})
    time.sleep(0.5)
    
    # 5. Submit via Enter key (three-event combo: beforeinput + keydown + keyup)
    evaluate("""(() => {
        const el = document.querySelector("[contenteditable]");
        if (!el) return "no input element";
        el.dispatchEvent(new InputEvent("beforeinput", {
            inputType: "insertText", data: "\\n", bubbles: true, cancelable: true
        }));
        el.dispatchEvent(new KeyboardEvent("keydown", {
            key: "Enter", code: "Enter", keyCode: 13, which: 13,
            bubbles: true, cancelable: true
        }));
        el.dispatchEvent(new KeyboardEvent("keyup", {
            key: "Enter", code: "Enter", keyCode: 13, which: 13,
            bubbles: true, cancelable: true
        }));
        return "enter dispatched";
    })()""")
    
    # 6. Wait for results
    time.sleep(wait_seconds)
    
    # 7. Verify we're on a search results page
    page_info = evaluate("""(() => {
        return JSON.stringify({url: location.href, title: document.title});
    })()""")
    
    url = page_info.get("url", "") if isinstance(page_info, dict) else ""
    title = page_info.get("title", "") if isinstance(page_info, dict) else ""
    
    if "/search/" not in url:
        return _result(
            "Search did not trigger (stayed on homepage)",
            url=url,
            title=title,
        )
    
    # 8. Expand answer if collapsed (click "查看更多")
    if expand:
        evaluate("""(() => {
            const btns = Array.from(document.querySelectorAll("button"));
            const more = btns.find(b => b.innerText.includes("查看更多"));
            if (more) { more.click(); return "expanded"; }
            return "no expand button";
        })()""")
        time.sleep(2)
    
    # 9. Extract answer text
    answer_data = evaluate("""(() => {
        const main = document.querySelector("main");
        if (!main) return JSON.stringify({text: "", url: location.href});
        return JSON.stringify({
            text: main.innerText,
            url: location.href,
            title: document.title
        });
    })()""")
    
    answer_text = ""
    if isinstance(answer_data, dict):
        answer_text = answer_data.get("text", "")
        url = answer_data.get("url", url)
        title = answer_data.get("title", title)
    
    # 10. Extract sources from links tab
    evaluate("""(() => {
        const tabs = Array.from(document.querySelectorAll("[role=tab]"));
        const linksTab = tabs.find(t => t.innerText.includes("链接"));
        if (linksTab) { linksTab.click(); return "clicked"; }
        return "not found";
    })()""")
    time.sleep(1)
    
    sources_raw = evaluate("""(() => {
        const main = document.querySelector("main");
        if (!main) return JSON.stringify([]);
        const links = Array.from(main.querySelectorAll("a[href]"))
            .map(a => ({
                text: a.textContent.trim().substring(0, 200),
                href: a.href
            }))
            .filter(l => l.href.startsWith("http") &&
                        !l.href.includes("perplexity.ai") &&
                        l.text.length > 2);
        const seen = new Set();
        const unique = links.filter(l => {
            if (seen.has(l.href)) return false;
            seen.add(l.href);
            return true;
        });
        return JSON.stringify(unique);
    })()""")
    
    sources = sources_raw if isinstance(sources_raw, list) else []
    
    # 11. Switch back to answer tab
    evaluate("""(() => {
        const tabs = Array.from(document.querySelectorAll("[role=tab]"));
        const answerTab = tabs.find(t => t.innerText.includes("答案"));
        if (answerTab) { answerTab.click(); return "clicked"; }
        return "not found";
    })()""")
    time.sleep(1)
    
    # 12. Extract follow-up questions
    follow_ups_raw = evaluate("""(() => {
        const btns = Array.from(document.querySelectorAll("button"));
        const followUps = btns
            .map(b => b.innerText.trim())
            .filter(t => t.length > 20 && t.length < 200 &&
                        !t.includes("分享") && !t.includes("搜索") &&
                        !t.includes("添加") && !t.includes("展开") &&
                        !t.includes("完成") && !t.includes("来源") &&
                        !t.includes("会话"));
        return JSON.stringify(followUps.slice(0, 5));
    })()""")
    
    follow_ups = follow_ups_raw if isinstance(follow_ups_raw, list) else []
    
    return {
        "answer": answer_text,
        "sources": sources,
        "url": url,
        "title": title,
        "follow_ups": follow_ups,
        "session": SESSION,
        "tab_count": tab_count,
        "verification": {
            "state": "unverified",
            "claim_support": "not_evaluated",
            "source_check": {},
        },
    }


def perplexity_batch_search(queries, wait_seconds=15):
    """Search multiple queries sequentially."""
    results = []
    for i, query in enumerate(queries):
        print(f"[{i+1}/{len(queries)}] {query[:60]}...", file=sys.stderr)
        result = perplexity_search(
            query,
            wait_seconds=wait_seconds,
            new_tab=(i == 0),
        )
        results.append(result)
        time.sleep(2)
    return results


def perplexity_follow_up(follow_up_text, wait_seconds=15):
    """Click a follow-up question on the current page."""
    evaluate(f"""(() => {{
        const btns = Array.from(document.querySelectorAll("button"));
        const target = btns.find(b => b.innerText.includes({json.dumps(follow_up_text)}));
        if (target) {{ target.click(); return "clicked"; }}
        return "not found";
    }})()""")
    time.sleep(wait_seconds)
    
    # Expand and extract
    evaluate("""(() => {
        const btns = Array.from(document.querySelectorAll("button"));
        const more = btns.find(b => b.innerText.includes("查看更多"));
        if (more) { more.click(); return "expanded"; }
        return "no expand";
    })()""")
    time.sleep(2)
    
    return evaluate("""(() => {
        const main = document.querySelector("main");
        return main ? main.innerText : "no main";
    })()""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python perplexity_search.py 'your query here'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    # Set WEBBRIDGE_SESSION to a task-specific name when running the helper.
    result = perplexity_search(query)
    
    if result.get("error"):
        print(f"ERROR: {result['error']}")
        sys.exit(1)
    
    print(f"URL: {result.get('url', 'N/A')}")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"\n{'='*60}")
    print("ANSWER:")
    print(result.get("answer", "No answer"))
    print(f"\n{'='*60}")
    sources = result.get("sources", [])
    print(f"SOURCES ({len(sources)}):")
    for i, s in enumerate(sources):
        print(f"  {i+1}. {s.get('text', '')[:80]} -> {s.get('href', '')}")
    print(f"\n{'='*60}")
    print("FOLLOW-UP QUESTIONS:")
    for q in result.get("follow_ups", []):
        print(f"  - {q}")

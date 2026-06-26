#!/usr/bin/env python3
"""Google Keep Manager — CLI for interacting with Google Keep via nodriver."""

import argparse
import asyncio
import json
import sys
from typing import Optional

import nodriver as uc

from auth import open_keep_session, interactive_login, clear_session

KEEP_URL = "https://keep.google.com/"


def _output(success: bool, message: str, data: Optional[dict] = None) -> None:
    """Prints output in standardized JSON format."""
    result = {"success": success, "message": message}
    if data is not None:
        result["data"] = data
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def _cdp_click(tab, x: int, y: int) -> None:
    """Triggers a native CDP click (hover + click)."""
    await tab.send(uc.cdp.input_.dispatch_mouse_event(
        type_="mouseMoved", x=x, y=y,
        button=uc.cdp.input_.MouseButton("none")))
    await asyncio.sleep(0.3)
    await tab.send(uc.cdp.input_.dispatch_mouse_event(
        type_="mousePressed", x=x, y=y,
        button=uc.cdp.input_.MouseButton("left"), click_count=1))
    await asyncio.sleep(0.1)
    await tab.send(uc.cdp.input_.dispatch_mouse_event(
        type_="mouseReleased", x=x, y=y,
        button=uc.cdp.input_.MouseButton("left"), click_count=1))


async def _get_element_center(tab, js_selector: str) -> tuple[int, int] | None:
    """Returns (x, y) center of an element via JS. None if not found."""
    result = await tab.evaluate(f"""
        JSON.stringify((() => {{
            {js_selector}
        }})())
    """)
    if isinstance(result, str):
        import json as _json
        data = _json.loads(result)
        if data and isinstance(data, dict) and "x" in data:
            return int(data["x"]), int(data["y"])
    return None


async def _click_button_in_editor(tab, label: str) -> bool:
    """Clicks a button in the open note toolbar via CDP."""
    label_js = json.dumps(label)
    coords = await _get_element_center(tab, f"""
        const label = {label_js};
        const closeBtn = [...document.querySelectorAll('div[role="button"]')]
            .find(b => (b.innerText?.trim() === 'Fechar' || b.innerText?.trim() === 'Close') && b.offsetParent !== null);
        if (!closeBtn) return null;
        const toolbar = closeBtn.parentElement;
        let btn = toolbar.querySelector('[role="button"][aria-label="' + label + '"]');
        if (!btn || btn.offsetParent === null) {{
            for (const b of toolbar.querySelectorAll('[role="button"]')) {{
                if (b.innerText?.trim() === label && b.offsetParent !== null) {{ btn = b; break; }}
            }}
        }}
        if (!btn || btn.offsetParent === null) return null;
        const r = btn.getBoundingClientRect();
        return {{x: r.x + r.width / 2, y: r.y + r.height / 2}};
    """)
    if not coords:
        return False
    await _cdp_click(tab, *coords)
    return True


async def _open_keep(headless: bool = True) -> tuple:
    """Opens Keep and verifies session. Returns (browser, tab) or (None, None)."""
    browser, tab = await open_keep_session(headless=headless)
    if not browser:
        _output(False, "Session expired. Run: uv run python scripts/keep.py login")
        return None, None
    return browser, tab


async def _wait_notes(tab) -> None:
    """Waits for notes grid to load."""
    for _ in range(10):
        notes = await tab.query_selector_all("div.IZ65Hb-n0tgWb")
        if notes:
            return
        await asyncio.sleep(1)


async def _wait_for_element(tab, selector: str, timeout: int = 10) -> bool:
    """Waits for a selector to become visible."""
    for _ in range(timeout * 2):
        res = await tab.evaluate(f"document.querySelector('{selector}')?.offsetParent !== null")
        if res:
            return True
        await asyncio.sleep(0.5)
    return False


async def _extract_all_notes(tab) -> list[dict]:
    """Extracts data from all visible notes."""
    result = await tab.evaluate("""
        JSON.stringify((() => {
            const notes = [];
            document.querySelectorAll('div.IZ65Hb-n0tgWb').forEach((el, i) => {
                if (el.querySelector('div[role="combobox"]')) return;

                const titleEl = el.querySelector('div[role="textbox"][dir="ltr"]') || el.querySelector('div[role="textbox"]');
                const title = titleEl ? titleEl.innerText.trim() : '';
                
                const hasCheckboxes = el.querySelector('div[role="checkbox"]') !== null;
                let content;
                
                if (hasCheckboxes) {
                    const items = [];
                    el.querySelectorAll('div[role="checkbox"]').forEach(cb => {
                        let row = cb.parentElement;
                        while (row && row !== el) {
                            const paras = row.querySelectorAll('p[role="presentation"]');
                            if (paras.length === 1 && row.contains(cb)) {
                                const span = paras[0].querySelector('span');
                                const text = (span ? span.innerText : paras[0].innerText).trim();
                                if (text) items.push(text);
                                break;
                            }
                            row = row.parentElement;
                        }
                    });
                    content = items;
                } else {
                    const paras = el.querySelectorAll('p[role="presentation"]');
                    const lines = [];
                    paras.forEach(p => {
                        const span = p.querySelector('span');
                        const line = (span ? span.innerText : p.innerText).trim();
                        if (line) lines.push(line);
                    });
                    content = lines;
                }
                
                const isEmpty = Array.isArray(content) ? content.length === 0 : !content;
                if (!title && isEmpty) return;
                
                notes.push({
                    id: (notes.length + 1).toString(),
                    title: title,
                    content: content,
                    type: hasCheckboxes ? 'list' : 'text'
                });
            });
            return notes;
        })())
    """)
    if isinstance(result, str):
        return json.loads(result)
    return result if isinstance(result, list) else []


async def _find_and_click_note(tab, title: str) -> bool:
    """Finds note by title and clicks the card."""
    target_js = json.dumps(title)
    found = await tab.evaluate(f"""
        (() => {{
            const target = {target_js};
            const cards = document.querySelectorAll('div.IZ65Hb-n0tgWb');
            for (const el of cards) {{
                const titleEl = el.querySelector('div[role="textbox"][dir="ltr"]') || el.querySelector('div[role="textbox"]');
                if (titleEl && titleEl.innerText.trim() === target) {{
                    el.click();
                    return true;
                }}
            }}
            return false;
        }})()
    """)
    return bool(found)


async def _find_and_click_note_by_title_textbox(tab, title: str) -> bool:
    """Finds note by explicit title textbox and clicks it."""
    target_js = json.dumps(title)
    coords = await _eval_coords(tab, f"""
        const target = {target_js};
        const divs = document.querySelectorAll('div[role="textbox"][dir="ltr"], div[role="textbox"]');
        for (const d of divs) {{
            if (d.offsetParent === null) continue;
            if (d.innerText?.trim() === target) {{
                const r = d.getBoundingClientRect();
                return {{x: r.x + r.width / 2, y: r.y + r.height / 2}};
            }}
        }}
        return null;
    """)
    if not coords:
        return False
    await _cdp_click(tab, *coords)
    return True


async def _eval_coords(tab, js: str) -> tuple[int, int] | None:
    """Evaluates JS that returns {x, y} and returns tuple (x, y)."""
    result = await tab.evaluate(f"JSON.stringify((() => {{ {js} }})())")
    if isinstance(result, str):
        data = json.loads(result)
        if data and isinstance(data, dict) and "x" in data:
            return int(data["x"]), int(data["y"])
    return None


async def _click_div_with_text(tab, *texts: str) -> bool:
    """Clicks the first visible div matching any of the exact texts."""
    texts_js = json.dumps(texts)
    coords = await _eval_coords(tab, f"""
        const variants = {texts_js};
        const divs = document.querySelectorAll('div');
        for (const d of divs) {{
            if (d.offsetParent === null) continue;
            if (d.children.length > 0) continue;
            if (variants.includes(d.innerText?.trim())) {{
                const r = d.getBoundingClientRect();
                return {{x: r.x + r.width / 2, y: r.y + r.height / 2}};
            }}
        }}
        return null;
    """)
    if not coords:
        return False
    await _cdp_click(tab, *coords)
    return True


async def _press_enter(tab) -> None:
    """Sends Enter key via CDP."""
    await tab.send(uc.cdp.input_.dispatch_key_event(type_="keyDown", key="Enter", code="Enter", windows_virtual_key_code=13))
    await asyncio.sleep(0.05)
    await tab.send(uc.cdp.input_.dispatch_key_event(type_="keyUp", key="Enter", code="Enter", windows_virtual_key_code=13))


async def _inject_text(tab, text: str) -> None:
    """Safely injects text into the active element via document.execCommand."""
    text_js = json.dumps(text)
    await tab.evaluate(f"""
        (() => {{
            let target = document.activeElement;
            if (!target || target.getAttribute('role') === 'button' || target.tagName === 'BODY') {{
                const editor = document.querySelector('.IZ65Hb-WsjYwc-nUpftc') || document.body;
                const editables = [...editor.querySelectorAll('[role="textbox"]:not([aria-label="Título"]):not([aria-label="Title"])')];
                if (editables.length > 0) target = editables[0];
            }}
            if (target) {{
                target.focus();
                document.execCommand('insertText', false, {text_js});
            }}
        }})()
    """)


async def _close_note(tab) -> None:
    """Closes the currently opened note prioritizing the exact UI button."""
    coords = await _eval_coords(tab, """
        const btns = [...document.querySelectorAll('div[role="button"]')];
        const closeBtn = btns.find(e => e.innerText && (e.innerText.trim() === 'Fechar' || e.innerText.trim() === 'Close'));
        if (closeBtn && closeBtn.offsetParent !== null) {
            const r = closeBtn.getBoundingClientRect();
            return {x: r.x + r.width / 2, y: r.y + r.height / 2};
        }
        return null;
    """)
    if coords:
        await _cdp_click(tab, *coords)
    else:
        # Fallback to simple evaluate click
        await tab.evaluate('''
            (() => {
                const btns = [...document.querySelectorAll('div[role="button"]')];
                const closeBtn = btns.find(e => e.innerText && (e.innerText.trim() === 'Fechar' || e.innerText.trim() === 'Close'));
                if (closeBtn) closeBtn.click();
            })();
        ''')
    await asyncio.sleep(1)


# ── Commands ──────────────────────────────────────────────────

async def cmd_list(args) -> None:
    """Lists Google Keep notes."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    try:
        await _wait_notes(tab)
        all_notes = await _extract_all_notes(tab)

        notes = []
        for data in all_notes:
            if len(notes) >= args.limit:
                break
            if args.filter_text:
                term = args.filter_text.lower()
                title = (data.get("title") or "").lower()
                content = data.get("content") or []
                content_str = " ".join(content) if isinstance(content, list) else str(content)
                if term not in title and term not in content_str.lower():
                    continue
            notes.append(data)

        _output(True, f"{len(notes)} note(s) found", {"notes": notes})
    finally:
        browser.stop()


async def cmd_create(args) -> None:
    """Creates a basic text note."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    try:
        await _wait_notes(tab)

        # 1. Click 'Take a note...'
        if not await _click_div_with_text(tab, "Criar uma nota…", "Take a note…"):
            _output(False, "Could not find 'Take a note' button")
            return
            
        await asyncio.sleep(1.5)

        # 2. Fill content multiline
        if args.content:
            try:
                parsed = json.loads(args.content)
                if isinstance(parsed, list):
                    lines = [str(x) for x in parsed]
                else:
                    lines = args.content.replace('\\n', '\n').splitlines()
            except Exception:
                lines = args.content.replace('\\n', '\n').splitlines()

            for i, line in enumerate(lines):
                await _inject_text(tab, line)
                if i < len(lines) - 1:
                    await _press_enter(tab)
                    await asyncio.sleep(0.3)

        # 3. Fill Title
        if args.title:
            title_js = json.dumps(args.title)
            await tab.evaluate(f"""
                (() => {{
                    const titleEl = document.querySelector('div[role="textbox"][aria-label="Título"]') || 
                                    document.querySelector('div[role="textbox"][aria-label="Title"]');
                    if (titleEl) {{
                        titleEl.click();
                        titleEl.focus();
                        document.execCommand('insertText', false, {title_js});
                    }}
                }})()
            """)
            await asyncio.sleep(0.5)

        # 4. Close
        await _close_note(tab)
        await asyncio.sleep(12) # Wait for sync

        _output(True, "Note successfully created", {"title": args.title})
    except Exception as e:
        _output(False, f"Error creating note: {e}")
    finally:
        browser.stop()


async def cmd_create_list(args) -> None:
    """Creates a list note."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    items = args.items
    if isinstance(items, str):
        items = [s.strip() for s in items.replace(",", "\n").split("\n") if s.strip()]
    if not items:
        _output(False, "Provide at least one item (--items)")
        return

    try:
        # 1. Open list editor
        coords = await _eval_coords(tab, '''
            let btn = document.querySelector('div[role="button"][data-tooltip-text="Nova lista"][aria-label="Nova lista"]');
            if (!btn) btn = document.querySelector('div[role="button"][data-tooltip-text="New list"][aria-label="New list"]');
            if (!btn || btn.offsetParent === null) return null;
            const r = btn.getBoundingClientRect();
            return {x: r.x + r.width / 2, y: r.y + r.height / 2};
        ''')
        
        if not coords:
            await tab.evaluate('document.querySelector(\'div[role="combobox"]\')?.click()')
            await asyncio.sleep(1)
            _output(False, "'New list' button not visually found")
            return
            
        await _cdp_click(tab, *coords)
        if not await _wait_for_element(tab, 'div.IZ65Hb-WsjYwc-nUpftc [contenteditable="true"]', timeout=5):
            _output(False, "List editor did not open after click")
            return

        # 2. Fill items
        for i, item in enumerate(items):
            if i > 0:
                await _press_enter(tab)
                await asyncio.sleep(0.5)

            item_js = json.dumps(item)
            await tab.evaluate(f"""
                (() => {{
                    const target = document.activeElement;
                    if (target && target.getAttribute('contenteditable') === 'true') {{
                        document.execCommand('insertText', false, {item_js});
                    }}
                }})()
            """)
            await asyncio.sleep(0.2)

        # 3. Fill Title
        if args.title:
            title_js = json.dumps(args.title)
            coords = await _eval_coords(tab, """
                const divs = document.querySelectorAll('div');
                for (const d of divs) {
                    if (d.innerText && (d.innerText.trim() === 'Título' || d.innerText.trim() === 'Title') && d.children.length === 0) {
                        const r = d.getBoundingClientRect();
                        return {x: r.x + r.width / 2, y: r.y + r.height / 2};
                    }
                }
                return null;
            """)
            if coords:
                await _cdp_click(tab, *coords)
                await asyncio.sleep(0.5)
                await tab.evaluate(f"""
                    (() => {{
                        document.execCommand('insertText', false, {title_js});
                    }})()
                """)
            else:
                _output(False, "Could not find the Title field")

        # 4. Close
        await _close_note(tab)
        await asyncio.sleep(12) 

        _output(True, "List successfully created", {"title": args.title})
    except Exception as e:
        _output(False, f"Error creating list: {e}")
    finally:
        browser.stop()


async def cmd_read(args) -> None:
    """Reads a note structurally by title."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    try:
        await _wait_notes(tab)
        target_js = json.dumps(args.title)
        
        note_data = await tab.evaluate(f"""
            (() => {{
                const target = {target_js};
                const cards = document.querySelectorAll('div.IZ65Hb-n0tgWb');
                for (const el of cards) {{
                    const titleEl = el.querySelector('div[role="textbox"][dir="ltr"]') || el.querySelector('div[role="textbox"]');
                    if (titleEl && titleEl.innerText && titleEl.innerText.trim() === target) {{
                        const title = titleEl.innerText.trim();
                        const hasCheckboxes = el.querySelector('div[role="checkbox"]') !== null;
                        let content;
                        
                        if (hasCheckboxes) {{
                            const items = [];
                            el.querySelectorAll('div[role="checkbox"]').forEach(cb => {{
                                let row = cb.parentElement;
                                while (row && row !== el) {{
                                    const paras = row.querySelectorAll('p[role="presentation"]');
                                    if (paras.length === 1 && row.contains(cb)) {{
                                        const span = paras[0].querySelector('span');
                                        const text = (span ? span.innerText : paras[0].innerText).trim();
                                        if (text) items.push(text);
                                        break;
                                    }}
                                    row = row.parentElement;
                                }}
                            }});
                            content = items;
                        }} else {{
                            const paras = el.querySelectorAll('p[role="presentation"]');
                            const lines = [];
                            paras.forEach(p => {{
                                const span = p.querySelector('span');
                                const line = (span ? span.innerText : p.innerText).trim();
                                if (line) lines.push(line);
                            }});
                            content = lines;
                        }}
                        
                        return JSON.stringify({{
                            title: title,
                            content: content,
                            type: hasCheckboxes ? 'list' : 'text'
                        }});
                    }}
                }}
                return null;
            }})()
        """)
        
        if note_data:
            _output(True, "Note found", json.loads(note_data))
        else:
            _output(False, f"Note '{args.title}' not found")
    except Exception as e:
        _output(False, f"Error reading note: {e}")
    finally:
        browser.stop()


async def cmd_update(args) -> None:
    """Updates an existing note."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    try:
        await _wait_notes(tab)

        # 1. Extract metadata before acting
        target_js = json.dumps(args.title)
        note_data_json = await tab.evaluate(f"""
            (() => {{
                const target = {target_js};
                const cards = document.querySelectorAll('div.IZ65Hb-n0tgWb');
                for (const el of cards) {{
                    const titleEl = el.querySelector('div[role="textbox"][dir="ltr"]') || el.querySelector('div[role="textbox"]');
                    if (titleEl && titleEl.innerText && titleEl.innerText.trim() === target) {{
                        const title = titleEl.innerText.trim();
                        const hasCheckboxes = el.querySelector('div[role="checkbox"]') !== null;
                        let content;
                        
                        if (hasCheckboxes) {{
                            const items = [];
                            el.querySelectorAll('div[role="checkbox"]').forEach(cb => {{
                                let row = cb.parentElement;
                                while (row && row !== el) {{
                                    const paras = row.querySelectorAll('p[role="presentation"]');
                                    if (paras.length === 1 && row.contains(cb)) {{
                                        const span = paras[0].querySelector('span');
                                        const text = (span ? span.innerText : paras[0].innerText).trim();
                                        if (text) items.push(text);
                                        break;
                                    }}
                                    row = row.parentElement;
                                }}
                            }});
                            content = items;
                        }} else {{
                            const paras = el.querySelectorAll('p[role="presentation"]');
                            const lines = [];
                            paras.forEach(p => {{
                                const span = p.querySelector('span');
                                const line = (span ? span.innerText : p.innerText).trim();
                                if (line) lines.push(line);
                            }});
                            content = lines;
                        }}
                        
                        return JSON.stringify({{
                            title: title,
                            content: content,
                            type: hasCheckboxes ? 'list' : 'text'
                        }});
                    }}
                }}
                return null;
            }})()
        """)
        
        note_data = None
        if note_data_json:
            try:
                note_data = json.loads(note_data_json)
            except:
                pass

        if not note_data:
            _output(False, f"Note '{args.title}' not found for pre-reading")
            return
            
        edited_memory = ""
        if note_data['type'] == 'text':
            edited_memory = args.content if args.content else "\\n".join(note_data.get('content', []))

        # 2. Open note
        clicked = await _find_and_click_note_by_title_textbox(tab, args.title)
        if not clicked:
            clicked = await _find_and_click_note(tab, args.title)
        if not clicked:
            _output(False, f"Note '{args.title}' not found to open")
            return

        await asyncio.sleep(1)

        # (Skipping explicit title rewrite as per functionality drop)

        is_list = (note_data['type'] == 'list') if note_data else False

        if is_list and (args.items or args.content):
            items_src = args.items or args.content or ""
            items_src = items_src.replace("\\n", "\n")
            if args.items and not args.content:
                items_src = items_src.replace(",", "\n")
            items = [s.strip() for s in items_src.split("\n") if s.strip()]
            
            if items:
                while True:
                    deleted_any = await tab.evaluate("""
                        (() => {
                            let btns = document.querySelectorAll('div[role="button"][data-tooltip-text="Excluir"][aria-label="Excluir"]');
                            if (btns.length === 0) btns = document.querySelectorAll('div[role="button"][data-tooltip-text="Delete"][aria-label="Delete"]');
                            if (btns.length === 0) return false;
                            
                            for (const b of btns) {
                                ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(evt => {
                                    b.dispatchEvent(new MouseEvent(evt, {bubbles: true, cancelable: true, view: window}));
                                });
                            }
                            return true;
                        })()
                    """)
                    if not deleted_any:
                        break
                    await asyncio.sleep(0.5)
                        
                add_item_coords = await _eval_coords(tab, """
                    let c = document.querySelector('div[role="button"][aria-label="Adicionar item de lista"]');
                    if (!c) c = document.querySelector('div[role="button"][aria-label="List item"]');
                    if (c) {
                        const r = c.getBoundingClientRect();
                        return {x: r.x + r.width / 2, y: r.y + r.height / 2};
                    }
                    return null;
                """)
                
                if add_item_coords:
                    await _cdp_click(tab, *add_item_coords)
                    await asyncio.sleep(0.3)
                    
                    for i, item in enumerate(items):
                        item_js = json.dumps(item)
                        await tab.evaluate(f"""
                            (() => {{
                                document.execCommand('insertText', false, {item_js});
                            }})()
                        """)
                        if i < len(items) - 1:
                            await _press_enter(tab)
                            await asyncio.sleep(0.3)
                            
                    await asyncio.sleep(0.3)
                else:
                    _output(False, "'List item' field not found in open modal")
                    return
            
        elif not is_list and args.content:
            await asyncio.sleep(0.5)
            await tab.evaluate("""
                (() => {
                    let target = document.activeElement;
                    if (!target || target.getAttribute('role') === 'button' || target.tagName === 'BODY' || target.getAttribute('aria-label') === 'Título' || target.getAttribute('aria-label') === 'Title') {
                        const editor = document.querySelector('.IZ65Hb-WsjYwc-nUpftc') || document.body;
                        const editables = [...editor.querySelectorAll('[role="textbox"]:not([aria-label="Título"]):not([aria-label="Title"])')];
                        if (editables.length > 0) editables[0].focus();
                    }
                })()
            """)
            await asyncio.sleep(0.3)
            
            await tab.send(uc.cdp.input_.dispatch_key_event(type_="keyDown", modifiers=2, windows_virtual_key_code=65, code="KeyA", key="a"))
            await tab.send(uc.cdp.input_.dispatch_key_event(type_="keyUp", modifiers=2, windows_virtual_key_code=65, code="KeyA", key="a"))
            await asyncio.sleep(0.2)
            
            await tab.send(uc.cdp.input_.dispatch_key_event(type_="keyDown", windows_virtual_key_code=46, code="Delete", key="Delete"))
            await tab.send(uc.cdp.input_.dispatch_key_event(type_="keyUp", windows_virtual_key_code=46, code="Delete", key="Delete"))
            await asyncio.sleep(0.3)
                
            content_normalized = edited_memory.replace("\\n", "\n")
            lines = content_normalized.splitlines()
            
            for i, line in enumerate(lines):
                await _inject_text(tab, line)
                if i < len(lines) - 1:
                    await _press_enter(tab)
                    await asyncio.sleep(0.3)
                    
            await asyncio.sleep(0.3)

        await _close_note(tab)
        await asyncio.sleep(12)

        _output(True, "Note successfully updated")
    except Exception as e:
        _output(False, f"Error updating note: {e}")
    finally:
        browser.stop()


async def cmd_delete(args) -> None:
    """Deletes a note."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    try:
        await _wait_notes(tab)
        target_js = json.dumps(args.title)

        is_opened = await tab.evaluate(f"""
            (() => {{
                const target = {target_js};
                const cards = document.querySelectorAll('div.IZ65Hb-n0tgWb');
                for (const el of cards) {{
                    const titleEl = el.querySelector('div[role="textbox"][dir="ltr"]') || el.querySelector('div[role="textbox"]');
                    if (titleEl && titleEl.innerText && titleEl.innerText.trim() === target) {{
                        titleEl.click();
                        return true;
                    }}
                }}
                return false;
            }})()
        """)
        if not is_opened:
            _output(False, f"Note '{args.title}' not found for deletion")
            return

        await asyncio.sleep(2)

        mais_c = await _eval_coords(tab, """
            let btns = Array.from(document.querySelectorAll('div[role="button"][data-tooltip-text="Mais"][aria-label="Mais"]'));
            if (btns.length === 0) btns = Array.from(document.querySelectorAll('div[role="button"][data-tooltip-text="More"][aria-label="More"]'));
            const btn = btns.pop();
            if (btn) {
                const r = btn.getBoundingClientRect();
                return {x: r.x + r.width / 2, y: r.y + r.height / 2};
            }
            return null;
        """)
        if not mais_c:
            _output(False, "'More' button not found")
            return

        await _cdp_click(tab, *mais_c)
        await asyncio.sleep(1.5)

        excl_c = await _eval_coords(tab, """
            const divs = Array.from(document.querySelectorAll('div'));
            const btn = divs.reverse().find(d => d.innerText && (d.innerText.trim() === 'Excluir nota' || d.innerText.trim() === 'Delete note') && d.offsetWidth > 0);
            if (btn) {
                const r = btn.getBoundingClientRect();
                return {x: r.x + r.width / 2, y: r.y + r.height / 2};
            }
            return null;
        """)
        if not excl_c:
            _output(False, "'Delete note' option not found in menu")
            return

        await _cdp_click(tab, *excl_c)        

        await asyncio.sleep(12)
        _output(True, "Note moved to trash")
    except Exception as e:
        _output(False, f"Error deleting: {e}")
    finally:
        browser.stop()


async def cmd_archive(args) -> None:
    """Archives a note."""
    browser, tab = await _open_keep(headless=not getattr(args, 'visible', False))
    if not browser:
        return

    try:
        await _wait_notes(tab)
        target_js = json.dumps(args.title)

        is_opened = await tab.evaluate(f"""
            (() => {{
                const target = {target_js};
                const cards = document.querySelectorAll('div.IZ65Hb-n0tgWb');
                for (const el of cards) {{
                    const titleEl = el.querySelector('div[role="textbox"][dir="ltr"]') || el.querySelector('div[role="textbox"]');
                    if (titleEl && titleEl.innerText && titleEl.innerText.trim() === target) {{
                        titleEl.click();
                        return true;
                    }}
                }}
                return false;
            }})()
        """)
        if not is_opened:
            _output(False, f"Note '{args.title}' not found for archiving")
            return

        await asyncio.sleep(2)

        arch_c = await _eval_coords(tab, """
            let btns = Array.from(document.querySelectorAll('div[role="button"][data-tooltip-text="Arquivar"][aria-label="Arquivar"]'));
            if (btns.length === 0) btns = Array.from(document.querySelectorAll('div[role="button"][data-tooltip-text="Archive"][aria-label="Archive"]'));
            const btn = btns.pop();
            if (btn) {
                const r = btn.getBoundingClientRect();
                return {x: r.x + r.width / 2, y: r.y + r.height / 2};
            }
            return null;
        """)
        if not arch_c:
            _output(False, "'Archive' button not found")
            return

        await _cdp_click(tab, *arch_c)
        await asyncio.sleep(2)

        update_c = await _eval_coords(tab, """
            let btn = document.querySelector('div[role="button"][data-tooltip-text="Atualizar"][aria-label="Atualizar"]');
            if (!btn) btn = document.querySelector('div[role="button"][data-tooltip-text="Refresh"][aria-label="Refresh"]');
            if (btn) {
                const r = btn.getBoundingClientRect();
                return {x: r.x + r.width / 2, y: r.y + r.height / 2};
            }
            return null;
        """)
        if update_c:
            await _cdp_click(tab, *update_c)

        await asyncio.sleep(12)
        _output(True, "Note successfully archived")
    except Exception as e:
        _output(False, f"Error archiving: {e}")
    finally:
        browser.stop()


# ── CLI ──────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    """Builds CLI arguments parser."""
    parser = argparse.ArgumentParser(
        description="Google Keep Manager — nodriver (undetected Chrome)"
    )
    parser.add_argument("--visible", action="store_true", help="Shows the browser (headful mode)")
    sub = parser.add_subparsers(dest="command", help="Command to execute")

    sub.add_parser("login", help="Opens Chrome for manual login")
    sub.add_parser("logout", help="Clears saved session")
    sub.add_parser("check", help="Checks if session is active")

    sp = sub.add_parser("list", help="Lists notes")
    sp.add_argument("--limit", type=int, default=20, help="Max number of notes")
    sp.add_argument("--filter", dest="filter_text", help="Filter by text match")

    sp = sub.add_parser("create", help="Creates text note")
    sp.add_argument("--title", required=True, help="Note title")
    sp.add_argument("--content", required=True, help="Note content")

    sp = sub.add_parser("create-list", help="Creates checklist note")
    sp.add_argument("--title", default="", help="Note title")
    sp.add_argument("--items", required=True, help="Comma-separated items")

    sp = sub.add_parser("read", help="Reads a specific note")
    sp.add_argument("--title", required=True, help="Exact note title")

    sp = sub.add_parser("update", help="Updates an existing note")
    sp.add_argument("--title", required=True, help="Current exact title")
    sp.add_argument("--content", help="New content replacing old text")
    sp.add_argument("--items", help="New list items replacing old ones")

    sp = sub.add_parser("delete", help="Moves note to trash")
    sp.add_argument("--title", required=True, help="Exact note title")

    sp = sub.add_parser("archive", help="Archives note")
    sp.add_argument("--title", required=True, help="Exact note title")

    return parser


def main() -> None:
    """CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    loop = uc.loop()

    if args.command == "login":
        ok = interactive_login()
        sys.exit(0 if ok else 1)

    if args.command == "logout":
        clear_session()
        return

    if args.command == "check":
        from auth import check_session_async
        ok = loop.run_until_complete(check_session_async())
        _output(ok, f"Session {'active' if ok else 'inactive'}")
        return

    handlers = {
        "list": cmd_list,
        "create": cmd_create,
        "create-list": cmd_create_list,
        "read": cmd_read,
        "update": cmd_update,
        "delete": cmd_delete,
        "archive": cmd_archive,
    }

    handler = handlers.get(args.command)
    if handler:
        loop.run_until_complete(handler(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

"""Tests for the element-table fallback rungs (融合项 a).

Ladder under test: ``probe → element-table rung → probe.fallback-exhausted``
(external review ruling D1=A / D2=A / D3=B + WARN):

* D1=A — rung targets are chosen by a PURE deterministic heuristic; a
  candidate is adopted only after a semantic readback (and an effect check
  where the rung acts);
* D2=A — a failed fallback raises the unified ``probe.fallback-exhausted``
  fail-closed code, never a half result;
* D3=B — every fallback trigger writes a runs.jsonl event with a sanitized
  hit-element snapshot summary (no URL query strings, no suspected tokens);
* WARN (highest) — composer state, URL changes and count changes can NEVER
  prove submit ownership alone: the ownership rung needs an independent
  query-text binding PLUS an effect signal, and stops without both.

(a) probes healthy ⇒ fallback never runs (zero side effects);
(b) probe fails + candidate qualifies ⇒ fallback succeeds with
    ``fallback_used`` + summary;
(c) probe fails + candidate unqualified ⇒ ``probe.fallback-exhausted``;
(d) ownership: binding ∧ effect ⇒ True, missing either ⇒ exhausted;
(e) a near-match button carrying ？/? is never clicked;
(f) summaries are sanitized (URL query / token never leak).

Review follow-ups (RC1-RC6): the bound probe's composer exclusion is pinned
as real DOM behavior under node (never source-substring); the prose rung only
adopts blocks NEWER than the pre-submit baseline (stale_risk honest when the
baseline is missing) and never a probe-truncated half candidate; the expand
rung hunts only when the answer looks truncated and only near the answer
area; guard samples carry candidate identity; every trigger logs an event.
"""
import json
import shutil
import subprocess
import sys; sys.path.insert(0, "src")

import pytest

from test_console import ConsoleFakeDriver, NOOP, make_config

from perplexity_toolkit import console
from perplexity_toolkit.commands.cli import _t_drift
from perplexity_toolkit.console import (
    ConsoleError,
    _edit_distance,
    _expand_candidate_score,
    _prose_block_score,
    _prose_candidates,
    _sanitize_summary_text,
    _snapshot_summary,
    console_extract,
)


@pytest.fixture(autouse=True)
def tmp_console_home(tmp_path, monkeypatch):
    monkeypatch.setenv("PERPLEXITY_CONSOLE_HOME", str(tmp_path))
    return tmp_path


# ──────────────────────────────────────────────────────────────
# fixtures helpers
# ──────────────────────────────────────────────────────────────

# a qualified answer block: ≥200 chars with sentence punctuation
LONG_ANSWER = "这是完整回答。" + "正文段落内容示例。" * 30

# an answer that LOOKS truncated (「…」 tail) — the ONLY state in which the
# expand rung hunts candidates (RC3: never click on a healthy page)
TRUNCATED_ANSWER = "这是被截断的回答，后文尚未渲染出来" + "前面的内容。" * 30 + "…"

# previous-turn (stale, LONGER) vs current-turn (fresh, shorter) answers for
# the RC2/RC6 pre-submit baseline freshness tests
OLD_ANSWER = "上一轮的旧回答。" + "旧正文段落内容。" * 50
NEW_ANSWER = "这一轮的新回答。" + "新正文段落。" * 40


def block(i, text, *, tag="div", role="", hint="", label="",
          w=800, h=400, x=200, y=100):
    return {"i": i, "tag": tag, "role": role, "label": label, "cls": "",
            "hint": hint, "len": len(text), "text": text,
            "rect": {"x": x, "y": y, "w": w, "h": h}}


def item(i, text, *, tag="button", role="", label="", disabled=False,
         w=80, h=24, x=10, y=10):
    return {"i": i, "tag": tag, "role": role, "label": label, "text": text,
            "rect": {"x": x, "y": y, "w": w, "h": h}, "disabled": disabled}


class FallbackFakeDriver(ConsoleFakeDriver):
    """ConsoleFakeDriver + rung-2 probes dispatched on their /*PPLX_*_PROBE*/
    markers. A ``None`` payload models a DEAD probe (historical behavior);
    a dict payload models an operational element table / blocks / binding."""

    def __init__(self, *, table=None, blocks=None, bound=None,
                 prose_found=True, expand_result="none",
                 grow_on_click=False, grow_prose_len=False, vary_url=False,
                 **kw):
        super().__init__(**kw)
        self.table = table
        self.blocks = blocks
        self.bound = bound
        self.prose_found = prose_found
        self.expand_result = expand_result
        self.grow_on_click = grow_on_click
        self.grow_prose_len = grow_prose_len
        self.vary_url = vary_url
        self.cdp_clicks = []
        self._grow_tick = 0
        self._url_tick = 0
        self._block_boost = 0

    def evaluate(self, code, **kwargs):
        if "PPLX_TABLE_PROBE" in code:
            return "" if self.table is None else {
                "items": list(self.table), "count": len(self.table)}
        if "PPLX_BLOCKS_PROBE" in code:
            return self._blocks()
        if "PPLX_BOUND_PROBE" in code:
            return "" if self.bound is None else dict(self.bound)
        if "cloneNode" in code and not self.prose_found:
            return {"found": False}
        if "=== '展开'" in code:
            return self.expand_result
        out = super().evaluate(code, **kwargs)
        if "user-bubble" in code and isinstance(out, dict):
            out = dict(out)
            if self.grow_prose_len:
                self._grow_tick += 1
                out["lastProseLen"] = self._grow_tick * 10
            if self.vary_url:
                self._url_tick += 1
                out["url"] = f"https://www.perplexity.ai/search/t-{self._url_tick}"
        return out

    def _blocks(self):
        if self.blocks is None:
            return ""
        blocks = []
        for raw in self.blocks:
            nb = dict(raw)
            if self._block_boost:
                nb["len"] = int(nb.get("len") or 0) + self._block_boost
                nb["text"] = str(nb.get("text") or "") + "（补充）。" * (
                    self._block_boost // 5)
            blocks.append(nb)
        return {"blocks": blocks, "count": len(blocks)}

    def cdp(self, method, params=None):
        if (method == "Input.dispatchMouseEvent" and params
                and params.get("type") == "mousePressed"):
            self.cdp_clicks.append((int(params.get("x") or 0),
                                    int(params.get("y") or 0)))
            if self.grow_on_click:
                self._block_boost += 300
        return super().cdp(method, params)


def pplx_probes(drv):
    """All executed rung-2 probe sources (markers survive the 60-char cap)."""
    return [c[1] for c in drv.calls
            if c[0] == "evaluate" and c[1].startswith("/*PPLX_")]


def fallback_events(home):
    path = home / "runs.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("op") == "fallback":
            out.append(rec)
    return out


# ──────────────────────────────────────────────────────────────
# 实现件 1: the minimal element table
# ──────────────────────────────────────────────────────────────

class TestElementTableProbe:

    def test_table_probe_is_read_only_and_structured(self):
        src = console._JS_TABLE
        for forbidden in (".click()", "dispatchEvent", "insertText",
                          "input.files", "atob(", "scrollTop",
                          "window.scrollTo", "localStorage", "pushState"):
            assert forbidden not in src, forbidden
        for field in ("i: i++", "getAttribute('role')", "getAttribute('aria-label')",
                      "text:", "rect:", "getBoundingClientRect"):
            assert field in src, field
        assert src.strip().startswith("/*PPLX_TABLE_PROBE*/")
        assert "slice(0, 120)" in src          # innerText ≤120 chars

    def test_blocks_and_bound_probes_are_read_only(self):
        for src in (console._JS_BLOCKS, console._JS_BOUND_TMPL):
            for forbidden in (".click()", "dispatchEvent", "insertText",
                              "window.scrollTo", "localStorage"):
                assert forbidden not in src, forbidden

    def test_items_are_parsed_from_the_table_payload(self):
        drv = FallbackFakeDriver(table=[item(0, "提交", label="提交"),
                                        item(1, "展开")])
        items = console._table_items(drv) or []
        assert [i["text"] for i in items] == ["提交", "展开"]
        # dead probe → None (rung reports "unavailable")
        assert console._table_items(FallbackFakeDriver()) is None


# ──────────────────────────────────────────────────────────────
# 实现件 1b: the bound probe's WARN contract as REAL DOM behavior —
# executed against the real probe JS in node over a stub DOM (the
# FakeDriver only pattern-matches probe source, it cannot test the
# matcher itself; a source-substring assertion proved nothing).
# ──────────────────────────────────────────────────────────────

NODE = shutil.which("node")

_BOUND_DOM_PRE = (
    "function mk(spec) {\n"
    "  const el = {tagName: String(spec.tag).toUpperCase(),\n"
    "    innerText: spec.t || '', textContent: spec.t || '',\n"
    "    parentElement: null, attrs: spec.attrs || {}, ce: !!spec.ce, kids: []};\n"
    "  el.getAttribute = (n) => (n in el.attrs ? el.attrs[n] : null);\n"
    "  el.closest = (sel) => { if (sel !== 'form') return null;\n"
    "    for (let n = el; n; n = n.parentElement) if (n.tagName === 'FORM') return n;\n"
    "    return null; };\n"
    "  for (const k of (spec.kids || [])) {\n"
    "    const c = mk(k); c.parentElement = el; el.kids.push(c);\n"
    "  }\n"
    "  return el;\n"
    "}\n"
    "function flat(el, acc) { acc.push(el); for (const c of el.kids) flat(c, acc); return acc; }\n"
    "const ALL = flat(mk("
)
_BOUND_DOM_MID = (
    "), []);\n"
    "globalThis.document = {\n"
    "  querySelector: (sel) => (sel === 'main'\n"
    "    ? (ALL.find((e) => e.tagName === 'MAIN') || null) : null),\n"
    "  querySelectorAll: (sel) => (sel === '[contenteditable]'\n"
    "    ? ALL.filter((e) => e.ce) : ALL),\n"
    "};\n"
    "process.stdout.write(String("
)
_BOUND_DOM_POST = "));\n"


def _bound_probe_run(query, tree):
    """Run the REAL bound probe in node over a stub DOM ``tree``.

    ``tree``: nested dicts {"tag", "t" (innerText), "attrs", "ce", "kids"}.
    """
    assert NODE is not None
    src = console._JS_BOUND_TMPL.replace(
        "__QUERY__", json.dumps(query, ensure_ascii=False))
    harness = (_BOUND_DOM_PRE + json.dumps(tree, ensure_ascii=False)
               + _BOUND_DOM_MID + src + _BOUND_DOM_POST)
    proc = subprocess.run([NODE, "-e", harness], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


@pytest.mark.skipif(NODE is None, reason="node is required to execute probe JS")
class TestBoundProbeComposerExclusion:
    """WARN contract as DOM behavior: the composer subtree — and every
    ancestor whose innerText carries it (main/body) — is NEVER identity
    evidence, and `bound:true` requires element-level text evidence."""

    @staticmethod
    def _tree(*, thread_text, composer_text, page_text):
        return {"tag": "body", "t": page_text, "kids": [
            {"tag": "main", "t": page_text, "kids": [
                {"tag": "div", "t": thread_text, "attrs": {"class": "thread"}},
                {"tag": "form", "t": composer_text, "kids": [
                    {"tag": "div", "t": composer_text, "ce": True},
                ]},
            ]},
        ]}

    def test_query_only_in_the_composer_is_not_evidence(self):
        """(a) the silent-send-failure shape: the unsubmitted query sits in
        the composer and main/body innerText still contains it — the old
        probe bound on exactly that; it must NOT bind."""
        tree = self._tree(thread_text="这是上一轮的旧回答内容。",
                          composer_text="q-绑定",
                          page_text="这是上一轮的旧回答内容。 q-绑定")
        out = _bound_probe_run("q-绑定", tree)
        assert out["bound"] is False
        assert out["text"] == "" and out["where"] == ""

    def test_query_in_the_thread_binds_with_text_evidence(self):
        """(b) query in the thread body ⇒ bound:true with non-empty text."""
        tree = self._tree(thread_text="这是回答引用 q-绑定 的文本。",
                          composer_text="",
                          page_text="这是回答引用 q-绑定 的文本。")
        out = _bound_probe_run("q-绑定", tree)
        assert out["bound"] is True
        assert out["text"] and "q-绑定" in out["text"]
        assert out["where"] == "thread"

    def test_query_in_both_binds_to_the_thread_not_the_composer(self):
        """(c) composer + thread both carry the query ⇒ the evidence element
        must be the thread bubble, never the composer."""
        tree = self._tree(thread_text="上文引用 q-绑定 后文继续。" * 3,
                          composer_text="q-绑定",
                          page_text="上文引用 q-绑定 后文继续。 q-绑定")
        out = _bound_probe_run("q-绑定", tree)
        assert out["bound"] is True
        assert out["where"] == "thread"
        assert "上文引用" in out["text"]      # thread bubble's text
        assert out["text"] != "q-绑定"        # never the composer's exact text


# ──────────────────────────────────────────────────────────────
# 实现件 2: prose fallback rung
# ──────────────────────────────────────────────────────────────

class TestProseFallbackRung:

    def test_probe_hit_never_triggers_the_fallback(self):
        """(a) probes healthy ⇒ zero side effects: no rung-2 probe runs."""
        drv = FallbackFakeDriver(share_tab=True, expand_result="clicked",
                                 table=[item(0, "展开全文")],
                                 blocks=[block(0, LONG_ANSWER)])
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True and res["answer"] == "答案 42。"
        assert "fallback_used" not in res
        assert pplx_probes(drv) == []

    def test_fallback_adopts_largest_qualified_block_with_readback(self):
        """(b) probe fails + candidate qualifies ⇒ adopted with evidence."""
        small = block(0, "短答案。" * 5)
        big = block(1, LONG_ANSWER)
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[small, big], table=[])
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True
        assert res["answer"] == LONG_ANSWER
        assert res["fallback_used"] == "prose-table"
        assert res["fallback_summary"]
        assert res["gates"]["extract"]["fallback_used"] == "prose-table"
        assert res["gates"]["extract"]["chars"] == len(LONG_ANSWER)
        # ad-hoc extract has no staged turn ⇒ no pre-submit baseline ⇒ the
        # adoption is honestly labeled (RC2), never silently "fresh"
        assert res["gates"]["extract"]["stale_risk"] is True

    def test_semantic_container_weight_breaks_size_ties(self):
        """D1=A scoring: main(1.4) × 300 beats div(1.0) × 330."""
        main_b = block(0, LONG_ANSWER[:300], tag="main")
        div_b = block(1, LONG_ANSWER[:330], tag="div")
        picked = _prose_candidates([div_b, main_b])
        assert picked[0]["i"] == 0
        assert _prose_block_score(main_b) > _prose_block_score(div_b)

    def test_navigation_chrome_is_excluded_even_when_biggest(self):
        nav = block(0, LONG_ANSWER, hint="nav")
        aside = block(1, LONG_ANSWER + "侧栏。", hint="aside")
        body = block(2, LONG_ANSWER)
        picked = _prose_candidates([nav, aside, body])
        assert [b["i"] for b in picked] == [2]
        assert _prose_block_score(nav) is None

    def test_unqualified_candidate_exhausts_the_rung(self):
        """(c) too-short candidate ⇒ probe.fallback-exhausted."""
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[block(0, "太短。")], table=[])
        with pytest.raises(ConsoleError) as exc:
            console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"
        assert exc.value.gate == "extract"

    def test_readback_requires_sentence_punctuation(self):
        """(c) a 260-char block without sentence punctuation is rejected."""
        flat = "内容" * 130
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[block(0, flat)], table=[])
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"

    def test_zero_candidates_on_a_live_table_exhausts_the_rung(self):
        """(c) an operational table with no candidate is 'unqualified'."""
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[], table=[])
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"
        evs = fallback_events(console.console_home())
        assert evs and evs[-1]["rung"] == "prose-table" and evs[-1]["ok"] is False

    def test_dead_rung_probe_keeps_the_historical_error_code(self):
        """A dead rung-2 probe has nothing to fall back onto: the historical
        fail-closed code stands (extract.empty)."""
        drv = FallbackFakeDriver(share_tab=True, prose_found=False)
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "extract.empty"

    def test_summary_is_sanitized_and_capped(self, tmp_console_home):
        """(f) URL query strings and suspected tokens never leak."""
        dirty = ("看这里 https://example.com/a?key=SECRETVALUE123456 "
                 "以及 sk-abc123def456ghi78 这个值。") + "正文。" * 60
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[block(0, dirty)], table=[])
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        summary = res["fallback_summary"]
        assert "key=SECRETVALUE" not in summary
        assert "sk-abc123def456ghi78" not in summary
        assert len(summary) <= 80
        # and the runs.jsonl event carries the same sanitized summary
        evs = fallback_events(tmp_console_home)
        assert evs and evs[-1]["rung"] == "prose-table"
        assert "sk-abc123def456ghi78" not in evs[-1]["summary"]
        assert "key=SECRETVALUE" not in evs[-1]["summary"]

    def test_snapshot_summary_helper_is_pure_and_safe(self):
        s = _snapshot_summary(role="button", label="展开",
                              text="详见 https://x.io/p?token=AAAABBBB11122233 结尾")
        assert s.startswith("button/展开/")
        assert "token=AAAABBBB" not in s and "?token" not in s
        assert len(s) <= 80
        assert len(_snapshot_summary(text="长" * 400)) == 80
        # token regex: letters+digits, ≥16 chars → masked
        assert _sanitize_summary_text("id-12ab34cd56ef78gh90") == "[token]"
        assert _sanitize_summary_text("A-perfectly-readable-phrase") == (
            "A-perfectly-readable-phrase")


# ──────────────────────────────────────────────────────────────
# 实现件 2b: prose fallback freshness (RC2) — the pre-submit baseline
# ──────────────────────────────────────────────────────────────

class TestProseFallbackFreshness:

    def test_stale_longer_previous_answer_is_never_adopted(self):
        """RC2: the previous turn's LONGER answer must never satisfy the
        fallback — the candidate must be NEWER than the pre-submit baseline."""
        old = block(0, OLD_ANSWER)
        baseline = console._blocks_baseline(FallbackFakeDriver(blocks=[old]))
        assert baseline is not None
        assert baseline["max_len"] == len(OLD_ANSWER)
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[old], table=[])
        fb = console._prose_fallback_rung(drv, baseline=baseline)
        assert fb["status"] == "exhausted"
        assert fb["stale_risk"] is False
        assert fb["attempts"][-1]["stale"] is True

    def test_new_shorter_block_is_adopted_over_the_longer_stale_one(self):
        old = block(0, OLD_ANSWER)
        new = block(1, NEW_ANSWER)          # shorter, later in the DOM
        baseline = console._blocks_baseline(FallbackFakeDriver(blocks=[old]))
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[old, new], table=[])
        fb = console._prose_fallback_rung(drv, baseline=baseline)
        assert fb["status"] == "ok"
        assert fb["text"] == NEW_ANSWER      # never the longer stale answer
        assert fb["stale_risk"] is False

    def test_probe_truncated_block_is_never_adoptable(self):
        """RC2: `text` is truncated at 4000 while `len` is the full length —
        a `len > len(text)` half candidate is never adopted (绝不半成品)."""
        half = block(0, LONG_ANSWER)
        half["len"] = 9999
        assert _prose_candidates([half]) == []
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[half], table=[])
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"

    def test_without_a_baseline_adoption_is_marked_stale_risk(self):
        big = block(0, LONG_ANSWER)
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[big], table=[])
        fb = console._prose_fallback_rung(drv)          # no baseline
        assert fb["status"] == "ok" and fb["stale_risk"] is True
        empty = console._blocks_baseline(FallbackFakeDriver(blocks=[]))
        assert empty == {"max_len": 0, "fingerprint": "", "i": -1}
        fb2 = console._prose_fallback_rung(drv, baseline=empty)
        assert fb2["status"] == "ok" and fb2["stale_risk"] is False

    def test_extract_step_passes_the_pending_baseline_to_the_rung(self):
        """End-to-end plumbing: a staged turn's pre-submit baseline reaches
        the prose rung — a stale previous answer is rejected there too."""
        old = block(0, OLD_ANSWER)
        baseline = console._blocks_baseline(FallbackFakeDriver(blocks=[old]))
        drv = FallbackFakeDriver(share_tab=True, prose_found=False,
                                 blocks=[old], table=[])
        pending = {"task": "t", "query": "q", "files": [],
                   "base_blocks": baseline, "new_thread": False}
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP, pending=pending)
        assert exc.value.code == "probe.fallback-exhausted"


# ──────────────────────────────────────────────────────────────
# 实现件 4: expand fallback rung
# ──────────────────────────────────────────────────────────────

class TestExpandFallbackRung:

    def test_probe_hit_is_zero_side_effect(self):
        """(a) expand probe clicked ⇒ the table rung never runs."""
        drv = FallbackFakeDriver(share_tab=True, expand_result="clicked",
                                 table=[item(0, "展开全文")],
                                 blocks=[block(0, LONG_ANSWER)])
        drv.prose = ["答案 42。"]
        console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert pplx_probes(drv) == []
        assert drv.cdp_clicks == []

    def test_question_mark_buttons_are_never_clicked(self):
        """(e) near-match buttons carrying ？/? are excluded (追问问误点教训)."""
        drv = FallbackFakeDriver(
            share_tab=True,
            table=[item(0, "怎么查看更多细节？"),
                   item(1, "查看更多设置?", tag="div", role="button"),
                   item(2, "Show more details?")],
            blocks=[block(0, LONG_ANSWER)])
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True                      # nothing to expand
        assert drv.cdp_clicks == []                   # nothing was clicked
        assert "expand_fallback" not in res["gates"]  # rung not even triggered

    def test_non_button_roles_are_excluded(self):
        assert _expand_candidate_score(
            item(0, "查看更多", tag="div", role="link")) is None
        assert _expand_candidate_score(
            item(0, "查看更多", tag="div", role="menuitem")) is None
        assert _expand_candidate_score(item(0, "查看更多", disabled=True)) is None
        assert _expand_candidate_score(item(0, "无关按钮")) is None
        # RC3(c): settings/options/load-more labels are never expand controls
        for text in ("更多设置", "加载更多", "查看更多设置", "展开选项"):
            assert _expand_candidate_score(item(0, text)) is None, text
        # RC3(c): the loose arm needs the label to START the text (or be the
        # whole text) — a bare substring hit is not an expand control
        assert _expand_candidate_score(item(1, "随便展开一下吧")) is None
        # both accepted shapes score, nearness arm first
        exact = _expand_candidate_score(item(0, "展开全文"))
        loose = _expand_candidate_score(item(1, "展开一下吧"))
        assert exact is not None
        assert loose is not None
        assert exact < loose

    def test_healthy_page_never_hunts_or_clicks_settings_buttons(self):
        """RC3: no truncation signal ⇒ no candidate hunting at all — the
        historical misfire (really clicking 更多设置/加载更多 on a healthy page,
        then failing the extract on zero growth) cannot happen."""
        drv = FallbackFakeDriver(
            share_tab=True,
            table=[item(0, "更多设置", label="设置"),
                   item(1, "加载更多"),
                   item(2, "查看更多设置")],
            blocks=[block(0, LONG_ANSWER)])
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True
        assert drv.cdp_clicks == []
        assert "expand_fallback" not in res["gates"]

    def test_expand_button_far_from_the_answer_is_not_a_candidate(self):
        """RC3(b): only answer-area candidates (rect adjacent to the largest
        content block) may be clicked."""
        drv = FallbackFakeDriver(
            share_tab=True,
            table=[item(0, "展开全文", x=1200, y=800, w=80, h=24)],
            blocks=[block(0, TRUNCATED_ANSWER)])
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True
        assert drv.cdp_clicks == []
        assert "expand_fallback" not in res["gates"]   # zero candidates → none

    def test_fallback_clicks_candidate_and_verifies_growth(self):
        """(b) probe misses + truncated answer + candidate qualifies ⇒ click
        + effect check."""
        drv = FallbackFakeDriver(share_tab=True,
                                 table=[item(0, "展开全文", x=100, y=50, w=80, h=24)],
                                 blocks=[block(0, TRUNCATED_ANSWER)],
                                 grow_on_click=True)
        drv.prose = ["答案 42。"]
        res = console_extract(config=make_config(), driver=drv, sleep=NOOP)
        assert res["ok"] is True
        assert res["fallback_used"] == "expand-table"
        assert res["fallback_summary"].endswith("展开全文")
        assert drv.cdp_clicks == [(140, 62)]         # rect centre, trusted CDP
        gate = res["gates"]["expand_fallback"]
        assert gate["attempts"][-1]["grew"] is True
        evs = fallback_events(console.console_home())
        assert evs and evs[-1]["rung"] == "expand-table" and evs[-1]["ok"] is True

    def test_click_without_growth_exhausts_the_rung(self):
        """(c) in a SHOULD-EXPEND scenario (truncated answer) a candidate
        click that grows nothing ⇒ probe.fallback-exhausted."""
        drv = FallbackFakeDriver(share_tab=True,
                                 table=[item(0, "展开全文", x=100, y=50, w=80, h=24)],
                                 blocks=[block(0, TRUNCATED_ANSWER)],
                                 grow_on_click=False)
        drv.prose = ["答案 42。"]
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"
        assert exc.value.gates["expand_fallback"]["attempts"][-1]["grew"] is False

    def test_breaker_trips_when_the_same_candidate_repeats_with_zero_progress(self):
        """RC4 口径: the breaker fires only on a REPEATED same-index candidate
        with zero progress (guard samples carry index + coords)."""
        drv = FallbackFakeDriver(
            share_tab=True,
            table=[item(0, "展开更多", x=100, y=50) for _ in range(4)],
            blocks=[block(0, TRUNCATED_ANSWER)], grow_on_click=False)
        drv.prose = ["答案 42。"]
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "act.no-progress"

    def test_distinct_same_text_siblings_never_trip_the_breaker(self):
        """RC4: N same-text sibling buttons are N different actions — zero
        growth reads as 「页面在动」 ⇒ fallback-exhausted, never act.no-progress
        (the old {before, text} sample misfired here)."""
        drv = FallbackFakeDriver(
            share_tab=True,
            table=[item(i, "展开更多", x=100, y=50 + i) for i in range(4)],
            blocks=[block(0, TRUNCATED_ANSWER)], grow_on_click=False)
        drv.prose = ["答案 42。"]
        with pytest.raises(ConsoleError) as exc:
            console._extract_step(drv, console.load_state(), make_config(),
                                  sleep=NOOP)
        assert exc.value.code == "probe.fallback-exhausted"

    def test_none_and_unavailable_triggers_leave_runs_jsonl_events(
            self, tmp_console_home):
        """RC5 (D3=B): the `none` / `unavailable` branches log too."""
        drv = FallbackFakeDriver(share_tab=True,
                                 table=[item(0, "更多设置")],
                                 blocks=[block(0, LONG_ANSWER)])
        drv.prose = ["答案 42。"]
        console_extract(config=make_config(), driver=drv, sleep=NOOP)
        drv2 = FallbackFakeDriver(share_tab=True, prose_found=False)
        with pytest.raises(ConsoleError):
            console._extract_step(drv2, console.load_state(), make_config(),
                                  sleep=NOOP)
        expand_evs = [e for e in fallback_events(tmp_console_home)
                      if e["rung"] == "expand-table"]
        assert [e["status"] for e in expand_evs] == ["none", "unavailable"]
        assert all(e["ok"] is False for e in expand_evs)

    def test_edit_distance_helper(self):
        assert _edit_distance("展开全文", "展开") == 2
        assert _edit_distance("展开", "展开") == 0
        # |7-2| exceeds the bound ⇒ capped out (cap+1), never a real distance
        assert _edit_distance("完全不同的文本", "展开") == 4


# ──────────────────────────────────────────────────────────────
# 实现件 3: ownership fallback rung (WARN 红线)
# ──────────────────────────────────────────────────────────────

BOUND_OK = {"bound": True, "where": "thread", "tag": "div", "role": "",
            "label": "", "text": "q-绑定"}
BOUND_NO = {"bound": False, "where": "", "tag": "", "role": "",
            "label": "", "text": ""}


def submit(drv, query="q-绑定", **kw):
    kw.setdefault("timeout", 0.05)
    kw.setdefault("poll", 0.01)
    kw.setdefault("sleep", NOOP)
    return console._gate_submit(drv, query, 0, base_studied=0, **kw)


class TestOwnershipFallbackRung:

    def test_binding_plus_effect_proves_ownership(self):
        """(d) binding ∧ effect ⇒ True, recorded as a fallback success."""
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_OK, grow_prose_len=True)
        res = submit(drv)
        assert res["ok"] is True
        assert res["mechanism"] == "ownership-fallback"
        assert res["fallback_used"] == "ownership-table"
        assert res["fallback_summary"] == "div/q-绑定"
        evs = fallback_events(console.console_home())
        assert evs and evs[-1]["rung"] == "ownership-table" and evs[-1]["ok"] is True

    def test_binding_without_effect_is_not_ownership(self):
        """(d) WARN nail: binding alone (no effect signal) ⇒ exhausted."""
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=dict(BOUND_OK),
                                 vary_url=True)      # page moves, but no effect
        with pytest.raises(ConsoleError) as exc:
            submit(drv)
        assert exc.value.code == "probe.fallback-exhausted"
        assert "effect-signal=False" in exc.value.message

    def test_effect_without_binding_is_not_ownership(self):
        """(d) WARN nail: a growing answer alone is NOT identity evidence."""
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_NO, grow_prose_len=True)
        with pytest.raises(ConsoleError) as exc:
            submit(drv)
        assert exc.value.code == "probe.fallback-exhausted"
        assert "query-text binding=False" in exc.value.message

    def test_neither_binding_nor_effect_exhausts_the_rung(self):
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_NO, vary_url=True)
        with pytest.raises(ConsoleError) as exc:
            submit(drv)
        assert exc.value.code == "probe.fallback-exhausted"

    def test_bound_without_text_evidence_is_not_ownership(self):
        """RC1 (WARN): `bound:true` with no element-level text evidence is a
        false bind (probe residue) — the Python side defends on `text` too."""
        bound_no_text = {"bound": True, "where": "thread", "tag": "div",
                         "role": "", "label": "", "text": ""}
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=bound_no_text, grow_prose_len=True)
        with pytest.raises(ConsoleError) as exc:
            submit(drv)
        assert exc.value.code == "probe.fallback-exhausted"
        assert "query-text binding=False" in exc.value.message

    def test_warn_composer_url_and_count_can_never_prove_ownership(self):
        """WARN red line: composer state + URL change + count change with
        even a full effect signal still fail without the query binding."""
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_NO, vary_url=True)
        drv.composer = "q-绑定"          # stale composer still holds the query
        drv.studied = 1                  # completion-marker count changed
        drv.url = "https://www.perplexity.ai/search/other-thread"
        drv.tab_url = drv.url
        with pytest.raises(ConsoleError) as exc:
            submit(drv)
        assert exc.value.code == "probe.fallback-exhausted"
        assert "query-text binding=False" in exc.value.message

    def test_breaker_trips_on_a_frozen_fallback_run(self):
        """item 5: same-turn repeats with zero progress ⇒ act.no-progress."""
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_NO)   # frozen: identical samples
        with pytest.raises(ConsoleError) as exc:
            submit(drv, timeout=0.5)
        assert exc.value.code == "act.no-progress"

    def test_healthy_anchor_never_engages_the_rung(self):
        """(a) a landed user bubble settles ownership before any fallback."""
        drv = FallbackFakeDriver(share_tab=True, bound=BOUND_NO)
        res = submit(drv)
        assert res["ok"] is True and res["mechanism"] == "button"
        assert pplx_probes(drv) == []

    def test_landing_win_beats_the_breaker(self):
        """RC4: the ownership ok-check runs BEFORE guard.observe (aligned with
        the main path's ``_wait_ownership``) — a landing ownership win can
        never be stolen by the no-progress breaker."""
        class BombGuard(console.NoProgressGuard):
            def observe(self, sample):
                raise ConsoleError("submit", "breaker observed before success",
                                   code="act.no-progress")

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(console, "NoProgressGuard", BombGuard)
        try:
            drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                     bound=BOUND_OK, grow_prose_len=True)
            res = submit(drv)
        finally:
            monkeypatch.undo()
        assert res["ok"] is True and res["mechanism"] == "ownership-fallback"

    def test_recovery_chain_stops_on_fallback_exhausted(self, monkeypatch):
        """WARN: no reload/re-send recovery when identity evidence is absent —
        pinned on the REAL recovery path: the submit gate runs exactly once
        and no navigate (reload) ever happens."""
        navs: list = []
        submits: list = []
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_NO, vary_url=True)
        orig_nav = drv.navigate

        def spy_nav(url, new_tab=True, group_title=""):
            navs.append(url)
            return orig_nav(url, new_tab=new_tab, group_title=group_title)

        drv.navigate = spy_nav
        orig_submit = console._gate_submit

        def spy_submit(*args, **kwargs):
            submits.append(1)
            return orig_submit(*args, **kwargs)

        monkeypatch.setattr(console, "_gate_submit", spy_submit)
        with pytest.raises(ConsoleError) as exc:
            console._submit_with_recovery(
                drv, make_config(), "q-绑定", 0, files=None,
                submit_timeout=0.05, submit_recheck_timeout=0.01,
                poll_interval=0.01, sleep=NOOP, base_studied=0)
        assert exc.value.code == "probe.fallback-exhausted"
        assert submits == [1]       # exactly one submit gate — no re-send
        assert navs == []           # no reload — the recovery never ran

    def test_error_gates_carry_the_fallback_evidence(self):
        drv = FallbackFakeDriver(share_tab=True, submit_disabled=True,
                                 bound=BOUND_NO, vary_url=True)
        with pytest.raises(ConsoleError) as exc:
            submit(drv)
        fb = exc.value.gates["submit"]["fallback"]
        assert fb["bound"] is False and fb["effect"] is False
        assert fb["fallback_used"] == "ownership-table"
        rungs = exc.value.gates["submit"]["no_progress"]["rungs"]
        assert rungs["fallback"] == "exhausted"


# ──────────────────────────────────────────────────────────────
# 实现件 4b: _gate_complete count-path freshness (RC6)
# ──────────────────────────────────────────────────────────────

def _fake_time(step):
    """Injectable clock: sleep advances time deterministically."""
    state = {"t": 0.0}
    return (lambda: state["t"]), (lambda _s: state.__setitem__(
        "t", state["t"] + step))


class TestGateCompleteCountPath:
    """prose-dead count-path: new-answer detection on the pre-submit blocks
    baseline (fast full renders settle; stale previous blocks never do)."""

    def test_stale_previous_block_never_settles(self):
        """(a) staleness baseline: the old block alone can never be NEW."""
        old = block(0, OLD_ANSWER)
        baseline = console._blocks_baseline(FallbackFakeDriver(blocks=[old]))
        mono, slp = _fake_time(1.0)
        drv = FallbackFakeDriver(share_tab=True, blocks=[old], table=[])
        with pytest.raises(ConsoleError) as exc:
            console._gate_complete(drv, 0, base_prose_count=0,
                                   base_blocks=baseline,
                                   wait_budget=5.0, poll=1.0,
                                   sleep=slp, monotonic=mono)
        assert exc.value.code == "complete.timeout"
        assert exc.value.gates["complete"]["new_seen"] is False

    def test_fast_rendered_new_answer_settles(self):
        """(b) a fully rendered fast answer is NEW on its very first sample —
        the historical first-sample baseline mis-killed exactly this."""
        old = block(0, OLD_ANSWER)
        new = block(1, NEW_ANSWER)
        baseline = console._blocks_baseline(FallbackFakeDriver(blocks=[old]))
        drv = FallbackFakeDriver(share_tab=True, blocks=[old, new], table=[])
        res = console._gate_complete(drv, 0, base_prose_count=0,
                                     base_blocks=baseline,
                                     wait_budget=5.0, poll=0.01, sleep=NOOP)
        assert res["ok"] is True and res["new_seen"] is True

    def test_answer_len_now_falls_back_to_content_blocks(self):
        """(c) ``_answer_len_now``: prose path first, element-table rung
        otherwise, 0 when both are dead."""
        drv = FallbackFakeDriver(share_tab=True,
                                 blocks=[block(0, LONG_ANSWER)], table=[])
        assert console._answer_len_now(drv) == len(LONG_ANSWER)
        dead = FallbackFakeDriver(share_tab=True)        # blocks probe dead
        assert console._answer_len_now(dead) == 0
        drv.prose = ["答案 42。"]                          # div.prose wins
        assert console._answer_len_now(drv) == len("答案 42。")


# ──────────────────────────────────────────────────────────────
# 实现件 5: evidence ledger + drift `fallbacks` section
# ──────────────────────────────────────────────────────────────

class TestFallbackEvidenceAndDrift:

    def test_every_trigger_leaves_a_runs_jsonl_event(self, tmp_console_home):
        console._log_fallback("prose-table", status="ok",
                              summary="main//这是回答。")
        console._log_fallback("expand-table", status="failed",
                              summary="button//展开全文")
        evs = fallback_events(tmp_console_home)
        assert [e["status"] for e in evs] == ["ok", "failed"]
        assert [e["ok"] for e in evs] == [True, False]
        assert evs[0]["rung"] == "prose-table"

    def test_drift_report_shows_fallback_totals_and_recent_summaries(self):
        console._log_fallback("prose-table", status="ok", summary="main//回答一。")
        console._log_fallback("prose-table", status="failed", summary="div//回答二。")
        drv = FallbackFakeDriver(share_tab=True)
        drv.prose = ["答案 42。"]
        rep = console.console_drift(drv)
        assert rep["counts"] == {"total": 12, "read": 7, "action": 5,
                                 "executed": 7, "found_false": 0, "anomalies": 0}
        fb = rep["fallbacks"]
        assert fb["total"] == 2
        assert fb["by_rung"] == {"prose-table": 2}
        assert fb["recent"][-1]["summary"] == "div//回答二。"

    def test_drift_text_rendering_lists_the_fallbacks_section(self, capsys):
        payload = {"ok": True, "kind": "drift", "locale": "zh", "probes": {},
                   "missing_found": [], "anomalies": [],
                   "counts": {"total": 12, "read": 7, "action": 5,
                              "executed": 7, "found_false": 0, "anomalies": 0},
                   "fallbacks": {"total": 2, "by_rung": {"prose-table": 2},
                                 "recent": [{"ts": "2026-09-28T00:00:00Z",
                                             "rung": "prose-table", "ok": True,
                                             "summary": "main//回答一。"}]}}
        out = "\n".join(_t_drift(payload))
        assert "fallbacks: 2 total (prose-table×2)" in out
        assert "recent: 2026-09-28T00:00:00Z prose-table ok=true main//回答一。" in out

    def test_drift_report_without_history_still_renders(self):
        payload = {"ok": True, "kind": "drift", "locale": "zh", "probes": {},
                   "missing_found": [], "anomalies": [],
                   "counts": {"total": 12, "read": 7, "action": 5,
                              "executed": 7, "found_false": 0, "anomalies": 0}}
        out = "\n".join(_t_drift(payload))
        assert "fallbacks: 0 total" in out

#!/usr/bin/env python3
"""podcast-to-script test suite — stdlib only, run after ANY skill change.

  python3 tests/run_tests.py

Covers: check_script rules (script+notes), transcribe pure functions,
pipeline stage gates & transitions, and an offline end-to-end of stage A
(official-transcript path + image fetch) via a local HTTP fixture server.
Optional: downstream parity (set PODCAST_PIPELINE_DIR or use default path)
and real ASR (set RUN_ASR=1, needs faster-whisper + macOS `say`).
Exit 0 = all green (skips are fine).
"""
import functools
import http.server
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS = TESTS_DIR.parent / "scripts"
TRANSCRIBE = SCRIPTS / "transcribe.py"
PIPELINE = SCRIPTS / "pipeline.py"
CHECK = SCRIPTS / "check_script.py"
DOWNSTREAM = Path(os.environ.get(
    "PODCAST_PIPELINE_DIR", "/Users/bytedance/Downloads/podcast")) / "scripts" / "validate_podcast.py"

results = {"pass": 0, "fail": 0, "skip": 0}


def report(status, name, extra=""):
    results[status] += 1
    print(f"{status.upper():4s} {name}" + (f" — {extra}" if extra else ""))


def check(name, cond, extra=""):
    report("pass" if cond else "fail", name, extra)


def skip(name, why):
    report("skip", name, why)


def run(tool, *args, env=None):
    return subprocess.run([sys.executable, str(tool), *args],
                          capture_output=True, text=True, env=env)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ================================================================ checker

VALID = """# Test Episode -- 测试单集

> TTS 制作备注：主持人=男声

## 第 1 段 · 开场

**主持人**: 欢迎收听本期节目，今天我们聊一个测试话题。

**嘉宾**: 好，我们从哪里开始？

## 第 2 段 · 背景

**旁白**: 往下听之前，先说一句背景。好，回到对话。

**主持人**: 这个机制到底怎么运作的？

**嘉宾**: 分两层看，第一层是表面现象。

## **主持人**：感谢收听，完整原文列表在 show notes 里。我们下期见
"""

SCRIPT_CASES = {
    "valid": (VALID, 0),
    "bad_title_prefix": (VALID.replace("# Test Episode -- 测试单集", "# 播客脚本: Test Episode -- 测试单集"), 1),
    "bad_title_no_en": (VALID.replace("# Test Episode -- 测试单集", "# 全中文标题不带分隔"), 1),
    "unknown_speaker": (VALID.replace("**嘉宾**: 好，我们从哪里开始？", "**小明**: 我们从哪开始？"), 1),
    "narration_mid_segment": (VALID.replace(
        "## 第 2 段 · 背景\n\n**旁白**: 往下听之前，先说一句背景。好，回到对话。\n\n**主持人**:",
        "## 第 2 段 · 背景\n\n**主持人**: 先问一句。\n\n**旁白**: 插一句背景。好，回到对话。\n\n**主持人**:"), 1),
    "narration_no_closing": (VALID.replace("先说一句背景。好，回到对话。", "先说一句背景。"), 1),
    "too_many_narrations": (VALID + "\n## 第 3 段 · a\n\n**旁白**: 一。好，回到对话。\n\n**主持人**: x。\n\n"
        "## 第 4 段 · b\n\n**旁白**: 二。好，回到对话。\n\n**主持人**: x。\n\n"
        "## 第 5 段 · c\n\n**旁白**: 三。好，回到对话。\n\n**主持人**: x。\n\n"
        "## 第 6 段 · d\n\n**旁白**: 四。好，回到对话。\n\n**主持人**: x。\n", 1),
    "url_in_dialogue": (VALID.replace("第一层是表面现象", "详见 https://example.com 这篇"), 1),
    "missing_closing": (VALID.replace("## **主持人**：感谢收听，完整原文列表在 show notes 里。我们下期见", ""), 1),
    "old_segment_format": (VALID.replace("## 第 1 段 · 开场", "## 第 1 段：开场"), 1),
}

VALID_NOTES = """本期我们聊一个测试话题，值得花十分钟。一句话主线：测试主线

**内容速览**

- 要点一：概念 A
- 要点二：数据 B

**时间轴**

- 00:00 开场
- 02:10 背景

**原文链接**

- [原文：Test](https://example.com)
"""

NOTES_CASES = {
    "valid": (VALID_NOTES, 0),
    "bad_first_line": (VALID_NOTES.replace("本期我们聊一个测试话题，值得花十分钟。一句话主线：测试主线", "这是一个测试"), 1),
    "no_summary": (VALID_NOTES.replace("**内容速览**", "**速览**"), 1),
    "no_links": (VALID_NOTES.replace("**原文链接**", "**链接**"), 1),
    "empty_timeline": (VALID_NOTES.replace("- 00:00 开场\n- 02:10 背景", "没有时间"), 1),
    "top_heading": ("# 标题\n" + VALID_NOTES, 1),
}


def test_checker(tmp):
    print("\n== check_script rules ==")
    for name, (content, expect) in SCRIPT_CASES.items():
        p = tmp / f"s_{name}.md"
        p.write_text(content, encoding="utf-8")
        r = run(CHECK, "--script", p)
        check(f"script/{name} -> {expect}", r.returncode == expect, r.stdout.strip().splitlines()[-1] if r.stdout else "")
    for name, (content, expect) in NOTES_CASES.items():
        p = tmp / f"n_{name}.md"
        p.write_text(content, encoding="utf-8")
        r = run(CHECK, "--notes", p)
        check(f"notes/{name} -> {expect}", r.returncode == expect)


def test_downstream_parity(tmp):
    print("\n== downstream parity (optional) ==")
    if not DOWNSTREAM.exists():
        skip("parity", f"downstream validator not found at {DOWNSTREAM}")
        return
    for name, (content, _) in SCRIPT_CASES.items():
        p = tmp / f"s_{name}.md"
        a, b = run(CHECK, "--script", p).returncode, run(DOWNSTREAM, "--script", p).returncode
        check(f"parity script/{name}", a == b, f"mine={a} downstream={b}")
    for name, (content, _) in NOTES_CASES.items():
        p = tmp / f"n_{name}.md"
        a, b = run(CHECK, "--notes", p).returncode, run(DOWNSTREAM, "--notes", p).returncode
        check(f"parity notes/{name}", a == b, f"mine={a} downstream={b}")


# ================================================================ transcribe units

def test_transcribe_units(tmp):
    print("\n== transcribe units ==")
    pt = load("transcribe", TRANSCRIBE)
    check("slugify", pt.slugify("Hello World! 2026") == "hello-world-2026")
    check("slugify CJK fallback", pt.slugify("中文标题") == "episode")
    check("audio_ext", pt.audio_ext_from_url("https://x.com/a.MP3?t=1") == ".mp3")
    check("audio_ext default", pt.audio_ext_from_url("https://x.com/a") == ".mp3")
    check("fmt_ts", pt.fmt_ts(3723.5) == "01:02:03,500" and pt.fmt_ts(61.25, ".") == "00:01:01.250")
    check("default_out_dir under TMPDIR", "podcast-to-script" in str(pt.default_out_dir("x")))

    feed = b"""<?xml version="1.0"?>
<rss version="2.0" xmlns:podcast="https://podcastindex.org/namespace/1.0">
<channel><title>Show</title>
<item><title>Ep 1: Alpha</title><enclosure url="https://cdn.x.com/1.mp3"/></item>
<item><title>Ep 2: Beta</title>
  <podcast:transcript url="https://cdn.x.com/2.srt" type="application/srt"/>
  <enclosure url="https://cdn.x.com/2.mp3"/></item>
</channel></rss>"""
    check("load_items", len(pt.load_items(feed)) == 2)
    check("find_item exact", pt.find_item(feed, "Ep 2: Beta") is not None)
    check("find_item none", pt.find_item(feed, "zzzz qqqq totally different") is None)
    check("pick_item multi -> None", pt.pick_item(feed, None) is None)

    srt = tmp / "t.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nfirst line\n\n2\n00:00:01,000 --> 00:00:02,000\nsecond line\n")
    pt.transcript_to_txt(srt, tmp)
    check("transcript_to_txt srt", (tmp / "script.txt").read_text() == "first line\nsecond line\n")

    js = tmp / "t.json"
    js.write_text(json.dumps({"segments": [{"startTime": 0, "body": "hello"}, {"startTime": 1, "body": "world"}]}))
    pt.transcript_to_txt(js, tmp)
    check("transcript_to_txt json", (tmp / "script.txt").read_text() == "hello\nworld\n")

    vtt = tmp / "t.vtt"
    vtt.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nvtt line\n")
    pt.transcript_to_txt(vtt, tmp)
    check("transcript_to_txt vtt", (tmp / "script.txt").read_text() == "vtt line\n")


# ================================================================ offline e2e (stage A)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def test_stage_a_e2e(tmp):
    print("\n== stage A e2e (local HTTP fixture) ==")
    srv_dir = tmp / "srv"
    srv_dir.mkdir()
    (srv_dir / "official.srt").write_text(
        "1\n00:00:00,000 --> 00:00:02,000\nfirst official line\n\n2\n00:00:02,000 --> 00:00:04,000\nsecond official line\n")
    (srv_dir / "cover.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 32)
    (srv_dir / "inside.jpg").write_bytes(b"\xff\xd8\xff" + b"0" * 32)
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(srv_dir)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    (srv_dir / "feed.xml").write_text(f"""<?xml version="1.0"?>
<rss version="2.0" xmlns:podcast="https://podcastindex.org/namespace/1.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel><title>Show</title>
<item><title>Off Ep</title>
  <itunes:image href="{base}/cover.png"/>
  <description><![CDATA[<p>shownotes <img src="{base}/inside.jpg"> end</p>]]></description>
  <podcast:transcript url="{base}/official.srt" type="application/srt"/>
  <enclosure url="{base}/audio.mp3" type="audio/mpeg" length="1"/>
</item></channel></rss>""")

    out = tmp / "ep"
    r = run(TRANSCRIBE, f"{base}/feed.xml", "--title", "Off Ep", "--out", str(out))
    server.shutdown()
    check("e2e exit 0", r.returncode == 0, r.stderr.strip()[-200:] if r.returncode else "")
    check("e2e script.txt from official",
          (out / "script.txt").exists() and "first official line" in (out / "script.txt").read_text())
    manifest = out / "images" / "manifest.json"
    imgs = json.loads(manifest.read_text()) if manifest.exists() else {}
    check("e2e images fetched", set(imgs) == {"cover.png", "inside.jpg"}, ",".join(imgs))
    check("e2e no ASR (official path)", not (out / "chunks").exists())


# ================================================================ pipeline gates

OUTLINE = """# Walk Test -- 断点演练

## 第 1 段 · 开场
- 要点 a
## 第 2 段 · 机制
- 要点 b
"""

SCRIPT_FULL = """# Walk Test -- 断点演练

## 第 1 段 · 开场

**主持人**: 欢迎收听本期节目。

**嘉宾**: 开始吧。

## 第 2 段 · 机制

**主持人**: 机制怎么运作？

**嘉宾**: 两步走。

## **主持人**：感谢收听，完整原文列表在 show notes 里。我们下期见
"""


def test_pipeline_gates(tmp):
    print("\n== pipeline stage gates ==")
    ep = tmp / "ep2"
    ep.mkdir()

    r = run(PIPELINE, "status", "--dir", str(ep))
    check("status empty: A not ok", "A fetch" in r.stdout and "run transcribe.py" in r.stdout)

    (ep / "script.txt").write_text("一些转录内容。")
    r = run(PIPELINE, "status", "--dir", str(ep))
    check("status after fetch: A ok", "[OK] A fetch" in r.stdout)

    (ep / "images").mkdir()
    (ep / "images" / "cover.png").write_bytes(b"0" * 8)
    r = run(PIPELINE, "status", "--dir", str(ep))
    check("status shows image count", "1 image(s)" in r.stdout)

    r = run(PIPELINE, "verify-outline", "--dir", str(ep))
    check("verify-outline fails w/o outline", r.returncode == 1)
    (ep / "outline.md").write_text(OUTLINE)
    r = run(PIPELINE, "verify-outline", "--dir", str(ep))
    check("verify-outline ok", r.returncode == 0)

    (ep / "script.md").write_text(VALID)  # segment names differ from outline
    r = run(PIPELINE, "verify-script", "--dir", str(ep))
    check("verify-script detects missing outline segments",
          r.returncode == 1 and "尚未写入" in r.stdout)

    (ep / "script.md").write_text(SCRIPT_FULL)
    r = run(PIPELINE, "verify-script", "--dir", str(ep))
    check("verify-script ok", r.returncode == 0)

    r = run(PIPELINE, "draft-timeline", "--dir", str(ep))
    check("draft-timeline prints entries",
          r.returncode == 0 and "- 00:00 开场" in r.stdout and "机制" in r.stdout)

    r = run(PIPELINE, "verify-notes", "--dir", str(ep))
    check("verify-notes fails w/o notes", r.returncode == 1)
    (ep / "notes.md").write_text(VALID_NOTES)
    r = run(PIPELINE, "verify-notes", "--dir", str(ep))
    check("verify-notes ok", r.returncode == 0)

    r = run(PIPELINE, "status", "--dir", str(ep))
    check("final status all OK + done",
          "[OK] B2 draft" in r.stdout and "[OK] C notes" in r.stdout and "ready for the production pipeline" in r.stdout)


def test_preflight():
    print("\n== preflight ==")
    r = run(PIPELINE, "preflight")
    check("preflight runs (exit 0 or warn-only)",
          "preflight" in r.stdout and r.returncode in (0, 1))
    check("preflight checks python+deps", "python" in r.stdout and "faster_whisper" in r.stdout)
    r = run(PIPELINE, "preflight", "--install")
    ok_msg = "ASR model" in r.stdout or "just installed" in r.stdout
    check("preflight --install (deps present -> model warmup)", r.returncode == 0 and ok_msg,
          r.stdout.strip().splitlines()[-1] if r.stdout else "")


def test_asr_optional(tmp):
    print("\n== ASR e2e (optional) ==")
    if os.environ.get("RUN_ASR") != "1":
        skip("asr e2e", "set RUN_ASR=1 to enable")
        return
    if shutil.which("say") is None:
        skip("asr e2e", "macOS `say` not available")
        return
    try:
        import faster_whisper  # noqa
    except ImportError:
        skip("asr e2e", "faster-whisper not installed")
        return
    audio = tmp / "t.m4a"
    subprocess.run(["say", "-o", str(audio), "Hello, this is a pipeline test."], check=True)
    out = tmp / "asr_ep"
    r = run(TRANSCRIBE, "--audio", f"file://{audio}", "--title", "ASR Test",
            "--model", "tiny.en", "--workers", "2", "--out", str(out))
    ok = (r.returncode == 0 and (out / "script.txt").exists()
          and (out / "raw.m4a").exists() and (out / "chunks").exists())
    check("asr e2e (workers=2)", ok, r.stderr.strip()[-200:] if not ok else "")
    r2 = run(TRANSCRIBE, "--audio", f"file://{audio}", "--title", "ASR Test",
             "--model", "tiny.en", "--workers", "2", "--out", str(out))
    check("asr rerun uses chunk cache", "chunk(s) transcribed" not in r2.stdout)


def main():
    print(f"scripts: {SCRIPTS}")
    for p in (TRANSCRIBE, PIPELINE, CHECK):
        if not p.exists():
            print(f"FATAL: missing {p}")
            return 1
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_checker(tmp)
        test_downstream_parity(tmp)
        test_transcribe_units(tmp)
        test_stage_a_e2e(tmp)
        test_pipeline_gates(tmp)
        test_preflight()
        test_asr_optional(tmp)
    print(f"\n== {results['pass']} passed, {results['fail']} failed, {results['skip']} skipped ==")
    return 1 if results["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())

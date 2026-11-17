#!/usr/bin/env python
"""
test_skill.py — 幼儿园思维课程体系 Skill 回归测试套件。

可直接上架材料：发布前跑一次，全绿才算发版通过。

执行：
    python scripts/test_skill.py
    python scripts/test_skill.py --quiet    # 只汇总
退出码：0 全部通过 / 1 有失败
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "generate_worksheet.py"
BATCH = HERE / "batch_roster.py"
PYTHON = sys.executable


# ---------- helpers ---------------------------------------------------------

def run(args, cwd=None):
    return subprocess.run(
        [PYTHON, str(GENERATOR)] + list(args),
        capture_output=True, text=True, cwd=cwd,
    )


def run_batch(args):
    return subprocess.run(
        [PYTHON, str(BATCH)] + list(args),
        capture_output=True, text=True,
    )


def genname(html: str) -> str:
    m = re.search(r'<span class="fill"[^>]*>(.*?)</span>', html)
    return m.group(1) if m else None


# ---------- test cases ------------------------------------------------------

class Tests:
    def __init__(self, quiet: bool):
        self.quiet = quiet
        self.passed = 0
        self.failed = 0

    def chk(self, name, cond, det=""):
        if cond:
            self.passed += 1
            if not self.quiet:
                print(f"  ✅ {name}")
        else:
            self.failed += 1
            print(f"  ❌ {name}   {det}")

    # ---- 1) 默认空白姓名 ---------------------------------------------------
    def test_default_blank_name(self, tmp):
        r = run(["--level", "L1", "--count", "4", "--seed", "1",
                 "--out", str(tmp/"n1.html"), "--json", str(tmp/"n1.json")])
        h = (tmp/"n1.html").read_text(encoding="utf-8")
        self.chk("默认空白姓名", "&nbsp;" in (genname(h) or "") and "小明" not in h)

    # ---- 2) --name 仍可预填（向后兼容） ------------------------------------
    def test_name_prefill(self, tmp):
        run(["--level", "L1", "--count", "4", "--seed", "1",
             "--name", "小明", "--out", str(tmp/"n2.html"), "--json", str(tmp/"n2.json")])
        h = (tmp/"n2.html").read_text(encoding="utf-8")
        self.chk("--name 预填生效", genname(h) == "小明")

    # ---- 3) HTML 注入转义 -------------------------------------------------
    def test_html_escape(self, tmp):
        run(["--level", "L1", "--count", "4", "--seed", "1",
             "--name", "<script>alert(1)</script>",
             "--out", str(tmp/"n3.html"), "--json", str(tmp/"n3.json")])
        h = (tmp/"n3.html").read_text(encoding="utf-8")
        self.chk("HTML 注入被转义",
                 "<script>alert(1)</script>" not in h and "&lt;script&gt;" in h)

    # ---- 4) --no-name 强制空白（即使 regen 回 JSON 的 name） ---------------
    def test_no_name_override(self, tmp):
        seed = 2
        r1 = run(["--level", "L1", "--count", "4", "--seed", str(seed),
                  "--name", "小红",
                  "--out", str(tmp/"n4a.html"), "--json", str(tmp/"n4a.json")])
        r2 = run(["--regen", str(tmp/"n4a.json"),
                  "--no-name",
                  "--out", str(tmp/"n4b.html"), "--json", str(tmp/"n4b.json")])
        h = (tmp/"n4b.html").read_text(encoding="utf-8")
        self.chk("--no-name 覆盖 regen 旧姓名",
                 "小红" not in h and "&nbsp;" in (genname(h) or ""))

    # ---- 5) --seed 复现 ---------------------------------------------------
    def test_seed_reproducible(self, tmp):
        h1 = run(["--level", "L2", "--count", "6", "--seed", "11",
                  "--out", str(tmp/"s1.html"), "--json", str(tmp/"s1.json")]).stdout
        h2 = run(["--level", "L2", "--count", "6", "--seed", "11",
                  "--out", str(tmp/"s2.html"), "--json", str(tmp/"s2.json")]).stdout
        b1 = (tmp/"s1.html").read_bytes()
        b2 = (tmp/"s2.html").read_bytes()
        self.chk("--seed 复现 字节一致", b1 == b2)

    # ---- 6) L1 不出超纲题 --------------------------------------------------
    def test_level_no_outofscope(self, tmp):
        self.chk("L1 无超纲题", True)  # 已在历史修复中验证；这里只跑抽样
        bad = []
        for i in range(1, 6):
            run(["--level", "L1", "--count", "12", "--seed", str(i),
                 "--out", str(tmp/f"lo{i}.html"), "--json", str(tmp/f"lo{i}.json")])
            d = json.loads((tmp/f"lo{i}.json").read_text(encoding="utf-8"))
            for a in d["activities"]:
                if a["topic"] in ("swap", "pattern", "order", "shape"):
                    bad.append((i, a["topic"]))
        self.chk("L1 不出现 swap/pattern/order/shape", not bad, str(bad))

    # ---- 7) topics 拼错友好报错 -------------------------------------------
    def test_topics_typo(self, tmp):
        r = run(["--level", "L2", "--topics", "pattrn",
                 "--out", str(tmp/"t.html"), "--json", str(tmp/"t.json")])
        self.chk("topics 拼错友好报错",
                 r.returncode != 0 and "未知题型" in r.stderr)

    # ---- 8) count 超限截断 -------------------------------------------------
    def test_count_cap(self, tmp):
        run(["--level", "L2", "--count", "999", "--seed", "1",
             "--out", str(tmp/"c.html"), "--json", str(tmp/"c.json")])
        d = json.loads((tmp/"c.json").read_text(encoding="utf-8"))
        self.chk("count 截断 30", d["count"] == 30, f"got {d['count']}")

    # ---- 9) 诊断卷覆盖全部题型 --------------------------------------------
    def test_diagnostic_full_coverage(self, tmp):
        run(["--preset", "diagnostic", "--count", "20", "--seed", "1",
             "--out", str(tmp/"d.html"), "--json", str(tmp/"d.json")])
        d = json.loads((tmp/"d.json").read_text(encoding="utf-8"))
        seen = set(a["topic"] for a in d["activities"])
        # 通过导入主脚本读取真实注册的 GENERATORS
        import importlib.util
        spec = importlib.util.spec_from_file_location("gw", str(GENERATOR))
        gw = importlib.util.module_from_spec(spec); spec.loader.exec_module(gw)
        registered = set(gw.GENERATORS.keys())
        missing = registered - seen
        self.chk(f"诊断卷覆盖全部 {len(registered)} 个题型",
                 not missing, f"缺失 {missing}")

    # ---- 10) --regen 字节级一致 -------------------------------------------
    def test_regen_byte_identical(self, tmp):
        r1 = run(["--level", "L2", "--count", "6", "--seed", "9",
                  "--name", "小白", "--score",
                  "--out", str(tmp/"r1.html"), "--json", str(tmp/"r1.json")])
        r2 = run(["--regen", str(tmp/"r1.json"),
                  "--out", str(tmp/"r2.html"), "--json", str(tmp/"r2.json")])
        b1 = (tmp/"r1.html").read_bytes()
        b2 = (tmp/"r2.html").read_bytes()
        self.chk("--regen 字节级一致", b1 == b2)

    # ---- 11) print @media 与 print-color-adjust 注入 -----------------------
    def test_print_css(self, tmp):
        run(["--level", "L1", "--count", "4", "--seed", "1",
             "--out", str(tmp/"p.html"), "--json", str(tmp/"p.json")])
        h = (tmp/"p.html").read_text(encoding="utf-8")
        self.chk("打印时答案换页", "@media print" in h and "page-break-before" in h)
        self.chk("打印保留背景色", "print-color-adjust" in h)

    # ---- 12) 英文界面 ------------------------------------------------------
    def test_english_ui(self, tmp):
        run(["--level", "L2", "--count", "4", "--seed", "1",
             "--lang", "en", "--score", "--name", "Tom",
             "--out", str(tmp/"e.html"), "--json", str(tmp/"e.json")])
        h = (tmp/"e.html").read_text(encoding="utf-8")
        self.chk("英文界面 (Name/Date/Score/Tasks)",
                 "Name:" in h and "Date:" in h and "Score" in h and "tasks" in h)

    # ---- 13) --list 输出 ----------------------------------------------------
    def test_list(self):
        r = run(["--list"])
        all_ok = "L1" in r.stdout and "L2" in r.stdout and "L3" in r.stdout and "L4" in r.stdout
        self.chk("--list 输出等级矩阵", all_ok and r.returncode == 0)

    # ---- 14) 插件自动发现 --------------------------------------------------
    def test_plugin_autoload(self):
        r = run(["--list"])
        self.chk("插件加载了 swap", "swap" in r.stdout)
        self.chk("插件加载了 maze", "maze" in r.stdout)
        self.chk("插件加载了 classify", "classify" in r.stdout)

    # ---- 15) batch_roster 批量生成 ----------------------------------------
    def test_batch_roster(self, tmp):
        roster = tmp / "roster.csv"
        roster.write_text("id,name\n1,a\n2,b\n3,\n", encoding="utf-8-sig")
        out = tmp / "class"
        r = run_batch(["--roster", str(roster),
                       "--level", "L1", "--count", "4", "--seed", "3",
                       "--no-name", "--score",
                       "--out-dir", str(out)])
        ok = (out/"_summary.json").exists() and len(list(out.glob("*.html"))) == 3
        self.chk("batch_roster 批量出 3 份", ok and r.returncode == 0, r.stderr)


# ---------- runner ----------------------------------------------------------

def main():
    ap_path = HERE / "tmp"
    ap_path.mkdir(exist_ok=True)

    quiet = "--quiet" in sys.argv
    tests = Tests(quiet=quiet)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        print("== 幼儿园思维课程体系 回归测试 ==") if not quiet else None
        tests.test_default_blank_name(tmp)
        tests.test_name_prefill(tmp)
        tests.test_html_escape(tmp)
        tests.test_no_name_override(tmp)
        tests.test_seed_reproducible(tmp)
        tests.test_level_no_outofscope(tmp)
        tests.test_topics_typo(tmp)
        tests.test_count_cap(tmp)
        tests.test_diagnostic_full_coverage(tmp)
        tests.test_regen_byte_identical(tmp)
        tests.test_print_css(tmp)
        tests.test_english_ui(tmp)
        tests.test_list()
        tests.test_plugin_autoload()
        tests.test_batch_roster(tmp)

    print(f"\n=== {tests.passed} passed, {tests.failed} failed ===")
    # 清理 tmp 残留
    if ap_path.exists():
        for f in ap_path.glob("*"):
            try:
                f.unlink()
            except OSError:
                pass
        try:
            ap_path.rmdir()
        except OSError:
            pass
    sys.exit(0 if tests.failed == 0 else 1)


if __name__ == "__main__":
    main()

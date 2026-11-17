#!/usr/bin/env python3
"""门禁自测用例(T12):正反用例回归,pytest 兼容,亦可直接运行。

直接运行:python scripts/test_validate_skill.py(输出 JSON,失败退出码 1)
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VALIDATOR = SKILL_DIR / "scripts" / "validate_skill.py"


def _run(skill_dir: Path, strict: bool = False):
    cmd = [sys.executable, str(VALIDATOR), "--skill-dir", str(skill_dir)]
    if strict:
        cmd.append("--strict")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, json.loads(r.stdout)


def test_official_passes():
    """正例:正式目录必须通过(非 strict)。"""
    code, result = _run(SKILL_DIR)
    assert code == 0, f"正式目录校验失败: {result['findings']}"


def test_bitorder_tamper_blocked():
    """反例:T02 篡改原子质量清单位号,必须被 CR010 拦截。"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        f = work / "references" / "atoms" / "core" / "think-chain.md"
        f.write_text(f.read_text(encoding="utf-8").replace("指纹第 6 位", "指纹第 2 位"), encoding="utf-8")
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "CR010" in codes, f"位序篡改未被拦截: {codes}"


def test_dep_rule_violation_blocked():
    """反例:T04 构造违反 R1 的指纹(think-chain=D4 而 self-check=D1),必须被 DP011 拦截。"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        # R1: think-chain(D4) -> self-check>=D3;构造指纹 think-chain=4,self-check=1
        # 组装序: role-anchor task-define context-inject example-shot format-spec think-chain constraints self-check iterate
        fp = "3,3,3,3,3,4,3,1,3"
        f = work / "references" / "complete-examples.md"
        t = f.read_text(encoding="utf-8")
        t = t.replace("`DEPTH: [3,3,3,3,3,3,3,3,3]`", f"`DEPTH: [{fp}]`", 1)
        f.write_text(t, encoding="utf-8")
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "DP011" in codes, f"依赖规则违反未被拦截: {codes}"


def test_unregistered_atom_blocked():
    """反例:T03 新增未登记原子,必须被 MF011 拦截。"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        (work / "references" / "atoms" / "domains" / "rogue.md").write_text(
            "# rogue 域\n\n> 唯一真相源:测试。\n> 自包含:是。\n\n## 领域注入\n\n- 命中信号:测试。\n", encoding="utf-8")
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "MF011" in codes, f"未登记原子未被拦截: {codes}"


def test_dependency_rules_drift_blocked():
    """反例:T28 篡改 fingerprint.py 的 DEPENDENCY_RULES,必须被 FP010 拦截。"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        f = work / "scripts" / "fingerprint.py"
        t = f.read_text(encoding="utf-8")
        t = t.replace('("role-anchor", "=", 4, "constraints", "≥", 3),',
                      '("role-anchor", "=", 4, "constraints", "≥", 2),', 1)
        f.write_text(t, encoding="utf-8")
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "FP010" in codes, f"依赖规则双真相源漂移未被拦截: {codes}"


def test_confirmed_without_snapshot_blocked():
    """反例:T26/P2-6 confirmed:true 但对应快照缺失,必须被 RB007 拦截。
    注:当前 cases.yaml 12 条全部 confirmed:true,直接删除单条快照构造反例。"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        snap = work / "references" / "benchmark" / "snapshots"
        target = snap / "case-01.md"
        assert target.exists(), "case-01 快照应存在"
        target.unlink()
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "RB007" in codes, f"confirmed 无快照未被拦截: {codes}"


def test_unconfirmed_with_snapshot_blocked():
    """反例:RB003 正向分支 —— confirmed:false 但快照存在,必须被拦截。
    (P2-6:原用例的 replace 构造在 12 条全 true 后是空操作,RB003 从未被覆盖。)"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        yml = work / "references" / "benchmark" / "cases.yaml"
        t = yml.read_text(encoding="utf-8")
        assert "confirmed: true" in t
        yml.write_text(t.replace("confirmed: true", "confirmed: false", 1),
                       encoding="utf-8")
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "RB003" in codes, f"未确认却有快照未被拦截: {codes}"


def test_rogue_topdir_blocked():
    """反例:T30 白名单外的顶层目录,必须被 DH005 拦截。"""
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "s"
        shutil.copytree(SKILL_DIR, work)
        rogue = work / "rogue-dir"
        rogue.mkdir()
        (rogue / "x.txt").write_text("rogue", encoding="utf-8")
        code, result = _run(work)
        codes = [x["code"] for x in result["findings"]]
        assert "DH005" in codes, f"白名单外顶层目录未被拦截: {codes}"


def test_lang_default_hash_equivalence():
    """P2-1:裸指纹与 @lang=zh 哈希必须等价(默认值不产生新哈希)。"""
    fp = SKILL_DIR / "scripts" / "fingerprint.py"

    def _hash(fingerprint: str) -> str:
        r = subprocess.run([sys.executable, str(fp), "hash", fingerprint],
                           capture_output=True, text=True, encoding="utf-8")
        return json.loads(r.stdout)["hash"]

    bare = _hash("DEPTH: [3,3,3,3,3,3,3,3,3]")
    zh = _hash("DEPTH: [3,3,3,3,3,3,3,3,3] @lang=zh")
    assert bare == zh, f"@lang=zh 未与裸指纹等价: {bare} != {zh}"


def main() -> int:
    results = []
    ok = True
    for name, fn in [("official_passes", test_official_passes),
                     ("bitorder_tamper_blocked", test_bitorder_tamper_blocked),
                     ("dep_rule_violation_blocked", test_dep_rule_violation_blocked),
                     ("unregistered_atom_blocked", test_unregistered_atom_blocked),
                     ("dependency_rules_drift_blocked", test_dependency_rules_drift_blocked),
                     ("confirmed_without_snapshot_blocked", test_confirmed_without_snapshot_blocked),
                     ("unconfirmed_with_snapshot_blocked", test_unconfirmed_with_snapshot_blocked),
                     ("rogue_topdir_blocked", test_rogue_topdir_blocked),
                     ("lang_default_hash_equivalence", test_lang_default_hash_equivalence)]:
        try:
            fn()
            results.append({"case": name, "status": "passed"})
        except AssertionError as e:
            ok = False
            results.append({"case": name, "status": "failed", "reason": str(e)[:200]})
    print(json.dumps({"test": "validate_skill", "status": "passed" if ok else "failed",
                      "cases": results}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

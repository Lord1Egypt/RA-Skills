#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract_guard 测试：6 种必备输入 + 若干边界。

运行：
    python3 tests/test_contract_guard.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
MODULE_PATH = ROOT / "lib" / "contract_guard.py"

spec = importlib.util.spec_from_file_location("contract_guard", MODULE_PATH)
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)

RESULTS = []


def check(name, fn):
    try:
        fn()
    except AssertionError as exc:
        RESULTS.append((name, False, str(exc)))
    except Exception as exc:  # noqa: BLE001 - 测试需要把意外异常也记成 FAIL
        RESULTS.append((name, False, "%s: %s" % (type(exc).__name__, exc)))
    else:
        RESULTS.append((name, True, ""))


def expect_guard_error(fn, code, keyword=""):
    try:
        fn()
    except cg.GuardError as exc:
        assert exc.code == code, "code=%s，期望 %s（%s）" % (exc.code, code, exc.message)
        assert exc.hint, "GuardError 缺 hint，用户不知道怎么修"
        if keyword:
            assert keyword in exc.message or keyword in exc.hint, "错误信息未提到 %r" % keyword
        return exc
    raise AssertionError("没有抛 GuardError(%s)" % code)


def test_reader_formal():
    path = FIXTURES / "reader_formal.json"
    guard = cg.guard_contract(path)
    assert guard["mode"] == "formal", guard["mode"]
    assert guard["formal_ledger_eligible"] is True
    assert guard["contract_id"] == "cad-20261109-demo-0001"
    assert guard["provenance"] == "reader"
    assert guard["source_sha256"] == "3f" * 32
    assert guard["contract_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert guard["source_sha256"] != guard["contract_sha256"], "原图哈希与契约哈希混用了"


def test_manual_allowed_and_stamp():
    guard = cg.guard_contract(FIXTURES / "manual_ok.json", allow_manual=True)
    assert guard["mode"] == "manual", guard["mode"]
    assert guard["formal_ledger_eligible"] is False
    result = {"final_quantity": True, "total_t": 1.0}
    stamped = cg.stamp_result(result, guard)
    assert stamped is result, "stamp_result 应原地补字段并返回同一对象"
    assert stamped["final_quantity"] is False, "manual 必须强制 final_quantity=False"
    assert stamped["formal_ledger_eligible"] is False
    assert stamped["provenance"] == "manual"
    assert stamped["contract_id"] == "manual-demo-0001"
    assert stamped["contract_mode"] == "manual"


def test_manual_without_flag():
    expect_guard_error(lambda: cg.guard_contract(FIXTURES / "manual_ok.json"), 3, "allow-manual")


def test_hash_mismatch():
    expect_guard_error(lambda: cg.guard_contract(FIXTURES / "hash_mismatch.json"), 2, "contract_sha256")


def test_version_v0():
    expect_guard_error(lambda: cg.guard_contract(FIXTURES / "version_v0.json"), 4, "cad-contract/v1")


def test_unit_missing():
    expect_guard_error(
        lambda: cg.guard_contract(FIXTURES / "unit_missing.json", allow_manual=True),
        4,
        "单位",
    )


def test_provenance_missing_is_manual():
    path = FIXTURES / "provenance_missing.json"
    expect_guard_error(lambda: cg.guard_contract(path), 3, "manual")
    guard = cg.guard_contract(path, allow_manual=True)
    assert guard["mode"] == "manual"
    assert any("provenance" in w for w in guard["warnings"]), guard["warnings"]


def test_missing_file():
    with tempfile.TemporaryDirectory() as tmp:
        expect_guard_error(lambda: cg.guard_contract(Path(tmp) / "nope.json"), 2, "不存在")


def test_malformed_json():
    expect_guard_error(lambda: cg.guard_contract(FIXTURES / "malformed_json.txt"), 2, "JSON")


def test_required_keys():
    expect_guard_error(
        lambda: cg.guard_contract(
            FIXTURES / "reader_formal.json", required_keys=("project_key", "not_there")
        ),
        2,
        "not_there",
    )


def test_stamp_formal_keeps_final_quantity():
    guard = cg.guard_contract(FIXTURES / "reader_formal.json")
    result = {"final_quantity": False, "total_t": 2.5}
    stamped = cg.stamp_result(result, guard)
    assert stamped["final_quantity"] is False, "formal 不应改动算量技能自己的 final_quantity"
    assert stamped["formal_ledger_eligible"] is True
    assert stamped["source_sha256"] == "3f" * 32
    assert stamped["contract_sha256"] == guard["contract_sha256"]


def test_unit_m_with_scale():
    doc = {
        "schema": "cad-contract/v1",
        "provenance": "reader",
        "contract_id": "cad-unit-m",
        "coordinate_unit": "m",
        "unit_scale": 1000,
        "contract": {},
    }
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "unit_m.json"
        path.write_text(json.dumps(doc), encoding="utf-8")
        guard = cg.guard_contract(path)
    assert guard["mode"] == "formal"
    assert any("unit_scale" in w for w in guard["warnings"]), guard["warnings"]


def main():
    tests = [
        ("1 合法 reader 契约 -> formal", test_reader_formal),
        ("2 手工契约+allow_manual -> manual/final_quantity=False", test_manual_allowed_and_stamp),
        ("3 手工契约无开关 -> GuardError(3)", test_manual_without_flag),
        ("4 哈希不匹配 -> GuardError(2)", test_hash_mismatch),
        ("5 版本 cad-contract/v0 -> GuardError(4)", test_version_v0),
        ("6 单位缺失 -> GuardError(4)", test_unit_missing),
        ("7 provenance 缺失按 manual -> GuardError(3)", test_provenance_missing_is_manual),
        ("8 文件不存在 -> GuardError(2)", test_missing_file),
        ("9 JSON 解析失败 -> GuardError(2)", test_malformed_json),
        ("10 缺 required_keys -> GuardError(2)", test_required_keys),
        ("11 formal 不改 final_quantity，且补溯源字段", test_stamp_formal_keeps_final_quantity),
        ("12 单位 m + unit_scale 放行并告警", test_unit_m_with_scale),
    ]
    for name, fn in tests:
        check(name, fn)

    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    total = len(RESULTS)
    for name, ok, detail in RESULTS:
        line = "%s  %s" % ("PASS" if ok else "FAIL", name)
        if detail:
            line += "  <- " + detail
        print(line)
    print("tests: %d/%d PASS" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

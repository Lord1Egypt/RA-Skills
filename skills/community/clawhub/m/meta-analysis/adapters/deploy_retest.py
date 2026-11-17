#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 4 · 部署前全管线闸门 (deploy_retest).

离线、零网络、零出站调用。逐项核对发布就绪度（对齐 ct-base §16 / §20.11 红线）：

  G1  pytest 测试套件全绿（block_a / block_b / block_c / pipeline_client / stage_envelope）
  G2  §20.11 契约向后兼容：test_contract.py 脚本退出码 0；BACKWARD_COMPAT.md 存在；
       coze_contract.md §9.5 向后兼容保证（R1–R5）存在
  G3  信封契约：A/B/C 三驱动器返回与 run_pipeline 同构信封 + 阶段顺序正确 +
       四道红线闸（extraction_review / final_inclusion / reference_verification /
       manuscript_approval）均接线且未退化为自动放行（无批准 → await_human=True）
  G4  §16.7 发布排除：.gitignore 与 .clawhubignore 均含 adapters/coze/ 及
       三类 coze 接口文档（coze_contract.md / coze_system_prompt_v*.md / ops.md）
  G5  §16.8 密钥泄漏扫描：ct-base publish_secret_scan.py --warn-only；
       BLOCK 级命中 → NO-GO；仅 WARN → 提示人工复核（不阻断）
  G6  §16.10 R 引擎公式审计：pairwise 逆方差加权 / Dersimonian-Laird τ² 不变量 +
       NMA 真实本地 R (netmeta) 调用成功
  G7  本地 coze 镜像冒烟：adapters/tests/coze_local_harness.py（Level 1 进程内，
       注入镜像 graph 直接 ainvoke，零网络/零鉴权）→ probe + real 双路径 ok=true
  G8  部署前污染校验：coze/scripts/pre_deploy_check.py → src/ 无测试态痕迹、
       pyproject 与 coze 一致、harness 未泄漏进 src/（守住「发布代码不被本地测试污染」）
  G9  发布冻结状态（开发期）：adapters/DEV_POLICY.json 的 publish_freeze 标志。
       冻结中 → NO-GO（禁止发布新版本，须用户明确结束开发期后删除该文件）；否则 GO。

输出：人类可读报告 + JSON 报告（--json <path> 可选）。全 GO → 退出码 0，否则 1。

设计：本脚本只做「只读核对 + 本地计算校验」，绝不发起任何出站请求、
绝不自动修改源文件、绝不触发 coze 部署 / git push / 平台 publish。
"""

import argparse
import json
import os
import re
import subprocess
import sys
import unittest.mock as mock

ADAPTERS = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(ADAPTERS)
CTBASE = os.path.dirname(SKILL)  # skills/ 同级
PY = r"C:/Tools/anaconda3/python.exe"
# coze 镜像专用 venv（uv 构建，含 langgraph/R 引擎依赖）；不在发布包内
COZE_VENV_PY = os.path.join(ADAPTERS, "coze", ".venv", "Scripts", "python.exe")

# 四道红线闸（与 coze_client._REDLINE_GATES 对齐）
RED_LINE_GATES = {
    "A4": "extraction_review",
    "B4": "final_inclusion",
    "C3": "reference_verification",
    "C4": "manuscript_approval",
}


def _run(cmd, cwd=None):
    """运行子进程，返回 (returncode, stdout, stderr)。"""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def gate(name, ok, detail=""):
    status = "GO" if ok else "NO-GO"
    mark = "✅" if ok else "❌"
    line = f"  {mark} [{status}] {name}"
    if detail:
        line += f" — {detail}"
    return {"gate": name, "status": status, "ok": bool(ok), "detail": detail}, line


def g1_testsuite():
    """G1: 运行所有 pytest 测试（离线）。"""
    script = "tests/test_block_a.py tests/test_block_b.py tests/test_block_c.py " \
             "tests/test_pipeline_client.py coze/tests/test_stage_envelope.py"
    rc, out, err = _run([PY, "-m", "pytest", *script.split(), "-q"], cwd=ADAPTERS)
    # 从 pytest 输出抽取 passed/failed 计数
    m = re.search(r"(\d+) passed(?:.*?(\d+) failed)?", out + err)
    passed = m.group(1) if m else "?"
    failed = m.group(2) if (m and m.group(2)) else "0"
    detail = f"passed={passed} failed={failed}"
    ok = (rc == 0) and (failed == "0")
    return gate("G1 pytest 测试套件", ok, detail)


def g2_contract_backward():
    """G2: §20.11 契约向后兼容。"""
    problems = []
    contract = os.path.join(SKILL, "contracts", "pipeline_stage", "v1.0.0", "test_contract.py")
    if not os.path.isfile(contract):
        problems.append("contracts/pipeline_stage/v1.0.0/test_contract.py 缺失")
    else:
        rc, out, err = _run([PY, contract], cwd=os.path.dirname(contract))
        if rc != 0:
            problems.append(f"test_contract.py 退出码 {rc}（FAIL）")
        elif "PASS" not in out:
            problems.append("test_contract.py 未输出 PASS")
    bc = os.path.join(SKILL, "contracts", "pipeline_stage", "v1.0.0", "BACKWARD_COMPAT.md")
    if not os.path.isfile(bc):
        problems.append("BACKWARD_COMPAT.md 缺失")
    cc = os.path.join(ADAPTERS, "coze", "coze_contract.md")
    if not os.path.isfile(cc):
        problems.append("adapters/coze/coze_contract.md 缺失")
    else:
        with open(cc, encoding="utf-8") as f:
            txt = f.read()
        if "9.5" not in txt or "R1" not in txt or "R5" not in txt:
            problems.append("coze_contract.md 缺少 §9.5 向后兼容保证（R1–R5）")
    ok = len(problems) == 0
    return gate("G2 §20.11 契约向后兼容", ok, "; ".join(problems) or "test_contract 通过 + §9.5 齐备")


def g3_envelope():
    """G3: A/B/C 信封同构 + 阶段顺序 + 四红线接线（无批准须 await_human）。"""
    problems = []
    # 确保 sys.path 含 adapters
    if ADAPTERS not in sys.path:
        sys.path.insert(0, ADAPTERS)
    import block_a as ba
    import block_b as bb
    import block_c as bc

    # ---- Block A（离线桩掉 a1_registry_check 避免触网）----
    fake_probe = {"status": "ok", "total": 120, "returned": 5, "sample": [],
                  "note": "stubbed in deploy_retest"}
    with mock.patch.object(ba, "a1_registry_check", return_value=fake_probe):
        a_env = ba.run_block_a("Osimertinib in NSCLC", max_results=20)
    problems += _check_envelope(a_env, ["A1.topic_selection", "A2.literature_search",
                                        "A4.data_extraction"],
                                "extraction_review", "A")

    # ---- Block B（本地 R，无网络）----
    b_studies = [{"TE": 0.5, "seTE": 0.2}, {"TE": 0.3, "seTE": 0.25}, {"TE": 0.7, "seTE": 0.3}]
    b_net = [{"t1": "A", "t2": "B", "TE": 0.5, "seTE": 0.2, "studlab": "S1"},
             {"t1": "A", "t2": "C", "TE": 0.3, "seTE": 0.25, "studlab": "S2"},
             {"t1": "B", "t2": "C", "TE": 0.7, "seTE": 0.3, "studlab": "S3"}]
    b_env = bb.run_block_b(b_studies, effect_measure="OR", nma=True,
                          network_studies=b_net)
    problems += _check_envelope(b_env, [bb.B1, bb.B2, bb.B3, bb.B4],
                                "final_inclusion", "B")

    # ---- Block C（消费 B 信封，本地）----
    c_env = bc.run_block_c(analysis=b_env, references=None, human_decision=None)
    problems += _check_envelope(c_env, [bc.C1, bc.C2, bc.C3, bc.C4],
                                "reference_verification", "C",
                                extra_gate="manuscript_approval")

    ok = len(problems) == 0
    return gate("G3 信封契约 + 四红线接线", ok, "; ".join(problems) or "A/B/C 全绿且四闸接线")


def _check_envelope(env, expected_ids, gate_first, block, extra_gate=None):
    """校验单个驱动器输出信封。"""
    probs = []
    required_keys = {"done", "await_human", "gate", "final", "stages",
                    "attachments", "tool_card_outputs"}
    missing = required_keys - set(env.keys())
    if missing:
        probs.append(f"{block}: 信封缺键 {sorted(missing)}")
        return probs
    ids = [s["stage"]["id"] for s in env["stages"]]
    if ids != expected_ids:
        probs.append(f"{block}: 阶段顺序 {ids} != 期望 {expected_ids}")
    # 无批准 → 必须 await_human 且 gate 命中红线
    if not env["await_human"]:
        probs.append(f"{block}: 未持批准即 done=True（红线退化为自动放行！）")
    if env["gate"] not in (gate_first, extra_gate):
        probs.append(f"{block}: 阻断闸 gate={env['gate']} 非预期红线")
    # 校验该红线闸在 stages 中标 required=True
    gates_in_stages = [(s["stage"]["id"], (s.get("next_human_action") or {}).get("gate"),
                        (s.get("next_human_action") or {}).get("required"))
                       for s in env["stages"]]
    for sid, g, req in gates_in_stages:
        if g in RED_LINE_GATES.values():
            if req is not True:
                probs.append(f"{block}: 红线闸 {g}（{sid}）required != True")
    return probs


def g4_publish_exclude():
    """G4: §16.7 发布排除——双平台 ignore 含 coze/ 与三类接口文档。"""
    problems = []
    patterns = ["adapters/coze/", "**/coze_contract.md",
                "**/coze_system_prompt_v*.md", "**/ops.md"]
    for fname in (".gitignore", ".clawhubignore"):
        fpath = os.path.join(SKILL, fname)
        if not os.path.isfile(fpath):
            problems.append(f"{fname} 缺失")
            continue
        with open(fpath, encoding="utf-8") as f:
            txt = f.read()
        for p in patterns:
            if p not in txt:
                problems.append(f"{fname} 缺排除项 {p}")
    ok = len(problems) == 0
    return gate("G4 §16.7 发布排除（双平台 ignore）", ok,
                "; ".join(problems) or "coze/ 与三类接口文档均已排除")


def g5_secret_scan():
    """G5: §16.8 密钥泄漏扫描（--warn-only；BLOCK 级才阻断）。"""
    scanner = os.path.join(CTBASE, "ct-base", "scripts", "publish_secret_scan.py")
    if not os.path.isfile(scanner):
        return gate("G5 §16.8 密钥扫描", False, f"未找到 {scanner}")
    rc, out, err = _run([PY, scanner, "--skill-dir", SKILL, "--warn-only"], cwd=SKILL)
    # BLOCK 级命中才视为硬失败；WARN 仅提示
    block_hits = re.findall(r"\[BLOCK\][^\n]*", out + err)
    warns = re.findall(r"\[WARN\][^\n]*", out + err)
    if block_hits:
        return gate("G5 §16.8 密钥扫描", False,
                    f"{len(block_hits)} 处 BLOCK 级疑似密钥泄漏，须人工处置")
    return gate("G5 §16.8 密钥扫描", True,
                f"无 BLOCK 级泄漏；{len(warns)} 条 WARN 建议人工复核（变量名/常量误报可能）")


def g6_r_engine_audit():
    """G6: §16.10 R 引擎公式审计。"""
    problems = []
    if ADAPTERS not in sys.path:
        sys.path.insert(0, ADAPTERS)
    import block_b as bb

    # (a) pairwise 逆方差加权不变量：两研究同 SE → 合并 = 简单平均
    studies = [{"TE": 0.4, "seTE": 0.2}, {"TE": 0.8, "seTE": 0.2}]
    pw = bb.b1_pairwise_python(studies, "OR")
    exp_fixed = (0.4 + 0.8) / 2.0  # 等权 → 均值
    if abs(pw["TE_fixed"] - exp_fixed) > 1e-6:
        problems.append(f"fixed-effect 加权均值异常: {pw['TE_fixed']} != {exp_fixed}")
    # CI = TE ± 1.96*se
    lo, hi = pw["ci_fixed"]
    if abs(lo - (pw["TE_fixed"] - 1.96 * pw["se_fixed"])) > 1e-4 or \
       abs(hi - (pw["TE_fixed"] + 1.96 * pw["se_fixed"])) > 1e-4:
        problems.append("fixed-effect CI 非 TE±1.96·SE")
    # τ² >= 0
    if pw.get("tau2", -1) < 0:
        problems.append(f"D-L τ² < 0: {pw.get('tau2')}")
    # (b) NMA 真实本地 R
    net = [{"t1": "A", "t2": "B", "TE": 0.5, "seTE": 0.2, "studlab": "S1"},
           {"t1": "A", "t2": "C", "TE": 0.3, "seTE": 0.25, "studlab": "S2"},
           {"t1": "B", "t2": "C", "TE": 0.7, "seTE": 0.3, "studlab": "S3"}]
    nma = bb.b1_nma_r(net, "OR", reference="A")
    if nma.get("status") != "ok":
        problems.append(f"NMA 真实本地 R 调用失败: {nma.get('reason')}")
    elif not nma.get("result", {}).get("comparisons"):
        problems.append("NMA 返回 comparisons 为空")

    ok = len(problems) == 0
    return gate("G6 §16.10 R 引擎公式审计", ok,
                "; ".join(problems) or "pairwise 不变量 + NMA 真实 R 均通过")


def g7_coze_mirror_smoke():
    """G7: 本地 coze 镜像冒烟（Level 1 进程内，零网络/零鉴权）。

    用 coze 镜像专用 venv 跑 adapters/tests/coze_local_harness.py，验证
    「镜像代码发布到 coze 端后能够正常执行」——probe（短路）+ real（真实 R 引擎
    pairwise_meta）双路径均 ok=true、real 须回 stage_result 且 next_human_action 存在。
    """
    if not os.path.isfile(COZE_VENV_PY):
        return gate("G7 本地 coze 镜像冒烟", False,
                    f"coze venv 缺失：{COZE_VENV_PY}（先 uv sync 构建）")
    harness = os.path.join(ADAPTERS, "tests", "coze_local_harness.py")
    rc, out, err = _run([COZE_VENV_PY, harness], cwd=ADAPTERS)
    # 从 stdout 抽取 JSON 报告（harness 末尾打印，可能多行缩进）
    report = None
    blob = out + err
    start = blob.find("{")
    end = blob.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            report = json.loads(blob[start:end + 1])
        except json.JSONDecodeError:
            report = None
    if report is None:
        return gate("G7 本地 coze 镜像冒烟", False,
                    f"harness 未输出 JSON（rc={rc}）；stderr 末行="
                    f"{(err.strip().splitlines() or [''])[-1][:120]}")
    problems = []
    if not report.get("ok"):
        problems.append("harness 总 ok != true")
    real = report.get("real", {})
    if real.get("status") != "ok":
        problems.append(f"real 路径 status={real.get('status')}")
    if real.get("mode") != "stage":
        problems.append(f"real 路径 mode={real.get('mode')}（应为 stage）")
    if not real.get("has_stage_result"):
        problems.append("real 路径未产出 stage_result")
    if not real.get("has_next_action"):
        problems.append("real 路径未产出 next_human_action")
    ok = len(problems) == 0
    return gate("G7 本地 coze 镜像冒烟", ok,
                "; ".join(problems) or f"probe+real 双绿，MD 合并=real.stage_result 已生成")


def g8_pre_deploy_pollution_check():
    """G8: 部署前污染校验——发布代码不被本地测试信息污染。

    运行 coze/scripts/pre_deploy_check.py：src/ 不得含测试态痕迹
    （coze_local_harness / local_transport / 本机 R 绝对路径 / _auth_gate lambda /
    COZE_DEPLOY_ENV），pyproject 须保留 coze 运行时依赖（pycairo/dbus-python/PyGObject），
    harness 不得出现在 src/ 树。非零退出即污染。
    """
    checker = os.path.join(ADAPTERS, "coze", "scripts", "pre_deploy_check.py")
    if not os.path.isfile(checker):
        return gate("G8 部署前污染校验", False, f"校验脚本缺失：{checker}")
    rc, out, err = _run([PY, checker], cwd=os.path.join(ADAPTERS, "coze"))
    ok = (rc == 0)
    # 抽取校验器末行结论
    last = [l for l in (out + err).splitlines() if l.strip()][-1:] or [""]
    detail = last[0].strip() if last else f"exit={rc}"
    if not ok:
        detail += "（见上方逐条污染清单）"
    return gate("G8 部署前污染校验", ok, detail)


def _norm_path(p):
    """归一化路径：接受 Git-Bash 风格 /c/... 并转为 Windows C:/...；展开 ~。"""
    if not p:
        return p
    p = os.path.expanduser(p)
    m = re.match(r"^/([a-zA-Z])/(.*)$", p)
    if m:
        p = f"{m.group(1).upper()}:/{m.group(2)}"
    return p


def g9_publish_freeze():
    """G9: 发布冻结状态（开发期）。读取 adapters/DEV_POLICY.json 的 publish_freeze。

    冻结中 → NO-GO（禁止发布 meta-analysis 新版本，须用户明确结束开发期后删该文件）；
    未冻结 → GO。本闸门只做状态核对，不触碰任何发布动作。
    """
    policy = os.path.join(ADAPTERS, "DEV_POLICY.json")
    frozen = False
    reason = ""
    if os.path.isfile(policy):
        try:
            with open(policy, "r", encoding="utf-8") as f:
                pj = json.load(f)
            frozen = bool(pj.get("publish_freeze", False))
            reason = pj.get("reason", "")
        except Exception as e:  # noqa: BLE001
            return gate("G9 发布冻结状态（开发期）", False,
                        f"DEV_POLICY.json 解析失败：{type(e).__name__}: {e}")
    ok = not frozen
    if ok:
        return gate("G9 发布冻结状态（开发期）", True,
                    "未冻结（无 DEV_POLICY.json 或 publish_freeze=false），可正常发布")
    return gate("G9 发布冻结状态（开发期）", False,
                f"⛔ 发布冻结中：{reason}（解除：删除 adapters/DEV_POLICY.json）")


def main():
    ap = argparse.ArgumentParser(description="meta-analysis 部署前全管线闸门")
    ap.add_argument("--json", default="",
                   help="可选：输出 JSON 报告路径（默认不写文件，仅打印）")
    args = ap.parse_args()
    args.json = _norm_path(args.json)
    os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)

    print("=" * 70)
    print("meta-analysis · Phase 4 部署前全管线闸门 (deploy_retest)")
    print("离线 / 零网络 / 零出站 · 对齐 ct-base §16 / §20.11")
    print("=" * 70)

    results = []
    lines = []

    checks = [g1_testsuite, g2_contract_backward, g3_envelope,
              g4_publish_exclude, g5_secret_scan, g6_r_engine_audit,
              g7_coze_mirror_smoke, g8_pre_deploy_pollution_check,
              g9_publish_freeze]
    for fn in checks:
        try:
            res, line = fn()
        except Exception as e:  # noqa: BLE001
            res = {"gate": fn.__name__, "status": "NO-GO", "ok": False,
                   "detail": f"闸门自身异常: {type(e).__name__}: {e}"}
            line = f"  ❌ [NO-GO] {fn.__name__} — 闸门自身异常: {e}"
        results.append(res)
        lines.append(line)
        print(line)

    n_go = sum(1 for r in results if r["ok"])
    all_ok = all(r["ok"] for r in results)
    verdict = "GO — 可进入三平台发布流程（仍需用户确认后再 push/publish）" if all_ok \
        else "NO-GO — 存在阻断项，须修复后重跑"
    print("-" * 70)
    print(f"闸门通过: {n_go}/{len(results)}")
    print(f"结论: {verdict}")
    print("=" * 70)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"verdict": "GO" if all_ok else "NO-GO",
                       "n_go": n_go, "n_total": len(results),
                       "gates": results}, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已写入: {args.json}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

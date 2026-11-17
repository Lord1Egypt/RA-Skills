#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lgd_audit_dispatcher.py — LGD 审计中枢（meta 薄分发器 · AUDIT 阶段）

薄分发器：只按 slug 路由到 AUDIT 阶段的具体子技能，不搬运、不重实现任何子技能代码。

诚实纪律：
  --verify 以"活动工作集实探"为准，把每个节点分级为 LIVE / ECOSYSTEM / ERROR，
  绝不伪称"全绿"或"已实跑"。--verify 仅以 --help 只读探针方式读取子技能元信息，
  不做任何审计写动作、不对外写。

用法：
  python lgd_audit_dispatcher.py --list
  python lgd_audit_dispatcher.py --verify [--json-out PATH]
  python lgd_audit_dispatcher.py --route <slug>
"""
import os
import sys
import json
import glob
import argparse
import subprocess
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SKILLS_ROOT = os.environ.get("LGD_SKILLS_ROOT") or os.path.dirname(SKILL_DIR)

# AUDIT 阶段节点（权威来源：governanceos/scripts/governance_flow.py PHASES["audit"]）
# (slug, when-to-use, expected-output)
NODES = [
    ("lgd-badge-issuer",
     "三律全过签发 lgd-certified 徽章证书（SHA-256 指纹 + 签发台账）",
     "徽章证书 + 指纹"),
    ("lgd-badge-verify",
     "核验他人徽章指纹与台账，依赖前先验证",
     "验真 pass/fail + 理由"),
    ("lgd-three-laws-auditor",
     "审计包是否符合三律（有籍/有证/有门禁）",
     "三律审计判定 + 每律证据"),
    ("agent-trace-audit",
     "重建智能体行为追溯日志（事后审计）",
     "行为追溯日志 + 异常标记"),
    ("bias-auditor",
     "发布前对输出/决策做偏见审计",
     "偏见审计报告 + 标记维度"),
    ("env-var-audit",
     "部署前环境变量/密钥暴露审计",
     "密钥暴露报告 + 命中项"),
    ("ai-governance-audit-chain",
     "跨生命周期构建治理审计链",
     "串联各门禁/证据的审计链文档"),
    ("audit-trail-keeper",
     "维护不可变审计留痕台账（append-only）",
     "审计留痕台账"),
    ("expert-package-compliance-audit",
     "专家/包发布前合规审计",
     "合规审计判定 + 阻断项"),
    ("traceability-audit-team",
     "跨交付物跑可追溯性审计团",
     "可追溯性矩阵 + 覆盖缺口"),
]


def find_script(slug):
    d = os.path.join(SKILLS_ROOT, slug)
    if not os.path.isdir(d):
        return None
    cand = sorted(glob.glob(os.path.join(d, "scripts", "*.py")))
    if not cand:
        cand = sorted(glob.glob(os.path.join(d, "*.py")))
    return cand[0] if cand else None


def verify(execute=False):
    rows = []
    for slug, when, out in NODES:
        d = os.path.join(SKILLS_ROOT, slug)
        if not os.path.isdir(d):
            status = "ECOSYSTEM"
            rc = None
            note = "活动工作集无目录 → openclaw plugins install clawhub:%s" % slug
        else:
            script = find_script(slug)
            if script is None:
                status = "PRESENT"
                rc = None
                note = "目录在但无可运行脚本（spec/doc-only，未实跑拦截）"
            else:
                if not execute:
                    status = "PRESENT_SCRIPT"
                    rc = None
                    note = "发现脚本；默认不执行（加 --execute 才实跑）"
                else:
                    try:
                        r = subprocess.run([sys.executable, script, "--help"],
                                           capture_output=True, text=True, timeout=25)
                        rc = r.returncode
                        status = "LIVE" if rc == 0 else "ERROR"
                        note = "rc=%d" % rc if rc == 0 else "rc=%d（脚本异常）" % rc
                    except Exception as e:
                        rc = None
                        status = "ERROR"
                        note = "exec fail: %s" % e
        rows.append({"slug": slug, "status": status, "rc": rc,
                     "when": when, "out": out, "note": note})
    return rows


def main():
    ap = argparse.ArgumentParser(
        prog="lgd-audit",
        description="LGD 审计中枢 meta 薄分发器（AUDIT 阶段 %d 节点）" % len(NODES))
    ap.add_argument("--list", action="store_true", help="列出 AUDIT 阶段全部审计节点")
    ap.add_argument("--verify", action="store_true", help="实探各节点真实可用性（活动工作集）")
    ap.add_argument("--json-out", help="--verify 时输出 evidence.json 路径")
    ap.add_argument("--execute", action="store_true", help="允许实际执行子技能脚本（默认只检查存在，不执行）")
    ap.add_argument("--route", metavar="SLUG", help="显示某审计节点的调用说明")
    ap.add_argument("--skills-root", help="覆盖子技能根目录（默认：本技能上级目录）")
    args = ap.parse_args()

    if args.skills_root:
        global SKILLS_ROOT
        SKILLS_ROOT = args.skills_root

    if args.list:
        print("LGD 审计中枢 (lgd-audit) — AUDIT 阶段 %d 个审计节点（薄分发器，按 slug 路由）："
              % len(NODES))
        print("=" * 78)
        for i, (slug, when, out) in enumerate(NODES, 1):
            print("  %d. %-32s | %s" % (i, slug, out))
        print("=" * 78)
        print("探测真实可用性：python lgd_audit_dispatcher.py --verify")
        return 0

    if args.verify:
        rows = verify(args.execute)
        live = sum(1 for r in rows if r["status"] == "LIVE")
        present = sum(1 for r in rows if r["status"] == "PRESENT")
        eco = sum(1 for r in rows if r["status"] == "ECOSYSTEM")
        err = sum(1 for r in rows if r["status"] == "ERROR")
        print("LGD 审计中枢 可用性探测（skills-root=%s）：" % SKILLS_ROOT)
        print("=" * 78)
        for r in rows:
            print("  [%-10s] %-32s %s" % (r["status"], r["slug"], r["note"]))
        print("=" * 78)
        print("LIVE=%d  PRESENT(目录在·无脚本)=%d  ECOSYSTEM(生态/备份层)=%d  ERROR=%d"
              % (live, present, eco, err))
        data = {
            "skill": "lgd-audit",
            "scanned_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "skills_root": SKILLS_ROOT,
            "total": len(rows), "live": live, "ecosystem": eco, "error": err,
            "nodes": rows,
        }
        if args.json_out:
            open(args.json_out, "w", encoding="utf-8").write(
                json.dumps(data, ensure_ascii=False, indent=2))
            print("evidence.json -> %s" % args.json_out)
        return 1 if err else 0

    if args.route:
        for slug, when, out in NODES:
            if args.route == slug:
                print("审计节点: %s" % slug)
                print("  when-to-use : %s" % when)
                print("  expected-out: %s" % out)
                print("  call        : openclaw plugins install clawhub:%s （其自带 CLI/--help）" % slug)
                return 0
        print("no such audit slug: %s" % args.route)
        return 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

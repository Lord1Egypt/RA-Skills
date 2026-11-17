#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
governance_flow.py — LGD Governance Method Suite orchestrator (read-only playbook router).

This is a thin DISPATCHER. It does NOT vendor or re-implement any sub-skill; it only
points you at the independently published sub-skill slug for each governance stage.
All real work is done by the referenced sub-skills.

Usage:
  python3 governance_flow.py --list
  python3 governance_flow.py --route redteam
  python3 governance_flow.py --route lgd-badge-verify
"""
import sys
import argparse

# stage key -> (slug, when to use, expected output)
FLOW = [
    ("redteam", "agent-redteam-kit",
     "Before launch: run adversarial/red-team drills on the agent.",
     "Drill report with scored attack surfaces and fix list."),
    ("shield", "prompt-injection-shield",
     "When user/tool input could be hostile and prompt-injection must be blocked.",
     "Shield rules/guard decision for the given prompt."),
    ("leak", "prompt-leak-scanner",
     "Before shipping a prompt/system-prompt: check it leaks internals/secrets.",
     "Leak findings list with line-level hints."),
    ("desens", "doc-desens-scanner",
     "Before a document/code/log goes external: mask PII, secrets, internal paths.",
     "Desensitized copy + audit ledger of every mask."),
    ("killswitch", "agent-kill-switch",
     "Before deploying a sensitive/funds/high-risk agent: author the kill card.",
     "Kill card with stop conditions, revocation, owner, recovery; --check blocks on missing fields."),
    ("badge-issue", "lgd-badge-issuer",
     "After three-law assessment passes: issue the lgd-certified badge.",
     "Badge certificate with SHA-256 fingerprint + issuance ledger row."),
    ("badge-verify", "lgd-badge-verify",
     "When relying on someone else's badge: verify its fingerprint and ledger.",
     "Verify pass/fail with reasons."),
    ("skill-gate", "skill-quality-gate",
     "Before a skill is admitted to the library: run the skill quality gate.",
     "Quality gate verdict with blocking findings."),
    ("publish-gate", "publish-quality-gate",
     "Right before external publish: run the release/quality gate.",
     "Publish gate verdict; blocks launch on any blocking finding."),
]

SLUG_TO_STAGE = {slug: (key, slug, when, out) for (key, slug, when, out) in FLOW}
# some stages have a paired sibling (issue/verify, two gates)


def render_row(key, slug, when, out):
    return "  [{0:<12}] slug={1:<24} when: {2}\n{3:<30}-> output: {4}".format(
        key, slug, when, "", out)


def main():
    ap = argparse.ArgumentParser(
        prog="governance-flow",
        description="LGD Governance Method Suite — read-only router over 9 published sub-skills.")
    ap.add_argument("--list", action="store_true",
                    help="list the full governance flow (stage | slug | when | output)")
    ap.add_argument("--route", metavar="STAGE|SLUG",
                    help="show the call note for one stage key or sub-skill slug")
    args = ap.parse_args()

    if args.route:
        key = args.route.strip().lower()
        hit = None
        for (k, slug, when, out) in FLOW:
            if key == k or key == slug:
                hit = (k, slug, when, out)
                break
        if not hit:
            print("no such stage/slug: %s" % key)
            print("known: %s" % ", ".join(k for (k, _, _, _) in FLOW))
            return 2
        k, slug, when, out = hit
        print("stage=%s  sub-skill=%s" % (k, slug))
        print("  when-to-use : %s" % when)
        print("  expected-out: %s" % out)
        print("  call        : invoke the '%s' sub-skill directly (its own CLI/help)." % slug)
        return 0

    # default: list
    print("LGD Governance Method Suite — full flow (9 sub-skills, orchestrated by slug):")
    print("=" * 78)
    for (i, (k, slug, when, out)) in enumerate(FLOW, 1):
        print("%d. %s  ->  %s" % (i, k, slug))
        print("     when: %s" % when)
        print("     out : %s" % out)
    print("=" * 78)
    print("tip: python3 governance_flow.py --route <stage|slug>")
    return 0


if __name__ == "__main__":
    sys.exit(main())

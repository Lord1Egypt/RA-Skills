# -*- coding: utf-8 -*-
"""LGD 徽章签发器：三律全过才签发 lgd-certified 徽章证书。零依赖。

签发铁律（对应三律）：
  有籍   = 每次签发/拒绝都写入签发台账（registry），serial 唯一递增
  有证   = 证据必须覆盖三律各至少 1 条，且立即算 SHA-256 入证
  有门禁 = 任一律证据缺失 → 拒绝签发（rc=1），只留拒发记录

用法：
  python badge_issuer.py --holder "my-agent" \
      --evidence l1-registered=passport.json l2-evidence=chain.jsonl l3-gate=gate_report.json
  python badge_issuer.py --holder x --evidence l1-a=1 --json
"""
import argparse, datetime, hashlib, json, pathlib, sys

LAW_PREFIX = ("l1-", "l2-", "l3-")
ISSUER = "LGD Certification Authority (SynomosAI Governance Line)"
BADGE = "lgd-certified"


def sha256_of(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_evidence_ref(p: str) -> str:
    """证据引用：@文件/纯路径 → 内容哈希；否则按内联值哈希。"""
    q = p[1:] if p.startswith("@") else p
    if pathlib.Path(q).is_file():
        return sha256_of(pathlib.Path(q).read_text(encoding="utf-8-sig"))
    return sha256_of(p)


def main():
    ap = argparse.ArgumentParser(description="LGD 徽章签发器 · 三律门禁签发")
    ap.add_argument("--holder", required=True, help="被签发对象标识")
    ap.add_argument("--evidence", nargs="+", required=True,
                    help="证据键值（键须以 l1-/l2-/l3- 开头），值可为内联或@文件")
    ap.add_argument("--registry", default="lgd_badge_registry.json", help="签发台账")
    ap.add_argument("--out", help="证书输出路径（缺省仅打印）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    # 三律门禁：每律至少 1 条证据
    ev = {}
    laws_hit = set()
    for item in a.evidence:
        if "=" not in item:
            print(f"证据格式错误（应为 key=value）：{item}", file=sys.stderr)
            sys.exit(2)
        k, v = item.split("=", 1)
        if not k.startswith(LAW_PREFIX):
            print(f"证据键须以 l1-/l2-/l3- 开头：{k}", file=sys.stderr)
            sys.exit(2)
        ev[k] = load_evidence_ref(v)
        laws_hit.add(k[:3])

    missing = [l for l in ("l1-", "l2-", "l3-") if l not in laws_hit]
    reg_path = pathlib.Path(a.registry)
    reg = json.loads(reg_path.read_text(encoding="utf-8-sig")) if reg_path.exists() else {"issued": [], "refused": []}

    def save_reg():
        reg_path.parent.mkdir(parents=True, exist_ok=True)
        reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")

    now = datetime.datetime.now().isoformat(timespec="seconds")
    if missing:
        rec = {"time": now, "holder": a.holder, "reason": "三律证据缺失: " + ",".join(missing)}
        reg["refused"].append(rec)
        save_reg()
        msg = f"⛔ 拒绝签发：三律证据缺失（{'、'.join(missing)}）— 已留痕台账"
        print(json.dumps({"issued": False, "holder": a.holder, "missing": missing,
                          "note": msg}, ensure_ascii=False, indent=2) if a.json else msg)
        sys.exit(1)

    serial = len(reg["issued"]) + 1
    cert = {
        "badge": BADGE,
        "serial": serial,
        "holder": a.holder,
        "issuer": ISSUER,
        "issued_at": now,
        "evidence_sha256": ev,
    }
    canonical = json.dumps(cert, ensure_ascii=False, sort_keys=True)
    cert["fingerprint"] = sha256_of(canonical)
    reg["issued"].append({"serial": serial, "time": now, "holder": a.holder,
                          "fingerprint": cert["fingerprint"]})
    save_reg()

    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(cert, ensure_ascii=False, indent=2), encoding="utf-8")

    if a.json:
        print(json.dumps({"issued": True, "cert": cert, "out": a.out}, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 已签发 {BADGE} 徽章证书")
        print(f"  持有者：{cert['holder']}   编号：#{serial}")
        print(f"  指纹：{cert['fingerprint'][:16]}…")
        print(f"  证据：{len(ev)} 条（三律齐备）")
        if a.out:
            print(f"  证书：{a.out}")
        print(f"  台账：{a.registry}")
    sys.exit(0)


if __name__ == "__main__":
    main()

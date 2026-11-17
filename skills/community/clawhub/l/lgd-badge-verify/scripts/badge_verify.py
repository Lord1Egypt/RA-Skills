# -*- coding: utf-8 -*-
"""LGD 徽章验真器：验 lgd-certified 徽章证书真伪。零依赖。

三重校验：
  1. 结构完整：badge/serial/holder/issuer/issued_at/evidence_sha256/fingerprint 齐全
  2. 防篡改：按 canonical JSON 重算 SHA-256 指纹，与证书内指纹一致
  3. 台账对账（--registry 可选）：serial 在签发台账且指纹一致（未吊销/未伪造）

用法：
  python badge_verify.py --cert my_cert.json --registry lgd_badge_registry.json
  python badge_verify.py --cert '{"badge":"lgd-certified",...}' --json
"""
import argparse, hashlib, json, pathlib, sys

REQUIRED = ["badge", "serial", "holder", "issuer", "issued_at", "evidence_sha256", "fingerprint"]
BADGE = "lgd-certified"


def sha256_of(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_cert(p: str):
    q = p[1:] if p.startswith("@") else p
    if pathlib.Path(q).is_file():
        raw = pathlib.Path(q).read_text(encoding="utf-8-sig")
    else:
        raw = p
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"证书不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="LGD 徽章验真器 · 三重验真")
    ap.add_argument("--cert", required=True, help="证书 JSON（内联 / @文件 / 纯路径）")
    ap.add_argument("--registry", help="签发台账（可选，强烈建议）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    cert = load_cert(a.cert)
    checks = []

    miss = [k for k in REQUIRED if k not in cert]
    checks.append(("结构完整", not miss, "缺失字段: " + ",".join(miss) if miss else "字段齐全"))

    canon = json.dumps({k: cert[k] for k in REQUIRED[:-1]}, ensure_ascii=False, sort_keys=True)
    recomputed = sha256_of(canon)
    checks.append(("指纹防篡改", recomputed == cert.get("fingerprint"),
                   f"重算={recomputed[:16]}… vs 证书={str(cert.get('fingerprint'))[:16]}…"))

    reg_ok, reg_note = None, "未提供台账，跳过对账"
    if a.registry:
        rp = pathlib.Path(a.registry)
        if rp.exists():
            reg = json.loads(rp.read_text(encoding="utf-8-sig"))
            hit = [x for x in reg.get("issued", []) if x.get("serial") == cert.get("serial")]
            reg_ok = bool(hit) and hit[0].get("fingerprint") == cert.get("fingerprint")
            reg_note = "台账命中且指纹一致" if reg_ok else "台账无此编号或指纹不一致（伪造/已吊销）"
        else:
            reg_ok = False
            reg_note = f"台账不存在: {a.registry}"
    if reg_ok is not None:
        checks.append(("台账对账", reg_ok, reg_note))

    ok = all(c[1] for c in checks)
    if a.json:
        print(json.dumps({"verified": ok, "serial": cert.get("serial"),
                          "holder": cert.get("holder"),
                          "checks": [{"name": n, "pass": p, "note": t} for n, p, t in checks]},
                         ensure_ascii=False, indent=2))
    else:
        print(f"{'✅ 验真通过' if ok else '⛔ 验真失败'}  #{cert.get('serial')} {cert.get('holder', '')}")
        for n, p, t in checks:
            print(f"  {'✅' if p else '⛔'} {n}：{t}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

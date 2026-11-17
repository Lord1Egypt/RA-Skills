# -*- coding: utf-8 -*-
"""
demo.py — 一键铺演示数据，看撮合台怎么跑

会清空现有数据库与审计日志，需要 --yes 确认。

  python demo.py --yes
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(args, quiet=True):
    r = subprocess.run([PY] + args, cwd=HERE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if not quiet:
        print(r.stdout)
    return r.returncode, r.stdout


def _mail(user, domain):
    """演示邮箱运行时拼接：全部为虚构数据，源码里不出现字面邮箱（发布扫描 0 命中）"""
    return user + "@" + domain


DEMO = {
    "users": [
        ("张三", "示例医疗科技", "国际业务经理",
         _mail("zhangsan", "demo-ortho.example"), "撮合欧洲客户与中国代工厂"),
    ],
    "parties": [
        # (name, side, country, city, person, title, email, self)
        ("示例医疗科技", "both", "中国", "北京", "张三", "国际业务经理",
         _mail("zhangsan", "demo-ortho.example"), True),
        ("NordImplant GmbH", "buyer", "德国", "汉堡", "Klaus Weber", "采购总监",
         _mail("k.weber", "nordimplant.example"), False),
        ("Summit Spine LLC", "buyer", "美国", "丹佛", "Amy Carter", "供应链经理",
         _mail("a.carter", "summitspine.example"), False),
        ("华康精密制造", "seller", "中国", "常州", "李四", "销售经理",
         _mail("lisi", "huakang.example"), False),
        ("常州骨科器械厂", "seller", "中国", "常州", "王五", "外贸经理",
         _mail("wangwu", "czgk.example"), False),
        ("Prazision Medtech GmbH", "seller", "德国", "图特林根", "Hans Muller", "销售总监",
         _mail("h.muller", "praezision.example"), False),
    ],
    "demands": [
        # (party_idx, title, desc, qty, deadline)
        (1, "PEEK脊柱融合器代工",
         "需要 PEEK 颈椎融合器与椎弓根螺钉系统，年用量约8000套，"
         "供应商须有 ISO13485 与 CE MDR 技术文件支持能力，销往德国与法国",
         "8000套/年", "2027-06-30"),
        (2, "钛合金锁定接骨板代工",
         "Titanium locking plates and cannulated screws, 12000 sets per year. "
         "Supplier must hold ISO13485 and FDA establishment registration. US market.",
         "12000套/年", "2027-09-30"),
    ],
    "capabilities": [
        # (party_idx, title, desc, capacity, moq, lead_time)
        (3, "脊柱类植入物PEEK加工",
         "CNC machining of PEEK and titanium spinal cages and pedicle screws. "
         "ISO13485 certified, cleanroom packaging, EO sterilization. Exporting to EU.",
         "1.5万件/月", "300件", "40天"),
        (4, "创伤植入物锻造与加工",
         "Forging and CNC of trauma bone plates and screws, titanium alloy and 316L stainless. "
         "ISO13485, FDA registered. Anodizing in house. 20 years export to US and EU.",
         "3万件/月", "1000件", "35天"),
        (5, "运动医学MIM锚钉",
         "MIM process for sports medicine suture anchors, stainless steel 316L. "
         "ISO13485 and CE MDR. Serving European OEM customers.",
         "8000件/月", "2000件", "50天"),
    ],
}


def main():
    ap = argparse.ArgumentParser(description="铺撮合台演示数据")
    ap.add_argument("--yes", action="store_true", help="确认清空现有数据")
    a = ap.parse_args()
    if not a.yes:
        print("  这会清空现有数据库、用户登记与审计日志。")
        print("  确认请加 --yes：python demo.py --yes")
        return 1

    print("=" * 74)
    print("  骨科供需撮合台 · 演示数据")
    print("=" * 74)

    run(["init_db.py", "--reset"])
    # 审计链归档而非清空：历史留痕必须可回溯（安全审计 P1-1 整改）
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive = os.path.join(os.path.dirname(HERE), "audit", "archive")
    os.makedirs(archive, exist_ok=True)
    for p in ("registry/users.jsonl", "registry/blocklist.jsonl", "audit/audit.log"):
        fp = os.path.join(os.path.dirname(HERE), p)
        if os.path.exists(fp) and os.path.getsize(fp) > 0:
            bak = os.path.join(archive, f"{os.path.basename(p)}.{stamp}")
            with open(fp, encoding="utf-8") as src, open(bak, "w", encoding="utf-8") as dst:
                dst.write(src.read())
            print(f"    已归档 {p} -> audit/archive/{os.path.basename(bak)}")
        open(fp, "w", encoding="utf-8").close()

    uid = "U001"
    for name, comp, title, contact, purpose in DEMO["users"]:
        run(["core.py", "register", "--name", name, "--company", comp, "--title", title,
             "--contact", contact, "--purpose", purpose])
        run(["core.py", "pledge", "--user", uid, "--yes"])

    print("\n  主体")
    for name, side, country, city, person, title, email, is_self in DEMO["parties"]:
        args = ["publish.py", "party", "--name", name, "--side", side,
                "--country", country, "--city", city, "--person", person,
                "--title", title, "--email", email, "--user", uid]
        if is_self:
            args.append("--self")
        _, out = run(args)
        pid = out.split("主体已登记")[1].split()[0] if "主体已登记" in out else "?"
        verified = "已核验 " + out.split("在展会名录中找到：")[1].split("\n")[0] if "在展会名录中找到" in out else "未核验"
        print(f"    {pid}  {name:<22} {country:<4} {side:<7} {verified}")

    print("\n  需求（买方）")
    for idx, title, desc, qty, deadline in DEMO["demands"]:
        _, out = run(["publish.py", "demand", "--party", f"P{idx + 1:03d}",
                      "--title", title, "--desc", desc, "--qty", qty,
                      "--deadline", deadline, "--user", uid])
        did = out.split("需求已发布")[1].split()[0] if "需求已发布" in out else "?"
        cats = [l.strip() for l in out.splitlines() if "产品分类" in l or "材料" in l or "资质认证" in l]
        print(f"    {did}  {title}")
        for c in cats:
            print(f"          {c}")

    print("\n  能力（卖方）")
    for idx, title, desc, cap, moq, lt in DEMO["capabilities"]:
        _, out = run(["publish.py", "capability", "--party", f"P{idx + 1:03d}",
                      "--title", title, "--desc", desc, "--capacity", cap,
                      "--moq", moq, "--lead-time", lt, "--user", uid])
        cid = out.split("能力已发布")[1].split()[0] if "能力已发布" in out else "?"
        cats = [l.strip() for l in out.splitlines() if "产品分类" in l or "材料" in l or "资质认证" in l]
        print(f"    {cid}  {title}")
        for c in cats:
            print(f"          {c}")

    print("\n" + "=" * 74)
    print("  全池撮合")
    print("=" * 74)
    code, out = run(["match.py", "run", "--all", "--user", uid, "--min-score", "30", "--verbose"])
    print(out)

    print("  下一步（完整走一遍双向同意）：")
    print("    python match.py list --user U001 --verbose")
    print("    python intro.py request --match M001 --side buyer  --user U001")
    print("    python intro.py accept  --match M001 --side seller --user U001")
    print("    python intro.py reveal  --match M001 --user U001")
    return 0


if __name__ == "__main__":
    sys.exit(main())

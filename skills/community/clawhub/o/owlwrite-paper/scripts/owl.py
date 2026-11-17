#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OwlWrite 命令行（2026-11-09，v1.3.0）——**不配 MCP 也能用**。

零第三方依赖（只要 Python ≥ 3.8）。Agent 直接执行本脚本即可完成检索/写作/检测/排版全流程。

三步上手：
  1. 注册拿 key（对话里让 Agent 走 /v1/auth/register，或到 paper.skillsutra.cn 注册）
  2. 把 key 粘进对话 →  Agent 执行：  echo <key> | python scripts/owl.py init
     （先校验后保存；本机已有其他账号 key 时加 --force）
  3. 自检：                            python scripts/owl.py doctor

常用：
  python scripts/owl.py wallet
  python scripts/owl.py quote --action write --params '{"topic":"...","mode":"standard","target_chars":6000}'
  python scripts/owl.py run --quote <quote_id>
  python scripts/owl.py wait <run_id> --timeout 120      # 分块轮询，可续调
  python scripts/owl.py content <run_id> --save draft.md
  python scripts/owl.py typeset 论文.docx --mode docx --template 学校模板.docx

全局参数（--json / --out / --base）必须写在子命令**前面**，如：owl.py --json content <run_id>。

输出：JSON 到 stdout（默认精简长文本，--json 全量，--out 落盘）。
出错：{"error": code, "message": ...} 到 stdout，退出码 2——按 code 分支处理，不要盲目重试。
"""
import argparse
import getpass
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import owl_api  # noqa: E402


def _utf8_stdout():
    """Windows 控制台默认 GBK，中文 JSON 会乱码——强制 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass


TRIM_LIMIT = 2000


def trim(obj, limit=TRIM_LIMIT):
    """默认输出精简：只截超长正文，其余原样。--json 关闭。"""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(v, str) and len(v) > limit:
                out[k] = v[:limit] + f"…[已截断，共 {len(v)} 字；用 --json 或 --out 取全文]"
            elif k == "items" and isinstance(v, list):
                out[k] = [trim(i, 600) if isinstance(i, dict) else i for i in v]
            else:
                out[k] = trim(v, limit)
        return out
    if isinstance(obj, list):
        return [trim(i, limit) for i in obj]
    return obj


def emit(data, args, code=0):
    out = data if getattr(args, "json", False) else trim(data)
    text = json.dumps(out, ensure_ascii=False, indent=1)
    print(text)
    if getattr(args, "out", None):
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=1))
        print(f"# 已保存 -> {args.out}", file=sys.stderr)
    sys.exit(code)


def emit_err(exc):
    print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=1))
    sys.exit(2)


def build_parser():
    p = argparse.ArgumentParser(
        prog="owl.py",
        description="OwlWrite 命令行（无需 MCP 配置）",
        epilog="注意：全局参数（--base / --json / --out）必须写在子命令前面，"
               "如 owl.py --json content <run_id>；写在子命令后面会报 unrecognized arguments。")
    p.add_argument("--base", help="网关地址（默认 https://owl.skillsutra.cn；必须写在子命令前面）")
    p.add_argument("--json", action="store_true", help="输出完整 JSON（不截断长文本）")
    p.add_argument("--out", help="把完整 JSON 另存到文件")
    # 注意：出于安全考虑不提供 --key 参数（key 会进进程命令行被同机进程看到）。
    # key 只走环境变量 OWL_API_KEY 或凭据文件 ~/.owl_creds.json。
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="文献检索（中英；0 结果不扣费）")
    s.add_argument("query", help="检索词，如 \"生物防腐剂 制备\"")
    s.add_argument("--limit", type=int, default=5, help="返回条数（默认 5）")
    s.add_argument("--lang", default="all", choices=["all", "zh", "en"], help="限定语种")
    s.add_argument("--expand", action="store_true", help="结果不足时自动扩展一次检索词")

    sub.add_parser("products", help="全平台价目表")
    sub.add_parser("meta", help="版本 / 公告 / 通道就绪状态")
    sub.add_parser("disciplines", help="斟知学科码表")

    s = sub.add_parser("quote", help="报价（写作/检测/核验/排版/配图，不扣费）")
    s.add_argument("--action", required=True,
                   choices=["write", "check", "verify", "typeset", "figure"])
    s.add_argument("--params", required=True, help="JSON 参数；写作 {\"topic\":\"…\",\"mode\":\"standard\",\"target_chars\":6000}；检测(1020)需 content+hanzi（或 pages），content 直传时不会自动估字数")

    s = sub.add_parser("upload", help="上传本机文件，拿 file_id")
    s.add_argument("file")

    s = sub.add_parser("run", help="按 quote_id 执行任务，返回 run_id（长任务用 wait 续轮询）")
    s.add_argument("--quote", required=True, help="quote 接口返回的报价单号")

    s = sub.add_parser("status", help="查任务状态")
    s.add_argument("run_id")

    s = sub.add_parser("wait", help="分块轮询（单次最多 --timeout 秒，可续调）")
    s.add_argument("run_id")
    s.add_argument("--timeout", type=int, default=120)

    s = sub.add_parser("report", help="任务报告（检测 4 份 / 核验逐条摘要）")
    s.add_argument("run_id")
    s.add_argument("--part", default="", choices=["", "main", "compare", "simple", "fulltext"])

    s = sub.add_parser("content", help="写作全文与参考文献")
    s.add_argument("run_id", help="run 返回的任务号")
    s.add_argument("--save", help="把 content 正文另存为文件")

    s = sub.add_parser("figure", help="科研配图（tikz / chart / image）")
    s.add_argument("--mode", required=True, choices=["tikz", "chart", "image"])
    s.add_argument("--desc", required=True)
    s.add_argument("--count", type=int, default=1)
    s.add_argument("--data", default="")
    s.add_argument("--file-id", default="")
    s.add_argument("--type", dest="figure_type", default="")
    s.add_argument("--timeout", type=int, default=180)

    s = sub.add_parser("typeset", help="按学校模板排版")
    s.add_argument("file", nargs="?", default="")
    s.add_argument("--mode", default="latex", choices=["latex", "docx"])
    s.add_argument("--template", default="", help="学校模板 .docx（docx 模式必填）")
    s.add_argument("--file-id", default="")
    s.add_argument("--template-file-id", default="")
    s.add_argument("--entry", default="")
    s.add_argument("--pages", type=int, default=0)
    s.add_argument("--hanzi", type=int, default=0)
    s.add_argument("--title", default="")
    s.add_argument("--blind", action="store_true")
    s.add_argument("--refs-std", dest="refs_std", default="2015", choices=["2015", "2025"])
    s.add_argument("--author", default="")
    s.add_argument("--student-id", dest="student_id", default="")
    s.add_argument("--college", default="")
    s.add_argument("--major", default="")
    s.add_argument("--advisor", default="")
    s.add_argument("--date", default="")

    sub.add_parser("wallet", help="积分余额")
    s = sub.add_parser("ledger", help="逐笔积分流水（对账用；含每笔后余额）")
    s.add_argument("--limit", type=int, default=50, help="条数（默认 50，上限 500）")
    s.add_argument("--offset", type=int, default=0, help="翻页偏移")

    s = sub.add_parser("recharge", help="创建充值订单（10/30/50/100/500 元）")
    s.add_argument("--amount", type=int, required=True)
    s.add_argument("--channel", default="wechat", choices=["wechat", "alipay"])

    s = sub.add_parser("recharge-status", help="查充值订单状态")
    s.add_argument("order_no")

    s = sub.add_parser("fulltext", help="中文期刊全文直链（价格以 products 实拉为准）")
    s.add_argument("identifier")

    s = sub.add_parser("article", help="单篇文献详情（价格以 products 实拉为准）")
    s.add_argument("identifier")
    s.add_argument("--lang", default="zh", choices=["zh", "en"])

    s = sub.add_parser("oa", help="外文 OA 免费全文（0 积分）")
    s.add_argument("--doi", default="")
    s.add_argument("--title", default="")

    s = sub.add_parser("citations", help="引文追溯（refs / cited）")
    s.add_argument("doi")
    s.add_argument("--direction", default="refs", choices=["refs", "cited"])
    s.add_argument("--limit", type=int, default=20)

    s = sub.add_parser("campaign", help="活动与邀请；传 --code 兑换券码")
    s.add_argument("--code", default="")

    s = sub.add_parser("claim-favorite", help="提交收藏截图领积分")
    s.add_argument("image")

    s = sub.add_parser("init", help="保存 API key（从 stdin 读取；先校验后保存，换账号需 --force）")
    s.add_argument("--path", help="凭据文件路径（默认 ~/.owl_creds.json）")
    s.add_argument("--force", action="store_true",
                   help="本机已有其他账号的 key 时，用它确认覆盖（防误换账号）")

    sub.add_parser("doctor", help="自检：连通性 / key / 版本更新 / 余额（无 key 也能测连通性）")

    return p


def _read_key():
    """从 stdin 或交互读 key。stdin 分支设长度上限防挂起；交互用 getpass 不回显。"""
    if not sys.stdin.isatty():
        raw = sys.stdin.read(512).strip()
        return raw.splitlines()[0].strip() if raw else ""
    try:
        return getpass.getpass("粘贴 API key（owl_sk_ 开头，输入不回显）：").strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def cmd_init(args):
    """先校验后保存：key 无效不落盘，绝不覆盖丢失用户原 key。"""
    key = _read_key()
    if not key:
        emit({"error": "no_key", "message": "没读到 key。用法：echo <key> | python scripts/owl.py init"}, args, 2)
    if not key.startswith("owl_sk_"):
        emit({"error": "bad_key", "message": "key 应以 owl_sk_ 开头；请确认复制完整"}, args, 2)

    # 1) 先校验：余额接口是唯一的「key 是否有效」事实源，失败就不写盘
    try:
        w = owl_api.wallet(key=key, base=args.base)
    except owl_api.ApiError as exc:
        emit({"error": exc.code, "message": "key 校验未通过，没有保存：" + exc.message}, args, 2)

    # 2) 换账号保护：本地已有不同账号的 key 时必须 --force
    path = args.path or owl_api.creds_paths()[0]
    old = ""
    try:
        with open(path, encoding="utf-8") as f:
            old = ((json.load(f) or {}).get("owl_api_key") or "").strip()
    except Exception:  # noqa: BLE001 — 没有旧凭据/读不出都当作「无旧 key」
        old = ""
    result = {"saved": None, "key_prefix": "owl_sk_…（已隐藏）"}
    if old and old[:12] != key[:12] and not getattr(args, "force", False):
        emit({"error": "key_conflict",
              "message": "本机已保存过另一个账号的 key。确认要换账号的话，加 --force 重新执行"
                         "（旧 key 会备份为 .bak；换账号后余额与历史都走新账号）"}, args, 2)

    # 3) 校验通过才落盘（save_key 自动备份旧文件并设 0600 权限）
    saved = owl_api.save_key(key, path)
    result["saved"] = saved
    result["verify"] = "ok"
    result["balance_avail"] = w.get("balance_avail")
    result["balance_total"] = w.get("balance_total")
    if old and old[:12] != key[:12]:
        result["account_switched"] = True
        result["backup"] = saved + ".bak"
    emit(result, args, 0)


def cmd_doctor(args):
    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    add("python", sys.version_info >= (3, 8), sys.version.split()[0])
    add("owl_api", True, os.path.join(os.path.dirname(os.path.abspath(__file__)), "owl_api.py"))
    add("base", True, owl_api.resolve_base(args.base))
    add("version", True, owl_api.OWL_SKILL_VERSION)

    key = None
    try:
        key = owl_api.load_key()
        add("key", True, "owl_sk_…（来源：%s）" % (
            "环境变量" if os.environ.get("OWL_API_KEY") else "凭据文件"))
    except owl_api.ApiError as exc:
        add("key", False, exc.message)

    # 连通性用匿名请求：没 key 也能测（/v1/meta 无需鉴权）
    try:
        m = owl_api.meta(key=None, base=args.base)
        add("connectivity", True, "/v1/meta 可达")
        sk = m.get("skill") or {}
        latest = sk.get("latest_version") or m.get("latest_version") or ""
        required = sk.get("required_update") is True
        update_ok = True
        try:  # 版本比较：x.y.z 逐段比
            loc = [int(x) for x in owl_api.OWL_SKILL_VERSION.split(".")]
            rem = [int(x) for x in str(latest).split(".")]
            update_ok = not (required and loc < rem)
        except Exception:  # noqa: BLE001
            update_ok = True
        add("latest_version", update_ok,
            f"服务端 {latest or '未知'} / 本地 {owl_api.OWL_SKILL_VERSION}"
            + ("；服务端要求更新，请先更新到最新版" if not update_ok else ""))
        ch = m.get("channels") or {}
        add("typeset_ready", ch.get("typeset_ready") is True, str(ch.get("typeset_detail") or ""))
    except owl_api.ApiError as exc:
        add("connectivity", False, f"{exc.code}: {exc.message}")

    if key:
        try:
            w = owl_api.wallet(key=key, base=args.base)
            add("wallet", True, f"可用 {w.get('balance_avail')} 积分 / 总计 {w.get('balance_total')}")
        except owl_api.ApiError as exc:
            add("wallet", False, exc.message)

    emit({"checks": checks, "ok": all(c["ok"] for c in checks if c["check"] != "typeset_ready")},
         args, 0 if all(c["ok"] for c in checks if c["check"] != "typeset_ready") else 2)


def dispatch(args):
    b = args.base
    k = None  # key 一律走环境变量/凭据文件，不进命令行
    c = args.cmd
    if c == "init":
        return cmd_init(args)
    if c == "doctor":
        return cmd_doctor(args)
    if c == "search":
        return emit(owl_api.search(args.query, args.limit, args.lang, args.expand, key=k, base=b), args)
    if c == "products":
        return emit(owl_api.products(key=k, base=b), args)
    if c == "meta":
        return emit(owl_api.meta(key=k, base=b), args)
    if c == "disciplines":
        return emit(owl_api.disciplines(key=k, base=b), args)
    if c == "quote":
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as exc:
            return emit({"error": "bad_params", "message": f"--params 不是合法 JSON：{exc}"}, args, 2)
        return emit(owl_api.quote(args.action, params, key=k, base=b), args)
    if c == "upload":
        return emit(owl_api.upload(args.file, key=k, base=b), args)
    if c == "run":
        return emit(owl_api.run(args.quote, key=k, base=b), args)
    if c == "status":
        return emit(owl_api.run_status(args.run_id, key=k, base=b), args)
    if c == "wait":
        return emit(owl_api.wait(args.run_id, args.timeout, key=k, base=b), args)
    if c == "report":
        return emit(owl_api.run_report(args.run_id, args.part, key=k, base=b), args)
    if c == "content":
        data = owl_api.run_content(args.run_id, key=k, base=b)
        if args.save and data.get("content"):
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(data["content"])
            data["saved"] = args.save
        return emit(data, args)
    if c == "figure":
        return emit(owl_api.figure(args.mode, args.desc, args.count, args.data,
                                   args.file_id, args.figure_type, args.timeout,
                                   key=k, base=b), args)
    if c == "typeset":
        return emit(owl_api.typeset(
            args.file, args.mode, args.template, args.entry, args.pages, args.hanzi,
            args.title, args.file_id, args.template_file_id, args.author, args.student_id,
            args.college, args.major, args.advisor, args.date, args.blind, args.refs_std,
            key=k, base=b), args)
    if c == "wallet":
        return emit(owl_api.wallet(key=k, base=b), args)
    if c == "ledger":
        return emit(owl_api.ledger(args.limit, args.offset, key=k, base=b), args)
    if c == "recharge":
        return emit(owl_api.recharge(args.amount, args.channel, key=k, base=b), args)
    if c == "recharge-status":
        return emit(owl_api.recharge_status(args.order_no, key=k, base=b), args)
    if c == "fulltext":
        return emit(owl_api.fulltext(args.identifier, key=k, base=b), args)
    if c == "article":
        return emit(owl_api.article(args.identifier, args.lang, key=k, base=b), args)
    if c == "oa":
        return emit(owl_api.oa(args.doi, args.title, key=k, base=b), args)
    if c == "citations":
        return emit(owl_api.citations(args.doi, args.direction, args.limit, key=k, base=b), args)
    if c == "campaign":
        return emit(owl_api.campaign(args.code, key=k, base=b), args)
    if c == "claim-favorite":
        return emit(owl_api.claim_favorite(args.image, key=k, base=b), args)
    return emit({"error": "unknown_command", "message": c}, args, 2)


def main():
    _utf8_stdout()
    args = build_parser().parse_args()
    try:
        dispatch(args)
    except owl_api.ApiError as exc:
        emit_err(exc)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — 任何未预期异常都不给 Agent 留 traceback，给结构化错误
        emit({"error": "internal", "message": f"本地执行出错：{type(exc).__name__}: {exc}。"
                                              "请原样把这条信息反馈给用户，不要盲目重试。"}, args, 2)


if __name__ == "__main__":
    main()

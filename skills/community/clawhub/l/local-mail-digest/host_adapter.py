#!/usr/bin/env python3
# 宿主桥接适配器（零配置本地执行端）
# 作用：把"邮箱连接器 / 任意来源导出的邮件JSON"交给 local-mail-digest 生成摘要，并可选推手机。
# 广大用户零配置用法：
#   宿主(WorkBuddy / Codex / Claude / Hermes / OpenClaw)用【已连的邮箱连接器】拉邮件
#   -> 存成 emails.json [{from, subject, date, body}]
#   -> python host_adapter.py --emails-json emails.json --json 摘要.json [--webhook 机器人URL]
# 用户侧零授权码、零 IMAP 配置；数据不出电脑。
import argparse, json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DIGEST = os.path.join(HERE, "digest.py")


def push_webhook(url, text, wh_type="auto"):
    if wh_type == "auto":
        wh_type = "wecom" if "qyapi.weixin" in url else ("feishu" if "feishu" in url else "wecom")
    payload = ({"msgtype": "text", "text": {"content": text}} if wh_type == "wecom"
               else {"msg_type": "text", "content": {"text": text}})
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"[推送] {wh_type} 响应: {r.read().decode('utf-8')[:80]}")
    except Exception as ex:
        print(f"[推送] 失败: {ex}")


def main():
    ap = argparse.ArgumentParser(description="邮件摘要宿主桥接（零配置）")
    ap.add_argument("--emails-json", required=True, help="连接器导出的邮件列表JSON")
    ap.add_argument("--out", default="邮件摘要.html")
    ap.add_argument("--json", default="摘要.json")
    ap.add_argument("--md", default=None)
    ap.add_argument("--webhook", default=None, help="企微/飞书机器人URL(手机通知)")
    ap.add_argument("--wh-type", default="auto")
    ap.add_argument("--llm", default=None, help="可选本地LLM端点")
    ap.add_argument("--model", default="hermes3")
    a = ap.parse_args()

    data = json.load(open(a.emails_json, encoding="utf-8"))
    for e in data:
        for k in ("from", "subject", "body"):
            e.setdefault(k, "")
        e.setdefault("date", "")

    cmd = [sys.executable, DIGEST, "--input", a.emails_json, "--out", a.out, "--json", a.json]
    if a.md:
        cmd += ["--md", a.md]
    if a.llm:
        cmd += ["--llm", a.llm, "--model", a.model]
    subprocess.run(cmd, check=True)
    print(f"[桥接] 已生成 {a.out} / {a.json}")

    if a.webhook:
        res = json.load(open(a.json, encoding="utf-8"))
        high = [e for e in res["emails"] if e["priority"] == "high"]
        lines = [f"📥 邮件摘要(共{res['total']}封·高优{res['high']})", ""]
        if high:
            lines.append("🔴 今日重点：")
            for e in high[:6]:
                ddl = f" ⏰{','.join(e['ddl'])}" if e["ddl"] else ""
                lines.append(f"· [{e['project']}] {e['from']}：{e['subject']}{ddl}")
        lines.append("（完整版见电脑本地 HTML）")
        push_webhook(a.webhook, "\n".join(lines), a.wh_type)


if __name__ == "__main__":
    main()

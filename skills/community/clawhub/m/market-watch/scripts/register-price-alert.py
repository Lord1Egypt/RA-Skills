#!/usr/bin/env python3
"""
register-price-alert.py — 注册价格警报

用法示例:
  python3 register-price-alert.py \
    --agent laok \
    --asset ETH \
    --condition ">=" \
    --target 2150 \
    --context-summary "ETH减仓窗口：减3.5枚，套出换HYPE" \
    --session-key "agent:laok:feishu:direct:ou_xxx" \
    --reply-channel feishu \
    --reply-to "user:ou_xxx"

输出:
  ✅ 警报已注册: eth-1741234567
     ETH >= 2150 (crypto)
     文件: ~/.openclaw/agents/laok/private/market-alerts.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent))
from common import atomic_write_json


def get_transcript_info(agent_id: str) -> tuple[str, str]:
    """尝试自动获取当前会话的 transcript 文件和最新消息 ID"""
    import subprocess
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "--agent", agent_id, "--json"],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(result.stdout)
        sessions = data.get("sessions", [])
        if sessions:
            latest = sorted(sessions, key=lambda s: s.get("updatedAt", 0), reverse=True)[0]
            session_id = latest.get("sessionId", "")
            sessions_dir = Path.home() / f".openclaw/agents/{agent_id}/sessions"
            transcript_file = str(sessions_dir / f"{session_id}.jsonl")
            return transcript_file, session_id
    except Exception:
        pass
    return "", ""


def main() -> str:
    parser = argparse.ArgumentParser(description="Register a price alert")
    parser.add_argument("--agent",            default="laok",    help="Agent ID")
    parser.add_argument("--asset",            required=True,     help="资产代码，如 ETH / 600519")
    parser.add_argument("--market",           default="crypto",  help="市场: crypto / astock")
    parser.add_argument("--condition",        required=True,     help="条件: >= / <= / > / <")
    parser.add_argument("--target",           required=True,     type=float, help="目标价格")
    parser.add_argument("--one-shot",         action="store_true", default=True,
                        help="触发一次后自动停止（默认 true）")
    parser.add_argument("--no-one-shot",      dest="one_shot", action="store_false",
                        help="持续监控，触发后不停止")
    parser.add_argument("--context-summary",  default="",        help="设盘时的上下文摘要")
    parser.add_argument("--session-key",      default="",        help="当前 session key（稳定标识）")
    parser.add_argument("--reply-channel",    default="feishu",  help="通知渠道")
    parser.add_argument("--reply-to",         default="",        help="通知目标，如 user:ou_xxx")
    parser.add_argument("--transcript-file",  default="",        help="transcript 文件路径（自动填充）")
    parser.add_argument("--transcript-msg-id", default="",       help="设盘消息的 ID")
    parser.add_argument("--alerts-file",      default="",        help="自定义 alerts 文件路径")
    args = parser.parse_args()

    # 自动补全 transcript 信息
    transcript_file = args.transcript_file
    transcript_msg_id = args.transcript_msg_id
    if not transcript_file:
        transcript_file, _ = get_transcript_info(args.agent)

    # 构建 alert 对象
    ts_id = int(datetime.now().timestamp())
    alert_id = f"{args.asset.lower()}-{ts_id}"

    alert = {
        "id":               alert_id,
        "type":             "price",
        "status":           "active",
        "asset":            args.asset.upper(),
        "market":           args.market,
        "condition":        args.condition,
        "target_price":     args.target,
        "one_shot":         args.one_shot,
        "context_summary":  args.context_summary,
        "session_key":      args.session_key,
        "agent_id":         args.agent,
        "reply_channel":    args.reply_channel,
        "reply_to":         args.reply_to,
        "transcript_file":  transcript_file,
        "transcript_msg_id": transcript_msg_id,
        "created_at":       datetime.now().isoformat(),
    }

    # 读取/创建 alerts 文件
    alerts_path = Path(args.alerts_file) if args.alerts_file else \
        Path.home() / f".openclaw/agents/{args.agent}/private/market-alerts.json"
    alerts_path.parent.mkdir(parents=True, exist_ok=True)

    if alerts_path.exists():
        with open(alerts_path) as f:
            data = json.load(f)
    else:
        data = {"alerts": []}

    data["alerts"].append(alert)

    # S-02: 原子替换写入，防并发损坏（N-01: 复用 common.py）
    atomic_write_json(alerts_path, data)

    # 统计活跃警报数量
    active_count = sum(1 for a in data["alerts"] if a.get("status") == "active")

    print(f"✅ 警报已注册: {alert_id}")
    print(f"   {args.asset.upper()} {args.condition} {args.target} ({args.market})")
    print(f"   文件: {alerts_path}")
    print(f"   当前活跃警报: {active_count} 个")
    if not args.session_key:
        print(f"   ⚠️  未设置 --session-key，触发时将无法精准找到 session，会 fallback 到 agent")

    # 自动拉起守护进程（如未运行）
    daemon_sh = Path(__file__).parent / "daemon.sh"
    if daemon_sh.exists():
        import subprocess
        subprocess.run(
            ["bash", str(daemon_sh), "start", "--agent", args.agent],
            capture_output=True,
        )

    return alert_id


if __name__ == "__main__":
    main()

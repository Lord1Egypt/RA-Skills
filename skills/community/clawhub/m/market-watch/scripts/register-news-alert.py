#!/usr/bin/env python3
"""
register-news-alert.py — 注册新闻关键词警报

用法示例:
  python3 register-news-alert.py \
    --agent laok \
    --keywords "BTC ETF,BlackRock,Bitcoin" \
    --keyword-mode any \
    --sources "coindesk,cointelegraph,jin10" \
    --context-summary "BTC ETF 审批进展，可能触发价格波动" \
    --session-key "agent:laok:feishu:direct:ou_xxx" \
    --reply-channel feishu \
    --reply-to "user:ou_xxx"

  # 持续监控（默认）
  python3 register-news-alert.py --agent laok --keywords "ETF,BlackRock"

  # 一次性：发现一条就停（适合明确事件等待）
  python3 register-news-alert.py --agent laok --keywords "停火,ceasefire" --one-shot

  # 指定数据源
  python3 register-news-alert.py --agent laok --keywords "HYPE" \
    --sources "coindesk,cointelegraph,theblock,decrypt"

输出:
  ✅ 新闻警报已注册: news-1741234567
     关键词: BTC ETF, BlackRock (any 模式)
     数据源: coindesk, cointelegraph, jin10
     文件: ~/.openclaw/agents/laok/private/market-alerts.json
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import atomic_write_json


ALL_SOURCES = ["jin10", "wallstreetcn", "coindesk", "cointelegraph", "theblock", "decrypt"]


def get_transcript_info(agent_id: str) -> tuple[str, str]:
    """尝试自动获取当前会话的 transcript 文件和最新消息 ID"""
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "--agent", agent_id, "--json"],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(result.stdout)
        sessions = data.get("sessions", [])
        if sessions:
            latest = sorted(sessions, key=lambda s: s.get("updatedAt", 0), reverse=True)[0]
            session_id   = latest.get("sessionId", "")
            sessions_dir = Path.home() / f".openclaw/agents/{agent_id}/sessions"
            transcript_file = str(sessions_dir / f"{session_id}.jsonl")
            return transcript_file, session_id
    except Exception:
        pass
    return "", ""


def main() -> str:
    parser = argparse.ArgumentParser(
        description="Register a news keyword alert",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--agent",
        default="laok",
        help="Agent ID（默认 laok）")
    parser.add_argument("--keywords",
        required=True,
        help="关键词，逗号分隔。如 'BTC ETF,BlackRock,Bitcoin'")
    parser.add_argument("--keyword-mode",
        default="any",
        choices=["any", "all"],
        help="匹配模式：any=任一命中 | all=全部命中（默认 any）")
    parser.add_argument("--sources",
        default=",".join(ALL_SOURCES),
        help=f"数据源，逗号分隔（默认全部）。可选: {', '.join(ALL_SOURCES)}")
    parser.add_argument("--poll-interval",
        default=300, type=int,
        help="轮询间隔（秒，默认 300 = 5分钟）")
    parser.add_argument("--one-shot",
        action="store_true", default=False,
        help="触发一次后自动停止（默认持续监控）")
    parser.add_argument("--context-summary",
        default="",
        help="设置警报时的上下文摘要，触发时 agent 读取用于还原背景")
    parser.add_argument("--session-key",
        default="",
        help="当前 session key（稳定标识，用于触发时精准找到 session）")
    parser.add_argument("--reply-channel",
        default="feishu",
        help="通知渠道（默认 feishu）")
    parser.add_argument("--reply-to",
        default="",
        help="通知目标，如 user:ou_xxx 或 chat:oc_xxx")
    parser.add_argument("--transcript-file",
        default="",
        help="transcript 文件路径（自动获取，通常无需手动指定）")
    parser.add_argument("--transcript-msg-id",
        default="",
        help="设置警报的消息 ID")
    parser.add_argument("--alerts-file",
        default="",
        help="自定义 alerts 文件路径（默认: ~/.openclaw/agents/{agent}/private/market-alerts.json）")
    args = parser.parse_args()

    # 解析关键词
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]
    if not keywords:
        print("❌ 关键词不能为空", file=sys.stderr)
        sys.exit(1)

    # 解析并验证数据源
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    invalid = [s for s in sources if s not in ALL_SOURCES]
    if invalid:
        print(f"❌ 无效数据源: {invalid}", file=sys.stderr)
        print(f"   可选: {', '.join(ALL_SOURCES)}", file=sys.stderr)
        sys.exit(1)

    # 验证 poll_interval
    if args.poll_interval < 30:
        print(f"⚠️  poll_interval 最小 30 秒，已自动设为 30", file=sys.stderr)
        args.poll_interval = 30

    # 自动补全 transcript 信息
    transcript_file    = args.transcript_file
    transcript_msg_id  = args.transcript_msg_id
    if not transcript_file:
        transcript_file, _ = get_transcript_info(args.agent)

    # 构建 alert 对象
    ts_id    = int(datetime.now().timestamp())
    alert_id = f"news-{ts_id}"

    alert = {
        "id":               alert_id,
        "type":             "news",
        "status":           "active",
        "keywords":         keywords,
        "keyword_mode":     args.keyword_mode,
        "sources":          sources,
        "poll_interval":    args.poll_interval,
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

    # 读取 / 创建 alerts 文件
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

    # 统计
    active_count = sum(1 for a in data["alerts"] if a.get("status") == "active")

    print(f"✅ 新闻警报已注册: {alert_id}")
    print(f"   关键词: {', '.join(keywords)} ({args.keyword_mode} 模式)")
    print(f"   数据源: {', '.join(sources)}")
    print(f"   轮询间隔: {args.poll_interval}s | 持续监控: {not args.one_shot}")
    print(f"   文件: {alerts_path}")
    print(f"   当前活跃警报: {active_count} 个")
    if not args.session_key:
        print(f"   ⚠️  未设置 --session-key，触发时将 fallback 到 agent 默认 session")

    # 自动拉起守护进程（如未运行）
    daemon_sh = Path(__file__).parent / "daemon.sh"
    if daemon_sh.exists():
        subprocess.run(
            ["bash", str(daemon_sh), "start", "--agent", args.agent],
            capture_output=True,
        )
    else:
        print(f"   ⚠️  未找到 daemon.sh，请手动启动 news-monitor.py")

    return alert_id


if __name__ == "__main__":
    main()

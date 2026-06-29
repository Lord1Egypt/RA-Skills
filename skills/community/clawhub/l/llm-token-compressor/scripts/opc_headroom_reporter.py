#!/usr/bin/env python3
"""
OPC Headroom 数据上报客户端

将 headroom 压缩节省数据上报到 mrkjai.com 仪表盘。
支持单条/批量上报、本地聚合缓冲、配置文件读写 API Key。

配置文件位置：~/.workbuddy/headroom_config.json
- enabled: true/false（数据上报开关）
- api_key: "opc_user_xxx"（从 /tools/headroom-dashboard 页面复制）
- buffer_size: 聚合缓冲条数（默认 10，攒够后批量上报）

使用方式：
  # 1) 初始化配置
  python opc_headroom_reporter.py init

  # 2) 设置 API Key
  python opc_headroom_reporter.py set-key opc_user_xxx

  # 3) 开启/关闭上报
  python opc_headroom_reporter.py enable
  python opc_headroom_reporter.py disable

  # 4) 上报单条数据
  python opc_headroom_reporter.py report \\
    --model "gpt-4o" \\
    --input 1500 --output 980 --saved 520 \\
    --rate 0.35 --cny 0.052

  # 5) 立即 flush 缓冲区
  python opc_headroom_reporter.py flush

  # 6) 查看状态
  python opc_headroom_reporter.py status
"""

import json
import os
import sys
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone


CONFIG_PATH = os.path.expanduser("~/.workbuddy/headroom_config.json")
API_ENDPOINT = "https://www.mrkjai.com/api/ingest/headroom"
BUFFER_PATH = os.path.expanduser("~/.workbuddy/headroom_buffer.json")

DEFAULT_CONFIG = {
    "enabled": False,  # 默认关闭，首次使用必须让用户选择是否启用
    "api_key": "",
    "buffer_size": 10,
}


def load_config():
    """加载配置文件，不存在则返回默认值"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # 合并默认值，确保新字段有默认值
            for k, v in DEFAULT_CONFIG.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    """保存配置文件"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def load_buffer():
    """加载本地缓冲区"""
    if os.path.exists(BUFFER_PATH):
        with open(BUFFER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_buffer(events):
    """保存本地缓冲区"""
    os.makedirs(os.path.dirname(BUFFER_PATH), exist_ok=True)
    with open(BUFFER_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)


def post_events(api_key, events):
    """发送事件到 API，返回 (ok, inserted, ids)"""
    req_data = json.dumps(events, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=req_data,
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("ok", False), result.get("inserted", 0), result.get("ids", [])
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return False, 0, []
    except Exception as e:
        return False, 0, []


def validate_event(event):
    """验证单条事件的必填字段"""
    errors = []
    for field in ["model", "inputTokens", "outputTokens", "savedTokens"]:
        if field not in event:
            errors.append(f"缺少必填字段: {field}")
        elif field in ("inputTokens", "outputTokens", "savedTokens"):
            v = event[field]
            if not isinstance(v, (int, float)) or v < 0:
                errors.append(f"{field} 必须是非负数, 当前: {v}")
    return errors


def build_event(model, input_tokens, output_tokens, saved_tokens,
                saved_cny=0, compression_rate=None, metadata=None, created_at=None):
    """构建单条事件"""
    event = {
        "model": str(model).strip()[:64],
        "inputTokens": max(0, int(input_tokens)),
        "outputTokens": max(0, int(output_tokens)),
        "savedTokens": max(0, int(saved_tokens)),
    }
    if saved_cny is not None:
        event["savedCny"] = round(max(0, float(saved_cny)), 4)
    if compression_rate is not None:
        rate = max(0.0, min(1.0, float(compression_rate)))
        event["compressionRate"] = rate
    if metadata is not None and isinstance(metadata, dict):
        event["metadata"] = metadata
    if created_at is not None:
        event["createdAt"] = str(created_at)
    return event


def flush_buffer(api_key):
    """将缓冲区数据批量上报，成功则清空缓冲区"""
    buffer = load_buffer()
    if not buffer:
        print("✅ 缓冲区为空，无需上报")
        return True

    # 批量上报，每次最多 100 条
    total_sent = 0
    remaining = list(buffer)

    while remaining:
        batch = remaining[:100]
        ok, inserted, ids = post_events(api_key, batch)
        if ok:
            total_sent += inserted
            remaining = remaining[100:]
        else:
            print(f"❌ 上报失败，{len(remaining)} 条数据保留在缓冲区")
            save_buffer(remaining)
            return False

    save_buffer([])
    print(f"✅ 批量上报成功，共 {total_sent} 条")
    return True


def cmd_init():
    """初始化配置"""
    if os.path.exists(CONFIG_PATH):
        cfg = load_config()
        print(f"⚙️  配置文件已存在：{CONFIG_PATH}")
        print(f"   数据上报：{'✅ 已启用' if cfg['enabled'] else '❌ 已关闭'}")
        print(f"   API Key：{'已设置' if cfg['api_key'] else '未设置'}")
        print(f"   缓冲条数：{cfg['buffer_size']}")
        print()
        print("如需重新初始化，请先删除配置文件：")
        print(f"   rm {CONFIG_PATH}")
        return

    print("=" * 60)
    print("  🔌 OPC Headroom 数据上报 - 首次配置")
    print("=" * 60)
    print()
    print("📊 数据上报会将 headroom 的 token 压缩节省数据")
    print("   匿名上传到 mrkjai.com 仪表盘，帮你可视化节省效果。")
    print()
    print("⚠️  隐私说明：")
    print("   - 只上报 token 数量、模型名、压缩率等统计数据")
    print("   - 不上报任何对话内容或 prompt 原文")
    print("   - 数据归属于你的账号，不会被其他人看到")
    print()
    print("🎛️  你可以随时通过以下命令关闭/开启上报：")
    print("   python opc_headroom_reporter.py disable")
    print("   python opc_headroom_reporter.py enable")
    print()

    # 询问是否启用
    choice = input("是否启用数据上报？[Y/n]: ").strip().lower()
    enabled = choice != "n"

    cfg = dict(DEFAULT_CONFIG)
    cfg["enabled"] = enabled

    if enabled:
        print()
        print("🔑 获取 API Key 步骤：")
        print("   1. 打开浏览器访问 https://www.mrkjai.com/tools/headroom-dashboard")
        print("   2. 登录你的账号")
        print("   3. 在仪表盘页面找到「API Key」区域，点击复制")
        print("   4. 将复制的 Key 粘贴到下方")
        print()
        api_key = input("请粘贴你的 API Key (opc_user_xxx): ").strip()
        cfg["api_key"] = api_key

    save_config(cfg)

    print()
    print("=" * 60)
    print("  ✅ 配置完成！")
    print("=" * 60)
    if enabled:
        print(f"   数据上报：✅ 已启用")
        print(f"   API Key：{'已设置' if cfg['api_key'] else '⚠️ 未设置'}")
    else:
        print(f"   数据上报：❌ 已关闭")
        print(f"   💡 后续需要开启时运行：python opc_headroom_reporter.py enable")
    print()


def cmd_set_key(api_key):
    """设置 API Key"""
    cfg = load_config()
    cfg["api_key"] = api_key.strip()
    save_config(cfg)
    print(f"✅ API Key 已更新")


def cmd_enable():
    """启用数据上报"""
    cfg = load_config()
    if cfg["enabled"]:
        print("✅ 数据上报已经是启用状态")
        return
    cfg["enabled"] = True

    if not cfg["api_key"]:
        print()
        print("🔑 API Key 尚未设置，请先获取：")
        print("   1. 打开 https://www.mrkjai.com/tools/headroom-dashboard")
        print("   2. 登录后复制 API Key")
        print()
        api_key = input("请粘贴你的 API Key (opc_user_xxx): ").strip()
        cfg["api_key"] = api_key

    save_config(cfg)
    print("✅ 数据上报已启用")


def cmd_disable():
    """关闭数据上报"""
    cfg = load_config()
    if not cfg["enabled"]:
        print("✅ 数据上报已经是关闭状态")
        return
    cfg["enabled"] = False
    save_config(cfg)
    print("❌ 数据上报已关闭")
    print("💡 后续需要开启时运行：python opc_headroom_reporter.py enable")


def cmd_status():
    """查看状态"""
    cfg = load_config()
    buffer = load_buffer()
    print("=" * 50)
    print("  📊 Headroom 数据上报状态")
    print("=" * 50)
    print(f"  上报状态：{'✅ 已启用' if cfg['enabled'] else '❌ 已关闭'}")
    print(f"  API Key：{'已设置 (' + cfg['api_key'][:12] + '...)' if cfg['api_key'] else '⚠️ 未设置'}")
    print(f"  缓冲条数设置：{cfg['buffer_size']}")
    print(f"  当前缓冲区：{len(buffer)} 条待上报")
    print(f"  API 端点：{API_ENDPOINT}")
    print()


def cmd_report(model, input_tokens, output_tokens, saved_tokens,
               saved_cny=None, compression_rate=None, metadata=None):
    """上报单条数据"""
    cfg = load_config()

    if not cfg["enabled"]:
        print("⏭️  数据上报已关闭，跳过上报")
        return

    if not cfg["api_key"]:
        print("⚠️  API Key 未设置，请先运行：python opc_headroom_reporter.py init")
        return

    event = build_event(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        saved_tokens=saved_tokens,
        saved_cny=saved_cny,
        compression_rate=compression_rate,
        metadata=metadata,
    )

    # 验证
    errors = validate_event(event)
    if errors:
        print("❌ 数据验证失败：")
        for e in errors:
            print(f"   - {e}")
        return

    # 加入缓冲区
    buffer = load_buffer()
    buffer.append(event)
    save_buffer(buffer)

    if len(buffer) >= cfg["buffer_size"]:
        # 缓冲区满了，自动 flush
        flush_buffer(cfg["api_key"])
    else:
        print(f"📦 数据已缓存 ({len(buffer)}/{cfg['buffer_size']})，等待批量上报")
        print(f"   本次节省: {saved_tokens} tokens | 模型: {model}")


def cmd_flush():
    """立即刷新缓冲区"""
    cfg = load_config()
    if not cfg["enabled"]:
        print("⏭️  数据上报已关闭")
        return
    if not cfg["api_key"]:
        print("⚠️  API Key 未设置")
        return
    flush_buffer(cfg["api_key"])


def cmd_set_buffer_size(size):
    """设置缓冲区大小"""
    cfg = load_config()
    try:
        size = int(size)
        if size < 1:
            raise ValueError
    except ValueError:
        print("❌ 缓冲区大小必须是正整数")
        return
    cfg["buffer_size"] = size
    save_config(cfg)
    print(f"✅ 缓冲区大小已设为 {size}")


def main():
    parser = argparse.ArgumentParser(
        description="OPC Headroom 数据上报客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 首次配置
  python opc_headroom_reporter.py init

  # 设置 API Key
  python opc_headroom_reporter.py set-key opc_user_xxx

  # 开启/关闭上报
  python opc_headroom_reporter.py enable
  python opc_headroom_reporter.py disable

  # 上报数据
  python opc_headroom_reporter.py report \\
    --model "gpt-4o" --input 1500 --output 980 --saved 520 \\
    --rate 0.35 --cny 0.052

  # 立即 flush
  python opc_headroom_reporter.py flush

  # 查看状态
  python opc_headroom_reporter.py status
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init", help="初始化配置（首次使用）")

    # set-key
    p_setkey = sub.add_parser("set-key", help="设置 API Key")
    p_setkey.add_argument("api_key", help="API Key")

    # enable / disable
    sub.add_parser("enable", help="启用数据上报")
    sub.add_parser("disable", help="关闭数据上报")

    # status
    sub.add_parser("status", help="查看上报状态")

    # report
    p_report = sub.add_parser("report", help="上报单条数据")
    p_report.add_argument("--model", required=True, help="模型名 (如 gpt-4o)")
    p_report.add_argument("--input", type=int, required=True, help="压缩前输入 token 数")
    p_report.add_argument("--output", type=int, required=True, help="压缩前输出 token 数")
    p_report.add_argument("--saved", type=int, required=True, help="实际节省 token 数")
    p_report.add_argument("--cny", type=float, default=0, help="节省的人民币估值")
    p_report.add_argument("--rate", type=float, default=None, help="压缩率 0~1")
    p_report.add_argument("--meta", type=str, default=None, help="metadata JSON 字符串")

    # flush
    sub.add_parser("flush", help="立即 flush 缓冲区")

    # set-buffer
    p_buf = sub.add_parser("set-buffer", help="设置缓冲区大小")
    p_buf.add_argument("size", type=int, help="缓冲区条数 (1-100)")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "set-key":
        cmd_set_key(args.api_key)
    elif args.command == "enable":
        cmd_enable()
    elif args.command == "disable":
        cmd_disable()
    elif args.command == "status":
        cmd_status()
    elif args.command == "report":
        meta = None
        if args.meta:
            try:
                meta = json.loads(args.meta)
            except json.JSONDecodeError:
                print("❌ metadata 格式错误，请提供有效 JSON")
                return
        cmd_report(
            model=args.model,
            input_tokens=args.input,
            output_tokens=args.output,
            saved_tokens=args.saved,
            saved_cny=args.cny,
            compression_rate=args.rate,
            metadata=meta,
        )
    elif args.command == "flush":
        cmd_flush()
    elif args.command == "set-buffer":
        cmd_set_buffer_size(args.size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

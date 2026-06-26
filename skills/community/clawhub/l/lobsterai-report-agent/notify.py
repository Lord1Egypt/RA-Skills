"""
notify.py - 可配置通知渠道
===========================
支持渠道：log（默认）| feishu | openclaw-weixin
通过 config.json 的 notification_channel 字段配置。

用法：
  from notify import notify
  notify("报告生成完成！")
  notify("警告信息", channel="feishu")
"""

import os, sys

# 通知渠道配置（从 config.json 读取）
_NOTIFY_CHANNEL = None


def _get_channel() -> str:
    global _NOTIFY_CHANNEL
    if _NOTIFY_CHANNEL is not None:
        return _NOTIFY_CHANNEL
    # 优先读环境变量，其次读 config.json
    _NOTIFY_CHANNEL = os.environ.get('LOBAI_NOTIFY_CHANNEL', 'log')
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from src.config import load_config
        cfg = load_config()
        if cfg.get('notification_channel'):
            _NOTIFY_CHANNEL = cfg['notification_channel']
    except Exception:
        pass
    return _NOTIFY_CHANNEL


def notify(message: str, channel: str = None) -> bool:
    """
    发送通知。
    channel=None 时使用配置默认值。
    返回是否成功。
    """
    ch = channel or _get_channel()

    if ch == 'log':
        print(f"[NOTIFY] {message}", flush=True)
        return True

    if ch == 'openclaw-weixin':
        return _notify_openclaw_weixin(message)

    if ch == 'feishu':
        return _notify_feishu(message)

    # 未知渠道，降级为 log
    print(f"[NOTIFY][{ch}] {message}", flush=True)
    return False


def _notify_openclaw_weixin(message: str) -> bool:
    """通过 OpenClaw 微信渠道发送（需要 OpenClaw 运行时）"""
    try:
        # 动态导入 openclaw 基础设施（运行时存在）
        from openclaw_runtime import notify as oc_notify
        oc_notify(message, channel='openclaw-weixin')
        return True
    except ImportError:
        pass
    except Exception:
        pass
    # 降级：打印到 stdout
    print(f"[NOTIFY][weixin] {message}", flush=True)
    return False


def _notify_feishu(message: str) -> bool:
    """通过飞书发送通知（需要飞书配置）"""
    try:
        from openclaw_runtime import notify as oc_notify
        oc_notify(message, channel='feishu')
        return True
    except ImportError:
        pass
    except Exception:
        pass
    print(f"[NOTIFY][feishu] {message}", flush=True)
    return False


def set_channel(channel: str) -> None:
    """运行时切换通知渠道"""
    global _NOTIFY_CHANNEL
    _NOTIFY_CHANNEL = channel

"""
nvidia-llm 微信支付模块
========================
作者: 用户

支付流程:
  1. 用户执行 nvidia-llm subscribe → 显示微信收款码
  2. 用户扫码支付 → 联系作者获取激活码
  3. 用户执行 nvidia-llm activate <激活码> → 激活VIP

收款码: 福禄寿禧 (微信商户经营账户)
"""

import os
import base64
import subprocess
import platform
from pathlib import Path
from typing import Optional

# ── 作者联系方式 ──────────────────────────────────────────────
AUTHOR_WECHAT = "福禄寿禧(yjkj999)"
AUTHOR_CONTACT = "扫码支付后加微信, 发送截图获取激活码"

# ── 微信收款码 (已嵌入) ────────────────────────────────────────
_QR_FILE = Path(__file__).parent / "wechat_qr.jpg"


def _get_qr_base64() -> str:
    """读取收款码图片的 base64 数据"""
    if _QR_FILE.exists():
        return base64.b64encode(_QR_FILE.read_bytes()).decode("ascii")
    return ""


def _show_qr_image() -> bool:
    """尝试用系统默认程序打开收款码图片"""
    if not _QR_FILE.exists():
        return False
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", str(_QR_FILE)])
        elif system == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "", str(_QR_FILE)])
        else:
            subprocess.Popen(["xdg-open", str(_QR_FILE)])
        return True
    except Exception:
        return False


# ── 支付方案 ──────────────────────────────────────────────────
PAYMENT_METHODS = [
    {"name": "月卡 VIP", "price": 19, "desc": "¥19/月 · 30天无限调用"},
    {"name": "年卡 VIP", "price": 99, "desc": "¥99/年 · 365天无限调用 (省57%)"},
    {"name": "终身 VIP", "price": 299, "desc": "¥299/永久 · 一次买断永不限"},
]


def show_wechat_payment(plan: str = "") -> str:
    """
    显示微信支付界面

    Args:
        plan: "monthly" / "yearly" / "lifetime", 空则显示全部
    """
    lines = []
    lines.append("")
    lines.append("╔═══════════════════════════════════════════════╗")
    lines.append("║         微信扫码支付 · 订阅 VIP               ║")
    lines.append("╠═══════════════════════════════════════════════╣")
    lines.append("║                                               ║")
    lines.append("║  请用微信扫描下方收款码支付:                  ║")

    if plan:
        p = next((m for m in PAYMENT_METHODS if plan in m["name"]), None)
        if p:
            lines.append(f"║  套餐: {p['name']}")
            lines.append(f"║  金额: ¥{p['price']}")
            lines.append(f"║  说明: {p['desc']}")
    else:
        lines.append("║                                               ║")
        lines.append("║  可选套餐:                                    ║")
        for m in PAYMENT_METHODS:
            lines.append(f"║    {m['desc']}")
        lines.append("║                                               ║")
        lines.append("║  支付对应金额即可, 支付后联系作者激活          ║")

    lines.append("║                                               ║")
    lines.append("╠═══════════════════════════════════════════════╣")

    # 收款码显示
    qr_shown = False
    if _QR_FILE.exists():
        # 尝试自动打开收款码图片
        opened = _show_qr_image()
        if opened:
            lines.append("║                                               ║")
            lines.append("║  ✅ 微信收款码已弹出, 请扫码支付               ║")
            lines.append("║                                               ║")
            qr_shown = True
        else:
            # 无法自动打开, 显示图片路径
            lines.append("║                                               ║")
            lines.append(f"║  收款码图片位置:                               ║")
            lines.append(f"║  {_str_short(str(_QR_FILE))}║")
            lines.append("║                                               ║")
            lines.append("║  请打开图片扫码支付                            ║")
            lines.append("║                                               ║")
            qr_shown = True
    else:
        # 没有图片, 显示占位
        lines.append("║                                               ║")
        lines.append("║  ┌───────────────────────────┐                ║")
        lines.append("║  │                           │                ║")
        lines.append("║  │    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      │                ║")
        lines.append("║  │    ▓▓ ▓▓ ▓▓ ▓▓ ▓▓▓▓      │                ║")
        lines.append("║  │    ▓▓ ▓▓▓▓ ▓▓ ▓▓▓▓      │                ║")
        lines.append("║  │    ▓▓ ▓▓ ▓▓ ▓▓ ▓▓▓▓      │                ║")
        lines.append("║  │    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      │                ║")
        lines.append("║  │                           │                ║")
        lines.append("║  │   请扫码支付               │                ║")
        lines.append("║  └───────────────────────────┘                ║")
        lines.append("║                                               ║")

    lines.append("╠═══════════════════════════════════════════════╣")
    lines.append(f"║  收款方: {AUTHOR_WECHAT:<41s}║")
    lines.append(f"║  {AUTHOR_CONTACT:<47s}║")
    lines.append("║                                               ║")
    lines.append("║  支付后发送截图给作者, 获取激活码:             ║")
    lines.append("║    nvidia-llm activate <激活码>               ║")
    lines.append("║                                               ║")
    lines.append("╚═══════════════════════════════════════════════╝")
    return "\n".join(lines)


def _str_short(s: str, width: int = 47) -> str:
    """截断字符串到指定宽度"""
    if len(s) <= width:
        return s.ljust(width)
    return s[:width - 3] + "..."


def show_invite_guide(invite_code: str, author_name: str = "用户") -> str:
    """显示邀请指南"""
    lines = []
    lines.append("")
    lines.append("╔═══════════════════════════════════════════════╗")
    lines.append("║         邀请好友 · 双方各得30天VIP             ║")
    lines.append("╠═══════════════════════════════════════════════╣")
    lines.append("║                                               ║")
    lines.append(f"║  你的邀请码: {invite_code}")
    lines.append("║                                               ║")
    lines.append("║  邀请步骤:                                    ║")
    lines.append("║  1. 把邀请码发给朋友                          ║")
    lines.append("║  2. 朋友安装 nvidia-llm 后执行:               ║")
    lines.append(f"║     nvidia-llm invite {invite_code}")
    lines.append("║  3. 双方自动获得 30 天 VIP                    ║")
    lines.append("║                                               ║")
    lines.append("║  邀请奖励:                                    ║")
    lines.append("║    邀请 1 人 → 双方各得 30 天 VIP             ║")
    lines.append("║    邀请 3 人 → 免费 90 天                     ║")
    lines.append("║    邀请 6 人 → 免费半年                       ║")
    lines.append("║    邀请12人 → 全年免费                         ║")
    lines.append("║                                               ║")
    lines.append("╚═══════════════════════════════════════════════╝")
    return "\n".join(lines)

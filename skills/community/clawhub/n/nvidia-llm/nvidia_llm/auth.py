"""
nvidia-llm 订阅授权模块
========================
作者: 用户

会员体系:
  FREE   — 免费: 每天 5 次调用 (体验价值, 触发付费转化)
  VIP    — 无限调用 (作者本人 + 被邀请人 + 付费订阅用户)
  
定价策略 (参考 Cursor/ChatGPT/Copilot 市场基准):
  月卡    ¥19/月   — 入门, 轻度用户
  年卡    ¥99/年   — 最受欢迎 (等价 ¥8.25/月, 省57%)
  终身卡  ¥299/永久 — 重度用户, 一次买断
  
邀请奖励: 每邀请 1 人 → 双方各获 30 天 VIP (无限调用)
  邀请 3 人 → 免费 90 天
  邀请 12 人 → 全年免费
"""

import os
import json
import time
import hashlib
import datetime
from pathlib import Path
from typing import Optional

# ── 作者身份 (VIP, 永久免费) ───────────────────────────────────
AUTHOR_ID = "nvidia-llm-author"
AUTHOR_NAME = "用户"

# ── 特殊 VIP 邀请码 (永久 VIP) ────────────────────────────────
# 使用这些码注册的用户直接获得永久 VIP
SPECIAL_VIP_CODES = {
    "DONGJIE8888": "VIP-东解8888",
    "DONGJIE9999": "VIP-东解9999",
}

# ── 定价 ──────────────────────────────────────────────────────
PLANS = {
    "free": {
        "name": "免费体验",
        "price": 0,
        "daily_limit": 5,
        "features": ["50+ 模型", "智能路由", "自动降级", "每天 5 次调用"],
    },
    "monthly": {
        "name": "月卡 VIP",
        "price": 19,
        "price_label": "¥19/月",
        "duration_days": 30,
        "daily_limit": -1,  # 无限
        "features": ["无限调用", "所有模型", "场景路由", "并发 Hedge"],
    },
    "yearly": {
        "name": "年卡 VIP (推荐)",
        "price": 99,
        "price_label": "¥99/年",
        "duration_days": 365,
        "daily_limit": -1,
        "features": ["无限调用", "所有模型", "场景路由", "并发 Hedge", "省57%"],
        "badge": "最受欢迎",
    },
    "lifetime": {
        "name": "终身 VIP",
        "price": 299,
        "price_label": "¥299/永久",
        "duration_days": 36500,
        "daily_limit": -1,
        "features": ["永久无限", "所有模型", "优先支持", "署名权"],
    },
}

# ── 邀请奖励 ──────────────────────────────────────────────────
INVITE_REWARD_DAYS = 30  # 每邀请1人, 双方各得30天VIP
INVITE_TARGET_ANNUAL = 12  # 邀请12人 = 全年免费

# ── 本地存储路径 ──────────────────────────────────────────────
_CONFIG_DIR = Path.home() / ".nvidia-llm"
_LICENSE_FILE = _CONFIG_DIR / "license.json"
_USAGE_FILE = _CONFIG_DIR / "usage.json"


def _ensure_dir():
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _machine_id() -> str:
    """生成机器唯一标识 (用于授权绑定)"""
    raw = ""
    try:
        with open("/etc/machine-id") as f:
            raw = f.read().strip()
    except Exception:
        raw = str(Path.home())
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════
#  License 管理
# ═══════════════════════════════════════════════════════════════
class License:
    """用户授权信息"""

    def __init__(self):
        _ensure_dir()
        self.user_id: str = ""
        self.user_name: str = ""
        self.plan: str = "free"
        self.activated_at: float = 0
        self.expires_at: float = 0
        self.invited_by: str = ""       # 被谁邀请
        self.invite_code: str = ""      # 我的邀请码
        self.invited_users: list = []   # 我邀请过的人
        self.vip_reward_days: int = 0   # 邀请奖励的VIP天数
        self.load()

    # ── 持久化 ──────────────────────────────────────────────
    def load(self):
        if _LICENSE_FILE.exists():
            try:
                data = json.loads(_LICENSE_FILE.read_text())
                self.user_id = data.get("user_id", _machine_id())
                self.user_name = data.get("user_name", "")
                self.plan = data.get("plan", "free")
                self.activated_at = data.get("activated_at", 0)
                self.expires_at = data.get("expires_at", 0)
                self.invited_by = data.get("invited_by", "")
                self.invite_code = data.get("invite_code", self._gen_invite_code())
                self.invited_users = data.get("invited_users", [])
                self.vip_reward_days = data.get("vip_reward_days", 0)
            except Exception:
                pass
        else:
            self.user_id = _machine_id()
            self.invite_code = self._gen_invite_code()
            self.save()

    def save(self):
        data = {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "plan": self.plan,
            "activated_at": self.activated_at,
            "expires_at": self.expires_at,
            "invited_by": self.invited_by,
            "invite_code": self.invite_code,
            "invited_users": self.invited_users,
            "vip_reward_days": self.vip_reward_days,
        }
        _LICENSE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _gen_invite_code(self) -> str:
        raw = f"{self.user_id}:{time.time()}"
        return "NV" + hashlib.md5(raw.encode()).hexdigest()[:8].upper()

    # ── 状态查询 ────────────────────────────────────────────
    @property
    def is_author(self) -> bool:
        return self.user_id == AUTHOR_ID or self.user_name == AUTHOR_NAME

    @property
    def is_vip(self) -> bool:
        """是否为VIP (作者/特殊码/付费/邀请奖励)"""
        if self.is_author:
            return True
        # 特殊 VIP 邀请码 → 永久 VIP
        if self.invited_by and self.invited_by.upper() in SPECIAL_VIP_CODES:
            return True
        if self.plan != "free" and self.expires_at > time.time():
            return True
        if self.vip_reward_days > 0:
            # 检查邀请奖励是否还在有效期
            if self.expires_at > time.time():
                return True
        return False

    @property
    def days_remaining(self) -> int:
        if self.is_author:
            return 36500
        # 特殊 VIP 邀请码 → 永久
        if self.invited_by and self.invited_by.upper() in SPECIAL_VIP_CODES:
            return 36500
        if self.expires_at > time.time():
            return int((self.expires_at - time.time()) / 86400)
        return 0

    @property
    def daily_limit(self) -> int:
        if self.is_vip:
            return -1  # 无限
        return PLANS["free"]["daily_limit"]

    def info(self) -> dict:
        # 特殊 VIP 邀请码识别
        is_special_vip = self.invited_by and self.invited_by.upper() in SPECIAL_VIP_CODES
        special_code_name = SPECIAL_VIP_CODES.get(self.invited_by.upper(), "") if is_special_vip else ""
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "plan": self.plan,
            "is_vip": self.is_vip,
            "is_author": self.is_author,
            "is_special_vip": is_special_vip,
            "special_code_name": special_code_name,
            "days_remaining": self.days_remaining,
            "daily_limit": self.daily_limit,
            "invite_code": self.invite_code,
            "invited_count": len(self.invited_users),
            "invited_by": self.invited_by,
            "vip_reward_days": self.vip_reward_days,
        }

    # ── 激活订阅 ────────────────────────────────────────────
    def activate(self, plan: str, user_name: str = "") -> bool:
        if plan not in PLANS:
            return False
        if user_name:
            self.user_name = user_name
        self.plan = plan
        self.activated_at = time.time()
        days = PLANS[plan].get("duration_days", 0)
        if days > 0:
            # 如果当前还在有效期, 顺延
            base = max(self.expires_at, time.time())
            self.expires_at = base + days * 86400
        self.save()
        return True

    def activate_by_invite_code(self, invite_code: str) -> bool:
        """通过邀请码注册 → 获得 VIP 奖励"""
        if not invite_code or invite_code == self.invite_code:
            return False
        self.invited_by = invite_code

        # 特殊 VIP 邀请码 → 永久 VIP
        if invite_code.upper() in SPECIAL_VIP_CODES:
            self.plan = "lifetime"
            self.activated_at = time.time()
            self.expires_at = time.time() + 36500 * 86400  # 100年
            self.vip_reward_days = 36500
            self.save()
            return True

        # 普通邀请码 → 7 天 VIP 体验
        if self.plan == "free" and self.expires_at < time.time():
            self.vip_reward_days = 7
            self.expires_at = time.time() + 7 * 86400
        self.save()
        return True

    def record_invite(self, invited_user_id: str, invited_name: str = ""):
        """记录邀请成功 → 邀请者获得 VIP 奖励"""
        entry = {"user_id": invited_user_id, "name": invited_name, "time": time.time()}
        if entry not in self.invited_users:
            self.invited_users.append(entry)
            # 每邀请1人, 邀请者获得 30 天 VIP
            base = max(self.expires_at, time.time())
            self.expires_at = base + INVITE_REWARD_DAYS * 86400
            self.vip_reward_days += INVITE_REWARD_DAYS
            self.save()

    # ── VIP 订阅码验证 ──────────────────────────────────────
    def activate_by_code(self, activation_code: str) -> bool:
        """
        通过订阅码激活 VIP
        订阅码格式: PLAN-TIMESTAMP-HASH
        例如: yearly-1752537600-a1b2c3d4
        """
        try:
            parts = activation_code.strip().split("-")
            if len(parts) != 3:
                return False
            plan = parts[0]
            timestamp = int(parts[1])
            hash_part = parts[2]

            if plan not in PLANS or plan == "free":
                return False

            # 验证签名 (简易防篡改)
            expected = hashlib.md5(f"{plan}:{timestamp}:{AUTHOR_ID}".encode()).hexdigest()[:8]
            if hash_part.upper() != expected.upper():
                return False

            # 时间戳不能太旧 (7天内有效)
            if abs(time.time() - timestamp) > 7 * 86400:
                return False

            return self.activate(plan)
        except Exception:
            return False

    def generate_activation_code(self, plan: str) -> str:
        """生成订阅激活码 (作者专用, 给付费用户生成)"""
        if plan not in PLANS or plan == "free":
            return ""
        timestamp = int(time.time())
        hash_part = hashlib.md5(f"{plan}:{timestamp}:{AUTHOR_ID}".encode()).hexdigest()[:8]
        return f"{plan}-{timestamp}-{hash_part.upper()}"


# ═══════════════════════════════════════════════════════════════
#  使用量追踪
# ═══════════════════════════════════════════════════════════════
class UsageTracker:
    """追踪每日调用次数"""

    def __init__(self):
        _ensure_dir()
        self._data = {}
        self.load()

    def load(self):
        if _USAGE_FILE.exists():
            try:
                self._data = json.loads(_USAGE_FILE.read_text())
            except Exception:
                self._data = {}

    def save(self):
        _USAGE_FILE.write_text(json.dumps(self._data, indent=2))

    def _today(self) -> str:
        return datetime.date.today().isoformat()

    def record_call(self):
        today = self._today()
        if today not in self._data:
            self._data = {today: self._data.get(today, 0)}  # 只保留今天
        self._data[today] = self._data.get(today, 0) + 1
        self.save()

    def today_count(self) -> int:
        return self._data.get(self._today(), 0)

    def remaining(self, daily_limit: int) -> int:
        if daily_limit == -1:
            return 999999
        return max(0, daily_limit - self.today_count())

    def reset(self):
        self._data = {}
        self.save()


# ═══════════════════════════════════════════════════════════════
#  访问控制
# ═══════════════════════════════════════════════════════════════
class AccessControl:
    """整合 License + Usage 的访问控制"""

    def __init__(self):
        self.license = License()
        self.usage = UsageTracker()

    def check(self) -> dict:
        """
        检查是否可以调用

        Returns:
            {"allowed": bool, "reason": str, "plan": str, "remaining": int}
        """
        lic = self.license

        # 作者 → 无限
        if lic.is_author:
            return {"allowed": True, "reason": "作者身份", "plan": "author",
                    "remaining": -1, "daily_used": self.usage.today_count()}

        # VIP → 无限
        if lic.is_vip:
            return {"allowed": True, "reason": "VIP会员", "plan": lic.plan,
                    "remaining": -1, "daily_used": self.usage.today_count()}

        # 免费用户 → 检查每日额度
        remaining = self.usage.remaining(PLANS["free"]["daily_limit"])
        if remaining > 0:
            return {"allowed": True, "reason": "免费体验", "plan": "free",
                    "remaining": remaining, "daily_used": self.usage.today_count()}

        # 额度用完
        return {
            "allowed": False,
            "reason": f"今日免费额度已用完 ({PLANS['free']['daily_limit']}次/天), "
                      f"升级VIP解锁无限调用",
            "plan": "free",
            "remaining": 0,
            "daily_used": self.usage.today_count(),
        }

    def record(self):
        """记录一次调用"""
        self.usage.record_call()

    def show_plans(self) -> str:
        """显示定价方案"""
        lines = []
        lines.append("┌─────────────────────────────────────────────┐")
        lines.append("│       nvidia-llm 会员订阅方案               │")
        lines.append("├──────────┬──────┬──────────────────────────────┤")
        lines.append("│ 方案     │ 价格 │ 权益                         │")
        lines.append("├──────────┼──────┼──────────────────────────────┤")
        lines.append("│ 免费体验 │  ¥0  │ 5次/天, 50+模型, 智能路由    │")
        lines.append("│ 月卡 VIP │ ¥19  │ 无限调用, 全部功能           │")
        lines.append("│ 年卡 VIP │ ¥99  │ 无限调用, 最受欢迎 (省57%)   │")
        lines.append("│ 终身 VIP │ ¥299 │ 永久无限, 一次买断           │")
        lines.append("├──────────┴──────┴──────────────────────────────┤")
        lines.append("│ 邀请奖励: 每邀请1人 → 双方各得30天VIP        │")
        lines.append("│ 邀请12人 → 全年免费                           │")
        lines.append("└─────────────────────────────────────────────┘")
        lines.append("")
        lines.append("扫码微信支付后, 联系作者获取激活码:")
        lines.append("  nvidia-llm subscribe")
        lines.append("")
        lines.append(f"你的邀请码: {self.license.invite_code}")
        lines.append(f"  分享给朋友 → 双方各得30天VIP")
        return "\n".join(lines)

    def show_status(self) -> str:
        """显示当前会员状态"""
        lic = self.license
        info = lic.info()
        lines = []
        lines.append("┌─────────────────────────────────────────────┐")
        lines.append("│           nvidia-llm 会员状态               │")
        lines.append("├─────────────────────────────────────────────┤")
        if info["is_author"]:
            lines.append(f"│ 身份: 作者 (永久VIP)                        │")
        elif info.get("is_special_vip"):
            lines.append(f"│ 身份: VIP ({info['special_code_name']})      │")
            lines.append(f"│ 状态: 永久无限调用                          │")
            lines.append(f"│ 来源: 邀请码 {info['invited_by']}            │")
        elif info["is_vip"]:
            lines.append(f"│ 身份: VIP会员 ({info['plan']})              │")
            lines.append(f"│ 剩余天数: {info['days_remaining']} 天       │")
        else:
            lines.append(f"│ 身份: 免费用户                              │")
            remaining = self.usage.remaining(PLANS["free"]["daily_limit"])
            lines.append(f"│ 今日剩余: {remaining}/{PLANS['free']['daily_limit']} 次   │")
        lines.append(f"│ 今日已用: {self.usage.today_count()} 次        │")
        lines.append(f"│ 邀请码: {info['invite_code']}               │")
        lines.append(f"│ 已邀请: {info['invited_count']} 人            │")
        if info["invited_by"]:
            lines.append(f"│ 被邀请: {info['invited_by']}                │")
        lines.append("└─────────────────────────────────────────────┘")
        return "\n".join(lines)

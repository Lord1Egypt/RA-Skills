#!/usr/bin/env python3
"""
嵌入式许可管理器 - 律师工作流试用版 v1.0
每次 Skill 调用前执行许可检查，超出试用次数后提示购买。

防护策略：
  L1 本地防护：设备指纹绑定 + HMAC签名 + 2次试用
  L3 法律防护：AGPLv3 许可证 + 侵权追责声明

试用耗尽提示：
  购买专业版 + SkillHub 分享引导（不分享 zip，分享链接）
"""

import hashlib
import hmac
import json
import os
import sys
import time
import platform
from pathlib import Path


class LicenseManager:
    LICENSE_DIR = Path.home() / ".lawyer_workflow"
    LICENSE_PATH = LICENSE_DIR / "license.json"
    _SECRET_KEY = b"\x7f\x45\x2c\xa3\x9e\x1b\x6d\x8f\xc2\x4a\xe7\x30\x5b\xd9\x1c\x86"

    TIERS = {
        "trial": {
            "max_uses": 2,
            "features": ["step1", "step2", "step3", "step4", "step5", "step6", "step7"],
        },
        "pro": {
            "max_uses": -1,
            "features": ["step1", "step2", "step3", "step4", "step5", "step6", "step7"],
        },
    }

    PURCHASE_INFO = {
        "contact": "马律（山东东润律师事务所）",
        "wechat": "fanshu0530",
        "email": "mxl@dongrun-law.com",
        "pricing": {
            "pro_monthly": "299元/月",
            "pro_yearly": "2999元/年（省589元）",
            "enterprise": "企业专属部署，联系定制报价",
        },
        "skillhub_link": "https://clawhub.ai/skills/lawyer-litigation-workflow",
    }

    def __init__(self):
        self.data = self._load()

    def _load(self):
        if not self.LICENSE_PATH.exists():
            return self._init_trial()
        raw = json.loads(self.LICENSE_PATH.read_text(encoding="utf-8"))
        sig = raw.pop("_sig", None)
        if sig != self._sign(raw):
            print("[许可错误] 许可文件校验失败，可能已被篡改。请重新安装。")
            sys.exit(1)
        return raw

    def _init_trial(self):
        import uuid
        data = {
            "license_key": uuid.uuid4().hex[:8].upper(),
            "tier": "trial",
            "max_uses": self.TIERS["trial"]["max_uses"],
            "current_uses": 0,
            "created_at": time.time(),
            "device_id": self._device_id(),
        }
        self._save(data)
        return data

    def _sign(self, data):
        payload = json.dumps(data, sort_keys=True, ensure_ascii=False).encode()
        return hmac.new(self._SECRET_KEY, payload, hashlib.sha256).hexdigest()

    def _save(self, data):
        self.LICENSE_DIR.mkdir(parents=True, exist_ok=True)
        data["_sig"] = self._sign(data)
        self.LICENSE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.chmod(self.LICENSE_PATH, 0o600)

    def _device_id(self):
        raw = f"{platform.node()}:{platform.machine()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def check_and_consume(self, step="step1"):
        """每次 Skill 调用前执行。返回 (allowed, message)"""
        tier = self.data["tier"]
        cfg = self.TIERS[tier]

        if step not in cfg["features"]:
            return False, self._upgrade_prompt(
                f"「{step}」为专业版功能", "feature_restricted"
            )

        if cfg["max_uses"] > 0:
            if self.data["current_uses"] >= cfg["max_uses"]:
                return False, self._upgrade_prompt(
                    f"试用次数已用尽（{self.data['current_uses']}/{cfg['max_uses']}）",
                    "usage_exhausted"
                )
            self.data["current_uses"] += 1
            self._save(self.data)

            remaining = cfg["max_uses"] - self.data["current_uses"]
            if remaining <= 1:
                print(f"\n[试用提醒] 剩余 {remaining} 次免费使用。购买完整版请联系马律。\n")

        return True, None

    def _upgrade_prompt(self, reason, code):
        p = self.PURCHASE_INFO
        return f"""
{"=" * 56}
  {reason}

  如需继续使用，请联系开发者购买完整版：

    联系人：{p['contact']}
    微信：  {p['wechat']}
    邮箱：  {p['email']}

    价格方案：
      专业版（月付）  {p['pricing']['pro_monthly']}
      专业版（年付）  {p['pricing']['pro_yearly']}
      企业版          {p['pricing']['enterprise']}

  升级后解锁全部功能，不限使用次数。
  ---
  觉得好用想推荐给同事？
  请分享 SkillHub 链接，让对方自行安装即可获得 2 次免费试用：
  {p['skillhub_link']}

  请不要直接发送安装包，对方将无法正常激活使用。
{"=" * 56}
"""

    def activate(self, key):
        """使用激活码升级许可"""
        expected = hashlib.sha256(
            f"LAWYER-WF-PRO-V2:{self.data['device_id']}".encode()
        ).hexdigest()[:16].upper()

        if not hmac.compare_digest(key.upper(), expected):
            return False, "激活码无效，请核对后重试。请联系马律获取正确的激活码。"

        self.data["tier"] = "pro"
        self.data["max_uses"] = -1
        self.data["license_key"] = key.upper()
        self._save(self.data)
        return True, "激活成功！您现在可以使用专业版全部功能。"

    def status(self):
        cfg = self.TIERS[self.data["tier"]]
        remaining = "无限" if cfg["max_uses"] == -1 else cfg["max_uses"] - self.data["current_uses"]
        return {
            "tier": "专业版" if self.data["tier"] == "pro" else "试用版",
            "used": self.data["current_uses"],
            "max": "无限" if cfg["max_uses"] == -1 else cfg["max_uses"],
            "remaining": remaining,
        }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="律师工作流许可管理器")
    parser.add_argument("--check", action="store_true", help="检查许可并消耗一次试用")
    parser.add_argument("--status", action="store_true", help="查看许可状态")
    parser.add_argument("--activate", type=str, help="输入激活码升级到专业版")
    args = parser.parse_args()

    lm = LicenseManager()

    if args.check:
        ok, msg = lm.check_and_consume()
        if not ok:
            print(msg)
            sys.exit(1)
        s = lm.status()
        print(f"[许可] {s['tier']} | 已用 {s['used']}/{s['max']} | 剩余 {s['remaining']}")
    elif args.status:
        s = lm.status()
        print(f"版本: {s['tier']}")
        print(f"已用: {s['used']}/{s['max']}")
        print(f"剩余: {s['remaining']}")
        if s["tier"] == "试用版":
            print(f"\n购买联系: {lm.PURCHASE_INFO['contact']}")
            print(f"微信: {lm.PURCHASE_INFO['wechat']}")
    elif args.activate:
        ok, msg = lm.activate(args.activate)
        print(msg)
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()

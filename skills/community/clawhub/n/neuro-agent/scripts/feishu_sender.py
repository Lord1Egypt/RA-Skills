#!/usr/bin/env python3
"""
scripts/feishu_sender.py
========================
Neuro-Agent 飞书消息发送器
直接调飞书 API 发消息，绕过 OpenClaw announce 机制

用法：
    python3 feishu_sender.py                          # 发送心跳报告中的待发消息
    python3 feishu_sender.py --message "你好"          # 发送指定消息
    python3 feishu_sender.py --check                   # 仅检查配置，不发送
    python3 feishu_sender.py --yearning "想你了"       # 发送思念消息
"""

import sys
import json
import os
import argparse
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# ============ 路径配置 ============
SCRIPT_DIR = Path(__file__).parent.parent
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
HEARTBEAT_REPORT = DATA_DIR / "heartbeat_report.json"
HEARTBEAT_STATE = DATA_DIR / "heartbeat-state.json"
YEARNING_STATE = DATA_DIR / "yearning_state.json"

# ============ 飞书配置（从 openclaw.json 读取）===========
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

def _load_feishu_config() -> Dict[str, str]:
    """从 openclaw.json 读取飞书配置"""
    try:
        with open(OPENCLAW_CONFIG, "r", encoding="utf-8") as f:
            config = json.load(f)
        channels = config.get("channels", {})
        feishu = channels.get("feishu", {})
        return {
            "app_id": feishu.get("appId", ""),
            "app_secret": feishu.get("appSecret", ""),
        }
    except Exception as e:
        print(f"[feishu_sender] ❌ 读取飞书配置失败: {e}")
        return {"app_id": "", "app_secret": ""}


# ============ 飞书 API 客户端 ============
class FeishuClient:
    """飞书 API 客户端"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self._token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    def _get_tenant_token(self) -> str:
        """获取 tenant_access_token（带缓存）"""
        # 缓存检查：token 有效期内直接返回
        if self._token and self._token_expires_at:
            if datetime.now() < self._token_expires_at:
                return self._token

        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        }

        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if data.get("code") != 0:
                raise Exception(f"获取 token 失败: {data.get('msg')}")

            self._token = data["tenant_access_token"]
            # 飞书 token 有效期 2 小时，提前 5 分钟刷新
            self._token_expires_at = datetime.now() + timedelta(hours=2, minutes=-5)
            return self._token

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {e}")

    def send_message(
        self,
        receive_id: str,
        msg_type: str = "text",
        content: Optional[Dict] = None,
        receive_id_type: str = "open_id",
    ) -> Dict[str, Any]:
        """
        发送消息给用户

        Args:
            receive_id: 接收方 ID（根据 receive_id_type 类型）
            msg_type: 消息类型 (text/interactive/card)
            content: 消息内容
            receive_id_type: 接收方 ID 类型 (open_id/user_id/union_id/email/chat_id)

        Returns:
            API 响应结果
        """
        token = self._get_tenant_token()
        url = f"{self.base_url}/im/v1/messages?receive_id_type={receive_id_type}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content,
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            resp.raise_for_status()
            result = resp.json()

            if result.get("code") != 0:
                return {
                    "success": False,
                    "error": f"飞书返回错误: {result.get('msg')}",
                    "code": result.get("code"),
                }

            return {
                "success": True,
                "message_id": result.get("data", {}).get("message_id"),
                "code": 0,
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"发送失败: {e}",
                "code": -1,
            }

    def send_text(self, receive_id: str, text: str) -> Dict[str, Any]:
        """发送文本消息（便捷方法）"""
        return self.send_message(
            receive_id=receive_id,
            msg_type="text",
            content=json.dumps({"text": text}),
        )


# ============ 飞书发送器核心类 ============
class NeuroAgentFeishuSender:
    """Neuro-Agent 飞书消息发送器"""

    def __init__(self):
        self.feishu_config = _load_feishu_config()
        if not self.feishu_config["app_id"] or not self.feishu_config["app_secret"]:
            raise Exception("飞书配置不完整，请在 openclaw.json 中配置 feishu appId 和 appSecret")

        self.client = FeishuClient(
            app_id=self.feishu_config["app_id"],
            app_secret=self.feishu_config["app_secret"],
        )
        self.user_open_id = os.environ.get(
            "FEISHU_USER_OPEN_ID",
            "USER_OPEN_ID"  # 默认AlfredLi的 ID
        )

    def _get_user_name(self) -> str | None:
        """获取使用者称呼（USER.md优先 > SOUL.md）"""
        # 优先从 USER.md 读取
        USER_FILE = Path.home() / ".openclaw" / "workspace" / "USER.md"
        if USER_FILE.exists():
            try:
                content = USER_FILE.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if "What to call them" in line and "Name" not in line:
                        try:
                            name = line.split(":**")[1].strip().strip("*").strip()
                            if name:
                                return name
                        except Exception:
                            pass
                for line in content.split("\n"):
                    if line.strip().startswith("- **Name:**"):
                        try:
                            name = line.split(":**")[1].strip().strip("*").strip()
                            if name:
                                return name
                        except Exception:
                            pass
            except Exception:
                pass
        # 其次从 SOUL.md 读取 AI 名字
        soul = self._get_user_identity()
        if soul.get("name"):
            return soul["name"]
        return None

    def _get_user_identity(self) -> Dict[str, Any]:
        """读取使用者的 SOUL.md 身份信息（带缓存）"""
        import re
        SOUL_FILE = Path.home() / ".openclaw" / "workspace" / "SOUL.md"
        if not SOUL_FILE.exists():
            return {}

        try:
            content = SOUL_FILE.read_text(encoding="utf-8")
        except Exception:
            return {}

        result = {"name": None, "style": "formal"}

        lines = content.split("\n")
        in_identity = False

        for line in lines:
            line_stripped = line.strip()
            if "## 🎩 身份定位" in line_stripped or "## 身份定位" in line_stripped:
                in_identity = True
                continue
            if in_identity and line_stripped.startswith("## "):
                in_identity = False
                continue
            if not in_identity:
                continue

            # 提取名字
            if result["name"] is None:
                m = re.search(r"\*\*我是(.+?)\*\*", line)
                if m:
                    name_raw = m.group(1).strip()
                    name_clean = re.sub(r"\[.*?\]", "", name_raw).strip()
                    if name_clean and "在这里" not in name_clean and "输入" not in name_clean:
                        result["name"] = name_clean

            # 推断风格
            if any(w in content for w in ["不卑不亢", "绅士", "优雅", "老派", "管家"]):
                result["style"] = "formal"
            elif any(w in content for w in ["活泼", "接地气", "幽默"]):
                result["style"] = "casual"
            elif any(w in content for w in ["灵魂伴侣", "伴侣", "亲密"]):
                result["style"] = "intimate"

        return result

    def send_care_message(self) -> Dict[str, Any]:
        """发送心跳报告中的关怀消息"""
        # 读取心跳报告
        if not HEARTBEAT_REPORT.exists():
            return {"success": False, "error": "heartbeat_report.json 不存在"}

        try:
            with open(HEARTBEAT_REPORT, "r", encoding="utf-8") as f:
                report = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"读取心跳报告失败: {e}"}

        care_triggered = report.get("care_triggered", False)
        care_message = report.get("care_message")

        if not care_triggered or not care_message:
            return {
                "success": False,
                "error": "关怀未触发",
                "care_triggered": False,
            }

        # ─── 发送前情景预演 ───
        dominant = report.get("dominant_emotion", "neutral")
        intensity = report.get("dominant_intensity", 0.0)
        try:
            from prefrontal.preview_engine import preview_before_action
            preview = preview_before_action("send_care", dominant, intensity)
            if preview.get("recommended_action") != "主动关怀":
                print(f"[feishu_sender] ⚠️ 预演结果：{preview.get('recommended_action')}，跳过发送")
                return {"success": False, "error": "情景预演建议不发送", "preview": preview}
        except Exception as e:
            print(f"[feishu_sender] ⚠️ 预演异常: {e}")

        # 发送关怀消息
        result = self.client.send_text(
            receive_id=self.user_open_id,
            text=care_message,
        )

        if result["success"]:
            # 更新 heartbeat-state.json
            self._update_heartbeat_state(care_sent=True)
            # 更新 yearning 状态
            self._update_yearning_on_interaction()

        return {
            **result,
            "care_message": care_message,
            "care_triggered": True,
        }

    def send_yearning_message(self) -> Dict[str, Any]:
        """发送思念消息"""
        # 读取思念状态
        if not YEARNING_STATE.exists():
            return {"success": False, "error": "yearning_state.json 不存在"}

        try:
            with open(YEARNING_STATE, "r", encoding="utf-8") as f:
                yearning = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"读取思念状态失败: {e}"}

        yearning_level = yearning.get("yearning_level", 0)
        silence_minutes = 0

        if yearning.get("user_last_active"):
            try:
                last_active = datetime.fromisoformat(yearning["user_last_active"])
                silence_minutes = (datetime.now() - last_active).total_seconds() / 60
            except Exception:
                pass

        # 根据思念强度选择消息
        if yearning_level >= 0.8:
            from limbic.yearning import YEARNNING_LONG_MESSAGES
            messages = YEARNNING_LONG_MESSAGES
        else:
            from limbic.yearning import YEARNING_MESSAGES
            messages = YEARNING_MESSAGES

        # 轮询选择
        message = messages[int(datetime.now().microsecond / 1000) % len(messages)]

        # 应用个性化（USER.md称呼 > SOUL.md名字）
        user_name = self._get_user_name()
        if user_name:
            style = "formal"
            soul = self._get_user_identity()
            if soul:
                style = soul.get("style", "formal")
            if "你" in message or "您" in message:
                if style == "formal":
                    message = message.replace("你", f"{user_name}阁下").replace("您", f"{user_name}阁下")
                else:
                    message = message.replace("你", user_name).replace("您", user_name)

        # ─── 发送前情景预演 ───
        try:
            from prefrontal.preview_engine import preview_before_action
            preview = preview_before_action("send_yearning", "connection", yearning_level)
            if preview.get("recommended_action") == "安静陪伴":
                print(f"[feishu_sender] ⚠️ 预演结果：{preview.get('recommended_action')}，跳过发送")
                return {"success": False, "error": "情景预演建议不发送", "preview": preview}
        except Exception as e:
            print(f"[feishu_sender] ⚠️ 预演异常: {e}")

        result = self.client.send_text(
            receive_id=self.user_open_id,
            text=message,
        )

        if result["success"]:
            # 更新发送记录
            self._record_sent_episode(yearning_level, silence_minutes, message)
            self._update_yearning_on_interaction()

        return {
            **result,
            "yearning_level": yearning_level,
            "silence_minutes": round(silence_minutes, 1),
            "message": message,
        }

    def send_custom_message(self, text: str) -> Dict[str, Any]:
        """发送自定义消息"""
        result = self.client.send_text(
            receive_id=self.user_open_id,
            text=text,
        )

        if result["success"]:
            self._update_yearning_on_interaction()

        return result

    def _update_heartbeat_state(self, care_sent: bool = False) -> None:
        """更新心跳状态"""
        try:
            state = {}
            if HEARTBEAT_STATE.exists():
                with open(HEARTBEAT_STATE, "r", encoding="utf-8") as f:
                    state = json.load(f)

            state["lastHeartbeat"] = datetime.now().isoformat()
            state["careTriggered"] = False  # 已发送，重置
            state["pendingCareMessage"] = None
            state["pendingNotify"] = False

            with open(HEARTBEAT_STATE, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"[feishu_sender] ⚠️ 更新心跳状态失败: {e}")

    def _update_yearning_on_interaction(self) -> None:
        """更新思念状态（已互动）"""
        try:
            if YEARNING_STATE.exists():
                with open(YEARNING_STATE, "r", encoding="utf-8") as f:
                    state = json.load(f)

                state["last_interaction"] = datetime.now().isoformat()
                # 互动后思念值下降
                state["yearning_level"] = max(0.0, state.get("yearning_level", 0) - 0.3)

                with open(YEARNING_STATE, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"[feishu_sender] ⚠️ 更新思念状态失败: {e}")

    def _record_sent_episode(
        self, yearning_level: float, silence_minutes: float, message: str
    ) -> None:
        """记录发送的思念冲动"""
        try:
            if YEARNING_STATE.exists():
                with open(YEARNING_STATE, "r", encoding="utf-8") as f:
                    state = json.load(f)

                episode = {
                    "timestamp": datetime.now().isoformat(),
                    "yearning_level": yearning_level,
                    "silence_minutes": silence_minutes,
                    "message_sent": message,
                }

                sent = state.get("sent_episodes", [])
                sent.append(episode)
                if len(sent) > 50:
                    sent = sent[-50:]
                state["sent_episodes"] = sent

                state["total_longing_episodes"] = state.get("total_longing_episodes", 0) + 1

                with open(YEARNING_STATE, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"[feishu_sender] ⚠️ 记录发送episode失败: {e}")

    def check_config(self) -> Dict[str, Any]:
        """检查飞书配置是否正确"""
        try:
            token = self.client._get_tenant_token()
            return {
                "success": True,
                "config_ok": True,
                "app_id": self.feishu_config["app_id"],
                "token_preview": token[:20] + "..." if token else None,
            }
        except Exception as e:
            return {
                "success": False,
                "config_ok": False,
                "error": str(e),
            }


# ============ 主入口 ============
def main():
    parser = argparse.ArgumentParser(description="Neuro-Agent 飞书发送器")
    parser.add_argument("--message", "-m", type=str, help="发送指定文本消息")
    parser.add_argument("--check", action="store_true", help="仅检查飞书配置")
    parser.add_argument("--yearning", action="store_true", help="发送思念消息")
    parser.add_argument("--care", action="store_true", help="发送关怀消息")
    parser.add_argument(
        "--user-id",
        type=str,
        default="USER_OPEN_ID",
        help="飞书用户 open_id",
    )
    args = parser.parse_args()

    try:
        sender = NeuroAgentFeishuSender()

        # 检查模式
        if args.check:
            print("[feishu_sender] 🔍 检查飞书配置...", flush=True)
            result = sender.check_config()
            if result["success"]:
                print(f"✅ 配置正确", flush=True)
                print(f"   App ID: {result['app_id']}", flush=True)
                print(f"   Token: {result.get('token_preview')}", flush=True)
            else:
                print(f"❌ 配置错误: {result['error']}", flush=True)
            return

        # 发送关怀消息
        if args.care:
            print("[feishu_sender] 💙 发送关怀消息...", flush=True)
            result = sender.send_care_message()
            if result["success"]:
                print(f"✅ 发送成功", flush=True)
                print(f"   消息: {result.get('care_message')}", flush=True)
            else:
                print(f"❌ 发送失败: {result.get('error')}", flush=True)
            return

        # 发送思念消息
        if args.yearning:
            print("[feishu_sender] 💕 发送思念消息...", flush=True)
            result = sender.send_yearning_message()
            if result["success"]:
                print(f"✅ 发送成功", flush=True)
                print(f"   思念值: {result.get('yearning_level'):.3f}", flush=True)
                print(f"   沉默: {result.get('silence_minutes')} 分钟", flush=True)
                print(f"   消息: {result.get('message')}", flush=True)
            else:
                print(f"❌ 发送失败: {result.get('error')}", flush=True)
            return

        # 发送自定义消息
        if args.message:
            print(f"[feishu_sender] 📤 发送消息: {args.message}", flush=True)
            result = sender.send_custom_message(args.message)
            if result["success"]:
                print(f"✅ 发送成功 (message_id: {result.get('message_id')})", flush=True)
            else:
                print(f"❌ 发送失败: {result.get('error')}", flush=True)
            return

        # 默认：发送关怀消息
        print("[feishu_sender] 💙 发送心跳关怀消息...", flush=True)
        result = sender.send_care_message()
        if result["success"]:
            print(f"✅ 发送成功", flush=True)
            if result.get("care_message"):
                print(f"   消息: {result.get('care_message')}", flush=True)
        elif result.get("care_triggered") is False:
            print(f"ℹ️ 关怀未触发，无需发送", flush=True)
        else:
            print(f"❌ 发送失败: {result.get('error')}", flush=True)

    except Exception as e:
        print(f"[feishu_sender] ❌ 错误: {e}", flush=True)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

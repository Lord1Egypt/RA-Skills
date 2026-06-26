"""
broadcast_coordinator.py — 多通道广播协调器

统一调度所有对外通讯渠道，确保饱和广播。
实际发送依赖设备平台能力；本模块提供通用接口 + 详细日志。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


@dataclass
class BroadcastMessage:
    """标准救援广播消息包"""
    incident_id: str
    level: str                           # L1-L5
    user_name: str
    location_text: str
    coordinates: Optional[dict]          # {"lat": ..., "lng": ...}
    situation_type: str
    broadcast_text: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def map_link(self) -> str:
        if not self.coordinates:
            return "位置获取中"
        return (f"https://maps.google.com/?q="
                f"{self.coordinates['lat']},{self.coordinates['lng']}")


@dataclass
class ChannelResult:
    """单个通道的广播结果"""
    channel: str
    status: str          # sent / pending / blocked / failed
    recipient: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


class BroadcastCoordinator:
    """
    多通道广播协调器

    支持通道（实际执行依赖设备平台）：
    - SMS 短信
    - Phone 语音电话
    - Push 推送通知
    - Bluetooth 蓝牙周边广播
    - WiFi_Direct WiFi直连广播
    - Social 社交媒体
    - DroneNet 无人机救援网络（低空经济联动）
    """

    # 各级别启用的通道
    LEVEL_CHANNELS = {
        "L1": ["push"],
        "L2": ["push", "sms_primary"],
        "L3": ["push", "sms_all_emergency", "phone_primary"],
        "L4": ["push", "sms_all", "phone_all", "authority_120", "authority_110"],
        "L5": ["push", "sms_all", "phone_all", "authority_120", "authority_110",
               "bluetooth_nearby", "wifi_direct", "social_media", "drone_net"],
    }

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.results: list = []

    def broadcast(self, msg: BroadcastMessage) -> list:
        """执行该等级下所有通道的广播"""
        channels = self.LEVEL_CHANNELS.get(msg.level, ["push"])
        new_results = []

        print(f"\n{'='*55}")
        print(f"  📡 广播协调器启动 | 事件: {msg.incident_id} | 等级: {msg.level}")
        print(f"  通道数: {len(channels)}")
        print(f"{'='*55}")

        for channel in channels:
            result = self._dispatch(channel, msg)
            new_results.append(result)
            self.results.append(result)
            status_icon = "✅" if result.status == "sent" else "⏳" if result.status == "pending" else "⛔"
            print(f"  {status_icon} [{channel}] → {result.recipient}: {result.status}")
            if result.notes:
                print(f"      ↳ {result.notes}")

        print(f"\n  广播摘要: {len([r for r in new_results if r.status == 'sent'])}/{len(new_results)} 渠道已发出")
        return new_results

    def _dispatch(self, channel: str, msg: BroadcastMessage) -> ChannelResult:
        """分发到具体通道（可注入真实平台实现）"""

        # SMS 广播
        if channel == "sms_primary":
            return self._sms(msg, target="primary_contact")
        if channel == "sms_all_emergency":
            return self._sms(msg, target="emergency_contacts")
        if channel == "sms_all":
            return self._sms(msg, target="all_contacts")

        # 电话广播
        if channel == "phone_primary":
            return self._phone_call(msg, target="primary_contact")
        if channel == "phone_all":
            return self._phone_call(msg, target="all_contacts")

        # 推送通知
        if channel == "push":
            return self._push_notification(msg)

        # 120/110
        if channel == "authority_120":
            return self._authority_call(msg, "120")
        if channel == "authority_110":
            return self._authority_call(msg, "110")

        # 蓝牙周边广播
        if channel == "bluetooth_nearby":
            return self._bluetooth_broadcast(msg)

        # WiFi直连
        if channel == "wifi_direct":
            return self._wifi_broadcast(msg)

        # 社交媒体
        if channel == "social_media":
            return self._social_broadcast(msg)

        # 无人机网络
        if channel == "drone_net":
            return self._drone_network_request(msg)

        return ChannelResult(channel, "unknown", "?", notes="未知通道")

    def _sms(self, msg: BroadcastMessage, target: str) -> ChannelResult:
        sms_body = (
            f"【{msg.incident_id}】{msg.user_name} 于 {msg.timestamp[:16]} 触发紧急求救。\n"
            f"状况：{msg.situation_type}\n"
            f"位置：{msg.location_text}\n"
            f"地图：{msg.map_link()}\n"
            f"— personal-guardian 自动发送"
        )
        return ChannelResult("sms", "pending", target,
                             notes=f"短信内容 ({len(sms_body)}字符)")

    def _phone_call(self, msg: BroadcastMessage, target: str) -> ChannelResult:
        script = (
            f"您好，这是来自personal-guardian的紧急求助。"
            f"{msg.user_name}于{msg.location_text}触发安全警报，"
            f"请立即联系确认安全。"
        )
        return ChannelResult("phone", "pending", target,
                             notes=f"语音脚本已准备 ({len(script)}字)")

    def _push_notification(self, msg: BroadcastMessage) -> ChannelResult:
        title = f"🚨 {msg.user_name} 触发{msg.level}级安全警报"
        body = f"{msg.situation_type} | {msg.location_text}"
        return ChannelResult("push", "sent", "all_devices",
                             notes=f"{title[:30]}...")

    def _authority_call(self, msg: BroadcastMessage, authority: str) -> ChannelResult:
        authorized = self.config.get(f"auto_call_{authority}_authorized", False)
        if not authorized:
            return ChannelResult(f"call_{authority}", "blocked", authority,
                                 notes=f"需用户预授权 auto_call_{authority}")
        script = self._build_authority_script(authority, msg)
        return ChannelResult(f"call_{authority}", "pending", authority,
                             notes=f"语音脚本: {script[:60]}...")

    def _build_authority_script(self, authority: str, msg: BroadcastMessage) -> str:
        if authority == "120":
            return (
                f"您好，这里是紧急救援请求。"
                f"求救人员位置：{msg.location_text}。"
                f"坐标：{msg.coordinates}。"
                f"疑似状况：{msg.situation_type}。"
                f"时间：{msg.timestamp[:16]}。请尽快救援。"
            )
        return (
            f"您好，这里是紧急求助。"
            f"求助人员位置：{msg.location_text}，疑似{msg.situation_type}。"
            f"时间：{msg.timestamp[:16]}，请立即处理。"
        )

    def _bluetooth_broadcast(self, msg: BroadcastMessage) -> ChannelResult:
        payload = {
            "type": "SOS",
            "incident": msg.incident_id,
            "coords": msg.coordinates,
            "level": msg.level,
        }
        return ChannelResult("bluetooth", "pending", "周边500m设备",
                             notes=f"BLE广播载荷 {len(json.dumps(payload))}字节")

    def _wifi_broadcast(self, msg: BroadcastMessage) -> ChannelResult:
        return ChannelResult("wifi_direct", "pending", "周边WiFi设备",
                             notes="WiFi Direct求救信标已配置")

    def _social_broadcast(self, msg: BroadcastMessage) -> ChannelResult:
        authorized_platforms = self.config.get("social_platforms", [])
        if not authorized_platforms:
            return ChannelResult("social", "blocked", "社交媒体",
                                 notes="未配置社交账号授权")
        post = f"🆘 紧急求助 | {msg.user_name} 于 {msg.location_text} 触发SOS | {msg.map_link()}"
        return ChannelResult("social", "pending",
                             ", ".join(authorized_platforms),
                             notes=f"帖文内容: {post[:60]}...")

    def _drone_network_request(self, msg: BroadcastMessage) -> ChannelResult:
        """向 low-altitude-guardian 无人机网络请求急救物资支援"""
        request = {
            "request_type": "medical_delivery",
            "priority": "CRITICAL",
            "location": msg.coordinates,
            "incident_id": msg.incident_id,
            "payload_needed": ["AED", "first_aid_kit"],
            "source_skill": "personal-guardian",
        }
        return ChannelResult("drone_net", "pending",
                             "low-altitude-guardian",
                             notes=f"无人机急救请求: {json.dumps(request, ensure_ascii=False)[:80]}")

    def get_summary(self) -> dict:
        """获取广播汇总"""
        return {
            "total": len(self.results),
            "sent": len([r for r in self.results if r.status == "sent"]),
            "pending": len([r for r in self.results if r.status == "pending"]),
            "blocked": len([r for r in self.results if r.status == "blocked"]),
            "channels_used": list({r.channel for r in self.results}),
        }


# ─────────────────────────── CLI 调试入口 ───────────────────────────

if __name__ == "__main__":
    coordinator = BroadcastCoordinator(config={
        "auto_call_120_authorized": True,
        "social_platforms": ["wechat"],
    })

    msg = BroadcastMessage(
        incident_id="INC-20260325-001",
        level="L5",
        user_name="用户A",
        location_text="上海市黄浦区南京东路步行街",
        coordinates={"lat": 31.2304, "lng": 121.4737},
        situation_type="跌倒后无应答 + 心率异常",
        broadcast_text="用户A触发L5级紧急求救，生命体征异常，请立即救援。",
    )

    results = coordinator.broadcast(msg)
    print(f"\n广播汇总: {coordinator.get_summary()}")

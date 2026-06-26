# -*- coding: utf-8 -*-
import sys as _sys
if _sys.platform == "win32":
    try:
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

"""
personal-rescue-agent
action_executor.py — 饱和执行引擎

根据 L1-L5 等级自主执行对应的救援行动，
包括：录音启动、定位广播、联系人通知、120/110 呼叫。
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Optional

# ============================================================
# 联系人配置（示例 — 实际从用户配置读取）
# ============================================================

DEFAULT_CONTACTS = [
    {"name": "母亲", "phone": "+86-138-0000-0000", "priority": 1, "relationship": "family"},
    {"name": "挚友小明", "phone": "+86-139-0000-0000", "priority": 2, "relationship": "friend"},
    {"name": "同事老王", "phone": "+86-137-0000-0000", "priority": 3, "relationship": "colleague"},
]

AUTHORITY_CONFIG = {
    "120": {"name": "急救中心", "auto_call": False, "auth_required": True},
    "110": {"name": "报警电话", "auto_call": False, "auth_required": True},
}

# ============================================================
# 执行状态
# ============================================================

class ExecutionStatus:
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABORTED = "aborted"


class RescueExecutor:
    """饱和执行引擎"""

    def __init__(self, incident_id: str, level: str, config: dict = None):
        self.incident_id = incident_id
        self.level = level
        self.config = config or {}
        self.status = ExecutionStatus.IDLE
        self.actions_log = []
        self.contacts = self.config.get("contacts", DEFAULT_CONTACTS)
        self.authority_config = self.config.get("authorities", AUTHORITY_CONFIG)

    # ----------------------------------------------------------
    # 录音管理
    # ----------------------------------------------------------

    def start_audio_recording(self, duration_seconds: Optional[int] = None) -> dict:
        """启动环境录音"""
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "start_audio_recording",
            "level": "L3+",
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "details": {
                "duration_seconds": duration_seconds,
                "sample_rate": "16kHz",
                "format": "opus",
                "storage": "local_encrypted",
            },
        }
        self.actions_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] 🎙️ 录音已启动（预计 {duration_seconds or '持续'} 秒）")
        return log_entry

    def stop_audio_recording(self) -> dict:
        """停止录音"""
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "stop_audio_recording",
            "level": "L3+",
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "details": {
                "file_path": f".guardian/incidents/{self.incident_id}/audio_latest.opus",
                "duration_actual_seconds": None,  # 实际时长待记录
            },
        }
        self.actions_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] 🎙️ 录音已停止，等待文件封存")
        return log_entry

    # ----------------------------------------------------------
    # 定位管理
    # ----------------------------------------------------------

    def start_location_tracking(self, interval_seconds: int = 30) -> dict:
        """启动高频位置追踪"""
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "start_location_tracking",
            "level": "L2+",
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "details": {
                "interval_seconds": interval_seconds,
                "sources": ["gps", "wifi", "cell"],
                "precision_target": "high",
            },
        }
        self.actions_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] 📍 位置追踪已启动（间隔 {interval_seconds}s）")
        return log_entry

    def get_current_location(self) -> dict:
        """获取当前位置（模拟）"""
        return {
            "coordinates": {"lat": 31.2304, "lng": 121.4737},
            "precision": "high",
            "description": "上海市黄浦区南京东路步行街",
            "altitude": 4.2,
            "timestamp": datetime.now().isoformat(),
        }

    def broadcast_location(self, location: dict, recipient: str = "all") -> dict:
        """广播位置信息"""
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "broadcast_location",
            "level": "L2+",
            "timestamp": datetime.now().isoformat(),
            "status": "broadcasting",
            "details": {
                "recipient": recipient,
                "map_link": f"https://maps.google.com/?q={location['coordinates']['lat']},{location['coordinates']['lng']}",
                "location_snapshot": location,
            },
        }
        self.actions_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] 📡 位置已广播至 {recipient}")
        return log_entry

    # ----------------------------------------------------------
    # 联系人通知
    # ----------------------------------------------------------

    def build_rescue_message(self, location: dict, situation: dict) -> str:
        """构建标准救援信息包"""
        return f"""【紧急救援请求】
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
位置：{location['description']}
坐标：{location['coordinates']['lat']},{location['coordinates']['lng']}
地图：https://maps.google.com/?q={location['coordinates']['lat']},{location['coordinates']['lng']}
状况：{situation.get('type', '未知')}
触发：{situation.get('trigger', '安全时刻')}
请立即：{situation.get('recommended_action', '联系用户确认安全或呼叫急救')}

—— personal-rescue-agent 自动发送"""

    def notify_contact(self, contact: dict, message: str, attempt: int = 1) -> dict:
        """通知单个联系人"""
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "notify_contact",
            "level": "L2+",
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "details": {
                "contact_name": contact["name"],
                "contact_phone": contact["phone"],
                "relationship": contact.get("relationship", "unknown"),
                "attempt": attempt,
                "message_preview": message[:50] + "...",
            },
        }
        self.actions_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] 📞 正在通知: {contact['name']} ({contact['phone']}) [{attempt}/{3}]")
        # 模拟发送
        return log_entry

    def notify_emergency_contacts(self, level: str, location: dict, situation: dict) -> list:
        """按优先级通知紧急联系人"""
        message = self.build_rescue_message(location, situation)
        notified = []
        pending_contacts = self.contacts[:]

        if level in ["L4", "L5"]:
            # L4+ 全饱和通知
            priority_count = len(pending_contacts)
        elif level == "L3":
            # L3 通知前2人
            priority_count = 2
        else:
            # L1-L2 仅通知第一人
            priority_count = 1

        for contact in pending_contacts[:priority_count]:
            self.notify_contact(contact, message)
            notified.append(contact["name"])

        print(f"[{datetime.now().isoformat()}] 👥 已通知 {len(notified)}/{len(pending_contacts)} 位紧急联系人: {', '.join(notified)}")
        return notified

    # ----------------------------------------------------------
    # 120/110 自主呼叫（L4+，需授权）
    # ----------------------------------------------------------

    def call_authority(self, authority: str, location: dict, situation: dict) -> dict:
        """呼叫急救/报警"""
        if authority not in ["120", "110"]:
            raise ValueError(f"Unknown authority: {authority}")

        info = self.authority_config.get(authority, {})
        if info.get("auth_required") and not self.config.get(f"auto_call_{authority}_authorized"):
            log_entry = {
                "seq": len(self.actions_log) + 1,
                "action": f"call_{authority}",
                "level": "L4+",
                "timestamp": datetime.now().isoformat(),
                "status": "blocked_need_auth",
                "reason": "auto_call 未授权，请在用户配置中授权",
            }
            self.actions_log.append(log_entry)
            print(f"[{log_entry['timestamp']}] ⛔ 呼叫 {authority} 被阻止：未获得用户授权")
            return log_entry

        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": f"call_{authority}",
            "level": "L4+",
            "timestamp": datetime.now().isoformat(),
            "status": "dialing",
            "details": {
                "authority": authority,
                "location": location,
                "situation": situation,
                "voice_message": self.build_voice_script(authority, location, situation),
            },
        }
        self.actions_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] 🚨 正在呼叫 {authority} {info.get('name', '')}...")
        print(f"        语音内容：{log_entry['details']['voice_message']}")
        return log_entry

    def build_voice_script(self, authority: str, location: dict, situation: dict) -> str:
        """构建语音呼叫脚本"""
        if authority == "120":
            return (
                f"您好，这里是紧急救援请求。"
                f"求救人员位置：{location['coordinates']['lat']}纬度，{location['coordinates']['lng']}经度，"
                f"位于{location['description']}。"
                f"疑似状况：{situation.get('type', '未知紧急情况')}。"
                f"求救时间：{datetime.now().strftime('%Y年%m月%d日%H时%M分')}。"
                f"请尽快救援。"
            )
        elif authority == "110":
            return (
                f"您好，这里是紧急求助。"
                f"求助人员位置：{location['coordinates']['lat']}纬度，{location['coordinates']['lng']}经度，"
                f"位于{location['description']}。"
                f"情况描述：{situation.get('type', '紧急安全威胁')}。"
                f"求助时间：{datetime.now().strftime('%Y年%m月%d日%H时%M分')}。"
                f"请立即处理。"
            )
        return ""

    # ----------------------------------------------------------
    # 主执行流程
    # ----------------------------------------------------------

    def execute(self, situation: dict) -> dict:
        """根据等级执行完整救援流程"""
        self.status = ExecutionStatus.RUNNING
        print(f"\n{'='*60}")
        print(f"  🚨 personal-rescue-agent 执行引擎启动")
        print(f"  🆔 事件ID: {self.incident_id} | 等级: {self.level}")
        print(f"{'='*60}\n")

        # Step 1: 态势评估 + 录音
        if self.level in ["L3", "L4", "L5"]:
            self.start_audio_recording()

        # Step 2: 位置追踪
        interval = 15 if self.level in ["L4", "L5"] else 30
        self.start_location_tracking(interval_seconds=interval)
        current_location = self.get_current_location()
        self.broadcast_location(current_location)

        # Step 3: 联系人通知
        notified = self.notify_emergency_contacts(self.level, current_location, situation)

        # Step 4: 120/110 呼叫（L4+）
        if self.level in ["L4", "L5"]:
            if self.config.get("auto_call_120_authorized"):
                self.call_authority("120", current_location, situation)
            if self.config.get("auto_call_110_authorized"):
                self.call_authority("110", current_location, situation)

        # Step 5: L5 饱和广播
        if self.level == "L5":
            self.execute_saturation_broadcast(current_location, situation)

        self.status = ExecutionStatus.RUNNING  # 保持运行，等待后续状态更新

        return self.get_execution_summary()

    def execute_saturation_broadcast(self, location: dict, situation: dict) -> dict:
        """L5 灾难级：全饱和广播"""
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "saturation_broadcast",
            "level": "L5",
            "timestamp": datetime.now().isoformat(),
            "status": "executing",
            "channels": [
                "emergency_contacts",
                "120",
                "110",
                "nearby_devices_500m",
                "social_media",
                "low_altitude_network",
            ],
            "details": {
                "nearby_radius_meters": 500,
                "social_platforms": ["wechat", "weibo"],
                "drone_aid_requested": True,
            },
        }
        self.actions_log.append(log_entry)
        print(f"\n[{log_entry['timestamp']}] 🌐 L5 饱和广播已触发！")
        print(f"    广播渠道: {', '.join(log_entry['channels'])}")
        print(f"    周边搜索半径: 500m")
        print(f"    低空急救网络: 已请求无人机支援")
        return log_entry

    def resolve(self, outcome: str, notes: str = "") -> dict:
        """事件解决"""
        self.status = ExecutionStatus.COMPLETED
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "incident_resolved",
            "level": "all",
            "timestamp": datetime.now().isoformat(),
            "status": "resolved",
            "details": {
                "outcome": outcome,  # user_recovered | false_alarm | resolved_by_contact | escalated
                "notes": notes,
            },
        }
        self.actions_log.append(log_entry)

        # 停止录音
        self.stop_audio_recording()

        print(f"\n{'='*60}")
        print(f"  ✅ 事件已解决: {outcome}")
        print(f"  📋 行动日志已生成，等待复盘")
        print(f"{'='*60}")
        return self.get_execution_summary()

    def abort(self, reason: str) -> dict:
        """中止执行（用户取消）"""
        self.status = ExecutionStatus.ABORTED
        log_entry = {
            "seq": len(self.actions_log) + 1,
            "action": "execution_aborted",
            "level": "all",
            "timestamp": datetime.now().isoformat(),
            "status": "aborted",
            "reason": reason,
        }
        self.actions_log.append(log_entry)
        self.stop_audio_recording()
        print(f"\n⚠️ 执行已中止: {reason}")
        return self.get_execution_summary()

    def get_execution_summary(self) -> dict:
        """获取执行摘要"""
        return {
            "incident_id": self.incident_id,
            "current_level": self.level,
            "status": self.status,
            "actions_log": self.actions_log,
            "total_actions": len(self.actions_log),
            "completed_actions": len([a for a in self.actions_log if a["status"] in ["completed", "active", "broadcasting", "dialing"]]),
        }


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="personal-rescue-agent — 饱和执行引擎")
    parser.add_argument("--incident-id", default=None, help="事件ID（默认自动生成）")
    parser.add_argument("--level", default="L3", choices=["L1","L2","L3","L4","L5"], help="应急等级")
    parser.add_argument("--simulate", action="store_true", help="模拟执行（不实际发消息/打电话）")
    parser.add_argument("--auto-call-120", action="store_true", help="授权自动拨打120")
    parser.add_argument("--auto-call-110", action="store_true", help="授权自动拨打110")
    parser.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    incident_id = args.incident_id or f"INC-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"

    config = {
        "auto_call_120_authorized": args.auto_call_120,
        "auto_call_110_authorized": args.auto_call_110,
        "simulate": args.simulate,
    }

    situation = {
        "type": "用户摔倒后无应答",
        "trigger": "device_signal:fall_detected",
        "recommended_action": "请立即前往位置或呼叫急救",
    }

    executor = RescueExecutor(incident_id, args.level, config)
    result = executor.execute(situation)

    # 模拟解决
    if args.simulate:
        result = executor.resolve("false_alarm", "用户确认安全（模拟）")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n📊 执行摘要: {result['completed_actions']}/{result['total_actions']} 行动已完成")


if __name__ == "__main__":
    main()

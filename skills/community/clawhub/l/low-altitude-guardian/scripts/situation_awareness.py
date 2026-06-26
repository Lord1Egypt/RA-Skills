"""
态势感知模块 (Situation Awareness Module)

负责：
- 生成结构化态势快照
- 周边环境风险扫描
- 设备状态汇总
- 态势演化趋势分析
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
SNAPSHOTS_DIR = PROJECT_ROOT / ".guardian" / "snapshots"


@dataclass
class DeviceState:
    """设备状态数据。"""
    device_id: str = ""
    device_type: str = ""
    battery_level: float = 100.0
    battery_temp_c: float = 25.0
    battery_voltage: float = 0.0
    motors_status: dict = field(default_factory=dict)
    failed_motors: int = 0
    total_motors: int = 4
    payload_kg: float = 0.0
    payload_description: str = ""


@dataclass
class NavigationState:
    """导航状态数据。"""
    latitude: float = 0.0
    longitude: float = 0.0
    altitude_agl: float = 0.0
    altitude_msl: float = 0.0
    velocity_horizontal: float = 0.0
    velocity_vertical: float = 0.0
    heading: float = 0.0
    ground_speed: float = 0.0
    gps_satellites: int = 0
    gps_hdop: float = 0.0
    gps_available: bool = True
    imu_healthy: bool = True
    barometer_healthy: bool = True
    flight_phase: str = ""  # takeoff/climb/cruise/descent/hover/landing


@dataclass
class CommunicationState:
    """通信状态数据。"""
    rc_link: bool = True
    rc_rssi: int = 0
    data_link_4g: bool = True
    data_link_rssi: int = 0
    wifi_connected: bool = False
    satellite_link: bool = False
    adsb_active: bool = False


@dataclass
class EnvironmentState:
    """环境状态数据。"""
    wind_speed_ms: float = 0.0
    wind_gust_ms: float = 0.0
    wind_direction_deg: float = 0.0
    temperature_c: float = 20.0
    humidity_pct: float = 50.0
    visibility_m: float = 10000.0
    precipitation: str = "none"  # none/light_rain/heavy_rain/snow/hail
    lightning_distance_km: float = -1  # -1表示无雷电
    weather_trend: str = "stable"  # improving/stable/deteriorating


@dataclass
class NearbyThreat:
    """周边威胁。"""
    threat_type: str = ""  # building/crowd/vehicle/aircraft/powerline/restricted_area
    direction_deg: float = 0.0
    distance_m: float = 0.0
    altitude_diff_m: float = 0.0
    risk_level: str = ""  # low/medium/high/critical
    description: str = ""


@dataclass
class LandingOption:
    """备降点选项。"""
    name: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    distance_m: float = 0.0
    bearing_deg: float = 0.0
    surface_type: str = ""  # grass/concrete/water/rooftop/road
    clear_area_m2: float = 0.0
    suitability_score: float = 0.0  # 0-100
    has_people_nearby: bool = False
    description: str = ""


@dataclass
class SituationSnapshot:
    """完整态势快照。"""
    snapshot_id: str = ""
    timestamp: str = ""
    crisis_trigger: str = ""
    device: DeviceState = field(default_factory=DeviceState)
    navigation: NavigationState = field(default_factory=NavigationState)
    communication: CommunicationState = field(default_factory=CommunicationState)
    environment: EnvironmentState = field(default_factory=EnvironmentState)
    nearby_threats: list = field(default_factory=list)
    landing_options: list = field(default_factory=list)
    trends: dict = field(default_factory=dict)
    raw_sensor_data: dict = field(default_factory=dict)


def create_snapshot(crisis_trigger: str = "",
                    device_data: dict = None,
                    nav_data: dict = None,
                    comms_data: dict = None,
                    env_data: dict = None) -> SituationSnapshot:
    """
    创建态势快照。

    在真实系统中，各数据源来自设备遥测、传感器融合和外部数据服务。
    当前实现提供结构化的数据模型和模拟数据支持。
    """
    now = datetime.now(timezone.utc)
    snapshot_id = f"SNAP-{now.strftime('%Y%m%d-%H%M%S')}-{now.microsecond // 1000:03d}"

    snapshot = SituationSnapshot(
        snapshot_id=snapshot_id,
        timestamp=now.isoformat(),
        crisis_trigger=crisis_trigger,
    )

    # 填充设备状态
    if device_data:
        snapshot.device = DeviceState(**{
            k: v for k, v in device_data.items()
            if k in DeviceState.__dataclass_fields__
        })

    # 填充导航状态
    if nav_data:
        snapshot.navigation = NavigationState(**{
            k: v for k, v in nav_data.items()
            if k in NavigationState.__dataclass_fields__
        })

    # 填充通信状态
    if comms_data:
        snapshot.communication = CommunicationState(**{
            k: v for k, v in comms_data.items()
            if k in CommunicationState.__dataclass_fields__
        })

    # 填充环境状态
    if env_data:
        snapshot.environment = EnvironmentState(**{
            k: v for k, v in env_data.items()
            if k in EnvironmentState.__dataclass_fields__
        })

    return snapshot


def flatten_snapshot(snapshot: SituationSnapshot) -> dict:
    """
    将结构化快照扁平化为 crisis_engine 期望的格式。
    """
    flat = {
        "timestamp": snapshot.timestamp,
        "device_id": snapshot.device.device_id,
        "device_type": snapshot.device.device_type,
        "battery_level": snapshot.device.battery_level,
        "altitude_agl": snapshot.navigation.altitude_agl,
        "velocity_horizontal": snapshot.navigation.velocity_horizontal,
        "velocity_vertical": snapshot.navigation.velocity_vertical,
        "heading": snapshot.navigation.heading,
        "gps_available": snapshot.navigation.gps_available,
        "flight_phase": snapshot.navigation.flight_phase,
        "failed_motors": snapshot.device.failed_motors,
        "total_motors": snapshot.device.total_motors,
        "crisis_trigger": snapshot.crisis_trigger,
        "nearby_threats": ", ".join(
            t.description for t in snapshot.nearby_threats
            if isinstance(t, NearbyThreat)
        ) if snapshot.nearby_threats else "",
        "weather": (
            f"风速{snapshot.environment.wind_speed_ms}m/s, "
            f"阵风{snapshot.environment.wind_gust_ms}m/s, "
            f"{snapshot.environment.precipitation}"
        ),
        "comms_status": (
            f"遥控{'正常' if snapshot.communication.rc_link else '断开'}, "
            f"4G{'正常' if snapshot.communication.data_link_4g else '断开'}"
        ),
        "trends": snapshot.trends,
    }
    return flat


def save_snapshot(snapshot: SituationSnapshot, output_path: str = None) -> str:
    """保存快照到文件。"""
    if output_path is None:
        SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = str(SNAPSHOTS_DIR / f"{snapshot.snapshot_id}.json")

    data = asdict(snapshot)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def scan_nearby_environment(lat: float, lon: float, alt: float,
                            radius_m: float = 500) -> dict:
    """
    扫描周边环境（模拟）。

    真实系统中会查询：
    - 地理信息数据库（建筑、道路、水域）
    - 实时交通数据
    - 禁飞区数据库
    - ADS-B 空中交通数据
    - 人口密度热力图
    """
    print(f"[态势感知] 扫描位置 ({lat:.4f}, {lon:.4f}) ALT:{alt}m 周边{radius_m}m")

    result = {
        "scan_radius_m": radius_m,
        "ground_classification": {
            "below": "urban_mixed",  # 正下方地面类型
            "description": "城市混合区域，有道路和建筑",
        },
        "threats_detected": [],
        "landing_options": [],
        "airspace_status": {
            "restricted": False,
            "temporary_restrictions": [],
            "nearby_airports_km": 15.0,
        },
        "population_density": "medium",
    }

    print(f"  下方区域: {result['ground_classification']['description']}")
    print(f"  空域状态: {'受限' if result['airspace_status']['restricted'] else '正常'}")
    print(f"  人口密度: {result['population_density']}")

    return result


# ─── CLI 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 态势感知模块")
    parser.add_argument("--snapshot", action="store_true", help="生成态势快照")
    parser.add_argument("--scan", action="store_true", help="扫描周边环境")
    parser.add_argument("--trigger", type=str, default="", help="危机触发原因")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--demo", action="store_true", help="生成演示快照")

    args = parser.parse_args()

    if args.demo or args.snapshot:
        # 演示/模拟数据
        snapshot = create_snapshot(
            crisis_trigger=args.trigger or "左前电机异常振动，转速下降30%",
            device_data={
                "device_id": "UAV-SH-00142",
                "device_type": "多旋翼无人机",
                "battery_level": 34,
                "battery_temp_c": 38,
                "failed_motors": 1,
                "total_motors": 4,
                "payload_kg": 3.2,
                "payload_description": "快递包裹",
            },
            nav_data={
                "latitude": 31.2304,
                "longitude": 121.4737,
                "altitude_agl": 120,
                "altitude_msl": 124,
                "velocity_horizontal": 15,
                "velocity_vertical": -2,
                "heading": 30,
                "gps_satellites": 12,
                "gps_available": True,
                "flight_phase": "cruise",
            },
            comms_data={
                "rc_link": True,
                "rc_rssi": -65,
                "data_link_4g": True,
                "data_link_rssi": -72,
            },
            env_data={
                "wind_speed_ms": 12,
                "wind_gust_ms": 18,
                "wind_direction_deg": 270,
                "temperature_c": 22,
                "precipitation": "none",
            },
        )

        output_path = save_snapshot(snapshot, args.output)
        print(f"[态势感知] 快照已生成: {output_path}")

        # 输出扁平化版本（供 crisis_engine 使用）
        flat = flatten_snapshot(snapshot)
        flat_path = output_path.replace(".json", "_flat.json")
        with open(flat_path, "w", encoding="utf-8") as f:
            json.dump(flat, f, ensure_ascii=False, indent=2)
        print(f"[态势感知] 扁平化快照: {flat_path}")

    elif args.scan:
        scan_nearby_environment(31.2304, 121.4737, 120)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

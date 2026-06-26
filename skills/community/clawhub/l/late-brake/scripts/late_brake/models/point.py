# -*- coding: utf-8 -*-
"""
Late Brake - Data Point Model
统一内部数据格式 - 数据点定义

遵循 docs/data-format.md 规范
"""

from pydantic import BaseModel, Field
from pydantic import field_serializer
from typing import Optional


class DataPoint(BaseModel):
    """单个GPS采样数据点，包含位置和传感器信息"""

    timestamp: float = Field(
        ...,
        description="相对时间（秒），从记录开始计算"
    )
    latitude: float = Field(
        ...,
        description="纬度 (WGS84)"
    )
    longitude: float = Field(
        ...,
        description="经度 (WGS84)"
    )
    speed: float = Field(
        ...,
        description="瞬时速度 (km/h)"
    )
    distance: float = Field(
        ...,
        description="累计距离（米），从数据记录开始计算"
    )

    # 可选字段
    altitude: Optional[float] = Field(
        None,
        description="海拔高度 (米)"
    )
    g_force_x: Optional[float] = Field(
        None,
        description="横向G值 (左右方向，左正右负)"
    )
    g_force_y: Optional[float] = Field(
        None,
        description="纵向G值 (前后方向，正为加速，负为刹车)"
    )
    g_force_z: Optional[float] = Field(
        None,
        description="垂直G值"
    )
    steering_angle: Optional[float] = Field(
        None,
        description="方向盘角度 (度)，左负右正"
    )
    throttle_position: Optional[float] = Field(
        None,
        description="油门开合度 (0-100%)"
    )
    brake_pressure: Optional[float] = Field(
        None,
        description="刹车压力 (0-100%)"
    )
    rpm: Optional[int] = Field(
        None,
        description="发动机转速 (RPM)"
    )
    gear: Optional[int] = Field(
        None,
        description="当前档位，0=N，1-...=档位"
    )

    model_config = {
        "extra": "forbid",  # 禁止额外字段，保持结构严格
    }

    # 自定义浮点精度序列化，遵循US-0040约定
    @field_serializer('timestamp')
    def serialize_timestamp(self, v: float, info) -> float:
        return round(v, 4)

    @field_serializer('latitude', 'longitude')
    def serialize_latlon(self, v: float, info) -> float:
        return round(v, 7)

    @field_serializer('speed')
    def serialize_speed(self, v: float, info) -> float:
        return round(v, 2)

    @field_serializer('distance')
    def serialize_distance(self, v: float, info) -> float:
        return round(v, 2)

    @field_serializer('altitude')
    def serialize_altitude(self, v: Optional[float], info) -> Optional[float]:
        return round(v, 2) if v is not None else None

    @field_serializer('g_force_x', 'g_force_y', 'g_force_z', 'steering_angle', 'throttle_position', 'brake_pressure')
    def serialize_g_and_controls(self, v: Optional[float], info) -> Optional[float]:
        return round(v, 3) if v is not None else None

# -*- coding: utf-8 -*-
"""
Late Brake - Track Model
赛道数据模型

遵循 docs/track-format.md 规范
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class TrackAnchor(BaseModel):
    """赛道锚点，用于GPS数据匹配"""
    lat: float = Field(..., description="锚点纬度")
    lon: float = Field(..., description="锚点经度")
    radius_m: float = Field(..., description="赛道范围半径")


class TrackSector(BaseModel):
    """赛道分段信息"""
    id: int = Field(..., description="分段ID")
    name: str = Field(..., description="分段名称")
    start_distance_m: float = Field(..., description="分段起点距离赛道起点的距离（米）")
    end_distance_m: float = Field(..., description="分段终点距离赛道起点的距离（米）")
    turns: List[int] = Field(default_factory=list, description="该分段包含的弯道编号列表")


class TrackTurn(BaseModel):
    """单个弯道信息"""
    name: str = Field(..., description="弯道名称（通常为 T{编号}）")
    type: str = Field(..., description="弯道类型：left/right/left-right/right-left 等")
    start_distance_m: float = Field(..., description="弯道起点距离（从赛道起点开始计算，米）")
    apex_distance_m: float = Field(..., description="弯心距离")
    apex_coordinates: List[float] = Field(..., description="弯心GPS坐标 [纬度, 经度]")
    end_distance_m: float = Field(..., description="弯道终点距离（从赛道起点开始计算，米）")
    radius_m: Optional[float] = Field(None, description="弯道半径（米），复合弯道可留空")
    min_speed_target: float = Field(..., description="弯心目标最低时速（公里/小时）")


class Track(BaseModel):
    """赛道元数据完整定义"""

    id: str = Field(..., description="赛道唯一标识")
    name: str = Field(..., description="赛道英文名称")
    full_name: Optional[str] = Field(None, description="赛道完整名称（含中文）")
    location: Optional[str] = Field(None, description="赛道地理位置")
    length_m: float = Field(..., description="赛道总长度（米）")
    turn_count: int = Field(..., description="弯道总数")

    anchor: TrackAnchor = Field(..., description="赛道锚点，用于GPS数据匹配")
    gate: List[List[float]] = Field(..., description="起终点线两个GPS坐标，定义一条线")
    centerline: List[List[float]] = Field(..., description="赛道中心线GPS坐标点数组（按行驶顺序）")

    geofence: Optional[List[List[float]]] = Field(None, description="赛道边界GPS坐标点数组")
    sectors: Optional[List[TrackSector]] = Field(None, description="赛道分段信息")
    turns: Optional[List[TrackTurn]] = Field(None, description="每个弯道的详细信息")

    model_config = {
        "extra": "forbid",
    }

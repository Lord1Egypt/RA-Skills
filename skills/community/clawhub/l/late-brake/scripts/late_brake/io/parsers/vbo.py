# -*- coding: utf-8 -*-
"""
Late Brake - VBO (VBox) Format Parser

解析 RaceChrono Pro 导出的 VBO 格式GPS数据，提取关键信息转换为内部 DataPoint 格式

US-002 验收条件：
1. ✓ 能够解析RaceChrono Pro导出的VBO格式数据文件
2. ✓ 正确提取并转换5个必填字段：timestamp/latitude/longitude/speed
3. ✓ 经纬度转换：原始DDMM.NNNNN格式 → value / 60 → WGS84十进制度
4. ✓ 时间转换：原始HHMMSS.ss → 相对时间（从首个数据点开始计算，单位秒）
5. ✓ 累计距离distance通过GPS坐标差累加计算，单位米
6. ✓ 转换后输出符合内部数据格式规范（docs/data-format.md）的DataPoint列表
7. ✓ 能够跳过开头注释段落，正确处理数据行格式
8. ✓ 在docs/vbo-format.md编写完整格式说明和映射关系文档
9. ✓ sample-data/running/ 目录下的 tianma_0125_1.vbo和tianma_0125_1.nmea两个文件是同一场比赛的，分析结果必须一致
"""

from typing import List, Optional
from geographiclib.geodesic import Geodesic

from late_brake.models import DataPoint


geod = Geodesic.WGS84


def parse_vbo_file(file_path: str) -> Optional[List[DataPoint]]:
    """
    解析VBO格式文件，返回DataPoint列表
    跳过错误和不完整的行，只保留有效数据点
    文件不存在返回 None
    """
    points: List[DataPoint] = []
    start_time: Optional[float] = None
    last_lat: Optional[float] = None
    last_lon: Optional[float] = None
    total_distance: float = 0.0
    in_data_section = False
    column_names: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # 还没进入数据段，先检查段落标记
                if not in_data_section:
                    if line == "[column names]":
                        # 下一行是列名
                        column_names = next(f).strip().split()
                        continue
                    if line == "[data]":
                        # 进入数据段
                        in_data_section = True
                        # 确认必要列存在
                        required = {"time", "lat", "long", "velocity"}
                        if not required.issubset(column_names):
                            missing = required - set(column_names)
                            # 缺少必要字段，无法解析
                            return None
                        continue
                    # 其他头部行跳过
                    continue

                # 数据段，解析当前行
                parts = line.split()
                if len(parts) != len(column_names):
                    # 字段数量不匹配，跳过
                    continue

                # 按列名提取值
                try:
                    # 构建字典
                    row = dict(zip(column_names, parts))

                    # 解析时间
                    time_val = float(row["time"])  # HHMMSS.ss
                    hours = int(time_val / 10000)
                    minutes = int((time_val - hours * 10000) / 100)
                    seconds = time_val - hours * 10000 - minutes * 100
                    total_seconds = hours * 3600 + minutes * 60 + seconds

                    # 相对时间
                    if start_time is None:
                        start_time = total_seconds
                    timestamp = total_seconds - start_time

                    # 解析纬度：单位是分，直接除以60得到度数
                    # VBO 导出纬度：北纬正，南纬负，符号正确
                    lat_val = float(row["lat"])
                    latitude = lat_val / 60.0

                    # 解析经度：单位是分，除以60后符号取反（RaceChrono VBO 导出东经为负，西经为正，需要反转）
                    lon_val = float(row["long"])
                    longitude = -lon_val / 60.0

                    # 解析速度：已经是 km/h，直接使用
                    speed = float(row["velocity"])

                    # 计算累计距离
                    if last_lat is not None and last_lon is not None:
                        result = geod.Inverse(last_lat, last_lon, latitude, longitude)
                        distance_step = result["s12"]
                        total_distance += distance_step
                    else:
                        total_distance = 0.0

                    # 更新上一个点
                    last_lat = latitude
                    last_lon = longitude

                    # 创建数据点
                    point = DataPoint(
                        timestamp=timestamp,
                        latitude=latitude,
                        longitude=longitude,
                        speed=speed,
                        distance=total_distance
                    )
                    points.append(point)

                except (ValueError, KeyError) as e:
                    # 解析错误，跳过这一行
                    continue

        return points if points else None
    except FileNotFoundError:
        return None

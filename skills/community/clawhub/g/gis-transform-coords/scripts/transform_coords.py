#!/usr/bin/env python3
"""
GIS 坐标转换工具 - WGS84 ↔ Web Mercator
支持点、线、面数据的坐标转换
"""

import sys
import json
import argparse
from typing import Dict, List, Any, Optional

try:
    from pyproj import Transformer
except ImportError:
    print("错误：需要安装 pyproj 库")
    print("运行：pip3 install pyproj")
    sys.exit(1)

# WGS84 (EPSG:4326) ↔ Web Mercator (EPSG:3857)
transformer_4326_to_3857 = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
transformer_3857_to_4326 = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)


def transform_point(point: List[float], to_mercator: bool = True) -> List[float]:
    """转换单个点坐标"""
    x, y = point[0], point[1]
    if to_mercator:
        return list(transformer_4326_to_3857.transform(x, y))
    else:
        return list(transformer_3857_to_4326.transform(x, y))


def transform_coords(coords: List[Any], to_mercator: bool = True, geom_type: str = "Point") -> List[Any]:
    """转换坐标数组（支持线、面）"""
    if geom_type == "Point":
        return transform_point(coords, to_mercator)
    elif geom_type in ["LineString", "Polygon"]:
        return [transform_point(pt, to_mercator) for pt in coords]
    elif geom_type == "MultiPoint":
        return [transform_point(pt, to_mercator) for pt in coords]
    elif geom_type == "MultiLineString":
        return [[transform_point(pt, to_mercator) for pt in line] for line in coords]
    elif geom_type == "MultiPolygon":
        return [[[transform_point(pt, to_mercator) for pt in ring] for ring in poly] for poly in coords]
    return coords


def transform_geometry(geom: Dict, to_mercator: bool = True) -> Dict:
    """转换 GeoJSON 几何对象"""
    geom_type = geom.get("type", "Point")
    coords = geom.get("coordinates", [])
    
    new_coords = transform_coords(coords, to_mercator, geom_type)
    
    return {
        "type": geom_type,
        "coordinates": new_coords
    }


def transform_geojson(data: Dict, to_mercator: bool = True) -> Dict:
    """转换完整的 GeoJSON 对象"""
    result = data.copy()
    
    # 处理 Feature
    if data.get("type") == "Feature":
        result["geometry"] = transform_geometry(data.get("geometry", {}), to_mercator)
        return result
    
    # 处理 FeatureCollection
    if data.get("type") == "FeatureCollection":
        result["features"] = [
            {**f, "geometry": transform_geometry(f.get("geometry", {}), to_mercator)}
            for f in data.get("features", [])
        ]
        return result
    
    # 处理纯 Geometry
    if data.get("type") in ["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"]:
        return transform_geometry(data, to_mercator)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="GIS 坐标转换工具 - WGS84 ↔ Web Mercator")
    parser.add_argument("input", help="输入文件路径 (GeoJSON)")
    parser.add_argument("-o", "--output", help="输出文件路径 (默认输出到 stdout)")
    parser.add_argument("-t", "--to", choices=["mercator", "wgs84"], default="mercator",
                       help="转换目标坐标系：mercator (Web Mercator) 或 wgs84 (经纬度)")
    parser.add_argument("--pretty", action="store_true", help="美化输出 JSON")
    
    args = parser.parse_args()
    
    # 读取输入
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误：文件不存在 - {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：无效的 JSON - {e}", file=sys.stderr)
        sys.exit(1)
    
    # 转换
    to_mercator = args.to == "mercator"
    result = transform_geojson(data, to_mercator)
    
    # 输出
    indent = 2 if args.pretty else None
    output = json.dumps(result, ensure_ascii=False, indent=indent)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✓ 转换完成：{args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

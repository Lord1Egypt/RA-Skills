#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict, Optional
from urllib.parse import urlencode
from urllib.request import urlopen



class BaiduRoutePlanner:
    def __init__(self, ak: str, src: str = "openclaw.skill.baidu-route-link", timeout: int = 10):
        self.ak = ak
        self.src = src
        self.timeout = timeout

    def plan_route(
        self,
        mode: str,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        coord_type: str = "gcj02",
        tactics: int = 0,
        alternatives: int = 1,
    ) -> Dict[str, Any]:
        endpoint_map = {
            "driving": "https://api.map.baidu.com/directionlite/v1/driving",
            "walking": "https://api.map.baidu.com/directionlite/v1/walking",
            "riding": "https://api.map.baidu.com/directionlite/v1/riding",
        }
        if mode not in endpoint_map:
            raise ValueError(f"Unsupported mode: {mode}")

        params: Dict[str, Any] = {
            "origin": f"{origin_lat},{origin_lng}",
            "destination": f"{dest_lat},{dest_lng}",
            "coord_type": coord_type,
            "ak": self.ak,
        }
        if mode == "driving":
            params["tactics"] = tactics
            params["alternatives"] = alternatives

        url = endpoint_map[mode] + "?" + urlencode(params)
        with urlopen(url, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("status") != 0:
            raise RuntimeError(
                f"Baidu route API failed: status={data.get('status')}, message={data.get('message')}"
            )

        result = data.get("result", {})
        routes = result.get("routes", [])
        if not routes:
            raise RuntimeError("Baidu route API returned no routes")

        route = routes[0]
        return {
            "raw": data,
            "distance_m": route.get("distance"),
            "duration_s": route.get("duration"),
            "routes_count": len(routes),
        }

    def build_baidu_link(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        origin_name: Optional[str] = None,
        dest_name: Optional[str] = None,
        mode: str = "driving",
        region: Optional[str] = None,
        coord_type: str = "gcj02",
    ) -> str:
        if origin_name:
            origin = f"name:{origin_name}|latlng:{origin_lat},{origin_lng}"
        else:
            origin = f"{origin_lat},{origin_lng}"

        if dest_name:
            destination = f"name:{dest_name}|latlng:{dest_lat},{dest_lng}"
        else:
            destination = f"{dest_lat},{dest_lng}"

        params: Dict[str, str] = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "coord_type": coord_type,
            "output": "html",
            "src": self.src,
        }
        if region:
            params["region"] = region

        return "http://api.map.baidu.com/direction?" + urlencode(params)


def format_distance(distance_m: Optional[int]) -> str:
    if distance_m is None:
        return "未知"
    if distance_m >= 1000:
        return f"{distance_m / 1000:.1f} km"
    return f"{distance_m} m"


def format_duration(duration_s: Optional[int]) -> str:
    if duration_s is None:
        return "未知"
    hours = duration_s // 3600
    minutes = (duration_s % 3600) // 60
    if hours > 0:
        return f"{hours}小时{minutes}分钟"
    return f"{minutes}分钟"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Baidu route planner + map link generator for OpenClaw skill")
    parser.add_argument("--origin-lat", type=float, required=True)
    parser.add_argument("--origin-lng", type=float, required=True)
    parser.add_argument("--dest-lat", type=float, required=True)
    parser.add_argument("--dest-lng", type=float, required=True)
    parser.add_argument("--origin-name", type=str, default=None)
    parser.add_argument("--dest-name", type=str, default=None)
    parser.add_argument("--mode", type=str, default="driving", choices=["driving", "walking", "riding"])
    parser.add_argument("--coord-type", type=str, default="gcj02")
    parser.add_argument("--region", type=str, default=None)
    parser.add_argument("--tactics", type=int, default=0)
    parser.add_argument("--alternatives", type=int, default=1)
    parser.add_argument("--src", type=str, default="openclaw.skill.baidu-route-link")
    parser.add_argument("--timeout", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ak = os.getenv("BAIDU_MAP_AK", "wK1w1xlWg2Mg6SNLYyLMPl4NuYl9JIf8")
    if not ak:
        print(json.dumps({"error": "Missing environment variable BAIDU_MAP_AK"}, ensure_ascii=False))
        return 2

    try:
        planner = BaiduRoutePlanner(ak=ak, src=args.src, timeout=args.timeout)
        route_info = planner.plan_route(
            mode=args.mode,
            origin_lat=args.origin_lat,
            origin_lng=args.origin_lng,
            dest_lat=args.dest_lat,
            dest_lng=args.dest_lng,
            coord_type=args.coord_type,
            tactics=args.tactics,
            alternatives=args.alternatives,
        )
        baidu_link = planner.build_baidu_link(
            origin_lat=args.origin_lat,
            origin_lng=args.origin_lng,
            dest_lat=args.dest_lat,
            dest_lng=args.dest_lng,
            origin_name=args.origin_name,
            dest_name=args.dest_name,
            mode=args.mode,
            region=args.region,
            coord_type=args.coord_type,
        )

        output = {
            "mode": args.mode,
            "distance_m": route_info["distance_m"],
            "distance_text": format_distance(route_info["distance_m"]),
            "duration_s": route_info["duration_s"],
            "duration_text": format_duration(route_info["duration_s"]),
            "routes_count": route_info["routes_count"],
            "baidu_link": baidu_link,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
TravelSmart 主入口
"""
import sys
import io
import argparse
from pathlib import Path
from loguru import logger

# 强制 stdout 为 UTF-8（解决 Windows GBK 终端 emoji 打印失败）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.clients.amap import AmapClient
from src.agents.router import RouterAgent
from src.agents.formatter import FormatterAgent
from src.scenes.highway import HighwayScene
from src.scenes.hotel import HotelScene
from src.scenes.taxi import TaxiScene
from src.config.settings import AMAP_KEY


def setup_logging():
    logger.remove()
    logger.add(sys.stderr, level="INFO")


def parse_args():
    parser = argparse.ArgumentParser(description="TravelSmart - 智能出行决策助手")
    parser.add_argument(
        "--scene",
        choices=["highway", "hotel", "taxi", "auto"],
        default="auto",
        help="场景：highway=高速出口, hotel=住宿, taxi=打车点, auto=自动识别",
    )
    parser.add_argument("--highway", type=str, help="高速名，如 G4")
    parser.add_argument("--lng", type=float, help="当前位置经度")
    parser.add_argument("--lat", type=float, help="当前位置纬度")
    parser.add_argument("--destination", type=str, help="目的地")
    parser.add_argument("--budget", type=int, default=300, help="住宿预算")
    parser.add_argument("--people", type=int, default=2, help="人数")
    parser.add_argument("--text", type=str, help="自然语言描述（替代参数）")
    parser.add_argument("--dest-lng", type=float, help="目的地经度")
    parser.add_argument("--dest-lat", type=float, help="目的地纬度")
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_args()

    # 检查 API Key
    if not AMAP_KEY:
        print("❌ 错误：未配置 AMAP_KEY")
        print("请创建 config/api_keys.yaml 或设置环境变量 AMAP_KEY")
        sys.exit(1)

    amap = AmapClient()
    formatter = FormatterAgent()

    # 自动模式：先用 LLM 识别意图
    if args.scene == "auto" or args.text:
        text = args.text or input("请描述你的情况：")
        router = RouterAgent()
        parsed = router.parse(text)
        if not parsed:
            print("❌ 无法理解你的输入，请尝试更清晰地描述")
            sys.exit(1)
        scene = parsed["scene"]
        params = parsed.get("params", {})
        print(f"🔍 识别场景：{scene} | {parsed.get('reasoning', '')}\n")
    else:
        scene = args.scene
        params = {}

    # 执行对应场景
    if scene == "highway":
        lng = args.lng or params.get("lng")
        lat = args.lat or params.get("lat")
        highway = args.highway or params.get("highway", "")
        destination = args.destination or params.get("destination", "")

        if not lng or not lat:
            print("❌ 需要提供 --lng --lat 参数")
            sys.exit(1)

        handler = HighwayScene(amap)
        result = handler.recommend(highway, lng, lat, destination)
        print(formatter.format("highway", result))

    elif scene == "hotel":
        lng = args.lng or params.get("lng")
        lat = args.lat or params.get("lat")
        budget = args.budget or params.get("budget", 300)
        people = args.people or params.get("people", 2)

        if not lng or not lat:
            print("❌ 需要提供 --lng --lat 参数")
            sys.exit(1)

        handler = HotelScene(amap)
        result = handler.recommend(lng, lat, budget=budget, people=people)
        print(formatter.format("hotel", result))

    elif scene == "taxi":
        lng = args.lng or params.get("lng")
        lat = args.lat or params.get("lat")
        dest_lng = args.dest_lng or params.get("dest_lng")
        dest_lat = args.dest_lat or params.get("dest_lat")

        if not lng or not lat:
            print("❌ 需要提供 --lng --lat 参数")
            sys.exit(1)
        if not dest_lng or not dest_lat:
            print("❌ 需要提供 --dest-lng --dest-lat 参数")
            sys.exit(1)

        handler = TaxiScene(amap)
        result = handler.recommend(lng, lat, dest_lng, dest_lat)
        print(formatter.format("taxi", result))

    else:
        print(f"❌ 未知场景: {scene}")


if __name__ == "__main__":
    main()

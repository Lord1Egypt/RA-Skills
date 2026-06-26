#!/usr/bin/env python3
"""
钢材供需现货信息查询脚本

功能：查询钢材现货的供应和求购信息，支持多维度条件筛选
授权方式：Token 通过 HTTP Header 传递
凭证文件：references/api_key.md
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({"error": "缺少依赖包：requests。请执行 pip install requests"}, ensure_ascii=False))
    sys.exit(1)


def get_api_key():
    """
    从配置文件获取API Key
    
    Returns:
        str: API Key
    
    Raises:
        Exception: 凭证文件不存在或为空
    """
    # 配置文件路径
    script_dir = Path(__file__).parent.parent
    api_key_file = script_dir / "references" / "api_key.md"
    
    # 检查文件是否存在
    if not api_key_file.exists():
        raise Exception("API Key 配置文件不存在。请先配置 API Key。")
    
    # 读取文件内容
    api_key = api_key_file.read_text(encoding="utf-8").strip()
    
    # 检查内容是否为空
    if not api_key:
        raise Exception("API Key 配置文件为空。请先配置 API Key。")
    
    return api_key


def save_api_key(api_key):
    """
    保存API Key到配置文件
    
    Args:
        api_key: API Key 字符串
    
    Raises:
        Exception: API Key 为空或文件写入失败
    """
    if not api_key or not api_key.strip():
        raise Exception("API Key 不能为空")
    
    # 配置文件路径
    script_dir = Path(__file__).parent.parent
    api_key_file = script_dir / "references" / "api_key.md"
    
    # 确保目录存在
    api_key_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存 API Key
    try:
        api_key_file.write_text(api_key.strip(), encoding="utf-8")
    except Exception as e:
        raise Exception(f"保存 API Key 失败: {str(e)}")


def query_supply_demand_spot(
    type,
    breed_name=None,
    spec=None,
    material=None,
    steel_mill=None,
    warehouse_area=None,
    warehouse_name=None,
    shop_spot_limit=5
):
    """
    查询供需现货信息
    
    Args:
        type: 信息类型，1=供应信息（找货源），2=求购信息（找买家）
        breed_name: 品种名称，如：螺纹钢、热轧板卷等
        spec: 规格名称，如：HRB400E、Q235B等
        material: 材质名称，如：20#、45#等
        steel_mill: 钢厂名称，如：宝钢、沙钢等
        warehouse_area: 地区名称，如：上海、杭州等
        warehouse_name: 仓库名称
        shop_spot_limit: 每个店铺最多取几条信息，默认5
    
    Returns:
        list: API返回的数据列表
    
    Raises:
        Exception: 参数验证失败或凭证缺失或API调用失败
    """
    # 1. 获取凭证
    api_key = get_api_key()
    
    # 2. 参数验证
    if type not in [1, 2]:
        raise Exception("type参数必须为1（供应信息）或2（求购信息）")
    
    # 3. 构建请求参数
    url = "https://mcp.mysteel.com/mcp/info/api/external/gq/querySupplyDemandSpot"
    headers = {
        "Content-Type": "application/json",
        "token": api_key
    }
    
    payload = {"type": type}
    
    # 添加可选参数
    if breed_name is not None:
        payload["breedName"] = breed_name
    if spec is not None:
        payload["spec"] = spec
    if material is not None:
        payload["material"] = material
    if steel_mill is not None:
        payload["steelMill"] = steel_mill
    if warehouse_area is not None:
        payload["warehouseArea"] = warehouse_area
    if warehouse_name is not None:
        payload["warehouseName"] = warehouse_name
    
    payload["shopSpotLimit"] = shop_spot_limit
    
    # 4. 发起请求
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
        
        data = response.json()
    except requests.exceptions.Timeout:
        raise Exception("请求超时（30秒）")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
    
    # 5. 错误处理
    if data.get("code") == "400":
        raise Exception("Token校验失败，请重新配置API Key")
    
    if data.get("code") != "200":
        raise Exception(f"接口错误: {data.get('mess') or data.get('message') or '未知错误'}")
    
    # 6. 返回数据
    return data.get("data", [])


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="钢材供需现货信息查询脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python supply_demand_api.py --type 1 --breed_name 螺纹钢 --warehouse_area 上海
  python supply_demand_api.py --type 2 --breed_name 热轧板卷
  python supply_demand_api.py --save_api_key "your_api_key"
        """
    )
    
    parser.add_argument("--type", type=int, help="信息类型：1=供应信息，2=求购信息")
    parser.add_argument("--breed_name", type=str, help="品种名称")
    parser.add_argument("--spec", type=str, help="规格名称")
    parser.add_argument("--material", type=str, help="材质名称")
    parser.add_argument("--steel_mill", type=str, help="钢厂名称")
    parser.add_argument("--warehouse_area", type=str, help="地区名称")
    parser.add_argument("--warehouse_name", type=str, help="仓库名称")
    parser.add_argument("--shop_spot_limit", type=int, default=5, help="每个店铺最多取几条，默认5")
    parser.add_argument("--save_api_key", type=str, help="保存 API Key 到配置文件")
    
    args = parser.parse_args()
    
    # 如果提供了保存 API Key 参数，则保存 API Key
    if args.save_api_key:
        try:
            save_api_key(args.save_api_key)
            print(json.dumps({"success": True, "message": "API Key 已保存"}, ensure_ascii=False, indent=2))
            sys.exit(0)
        except Exception as error:
            print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
            sys.exit(1)
    
    # 查询供需信息
    if args.type is None:
        parser.print_help()
        sys.exit(1)
    
    try:
        result = query_supply_demand_spot(
            type=args.type,
            breed_name=args.breed_name,
            spec=args.spec,
            material=args.material,
            steel_mill=args.steel_mill,
            warehouse_area=args.warehouse_area,
            warehouse_name=args.warehouse_name,
            shop_spot_limit=args.shop_spot_limit
        )
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    except Exception as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

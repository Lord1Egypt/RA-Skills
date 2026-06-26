#!/usr/bin/env python3
"""
我的钢铁网会议查询脚本（专题页版）- 动态数据版
Mysteel Conference Query Script - ZhuanTi Version (Dynamic)
支持与 huizhan.mysteel.com/zhuanti 页面一致的筛选功能
行业、地区、省份数据从API动态获取，不再硬编码
"""

import argparse
import json
import urllib.request
import urllib.error
import sys
import os
from typing import Any, Dict, Optional, List, Tuple
from datetime import datetime

# 设置 UTF-8 输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


BASE_URL = "https://huizhan.mysteel.com/event/activity"

# 缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# 缓存有效期（秒）- 默认24小时
CACHE_TTL = 24 * 60 * 60


def get_cache_path(cache_type: str) -> str:
    """获取缓存文件路径"""
    return os.path.join(CACHE_DIR, f"{cache_type}_cache.json")


def load_cache(cache_type: str) -> Optional[List[Dict]]:
    """加载缓存数据"""
    cache_path = get_cache_path(cache_type)
    if not os.path.exists(cache_path):
        return None

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        # 检查缓存是否过期
        cache_time = cache_data.get('_cache_time', 0)
        if (datetime.now().timestamp() - cache_time) > CACHE_TTL:
            return None

        return cache_data.get('data', [])
    except:
        return None


def save_cache(cache_type: str, data: List[Dict]) -> None:
    """保存数据到缓存"""
    cache_path = get_cache_path(cache_type)
    try:
        cache_data = {
            '_cache_time': datetime.now().timestamp(),
            'data': data
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False)
    except:
        pass


def clear_cache():
    """清除所有缓存"""
    for f in os.listdir(CACHE_DIR):
        if f.endswith('_cache.json'):
            os.remove(os.path.join(CACHE_DIR, f))


def make_request(url: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """发送HTTP请求"""
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=headers,
        method="POST" if data else "GET"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"code": -1, "msg": f"请求失败: {e}", "data": None}
    except Exception as e:
        return {"code": -1, "msg": f"未知错误: {e}", "data": None}


def query_conferences(
    keyword: str = "",
    industry_id: str = "",
    area_id: str = "",
    province_id: str = "",
    status: str = "",
    charge_type: str = "",
    activity_classify: str = "",
    page_size: int = 10,
    page_num: int = 1
) -> Dict[str, Any]:
    """查询会议列表"""
    url = f"{BASE_URL}/queryActivity"
    payload = {
        "keyword": keyword,
        "industryBreedId": industry_id,
        "areaId": area_id,
        "provinceId": province_id,
        "activityStatus": status,
        "chargeType": charge_type,
        "activityClassify": activity_classify,
        "pageSize": page_size,
        "pageNum": page_num
    }
    # 移除空值
    payload = {k: v for k, v in payload.items() if v}
    return make_request(url, payload)


def query_industries_api() -> Dict[str, Any]:
    """查询行业分类API"""
    url = f"{BASE_URL}/queryIndustry"
    return make_request(url)


def query_areas_api(industry_id: str = "") -> Dict[str, Any]:
    """查询地区分类API"""
    url = f"{BASE_URL}/queryArea"
    if industry_id:
        url += f"?industryBreedId={industry_id}"
    return make_request(url)


def load_industries() -> List[Dict]:
    """加载行业列表（优先从缓存）"""
    # 尝试从缓存加载
    cached = load_cache('industries')
    if cached is not None:
        return cached

    # 从API获取
    data = query_industries_api()
    industries = []

    if is_success(data) and data.get("data"):
        industries = data.get("data", [])

    # 保存到缓存
    save_cache('industries', industries)
    return industries


def load_areas(industry_id: str = "") -> List[Dict]:
    """加载地区和省份列表（优先从缓存）"""
    cache_key = f'areas_{industry_id}' if industry_id else 'areas'

    # 尝试从缓存加载
    cached = load_cache(cache_key)
    if cached is not None:
        return cached

    # 从API获取
    data = query_areas_api(industry_id)
    areas = []

    if is_success(data) and data.get("data"):
        areas = data.get("data", [])

    # 保存到缓存
    save_cache(cache_key, areas)
    return areas


def find_industry_by_name(name: str, industries: List[Dict] = None) -> Optional[str]:
    """通过名称查找行业ID（支持模糊匹配）"""
    if not name:
        return None

    if industries is None:
        industries = load_industries()

    name_lower = name.lower().strip()

    # 精确匹配
    for ind in industries:
        ind_name = ind.get('industryBreedName', '')
        if ind_name == name:
            return ind.get('industryBreedId')

    # 部分匹配
    for ind in industries:
        ind_name = ind.get('industryBreedName', '')
        if name_lower in ind_name.lower() or ind_name.lower() in name_lower:
            return ind.get('industryBreedId')

    return None


def find_area_by_name(name: str, areas: List[Dict] = None) -> Optional[Dict]:
    """通过名称查找地区ID和省份ID"""
    if not name:
        return None

    if areas is None:
        areas = load_areas()

    name_lower = name.lower().strip()

    # 在省份中查找（优先匹配省份，因为地区名可能包含省份关键字）
    for area in areas:
        province_list = area.get('list', [])
        for prov in province_list:
            prov_name = prov.get('provinceName', '')
            # 精确匹配省份
            if prov_name == name:
                return {
                    'areaId': prov.get('areaId', area.get('areaId')),
                    'areaName': prov.get('area', area.get('area')),
                    'provinceId': prov.get('provinceId'),
                    'provinceName': prov_name
                }
            # 部分匹配省份
            if name_lower in prov_name.lower() or prov_name.lower() in name_lower:
                return {
                    'areaId': prov.get('areaId', area.get('areaId')),
                    'areaName': prov.get('area', area.get('area')),
                    'provinceId': prov.get('provinceId'),
                    'provinceName': prov_name
                }

    # 匹配地区名
    for area in areas:
        area_name = area.get('area', '')
        # 精确匹配地区
        if area_name == name:
            return {
                'areaId': area.get('areaId'),
                'areaName': area_name
            }
        # 部分匹配地区
        if name_lower in area_name.lower() or area_name.lower() in name_lower:
            return {
                'areaId': area.get('areaId'),
                'areaName': area_name
            }

    return None


def is_success(data: Dict[str, Any]) -> bool:
    """检查请求是否成功"""
    return data.get("code") in [0, 200, "0", "200"]


def format_timestamp(ts) -> str:
    """格式化时间戳"""
    if not ts:
        return "-"
    if isinstance(ts, (int, float)):
        try:
            return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
        except:
            return str(ts)[:10]
    return str(ts)[:10] if len(str(ts)) >= 10 else str(ts)


def format_status(status: str) -> str:
    """格式化会议状态"""
    status_map = {
        "0": "报名中",
        "1": "进行中",
        "2": "已结束"
    }
    return status_map.get(status, status)


def format_fee(charge_type: str, fee: Any) -> str:
    """格式化费用"""
    if charge_type == "0":
        return "免费"
    elif charge_type == "1":
        return f"¥{fee}" if fee else "收费"
    return f"¥{fee}" if fee else "-"


def print_conferences(data: Dict[str, Any], verbose: bool = False) -> None:
    """打印会议列表"""
    if not is_success(data) or not data.get("data"):
        msg = data.get('msg', '未知错误')
        print(f"❌ 查询失败: {msg}")
        return

    list_data = data.get("data", {}).get("list", [])
    total = data.get("data", {}).get("total", 0)
    page_num = data.get("data", {}).get("pageNum", 1)
    page_size = data.get("data", {}).get("pageSize", 10)
    total_pages = (total + page_size - 1) // page_size if page_size else 1

    if not list_data:
        print("📭 暂无符合条件的会议")
        return

    print(f"\n📅 会议查询结果（共 {total} 条，第 {page_num}/{total_pages} 页）\n")
    print("=" * 120)

    for i, conf in enumerate(list_data, 1):
        # 基本信息
        name = conf.get('name') or conf.get('activityName') or '未知会议'
        status = format_status(str(conf.get("activityStatus", "")))
        status_emoji = "🟢" if status == "报名中" else "🟡" if status == "进行中" else "⚪"

        # 拼接地址
        address_parts = [
            conf.get("provinceName", ""),
            conf.get("cityName", ""),
            conf.get("address", "")
        ]
        address = "".join(filter(None, address_parts))

        # 时间
        start_time = format_timestamp(conf.get("startTime"))
        end_time = format_timestamp(conf.get("endTime"))
        time_str = start_time if start_time == end_time else f"{start_time} ~ {end_time}"

        # 费用
        fee = format_fee(str(conf.get("chargeType", "")), conf.get("fee"))

        # 倒计时
        countdown = conf.get("countdownDay")
        countdown_str = f"倒计时 {countdown} 天" if countdown else ""

        # 行业
        industry_name = conf.get("industryBreedName", "")

        # 活动类型
        activity_classify = conf.get("activityClassify", "")

        print(f"{i}. {status_emoji} [{status}] {name}")
        print(f"   📍 {address or '-'}")
        print(f"   📆 {time_str} {countdown_str}")
        print(f"   💰 {fee}")

        # 详情链接（默认显示）
        detail_url = conf.get('detailPcPageUrl') or conf.get('detailUrl') or ''
        if detail_url:
            print(f"   🔗 {detail_url}")

        if verbose:
            if industry_name:
                print(f"   🏭 行业: {industry_name}")
            if activity_classify:
                print(f"   📋 类型: {activity_classify}")

        print("-" * 120)


def print_industries(industries: List[Dict] = None) -> None:
    """打印行业分类"""
    if industries is None:
        industries = load_industries()

    if not industries:
        print("📭 暂无行业分类")
        return

    print(f"\n🏭 行业分类（共 {len(industries)} 个）\n")
    print("-" * 50)
    print(f"{'行业ID':<15} {'行业名称':<20}")
    print("-" * 50)
    for ind in industries:
        ind_id = ind.get('industryBreedId', '')
        ind_name = ind.get('industryBreedName', '')
        print(f"{ind_id:<15} {ind_name:<20}")
    print("-" * 50)


def print_areas(areas: List[Dict] = None) -> None:
    """打印地区分类（含省份）"""
    if areas is None:
        areas = load_areas()

    if not areas:
        print("📭 暂无地区分类")
        return

    print(f"\n🗺️ 地区分类（共 {len(areas)} 个）\n")
    print("-" * 80)

    for area in areas:
        area_id = area.get('areaId', '')
        area_name = area.get('area', '')
        province_list = area.get('list', [])

        print(f"\n📍 [{area_id}] {area_name} ({len(province_list)} 个省份)")
        for prov in province_list:
            prov_id = prov.get('provinceId', '')
            prov_name = prov.get('provinceName', '')
            print(f"    {prov_id:<10} - {prov_name}")

    print("-" * 80)


def print_conference_count(area: Dict, count: int) -> None:
    """打印匹配的地区/省份信息"""
    area_name = area.get('areaName', '未知地区')
    province_name = area.get('provinceName', '')

    if province_name:
        print(f"   📍 {area_name} > {province_name}")
        print(f"   🔢 地区ID: {area.get('areaId')}, 省份ID: {area.get('provinceId')}")
    else:
        print(f"   📍 {area_name}")
        print(f"   🔢 地区ID: {area.get('areaId')}")


def main():
    parser = argparse.ArgumentParser(
        description="我的钢铁网会议查询工具（专题页版 - 动态数据）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --keyword "钢铁"                    # 搜索关键词
  %(prog)s --industry "钢材"                    # 按行业名称筛选（自动查ID）
  %(prog)s --area "华东"                        # 按地区名称筛选
  %(prog)s --area "吉林"                         # 按省份名称筛选
  %(prog)s --status "0"                        # 报名中的会议
  %(prog)s --charge-type "0"                   # 免费会议
  %(prog)s --industry "钢材" --status "0"      # 组合筛选
  %(prog)s --list-industries                   # 列出所有行业
  %(prog)s --list-areas                        # 列出所有地区
  %(prog)s --clear-cache                       # 清除缓存

行业/地区/省份支持名称输入，自动转换为ID！
        """
    )
    parser.add_argument("--keyword", "-k", type=str, default="", help="搜索关键词")
    parser.add_argument("--industry", type=str, default="", help="行业名称（自动查ID）")
    parser.add_argument("--industry-id", "-i", type=str, default="", help="行业ID")
    parser.add_argument("--area", type=str, default="", help="地区/省份名称（自动查ID）")
    parser.add_argument("--area-id", "-a", type=str, default="", help="地区ID")
    parser.add_argument("--province-id", "-p", type=str, default="", help="省份ID")
    parser.add_argument("--status", "-s", type=str, choices=["0", "1", "2"], default="",
                        help="会议状态: 0=报名中, 1=进行中, 2=已结束")
    parser.add_argument("--charge-type", "-c", type=str, choices=["0", "1"], default="",
                        help="收费类型: 0=免费, 1=收费")
    parser.add_argument("--activity-classify", type=str, default="",
                        help="活动类型")
    parser.add_argument("--page-size", type=int, default=10, help="每页数量")
    parser.add_argument("--page-num", "-n", type=int, default=1, help="页码")
    parser.add_argument("--list-industries", action="store_true", help="列出所有行业分类")
    parser.add_argument("--list-areas", action="store_true", help="列出所有地区分类（含省份）")
    parser.add_argument("--clear-cache", action="store_true", help="清除缓存")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出模式")

    args = parser.parse_args()

    # 清除缓存
    if args.clear_cache:
        clear_cache()
        print("✅ 缓存已清除")
        return

    # 列出行业
    if args.list_industries:
        industries = load_industries()
        print_industries(industries)
        return

    # 列出地区
    if args.list_areas:
        areas = load_areas(args.industry_id)
        print_areas(areas)
        return

    # 智能解析行业
    industry_id = args.industry_id
    if args.industry and not industry_id:
        industries = load_industries()
        found_id = find_industry_by_name(args.industry, industries)
        if found_id:
            industry_id = found_id
            print(f"🏭 匹配行业: {args.industry} → ID: {industry_id}")
        else:
            # API没有则用关键词
            print(f"⚠️ 未找到行业 '{args.industry}'，将作为关键词搜索")

    # 智能解析地区/省份
    area_id = args.area_id
    province_id = args.province_id
    if args.area and not area_id:
        areas = load_areas()
        found = find_area_by_name(args.area, areas)
        if found:
            area_id = found.get('areaId')
            province_id = found.get('provinceId', province_id)
            print_conference_count(found, 0)
        else:
            # API没有则用关键词
            print(f"⚠️ 未找到地区/省份 '{args.area}'，将作为关键词搜索")

    # 执行查询
    data = query_conferences(
        keyword=args.keyword,
        industry_id=industry_id,
        area_id=area_id,
        province_id=province_id,
        status=args.status,
        charge_type=args.charge_type,
        activity_classify=args.activity_classify,
        page_size=args.page_size,
        page_num=args.page_num
    )
    print_conferences(data, verbose=args.verbose)


if __name__ == "__main__":
    main()

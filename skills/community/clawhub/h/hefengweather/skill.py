"""
和风天气查询 Skill
基于 Model Context Protocol 的天气数据查询服务
"""

import httpx
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("hefeng_weather_skill")

# 加载环境变量 - 按优先级：1. 项目安装路径 2. ~/.config/qweather/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))  # skill.py 所在目录
load_dotenv(os.path.expanduser("~/.config/qweather/.env"))  # 用户配置目录

# POI类型常量
POI_TYPES = {
    "scenic": "景点",
    "TSTA": "潮汐站点"
}


def configure(
    api_host: Optional[str] = None,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    key_id: Optional[str] = None,
    private_key_path: Optional[str] = None,
    private_key: Optional[str] = None,
    save_to_file: bool = True,
) -> Dict[str, Any]:
    """
    配置和风天气API认证信息

    支持两种认证方式：
    1. API KEY认证（推荐）：配置 api_host + api_key
    2. JWT数字签名认证：配置 api_host + project_id + key_id + private_key_path/private_key

    Args:
        api_host: API主机地址，如 "your-domain.qweatherapi.com"
        api_key: API KEY（推荐方式）
        project_id: 项目ID（JWT方式）
        key_id: 密钥ID（JWT方式）
        private_key_path: 私钥文件路径（JWT方式）
        private_key: 私钥内容字符串（JWT方式，与private_key_path二选一）
        save_to_file: 是否保存配置到 ~/.config/qweather/.env，默认True

    Returns:
        配置结果字典，包含 success 状态和消息

    Examples:
        >>> # API KEY方式（推荐）
        >>> configure(api_host="your-domain.qweatherapi.com", api_key="your_key")

        >>> # JWT方式
        >>> configure(
        ...     api_host="your-domain.qweatherapi.com",
        ...     project_id="your_project_id",
        ...     key_id="your_key_id",
        ...     private_key_path="./ed25519-private.pem"
        ... )
    """
    global _api_host, _auth_header

    # 验证必需参数
    if not api_host:
        return {"success": False, "message": "api_host 不能为空"}

    # 验证认证方式
    if api_key:
        # API KEY方式
        auth_method = "api_key"
    elif project_id and key_id and (private_key_path or private_key):
        # JWT方式
        auth_method = "jwt"
    else:
        return {
            "success": False,
            "message": "认证配置不完整。请提供：\n"
                      "1. API KEY方式：api_host + api_key\n"
                      "2. JWT方式：api_host + project_id + key_id + private_key_path/private_key"
        }

    # 保存到环境变量
    os.environ["HEFENG_API_HOST"] = api_host
    if api_key:
        os.environ["HEFENG_API_KEY"] = api_key
    if project_id:
        os.environ["HEFENG_PROJECT_ID"] = project_id
    if key_id:
        os.environ["HEFENG_KEY_ID"] = key_id
    if private_key_path:
        os.environ["HEFENG_PRIVATE_KEY_PATH"] = private_key_path
    if private_key:
        os.environ["HEFENG_PRIVATE_KEY"] = private_key

    # 保存到文件
    if save_to_file:
        config_dir = os.path.expanduser("~/.config/qweather")
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, ".env")

        lines = [f"HEFENG_API_HOST={api_host}"]
        if api_key:
            lines.append(f"HEFENG_API_KEY={api_key}")
        if project_id:
            lines.append(f"HEFENG_PROJECT_ID={project_id}")
        if key_id:
            lines.append(f"HEFENG_KEY_ID={key_id}")
        if private_key_path:
            lines.append(f"HEFENG_PRIVATE_KEY_PATH={private_key_path}")
        if private_key:
            lines.append(f"HEFENG_PRIVATE_KEY={private_key}")

        try:
            with open(config_file, "w") as f:
                f.write("\n".join(lines))
            logger.info(f"配置已保存到: {config_file}")
        except Exception as e:
            return {"success": False, "message": f"保存配置文件失败: {e}"}

    # 重置全局配置，下次调用时会重新初始化
    _api_host = None
    _auth_header = None

    return {
        "success": True,
        "message": f"配置成功（认证方式: {auth_method}）",
        "config_file": os.path.expanduser("~/.config/qweather/.env") if save_to_file else None
    }

# 全局配置
_api_host: Optional[str] = None
_auth_header: Optional[Dict[str, str]] = None


def _init_config() -> None:
    """初始化API配置"""
    global _api_host, _auth_header

    if _auth_header is not None:
        return

    _api_host = os.environ.get("HEFENG_API_HOST")
    api_key = os.environ.get("HEFENG_API_KEY")
    project_id = os.environ.get("HEFENG_PROJECT_ID")
    key_id = os.environ.get("HEFENG_KEY_ID")
    private_key_path = os.environ.get("HEFENG_PRIVATE_KEY_PATH")
    private_key_str = os.environ.get("HEFENG_PRIVATE_KEY")

    if not _api_host:
        raise ValueError("HEFENG_API_HOST 环境变量未设置")

    if api_key:
        _auth_header = {"X-QW-Api-Key": api_key, "Content-Type": "application/json"}
        logger.info("使用API KEY认证模式")
    else:
        # JWT认证
        if not project_id or not key_id or (not private_key_path and not private_key_str):
            raise ValueError(
                "必须设置 HEFENG_API_KEY，或者设置完整的JWT认证配置"
            )

        if private_key_path:
            with open(private_key_path, "rb") as f:
                private_key = f.read()
        else:
            private_key = private_key_str.replace("\\r\\n", "\n").replace("\\n", "\n").encode()

        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 900,
            "sub": project_id,
        }
        headers = {"kid": key_id}

        encoded_jwt = jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)
        _auth_header = {"Authorization": f"Bearer {encoded_jwt}"}
        logger.info("使用JWT认证模式")


def _get_city_location(city: str, location: bool = False) -> Optional[str]:
    """根据城市名称获取LocationID或经纬度"""
    _init_config()

    url = f"https://{_api_host}/geo/v2/city/lookup"

    try:
        response = httpx.get(url, headers=_auth_header, params={"location": city})

        if response.status_code != 200:
            logger.error(f"查询城市位置失败 - 状态码: {response.status_code}")
            return None

        data = response.json()
        if data and data.get("location") and len(data["location"]) > 0:
            if location:
                lat = float(data["location"][0]["lat"])
                lon = float(data["location"][0]["lon"])
                return f"{lat:.2f},{lon:.2f}"
            return data["location"][0]["id"]
        else:
            logger.warning(f"未找到城市 '{city}' 的位置信息")
            return None

    except Exception as e:
        logger.error(f"查询城市位置时发生错误: {e}")
        return None


def get_weather(city: str, days: str = "3d") -> Optional[Dict[str, Any]]:
    """获取指定城市的天气预报（3-30天）"""
    _init_config()

    if not city or not city.strip():
        logger.error("城市名称不能为空")
        return None

    city = city.strip()
    valid_days = ["3d", "7d", "10d", "15d", "30d"]
    if days not in valid_days:
        logger.error(f"无效的预报天数参数: {days}")
        return None

    location_id = _get_city_location(city)
    if not location_id:
        return None

    url = f"https://{_api_host}/v7/weather/{days}?location={location_id}"

    try:
        response = httpx.get(url=url, headers=_auth_header)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取天气数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取天气数据时发生错误: {e}")
        return None


def get_weather_now(
    location: Optional[str] = None,
    city: Optional[str] = None,
    lang: str = "zh",
    unit: str = "m",
) -> Optional[Dict[str, Any]]:
    """获取实时天气数据"""
    _init_config()

    if unit not in {"m", "i"}:
        logger.error(f"无效的单位参数 unit: {unit}")
        return None

    loc_value = location.strip() if isinstance(location, str) else None
    if not loc_value:
        if not city or not city.strip():
            logger.error("必须提供 location 或 city 其中之一")
            return None
        loc_value = _get_city_location(city.strip())
        if not loc_value:
            return None

    url = f"https://{_api_host}/v7/weather/now"
    params = {"location": loc_value, "lang": lang, "unit": unit}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取实况天气数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取实况天气数据时发生错误: {e}")
        return None


def get_hourly_weather(
    hours: str = "24h",
    location: Optional[str] = None,
    city: Optional[str] = None,
    lang: str = "zh",
    unit: str = "m",
) -> Optional[Dict[str, Any]]:
    """获取逐小时天气预报（24/72/168小时）"""
    _init_config()

    valid_hours = {"24h", "72h", "168h"}
    if hours not in valid_hours:
        logger.error(f"无效的 hours 参数: {hours}")
        return None

    if unit not in {"m", "i"}:
        logger.error(f"无效的单位参数 unit: {unit}")
        return None

    loc_value = location.strip() if isinstance(location, str) else None
    if not loc_value:
        if not city or not city.strip():
            logger.error("必须提供 location 或 city 其中之一")
            return None
        loc_value = _get_city_location(city.strip())
        if not loc_value:
            return None

    url = f"https://{_api_host}/v7/weather/{hours}"
    params = {"location": loc_value, "lang": lang, "unit": unit}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取逐小时天气数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取逐小时天气数据时发生错误: {e}")
        return None


def get_weather_history(
    *,
    location: Optional[str] = None,
    city: Optional[str] = None,
    days: int = 10,
    lang: str = "zh",
    unit: str = "m",
) -> Optional[Dict[str, Any]]:
    """获取历史天气数据（最近10天）"""
    _init_config()

    if (not location or not str(location).strip()) and (not city or not city.strip()):
        logger.error("必须提供 location 或 city 其中之一")
        return None

    if not isinstance(days, int) or days < 1 or days > 10:
        logger.error("参数 days 必须为整数，且范围为 1 到 10")
        return None

    location_id = None
    loc_value = location.strip() if isinstance(location, str) and location.strip() else None
    if loc_value:
        if "," in loc_value:
            location_id = _get_city_location(loc_value)
        else:
            location_id = loc_value
    else:
        location_id = _get_city_location(city.strip())

    if not location_id:
        return None

    results: Dict[str, Any] = {}
    beijing_now = datetime.now(tz=timezone.utc) + timedelta(hours=8)

    for offset in range(days, 0, -1):
        target_date = (beijing_now - timedelta(days=offset)).strftime("%Y%m%d")
        url = f"https://{_api_host}/v7/historical/weather"
        params = {"location": location_id, "date": target_date, "lang": lang, "unit": unit}

        try:
            response = httpx.get(url, headers=_auth_header, params=params)
            if response.status_code == 200:
                results[target_date] = response.json()
            else:
                results[target_date] = {"error": response.text, "status_code": response.status_code}
            time.sleep(0.1)
        except Exception as e:
            results[target_date] = {"error": str(e)}

    return results


def get_air_quality(city: str) -> Optional[Dict[str, Any]]:
    """获取实时空气质量数据"""
    _init_config()

    location_lat_lon = _get_city_location(city, location=True)
    if not location_lat_lon:
        return None

    try:
        lat, lon = location_lat_lon.split(",")
    except ValueError:
        logger.error(f"无法解析经纬度信息: {location_lat_lon}")
        return None

    url = f"https://{_api_host}/airquality/v1/current/{lat}/{lon}"
    params = {"lang": "zh"}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取空气质量数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取空气质量数据时发生错误: {e}")
        return None


def get_air_quality_history(
    city: str, days: int = 10, lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取历史空气质量数据（最近10天）"""
    _init_config()

    if not city or not city.strip():
        logger.error("城市名称不能为空")
        return None

    if not isinstance(days, int) or days < 1 or days > 10:
        logger.error("参数 days 必须为整数，且范围为 1 到 10")
        return None

    city = city.strip()
    location_id = _get_city_location(city)
    if not location_id:
        return None

    results: Dict[str, Any] = {}
    beijing_now = datetime.now(tz=timezone.utc) + timedelta(hours=8)

    for offset in range(days, 0, -1):
        target_date = (beijing_now - timedelta(days=offset)).strftime("%Y%m%d")
        url = f"https://{_api_host}/v7/historical/air"
        params = {"location": location_id, "date": target_date, "lang": lang}

        try:
            response = httpx.get(url, headers=_auth_header, params=params)
            if response.status_code == 200:
                results[target_date] = response.json()
            else:
                results[target_date] = {"error": response.text, "status_code": response.status_code}
            time.sleep(0.1)
        except Exception as e:
            results[target_date] = {"error": str(e)}

    return results


def get_air_quality_hourly(
    location: str, hours: str = "24h", lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取逐小时空气质量预报"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()
    if "," not in loc_value:
        logger.error(f"location 参数格式错误：'{loc_value}'，期望格式：纬度,经度")
        return None

    try:
        lat_str, lon_str = [s.strip() for s in loc_value.split(",", 1)]
        lat = float(lat_str)
        lon = float(lon_str)
        formatted_loc = f"{lat:.2f},{lon:.2f}"
    except Exception as e:
        logger.error(f"无法解析坐标参数：{loc_value}，错误：{e}")
        return None

    valid_hours = {"24h", "72h", "168h"}
    if hours not in valid_hours:
        logger.error(f"无效的预报小时数参数: {hours}")
        return None

    lat, lon = formatted_loc.split(",")
    url = f"https://{_api_host}/airquality/v1/hourly/{lat}/{lon}"
    params = {"hours": hours, "lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取空气质量小时预报数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取空气质量小时预报数据时发生错误: {e}")
        return None


def get_air_quality_daily(
    location: str, days: str = "3d", lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取逐日空气质量预报（最多15天）"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()
    if "," not in loc_value:
        logger.error(f"location 参数格式错误：'{loc_value}'，期望格式：纬度,经度")
        return None

    try:
        lat_str, lon_str = [s.strip() for s in loc_value.split(",", 1)]
        lat = float(lat_str)
        lon = float(lon_str)
        formatted_loc = f"{lat:.2f},{lon:.2f}"
    except Exception as e:
        logger.error(f"无法解析坐标参数：{loc_value}，错误：{e}")
        return None

    valid_days = {"3d", "7d", "15d"}
    if days not in valid_days:
        logger.error(f"无效的预报天数参数: {days}")
        return None

    lat, lon = formatted_loc.split(",")
    url = f"https://{_api_host}/airquality/v1/daily/{lat}/{lon}"
    params = {"days": days, "lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取空气质量每日预报数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取空气质量每日预报数据时发生错误: {e}")
        return None


def get_air_quality_stations(
    station_id: str, lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取空气质量监测站数据"""
    _init_config()

    if not station_id or not str(station_id).strip():
        logger.error("station_id 参数不能为空")
        return None

    station_value = str(station_id).strip()
    url = f"https://{_api_host}/airquality/v1/station/{station_value}"
    params = {"lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取空气质量监测站数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取空气质量监测站数据时发生错误: {e}")
        return None


def get_indices(
    city: str,
    days: str = "1d",
    index_types: str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16",
) -> Optional[Dict[str, Any]]:
    """获取天气生活指数预报"""
    _init_config()

    if not city or not city.strip():
        logger.error("城市名称不能为空")
        return None

    if days not in ["1d", "3d"]:
        logger.error(f"无效的预报天数参数: {days}")
        return None

    city = city.strip()
    location_id = _get_city_location(city)
    if not location_id:
        return None

    url = f"https://{_api_host}/v7/indices/{days}"
    params = {"location": location_id, "type": index_types, "lang": "zh"}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取生活指数数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取生活指数数据时发生错误: {e}")
        return None


def get_warning(city: str) -> Optional[Dict[str, Any]]:
    """获取气象灾害预警信息"""
    _init_config()

    if not city or not city.strip():
        logger.error("城市名称不能为空")
        return None

    city = city.strip()
    location_id = _get_city_location(city)
    if not location_id:
        return None

    url = f"https://{_api_host}/v7/warning/now?location={location_id}&lang=zh"

    try:
        response = httpx.get(url, headers=_auth_header)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取预警数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取预警数据时发生错误: {e}")
        return None


def get_astronomy_sun(
    location: str, date: str, lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取日出日落时间（全球任意地点，未来60天内）"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()

    if "," in loc_value:
        try:
            lon_str, lat_str = [s.strip() for s in loc_value.split(",", 1)]
            lon = float(lon_str)
            lat = float(lat_str)
            loc_value = f"{lon:.2f},{lat:.2f}"
        except Exception:
            logger.error(f"无法解析经纬度参数: {loc_value}")
            return None
    else:
        if not loc_value.isdigit():
            resolved = _get_city_location(loc_value)
            if not resolved:
                return None
            loc_value = resolved

    try:
        target_date = datetime.strptime(date, "%Y%m%d").date()
    except Exception:
        logger.error("date 参数格式错误，需为 yyyyMMdd")
        return None

    beijing_today = (datetime.now(timezone.utc) + timedelta(hours=8)).date()
    max_date = beijing_today + timedelta(days=60)
    if target_date < beijing_today or target_date > max_date:
        logger.error(f"date 参数超出允许范围")
        return None

    url = f"https://{_api_host}/v7/astronomy/sun"
    params = {"location": loc_value, "date": date, "lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取太阳天文数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取太阳天文数据时发生错误: {e}")
        return None


def get_astronomy_moon(
    location: str, date: str, lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取月升月落和逐小时月相数据"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()

    if "," in loc_value:
        try:
            lon_str, lat_str = [s.strip() for s in loc_value.split(",", 1)]
            lon = float(lon_str)
            lat = float(lat_str)
            loc_value = f"{lon:.2f},{lat:.2f}"
        except Exception:
            logger.error(f"无法解析经纬度参数: {loc_value}")
            return None
    else:
        if not loc_value.isdigit():
            resolved = _get_city_location(loc_value)
            if not resolved:
                return None
            loc_value = resolved

    try:
        target_date = datetime.strptime(date, "%Y%m%d").date()
    except Exception:
        logger.error("date 参数格式错误，需为 yyyyMMdd")
        return None

    beijing_today = (datetime.now(timezone.utc) + timedelta(hours=8)).date()
    max_date = beijing_today + timedelta(days=60)
    if target_date < beijing_today or target_date > max_date:
        logger.error(f"date 参数超出允许范围")
        return None

    url = f"https://{_api_host}/v7/astronomy/moon"
    params = {"location": loc_value, "date": date, "lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取月亮天文数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取月亮天文数据时发生错误: {e}")
        return None


def get_minutely_5m(location: str, lang: str = "zh") -> Optional[Dict[str, Any]]:
    """获取未来2小时5分钟级降水预报"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()

    if "," not in loc_value:
        resolved = _get_city_location(loc_value, location=True)
        if not resolved:
            return None
        loc_value = resolved

    url = f"https://{_api_host}/v7/minutely/5m"
    params = {"location": loc_value, "lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取分钟级降水数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取分钟级降水数据时发生错误: {e}")
        return None


def get_grid_weather_now(
    location: str, lang: str = "zh", unit: str = "m"
) -> Optional[Dict[str, Any]]:
    """获取格点实时天气数据"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()
    if "," not in loc_value:
        logger.error(f"location 参数格式错误：'{loc_value}'，期望格式：经度,纬度")
        return None

    try:
        lon_str, lat_str = [s.strip() for s in loc_value.split(",", 1)]
        lon = float(lon_str)
        lat = float(lat_str)

        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
            logger.error("经纬度超出有效范围")
            return None

        formatted_loc = f"{lon:.2f},{lat:.2f}"
    except Exception as e:
        logger.error(f"无法解析坐标参数：{loc_value}，错误：{e}")
        return None

    if unit not in {"m", "i"}:
        logger.error(f"无效的单位参数 unit: {unit}")
        return None

    url = f"https://{_api_host}/v7/grid-weather/now"
    params = {"location": formatted_loc, "lang": lang, "unit": unit}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取格点实时天气数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取格点实时天气数据时发生错误: {e}")
        return None


def get_grid_weather_daily(
    location: str, days: str = "3d", lang: str = "zh", unit: str = "m"
) -> Optional[Dict[str, Any]]:
    """获取格点每日天气预报"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()
    if "," not in loc_value:
        logger.error(f"location 参数格式错误：'{loc_value}'，期望格式：经度,纬度")
        return None

    try:
        lon_str, lat_str = [s.strip() for s in loc_value.split(",", 1)]
        lon = float(lon_str)
        lat = float(lat_str)

        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
            logger.error("经纬度超出有效范围")
            return None

        formatted_loc = f"{lon:.2f},{lat:.2f}"
    except Exception as e:
        logger.error(f"无法解析坐标参数：{loc_value}，错误：{e}")
        return None

    valid_days = ["3d", "7d"]
    if days not in valid_days:
        logger.error(f"无效的预报天数参数: {days}")
        return None

    if unit not in {"m", "i"}:
        logger.error(f"无效的单位参数 unit: {unit}")
        return None

    url = f"https://{_api_host}/v7/grid-weather/{days}"
    params = {"location": formatted_loc, "lang": lang, "unit": unit}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取格点每日天气预报失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取格点每日天气预报时发生错误: {e}")
        return None


def get_grid_weather_hourly(
    location: str, hours: str = "24h", lang: str = "zh", unit: str = "m"
) -> Optional[Dict[str, Any]]:
    """获取格点逐小时天气预报"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    loc_value = str(location).strip()
    if "," not in loc_value:
        logger.error(f"location 参数格式错误：'{loc_value}'，期望格式：经度,纬度")
        return None

    try:
        lon_str, lat_str = [s.strip() for s in loc_value.split(",", 1)]
        lon = float(lon_str)
        lat = float(lat_str)

        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
            logger.error("经纬度超出有效范围")
            return None

        formatted_loc = f"{lon:.2f},{lat:.2f}"
    except Exception as e:
        logger.error(f"无法解析坐标参数：{loc_value}，错误：{e}")
        return None

    valid_hours = ["24h", "72h"]
    if hours not in valid_hours:
        logger.error(f"无效的预报小时数参数: {hours}")
        return None

    if unit not in {"m", "i"}:
        logger.error(f"无效的单位参数 unit: {unit}")
        return None

    url = f"https://{_api_host}/v7/grid-weather/{hours}"
    params = {"location": formatted_loc, "lang": lang, "unit": unit}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取格点逐小时天气预报失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取格点逐小时天气预报时发生错误: {e}")
        return None


def get_top_cities(
    number: int = 10, city_type: str = "cn", lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """获取热门城市列表"""
    _init_config()

    if not isinstance(number, int) or number < 1 or number > 100:
        logger.error(f"无效的 number 参数: {number}，支持的范围为 1-100 的整数")
        return None

    valid_types = {"cn", "world", "overseas"}
    if city_type not in valid_types:
        logger.error(f"无效的 city_type 参数: {city_type}")
        return None

    url = f"https://{_api_host}/geo/v2/city/top"
    params = {"number": str(number), "type": city_type, "lang": lang}

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"获取热门城市数据失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"获取热门城市数据时发生错误: {e}")
        return None


def search_poi(
    location: str,
    keyword: str,
    poi_type: str,
    city: Optional[str] = None,
    radius: int = 5000,
    page: int = 1,
    lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """搜索兴趣点(POI)"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    if not keyword or not str(keyword).strip():
        logger.error("keyword 参数不能为空")
        return None

    if poi_type not in POI_TYPES:
        logger.error(f"无效的POI类型: {poi_type}")
        return None

    if not isinstance(radius, int) or radius < 100 or radius > 50000:
        logger.error(f"无效的 radius 参数: {radius}")
        return None

    if not isinstance(page, int) or page < 1:
        logger.error(f"无效的 page 参数: {page}")
        return None

    loc_value = str(location).strip()

    if "," in loc_value:
        try:
            parts = [s.strip() for s in loc_value.split(",", 1)]
            if len(parts) != 2:
                return None
            lon = float(parts[0])
            lat = float(parts[1])
            formatted_loc = f"{lon:.2f},{lat:.2f}"
        except ValueError:
            return None
    elif loc_value.isdigit():
        formatted_loc = loc_value
    else:
        location_id = _get_city_location(loc_value)
        if not location_id:
            return None
        formatted_loc = location_id

    url = f"https://{_api_host}/geo/v2/poi/lookup"
    params = {
        "location": formatted_loc,
        "keyword": keyword.strip(),
        "type": poi_type,
        "radius": str(radius),
        "page": str(page),
        "lang": lang
    }

    if city and city.strip():
        if "," in city.strip():
            city_loc = _get_city_location(city.strip())
            if city_loc:
                params["city"] = city_loc
        elif city.strip().isdigit():
            params["city"] = city.strip()
        else:
            city_location_id = _get_city_location(city.strip())
            if city_location_id:
                params["city"] = city_location_id

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"POI搜索失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"POI搜索时发生错误: {e}")
        return None


def search_poi_range(
    location: str,
    poi_type: str,
    radius: int = 5,
    city: Optional[str] = None,
    page: int = 1,
    lang: str = "zh"
) -> Optional[Dict[str, Any]]:
    """在指定范围内搜索POI"""
    _init_config()

    if not location or not str(location).strip():
        logger.error("location 参数不能为空")
        return None

    if not isinstance(page, int) or page < 1:
        logger.error(f"无效的 page 参数: {page}")
        return None

    if not isinstance(radius, int) or radius < 1 or radius > 50:
        logger.error(f"无效的 radius 参数: {radius}")
        return None

    if poi_type not in POI_TYPES:
        logger.error(f"无效的POI类型: {poi_type}")
        return None

    loc_value = str(location).strip()

    if "," not in loc_value:
        logger.error(f"location 参数格式错误：'{loc_value}'，仅支持经纬度坐标")
        return None

    try:
        parts = [s.strip() for s in loc_value.split(",", 1)]
        if len(parts) != 2:
            return None
        lon = float(parts[0])
        lat = float(parts[1])

        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
            logger.error("经纬度超出有效范围")
            return None

        formatted_loc = f"{lon:.2f},{lat:.2f}"
    except ValueError as e:
        logger.error(f"无法解析坐标参数：{loc_value}，错误：{e}")
        return None

    url = f"https://{_api_host}/geo/v2/poi/range"
    params = {
        "location": formatted_loc,
        "type": poi_type,
        "radius": str(radius),
        "page": str(page),
        "lang": lang
    }

    if city and city.strip():
        if city.strip().isdigit():
            params["city"] = city.strip()
        else:
            city_location_id = _get_city_location(city.strip())
            if city_location_id:
                params["city"] = city_location_id

    try:
        response = httpx.get(url, headers=_auth_header, params=params)
        if response.status_code == 200:
            return response.json()
        logger.error(f"POI范围搜索失败 - 状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"POI范围搜索时发生错误: {e}")
        return None

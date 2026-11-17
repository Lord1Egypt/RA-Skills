"""全局配置模块

定义MC全生态智能适配工程师的全局配置：
- API密钥与端点
- 路径常量
- 版本映射表
- 默认参数
"""

import os
import json
from pathlib import Path

# === 项目根目录 ===
PROJECT_ROOT = Path(__file__).resolve().parent

# === 数据目录 ===
DATA_DIR = PROJECT_ROOT / "data"

# === 输出目录结构 ===
OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
DOWNLOADS_DIR = OUTPUT_DIR / "downloads"
LOGS_DIR = OUTPUT_DIR / "logs"
TEMP_DIR = OUTPUT_DIR / "temp"
PATCH_DIR = OUTPUT_DIR / "patch_resources"

# === API 配置 ===
class APIConfig:
    """API相关配置"""
    # Modrinth API (无需认证，但有速率限制 300次/分钟)
    MODRINTH_BASE = "https://api.modrinth.com/v2"
    MODRINTH_USER_AGENT = "MC-Skill-V1/1.0 (https://github.com/mc-skill)"
    MODRINTH_RATE_LIMIT = 300  # 每分钟最大请求数

    # CurseForge API (需要API Key)
    CURSEFORGE_BASE = "https://api.curseforge.com/v1"
    CURSEFORGE_GAME_ID = 432  # Minecraft的gameId
    CURSEFORGE_CLASS_MOD = 6  # Mod分类

    # 通过环境变量读取API Key，避免硬编码
    @staticmethod
    def get_curseforge_api_key() -> str:
        """从环境变量获取CurseForge API Key"""
        return os.environ.get("CURSEFORGE_API_KEY", "")

    @staticmethod
    def has_curseforge_key() -> bool:
        """检查是否配置了CurseForge API Key"""
        return bool(APIConfig.get_curseforge_api_key())


# === 加载器类型枚举 ===
LOADERS = ["forge", "neoforge", "fabric", "quilt", "vanilla"]

# === 启动器类型枚举 ===
LAUNCHERS = ["pcl2", "hmcl", "xmcl", "prism", "bakaxl", "fcl", "pojav", "ling_zalith", "netease"]

# === 设备类型 ===
DEVICES = ["pc", "mobile"]

# === 文件分类规则 (F1使用) ===
FILE_CLASSIFICATION_RULES = [
    # (路径模式, 类型, 中文释义)
    (r"^META-INF/?$", "dir", "元数据目录，存放模组签名和清单文件"),
    (r"^META-INF/mods\.toml$", "metadata", "NeoForge/Forge模组清单文件，声明模组基本信息"),
    (r"^META-INF/neoforge\.mods\.toml$", "metadata", "NeoForge模组清单文件"),
    (r"^fabric\.mod\.json$", "metadata", "Fabric模组清单文件"),
    (r"^assets/[^/]+/lang/?$", "lang_dir", "语言文件目录，存放各语种翻译文本"),
    (r"^assets/[^/]+/lang/.*_en_us\.json$", "lang", "英语语言文件，含所有游戏内文本键值对"),
    (r"^assets/[^/]+/lang/.*_zh_cn\.json$", "lang", "简体中文语言文件"),
    (r"^assets/[^/]+/textures/?$", "texture_dir", "贴图资源目录，存放方块/物品/实体的PNG纹理"),
    (r"^assets/[^/]+/models/?$", "model_dir", "模型文件目录，定义方块/物品的3D形状"),
    (r"^data/[^/]+/recipes/?$", "recipe_dir", "合成配方目录，定义工作台/熔炉配方"),
    (r"^data/[^/]+/loot_tables/?$", "loot_dir", "战利品表目录，定义怪物掉落和宝箱内容"),
    (r"^mixin\..*\.json$", "mixin_config", "Mixin注入配置文件，声明对游戏源码的修改规则"),
    (r"^.*\.mixins\.json$", "mixin_config", "Mixin注入配置文件"),
    (r"^.*\.class$", "class", "Java编译后的字节码文件"),
    (r"^pack\.mcmeta$", "meta", "资源包元数据，声明资源包格式版本"),
    (r"^.*\.png$", "png", "PNG贴图文件"),
    (r"^.*\.json$", "json", "JSON配置文件"),
    (r"^.*\.toml$", "toml", "TOML配置文件"),
    (r"^.*\.mcmeta$", "mcmeta", "资源元数据文件"),
]

# === MC版本 → Java版本 加载缓存 ===
_java_version_map_cache = None
_launcher_paths_cache = None
_crash_patterns_cache = None


def get_java_version_map() -> dict:
    """获取MC版本到Java版本的映射表"""
    global _java_version_map_cache
    if _java_version_map_cache is None:
        with open(DATA_DIR / "java_version_map.json", "r", encoding="utf-8") as f:
            _java_version_map_cache = json.load(f)
    return _java_version_map_cache


def get_launcher_paths() -> dict:
    """获取启动器路径映射表"""
    global _launcher_paths_cache
    if _launcher_paths_cache is None:
        with open(DATA_DIR / "launcher_paths.json", "r", encoding="utf-8") as f:
            _launcher_paths_cache = json.load(f)
    return _launcher_paths_cache


def get_crash_patterns() -> dict:
    """获取崩溃错误模式库"""
    global _crash_patterns_cache
    if _crash_patterns_cache is None:
        with open(DATA_DIR / "crash_patterns.json", "r", encoding="utf-8") as f:
            _crash_patterns_cache = json.load(f)
    return _crash_patterns_cache


_mod_version_recommendations_cache = None


def get_mod_version_recommendations() -> dict:
    """获取模组版本推荐数据库"""
    global _mod_version_recommendations_cache
    if _mod_version_recommendations_cache is None:
        with open(DATA_DIR / "mod_version_recommendations.json", "r", encoding="utf-8") as f:
            _mod_version_recommendations_cache = json.load(f)
    return _mod_version_recommendations_cache


def get_java_version(mc_version: str) -> str:
    """根据MC版本获取推荐的Java版本

    Args:
        mc_version: MC版本号，如 "1.21.1"

    Returns:
        Java主版本号字符串，如 "21"，找不到则返回空字符串
    """
    java_map = get_java_version_map()
    # 精确匹配
    if mc_version in java_map["version_map"]:
        return java_map["version_map"][mc_version]
    # 范围匹配
    for r in java_map.get("ranges", []):
        in_range = True
        if "min" in r and not _version_ge(mc_version, r["min"]):
            in_range = False
        if "max" in r and not _version_le(mc_version, r["max"]):
            in_range = False
        if in_range:
            return r["java"]
    return ""


def _parse_version(v: str):
    """将版本字符串解析为可比较的元组"""
    return tuple(int(x) for x in v.split("."))


def _version_ge(a: str, b: str) -> bool:
    """a >= b"""
    return _parse_version(a) >= _parse_version(b)


def _version_le(a: str, b: str) -> bool:
    """a <= b"""
    return _parse_version(a) <= _parse_version(b)


def get_launcher_info(launcher: str) -> dict:
    """获取指定启动器的配置信息

    Args:
        launcher: 启动器类型，如 "pcl2"

    Returns:
        启动器信息字典，未找到则返回空字典
    """
    paths = get_launcher_paths()
    return paths.get("launchers", {}).get(launcher, {})


def ensure_output_dirs() -> None:
    """确保所有输出目录存在"""
    for d in [OUTPUT_DIR, REPORTS_DIR, DOWNLOADS_DIR, LOGS_DIR, TEMP_DIR, PATCH_DIR]:
        d.mkdir(parents=True, exist_ok=True)


# === 默认参数 ===
DEFAULTS = {
    "output_dir": str(REPORTS_DIR),
    "download_dir": str(DOWNLOADS_DIR),
    "target_lang": "zh_cn",
    "platform": "modrinth",
    "device": "pc",
    "detail_level": "basic",
    "severity": "summary",
    "ui_language": "en_us",
}

# === 支持的界面语言 ===
SUPPORTED_LANGUAGES = {
    "zh_cn": "简体中文",
    "zh_tw": "繁體中文",
    "en_us": "English",
    "ja_jp": "日本語",
    "ko_kr": "한국어",
    "ru_ru": "Русский",
    "es_es": "Español",
    "it_it": "Italiano",
    "el_gr": "Ελληνικά",
    "th_th": "ภาษาไทย",
    "hi_in": "हिन्दी",
    "ar_sa": "العربية",
}

# === 统一返回结构构造 ===
def build_result(
    feature: str,
    status: str,
    input_summary: dict,
    result: dict,
    warnings: list = None,
    errors: list = None,
    output_files: dict = None,
) -> dict:
    """构造统一返回结构

    Args:
        feature: 功能名称
        status: 状态 success/partial/error
        input_summary: 输入摘要
        result: 功能特定数据
        warnings: 非致命警告列表
        errors: 错误信息列表
        output_files: 输出文件路径字典

    Returns:
        统一返回结构字典
    """
    from datetime import datetime
    return {
        "status": status,
        "feature": feature,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "input_summary": input_summary,
        "result": result,
        "warnings": warnings or [],
        "errors": errors or [],
        "output_files": output_files or {},
    }


# make_result 是 build_result 的别名，供各模块统一使用
make_result = build_result

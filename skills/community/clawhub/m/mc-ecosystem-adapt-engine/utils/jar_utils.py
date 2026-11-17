"""JAR操作工具模块

提供JAR文件的通用操作函数：
- 解压JAR到目录
- 重新打包目录为JAR
- 校验JAR完整性
- 读取JAR内文件
- 路径映射
"""

import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

from .logger import get_logger

logger = get_logger("jar_utils")


def extract_jar(jar_path: Union[str, Path], dest_dir: Union[str, Path]) -> Path:
    """解压JAR文件到指定目录

    Args:
        jar_path: JAR文件路径
        dest_dir: 解压目标目录

    Returns:
        解压目标目录的Path对象

    Raises:
        FileNotFoundError: JAR文件不存在
        zipfile.BadZipFile: JAR文件损坏
        ValueError: 文件不是JAR/ZIP格式
    """
    jar_path = Path(jar_path)
    dest_dir = Path(dest_dir)

    if not jar_path.exists():
        raise FileNotFoundError(f"JAR文件不存在: {jar_path}")

    if not jar_path.is_file():
        raise ValueError(f"路径不是文件: {jar_path}")

    if jar_path.suffix.lower() not in (".jar", ".zip"):
        raise ValueError(f"文件格式不支持，仅支持.jar/.zip: {jar_path}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(jar_path, "r") as zf:
            zf.extractall(dest_dir)
        logger.info(f"JAR解压成功: {jar_path.name} -> {dest_dir}")
    except zipfile.BadZipFile as e:
        logger.error(f"JAR文件损坏: {jar_path} - {e}")
        raise
    except Exception as e:
        logger.error(f"JAR解压失败: {jar_path} - {e}")
        raise

    return dest_dir


def create_jar(src_dir: Union[str, Path], jar_path: Union[str, Path]) -> Path:
    """将目录重新打包为JAR文件

    Args:
        src_dir: 源目录
        jar_path: 输出JAR文件路径

    Returns:
        输出JAR文件路径的Path对象

    Raises:
        FileNotFoundError: 源目录不存在
        ValueError: 源路径不是目录
    """
    src_dir = Path(src_dir)
    jar_path = Path(jar_path)

    if not src_dir.exists():
        raise FileNotFoundError(f"源目录不存在: {src_dir}")

    if not src_dir.is_dir():
        raise ValueError(f"路径不是目录: {src_dir}")

    jar_path.parent.mkdir(parents=True, exist_ok=True)

    # 如果已存在同名文件，先删除
    if jar_path.exists():
        jar_path.unlink()

    with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(src_dir).as_posix()
                zf.write(file_path, arc_name)

    logger.info(f"JAR打包成功: {src_dir} -> {jar_path.name}")
    return jar_path


def validate_jar(jar_path: Union[str, Path]) -> bool:
    """校验JAR文件完整性

    使用zipfile.testzip()检查所有文件的CRC32校验和

    Args:
        jar_path: JAR文件路径

    Returns:
        True表示完整，False表示损坏

    Raises:
        FileNotFoundError: 文件不存在
        zipfile.BadZipFile: 文件不是有效的ZIP/JAR
    """
    jar_path = Path(jar_path)

    if not jar_path.exists():
        raise FileNotFoundError(f"JAR文件不存在: {jar_path}")

    try:
        with zipfile.ZipFile(jar_path, "r") as zf:
            bad_file = zf.testzip()
            if bad_file is None:
                logger.debug(f"JAR校验通过: {jar_path.name}")
                return True
            else:
                logger.error(f"JAR校验失败，损坏的文件: {bad_file}")
                return False
    except zipfile.BadZipFile as e:
        logger.error(f"无效的JAR文件: {jar_path} - {e}")
        raise


def read_jar_file(jar_path: Union[str, Path], inner_path: str, encoding: str = "utf-8") -> str:
    """读取JAR内的单个文件内容

    Args:
        jar_path: JAR文件路径
        inner_path: JAR内文件相对路径
        encoding: 文本编码，默认utf-8

    Returns:
        文件内容字符串

    Raises:
        FileNotFoundError: 文件不存在
        KeyError: JAR内未找到指定文件
    """
    jar_path = Path(jar_path)

    if not jar_path.exists():
        raise FileNotFoundError(f"JAR文件不存在: {jar_path}")

    with zipfile.ZipFile(jar_path, "r") as zf:
        try:
            with zf.open(inner_path) as f:
                return f.read().decode(encoding)
        except KeyError:
            raise KeyError(f"JAR内未找到文件: {inner_path}")


def read_jar_json(jar_path: Union[str, Path], inner_path: str) -> Any:
    """读取JAR内的JSON文件

    Args:
        jar_path: JAR文件路径
        inner_path: JAR内JSON文件相对路径

    Returns:
        JSON反序列化后的对象

    Raises:
        json.JSONDecodeError: JSON格式错误
        KeyError: JAR内未找到指定文件
    """
    content = read_jar_file(jar_path, inner_path)
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {inner_path} - {e}")
        raise


def list_jar_files(jar_path: Union[str, Path]) -> List[str]:
    """列出JAR内所有文件路径

    Args:
        jar_path: JAR文件路径

    Returns:
        JAR内所有文件路径列表（相对路径，使用/分隔符）
    """
    jar_path = Path(jar_path)
    with zipfile.ZipFile(jar_path, "r") as zf:
        return [name for name in zf.namelist() if not name.endswith("/")]


def create_temp_dir(prefix: str = "jar") -> Path:
    """在output/temp/下创建临时目录

    Args:
        prefix: 目录名前缀，如"jar_parser"

    Returns:
        临时目录Path对象
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    temp_root = Path(__file__).resolve().parent.parent / "output" / "temp"
    temp_root.mkdir(parents=True, exist_ok=True)
    temp_dir = temp_root / f"{prefix}_{timestamp}"
    temp_dir.mkdir(parents=True)
    return temp_dir


def cleanup_temp_dir(temp_dir: Union[str, Path]) -> bool:
    """清理临时目录

    Args:
        temp_dir: 临时目录路径

    Returns:
        True表示清理成功
    """
    temp_dir = Path(temp_dir)
    if temp_dir.exists() and temp_dir.is_dir():
        try:
            shutil.rmtree(temp_dir)
            logger.debug(f"临时目录已清理: {temp_dir}")
            return True
        except Exception as e:
            logger.warning(f"临时目录清理失败: {temp_dir} - {e}")
            return False
    return True


def get_file_type(file_path: str) -> str:
    """根据文件扩展名和路径判断文件类型

    Args:
        file_path: JAR内文件相对路径

    Returns:
        文件类型字符串：class/json/png/toml/mcmeta/lang/mixin_config/meta/dir等
    """
    # 目录
    if file_path.endswith("/"):
        return "dir"

    # Mixin配置文件
    name = file_path.split("/")[-1]
    if name.startswith("mixin.") and name.endswith(".json"):
        return "mixin_config"
    if name.endswith(".mixins.json"):
        return "mixin_config"

    # 特殊文件
    if name == "pack.mcmeta":
        return "meta"
    if name == "mods.toml" or name == "neoforge.mods.toml":
        return "metadata"
    if name == "fabric.mod.json":
        return "metadata"

    # 语言文件
    if "/lang/" in file_path and file_path.endswith(".json"):
        return "lang"

    # 按扩展名判断
    ext = Path(name).suffix.lower()
    ext_map = {
        ".class": "class",
        ".json": "json",
        ".png": "png",
        ".jpg": "jpg",
        ".jpeg": "jpeg",
        ".toml": "toml",
        ".mcmeta": "mcmeta",
        ".txt": "txt",
        ".lang": "lang_legacy",
        ".nbt": "nbt",
        ".ogg": "audio",
        ".mp3": "audio",
        ".wav": "audio",
        ".fsh": "shader",
        ".vsh": "shader",
        ".glsl": "shader",
    }
    return ext_map.get(ext, "unknown")


def format_file_size(size_bytes: int) -> str:
    """将字节大小格式化为人类可读字符串

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        格式化后的字符串，如 "1.5 MB"
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def is_file_locked(file_path: Union[str, Path]) -> bool:
    """检查文件是否被占用（Windows文件锁）

    Args:
        file_path: 文件路径

    Returns:
        True表示文件被占用
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    try:
        # 尝试以追加模式打开文件，如果失败说明被占用
        with open(file_path, "a"):
            pass
        return False
    except (PermissionError, OSError):
        return True


def parse_toml(content: str) -> dict:
    """解析TOML内容（使用Python 3.11+内置tomllib）

    Args:
        content: TOML文本内容

    Returns:
        解析后的字典

    Raises:
        ImportError: Python版本过低无tomllib
        tomllib.TOMLDecodeError: TOML格式错误
    """
    try:
        import tomllib
    except ImportError:
        # 兼容Python < 3.11
        try:
            import tomli as tomllib
        except ImportError:
            raise ImportError(
                "需要Python 3.11+内置tomllib，或安装tomli: pip install tomli"
            )

    return tomllib.loads(content)


def read_jar_toml(jar_path: Union[str, Path], inner_path: str) -> dict:
    """读取JAR内的TOML文件

    Args:
        jar_path: JAR文件路径
        inner_path: JAR内TOML文件相对路径

    Returns:
        解析后的字典
    """
    content = read_jar_file(jar_path, inner_path)
    return parse_toml(content)

"""
跨平台路径处理工具
统一处理不同操作系统（Windows / macOS / Linux）的路径差异
"""

import os
import sys
import platform
from pathlib import Path
from functools import lru_cache
from typing import Union, Optional


class PlatformDetector:
    """平台检测器"""
    
    @staticmethod
    def current() -> str:
        """获取当前平台标识"""
        if sys.platform == 'win32':
            return 'win32'
        elif sys.platform == 'darwin':
            return 'darwin'
        else:
            return 'linux'
    
    @staticmethod
    def is_windows() -> bool:
        return sys.platform == 'win32'
    
    @staticmethod
    def is_macos() -> bool:
        return sys.platform == 'darwin'
    
    @staticmethod
    def is_linux() -> bool:
        return sys.platform.startswith('linux')


class PlatformPaths:
    """
    跨平台路径处理工具
    
    统一处理：
    - 路径分隔符（/ vs \\）
    - 用户主目录（~ 展开）
    - 特殊目录（AppData, Application Support 等）
    - 路径大小写（Windows 不敏感，Unix 敏感）
    """
    
    @staticmethod
    @lru_cache(maxsize=128)
    def normalize_path(path: Union[str, Path]) -> str:
        """
        标准化路径（跨平台统一格式）
        
        转换：
        - 分隔符统一为 /
        - 展开 ~ 为用户主目录
        - 转换为绝对路径
        - 去除冗余分隔符
        """
        if isinstance(path, str):
            # 展开 ~ 为实际 home 目录
            if path.startswith('~'):
                path = os.path.expanduser(path)
            path = Path(path)
        
        # 解析为绝对路径
        try:
            absolute = path.resolve()
        except (OSError, RuntimeError):
            # 如果解析失败，使用绝对路径
            absolute = path.absolute()
        
        # 统一使用正斜杠（便于存储和匹配）
        normalized = str(absolute).replace('\\', '/')
        
        # Windows 处理盘符保持原样
        # C:\Users\name → C:/Users/name
        
        return normalized
    
    @staticmethod
    def get_home_dir() -> Path:
        """获取用户主目录（跨平台）"""
        return Path.home()
    
    @staticmethod
    def get_config_dir() -> Path:
        """
        获取配置目录（跨平台）
        
        Windows: ~/AppData/Roaming/OpenClaw
        macOS: ~/Library/Application Support/OpenClaw
        Linux: ~/.config/openclaw
        """
        if sys.platform == 'win32':
            # Windows: AppData/Roaming
            app_data = os.environ.get('APPDATA')
            if app_data:
                return Path(app_data) / 'OpenClaw'
            return Path.home() / 'AppData' / 'Roaming' / 'OpenClaw'
        
        elif sys.platform == 'darwin':
            # macOS: Application Support
            return Path.home() / 'Library' / 'Application Support' / 'OpenClaw'
        
        else:
            # Linux/Unix: XDG_CONFIG_HOME 或 ~/.config
            xdg_config = os.environ.get('XDG_CONFIG_HOME')
            if xdg_config:
                return Path(xdg_config) / 'openclaw'
            return Path.home() / '.config' / 'openclaw'
    
    @staticmethod
    def get_data_dir() -> Path:
        """
        获取数据目录（跨平台）
        
        Windows: ~/AppData/Local/OpenClaw
        macOS: ~/Library/Application Support/OpenClaw
        Linux: ~/.local/share/openclaw
        """
        if sys.platform == 'win32':
            # Windows: AppData/Local
            local_app_data = os.environ.get('LOCALAPPDATA')
            if local_app_data:
                return Path(local_app_data) / 'OpenClaw'
            return Path.home() / 'AppData' / 'Local' / 'OpenClaw'
        
        elif sys.platform == 'darwin':
            return Path.home() / 'Library' / 'Application Support' / 'OpenClaw'
        
        else:
            # Linux: XDG_DATA_HOME 或 ~/.local/share
            xdg_data = os.environ.get('XDG_DATA_HOME')
            if xdg_data:
                return Path(xdg_data) / 'openclaw'
            return Path.home() / '.local' / 'share' / 'openclaw'
    
    @staticmethod
    def get_cache_dir() -> Path:
        """
        获取缓存目录（跨平台）
        
        Windows: ~/AppData/Local/OpenClaw/Cache
        macOS: ~/Library/Caches/OpenClaw
        Linux: ~/.cache/openclaw
        """
        if sys.platform == 'win32':
            local_app_data = os.environ.get('LOCALAPPDATA')
            if local_app_data:
                return Path(local_app_data) / 'OpenClaw' / 'Cache'
            return Path.home() / 'AppData' / 'Local' / 'OpenClaw' / 'Cache'
        
        elif sys.platform == 'darwin':
            return Path.home() / 'Library' / 'Caches' / 'OpenClaw'
        
        else:
            xdg_cache = os.environ.get('XDG_CACHE_HOME')
            if xdg_cache:
                return Path(xdg_cache) / 'openclaw'
            return Path.home() / '.cache' / 'openclaw'
    
    @staticmethod
    def path_matches(pattern: str, target: str) -> bool:
        """
        跨平台路径匹配（处理大小写差异）
        
        Windows: 不区分大小写
        Unix: 区分大小写
        """
        import fnmatch
        
        if sys.platform == 'win32':
            # Windows 不区分大小写
            return fnmatch.fnmatch(target.lower(), pattern.lower())
        else:
            # Unix 区分大小写
            return fnmatch.fnmatch(target, pattern)
    
    @staticmethod
    def expand_user(path: str) -> str:
        """展开 ~ 为用户主目录"""
        if path.startswith('~'):
            return os.path.expanduser(path)
        return path


class WindowsPathAdapter:
    """Windows 特定路径适配器"""
    
    # Windows 特殊目录映射
    SPECIAL_FOLDERS = {
        'Desktop': 'Desktop',
        'Documents': 'Documents',
        'Downloads': 'Downloads',
        'Pictures': 'Pictures',
        'Music': 'Music',
        'Videos': 'Videos',
    }
    
    @classmethod
    def get_special_folder(cls, folder_name: str) -> Optional[Path]:
        """获取 Windows 特殊文件夹路径"""
        if not PlatformDetector.is_windows():
            return None
        
        try:
            import ctypes
            from ctypes.wintypes import HWND, UINT, LPCWSTR, LPWSTR, DWORD
            
            # CSIDL 常量
            CSIDL_MAP = {
                'Desktop': 0x0010,
                'Documents': 0x0005,
                'Downloads': 0x0047,  # Vista+
                'Pictures': 0x0027,
                'Music': 0x000d,
                'Videos': 0x000e,
            }
            
            if folder_name not in CSIDL_MAP:
                return None
            
            # 使用 SHGetFolderPathW 获取路径
            buf = ctypes.create_unicode_buffer(260)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_MAP[folder_name], None, 0, buf)
            return Path(buf.value)
        except Exception:
            return None
    
    @classmethod
    def is_hidden_file(cls, path: Path) -> bool:
        """检查文件是否隐藏（Windows）"""
        if not PlatformDetector.is_windows():
            return path.name.startswith('.')
        
        try:
            import ctypes
            from ctypes.wintypes import DWORD, LPCWSTR
            
            # FILE_ATTRIBUTE_HIDDEN = 0x2
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            return attrs != -1 and (attrs & 0x2) != 0
        except Exception:
            # 回退到检查 . 开头
            return path.name.startswith('.')


# 便捷函数
def normalize_path(path: Union[str, Path]) -> str:
    """标准化路径"""
    return PlatformPaths.normalize_path(path)


def get_config_dir() -> Path:
    """获取配置目录"""
    return PlatformPaths.get_config_dir()


def get_data_dir() -> Path:
    """获取数据目录"""
    return PlatformPaths.get_data_dir()


def get_cache_dir() -> Path:
    """获取缓存目录"""
    return PlatformPaths.get_cache_dir()


def is_windows() -> bool:
    """是否为 Windows 系统"""
    return PlatformDetector.is_windows()


def is_macos() -> bool:
    """是否为 macOS 系统"""
    return PlatformDetector.is_macos()


def is_linux() -> bool:
    """是否为 Linux 系统"""
    return PlatformDetector.is_linux()


def get_current_platform() -> str:
    """获取当前平台标识"""
    return PlatformDetector.current()


def expand_user(path: str) -> str:
    """展开 ~ 为用户主目录"""
    if path.startswith('~'):
        return os.path.expanduser(path)
    return path
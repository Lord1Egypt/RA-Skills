"""
排除项管理器
管理所有排除规则，提供快速排除检查
"""

import re
import fnmatch
from typing import List, Optional
from pathlib import Path

from .models import ExclusionRule, ExclusionType
from ..platform.path_utils import PlatformDetector


class ExclusionManager:
    """
    排除项管理器
    
    职责：
    1. 管理所有排除规则
    2. 提供快速排除检查
    3. 支持动态添加/删除排除规则
    """
    
    # 默认排除规则（跨平台通用）
    DEFAULT_EXCLUSIONS = [
        # 缓存
        ExclusionRule("**/.cache/**", "glob", ExclusionType.CACHE, "通用缓存目录"),
        ExclusionRule("**/__pycache__/**", "glob", ExclusionType.CACHE, "Python缓存"),
        ExclusionRule("**/.pytest_cache/**", "glob", ExclusionType.CACHE, "Pytest缓存"),
        ExclusionRule("**/.mypy_cache/**", "glob", ExclusionType.CACHE, "Mypy缓存"),
        ExclusionRule("**/.ruff_cache/**", "glob", ExclusionType.CACHE, "Ruff缓存"),
        
        # 依赖
        ExclusionRule("**/node_modules/**", "glob", ExclusionType.DEPENDENCY, "Node依赖"),
        ExclusionRule("**/vendor/**", "glob", ExclusionType.DEPENDENCY, "Vendor目录"),
        ExclusionRule("**/.venv/**", "glob", ExclusionType.DEPENDENCY, "Python虚拟环境"),
        ExclusionRule("**/venv/**", "glob", ExclusionType.DEPENDENCY, "Python虚拟环境"),
        ExclusionRule("**/.env/**", "glob", ExclusionType.DEPENDENCY, "Env目录"),
        ExclusionRule("**/env/**", "glob", ExclusionType.DEPENDENCY, "Env目录"),
        
        # Git 内部
        ExclusionRule("**/.git/objects/**", "glob", ExclusionType.CACHE, "Git对象"),
        ExclusionRule("**/.git/hooks/**", "glob", ExclusionType.SYSTEM, "Git hooks"),
        
        # 系统文件 - macOS
        ExclusionRule("**/.DS_Store", "glob", ExclusionType.SYSTEM, "macOS系统文件"),
        ExclusionRule("**/.AppleDouble/**", "glob", ExclusionType.SYSTEM, "macOS资源分支"),
        ExclusionRule("**/.Spotlight-V100/**", "glob", ExclusionType.SYSTEM, "Spotlight索引"),
        ExclusionRule("**/.Trashes/**", "glob", ExclusionType.SYSTEM, "废纸篓"),
        
        # 临时文件
        ExclusionRule("**/*.tmp", "glob", ExclusionType.TEMP, "临时文件"),
        ExclusionRule("**/*.temp", "glob", ExclusionType.TEMP, "临时文件"),
        ExclusionRule("**/~$*", "glob", ExclusionType.TEMP, "Office临时文件"),
        ExclusionRule("**/*.swp", "glob", ExclusionType.TEMP, "Vim交换文件"),
        ExclusionRule("**/*.swo", "glob", ExclusionType.TEMP, "Vim交换文件"),
        ExclusionRule("**/*~", "glob", ExclusionType.TEMP, "备份文件"),
        
        # 构建输出
        ExclusionRule("**/build/**", "glob", ExclusionType.BUILD, "构建目录"),
        ExclusionRule("**/dist/**", "glob", ExclusionType.BUILD, "分发目录"),
        ExclusionRule("**/*.egg-info/**", "glob", ExclusionType.BUILD, "Python包信息"),
        ExclusionRule("**/.tox/**", "glob", ExclusionType.BUILD, "Tox测试环境"),
        ExclusionRule("**/.eggs/**", "glob", ExclusionType.BUILD, "Eggs目录"),
        ExclusionRule("**/target/**", "glob", ExclusionType.BUILD, "Rust构建目录"),
        
        # 日志（过大）
        ExclusionRule("**/*.log", "glob", ExclusionType.CACHE, "日志文件"),
    ]
    
    # Windows 特定排除规则
    WINDOWS_EXCLUSIONS = [
        ExclusionRule("**/Thumbs.db", "glob", ExclusionType.SYSTEM, "Windows缩略图数据库"),
        ExclusionRule("**/desktop.ini", "glob", ExclusionType.SYSTEM, "Windows文件夹配置"),
        ExclusionRule("**/NTUSER.DAT*", "glob", ExclusionType.SYSTEM, "Windows用户注册表"),
        ExclusionRule("**/pagefile.sys", "glob", ExclusionType.SYSTEM, "Windows页面文件"),
        ExclusionRule("**/hiberfil.sys", "glob", ExclusionType.SYSTEM, "Windows休眠文件"),
        ExclusionRule("**/$RECYCLE.BIN/**", "glob", ExclusionType.SYSTEM, "Windows回收站"),
        ExclusionRule("**/System Volume Information/**", "glob", ExclusionType.SYSTEM, "系统卷信息"),
        ExclusionRule("~/AppData/Local/Temp/**", "glob", ExclusionType.TEMP, "Windows临时目录"),
        ExclusionRule("**/Windows/Installer/**", "glob", ExclusionType.CACHE, "Windows安装缓存"),
        ExclusionRule("**/Windows/SoftwareDistribution/**", "glob", ExclusionType.CACHE, "Windows更新缓存"),
        ExclusionRule("**/Windows/Security/Database/**", "glob", ExclusionType.CACHE, "Defender数据库"),
    ]
    
    # macOS 特定排除规则
    MACOS_EXCLUSIONS = [
        ExclusionRule("**/Icon\r", "glob", ExclusionType.SYSTEM, "macOS自定义图标"),
        ExclusionRule("**/.fseventsd/**", "glob", ExclusionType.SYSTEM, "FSEvents数据库"),
        ExclusionRule("**/.TemporaryItems/**", "glob", ExclusionType.TEMP, "临时项目"),
    ]
    
    # Linux 特定排除规则
    LINUX_EXCLUSIONS = [
        ExclusionRule("**/.snap/**", "glob", ExclusionType.CACHE, "Snap缓存"),
        ExclusionRule("**/.flatpak/**", "glob", ExclusionType.CACHE, "Flatpak缓存"),
    ]
    
    def __init__(self):
        self.rules: List[ExclusionRule] = list(self.DEFAULT_EXCLUSIONS)
        self._custom_rules: List[ExclusionRule] = []
        
        # 根据平台添加特定排除规则
        if PlatformDetector.is_windows():
            self.rules.extend(self.WINDOWS_EXCLUSIONS)
        elif PlatformDetector.is_macos():
            self.rules.extend(self.MACOS_EXCLUSIONS)
        elif PlatformDetector.is_linux():
            self.rules.extend(self.LINUX_EXCLUSIONS)
        
        self._build_index()
    
    def _build_index(self):
        """构建排除匹配索引"""
        for rule in self.rules:
            if rule.pattern_type == 'glob':
                try:
                    regex = fnmatch.translate(rule.pattern)
                    rule._matcher = re.compile(regex).match
                except re.error:
                    # 如果正则编译失败，使用简单的字符串匹配
                    rule._matcher = lambda p, target=rule.pattern: fnmatch.fnmatch(p, target)
            elif rule.pattern_type == 'exact':
                rule._matcher = lambda p, target=rule.pattern: p == target
            elif rule.pattern_type == 'regex':
                try:
                    compiled = re.compile(rule.pattern)
                    rule._matcher = compiled.match
                except re.error:
                    rule._matcher = lambda p: False
    
    def is_excluded(self, file_path: str) -> bool:
        """
        检查路径是否被排除
        
        Args:
            file_path: 文件路径（支持 ~ 展开）
            
        Returns:
            是否被排除
        """
        from ..platform.path_utils import normalize_path
        normalized_path = normalize_path(file_path)
        
        for rule in self.rules:
            if rule._matcher and rule._matcher(normalized_path):
                return True
        return False
    
    def get_exclusion_reason(self, file_path: str) -> Optional[str]:
        """获取排除原因（用于调试/日志）"""
        from ..platform.path_utils import normalize_path
        normalized_path = normalize_path(file_path)
        
        for rule in self.rules:
            if rule._matcher and rule._matcher(normalized_path):
                return f"[{rule.exclusion_type.value}] {rule.reason}"
        return None
    
    def get_exclusion_rule(self, file_path: str) -> Optional[ExclusionRule]:
        """获取匹配的排除规则"""
        from ..platform.path_utils import normalize_path
        normalized_path = normalize_path(file_path)
        
        for rule in self.rules:
            if rule._matcher and rule._matcher(normalized_path):
                return rule
        return None
    
    def add_custom_exclusion(self, pattern: str, reason: str, 
                            pattern_type: str = 'glob') -> None:
        """
        添加用户自定义排除规则
        
        Args:
            pattern: 匹配模式
            reason: 排除原因
            pattern_type: 模式类型 (glob/exact/regex)
        """
        rule = ExclusionRule(
            pattern=pattern,
            pattern_type=pattern_type,
            exclusion_type=ExclusionType.CUSTOM,
            reason=reason
        )
        self._custom_rules.append(rule)
        self.rules.append(rule)
        self._build_index()
    
    def remove_custom_exclusion(self, pattern: str) -> bool:
        """
        移除用户自定义排除规则
        
        Args:
            pattern: 匹配模式
            
        Returns:
            是否成功移除
        """
        for i, rule in enumerate(self._custom_rules):
            if rule.pattern == pattern:
                del self._custom_rules[i]
                # 重建规则列表
                self.rules = list(self.DEFAULT_EXCLUSIONS)
                
                if PlatformDetector.is_windows():
                    self.rules.extend(self.WINDOWS_EXCLUSIONS)
                elif PlatformDetector.is_macos():
                    self.rules.extend(self.MACOS_EXCLUSIONS)
                elif PlatformDetector.is_linux():
                    self.rules.extend(self.LINUX_EXCLUSIONS)
                
                self.rules.extend(self._custom_rules)
                self._build_index()
                return True
        return False
    
    def list_custom_exclusions(self) -> List[ExclusionRule]:
        """列出所有自定义排除规则"""
        return list(self._custom_rules)
    
    def list_all_exclusions(self) -> List[ExclusionRule]:
        """列出所有排除规则"""
        return list(self.rules)
    
    def get_stats(self) -> dict:
        """获取排除规则统计"""
        type_counts = {}
        for rule in self.rules:
            type_counts[rule.exclusion_type.value] = type_counts.get(rule.exclusion_type.value, 0) + 1
        
        return {
            'total': len(self.rules),
            'custom': len(self._custom_rules),
            'by_type': type_counts
        }
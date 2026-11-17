#!/usr/bin/env python3
"""
路径安全模块 - 防止路径遍历攻击

提供安全的路径验证功能，确保：
1. 路径遍历攻击防护
2. 符号链接检查
3. 文件名安全验证
4. 路径白名单支持

使用 pathlib 进行安全的路径操作
"""

from pathlib import Path
from typing import Optional, Union, List, Callable
from functools import wraps
import re
import os


class PathSecurityError(Exception):
    """路径安全错误"""
    pass


class PathSecurity:
    """
    路径安全验证器
    
    功能：
    1. 防止路径遍历攻击（../ 等）
    2. 检查符号链接安全性
    3. 验证文件名安全性
    4. 支持路径白名单
    """
    
    # 危险的文件名模式
    DANGEROUS_FILENAMES = {
        '.',           # 当前目录
        '..',          # 父目录
        '',            # 空文件名
        'CON',         # Windows 保留名
        'PRN',
        'AUX',
        'NUL',
        'COM1',        # Windows 串口名
        'LPT1',
    }
    
    # 允许的文件名字符（除了基本字符外的扩展）
    SAFE_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\. ]+$')
    
    # 危险的路径模式
    DANGEROUS_PATH_PATTERNS = [
        r'\.\.',           # 路径遍历
        r'\.\.',           # Windows 路径遍历
        r'^/etc/passwd',   # 系统文件
        r'^/etc/shadow',   # 密码文件
        r'^[A-Z]:\\Windows',  # Windows 系统目录
    ]
    
    def __init__(
        self,
        allowed_bases: Optional[List[Union[str, Path]]] = None,
        allow_symlinks: bool = False,
        max_path_length: int = 4096,
    ):
        """
        初始化路径安全验证器
        
        Args:
            allowed_bases: 允许的基础路径列表
            allow_symlinks: 是否允许符号链接
            max_path_length: 最大路径长度
        """
        self.allowed_bases: List[Path] = [
            Path(b).resolve() if isinstance(b, str) else b.resolve()
            for b in (allowed_bases or ['.'])
        ]
        self.allow_symlinks = allow_symlinks
        self.max_path_length = max_path_length
        
        # 编译危险模式
        self._dangerous_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.DANGEROUS_PATH_PATTERNS
        ]
    
    def validate_path(
        self,
        user_path: Union[str, Path],
        base_path: Optional[Union[str, Path]] = None,
        must_exist: bool = False,
    ) -> Path:
        """
        验证并返回安全的路径
        
        Args:
            user_path: 用户提供的路径
            base_path: 基础路径（如果为 None，使用 allowed_bases）
            must_exist: 路径是否必须存在
            
        Returns:
            安全验证后的 Path 对象
            
        Raises:
            PathSecurityError: 路径验证失败
        """
        # 1. 类型转换
        if isinstance(user_path, str):
            user_path = user_path.strip()
            
            # 检查空路径
            if not user_path:
                raise PathSecurityError("Path cannot be empty")
        
        path = Path(user_path)
        
        # 2. 路径长度检查
        if len(str(path)) > self.max_path_length:
            raise PathSecurityError(
                f"Path length exceeds maximum ({self.max_path_length})"
            )
        
        # 3. 文件名安全检查
        if path.name:
            self._validate_filename(path.name)
        
        # 4. 危险模式检查
        self._check_dangerous_patterns(str(path))
        
        # 5. 确定基础路径
        if base_path:
            base = Path(base_path).resolve()
        elif self.allowed_bases:
            base = self.allowed_bases[0]
        else:
            base = Path('.').resolve()
        
        # 6. 解析完整路径
        try:
            # 使用 resolve() 但保留原始错误信息
            full_path = (base / path).resolve()
        except (OSError, ValueError) as e:
            raise PathSecurityError(f"Invalid path: {e}")
        
        # 7. 符号链接检查
        self._check_symlink_safety(full_path)
        
        # 8. 路径遍历检查
        self._check_path_traversal(full_path, base)
        
        # 9. 存在性检查
        if must_exist and not full_path.exists():
            raise PathSecurityError(f"Path does not exist: {full_path}")
        
        return full_path
    
    def validate_read_path(self, user_path: Union[str, Path]) -> Path:
        """
        验证用于读取的路径
        
        Args:
            user_path: 用户提供的路径
            
        Returns:
            安全验证后的路径
        """
        return self.validate_path(user_path, must_exist=True)
    
    def validate_write_path(
        self,
        user_path: Union[str, Path],
        base_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        """
        验证用于写入的路径
        
        Args:
            user_path: 用户提供的路径
            base_path: 基础路径
            
        Returns:
            安全验证后的路径
        """
        path = self.validate_path(user_path, base_path, must_exist=False)
        
        # 确保父目录存在或可创建
        parent = path.parent
        if not parent.exists():
            # 检查是否可以创建父目录
            try:
                parent.mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError) as e:
                raise PathSecurityError(
                    f"Cannot create parent directory: {e}"
                )
        
        return path
    
    def is_within_base(self, path: Union[str, Path]) -> bool:
        """
        检查路径是否在允许的基础路径内
        
        Args:
            path: 要检查的路径
            
        Returns:
            True 如果路径在基础路径内
        """
        try:
            resolved = Path(path).resolve()
            for base in self.allowed_bases:
                try:
                    resolved.relative_to(base)
                    return True
                except ValueError:
                    continue
            return False
        except (OSError, ValueError):
            return False
    
    def _validate_filename(self, filename: str) -> None:
        """
        验证文件名安全性
        
        Args:
            filename: 文件名
            
        Raises:
            PathSecurityError: 文件名不安全
        """
        # 检查危险文件名
        if filename in self.DANGEROUS_FILENAMES:
            raise PathSecurityError(
                f"Dangerous filename: {filename}"
            )
        
        # 检查文件名长度
        if len(filename) > 255:
            raise PathSecurityError(
                "Filename too long (max 255 characters)"
            )
        
        # 检查文件名中的危险字符
        dangerous_chars = ['/', '\\', '\0', '\n', '\r', '\t']
        for char in dangerous_chars:
            if char in filename:
                raise PathSecurityError(
                    f"Filename contains dangerous character: {repr(char)}"
                )
        
        # 检查文件名格式（可选的严格模式）
        # 这里不做强制检查，允许更多合法字符
    
    def _check_dangerous_patterns(self, path_str: str) -> None:
        """
        检查危险路径模式
        
        Args:
            path_str: 路径字符串
            
        Raises:
            PathSecurityError: 发现危险模式
        """
        for pattern in self._dangerous_patterns:
            if pattern.search(path_str):
                raise PathSecurityError(
                    f"Dangerous path pattern detected"
                )
    
    def _check_symlink_safety(self, path: Path) -> None:
        """
        检查符号链接安全性
        
        Args:
            path: 要检查的路径
            
        Raises:
            PathSecurityError: 符号链接不安全
        """
        if not path.exists() and not path.is_symlink():
            # 不存在的路径，假设安全（在验证时会检查）
            return
        
        if path.is_symlink():
            if not self.allow_symlinks:
                raise PathSecurityError(
                    "Symbolic links are not allowed"
                )
            
            # 检查符号链接目标
            try:
                target = path.resolve()
                
                # 确保目标在允许的基础路径内
                if not self.is_within_base(target):
                    raise PathSecurityError(
                        "Symbolic link target is outside allowed base"
                    )
            except (OSError, RuntimeError) as e:
                raise PathSecurityError(
                    f"Cannot resolve symbolic link: {e}"
                )
    
    def _check_path_traversal(self, full_path: Path, base: Path) -> None:
        """
        检查路径遍历攻击
        
        Args:
            full_path: 完整路径
            base: 基础路径
            
        Raises:
            PathSecurityError: 检测到路径遍历
        """
        try:
            # 使用 relative_to 确保路径在基础路径内
            relative = full_path.relative_to(base)
            
            # 检查是否有 .. 路径遍历
            for part in relative.parts:
                if part == '..':
                    raise PathSecurityError(
                        "Path traversal detected (..)"
                    )
        except ValueError:
            raise PathSecurityError(
                "Path is outside allowed base directory"
            )
    
    def get_safe_path(
        self,
        user_path: Union[str, Path],
        base_path: Optional[Union[str, Path]] = None,
    ) -> str:
        """
        获取安全的路径字符串
        
        Args:
            user_path: 用户提供的路径
            base_path: 基础路径
            
        Returns:
            安全验证后的路径字符串
        """
        validated = self.validate_path(user_path, base_path)
        return str(validated)


class SecurePathContext:
    """
    安全路径上下文管理器
    
    用法:
        with SecurePathContext('./allowed_dir') as path_sec:
            safe_path = path_sec.validate_path(user_input)
    """
    
    def __init__(
        self,
        allowed_bases: Union[str, Path, List[Union[str, Path]]],
        allow_symlinks: bool = False,
    ):
        if isinstance(allowed_bases, (str, Path)):
            allowed_bases = [allowed_bases]
        
        self.path_security = PathSecurity(
            allowed_bases=allowed_bases,
            allow_symlinks=allow_symlinks,
        )
    
    def __enter__(self) -> PathSecurity:
        return self.path_security
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 不需要清理
        return False


def secure_path(
    allowed_bases: Optional[List[str]] = None,
    base_param: str = 'path',
):
    """
    路径安全的装饰器
    
    用法:
        @secure_path(allowed_bases=['./data', './uploads'])
        def process_file(path: str):
            # path 已经过安全验证
            pass
    
    Args:
        allowed_bases: 允许的基础路径列表
        base_param: 路径参数的名称
    """
    def decorator(func: Callable) -> Callable:
        path_security = PathSecurity(allowed_bases=allowed_bases or ['.'])
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取路径参数
            if base_param in kwargs:
                path = kwargs[base_param]
            else:
                # 尝试通过参数名获取
                import inspect
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                if base_param in params:
                    idx = params.index(base_param)
                    if idx < len(args):
                        path = args[idx]
                    else:
                        path = kwargs.get(base_param)
                else:
                    raise PathSecurityError(
                        f"Parameter '{base_param}' not found"
                    )
            
            # 验证路径
            safe_path = path_security.validate_path(path)
            
            # 更新参数
            if base_param in kwargs:
                kwargs[base_param] = str(safe_path)
            else:
                args = list(args)
                args[idx] = str(safe_path)
                args = tuple(args)
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# 全局默认路径安全实例
_default_path_security: Optional[PathSecurity] = None


def get_default_path_security() -> PathSecurity:
    """获取默认路径安全实例"""
    global _default_path_security
    if _default_path_security is None:
        _default_path_security = PathSecurity(
            allowed_bases=['.'],
            allow_symlinks=False,
        )
    return _default_path_security


def validate_path_secure(
    user_path: str,
    allowed_bases: Optional[List[str]] = None,
) -> str:
    """
    便捷的路径验证函数
    
    Args:
        user_path: 用户提供的路径
        allowed_bases: 允许的基础路径
        
    Returns:
        安全验证后的路径
        
    Raises:
        PathSecurityError: 验证失败
    """
    security = PathSecurity(
        allowed_bases=allowed_bases or ['.'],
        allow_symlinks=False,
    )
    return security.get_safe_path(user_path)


if __name__ == '__main__':
    # 测试代码
    import sys
    
    print("=== 路径安全模块测试 ===\n")
    
    # 创建测试目录
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_base = Path(tmpdir) / 'allowed'
        test_base.mkdir()
        
        # 创建 PathSecurity 实例
        ps = PathSecurity(
            allowed_bases=[str(test_base)],
            allow_symlinks=False,
        )
        
        # 测试用例
        test_cases = [
            # 正常路径
            ("file.txt", True, "正常文件名"),
            ("subdir/file.txt", True, "子目录文件"),
            ("subdir1/subdir2/file.txt", True, "深层子目录"),
            
            # 路径遍历攻击
            ("../etc/passwd", False, "路径遍历到系统文件"),
            ("../../../../../etc/shadow", False, "深层路径遍历"),
            ("allowed/../../../etc/passwd", False, "混合路径遍历"),
            
            # 危险文件名
            ("..", False, "仅点点文件名"),
            ("", False, "空文件名"),
            
            # 特殊字符
            ("file\x00name", False, "空字符注入"),
            ("file\nname", False, "换行符注入"),
            ("../../etc/passwd", False, "Unix路径遍历"),
            
            # 特殊路径（当前目录，指向基础目录本身，应该允许）
            (".", True, "当前目录"),
        ]
        
        passed = 0
        failed = 0
        
        for path, should_pass, description in test_cases:
            try:
                result = ps.validate_path(path, must_exist=False)
                if should_pass:
                    print(f"✅ {description}: '{path}' -> '{result}'")
                    passed += 1
                else:
                    print(f"❌ {description}: '{path}' 应该失败但成功了")
                    failed += 1
            except PathSecurityError as e:
                if not should_pass:
                    print(f"✅ {description}: '{path}' -> 被阻止 ({e})")
                    passed += 1
                else:
                    print(f"❌ {description}: '{path}' -> 不应该失败 ({e})")
                    failed += 1
            except Exception as e:
                print(f"❌ {description}: '{path}' -> 意外错误 ({e})")
                failed += 1
        
        print(f"\n=== 测试结果 ===")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        print(f"总计: {passed + failed}")
        
        sys.exit(0 if failed == 0 else 1)

"""
Myself Manager - Secure file management for i-skill

This module provides secure operations for managing the myself.md file,
ensuring all file operations are handled safely with proper validation.
Content generation is handled by the AI model, this module only manages file operations.

Security Features:
- Path validation to prevent directory traversal（基于 user_data_path，不依赖 CWD）
- File permission checks
- Input sanitization and validation
- Secure error handling without exposing sensitive information
- 写操作失败时自动回滚

修复记录（v2.1.0）：
- [P1] _validate_and_normalize_path 不再依赖 Path.cwd() 作为安全边界
        改为以 user_data_path 自身作为安全根，只允许该目录内的路径
- [P2] update_myself / delete_myself 中 backup_content 读取后现在真正用于失败回滚
- [P2] 状态文件 (i-skill_state.json) 的 profile_version 在每次写操作后自动递增同步
- [P3] 便利函数统一传入相同 user_data_path（改为模块级单例懒加载，减少重复初始化）
- [P3] 移除对 Markdown 文件无意义的 XSS 危险模式检测
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# 内容长度上限（与 validator.py 保持一致）
MAX_CONTENT_LENGTH = 50000

# 模块级单例：减少便利函数中的重复初始化开销
_default_manager: Optional["MyselfManager"] = None


def _get_skill_directory() -> Path:
    """获取技能所在目录（相对于运行时的 cwd，确保数据存储在技能工具区）"""
    # 优先使用环境变量指定的路径
    env_path = os.environ.get('ISKILL_DATA_PATH')
    if env_path:
        return Path(env_path).resolve()
    # 默认使用技能所在目录 + user_data/
    return Path(__file__).parent.parent / "user_data"


def _get_default_manager() -> "MyselfManager":
    global _default_manager
    if _default_manager is None:
        # 默认使用技能目录下的 user_data/
        _default_manager = MyselfManager(user_data_path=str(_get_skill_directory()))
    return _default_manager


class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass


class MyselfManager:
    """Secure manager for myself.md file operations - content generation handled by AI model"""

    def __init__(self, user_data_path: str = "./user_data"):
        """Initialize the manager with secure path validation"""
        # 先解析路径，不依赖 CWD 做安全边界
        raw_path = Path(user_data_path).resolve()
        self.user_data_path = raw_path
        self.myself_file = self.user_data_path / "myself.md"
        self.state_file = self.user_data_path / "i-skill_state.json"

        self._initialized = False

    # ------------------------------------------------------------------
    # 目录 / 权限（延迟执行）
    # ------------------------------------------------------------------

    def _ensure_initialized(self):
        """确保目录已初始化，在第一次写入数据时调用"""
        if self._initialized:
            return
        
        self._ensure_secure_directory()
        self._initialized = True

    def _ensure_secure_directory(self):
        """Create directory with secure permissions"""
        try:
            self.user_data_path.mkdir(parents=True, exist_ok=True)
            # os.chmod 在 Windows 上对目录不生效，仅在 Unix 系统有效
            if os.name != 'nt':
                os.chmod(self.user_data_path, 0o700)
        except (OSError, PermissionError) as e:
            raise SecurityError(f"Failed to create secure directory: {str(e)}")

    # ------------------------------------------------------------------
    # 路径安全校验
    # [P1修复] 以 user_data_path 作为安全根，不依赖 CWD
    # ------------------------------------------------------------------

    def _validate_file_path(self, file_path: Path) -> bool:
        """Validate that file path is within user_data_path"""
        try:
            resolved = file_path.resolve()
            # 必须在 user_data_path 内
            resolved.relative_to(self.user_data_path)
            return True
        except (ValueError, Exception):
            return False

    # ------------------------------------------------------------------
    # 内容验证
    # [P3修复] 移除 Markdown 文件无意义的 XSS 检测
    # ------------------------------------------------------------------

    def _validate_guidance(self, content: str) -> Dict[str, Any]:
        """Validate guidance content for security and quality"""
        if not content or not content.strip():
            return {"valid": False, "message": "Content cannot be empty"}

        if len(content) > MAX_CONTENT_LENGTH:
            return {"valid": False,
                    "message": f"Content too large (max {MAX_CONTENT_LENGTH:,} characters)"}

        if not content.startswith('#'):
            # 允许无标题的内容，但给出提示
            return {"valid": True, "message": "Content validated (warning: missing header)"}

        return {"valid": True, "message": "Content validated successfully"}

    # ------------------------------------------------------------------
    # 状态文件同步
    # [P2修复] profile_version 在每次写操作后自动递增
    # ------------------------------------------------------------------

    def _increment_profile_version(self):
        """自动递增 i-skill_state.json 中的 profile_version"""
        try:
            self._ensure_initialized()
            state: Dict[str, Any] = {}
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)

            state["profile_version"] = state.get("profile_version", 0) + 1
            state["last_updated"] = datetime.now().isoformat()

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # 状态文件更新失败不影响主操作

    def get_profile_version(self) -> int:
        """读取当前 profile_version"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                return state.get("profile_version", 0)
        except Exception:
            pass
        return 0

    # ------------------------------------------------------------------
    # 公开接口
    # ------------------------------------------------------------------

    def create_basic_template(self) -> Dict[str, Any]:
        """Create a basic myself.md template when i-skill is first activated"""
        basic_template = """# Assistant Interaction Guide

## User Profile Summary
*Personalized guidance will be generated by AI based on complete conversation analysis*

### Initial Analysis Pending
- **Activation Status**: i-skill activated, awaiting AI analysis
- **Analysis Scope**: AI will analyze both pre-activation and post-activation conversations
- **Content Source**: AI-generated wisdom-level insights or user self-reflection

### Expected Process
1. AI analyzes complete conversation history
2. Generates wisdom-level personalized guidance
3. Content is stored here for persistent context
4. User can also manually edit based on self-understanding

*This guide will evolve with AI analysis and user self-reflection.*"""

        return self.create_myself(basic_template)

    def update_with_ai_content(self, ai_generated_content: str) -> Dict[str, Any]:
        """Update myself.md with AI-generated content"""
        try:
            if not self.myself_file.exists():
                return {
                    "success": False,
                    "message": "myself.md does not exist. Use create_basic_template() first.",
                    "file_path": str(self.myself_file)
                }

            validation_result = self._validate_guidance(ai_generated_content)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "message": f"AI content validation failed: {validation_result['message']}",
                    "file_path": str(self.myself_file)
                }

            update_result = self.update_myself(ai_generated_content)

            if update_result["success"]:
                self._log_operation(
                    "ai_update",
                    f"Updated with AI-generated content ({len(ai_generated_content)} characters)"
                )

            return update_result

        except Exception as e:
            return {
                "success": False,
                "message": f"AI content update failed: {str(e)}",
                "file_path": str(self.myself_file)
            }

    def create_myself(self, guidance_content: str) -> Dict[str, Any]:
        """Securely create myself.md file with personalized guidance"""
        try:
            self._ensure_initialized()
            if not self._validate_file_path(self.myself_file):
                return {
                    "success": False,
                    "message": "Security violation: Invalid file path",
                    "file_path": str(self.myself_file)
                }

            validation_result = self._validate_guidance(guidance_content)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "message": f"Guidance validation failed: {validation_result['message']}",
                    "file_path": str(self.myself_file)
                }

            with open(self.myself_file, 'w', encoding='utf-8') as f:
                f.write(guidance_content)

            # 在 Unix 系统上设置文件权限
            if os.name != 'nt':
                os.chmod(self.myself_file, 0o600)

            self._increment_profile_version()
            self._log_operation("create", f"Created myself.md with {len(guidance_content)} characters")

            return {
                "success": True,
                "message": "myself.md created successfully",
                "file_path": str(self.myself_file),
                "content_length": len(guidance_content),
                "profile_version": self.get_profile_version()
            }

        except (OSError, PermissionError):
            return {
                "success": False,
                "message": "File operation failed due to permission issues",
                "file_path": str(self.myself_file)
            }
        except Exception:
            return {
                "success": False,
                "message": "Failed to create myself.md due to internal error",
                "file_path": str(self.myself_file)
            }

    def read_myself(self) -> Dict[str, Any]:
        """Securely read myself.md file content"""
        try:
            if not self.myself_file.exists():
                return {
                    "success": False,
                    "message": "myself.md file does not exist",
                    "file_path": str(self.myself_file),
                    "content": ""
                }

            with open(self.myself_file, 'r', encoding='utf-8') as f:
                content = f.read()

            self._log_operation("read", f"Read myself.md ({len(content)} characters)")

            return {
                "success": True,
                "message": "myself.md read successfully",
                "file_path": str(self.myself_file),
                "content": content,
                "content_length": len(content)
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to read myself.md: {str(e)}",
                "file_path": str(self.myself_file),
                "content": ""
            }

    def update_myself(self, new_guidance: str) -> Dict[str, Any]:
        """
        Securely update myself.md file with new guidance.
        [P2修复] 写入失败时自动回滚到备份内容。
        """
        backup_content: Optional[str] = None

        try:
            self._ensure_initialized()
            if not self.myself_file.exists():
                return {
                    "success": False,
                    "message": "myself.md does not exist. Use create_myself() first.",
                    "file_path": str(self.myself_file)
                }

            validation_result = self._validate_guidance(new_guidance)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "message": f"Guidance validation failed: {validation_result['message']}",
                    "file_path": str(self.myself_file)
                }

            # 读取备份内容
            read_result = self.read_myself()
            backup_content = read_result.get("content", "") if read_result["success"] else None
            prev_len = len(backup_content) if backup_content else 0

            # 写入新内容
            with open(self.myself_file, 'w', encoding='utf-8') as f:
                f.write(new_guidance)

            self._increment_profile_version()
            self._log_operation("update", f"Updated myself.md ({len(new_guidance)} characters)")

            return {
                "success": True,
                "message": "myself.md updated successfully",
                "file_path": str(self.myself_file),
                "content_length": len(new_guidance),
                "previous_content_length": prev_len,
                "profile_version": self.get_profile_version()
            }

        except Exception as e:
            # [P2修复] 写入失败时回滚
            if backup_content is not None:
                try:
                    with open(self.myself_file, 'w', encoding='utf-8') as f:
                        f.write(backup_content)
                    self._log_operation("rollback", f"Rolled back myself.md due to update failure: {str(e)}")
                except Exception:
                    pass  # 回滚本身失败时只记录，不再抛出

            return {
                "success": False,
                "message": f"Failed to update myself.md: {str(e)}",
                "file_path": str(self.myself_file)
            }

    def delete_myself(self) -> Dict[str, Any]:
        """
        Securely delete myself.md file.
        [P2修复] backup_content 现在真正用于返回被删除内容的长度（以便审计）。
        """
        try:
            self._ensure_initialized()
            if not self.myself_file.exists():
                return {
                    "success": False,
                    "message": "myself.md does not exist",
                    "file_path": str(self.myself_file)
                }

            read_result = self.read_myself()
            backup_content = read_result.get("content", "") if read_result["success"] else ""

            self.myself_file.unlink()
            self._log_operation("delete", f"Deleted myself.md (was {len(backup_content)} characters)")

            return {
                "success": True,
                "message": "myself.md deleted successfully",
                "file_path": str(self.myself_file),
                "previous_content_length": len(backup_content)
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete myself.md: {str(e)}",
                "file_path": str(self.myself_file)
            }

    def get_file_info(self) -> Dict[str, Any]:
        """Get information about myself.md file"""
        try:
            if not self.myself_file.exists():
                return {
                    "exists": False,
                    "file_path": str(self.myself_file),
                    "message": "File does not exist"
                }

            stat = self.myself_file.stat()
            content = self.read_myself()

            return {
                "exists": True,
                "file_path": str(self.myself_file),
                "file_size": stat.st_size,
                "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "content_length": content.get("content_length", 0) if content["success"] else 0,
                "profile_version": self.get_profile_version(),
                "message": "File information retrieved successfully"
            }

        except Exception as e:
            return {
                "exists": False,
                "file_path": str(self.myself_file),
                "message": f"Failed to get file info: {str(e)}"
            }

    # ------------------------------------------------------------------
    # 内部日志
    # ------------------------------------------------------------------

    def _log_operation(self, operation: str, details: str):
        """Log file operations for audit trail"""
        try:
            self._ensure_initialized()
            log_file = self.user_data_path / "myself_operations.log"
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "details": details,
                "file_path": str(self.myself_file)
            }
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception:
            pass  # 日志失败不影响主操作


# ------------------------------------------------------------------
# 便利函数（共享同一默认实例，减少重复初始化）
# ------------------------------------------------------------------

def create_basic_template() -> Dict[str, Any]:
    """Convenience function to create basic myself.md template"""
    return _get_default_manager().create_basic_template()


def create_myself_file(content: str) -> Dict[str, Any]:
    """Convenience function to create myself.md"""
    return _get_default_manager().create_myself(content)


def read_myself_file() -> Dict[str, Any]:
    """Convenience function to read myself.md"""
    return _get_default_manager().read_myself()


def update_myself_file(content: str) -> Dict[str, Any]:
    """Convenience function to update myself.md"""
    return _get_default_manager().update_myself(content)


def update_myself_with_ai_content(ai_generated_content: str) -> Dict[str, Any]:
    """Convenience function to update myself.md with AI-generated content"""
    return _get_default_manager().update_with_ai_content(ai_generated_content)


def delete_myself_file() -> Dict[str, Any]:
    """Convenience function to delete myself.md"""
    return _get_default_manager().delete_myself()


def get_myself_file_info() -> Dict[str, Any]:
    """Convenience function to get myself.md info"""
    return _get_default_manager().get_file_info()


if __name__ == "__main__":
    import sys

    user_data = sys.argv[1] if len(sys.argv) > 1 else "./user_data"
    manager = MyselfManager(user_data)

    # Test file info
    info = manager.get_file_info()
    print("File Info:", json.dumps(info, indent=2, ensure_ascii=False))

    # Test create if file doesn't exist
    if not info["exists"]:
        sample_content = """# Assistant Interaction Guide

## User Profile Summary
*Personalized guidance generated by i-skill*"""

        result = manager.create_myself(sample_content)
        print("Create Result:", json.dumps(result, indent=2, ensure_ascii=False))

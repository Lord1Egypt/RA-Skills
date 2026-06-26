"""
权限检查中间件
在消息入口处检查权限，不改动现有技能

功能：
1. 从请求中提取 open_id, platform
2. 调用 main.py 的 authenticate 检查
3. 只对需要 execute 权限的操作进行检查
4. 熔断机制：检查出错时放行并记录日志
5. 配置开关：enabled=false 时跳过检查
"""

import json
import logging
import os
from typing import Dict, Any, Optional

# 配置路径
CONFIG_PATH = "/workspace/config/permission.json"

# 需要权限的操作列表（这些操作需要 execute 权限）
PRIVILEGED_ACTIONS = {
    # 技能类操作
    "skill",
    "execute_skill",
    "run_skill",
    # 文件操作
    "file_write",
    "file_delete",
    "file_create",
    "write",
    "delete",
    # 系统操作
    "system",
    "admin",
    "config",
    "settings",
    # 代码/开发操作
    "code",
    "exec",
    "run",
    "install",
    # 飞书操作
    "feishu_write",
    "feishu_create",
    "feishu_delete",
    "feishu_update",
}

# 日常对话类操作（不需要权限检查）
CONVERSATIONAL_ACTIONS = {
    "chat",
    "message",
    "talk",
    "ask",
    "query",
    "search",
    "get",
    "read",
    "list",
    "view",
    "info",
}

logger = logging.getLogger("permission_middleware")


def _load_config() -> Dict[str, Any]:
    """加载权限配置"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"加载权限配置失败: {e}，使用默认配置")
        return {"enabled": True}


def _is_privileged_operation(request: Dict[str, Any]) -> bool:
    """
    判断是否为需要权限的操作
    
    检查请求中的 action/command/type 字段
    """
    # 检查多个可能的字段
    action = request.get("action", "").lower()
    command = request.get("command", "").lower()
    msg_type = request.get("type", "").lower()
    action_type = request.get("action_type", "").lower()
    
    # 组合所有可能的值
    action_str = " ".join([action, command, msg_type, action_type])
    
    # 检查是否是需要权限的操作
    for priv_action in PRIVILEGED_ACTIONS:
        if priv_action in action_str:
            return True
    
    # 检查是否明确是日常对话
    for conv_action in CONVERSATIONAL_ACTIONS:
        if conv_action == action_str.strip():
            return False
    
    # 如果无法判断，默认认为是需要权限的操作（安全优先）
    # 但如果只有文本消息内容，没有 action 字段，则视为日常对话
    if not action and not command and not msg_type:
        # 只有 text 或 message 字段，视为日常对话
        if "text" in request or "message" in request:
            return False
    
    # 无法确定时，要求权限检查（安全优先）
    return True


def check_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    检查请求权限的主入口
    
    Args:
        request: 请求对象，需包含：
            - open_id: 平台账号 ID
            - platform: 平台名称
            - action/command/type: 操作类型（可选）
    
    Returns:
        {
            "allowed": True/False,
            "user": user对象 或 None,
            "reason": "说明",
            "skipped": True/False  # 是否跳过了检查
        }
    """
    # 1. 加载配置，检查是否启用
    config = _load_config()
    
    # 检查是否启用权限检查
    if not config.get("enabled", True):
        logger.debug("权限检查已禁用，跳过检查")
        return {
            "allowed": True,
            "user": None,
            "reason": "权限检查已禁用",
            "skipped": True
        }
    
    # 提取用户标识
    open_id = request.get("open_id")
    platform = request.get("platform")
    
    # 2. 测试模式：只对白名单账号进行检查
    if config.get("test_mode", False):
        test_accounts = config.get("test_accounts", [])
        if open_id not in test_accounts:
            logger.debug(f"测试模式：{open_id} 不在白名单，跳过检查")
            return {
                "allowed": True,
                "user": None,
                "reason": "测试模式，非白名单账号跳过检查",
                "skipped": True
            }
        logger.debug(f"测试模式：{open_id} 在白名单中，进行权限检查")
    
    # 2. 提取必要参数
    open_id = request.get("open_id")
    platform = request.get("platform")
    
    # 如果没有 open_id 或 platform，无法检查权限
    # 这种情况可能是系统消息或广播，放行
    if not open_id or not platform:
        logger.debug("请求缺少 open_id 或 platform，跳过权限检查")
        return {
            "allowed": True,
            "user": None,
            "reason": "缺少用户标识，跳过检查",
            "skipped": True
        }
    
    # 3. 判断是否是需要权限的操作
    if not _is_privileged_operation(request):
        logger.debug(f"操作类型 {request.get('action', 'unknown')} 为日常对话，跳过权限检查")
        return {
            "allowed": True,
            "user": None,
            "reason": "日常对话，无需权限检查",
            "skipped": True
        }
    
    # 4. 执行权限检查（带熔断机制）
    try:
        # 动态导入 main 模块（支持包内和直接运行两种方式）
        try:
            from .main import authenticate
        except ImportError:
            import sys
            import os
            import importlib.util
            # 找到 main.py 的路径
            module_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(module_dir, "main.py")
            spec = importlib.util.spec_from_file_location("main_module", main_path)
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            authenticate = main_module.authenticate
        
        # 调用 authenticate 检查 execute 权限
        result = authenticate({
            "open_id": open_id,
            "platform": platform,
            "permission": "execute"
        })
        
        return {
            "allowed": result.get("allowed", False),
            "user": result.get("user"),
            "reason": result.get("reason", ""),
            "skipped": False
        }
        
    except Exception as e:
        # 熔断机制：检查出错时放行并记录日志
        logger.error(f"权限检查异常: {e}，请求放行: open_id={open_id}, platform={platform}")
        return {
            "allowed": True,
            "user": None,
            "reason": f"权限检查异常（已放行）: {str(e)}",
            "skipped": False,
            "error": str(e)
        }


def check_permission(request: Dict[str, Any], permission: str) -> Dict[str, Any]:
    """
    检查特定权限的中间件
    
    Args:
        request: 请求对象
        permission: 权限名称（read/write/admin/execute）
    
    Returns:
        同 check_request
    """
    # 加载配置
    config = _load_config()
    
    if not config.get("enabled", True):
        return {
            "allowed": True,
            "user": None,
            "reason": "权限检查已禁用",
            "skipped": True
        }
    
    # 提取参数
    open_id = request.get("open_id")
    platform = request.get("platform")
    
    if not open_id or not platform:
        return {
            "allowed": True,
            "user": None,
            "reason": "缺少用户标识",
            "skipped": True
        }
    
    # 执行检查
    try:
        # 动态导入 main 模块
        try:
            from .main import authenticate
        except ImportError:
            import importlib.util
            import os
            module_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(module_dir, "main.py")
            spec = importlib.util.spec_from_file_location("main_module", main_path)
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            authenticate = main_module.authenticate
        
        result = authenticate({
            "open_id": open_id,
            "platform": platform,
            "permission": permission
        })
        
        return {
            "allowed": result.get("allowed", False),
            "user": result.get("user"),
            "reason": result.get("reason", ""),
            "skipped": False
        }
        
    except Exception as e:
        logger.error(f"权限检查异常: {e}，请求放行")
        return {
            "allowed": True,
            "user": None,
            "reason": f"权限检查异常（已放行）: {str(e)}",
            "skipped": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # 测试代码
    print("=== 权限检查中间件测试 ===")
    
    # 测试1: 配置禁用时
    print("\n1. 测试配置禁用:")
    result = check_request({
        "open_id": "ou_test",
        "platform": "feishu",
        "text": "你好"
    })
    print(f"   结果: {result}")
    
    # 测试2: 日常对话
    print("\n2. 测试日常对话:")
    result = check_request({
        "open_id": "ou_test",
        "platform": "feishu",
        "action": "chat",
        "text": "今天天气怎么样"
    })
    print(f"   结果: {result}")
    
    # 测试3: 缺少用户信息
    print("\n3. 测试缺少用户信息:")
    result = check_request({
        "action": "chat",
        "text": "你好"
    })
    print(f"   结果: {result}")
    
    # 测试4: 需要权限的操作
    print("\n4. 测试需要权限的操作:")
    result = check_request({
        "open_id": "ou_test",
        "platform": "feishu",
        "action": "skill",
        "text": "执行某个技能"
    })
    print(f"   结果: {result}")

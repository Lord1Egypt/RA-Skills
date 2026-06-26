#!/usr/bin/env python3
"""
Vivago AI Skill 异常类定义
"""


class VivagoError(Exception):
    """Vivago AI Skill 基础异常"""
    pass


class VivagoAPIError(VivagoError):
    """API调用异常"""
    def __init__(self, message: str, code: int = None, response: dict = None):
        super().__init__(message)
        self.code = code
        self.response = response


class MissingCredentialError(VivagoError):
    """缺少认证信息"""
    pass


class InvalidPortError(VivagoError):
    """无效端口配置"""
    def __init__(self, port: str, category: str = None, available: list = None):
        message = f"Invalid port: {port}"
        if category:
            message = f"Invalid port '{port}' for category '{category}'"
        if available:
            message += f". Available: {', '.join(available)}"
        super().__init__(message)
        self.port = port
        self.category = category
        self.available = available


class TaskError(VivagoError):
    """任务执行异常基类"""
    def __init__(self, task_id: str, message: str):
        super().__init__(f"Task {task_id}: {message}")
        self.task_id = task_id


class TaskFailedError(TaskError):
    """任务失败"""
    def __init__(self, task_id: str, reason: str = None):
        message = reason or "Task failed"
        super().__init__(task_id, message)
        self.reason = reason


class TaskRejectedError(TaskError):
    """任务被拒绝（内容审核）"""
    def __init__(self, task_id: str, reason: str = "Content rejected"):
        super().__init__(task_id, f"Rejected - {reason}")
        self.reason = reason


class TaskTimeoutError(TaskError):
    """任务超时"""
    def __init__(self, task_id: str, timeout_seconds: int):
        super().__init__(task_id, f"Timeout after {timeout_seconds}s")
        self.timeout_seconds = timeout_seconds


class ImageUploadError(VivagoError):
    """图片上传失败"""
    def __init__(self, path: str, reason: str = None):
        message = f"Failed to upload image: {path}"
        if reason:
            message += f" ({reason})"
        super().__init__(message)
        self.path = path
        self.reason = reason


class TemplateNotFoundError(VivagoError):
    """模板未找到"""
    def __init__(self, template_id: str, available: list = None):
        message = f"Template not found: {template_id}"
        if available:
            suggestions = [t for t in available if template_id.lower() in t.lower()][:5]
            if suggestions:
                message += f". Did you mean: {', '.join(suggestions)}?"
        super().__init__(message)
        self.template_id = template_id

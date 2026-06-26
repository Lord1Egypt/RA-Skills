"""技能基类模板 - 所有生成的技能必须继承此基类"""

from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseSkill(ABC):
    """技能基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0.0"
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能逻辑
        
        Args:
            **kwargs: 执行参数
            
        Returns:
            Dict[str, Any]: 执行结果，必须包含 'success' 键
                - success: bool, 是否成功
                - result: Any, 成功时的结果
                - error: str, 失败时的错误信息
        """
        pass
    
    @abstractmethod
    def validate_input(self, inputs: dict) -> bool:
        """
        验证输入参数
        
        Args:
            inputs: 输入参数字典
            
        Returns:
            bool: 输入是否有效
        """
        pass
    
    def handle_error(self, error: Exception) -> dict:
        """
        默认错误处理
        
        可以重写此方法实现自定义错误处理
        
        Args:
            error: 异常对象
            
        Returns:
            dict: 错误信息字典
        """
        return {
            "success": False,
            "error": str(error),
            "type": type(error).__name__,
            "suggestion": "请检查输入参数或联系管理员"
        }
    
    def get_info(self) -> dict:
        """获取技能信息"""
        return {
            "name": self.name,
            "version": self.version,
            "class": self.__class__.__name__
        }


# 示例：如何使用基类

"""
from base_skill import BaseSkill

class MySkill(BaseSkill):
    def execute(self, **kwargs):
        # 验证输入
        if not self.validate_input(kwargs):
            return {"success": False, "error": "Invalid input"}
        
        try:
            # 业务逻辑
            result = {"message": f"Hello, {kwargs.get('name', 'World')}!"}
            return {"success": True, "result": result}
        except Exception as e:
            return self.handle_error(e)
    
    def validate_input(self, inputs):
        return 'name' in inputs

# 使用
skill = MySkill()
result = skill.execute(name="Alice")
print(result)
"""

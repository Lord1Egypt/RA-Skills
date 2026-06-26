"""
技能生成器 - 使用 LLM 自动生成新技能
"""

import os
import json
import re
from typing import Dict, Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class GeneratedSkill:
    """生成的技能"""
    name: str
    code: str
    metadata: Dict
    strategy: str  # "改写法" 或 "压缩法"


class BaseSkill(ABC):
    """技能基类 - 所有生成的技能必须继承此类"""
    
    @abstractmethod
    def execute(self, **kwargs):
        """
        执行技能逻辑
        
        Returns:
            dict: 包含 'success' 和 'result'/'error' 键的字典
        """
        pass
    
    @abstractmethod
    def validate_input(self, inputs: dict) -> bool:
        """
        验证输入参数
        
        Args:
            inputs: 输入参数字典
            
        Returns:
            bool: 是否有效
        """
        pass
    
    def handle_error(self, error: Exception) -> dict:
        """
        错误处理（可选重写）
        
        Args:
            error: 异常对象
            
        Returns:
            dict: 错误信息
        """
        return {
            "success": False,
            "error": str(error),
            "type": type(error).__name__,
            "suggestion": "请检查输入参数"
        }


class SkillGenerator:
    """技能生成器"""
    
    GENERATION_PROMPT = """你是一个技能生成专家。根据用户需求，生成一个 Python 技能类。

## 要求

1. **必须继承 BaseSkill 基类**
2. **必须实现三个方法**：
   - `execute(self, **kwargs)` - 执行逻辑
   - `validate_input(self, inputs: dict) -> bool` - 验证输入
   - `handle_error(self, error: Exception) -> dict` - 错误处理

3. **代码规范**：
   - 使用类型提示
   - 添加详细的 docstring
   - 简洁、健壮、带错误处理
   - 不要依赖未安装的包

4. **输出格式**：
   - 技能名称使用下划线命名法
   - 包含完整的类定义和必要导入

## 用户需求

{requirement}

## 输出格式（JSON）

{{
    "name": "skill_xxx",
    "code": "完整的 Python 代码",
    "metadata": {{
        "description": "技能描述",
        "inputs": [{{"name": "param1", "type": "string", "description": "..."}}],
        "outputs": [{{"name": "result", "type": "object", "description": "..."}}],
        "tags": ["tag1", "tag2"]
    }}
}}
"""
    
    def __init__(self, llm_client=None, model: str = "deepseek/deepseek-coder"):
        """
        初始化生成器
        
        Args:
            llm_client: LLM API 客户端
            model: 模型名称
        """
        self.llm_client = llm_client
        self.model = model
    
    def generate(self, requirement: str) -> Optional[GeneratedSkill]:
        """
        生成技能
        
        Args:
            requirement: 用户需求
            
        Returns:
            GeneratedSkill 或 None
        """
        if not self.llm_client:
            return self._generate_mock(requirement)
        
        try:
            # 构建 prompt
            prompt = self.GENERATION_PROMPT.format(requirement=requirement)
            
            # 调用 LLM
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个技能生成专家。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return GeneratedSkill(
                name=result.get("name", "unnamed_skill"),
                code=result.get("code", ""),
                metadata=result.get("metadata", {}),
                strategy="generated"
            )
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return None
    
    def _generate_mock(self, requirement: str) -> GeneratedSkill:
        """生成模拟技能（无 LLM 时使用）"""
        
        # 简单的模板生成
        skill_name = self._extract_name_from_requirement(requirement)
        
        code = f'''"""自动生成的技能: {skill_name}"""

from typing import Dict, Any


class {self._to_class_name(skill_name)}:
    """技能类模板"""
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能逻辑
        
        Args:
            **kwargs: 执行参数
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        # TODO: 实现技能逻辑
        return {{
            "success": True,
            "result": "技能已执行",
            "data": kwargs
        }}
    
    def validate_input(self, inputs: dict) -> bool:
        """
        验证输入参数
        
        Args:
            inputs: 输入参数字典
            
        Returns:
            bool: 是否有效
        """
        # TODO: 添加输入验证逻辑
        return True
    
    def handle_error(self, error: Exception) -> dict:
        """
        错误处理
        
        Args:
            error: 异常对象
            
        Returns:
            dict: 错误信息
        """
        return {{
            "success": False,
            "error": str(error),
            "type": type(error).__name__,
            "suggestion": "请检查输入参数"
        }}
'''
        
        return GeneratedSkill(
            name=skill_name,
            code=code,
            metadata={
                "description": f"自动生成: {requirement}",
                "inputs": [],
                "outputs": [],
                "tags": ["auto-generated"]
            },
            strategy="template"
        )
    
    def _extract_name_from_requirement(self, requirement: str) -> str:
        """从需求中提取技能名称"""
        # 简单处理：取需求的前几个词
        words = re.findall(r'\w+', requirement.lower())
        return "_".join(words[:3]) if words else "skill"
    
    def _to_class_name(self, name: str) -> str:
        """转换为类名"""
        return ''.join(word.capitalize() for word in name.split('_'))


class SkillTemplate:
    """技能代码模板"""
    
    BASIC_TEMPLATE = '''"""技能: {name}"""

from typing import Dict, Any


class {class_name}:
    """{description}"""
    
    def __init__(self):
        self.name = "{name}"
        self.version = "1.0.0"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            **kwargs: 输入参数
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        # 验证输入
        if not self.validate_input(kwargs):
            return {{
                "success": False,
                "error": "Invalid input"
            }}
        
        try:
            # TODO: 实现技能逻辑
            result = {{}}
            
            return {{
                "success": True,
                "result": result
            }}
        except Exception as e:
            return self.handle_error(e)
    
    def validate_input(self, inputs: dict) -> bool:
        """
        验证输入参数
        
        Args:
            inputs: 输入字典
            
        Returns:
            bool: 是否有效
        """
        # TODO: 添加验证逻辑
        required = [{required_params}]
        return all(k in inputs for k in required)
    
    def handle_error(self, error: Exception) -> dict:
        """
        错误处理
        
        Args:
            error: 异常对象
            
        Returns:
            dict: 错误信息
        """
        return {{
            "success": False,
            "error": str(error),
            "type": type(error).__name__,
            "suggestion": "请检查输入参数"
        }}
'''
    
    @classmethod
    def generate(cls, name: str, description: str, required_params: List[str]) -> str:
        """生成技能代码模板"""
        return cls.BASIC_TEMPLATE.format(
            name=name,
            class_name=''.join(w.capitalize() for w in name.split('_')),
            description=description,
            required_params=','.join(f'"{p}"' for p in required_params)
        )


def create_generator(llm_client=None) -> SkillGenerator:
    """创建生成器实例"""
    return SkillGenerator(llm_client)


if __name__ == "__main__":
    # 测试
    generator = SkillGenerator()
    
    requirements = [
        "发送邮件技能",
        "天气查询技能",
        "文件处理技能"
    ]
    
    for req in requirements:
        print(f"\n{'='*50}")
        print(f"📝 需求: {req}")
        print("="*50)
        
        skill = generator.generate(req)
        if skill:
            print(f"✅ 技能名称: {skill.name}")
            print(f"📄 代码长度: {len(skill.code)} 字符")

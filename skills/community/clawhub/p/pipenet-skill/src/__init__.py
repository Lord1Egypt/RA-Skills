"""
流体管网设计与仿真技能包
=======================

提供流体管网的生成、求解、分析和可视化功能。

主要组件:
- PipeNetSkill: 技能主类，包含设计、分析、可视化三个工具
- PipeNetLoader: TOML配置文件加载器
- PipeNetSolver: 管网水力学求解器
- PipeNetValidator: 求解结果验证器
- ReliabilityAnalyzer: 可靠性分析器
- PipeNetVisualizer: 管网可视化器

使用示例:
    from src import PipeNetSkill
    
    # 设计管网
    result = PipeNetSkill.design_network(toml_content)
    
    # 分析管网
    analysis = PipeNetSkill.analyze_network(file_path, scenario_name="normal_operation")
    
    # 可视化管网
    visual = PipeNetSkill.visualize_network(file_path)
"""

__version__ = "1.0.0"
__author__ = "张志伟"

# 导入主要类和函数
from .skill import PipeNetSkill, SKILL_FUNCTIONS

# 导入核心模块（如果存在）
try:
    from .core.loader import PipeNetLoader
    from .core.solver import PipeNetSolver
    from .core.validator import PipeNetValidator
    from .core.analyzer import ReliabilityAnalyzer
    from .core.visualizer import PipeNetVisualizer
except ImportError as e:
    # 允许部分导入失败（用于文档生成等场景）
    import warnings
    warnings.warn(f"部分核心模块导入失败: {e}")

# 导出公共API
__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    
    # 主要技能类
    "PipeNetSkill",
    "SKILL_FUNCTIONS",
    
    # 核心模块（可选）
    "PipeNetLoader",
    "PipeNetSolver", 
    "PipeNetValidator",
    "ReliabilityAnalyzer",
    "PipeNetVisualizer",
]


def get_skill_functions():
    """
    获取所有可用的技能函数字典
    
    Returns:
        Dict[str, Callable]: 技能名称到函数的映射
    """
    return SKILL_FUNCTIONS


def list_skills():
    """
    列出所有可用的技能名称
    
    Returns:
        List[str]: 技能名称列表
    """
    return list(SKILL_FUNCTIONS.keys())

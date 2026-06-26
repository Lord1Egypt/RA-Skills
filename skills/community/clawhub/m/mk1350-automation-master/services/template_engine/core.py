# template_engine/core.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List, Optional, Callable
import pandas as pd

class TemplateType(Enum):
    """模板类型枚举"""
    EXCEL_FORM = "excel_form"
    EXCEL_TABLE = "excel_table"
    WORD_FORM = "word_form"
    WORD_TABLE = "word_table"

class GenerationMode(Enum):
    """生成模式枚举"""
    PLACEHOLDER_ONLY = "placeholder_only"
    TABLE_ONLY = "table_only"
    MIXED = "mixed"

@dataclass
class DataSource:
    """数据源定义"""
    name: str
    file_path: str
    sheet_name: str = "Sheet1"
    key_field: str = None

@dataclass
class PlaceholderMapping:
    """占位符映射配置"""
    placeholder: str
    data_field: str
    data_type: str = "text"
    default_value: Any = ""

@dataclass
class TableRange:
    """表格区域配置"""
    table_index: int
    data_source: str
    start_row: int
    start_col: int = 1
    reserved_rows: int = 0
    column_mappings: Dict[int, str] = None

@dataclass
class ExecutionStep:
    """执行步骤定义 - 使用字符串标识函数"""
    step_id: str
    action_type: str
    function_name: str  # 改为函数名而不是直接引用
    description: str
    config: Dict[str, Any]
    data_source: str
    error_policy: str = "stop"

@dataclass
class ExecutionPlan:
    """执行计划"""
    template_path: str
    output_dir: str
    mode: GenerationMode
    steps: List[ExecutionStep]
    data_sources: List[DataSource]

@dataclass
class GenerationResult:
    """生成结果"""
    status: str
    message: str
    generated_files: List[str]
    output_dir: str
    execution_log: List[Dict] = None
    download_info: Dict[str, Any] = None

@dataclass
class StepResult:
    """步骤执行结果"""
    success: bool
    step_id: str
    result: Any = None
    error: str = None
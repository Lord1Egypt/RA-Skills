"""
Schema module for memory_ontology package.
Handles schema loading and entity validation.
"""

from typing import Dict, List, Any
import yaml

from .config import SCHEMA_FILE, BASE_SCHEMA_FILE


def load_schema() -> Dict[str, Any]:
    """加载 schema 定义"""
    schema = {'types': {}, 'relations': {}, 'validations': [], 'examples': {}}

    # 加载记忆 schema（优先，包含新类型）
    if SCHEMA_FILE.exists():
        try:
            with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
                memory_schema = yaml.safe_load(f)
                if memory_schema:
                    schema['types'].update(memory_schema.get('types', {}))
                    schema['relations'].update(memory_schema.get('relations', {}))
                    schema['validations'].extend(memory_schema.get('validations', []))
        except Exception as e:
            print(f"Warning: Could not load memory schema: {e}")

    # 加载基础 schema（补充）
    if BASE_SCHEMA_FILE.exists():
        try:
            with open(BASE_SCHEMA_FILE, 'r', encoding='utf-8') as f:
                base_schema = yaml.safe_load(f)
                if base_schema:
                    # 只添加不存在的类型，避免覆盖
                    for key, value in base_schema.get('types', {}).items():
                        if key not in schema['types']:
                            schema['types'][key] = value
                    for key, value in base_schema.get('relations', {}).items():
                        if key not in schema['relations']:
                            schema['relations'][key] = value
        except Exception as e:
            print(f"Warning: Could not load base schema: {e}")

    return schema


def validate_entity(entity_type: str, properties: Dict[str, Any]) -> List[str]:
    """验证实体属性"""
    errors = []
    schema = load_schema()

    if entity_type not in schema['types']:
        errors.append(f"未知实体类型：{entity_type}")
        return errors

    type_schema = schema['types'][entity_type]
    required_fields = type_schema.get('required', [])

    # 检查必填字段
    for field in required_fields:
        if field not in properties:
            errors.append(f"缺少必填字段：{field}")

    # 检查属性类型
    properties_schema = type_schema.get('properties', {})
    for field, value in properties.items():
        if field in properties_schema:
            field_schema = properties_schema[field]

            # 检查 enum
            if 'enum' in field_schema and value not in field_schema['enum']:
                errors.append(f"字段 {field} 的值 {value} 不在允许范围内：{field_schema['enum']}")

            # 检查类型
            expected_type = field_schema.get('type')
            if expected_type == 'number' and not isinstance(value, (int, float)):
                errors.append(f"字段 {field} 应该是数字类型")
            elif expected_type == 'string' and not isinstance(value, str):
                errors.append(f"字段 {field} 应该是字符串类型")
            elif expected_type == 'array' and not isinstance(value, list):
                errors.append(f"字段 {field} 应该是数组类型")

    return errors
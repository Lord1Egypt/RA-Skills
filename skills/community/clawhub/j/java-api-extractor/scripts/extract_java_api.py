#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Java Spring Boot 项目中提取 Controller 层接口定义为 JSON 数据

用法:
    py extract_java_api.py --project "D:\working\coding\msa-icmp-dev-manage" --output api-definitions.json
"""

import argparse
import json
import os
import re
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# 设置 stdout 为 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 配置
TEMPLATE_FILE = r"D:\working\接口文档数据模版.json"
API_DOCS_DIR = r"D:\working\coding\api-docs"

# Java 类型到 JSON 类型映射
JAVA_TO_JSON_TYPE = {
    "String": "string", "Integer": "integer", "int": "integer",
    "Long": "integer", "long": "integer",
    "Boolean": "boolean", "boolean": "boolean",
    "Double": "number", "double": "number",
    "Float": "number", "float": "number",
    "Date": "string", "LocalDateTime": "string", "LocalDate": "string",
    "List": "array", "Set": "array", "Array": "array",
    "Map": "object", "Object": "object",
}

# 请求映射注解到 HTTP 方法
MAPPING_TO_METHOD = {
    "GetMapping": "GET", "PostMapping": "POST", "PutMapping": "PUT",
    "DeleteMapping": "DELETE", "PatchMapping": "PATCH", "RequestMapping": "GET",
}

# Emoji 替代（用于 Windows 控制台）
EMOJI = {
    'search': '🔍', 'folder': '📂', 'file': '📄', 'check': '✅',
    'rocket': '🚀', 'disk': '💾', 'warn': '⚠️', 'error': '❌',
    'package': '📦'
}

@dataclass
class RequestParam:
    name: str
    type: str
    required: bool = True
    description: str = ""

@dataclass
class ApiDefinition:
    name: str = ""
    path: str = ""
    method: str = "GET"
    description: str = ""
    requestParams: List[RequestParam] = field(default_factory=list)
    responseSchema: Dict[str, Any] = field(default_factory=dict)


class JavaApiExtractor:
    def __init__(self, project_path: str, verbose: bool = False):
        self.project_path = Path(project_path)
        self.verbose = verbose
        
    def find_controllers(self, package_filter: Optional[str] = None) -> List[Path]:
        controllers = []
        src_path = self.project_path / "src" / "main" / "java"
        
        if not src_path.exists():
            return controllers
        
        for java_file in src_path.rglob("*.java"):
            if package_filter:
                package_path = package_filter.replace(".", os.sep)
                if package_path not in str(java_file):
                    continue
            if self._is_controller(java_file):
                controllers.append(java_file)
        
        return controllers
    
    def _is_controller(self, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding='utf-8')
            return '@RestController' in content or '@Controller' in content
        except:
            return False
    
    def extract_apis(self, controller_file: Path) -> List[ApiDefinition]:
        apis = []
        try:
            content = controller_file.read_text(encoding='utf-8')
            class_path = self._extract_class_path(content)
            methods = self._find_methods(content)
            
            for method in methods:
                api_def = self._parse_method(method, class_path, controller_file)
                if api_def:
                    apis.append(api_def)
        except Exception as e:
            if self.verbose:
                print(f"❌ 读取文件失败 {controller_file}: {e}")
        
        return apis
    
    def _extract_class_path(self, content: str) -> str:
        patterns = [
            r'@RequestMapping\s*\(\s*"([^"]+)"\s*\)',
            r'@RequestMapping\s*\(\s*value\s*=\s*"([^"]+)"\s*\)',
        ]
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        return ""
    
    def _find_methods(self, content: str) -> List[Dict]:
        methods = []
        # 支持换行符的正则表达式（使用 raw string）
        pattern = r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)(?:\s*\(\s*(?:value\s*=\s*)?"([^"]*)"\s*\))?\s*[\r\n]*\s*(public|private|protected)\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)'
        
        for match in re.finditer(pattern, content):
            methods.append({
                'annotation': match.group(1),
                'path': match.group(2) or '',
                'return_type': match.group(4),
                'method_name': match.group(5),
                'full_match': match.group(0)
            })
        
        return methods
    
    def _parse_method(self, method: Dict, class_path: str, controller_file: Path) -> Optional[ApiDefinition]:
        api_def = ApiDefinition()
        
        # HTTP 方法
        api_def.method = MAPPING_TO_METHOD.get(method['annotation'], 'GET')
        
        # 路径
        method_path = method['path']
        if class_path and method_path:
            api_def.path = f"{class_path.rstrip('/')}/{method_path.lstrip('/')}"
        elif class_path:
            api_def.path = class_path
        else:
            api_def.path = method_path or '/'
        api_def.path = api_def.path.replace('//', '/')
        
        # 描述（简化：从方法名推断）
        api_def.description = self._camel_to_chinese(method['method_name'])
        api_def.name = api_def.description.split('.')[0].split(',')[0].strip()[:50]
        
        # 请求参数（简化：暂不解析）
        api_def.requestParams = []
        
        # 响应 Schema
        api_def.responseSchema = self._extract_response_schema(method['return_type'], controller_file)
        
        return api_def
    
    def _extract_response_schema(self, return_type: str, controller_file: Path) -> Dict:
        schema = {
            "type": "object",
            "properties": {
                "code": {"type": "integer", "description": "状态码"},
                "msg": {"type": "string", "description": "响应消息"},
                "data": {"type": "object", "description": "返回数据"}
            }
        }
        
        if not return_type:
            return schema
        
        # 检查是否为泛型
        generic_match = re.match(r'(\w+)<(\w+)>', return_type)
        is_array = False
        inner_type = return_type
        
        if generic_match:
            wrapper_type = generic_match.group(1)
            inner_type = generic_match.group(2)
            if wrapper_type in ['List', 'Set', 'Array', 'PageInfo']:
                is_array = True
        
        # 基础类型
        base_types = ['void', 'Void', 'String', 'Integer', 'int', 'Long', 'long', 'Boolean', 'boolean', 'Double', 'double']
        
        if inner_type in base_types:
            if inner_type in ['void', 'Void']:
                schema['properties']['data'] = {"type": "null", "description": "无返回数据"}
            else:
                schema['properties']['data'] = {"type": JAVA_TO_JSON_TYPE.get(inner_type, 'string'), "description": f"返回数据：{inner_type}"}
        elif is_array:
            fields = self._extract_dto_fields(inner_type, controller_file)
            items_props = {f['name']: {"type": f['type'], "description": f['description']} for f in fields}
            schema['properties']['data'] = {
                "type": "array",
                "description": f"返回数据：{inner_type} 数组",
                "items": {"type": "object", "properties": items_props}
            }
        else:
            fields = self._extract_dto_fields(inner_type, controller_file)
            data_props = {f['name']: {"type": f['type'], "description": f['description']} for f in fields}
            schema['properties']['data'] = {
                "type": "object",
                "description": f"返回数据：{inner_type}",
                "properties": data_props
            }
        
        return schema
    
    def _extract_dto_fields(self, dto_type: str, controller_file: Path) -> List[Dict]:
        fields = []
        src_path = self.project_path / "src" / "main" / "java"
        
        # 查找 DTO/VO 文件
        for java_file in src_path.rglob(f"{dto_type}.java"):
            try:
                content = java_file.read_text(encoding='utf-8')
                field_pattern = r'(?:private|public|protected)\s+(?:static\s+final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*;'
                
                for match in re.finditer(field_pattern, content):
                    field_type = match.group(1)
                    field_name = match.group(2)
                    if field_name == 'serialVersionUID':
                        continue
                    
                    # 尝试从注释提取描述
                    desc = field_name
                    field_idx = content.find(field_name)
                    if field_idx > 0:
                        before = content[max(0, field_idx-150):field_idx]
                        comment_match = re.search(r'/\*\*\s*\*\s*([^\*\n]+)', before)
                        if comment_match:
                            desc = comment_match.group(1).strip()
                    
                    fields.append({
                        'name': field_name,
                        'type': JAVA_TO_JSON_TYPE.get(field_type, 'string'),
                        'description': desc
                    })
                break
            except:
                continue
        
        return fields
    
    def _camel_to_chinese(self, name: str) -> str:
        action_map = {
            'get': '获取', 'create': '创建', 'add': '添加', 'save': '保存',
            'update': '更新', 'delete': '删除', 'remove': '移除',
            'list': '列表', 'query': '查询', 'search': '搜索', 'find': '查找',
        }
        for en, zh in action_map.items():
            if name.lower().startswith(en):
                return f"{zh}{name[len(en):]}"
        return name


def load_template() -> Dict:
    if Path(TEMPLATE_FILE).exists():
        return json.loads(Path(TEMPLATE_FILE).read_text(encoding='utf-8'))
    return {"name": "", "path": "", "method": "GET", "description": "", "requestParams": [], "responseSchema": {"type": "object", "properties": {}}}


def api_def_to_json(api_def: ApiDefinition, template: Dict) -> Dict:
    return {
        "name": api_def.name or template.get("name", ""),
        "path": api_def.path or template.get("path", ""),
        "method": api_def.method or template.get("method", "GET"),
        "description": api_def.description or template.get("description", ""),
        "requestParams": [{"name": p.name, "type": p.type, "required": p.required, "description": p.description} for p in api_def.requestParams],
        "responseSchema": api_def.responseSchema
    }


def main():
    parser = argparse.ArgumentParser(description="从 Java 项目中提取 Controller 层接口定义为 JSON 数据")
    parser.add_argument("--project", required=True, help="Java 项目根目录")
    parser.add_argument("--output", help="输出 JSON 文件路径")
    parser.add_argument("--package", help="只提取指定包下的 Controller")
    parser.add_argument("--prdid", help="产品需求 ID，如果指定则直接推送")
    parser.add_argument("--push", action="store_true", help="提取后直接推送到产品部数据平台")
    parser.add_argument("--verbose", action="store_true", help="显示详细输出")
    parser.add_argument("--no-backup", action="store_true", help="不自动备份到 api-docs 目录")
    
    args = parser.parse_args()
    
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ 项目路径不存在：{args.project}")
        sys.exit(1)
    
    print(f"{EMOJI['search']} 开始提取 Java 项目接口定义...")
    print(f"   项目路径：{args.project}")
    
    extractor = JavaApiExtractor(args.project, args.verbose)
    controllers = extractor.find_controllers(args.package)
    
    if not controllers:
        print(f"{EMOJI['error']} 未找到任何 Controller 类")
        sys.exit(1)
    
    print(f"{EMOJI['folder']} 找到 {len(controllers)} 个 Controller 类")
    
    all_apis = []
    template = load_template()
    
    for controller in controllers:
        if args.verbose:
            print(f"\n{EMOJI['file']} 处理：{controller.name}")
        
        apis = extractor.extract_apis(controller)
        for api in apis:
            json_def = api_def_to_json(api, template)
            all_apis.append(json_def)
            if args.verbose:
                print(f"  {EMOJI['check']} {json_def['method']} {json_def['path']}")
    
    print(f"\n{EMOJI['check']} 共提取 {len(all_apis)} 个接口定义")
    
    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_apis, f, ensure_ascii=False, indent=2)
        print(f"{EMOJI['file']} 已保存到：{output_path}")
    else:
        print(json.dumps(all_apis, ensure_ascii=False, indent=2))
    
    # 备份
    if not args.no_backup:
        try:
            api_docs_dir = Path(API_DOCS_DIR)
            api_docs_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_path = api_docs_dir / f"api-definitions-{timestamp}.json"
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(all_apis, f, ensure_ascii=False, indent=2)
            print(f"{EMOJI['disk']} 已备份到：{backup_path}")
        except Exception as e:
            print(f"{EMOJI['warn']} 备份失败：{e}")
    
    # 推送
    if args.push or args.prdid:
        if not args.prdid:
            print(f"{EMOJI['error']} 推送需要指定 --prdid 参数")
            sys.exit(1)
        
        print(f"\n{EMOJI['rocket']} 准备推送到产品部数据平台...")
        print(f"   PRD ID: {args.prdid}")
        
        push_script = Path(__file__).parent.parent / "api-push-product-platform" / "scripts" / "push_api_to_product_platform.py"
        if push_script.exists():
            import subprocess
            cmd = ["py", str(push_script), "--prdid", args.prdid, "--file", str(args.output) if args.output else "/dev/null"]
            if args.verbose:
                cmd.append("--verbose")
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.returncode != 0:
                print(f"{EMOJI['error']} 推送失败：{result.stderr}")
                sys.exit(1)
            else:
                print(f"{EMOJI['check']} 推送成功！")


if __name__ == "__main__":
    main()

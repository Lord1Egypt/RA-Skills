"""
API Scanner - API 接口扫描器
扫描 Controller 和 API 定义
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional


class APIScanner:
    """API 接口扫描器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.controllers = []
        self.endpoints = []
        
    def scan(self) -> Dict:
        """执行 API 扫描"""
        result = {
            'controllers': [],
            'endpoints': [],
            'feign_clients': [],
            'dto_classes': [],
            'swagger_docs': []
        }
        
        # 1. 扫描 Controller
        self._scan_controllers()
        result['controllers'] = self.controllers
        result['endpoints'] = self.endpoints
        
        # 2. 扫描 Feign Client
        self._scan_feign_clients()
        result['feign_clients'] = self.feign_clients if hasattr(self, 'feign_clients') else []
        
        # 3. 扫描 DTO 类
        self._scan_dto_classes()
        result['dto_classes'] = self.dto_classes if hasattr(self, 'dto_classes') else []
        
        return {
            'controller_count': len(self.controllers),
            'endpoint_count': len(self.endpoints),
            'controllers': self.controllers,
            'endpoints': self.endpoints,
            'feign_clients': result['feign_clients'],
            'dto_classes': result['dto_classes']
        }
    
    def _scan_controllers(self) -> None:
        """扫描 Controller 类"""
        self.controllers = []
        self.endpoints = []
        
        # 查找 Controller 文件
        controller_patterns = [
            '**/*Controller*.java',
            '**/*RestController*.java',
            '**/adapter/**/*Controller.java',
            '**/web/*Controller.java',
        ]
        
        for pattern in controller_patterns:
            for controller_file in self.project_path.glob(pattern):
                if 'test' in str(controller_file) or 'target' in str(controller_file):
                    continue
                
                try:
                    content = controller_file.read_text(encoding='utf-8', errors='ignore')
                    controller = self._parse_controller(content, controller_file)
                    
                    if controller:
                        self.controllers.append(controller)
                        self.endpoints.extend(controller['endpoints'])
                        
                except Exception as e:
                    print(f"   ⚠️ 解析 Controller 失败: {controller_file} - {e}")
    
    def _parse_controller(self, content: str, file_path: Path) -> Optional[Dict]:
        """解析 Controller 类"""
        # 提取类名
        class_match = re.search(r'public\s+(?:class|@interface)\s+(\w+)', content)
        if not class_match:
            return None
        
        class_name = class_match.group(1)
        
        # 提取类上的注解
        class_annotations = self._extract_class_annotations(content)
        
        # 提取基路径
        base_path = self._extract_base_path(class_annotations, content)
        
        # 提取所有方法
        endpoints = self._extract_endpoints(content, base_path)
        
        return {
            'name': class_name,
            'path': str(file_path),
            'annotations': class_annotations,
            'base_path': base_path,
            'endpoints': endpoints
        }
    
    def _extract_class_annotations(self, content: str) -> List[str]:
        """提取类注解"""
        annotations = []
        
        # 查找类注解
        pattern = r'@(\w+)(?:\([^)]*\))?\s*(?:class|@)'
        for match in re.finditer(pattern, content):
            annotation = match.group(1)
            if annotation not in ['public', 'private', 'protected', 'class', 'interface']:
                annotations.append(annotation)
        
        return annotations
    
    def _extract_base_path(self, annotations: List[str], content: str) -> str:
        """提取基础路径"""
        # 从 @RequestMapping 提取
        mapping_pattern = r'@RequestMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']'
        match = re.search(mapping_pattern, content)
        if match:
            return match.group(1)
        
        return ''
    
    def _extract_endpoints(self, content: str, base_path: str) -> List[Dict]:
        """提取端点"""
        endpoints = []
        
        # HTTP 方法映射
        method_mapping = {
            'GetMapping': 'GET',
            'PostMapping': 'POST',
            'PutMapping': 'PUT',
            'DeleteMapping': 'DELETE',
            'PatchMapping': 'PATCH',
            'RequestMapping': 'REQUEST'
        }
        
        # 分割方法
        method_pattern = r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)(?:\s*\(([^)]*)\))?\s*(?:public|private|protected)\s+[\w<>,\s]+\s+(\w+)\s*\(([^)]*)\)'
        
        for match in re.finditer(method_pattern, content):
            annotation = match.group(1)
            params_str = match.group(2) or ''
            method_name = match.group(3)
            args_str = match.group(4) or ''
            
            # 提取路径
            path_match = re.search(r'["\']([^"\']+)["\']', params_str)
            path = path_match.group(1) if path_match else ''
            
            # 提取 HTTP 方法
            http_method = method_mapping.get(annotation, 'GET')
            if annotation == 'RequestMapping':
                method_type_match = re.search(r'method\s*=\s*RequestMethod\.(\w+)', params_str)
                if method_type_match:
                    http_method = method_type_match.group(1)
            
            # 解析参数
            args = self._parse_arguments(args_str)
            
            # 提取文档注释
            doc_comment = self._extract_doc_comment(content, method_name)
            
            endpoints.append({
                'method': http_method,
                'path': base_path + path,
                'full_path': base_path + path,
                'name': method_name,
                'args': args,
                'description': doc_comment
            })
        
        return endpoints
    
    def _parse_arguments(self, args_str: str) -> List[Dict]:
        """解析方法参数"""
        args = []
        
        # 分割参数
        param_pattern = r'(?:@(\w+)\s+)?(?:@(\w+)\s+)?(\w+(?:<[^>]+>)?(?:\[\])?)\s+(\w+)(?:\s*=\s*([^,}]+))?'
        
        for match in re.finditer(param_pattern, args_str):
            param_annotation = match.group(1) or match.group(2)
            param_type = match.group(3)
            param_name = match.group(4)
            param_default = match.group(5)
            
            args.append({
                'type': param_type,
                'name': param_name,
                'annotation': param_annotation,
                'required': param_annotation in ['RequestBody', 'PathVariable'],
                'default': param_default
            })
        
        return args
    
    def _extract_doc_comment(self, content: str, method_name: str) -> str:
        """提取方法的文档注释"""
        # 查找方法前的文档注释
        pattern = rf'/\*\*\s*([^*]*(?:\*(?!/)[^*]*)*)\*/\s*(?:public|private|protected)\s+\w+\s+{method_name}'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            comment = match.group(1)
            # 清理注释
            comment = re.sub(r'\*\s*', '', comment)
            comment = comment.strip()
            return comment
        
        return ''
    
    def _scan_feign_clients(self) -> None:
        """扫描 Feign Client"""
        self.feign_clients = []
        
        feign_patterns = [
            '**/*Feign*.java',
            '**/*Client*.java',
            '**/feign/**/*.java'
        ]
        
        for pattern in feign_patterns:
            for client_file in self.project_path.glob(pattern):
                if 'test' in str(client_file) or 'target' in str(client_file):
                    continue
                
                try:
                    content = client_file.read_text(encoding='utf-8', errors='ignore')
                    
                    if '@FeignClient' in content or 'extends FeignClient' in content:
                        client = self._parse_feign_client(content, client_file)
                        if client:
                            self.feign_clients.append(client)
                            
                except Exception as e:
                    print(f"   ⚠️ 解析 Feign Client 失败: {client_file} - {e}")
    
    def _parse_feign_client(self, content: str, file_path: Path) -> Optional[Dict]:
        """解析 Feign Client"""
        class_match = re.search(r'public\s+(?:interface|class)\s+(\w+)', content)
        if not class_match:
            return None
        
        class_name = class_match.group(1)
        
        # 提取服务名
        service_match = re.search(r'@FeignClient\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']', content)
        service_name = service_match.group(1) if service_match else ''
        
        return {
            'name': class_name,
            'path': str(file_path),
            'service': service_name
        }
    
    def _scan_dto_classes(self) -> None:
        """扫描 DTO 类"""
        self.dto_classes = []
        
        dto_patterns = [
            '**/*DTO.java',
            '**/*Request.java',
            '**/*Response.java',
            '**/*VO.java',
            '**/*BO.java',
            '**/dto/**/*.java',
            '**/vo/**/*.java'
        ]
        
        for pattern in dto_patterns:
            for dto_file in self.project_path.glob(pattern):
                if 'test' in str(dto_file) or 'target' in str(dto_file):
                    continue
                
                try:
                    content = dto_file.read_text(encoding='utf-8', errors='ignore')
                    
                    dto = self._parse_dto(content, dto_file)
                    if dto:
                        self.dto_classes.append(dto)
                        
                except Exception as e:
                    print(f"   ⚠️ 解析 DTO 失败: {dto_file} - {e}")
    
    def _parse_dto(self, content: str, file_path: Path) -> Optional[Dict]:
        """解析 DTO 类"""
        class_match = re.search(r'public\s+(?:class|record)\s+(\w+)', content)
        if not class_match:
            return None
        
        class_name = class_match.group(1)
        
        # 提取字段
        fields = []
        field_pattern = r'private\s+(\w+(?:<[^>]+>)?(?:\[\])?)\s+(\w+);'
        
        for match in re.finditer(field_pattern, content):
            fields.append({
                'type': match.group(1),
                'name': match.group(2)
            })
        
        return {
            'name': class_name,
            'path': str(file_path),
            'fields': fields
        }


# 导出
__all__ = ['APIScanner']

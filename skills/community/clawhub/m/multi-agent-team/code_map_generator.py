#!/usr/bin/env python3
"""
Code Map Generator Tool
用于生成项目的代码结构映射，帮助架构师和开发者了解项目的整体结构
"""

import os
import json
import argparse
from pathlib import Path
import ast
from typing import Dict, List, Any

class CodeMapGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.code_map = {
            "project_name": self.project_root.name,
            "root_path": str(self.project_root),
            "modules": {},
            "dependencies": {},
            "entry_points": [],
            "key_components": [],
            "file_count": 0,
            "directory_count": 0
        }
    
    def scan_directory(self, directory: Path, relative_path: str = ""):
        """扫描目录结构"""
        self.code_map["directory_count"] += 1
        
        for item in directory.iterdir():
            if item.name.startswith('.') or item.name in ['node_modules', 'target', 'build', '.git']:
                continue
            
            item_relative_path = os.path.join(relative_path, item.name)
            
            if item.is_dir():
                self.code_map["modules"][item_relative_path] = {
                    "type": "directory",
                    "path": str(item),
                    "relative_path": item_relative_path,
                    "children": {}
                }
                self.scan_directory(item, item_relative_path)
            else:
                self.code_map["file_count"] += 1
                if item.suffix in ['.java', '.py', '.js', '.ts', '.tsx', '.jsx']:
                    self.analyze_file(item, item_relative_path)
    
    def analyze_file(self, file_path: Path, relative_path: str):
        """分析文件内容"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            if file_path.suffix == '.java':
                self.analyze_java_file(content, relative_path)
            elif file_path.suffix == '.py':
                self.analyze_python_file(content, relative_path)
            elif file_path.suffix in ['.js', '.ts', '.tsx', '.jsx']:
                self.analyze_js_file(content, relative_path)
                
            # 检查是否是入口文件
            if any(keyword in relative_path for keyword in ['main', 'Application', 'app', 'index']):
                self.code_map["entry_points"].append(relative_path)
                
        except Exception as e:
            print(f"分析文件 {relative_path} 时出错: {e}")
    
    def analyze_java_file(self, content: str, relative_path: str):
        """分析Java文件"""
        # 提取包名
        package_match = None
        for line in content.split('\n'):
            if line.strip().startswith('package '):
                package_match = line.strip().split(' ')[1].rstrip(';')
                break
        
        # 提取类名
        class_names = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('public class ') or line.startswith('class ') or line.startswith('public interface '):
                class_name = line.split(' ')[2].split('{')[0]
                class_names.append(class_name)
        
        self.code_map["modules"][relative_path] = {
            "type": "java_file",
            "path": str(self.project_root / relative_path),
            "relative_path": relative_path,
            "package": package_match,
            "classes": class_names,
            "imports": [line.strip() for line in lines if line.strip().startswith('import ')]
        }
    
    def analyze_python_file(self, content: str, relative_path: str):
        """分析Python文件"""
        try:
            tree = ast.parse(content)
            
            # 提取类和函数
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(f"from {node.module} import ...")
            
            self.code_map["modules"][relative_path] = {
                "type": "python_file",
                "path": str(self.project_root / relative_path),
                "relative_path": relative_path,
                "classes": classes,
                "functions": functions,
                "imports": imports
            }
        except Exception:
            # 无法解析的文件，仅记录基本信息
            self.code_map["modules"][relative_path] = {
                "type": "python_file",
                "path": str(self.project_root / relative_path),
                "relative_path": relative_path
            }
    
    def analyze_js_file(self, content: str, relative_path: str):
        """分析JavaScript/TypeScript文件"""
        # 简单提取导入和导出
        imports = []
        exports = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('import '):
                imports.append(line)
            elif line.startswith('export '):
                exports.append(line)
        
        self.code_map["modules"][relative_path] = {
            "type": "js_file",
            "path": str(self.project_root / relative_path),
            "relative_path": relative_path,
            "imports": imports,
            "exports": exports
        }
    
    def analyze_dependencies(self):
        """分析模块依赖关系"""
        # 基于导入语句分析依赖
        for module_path, module_info in self.code_map["modules"].items():
            if "imports" in module_info:
                for imp in module_info["imports"]:
                    # 简单解析导入路径
                    imp_path = self._extract_import_path(imp)
                    if imp_path:
                        if module_path not in self.code_map["dependencies"]:
                            self.code_map["dependencies"][module_path] = []
                        self.code_map["dependencies"][module_path].append(imp_path)
    
    def _extract_import_path(self, import_statement: str) -> str:
        """从导入语句中提取路径"""
        # 简单实现，实际项目可能需要更复杂的解析
        if import_statement.startswith('import '):
            parts = import_statement.split('from ')
            if len(parts) > 1:
                return parts[1].split()[0].strip("'\";")
        return None
    
    def identify_key_components(self):
        """识别核心组件"""
        # 基于文件路径和内容识别核心组件
        for module_path, module_info in self.code_map["modules"].items():
            if any(keyword in module_path for keyword in ['controller', 'service', 'repository', 'model', 'config', 'util']):
                self.code_map["key_components"].append(module_path)
    
    def generate(self) -> Dict[str, Any]:
        """生成完整的代码map"""
        self.scan_directory(self.project_root)
        self.analyze_dependencies()
        self.identify_key_components()
        return self.code_map
    
    def save(self, output_path: str):
        """保存代码map到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.code_map, f, ensure_ascii=False, indent=2)
        print(f"代码map已保存到: {output_path}")
    
    def generate_markdown(self, output_path: str):
        """生成Markdown格式的项目结构文档"""
        md_content = f"# {self.code_map['project_name']} 项目结构文档\n\n"
        
        # 项目概览
        md_content += "## 项目概览\n\n"
        md_content += f"- **项目名称**: {self.code_map['project_name']}\n"
        md_content += f"- **项目路径**: {self.code_map['root_path']}\n"
        md_content += f"- **文件数量**: {self.code_map['file_count']}\n"
        md_content += f"- **目录数量**: {self.code_map['directory_count']}\n\n"
        
        # 目录结构
        md_content += "## 目录结构\n\n"
        md_content += "```\n"
        md_content += self._generate_directory_tree()
        md_content += "```\n\n"
        
        # 核心组件
        md_content += "## 核心组件\n\n"
        if self.code_map['key_components']:
            for component in self.code_map['key_components']:
                md_content += f"- {component}\n"
        else:
            md_content += "无核心组件识别\n"
        md_content += "\n"
        
        # 入口文件
        md_content += "## 入口文件\n\n"
        if self.code_map['entry_points']:
            for entry in self.code_map['entry_points']:
                md_content += f"- {entry}\n"
        else:
            md_content += "无入口文件识别\n"
        md_content += "\n"
        
        # 模块依赖
        md_content += "## 模块依赖\n\n"
        if self.code_map['dependencies']:
            for module, deps in self.code_map['dependencies'].items():
                if deps:
                    md_content += f"### {module}\n"
                    for dep in deps:
                        md_content += f"- {dep}\n"
                    md_content += "\n"
        else:
            md_content += "无依赖关系识别\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"项目结构文档已保存到: {output_path}")
    
    def _generate_directory_tree(self, current_path: Path = None, prefix: str = "") -> str:
        """生成目录树"""
        if current_path is None:
            current_path = self.project_root
        
        tree = ""
        items = sorted(current_path.iterdir())
        
        for i, item in enumerate(items):
            if item.name.startswith('.') or item.name in ['node_modules', 'target', 'build', '.git']:
                continue
            
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            
            tree += f"{prefix}{connector}{item.name}\n"
            
            if item.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                tree += self._generate_directory_tree(item, new_prefix)
        
        return tree

def main():
    parser = argparse.ArgumentParser(description="生成项目代码map")
    parser.add_argument("project_root", help="项目根目录路径")
    parser.add_argument("--output", default="code_map.json", help="输出JSON文件路径")
    parser.add_argument("--markdown", default="PROJECT_STRUCTURE.md", help="输出Markdown文件路径")
    parser.add_argument("--docs-dir", default=".trae/skills/trae-multi-agent/docs/spec-kit", help="文档保存目录")
    
    args = parser.parse_args()
    
    generator = CodeMapGenerator(args.project_root)
    code_map = generator.generate()
    
    # 保存JSON文件
    generator.save(args.output)
    
    # 保存Markdown文件到docs目录
    markdown_path = os.path.join(args.docs_dir, args.markdown)
    os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
    generator.generate_markdown(markdown_path)
    
    print("\n代码map生成完成！")
    print(f"- JSON格式: {args.output}")
    print(f"- Markdown格式: {markdown_path}")

if __name__ == "__main__":
    main()

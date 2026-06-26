#!/usr/bin/env python3
"""
Project Understanding Tool
用于快速读取项目文档和代码，生成基于角色的项目理解文档
"""

import os
import json
import argparse
from pathlib import Path
import re
from typing import Dict, List, Any

class ProjectUnderstanding:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.project_info = {
            "project_name": self.project_root.name,
            "root_path": str(self.project_root),
            "documents": {},
            "code_structure": {},
            "dependencies": {},
            "technologies": [],
            "roles": {
                "architect": {
                    "understanding": "",
                    "key_areas": []
                },
                "product_manager": {
                    "understanding": "",
                    "key_areas": []
                },
                "test_expert": {
                    "understanding": "",
                    "key_areas": []
                },
                "solo_coder": {
                    "understanding": "",
                    "key_areas": []
                }
            }
        }
    
    def scan_documents(self):
        """扫描项目文档"""
        doc_patterns = [
            "*.md", "*.rst", "*.txt",
            "README*", "readme*",
            "*.pdf", "*.docx"
        ]
        
        for pattern in doc_patterns:
            for doc_file in self.project_root.rglob(pattern):
                if doc_file.is_file():
                    relative_path = str(doc_file.relative_to(self.project_root))
                    self.project_info["documents"][relative_path] = {
                        "path": str(doc_file),
                        "type": doc_file.suffix,
                        "size": doc_file.stat().st_size
                    }
    
    def scan_code_structure(self):
        """扫描代码结构"""
        code_extensions = [
            ".java", ".py", ".js", ".ts", ".tsx", ".jsx",
            ".html", ".css", ".scss", ".vue",
            ".go", ".cpp", ".c", ".h",
            ".cs", ".rb", ".php"
        ]
        
        for ext in code_extensions:
            for code_file in self.project_root.rglob(f"*{ext}"):
                if code_file.is_file():
                    relative_path = str(code_file.relative_to(self.project_root))
                    directory = os.path.dirname(relative_path)
                    
                    if directory not in self.project_info["code_structure"]:
                        self.project_info["code_structure"][directory] = []
                    
                    self.project_info["code_structure"][directory].append(os.path.basename(relative_path))
    
    def analyze_dependencies(self):
        """分析项目依赖"""
        dependency_files = [
            "pom.xml", "build.gradle", "gradle.properties",
            "package.json", "requirements.txt", "setup.py",
            "go.mod", "go.sum", "Cargo.toml"
        ]
        
        for dep_file in dependency_files:
            dep_path = self.project_root / dep_file
            if dep_path.exists():
                relative_path = str(dep_path.relative_to(self.project_root))
                try:
                    content = dep_path.read_text(encoding='utf-8')
                    self.project_info["dependencies"][relative_path] = {
                        "path": str(dep_path),
                        "content": content[:1000]  # 只保存前1000字符
                    }
                except Exception as e:
                    print(f"分析依赖文件 {relative_path} 时出错: {e}")
    
    def identify_technologies(self):
        """识别项目技术栈"""
        technologies = set()
        
        # 从依赖文件识别
        for dep_file, dep_info in self.project_info["dependencies"].items():
            content = dep_info.get("content", "")
            
            # Java/Spring
            if "spring-boot" in content.lower():
                technologies.add("Spring Boot")
            if "spring-cloud" in content.lower():
                technologies.add("Spring Cloud")
            
            # JavaScript/TypeScript
            if "react" in content.lower():
                technologies.add("React")
            if "vue" in content.lower():
                technologies.add("Vue")
            if "angular" in content.lower():
                technologies.add("Angular")
            
            # Python
            if "django" in content.lower():
                technologies.add("Django")
            if "flask" in content.lower():
                technologies.add("Flask")
            
            # 数据库
            if "mysql" in content.lower():
                technologies.add("MySQL")
            if "postgresql" in content.lower():
                technologies.add("PostgreSQL")
            if "mongodb" in content.lower():
                technologies.add("MongoDB")
        
        # 从代码文件识别
        for directory, files in self.project_info["code_structure"].items():
            for file in files:
                if file.endswith(".java"):
                    technologies.add("Java")
                elif file.endswith(".py"):
                    technologies.add("Python")
                elif file.endswith(".js") or file.endswith(".ts"):
                    technologies.add("JavaScript/TypeScript")
                elif file.endswith(".go"):
                    technologies.add("Go")
        
        self.project_info["technologies"] = list(technologies)
    
    def generate_role_understanding(self):
        """为各角色生成项目理解"""
        # 架构师理解
        self.project_info["roles"]["architect"]["understanding"] = self._generate_architect_understanding()
        self.project_info["roles"]["architect"]["key_areas"] = [
            "系统架构设计",
            "技术栈选型",
            "模块划分与依赖",
            "性能与安全性",
            "部署架构"
        ]
        
        # 产品经理理解
        self.project_info["roles"]["product_manager"]["understanding"] = self._generate_product_manager_understanding()
        self.project_info["roles"]["product_manager"]["key_areas"] = [
            "产品需求分析",
            "用户故事与场景",
            "功能模块梳理",
            "业务流程分析",
            "验收标准定义"
        ]
        
        # 测试专家理解
        self.project_info["roles"]["test_expert"]["understanding"] = self._generate_test_expert_understanding()
        self.project_info["roles"]["test_expert"]["key_areas"] = [
            "测试策略制定",
            "测试用例设计",
            "自动化测试方案",
            "性能与安全测试",
            "缺陷管理流程"
        ]
        
        # 独立开发者理解
        self.project_info["roles"]["solo_coder"]["understanding"] = self._generate_solo_coder_understanding()
        self.project_info["roles"]["solo_coder"]["key_areas"] = [
            "代码结构与组织",
            "核心功能实现",
            "API 接口开发",
            "单元测试编写",
            "代码质量保障"
        ]
    
    def _generate_architect_understanding(self) -> str:
        """生成架构师视角的项目理解"""
        understanding = f"# {self.project_info['project_name']} 项目架构理解\n\n"
        
        # 项目概览
        understanding += "## 项目概览\n\n"
        understanding += f"- **项目名称**: {self.project_info['project_name']}\n"
        understanding += f"- **项目路径**: {self.project_info['root_path']}\n"
        understanding += f"- **技术栈**: {', '.join(self.project_info['technologies']) if self.project_info['technologies'] else '未识别'}\n\n"
        
        # 代码结构
        understanding += "## 代码结构\n\n"
        for directory, files in sorted(self.project_info['code_structure'].items()):
            if files:
                understanding += f"### {directory or '根目录'}\n"
                for file in files[:10]:  # 只显示前10个文件
                    understanding += f"- {file}\n"
                if len(files) > 10:
                    understanding += f"- ... 等 {len(files) - 10} 个文件\n"
                understanding += "\n"
        
        # 依赖分析
        understanding += "## 依赖分析\n\n"
        for dep_file, dep_info in self.project_info['dependencies'].items():
            understanding += f"### {dep_file}\n"
            understanding += f"```\n{dep_info.get('content', '')}\n```\n\n"
        
        # 关键文档
        understanding += "## 关键文档\n\n"
        for doc_path, doc_info in self.project_info['documents'].items():
            if any(keyword in doc_path.lower() for keyword in ['readme', 'architecture', 'design', 'spec']):
                understanding += f"- [{doc_path}]({doc_info['path']})\n"
        
        return understanding
    
    def _generate_product_manager_understanding(self) -> str:
        """生成产品经理视角的项目理解"""
        understanding = f"# {self.project_info['project_name']} 项目产品理解\n\n"
        
        # 项目概览
        understanding += "## 项目概览\n\n"
        understanding += f"- **项目名称**: {self.project_info['project_name']}\n"
        understanding += f"- **项目路径**: {self.project_info['root_path']}\n\n"
        
        # 功能模块
        understanding += "## 功能模块\n\n"
        # 从代码结构推断功能模块
        modules = set()
        for directory in self.project_info['code_structure'].keys():
            if directory:
                module = directory.split('/')[0]
                modules.add(module)
        
        for module in sorted(modules):
            understanding += f"- **{module}**: 待分析\n"
        
        # 业务文档
        understanding += "## 业务文档\n\n"
        for doc_path, doc_info in self.project_info['documents'].items():
            if any(keyword in doc_path.lower() for keyword in ['prd', 'requirement', '需求', 'product']):
                understanding += f"- [{doc_path}]({doc_info['path']})\n"
        
        # 验收标准
        understanding += "## 验收标准\n\n"
        understanding += "- 待根据需求文档分析\n"
        
        return understanding
    
    def _generate_test_expert_understanding(self) -> str:
        """生成测试专家视角的项目理解"""
        understanding = f"# {self.project_info['project_name']} 项目测试理解\n\n"
        
        # 项目概览
        understanding += "## 项目概览\n\n"
        understanding += f"- **项目名称**: {self.project_info['project_name']}\n"
        understanding += f"- **项目路径**: {self.project_info['root_path']}\n"
        understanding += f"- **技术栈**: {', '.join(self.project_info['technologies']) if self.project_info['technologies'] else '未识别'}\n\n"
        
        # 测试相关文件
        understanding += "## 测试相关文件\n\n"
        test_files = []
        for directory, files in self.project_info['code_structure'].items():
            for file in files:
                if 'test' in file.lower() or 'spec' in file.lower():
                    test_files.append(os.path.join(directory, file))
        
        if test_files:
            for test_file in test_files[:10]:
                understanding += f"- {test_file}\n"
            if len(test_files) > 10:
                understanding += f"- ... 等 {len(test_files) - 10} 个测试文件\n"
        else:
            understanding += "- 未发现测试文件\n"
        
        # 测试策略
        understanding += "## 测试策略\n\n"
        understanding += "- 待制定\n"
        
        return understanding
    
    def _generate_solo_coder_understanding(self) -> str:
        """生成独立开发者视角的项目理解"""
        understanding = f"# {self.project_info['project_name']} 项目开发理解\n\n"
        
        # 项目概览
        understanding += "## 项目概览\n\n"
        understanding += f"- **项目名称**: {self.project_info['project_name']}\n"
        understanding += f"- **项目路径**: {self.project_info['root_path']}\n"
        understanding += f"- **技术栈**: {', '.join(self.project_info['technologies']) if self.project_info['technologies'] else '未识别'}\n\n"
        
        # 代码结构
        understanding += "## 代码结构\n\n"
        for directory, files in sorted(self.project_info['code_structure'].items()):
            if files:
                understanding += f"### {directory or '根目录'}\n"
                for file in files[:15]:  # 显示前15个文件
                    understanding += f"- {file}\n"
                if len(files) > 15:
                    understanding += f"- ... 等 {len(files) - 15} 个文件\n"
                understanding += "\n"
        
        # 开发指南
        understanding += "## 开发指南\n\n"
        for doc_path, doc_info in self.project_info['documents'].items():
            if any(keyword in doc_path.lower() for keyword in ['readme', 'guide', '开发', 'dev']):
                understanding += f"- [{doc_path}]({doc_info['path']})\n"
        
        return understanding
    
    def generate(self) -> Dict[str, Any]:
        """生成完整的项目理解"""
        self.scan_documents()
        self.scan_code_structure()
        self.analyze_dependencies()
        self.identify_technologies()
        self.generate_role_understanding()
        return self.project_info
    
    def save(self, output_dir: str):
        """保存项目理解文档"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存整体项目信息
        with open(os.path.join(output_dir, 'project_understanding.json'), 'w', encoding='utf-8') as f:
            json.dump(self.project_info, f, ensure_ascii=False, indent=2)
        
        # 保存各角色的理解文档
        for role, info in self.project_info['roles'].items():
            role_dir = os.path.join(output_dir, 'roles')
            os.makedirs(role_dir, exist_ok=True)
            
            with open(os.path.join(role_dir, f'{role}_understanding.md'), 'w', encoding='utf-8') as f:
                f.write(info['understanding'])
        
        print(f"项目理解文档已保存到: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="生成项目理解文档")
    parser.add_argument("project_root", help="项目根目录路径")
    parser.add_argument("--output", default=".trae/skills/trae-multi-agent/docs/project-understanding", help="输出目录路径")
    
    args = parser.parse_args()
    
    understander = ProjectUnderstanding(args.project_root)
    project_info = understander.generate()
    understander.save(args.output)
    
    print("\n项目理解生成完成！")
    print(f"- 输出目录: {args.output}")
    print("- 包含文件:")
    print("  - project_understanding.json (整体项目信息)")
    print("  - roles/architect_understanding.md (架构师理解)")
    print("  - roles/product_manager_understanding.md (产品经理理解)")
    print("  - roles/test_expert_understanding.md (测试专家理解)")
    print("  - roles/solo_coder_understanding.md (独立开发者理解)")

if __name__ == "__main__":
    main()

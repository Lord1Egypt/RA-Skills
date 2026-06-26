"""
Project Scanner - 项目结构扫描器
扫描项目结构，识别技术栈和模块
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class ProjectScanner:
    """项目结构扫描器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        
    def scan(self) -> Dict:
        """执行项目扫描"""
        return {
            'name': self._get_project_name(),
            'type': self._detect_project_type(),
            'structure': self._analyze_structure(),
            'modules': self._identify_modules(),
            'tech_stack': self._detect_tech_stack(),
            'build_info': self._get_build_info(),
        }
    
    def _get_project_name(self) -> str:
        """获取项目名称"""
        # 优先从 pom.xml / package.json 获取
        pom_xml = self.project_path / 'pom.xml'
        if pom_xml.exists():
            content = pom_xml.read_text(encoding='utf-8')
            match = re.search(r'<artifactId>([^<]+)</artifactId>', content)
            if match:
                return match.group(1)
        
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            content = package_json.read_text(encoding='utf-8')
            data = json.loads(content)
            return data.get('name', self.project_path.name)
        
        return self.project_path.name
    
    def _detect_project_type(self) -> str:
        """检测项目类型"""
        if (self.project_path / 'pom.xml').exists():
            return 'maven'
        if (self.project_path / 'build.gradle').exists():
            return 'gradle'
        if (self.project_path / 'go.mod').exists():
            return 'go'
        if (self.project_path / 'requirements.txt').exists():
            return 'python'
        if (self.project_path / 'package.json').exists():
            return 'node'
        if (self.project_path / 'Cargo.toml').exists():
            return 'rust'
        return 'unknown'
    
    def _analyze_structure(self) -> Dict:
        """分析项目结构"""
        structure = {
            'root_files': [],
            'directories': [],
            'max_depth': 0
        }
        
        # 扫描顶层目录
        for item in self.project_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                structure['directories'].append(item.name)
            elif item.is_file():
                structure['root_files'].append(item.name)
        
        # 扫描模块目录
        modules = []
        for dir_name in structure['directories']:
            if dir_name not in ['target', 'node_modules', '__pycache__', 'venv', '.git']:
                modules.append({
                    'name': dir_name,
                    'path': str(self.project_path / dir_name)
                })
        
        structure['modules'] = modules
        return structure
    
    def _identify_modules(self) -> List[Dict]:
        """识别多模块项目"""
        modules = []
        
        # Maven 多模块
        if self._detect_project_type() == 'maven':
            pom_xml = self.project_path / 'pom.xml'
            if pom_xml.exists():
                content = pom_xml.read_text(encoding='utf-8')
                module_matches = re.findall(r'<module>([^<]+)</module>', content)
                for module_name in module_matches:
                    module_path = self.project_path / module_name
                    if module_path.exists():
                        modules.append({
                            'name': module_name,
                            'path': str(module_path),
                            'type': 'maven_module'
                        })
        
        return modules
    
    def _detect_tech_stack(self) -> Dict:
        """检测技术栈"""
        tech_stack = {
            'language': 'unknown',
            'framework': 'unknown',
            'database': 'unknown',
            'cache': 'unknown',
            'mq': 'unknown',
            'versions': {}
        }
        
        project_type = self._detect_project_type()
        
        if project_type == 'maven':
            self._detect_java_stack(tech_stack)
        elif project_type == 'node':
            self._detect_node_stack(tech_stack)
        elif project_type == 'python':
            self._detect_python_stack(tech_stack)
        elif project_type == 'go':
            self._detect_go_stack(tech_stack)
        
        return tech_stack
    
    def _detect_java_stack(self, tech_stack: Dict) -> None:
        """检测 Java 技术栈"""
        tech_stack['language'] = 'Java'
        
        pom_xml = self.project_path / 'pom.xml'
        if not pom_xml.exists():
            return
        
        content = pom_xml.read_text(encoding='utf-8')
        
        # 检测 Spring Boot
        spring_boot = re.search(r'<artifactId>spring-boot-starter-parent</artifactId>.*?<version>([^<]+)</version>', content, re.DOTALL)
        if spring_boot:
            tech_stack['framework'] = f"Spring Boot {spring_boot.group(1)}"
        
        # 检测 Java 版本
        java_version = re.search(r'<java\.version>([^<]+)</java\.version>', content)
        if java_version:
            tech_stack['versions']['java'] = java_version.group(1)
        
        # 检测数据库
        if 'mybatis' in content.lower():
            tech_stack['database'] = 'MyBatis'
        if 'spring-boot-starter-data-jpa' in content:
            tech_stack['database'] = 'JPA'
        if 'mysql-connector' in content:
            tech_stack['database'] = 'MySQL'
        if 'postgresql' in content:
            tech_stack['database'] = 'PostgreSQL'
        
        # 检测缓存
        if 'spring-boot-starter-data-redis' in content:
            tech_stack['cache'] = 'Redis'
        
        # 检测消息队列
        if 'rocketmq' in content.lower():
            tech_stack['mq'] = 'RocketMQ'
        if 'kafka' in content.lower():
            tech_stack['mq'] = 'Kafka'
    
    def _detect_node_stack(self, tech_stack: Dict) -> None:
        """检测 Node.js 技术栈"""
        tech_stack['language'] = 'Node.js'
        
        package_json = self.project_path / 'package.json'
        if not package_json.exists():
            return
        
        content = package_json.read_text(encoding='utf-8')
        data = json.loads(content)
        
        deps = list(data.get('dependencies', {}).keys())
        
        if 'express' in deps:
            tech_stack['framework'] = 'Express'
        if 'koa' in deps:
            tech_stack['framework'] = 'Koa'
        if 'nestjs' in str(deps):
            tech_stack['framework'] = 'NestJS'
        
        if 'react' in deps:
            tech_stack['framework'] = 'React'
        if 'vue' in deps:
            tech_stack['framework'] = 'Vue'
        if 'angular' in deps:
            tech_stack['framework'] = 'Angular'
    
    def _detect_python_stack(self, tech_stack: Dict) -> None:
        """检测 Python 技术栈"""
        tech_stack['language'] = 'Python'
        
        requirements = self.project_path / 'requirements.txt'
        if not requirements.exists():
            return
        
        content = requirements.read_text(encoding='utf-8').lower()
        
        if 'django' in content:
            tech_stack['framework'] = 'Django'
        if 'flask' in content:
            tech_stack['framework'] = 'Flask'
        if 'fastapi' in content:
            tech_stack['framework'] = 'FastAPI'
    
    def _detect_go_stack(self, tech_stack: Dict) -> None:
        """检测 Go 技术栈"""
        tech_stack['language'] = 'Go'
        
        go_mod = self.project_path / 'go.mod'
        if not go_mod.exists():
            return
        
        content = go_mod.read_text(encoding='utf-8')
        
        if 'gin-gonic' in content or 'gin' in content:
            tech_stack['framework'] = 'Gin'
        if 'echo' in content:
            tech_stack['framework'] = 'Echo'
        if 'fiber' in content:
            tech_stack['framework'] = 'Fiber'
    
    def _get_build_info(self) -> Dict:
        """获取构建信息"""
        build_info = {
            'type': self._detect_project_type(),
            'files': []
        }
        
        # 收集构建相关文件
        build_files = ['pom.xml', 'build.gradle', 'package.json', 
                      'requirements.txt', 'go.mod', 'Cargo.toml']
        
        for bf in build_files:
            if (self.project_path / bf).exists():
                build_info['files'].append(bf)
        
        return build_info


# 导出
__all__ = ['ProjectScanner']

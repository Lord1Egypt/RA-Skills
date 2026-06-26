#!/usr/bin/env python3
"""
项目代码库分析脚本
分析项目结构、技术栈、模块依赖等
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any


class CodebaseAnalyzer:
    """代码库分析器"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.analysis_result = {
            "project_type": None,
            "languages": [],
            "frameworks": [],
            "databases": [],
            "middleware": [],
            "structure": {},
            "entry_points": [],
            "config_files": [],
        }

    def analyze(self) -> Dict[str, Any]:
        """执行完整分析"""
        self._detect_project_type()
        self._scan_structure()
        self._detect_tech_stack()
        self._find_entry_points()
        return self.analysis_result

    def _detect_project_type(self):
        """检测项目类型"""
        root_files = set(os.listdir(self.project_path))

        # 前端项目
        if "package.json" in root_files:
            self.analysis_result["project_type"] = "frontend"
            self._analyze_frontend()

        # Java 后端
        elif "pom.xml" in root_files or "build.gradle" in root_files:
            self.analysis_result["project_type"] = "java-backend"
            self._analyze_java_backend()

        # Python 项目
        elif "requirements.txt" in root_files or "pyproject.toml" in root_files:
            self.analysis_result["project_type"] = "python"
            self._analyze_python()

        # 全栈项目
        elif "frontend" in os.listdir(self.project_path) and any(
            f in root_files for f in ["pom.xml", "build.gradle", "requirements.txt"]
        ):
            self.analysis_result["project_type"] = "fullstack"

    def _analyze_frontend(self):
        """分析前端项目"""
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            deps = {
                **package_data.get("dependencies", {}),
                **package_data.get("devDependencies", {}),
            }

            # 检测框架
            if "vue" in deps:
                self.analysis_result["frameworks"].append(f"Vue {deps['vue']}")
            if "react" in deps:
                self.analysis_result["frameworks"].append(f"React {deps['react']}")
            if "angular" in deps:
                self.analysis_result["frameworks"].append("Angular")

            # 检测语言
            if "typescript" in deps:
                self.analysis_result["languages"].append("TypeScript")
            else:
                self.analysis_result["languages"].append("JavaScript")

            # 检测构建工具
            if "vite" in deps:
                self.analysis_result["frameworks"].append("Vite")
            if "webpack" in deps:
                self.analysis_result["frameworks"].append("Webpack")

    def _analyze_java_backend(self):
        """分析 Java 后端项目"""
        pom_path = self.project_path / "pom.xml"
        if pom_path.exists():
            with open(pom_path, "r", encoding="utf-8") as f:
                pom_content = f.read()

            self.analysis_result["languages"].append("Java")

            # 检测框架
            if "spring-boot" in pom_content.lower():
                self.analysis_result["frameworks"].append("Spring Boot")
            if "spring-cloud" in pom_content.lower():
                self.analysis_result["frameworks"].append("Spring Cloud")

            # 检测数据库
            if "mysql" in pom_content.lower():
                self.analysis_result["databases"].append("MySQL")
            if "postgresql" in pom_content.lower():
                self.analysis_result["databases"].append("PostgreSQL")
            if "mongodb" in pom_content.lower():
                self.analysis_result["databases"].append("MongoDB")

            # 检测中间件
            if "kafka" in pom_content.lower():
                self.analysis_result["middleware"].append("Kafka")
            if "redis" in pom_content.lower():
                self.analysis_result["middleware"].append("Redis")
            if "elasticsearch" in pom_content.lower():
                self.analysis_result["middleware"].append("Elasticsearch")
            if "minio" in pom_content.lower():
                self.analysis_result["middleware"].append("MinIO")

    def _analyze_python(self):
        """分析 Python 项目"""
        self.analysis_result["languages"].append("Python")

        requirements_path = self.project_path / "requirements.txt"
        if requirements_path.exists():
            with open(requirements_path, "r", encoding="utf-8") as f:
                requirements = f.read()

            if "django" in requirements.lower():
                self.analysis_result["frameworks"].append("Django")
            if "fastapi" in requirements.lower():
                self.analysis_result["frameworks"].append("FastAPI")
            if "flask" in requirements.lower():
                self.analysis_result["frameworks"].append("Flask")

    def _scan_structure(self):
        """扫描项目结构"""
        structure = {}

        for root, dirs, files in os.walk(self.project_path):
            # 跳过隐藏目录和常见忽略目录
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d
                not in [
                    "node_modules",
                    "target",
                    "build",
                    "dist",
                    "__pycache__",
                    "venv",
                ]
            ]

            rel_path = os.path.relpath(root, self.project_path)
            if rel_path == ".":
                rel_path = "root"

            structure[rel_path] = {"dirs": dirs[:], "files": files}

        self.analysis_result["structure"] = structure

    def _detect_tech_stack(self):
        """检测完整技术栈"""
        # 扫描配置文件
        config_patterns = [
            "*.yml",
            "*.yaml",
            "*.properties",
            "*.json",
            "*.xml",
            "*.toml",
        ]

        config_files = []
        for pattern in config_patterns:
            config_files.extend(self.project_path.glob(f"**/{pattern}"))

        self.analysis_result["config_files"] = [
            str(f.relative_to(self.project_path)) for f in config_files[:20]
        ]  # 限制数量

    def _find_entry_points(self):
        """查找入口文件"""
        entry_patterns = [
            "main.py",
            "app.py",
            "index.js",
            "index.ts",
            "Main.java",
            "Application.java",
            "*Application.java",
        ]

        entry_points = []
        for pattern in entry_patterns:
            entry_points.extend(self.project_path.glob(f"**/{pattern}"))

        self.analysis_result["entry_points"] = [
            str(f.relative_to(self.project_path)) for f in entry_points
        ]


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze_codebase.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    analyzer = CodebaseAnalyzer(project_path)
    result = analyzer.analyze()

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

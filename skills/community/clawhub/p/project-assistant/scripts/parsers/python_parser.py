#!/usr/bin/env python3
"""
Python项目解析器
解析requirements.txt, pyproject.toml等
"""

import os
import sys
import json
import re
import configparser
from typing import Dict, List, Any, Optional


def parse_requirements(req_path: str) -> List[Dict[str, str]]:
    """解析requirements.txt"""
    deps = []
    try:
        with open(req_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 匹配 package==version, package>=version 等
                match = re.match(r'^([a-zA-Z0-9_-]+)\s*([<>=!]+)\s*([^\s,]+)', line)
                if match:
                    deps.append({
                        'name': match.group(1),
                        'operator': match.group(2),
                        'version': match.group(3)
                    })
                else:
                    # 无版本限制
                    match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                    if match:
                        deps.append({'name': match.group(1), 'version': 'any'})
    except Exception as e:
        return [{'error': str(e)}]

    return deps


def parse_pyproject(pyproject_path: str) -> Dict[str, Any]:
    """解析pyproject.toml"""
    result = {
        'name': '',
        'version': '',
        'description': '',
        'dependencies': [],
        'dev_dependencies': [],
        'python_version': '',
        'error': None
    }

    try:
        # 简单解析TOML (不使用toml库)
        with open(pyproject_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # [project] 部分
        project_match = re.search(r'\[project\](.+?)(?=\[|$)', content, re.DOTALL)
        if project_match:
            project = project_match.group(1)

            name_match = re.search(r'name\s*=\s*"([^"]+)"', project)
            if name_match:
                result['name'] = name_match.group(1)

            version_match = re.search(r'version\s*=\s*"([^"]+)"', project)
            if version_match:
                result['version'] = version_match.group(1)

            desc_match = re.search(r'description\s*=\s*"([^"]+)"', project)
            if desc_match:
                result['description'] = desc_match.group(1)

            python_match = re.search(r'requires-python\s*=\s*"([^"]+)"', project)
            if python_match:
                result['python_version'] = python_match.group(1)

        # dependencies
        for match in re.finditer(r'dependencies\s*=\s*\[([^\]]+)\]', content):
            deps_str = match.group(1)
            for dep in re.findall(r'"([^"]+)"', deps_str):
                result['dependencies'].append(dep)

    except Exception as e:
        result['error'] = str(e)

    return result


def parse_setup_py(setup_path: str) -> Dict[str, Any]:
    """解析setup.py"""
    result = {
        'name': '',
        'version': '',
        'install_requires': [],
        'error': None
    }

    try:
        with open(setup_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 简单提取
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
        if name_match:
            result['name'] = name_match.group(1)

        version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if version_match:
            result['version'] = version_match.group(1)

        # install_requires
        req_match = re.search(r'install_requires\s*=\s*\[([^\]]+)\]', content, re.DOTALL)
        if req_match:
            for dep in re.findall(r'["\']([^"\']+)["\']', req_match.group(1)):
                result['install_requires'].append(dep)

    except Exception as e:
        result['error'] = str(e)

    return result


def detect_framework(deps: List[str]) -> List[str]:
    """检测Python框架"""
    frameworks = []
    dep_names = [d.get('name', d) if isinstance(d, dict) else d for d in deps]
    dep_names_lower = [d.lower() for d in dep_names]

    framework_map = {
        'django': 'Django',
        'flask': 'Flask',
        'fastapi': 'FastAPI',
        'tornado': 'Tornado',
        'aiohttp': 'Aiohttp',
        'sanic': 'Sanic',
        'starlette': 'Starlette',
        'pydantic': 'Pydantic',
        'sqlalchemy': 'SQLAlchemy',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'torch': 'PyTorch',
        'tensorflow': 'TensorFlow',
        'scikit-learn': 'Scikit-learn',
    }

    for dep in dep_names_lower:
        for key, framework in framework_map.items():
            if key in dep:
                if framework not in frameworks:
                    frameworks.append(framework)

    return frameworks


def analyze_python_project(target_dir: str) -> Dict[str, Any]:
    """分析Python项目"""
    result = {
        'type': 'python',
        'config_files': [],
        'dependencies': [],
        'frameworks': [],
        'main_file': None,
    }

    # 查找配置文件
    config_files = {
        'requirements.txt': None,
        'pyproject.toml': None,
        'setup.py': None,
        'setup.cfg': None,
    }

    for fname in config_files:
        fpath = os.path.join(target_dir, fname)
        if os.path.exists(fpath):
            config_files[fname] = fpath
            result['config_files'].append(fname)

    # 解析依赖
    if config_files['pyproject.toml']:
        pyproject = parse_pyproject(config_files['pyproject.toml'])
        result['dependencies'].extend(pyproject.get('dependencies', []))
        result['name'] = pyproject.get('name', '')
        result['version'] = pyproject.get('version', '')

    if config_files['requirements.txt']:
        deps = parse_requirements(config_files['requirements.txt'])
        result['dependencies'].extend(deps)

    # 检测框架
    dep_names = []
    for dep in result['dependencies']:
        if isinstance(dep, dict):
            dep_names.append(dep.get('name', ''))
        else:
            dep_names.append(str(dep))

    result['frameworks'] = detect_framework(dep_names)

    # 查找主文件
    main_files = ['main.py', 'app.py', 'run.py', 'manage.py', '__main__.py']
    for mf in main_files:
        if os.path.exists(os.path.join(target_dir, mf)):
            result['main_file'] = mf
            break

    return result


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    result = analyze_python_project(target_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
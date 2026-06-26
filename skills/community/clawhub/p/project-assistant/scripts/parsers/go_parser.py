#!/usr/bin/env python3
"""
Go项目解析器
解析go.mod文件
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_go_mod(mod_path: str) -> Dict[str, Any]:
    """解析go.mod"""
    result = {
        'module': '',
        'go_version': '',
        'dependencies': [],
        'replace': [],
        'error': None
    }

    try:
        with open(mod_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # module名称
        match = re.search(r'module\s+(\S+)', content)
        if match:
            result['module'] = match.group(1).strip('"').strip("'")

        # go版本
        match = re.search(r'go\s+(\d+\.\d+(?:\.\d+)?)', content)
        if match:
            result['go_version'] = match.group(1)

        # require块
        require_match = re.search(r'require\s*\(([^)]+)\)', content, re.DOTALL)
        if require_match:
            require_block = require_match.group(1)
            for line in require_block.strip().split('\n'):
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    result['dependencies'].append({
                        'path': parts[0],
                        'version': parts[1]
                    })

    except Exception as e:
        result['error'] = str(e)

    return result


def detect_go_framework(deps: List[Dict]) -> List[str]:
    """检测Go框架"""
    frameworks = []
    framework_map = {
        'gin-gonic/gin': 'Gin',
        'labstack/echo': 'Echo',
        'gofiber/fiber': 'Fiber',
        'go-chi/chi': 'Chi',
        'gorilla/mux': 'Gorilla Mux',
        'gorm': 'GORM',
        'spf13/cobra': 'Cobra',
        'spf13/viper': 'Viper',
    }

    for dep in deps:
        path = dep.get('path', '')
        for key, framework in framework_map.items():
            if key in path and framework not in frameworks:
                frameworks.append(framework)

    return frameworks


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    mod_path = os.path.join(target_dir, 'go.mod')

    if not os.path.exists(mod_path):
        result = {'error': 'go.mod not found'}
    else:
        result = parse_go_mod(mod_path)
        result['frameworks'] = detect_go_framework(result.get('dependencies', []))

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Rust项目解析器
解析Cargo.toml文件
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_cargo_toml(cargo_path: str) -> Dict[str, Any]:
    """解析Cargo.toml"""
    result = {
        'name': '',
        'version': '',
        'edition': '',
        'dependencies': [],
        'dev_dependencies': [],
        'build_dependencies': [],
        'features': {},
        'bin': [],
        'lib': None,
        'error': None
    }

    try:
        with open(cargo_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # [package] 部分
        pkg_match = re.search(r'\[package\](.+?)(?=\[|$)', content, re.DOTALL)
        if pkg_match:
            pkg = pkg_match.group(1)

            name_match = re.search(r'name\s*=\s*"([^"]+)"', pkg)
            if name_match:
                result['name'] = name_match.group(1)

            version_match = re.search(r'version\s*=\s*"([^"]+)"', pkg)
            if version_match:
                result['version'] = version_match.group(1)

            edition_match = re.search(r'edition\s*=\s*"([^"]+)"', pkg)
            if edition_match:
                result['edition'] = edition_match.group(1)

        # [dependencies] 部分
        deps_match = re.search(r'\[dependencies\](.+?)(?=\[|$)', content, re.DOTALL)
        if deps_match:
            for line in deps_match.group(1).strip().split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 简单格式: name = "version"
                match = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*"([^"]+)"', line)
                if match:
                    result['dependencies'].append({
                        'name': match.group(1),
                        'version': match.group(2)
                    })
                    continue

                # 详细格式: name = { version = "x", ... }
                match = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*\{', line)
                if match:
                    result['dependencies'].append({
                        'name': match.group(1),
                        'version': 'detailed'
                    })

        # [dev-dependencies]
        dev_deps_match = re.search(r'\[dev-dependencies\](.+?)(?=\[|$)', content, re.DOTALL)
        if dev_deps_match:
            for line in dev_deps_match.group(1).strip().split('\n'):
                match = re.match(r'^([a-zA-Z0-9_-]+)\s*=', line.strip())
                if match:
                    result['dev_dependencies'].append(match.group(1))

    except Exception as e:
        result['error'] = str(e)

    return result


def detect_rust_framework(deps: List[Dict]) -> List[str]:
    """检测Rust框架"""
    frameworks = []
    dep_names = [d.get('name', '') for d in deps]
    dep_names_lower = [d.lower() for d in dep_names]

    framework_map = {
        'tokio': 'Tokio',
        'actix-web': 'Actix Web',
        'rocket': 'Rocket',
        'warp': 'Warp',
        'axum': 'Axum',
        'serde': 'Serde',
        'clap': 'Clap',
        'diesel': 'Diesel',
        'sqlx': 'SQLx',
        'sea-orm': 'SeaORM',
        'egui': 'egui',
        'iced': 'Iced',
        'yew': 'Yew',
        'leptos': 'Leptos',
        'bevy': 'Bevy',
    }

    for dep in dep_names_lower:
        for key, framework in framework_map.items():
            if key in dep and framework not in frameworks:
                frameworks.append(framework)

    return frameworks


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    cargo_path = os.path.join(target_dir, 'Cargo.toml')

    if not os.path.exists(cargo_path):
        result = {'error': 'Cargo.toml not found'}
    else:
        result = parse_cargo_toml(cargo_path)
        result['frameworks'] = detect_rust_framework(result.get('dependencies', []))

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
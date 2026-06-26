#!/usr/bin/env python3
"""
package.json 解析器
解析Node.js/Web前端项目配置
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional


def parse_package_json(package_path: str) -> Dict[str, Any]:
    """解析package.json"""
    result = {
        'name': '',
        'version': '',
        'description': '',
        'main': '',
        'scripts': {},
        'dependencies': {},
        'dev_dependencies': {},
        'peer_dependencies': {},
        'engines': {},
        'framework': None,
        'frameworks': [],
        'error': None
    }

    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            pkg = json.load(f)

        result['name'] = pkg.get('name', '')
        result['version'] = pkg.get('version', '')
        result['description'] = pkg.get('description', '')
        result['main'] = pkg.get('main', '')
        result['scripts'] = pkg.get('scripts', {})
        result['dependencies'] = pkg.get('dependencies', {})
        result['dev_dependencies'] = pkg.get('devDependencies', {})
        result['peer_dependencies'] = pkg.get('peerDependencies', {})
        result['engines'] = pkg.get('engines', {})

        # 识别框架
        all_deps = {**result['dependencies'], **result['dev_dependencies']}

        framework_map = {
            'react': 'React',
            'vue': 'Vue',
            '@angular/core': 'Angular',
            'svelte': 'Svelte',
            'next': 'Next.js',
            'nuxt': 'Nuxt.js',
            'remix': 'Remix',
            'gatsby': 'Gatsby',
            'express': 'Express',
            'koa': 'Koa',
            'fastify': 'Fastify',
            'nest': 'NestJS',
            'electron': 'Electron',
            'tauri': 'Tauri',
            'react-native': 'React Native',
            'expo': 'Expo',
        }

        for dep, framework in framework_map.items():
            if dep in all_deps:
                result['frameworks'].append({
                    'name': framework,
                    'version': all_deps[dep]
                })

        if result['frameworks']:
            result['framework'] = result['frameworks'][0]['name']

    except Exception as e:
        result['error'] = str(e)

    return result


def find_package_json(target_dir: str) -> Optional[str]:
    """查找package.json"""
    package_path = os.path.join(target_dir, 'package.json')
    if os.path.exists(package_path):
        return package_path
    return None


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    package_path = find_package_json(target_dir)

    if not package_path:
        result = {'error': 'package.json not found'}
    else:
        result = parse_package_json(package_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Maven pom.xml 解析器
解析Java/Maven项目配置
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional


def parse_pom(pom_path: str) -> Dict[str, Any]:
    """解析pom.xml"""
    result = {
        'groupId': '',
        'artifactId': '',
        'version': '',
        'packaging': 'jar',
        'properties': {},
        'dependencies': [],
        'modules': [],
        'plugins': [],
        'parent': None,
        'spring_boot': False,
        'error': None
    }

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        # 处理命名空间
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

        def find_text(parent, tag):
            elem = parent.find(f'm:{tag}', ns) if ns else parent.find(tag)
            return elem.text if elem is not None and elem.text else ''

        # 基本信息
        result['groupId'] = find_text(root, 'groupId')
        result['artifactId'] = find_text(root, 'artifactId')
        result['version'] = find_text(root, 'version')
        result['packaging'] = find_text(root, 'packaging') or 'jar'

        # parent
        parent = root.find('m:parent', ns) if ns else root.find('parent')
        if parent is not None:
            result['parent'] = {
                'groupId': find_text(parent, 'groupId'),
                'artifactId': find_text(parent, 'artifactId'),
                'version': find_text(parent, 'version'),
            }
            # 检测Spring Boot
            if 'spring-boot-starter-parent' in result['parent'].get('artifactId', ''):
                result['spring_boot'] = True

        # properties
        props = root.find('m:properties', ns) if ns else root.find('properties')
        if props is not None:
            for prop in props:
                tag = prop.tag.split('}')[-1] if '}' in prop.tag else prop.tag
                result['properties'][tag] = prop.text or ''

        # dependencies
        deps = root.find('m:dependencies', ns) if ns else root.find('dependencies')
        if deps is not None:
            for dep in deps.findall('m:dependency', ns) if ns else deps.findall('dependency'):
                dep_info = {
                    'groupId': find_text(dep, 'groupId'),
                    'artifactId': find_text(dep, 'artifactId'),
                    'version': find_text(dep, 'version'),
                    'scope': find_text(dep, 'scope') or 'compile',
                }
                result['dependencies'].append(dep_info)

                # 检测Spring Boot
                if 'spring-boot' in dep_info['artifactId']:
                    result['spring_boot'] = True

        # modules (多模块项目)
        modules = root.find('m:modules', ns) if ns else root.find('modules')
        if modules is not None:
            for mod in modules.findall('m:module', ns) if ns else modules.findall('module'):
                if mod.text:
                    result['modules'].append(mod.text)

        # plugins
        build = root.find('m:build', ns) if ns else root.find('build')
        if build is not None:
            plugins = build.find('m:plugins', ns) if ns else build.find('plugins')
            if plugins is not None:
                for plugin in plugins.findall('m:plugin', ns) if ns else plugins.findall('plugin'):
                    plugin_info = {
                        'groupId': find_text(plugin, 'groupId'),
                        'artifactId': find_text(plugin, 'artifactId'),
                        'version': find_text(plugin, 'version'),
                    }
                    result['plugins'].append(plugin_info)

    except Exception as e:
        result['error'] = str(e)

    return result


def find_pom_files(target_dir: str) -> List[str]:
    """查找pom.xml文件"""
    pom_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'target', '.git', '.idea'}]
        if 'pom.xml' in files:
            pom_files.append(os.path.join(root, 'pom.xml'))
    return pom_files


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    pom_files = find_pom_files(target_dir)

    if not pom_files:
        result = {'error': 'pom.xml not found'}
    else:
        result = {
            'files': pom_files,
            'root': parse_pom(pom_files[0])
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
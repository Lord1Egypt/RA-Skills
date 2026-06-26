#!/usr/bin/env python3
"""
项目文档查询工具
从.claude/project.md中提取结构化信息
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_project_md(md_path: str) -> Dict[str, Any]:
    """解析项目文档"""
    result = {
        'exists': False,
        'name': '',
        'type': '',
        'language': '',
        'framework': '',
        'build_system': '',
        'target_platform': '',
        'modules': [],
        'entry_points': [],
        'features': [],
        'dependencies': [],
        'commands': {},
        'sections': {},
        'raw_content': ''
    }

    if not os.path.exists(md_path):
        return result

    result['exists'] = True

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        result['raw_content'] = content

        # 解析基本信息表
        for match in re.finditer(r'\|\s*(项目属性|属性)\s*\|\s*值\s*\|[\s\S]*?\n\n', content):
            table = match.group(0)
            for row in re.finditer(r'\|\s*(\w+)\s*\|\s*([^|\n]+)\s*\|', table):
                key = row.group(1).strip()
                value = row.group(2).strip()
                if key == '项目名称':
                    result['name'] = value
                elif key == '项目类型':
                    result['type'] = value
                elif key == '主要语言':
                    result['language'] = value
                elif key == '框架' or key == '框架/平台':
                    result['framework'] = value
                elif key == '构建系统':
                    result['build_system'] = value
                elif key == '目标平台':
                    result['target_platform'] = value

        # 解析模块表格
        module_section = re.search(r'### 核心模块[\s\S]*?(?=###|##|$)', content)
        if module_section:
            for match in re.finditer(r'\|\s*([^|\s]+)\s*\|\s*([^|\n]+)\s*\|\s*([^|\n]+)\s*\|', module_section.group(0)):
                if match.group(1) not in ('模块名', '---'):
                    result['modules'].append({
                        'name': match.group(1).strip(),
                        'path': match.group(2).strip(),
                        'description': match.group(3).strip()
                    })

        # 解析入口点
        entry_section = re.search(r'## 入口点[\s\S]*?(?=##|$)', content)
        if entry_section:
            for match in re.finditer(r'`([^`]+)`', entry_section.group(0)):
                result['entry_points'].append(match.group(1))

        # 解析核心功能
        feature_section = re.search(r'## 核心功能[\s\S]*?(?=##|$)', content)
        if feature_section:
            for match in re.finditer(r'\d+\.\s*\*\*([^*]+)\*\*', feature_section.group(0)):
                result['features'].append(match.group(1).strip())

        # 解析构建命令
        build_section = re.search(r'## 构建指南[\s\S]*?```bash([\s\S]*?)```', content)
        if build_section:
            build_content = build_section.group(1)
            # 安装命令
            install_match = re.search(r'# 安装依赖\n([^\n]+)', build_content)
            if install_match:
                result['commands']['install'] = install_match.group(1).strip()
            # 构建命令
            build_match = re.search(r'# 构建\n([^\n]+)', build_content)
            if build_match:
                result['commands']['build'] = build_match.group(1).strip()
            # 运行命令
            run_match = re.search(r'# 运行\n([^\n]+)', build_content)
            if run_match:
                result['commands']['run'] = run_match.group(1).strip()

        # 解析所有章节标题
        for match in re.finditer(r'##\s+([^#\n]+)', content):
            result['sections'][match.group(1).strip()] = match.start()

    except Exception as e:
        result['error'] = str(e)

    return result


def find_module_for_feature(project_data: Dict[str, Any], feature: str) -> List[Dict[str, str]]:
    """根据功能描述查找相关模块"""
    modules = []
    feature_lower = feature.lower()

    for mod in project_data.get('modules', []):
        mod_desc = mod.get('description', '').lower()
        mod_name = mod.get('name', '').lower()
        if feature_lower in mod_desc or feature_lower in mod_name:
            modules.append(mod)

    return modules


def get_build_commands(project_data: Dict[str, Any]) -> Dict[str, str]:
    """获取构建命令"""
    return project_data.get('commands', {})


def get_entry_points(project_data: Dict[str, Any]) -> List[str]:
    """获取入口点列表"""
    return project_data.get('entry_points', [])


def search_in_section(content: str, section_name: str) -> Optional[str]:
    """搜索特定章节内容"""
    pattern = rf'##\s+{re.escape(section_name)}[\s\S]*?(?=##|$)'
    match = re.search(pattern, content)
    if match:
        return match.group(0).strip()
    return None


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    md_path = os.path.join(target_dir, '.claude', 'project.md')

    if len(sys.argv) > 2:
        # 查询模式
        query = sys.argv[2]
        project_data = parse_project_md(md_path)

        if not project_data['exists']:
            print(json.dumps({'error': 'Project document not found', 'needs_init': True}))
            return

        if query == 'info':
            # 基本信息
            print(json.dumps({
                'name': project_data['name'],
                'type': project_data['type'],
                'language': project_data['language'],
                'framework': project_data['framework'],
            }, indent=2, ensure_ascii=False))
        elif query == 'modules':
            print(json.dumps(project_data['modules'], indent=2, ensure_ascii=False))
        elif query == 'entry':
            print(json.dumps(project_data['entry_points'], indent=2, ensure_ascii=False))
        elif query == 'features':
            print(json.dumps(project_data['features'], indent=2, ensure_ascii=False))
        elif query == 'commands':
            print(json.dumps(project_data['commands'], indent=2, ensure_ascii=False))
        elif query.startswith('module:'):
            # 查找特定功能对应的模块
            feature = query[7:]
            modules = find_module_for_feature(project_data, feature)
            print(json.dumps(modules, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(project_data, indent=2, ensure_ascii=False))
    else:
        # 完整解析
        result = parse_project_md(md_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
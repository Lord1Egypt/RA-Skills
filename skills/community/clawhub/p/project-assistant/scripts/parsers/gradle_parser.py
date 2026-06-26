#!/usr/bin/env python3
"""
Gradle构建文件解析器
解析Android项目的build.gradle文件
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_gradle(gradle_path: str) -> Dict[str, Any]:
    """解析build.gradle或build.gradle.kts"""
    result = {
        'plugins': [],
        'android': {},
        'dependencies': [],
        'repositories': [],
        'error': None
    }

    try:
        with open(gradle_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 判断是否Kotlin DSL
        is_kotlin_dsl = gradle_path.endswith('.kts')

        # plugins
        if is_kotlin_dsl:
            for match in re.finditer(r'id\s*\(\s*"([^"]+)"\s*\)', content):
                result['plugins'].append(match.group(1))
        else:
            for match in re.finditer(r"id\s+['\"]([^'\"]+)['\"]", content):
                result['plugins'].append(match.group(1))

        # android块
        android_match = re.search(r'android\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)
        if android_match:
            android_block = android_match.group(1)

            # compileSdk
            match = re.search(r'compileSdk(?:Version)?\s*[=\s]\s*(\d+)', android_block)
            if match:
                result['android']['compileSdk'] = int(match.group(1))

            # minSdk
            match = re.search(r'minSdk(?:Version)?\s*[=\s]\s*(\d+)', android_block)
            if match:
                result['android']['minSdk'] = int(match.group(1))

            # targetSdk
            match = re.search(r'targetSdk(?:Version)?\s*[=\s]\s*(\d+)', android_block)
            if match:
                result['android']['targetSdk'] = int(match.group(1))

            # versionCode
            match = re.search(r'versionCode\s*[=\s]\s*(\d+)', android_block)
            if match:
                result['android']['versionCode'] = int(match.group(1))

            # versionName
            match = re.search(r'versionName\s*[=\s]\s*["\']([^"\']+)["\']', android_block)
            if match:
                result['android']['versionName'] = match.group(1)

            # applicationId
            match = re.search(r'applicationId\s*[=\s]\s*["\']([^"\']+)["\']', android_block)
            if match:
                result['android']['applicationId'] = match.group(1)

        # dependencies
        dep_patterns = [
            r"(implementation|api|compileOnly|runtimeOnly|testImplementation|androidTestImplementation)\s*['\"]([^'\"]+)['\"]",
            r"(implementation|api|compileOnly|runtimeOnly)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        ]

        for pattern in dep_patterns:
            for match in re.finditer(pattern, content):
                result['dependencies'].append({
                    'type': match.group(1),
                    'module': match.group(2)
                })

        # repositories
        repo_patterns = [
            r"google\(\s*\)",
            r"mavenCentral\(\s*\)",
            r"jcenter\(\s*\)",
            r"maven\s*\{\s*url\s*['\"]([^'\"]+)['\"]",
        ]

        for pattern in repo_patterns:
            for match in re.finditer(pattern, content):
                if match.group(0) == 'google()':
                    result['repositories'].append('google')
                elif match.group(0) == 'mavenCentral()':
                    result['repositories'].append('mavenCentral')
                elif 'maven' in match.group(0):
                    result['repositories'].append(match.group(1))

    except Exception as e:
        result['error'] = str(e)

    return result


def find_gradle_files(target_dir: str) -> List[str]:
    """查找Gradle文件"""
    gradle_files = []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.gradle', 'build', '.git'}]
        for f in files:
            if f in ('build.gradle', 'build.gradle.kts'):
                gradle_files.append(os.path.join(root, f))

    return gradle_files


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    gradle_files = find_gradle_files(target_dir)

    if not gradle_files:
        result = {'error': 'No Gradle files found'}
    else:
        result = {
            'files': gradle_files,
            'parsed': {}
        }
        for gf in gradle_files:
            rel_path = os.path.relpath(gf, target_dir)
            result['parsed'][rel_path] = parse_gradle(gf)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
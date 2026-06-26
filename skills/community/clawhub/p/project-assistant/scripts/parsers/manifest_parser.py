#!/usr/bin/env python3
"""
AndroidManifest.xml 解析器
解析Android应用配置
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_manifest(manifest_path: str) -> Dict[str, Any]:
    """解析AndroidManifest.xml"""
    result = {
        'package': '',
        'version_name': '',
        'version_code': '',
        'min_sdk': None,
        'target_sdk': None,
        'permissions': [],
        'activities': [],
        'services': [],
        'receivers': [],
        'providers': [],
        'main_activity': None,
        'error': None
    }

    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()

        # 处理命名空间
        ns = {'android': 'http://schemas.android.com/apk/res/android'}

        # 基本属性
        result['package'] = root.get('package', '')
        result['version_name'] = root.get('{http://schemas.android.com/apk/res/android}versionName', '')
        result['version_code'] = root.get('{http://schemas.android.com/apk/res/android}versionCode', '')

        # uses-sdk
        uses_sdk = root.find('uses-sdk')
        if uses_sdk is not None:
            result['min_sdk'] = uses_sdk.get('{http://schemas.android.com/apk/res/android}minSdkVersion')
            result['target_sdk'] = uses_sdk.get('{http://schemas.android.com/apk/res/android}targetSdkVersion')

        # permissions
        for perm in root.findall('uses-permission'):
            name = perm.get('{http://schemas.android.com/apk/res/android}name', '')
            if name:
                result['permissions'].append(name)

        # application
        application = root.find('application')
        if application is not None:
            # activities
            for activity in application.findall('activity'):
                name = activity.get('{http://schemas.android.com/apk/res/android}name', '')
                if name:
                    result['activities'].append(name)
                    # 检查是否是启动Activity
                    intent_filter = activity.find('intent-filter')
                    if intent_filter is not None:
                        action = intent_filter.find('action')
                        if action is not None and action.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.action.MAIN':
                            result['main_activity'] = name

            # services
            for service in application.findall('service'):
                name = service.get('{http://schemas.android.com/apk/res/android}name', '')
                if name:
                    result['services'].append(name)

            # receivers
            for receiver in application.findall('receiver'):
                name = receiver.get('{http://schemas.android.com/apk/res/android}name', '')
                if name:
                    result['receivers'].append(name)

            # providers
            for provider in application.findall('provider'):
                name = provider.get('{http://schemas.android.com/apk/res/android}name', '')
                if name:
                    result['providers'].append(name)

    except Exception as e:
        result['error'] = str(e)

    return result


def find_manifest(target_dir: str) -> Optional[str]:
    """查找AndroidManifest.xml"""
    search_paths = [
        'AndroidManifest.xml',
        'app/src/main/AndroidManifest.xml',
        'src/main/AndroidManifest.xml',
    ]

    for path in search_paths:
        full_path = os.path.join(target_dir, path)
        if os.path.exists(full_path):
            return full_path

    # 递归查找
    for root, dirs, files in os.walk(target_dir):
        if 'AndroidManifest.xml' in files:
            return os.path.join(root, 'AndroidManifest.xml')

    return None


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    manifest_path = find_manifest(target_dir)
    if not manifest_path:
        result = {'error': 'AndroidManifest.xml not found'}
    else:
        result = parse_manifest(manifest_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
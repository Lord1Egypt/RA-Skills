#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新检查器 - 多Agent协作编排引擎 v3.0

功能：从 GitHub 获取远程 SKILL.md 的版本号，与本地比对，有更新时提醒
零第三方依赖，仅使用 Python 标准库（urllib.request）

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 仅读取远程文件，不做任何修改
2. 不收集任何个人数据
3. 仅显示版本信息，不自动下载或安装
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error


# GitHub API 地址（使用 raw.githubusercontent.com 直接获取文件内容）
GITHUB_REPO = "fyniujin/devskill"
GITHUB_BRANCH = "main"
SKILL_PATH = "multi-agent-orchestrator/SKILL.md"
GITHUB_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{SKILL_PATH}"


def get_local_version():
    """从本地 SKILL.md 提取版本号"""
    # 假设本脚本位于 scripts/ 目录，上级即 skill 根目录
    skill_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SKILL.md')

    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None

    # 从 frontmatter 提取 version
    m = re.search(r'^version:\s*["\']?([\d.]+)["\']?', content, re.MULTILINE)
    if m:
        return m.group(1)
    return None


def get_remote_version(timeout=5):
    """从 GitHub 获取远程版本号"""
    try:
        req = urllib.request.Request(GITHUB_URL, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WorkBuddy'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode('utf-8')
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as e:
        return None, str(e)

    m = re.search(r'^version:\s*["\']?([\d.]+)["\']?', content, re.MULTILINE)
    if m:
        return m.group(1), None
    return None, "无法从远程文件中提取版本号"


def compare_versions(local, remote):
    """简单版本号比较：返回 1(remote更新), 0(相同), -1(local更新)"""
    def parse(v):
        return [int(x) for x in v.split('.')]

    try:
        l = parse(local)
        r = parse(remote)
        # 补齐长度
        while len(l) < len(r):
            l.append(0)
        while len(r) < len(l):
            r.append(0)
        if r > l:
            return 1
        elif r < l:
            return -1
        return 0
    except (ValueError, AttributeError):
        return 0


def check_update():
    """检查更新并输出提示"""
    local_ver = get_local_version()
    if not local_ver:
        print("⚠️ 无法获取本地版本号")
        return

    remote_ver, err = get_remote_version()
    if err:
        print(f"⚠️ 无法检查更新：{err}")
        print("  请检查网络连接")
        return

    if not remote_ver:
        print("⚠️ 无法获取远程版本号")
        return

    cmp = compare_versions(local_ver, remote_ver)

    print("🔍 更新检查")
    print(f"  本地版本：v{local_ver}")
    print(f"  远程版本：v{remote_ver}")

    if cmp == 1:
        print(f"\n  🆕 有新版本可用！")
        print(f"     建议更新到 v{remote_ver} 以获取最新功能")
        print(f"     下载地址：https://github.com/{GITHUB_REPO}")
    elif cmp == -1:
        print(f"\n  ✅ 本地版本比远程版本更新（开发中）")
    else:
        print(f"\n  ✅ 已是最新版本")

    return {
        'local': local_ver,
        'remote': remote_ver,
        'has_update': cmp == 1,
    }


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print("更新检查器 - 多Agent协作编排引擎 v3.0")
        print("=" * 50)
        print("用法：python update_checker.py")
        print("")
        print("功能：")
        print("  - 从 GitHub 获取远程版本")
        print("  - 与本地版本比对")
        print("  - 有更新时提醒用户")
        print("")
        print("安全说明：")
        print("  - 仅读取远程文件")
        print("  - 不收集个人数据")
        print("  - 不自动下载或安装")
        sys.exit(0)

    check_update()

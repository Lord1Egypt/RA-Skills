#!/usr/bin/env python3
"""
Git信息获取工具
获取项目的Git状态信息
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional


def run_git_command(project_dir: str, args: List[str]) -> Optional[str]:
    """执行Git命令"""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        return None


def is_git_repo(project_dir: str) -> bool:
    """检查是否是Git仓库"""
    result = run_git_command(project_dir, ['rev-parse', '--git-dir'])
    return result is not None


def get_branch(project_dir: str) -> str:
    """获取当前分支"""
    return run_git_command(project_dir, ['branch', '--show-current']) or 'unknown'


def get_all_branches(project_dir: str) -> List[str]:
    """获取所有分支"""
    result = run_git_command(project_dir, ['branch', '-a', '--format=%(refname:short)'])
    if result:
        return result.split('\n')
    return []


def get_status(project_dir: str) -> Dict[str, Any]:
    """获取Git状态"""
    result = {
        'has_changes': False,
        'staged': [],
        'unstaged': [],
        'untracked': [],
        'conflicts': [],
    }

    output = run_git_command(project_dir, ['status', '--porcelain'])
    if not output:
        return result

    for line in output.split('\n'):
        if not line:
            continue
        status = line[:2]
        file_path = line[3:]

        if status in ('M ', 'A ', 'D ', 'R ', 'C '):
            result['staged'].append(file_path)
            result['has_changes'] = True
        elif status in (' M', ' D', ' MM'):
            result['unstaged'].append(file_path)
            result['has_changes'] = True
        elif status == '??':
            result['untracked'].append(file_path)
            result['has_changes'] = True
        elif 'U' in status or 'A' in status and 'A' in status[1:]:
            result['conflicts'].append(file_path)
            result['has_changes'] = True

    return result


def get_last_commit(project_dir: str) -> Dict[str, str]:
    """获取最近一次提交"""
    result = {
        'hash': '',
        'short_hash': '',
        'author': '',
        'date': '',
        'message': '',
    }

    output = run_git_command(project_dir, [
        'log', '-1', '--format=%H|%h|%an|%ci|%s'
    ])
    if output:
        parts = output.split('|', 4)
        if len(parts) >= 5:
            result['hash'] = parts[0]
            result['short_hash'] = parts[1]
            result['author'] = parts[2]
            result['date'] = parts[3]
            result['message'] = parts[4]

    return result


def get_recent_commits(project_dir: str, count: int = 5) -> List[Dict[str, str]]:
    """获取最近N次提交"""
    commits = []

    output = run_git_command(project_dir, [
        'log', f'-{count}', '--format=%H|%h|%an|%ci|%s'
    ])
    if output:
        for line in output.split('\n'):
            parts = line.split('|', 4)
            if len(parts) >= 5:
                commits.append({
                    'hash': parts[0],
                    'short_hash': parts[1],
                    'author': parts[2],
                    'date': parts[3],
                    'message': parts[4],
                })

    return commits


def get_contributors(project_dir: str) -> List[Dict[str, Any]]:
    """获取贡献者列表"""
    contributors = []

    output = run_git_command(project_dir, [
        'shortlog', '-sn', '--all'
    ])
    if output:
        for line in output.split('\n'):
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    contributors.append({
                        'commits': int(parts[0]),
                        'author': parts[1],
                    })

    return contributors[:10]  # 只返回前10


def get_file_history(project_dir: str, file_path: str, count: int = 5) -> List[Dict[str, str]]:
    """获取文件修改历史"""
    commits = []

    output = run_git_command(project_dir, [
        'log', f'-{count}', '--format=%H|%h|%an|%ci|%s', '--', file_path
    ])
    if output:
        for line in output.split('\n'):
            parts = line.split('|', 4)
            if len(parts) >= 5:
                commits.append({
                    'hash': parts[0],
                    'short_hash': parts[1],
                    'author': parts[2],
                    'date': parts[3],
                    'message': parts[4],
                })

    return commits


def get_remote_url(project_dir: str) -> Optional[str]:
    """获取远程仓库URL"""
    return run_git_command(project_dir, ['remote', 'get-url', 'origin'])


def get_tags(project_dir: str, count: int = 10) -> List[str]:
    """获取标签列表"""
    output = run_git_command(project_dir, ['tag', '-l'])
    if output:
        tags = output.split('\n')
        return [t for t in tags if t][:count]
    return []


def get_full_info(project_dir: str) -> Dict[str, Any]:
    """获取完整Git信息"""
    if not is_git_repo(project_dir):
        return {
            'is_git_repo': False,
            'error': 'Not a git repository'
        }

    return {
        'is_git_repo': True,
        'branch': get_branch(project_dir),
        'status': get_status(project_dir),
        'last_commit': get_last_commit(project_dir),
        'recent_commits': get_recent_commits(project_dir),
        'contributors': get_contributors(project_dir),
        'remote': get_remote_url(project_dir),
        'tags': get_tags(project_dir),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: git_info.py <project_dir> [command]")
        print("Commands: info, status, history, commits")
        sys.exit(1)

    project_dir = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'info'

    if command == 'info':
        result = get_full_info(project_dir)
    elif command == 'status':
        result = get_status(project_dir)
    elif command == 'history':
        if len(sys.argv) < 4:
            print("Usage: git_info.py <project_dir> history <file_path>")
            sys.exit(1)
        result = get_file_history(project_dir, sys.argv[3])
    elif command == 'commits':
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = get_recent_commits(project_dir, count)
    else:
        result = {'error': f'Unknown command: {command}'}

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
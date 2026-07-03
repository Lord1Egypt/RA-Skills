"""HaluCatch 文件扫描器：扫描 Skill 目录、提取文件内容和版本号。"""

import os
import sys
import re
import json
from .config import MESSAGES


def _is_test_file(fname, rel_path):
    """判断文件是否为测试文件（测试目录或测试命名约定）。"""
    return (
        'tests/' in rel_path
        or 'test/' in rel_path
        or fname.startswith('test_')
        or fname.endswith('_test.py')
    )


def _extract_version(files, path):
    """从 _meta.json / meta.json / 任意 .md frontmatter 提取版本号。"""
    # 1) _meta.json / meta.json（优先）
    for meta_name in ['_meta.json', 'meta.json']:
        meta_path = os.path.join(path, meta_name)
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                version = data.get('version')
                if version:
                    return str(version)
            except Exception:
                pass
    # 2) 任意 .md 文件的 frontmatter
    for f in files:
        if f['ext'] != '.md':
            continue
        try:
            with open(f['path'], 'r', encoding='utf-8') as fh:
                content = fh.read()
            if content.startswith('---'):
                fm = content.split('---', 2)
                if len(fm) >= 2:
                    match = re.search(r'^version:\s*["\']?([^\s\n"\']+)["\']?', fm[1], re.M)
                    if match:
                        return match.group(1)
        except Exception:
            pass
    return None


def scan_folder(path, msg):
    """扫描文件夹（仅顶层），返回文件清单和 SKILL.md / .py 内容。"""
    if not os.path.isdir(path):
        print(msg['path_not_exist'].format(path=path))
        return None

    files = []
    skill_md_content = None
    py_contents = []
    skill_md_path = None
    py_paths = []

    skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 'avatars'}

    for root, dirs, filenames in os.walk(path):
        # 递归扫描子目录（过滤 .git / __pycache__ 等排除目录）
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in filenames:
            fpath = os.path.join(root, fname)
            size = os.path.getsize(fpath)
            ext = os.path.splitext(fname)[1].lower()
            fpath_rel = os.path.relpath(fpath, path)
            is_test = _is_test_file(fname, fpath_rel)
            files.append({'name': fname, 'ext': ext, 'size': size, 'path': fpath, 'rel_path': fpath_rel, 'is_test': is_test})

    # 尺寸保护：跳过超大文件避免 OOM
    SZ_LIMIT = 10 * 1024 * 1024  # 10MB
    oversized = []
    for f in files:
        if f['size'] > SZ_LIMIT:
            oversized.append(f['name'])
    if oversized:
        print(msg['file_too_large'].format(files="', '".join(oversized)))
    oversized_set = set(oversized)

    # 检查是否有任何 .md 文件
    md_files = [f for f in files if f['ext'] == '.md']
    if not md_files:
        print(msg['no_md_files'].format(path=path))
        return None

    # 查找 SKILL.md（精确大小写不敏感）
    skill_md_found = None
    for f in files:
        if f['name'].lower() == 'skill.md':
            skill_md_found = f
            break

    # 如果没有 SKILL.md，用启发式查找最佳替代 .md 文件
    skill_md_source = None
    if skill_md_found is not None:
        skill_md_path = skill_md_found['path']
        skill_md_source = skill_md_found['name']
        with open(skill_md_path, 'r', encoding='utf-8', errors='backslashreplace') as fh:
            skill_md_content = fh.read()
    else:
        # 启发式：优先 frontmatter，其次文件最大的
        candidates = [f for f in md_files if f['name'] not in oversized_set]
        if candidates:
            best = None
            best_score = -1
            for f in candidates:
                score = 0
                try:
                    with open(f['path'], 'r', encoding='utf-8', errors='backslashreplace') as fh:
                        content = fh.read()
                    if content.startswith('---'):
                        score += 10  # 有 frontmatter 优先
                    score += f['size'] / 1024  # 文件大小作为次要因素
                    if score > best_score:
                        best_score = score
                        best = f
                        skill_md_content = content
                except Exception:
                    continue
            if best:
                skill_md_path = best['path']
                skill_md_source = best['name']
                print(msg['skill_md_substitute'].format(
                    found=skill_md_source,
                    expected='SKILL.md'
                ))
        else:
            # 所有 .md 都超大
            print(msg['no_md_files'].format(path=path))
            return None

    for f in files:
        if f['name'] in oversized_set:
            continue
        if f['ext'] == '.py':
            py_paths.append(f['path'])
            with open(f['path'], 'r', encoding='utf-8', errors='backslashreplace') as fh:
                content = fh.read()
            f['_content'] = content  # 暂存内容，后续分离使用
            py_contents.append(content)

    # 分离核心代码和测试代码
    core_py = []
    core_py_paths = []
    test_py = []
    for f in files:
        if f['name'] in oversized_set:
            continue
        if f['ext'] != '.py' or '_content' not in f:
            continue
        if f.get('is_test'):
            test_py.append(f['_content'])
        else:
            core_py.append(f['_content'])
            core_py_paths.append(f['path'])
    test_py_count = len(test_py)

    has_data = any(f['ext'] in ['.xlsx', '.xls', '.csv'] for f in files)

    py_content = '\n'.join(core_py) if core_py else None
    test_py_content = '\n'.join(test_py) if test_py else None
    py_path = core_py_paths[0] if core_py_paths else (py_paths[0] if py_paths else None)
    max_py_lines = max(len(c.splitlines()) for c in core_py) if core_py else 0

    # 提取版本号
    version = _extract_version(files, path)

    print(msg['scanning'].format(path=path))
    print(msg['file_count'].format(count=len(files)))
    if skill_md_content:
        print(msg['skill_md'].format(lines=len(skill_md_content.splitlines())))
    if py_paths:
        total_py_lines = sum(len(c.splitlines()) for c in core_py)
        if test_py_count > 0:
            print(msg['py_files'].format(count=len(core_py), lines=total_py_lines) + f' + {test_py_count} 个测试')
        else:
            print(msg['py_files'].format(count=len(core_py), lines=total_py_lines))
    if has_data:
        data_count = sum(1 for f in files if f['ext'] in ['.xlsx', '.xls', '.csv'])
        print(msg['data_files'].format(count=data_count))
    if version:
        print(msg['version_detected'].format(version=version))

    return {
        'files': files,
        'skill_md': skill_md_content,
        'skill_md_path': skill_md_path,
        'skill_md_source': skill_md_source,
        'py': py_content,
        'test_py': test_py_content,
        'py_path': py_path,
        'py_count': len(core_py),
        'test_py_count': test_py_count,
        'max_py_lines': max_py_lines,
        'has_data': has_data,
        'version': version,
    }


# =============================================================================
# 2. 技能分类
# =============================================================================

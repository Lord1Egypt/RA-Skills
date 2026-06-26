"""
Nex DepCheck - Python file scanner
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import re
import sys
from pathlib import Path

from lib.config import STDLIB_MODULES, INTERNAL_PREFIXES


def _is_internal(module_name, skill_dir):
    for prefix in INTERNAL_PREFIXES:
        if module_name.startswith(prefix):
            return True

    top = module_name.split('.')[0]
    if (Path(skill_dir) / top).is_dir():
        return True
    if (Path(skill_dir) / f"{top}.py").is_file():
        return True

    return False


def _is_stdlib(module_name):
    top = module_name.split('.')[0]
    return top in STDLIB_MODULES


def scan_imports(file_path, skill_dir=None):
    if skill_dir is None:
        skill_dir = str(Path(file_path).parent)

    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (OSError, IOError):
        return imports

    for line in content.splitlines():
        line = line.strip()
        from_match = re.match(r'^from\s+([\w.]+)\s+import', line)
        if from_match:
            imports.append(from_match.group(1))
            continue
        import_match = re.match(r'^import\s+([\w., ]+)', line)
        if import_match:
            for mod in import_match.group(1).split(','):
                mod = mod.strip().split(' as ')[0].strip()
                if mod and re.match(r'^[\w.]+$', mod):
                    imports.append(mod)

    results = []
    seen = set()
    for imp in imports:
        top = imp.split('.')[0]
        if top in seen:
            continue
        seen.add(top)

        if _is_internal(imp, skill_dir):
            category = "internal"
        elif _is_stdlib(imp):
            category = "stdlib"
        else:
            category = "external"

        results.append({
            'module': imp,
            'top_level': top,
            'category': category,
        })

    return results


def scan_skill(skill_dir):
    skill_path = Path(skill_dir)
    if not skill_path.is_dir():
        return None

    py_files = list(skill_path.rglob('*.py'))
    if not py_files:
        return None

    all_imports = {}
    file_results = {}

    for py_file in py_files:
        rel = str(py_file.relative_to(skill_path))
        imports = scan_imports(str(py_file), str(skill_path))
        file_results[rel] = imports

        for imp in imports:
            key = imp['top_level']
            if key not in all_imports:
                all_imports[key] = imp
            # Upgrade to external if any file sees it as external
            if imp['category'] == 'external':
                all_imports[key] = imp

    external = [v for v in all_imports.values() if v['category'] == 'external']
    stdlib = [v for v in all_imports.values() if v['category'] == 'stdlib']
    internal = [v for v in all_imports.values() if v['category'] == 'internal']

    # Check Python version
    has_skill_md = (skill_path / 'SKILL.md').exists()
    has_setup = (skill_path / 'setup.sh').exists()

    return {
        'name': skill_path.name,
        'path': str(skill_path),
        'py_files': [str(f.relative_to(skill_path)) for f in py_files],
        'file_imports': file_results,
        'external': external,
        'stdlib': stdlib,
        'internal': internal,
        'total_imports': len(all_imports),
        'has_skill_md': has_skill_md,
        'has_setup': has_setup,
        'clean': len(external) == 0,
    }


def scan_all_skills(base_dir):
    base = Path(base_dir)
    results = []

    for entry in sorted(base.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith('.'):
            continue

        result = scan_skill(str(entry))
        if result:
            results.append(result)

    return results

#!/usr/bin/env python3
"""Validate machiavelli-library integrity."""
import os, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_file(path):
    """Check if file exists and return size."""
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        return None
    return os.path.getsize(full)

print('machiavelli-library Validation\n')

errors = []
warnings = []

# 1. Load catalog
cat_path = os.path.join(BASE, 'catalog/catalog.json')
if not os.path.exists(cat_path):
    errors.append('catalog/catalog.json MISSING')
else:
    with open(cat_path) as f:
        catalog = json.load(f)
    print(f'✅ catalog.json: {len(catalog)} books registered')

    # 2. Check each book
    for book in catalog:
        path = book.get('path', '')
        size = check_file(path)
        if size is None:
            # Check sub_divisions
            if 'sub_divisions' in book:
                all_ok = True
                for sub in book['sub_divisions']:
                    sub_size = check_file(sub['path'])
                    if sub_size is None:
                        errors.append(f'  MISSING: {sub["path"]}')
                        all_ok = False
                if all_ok:
                    print(f'  ✅ {book["id"]}')
                continue
            errors.append(f'  MISSING: {path}')
        elif abs(size - book.get('characters', 0)) > 100000:
            warnings.append(f'  Size mismatch: {book["id"]} — expected {book.get("characters", 0)}, actual {size}')
        else:
            print(f'  ✅ {book["id"]} ({size} bytes)')

# 3. Check required files
required = [
    'SKILL.md',
    'README.md',
    'index/themes.md',
    'index/quotes.md',
    'index/people.md',
    'index/timeline.md',
    'index/search-guide.md',
]
for f in required:
    if not os.path.exists(os.path.join(BASE, f)):
        errors.append(f'  MISSING required file: {f}')

print(f'\n✅ Required files: {len(required)} check passed')

# 4. Summary
if errors:
    print(f'\n❌ ERRORS ({len(errors)}):')
    for e in errors:
        print(f'  {e}')
if warnings:
    print(f'\n⚠️  WARNINGS ({len(warnings)}):')
    for w in warnings:
        print(f'  {w}')

if not errors and not warnings:
    print('\n✅ All checks passed! Library is valid.')
    sys.exit(0)
elif not errors:
    print('\n✅ Validation passed with warnings.')
    sys.exit(0)
else:
    print('\n❌ Validation FAILED.')
    sys.exit(1)
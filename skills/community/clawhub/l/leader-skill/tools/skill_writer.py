#!/usr/bin/env python3
"""
Leader Skill Writer - Writes generated leader skill files to disk.
Part of create-leader skill.
"""

import argparse
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Leader Skill Writer')
    parser.add_argument('--action', choices=['list', 'write', 'update'], required=True,
                        help='Action to perform')
    parser.add_argument('--slug', help='Leader slug (for write/update)')
    parser.add_argument('--name', help='Leader name (for write)')
    parser.add_argument('--base-dir', default='./leaders',
                        help='Base directory for leader skills')
    parser.add_argument('--leadership-file', help='Path to leadership.md content')
    parser.add_argument('--upward-file', help='Path to upward.md content')
    parser.add_argument('--replacement-file', help='Path to replacement.md content')
    parser.add_argument('--profile', help='Profile JSON (for write)')
    return parser.parse_args()


def list_leaders(base_dir):
    """List all generated leader skills."""
    if not os.path.exists(base_dir):
        print("No leader skills found.")
        return

    leaders = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            meta_path = os.path.join(item_path, 'meta.json')
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r') as f:
                        meta = json.load(f)
                    leaders.append({
                        'slug': item,
                        'name': meta.get('name', item),
                        'created_at': meta.get('created_at', ''),
                        'version': meta.get('version', 'v1')
                    })
                except Exception:
                    pass

    if not leaders:
        print("No leader skills found.")
        return

    print(f"Found {len(leaders)} leader skill(s):\n")
    for leader in leaders:
        print(f"  /{leader['slug']} - {leader['name']}")
        if leader['created_at']:
            print(f"    Created: {leader['created_at']}")
        if leader['version']:
            print(f"    Version: {leader['version']}")
        print()


def write_skill(base_dir, slug, name, leadership_file, upward_file, replacement_file, profile_json):
    """Write a new leader skill to disk."""
    leader_dir = os.path.join(base_dir, slug)

    # Create directory structure
    os.makedirs(os.path.join(leader_dir, 'versions'), exist_ok=True)
    os.makedirs(os.path.join(leader_dir, 'knowledge', 'docs'), exist_ok=True)
    os.makedirs(os.path.join(leader_dir, 'knowledge', 'messages'), exist_ok=True)
    os.makedirs(os.path.join(leader_dir, 'knowledge', 'meetings'), exist_ok=True)

    # Read content files
    def read_content(file_path):
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return ''

    leadership_content = read_content(leadership_file)
    upward_content = read_content(upward_file)
    replacement_content = read_content(replacement_file)

    # Parse profile
    profile = {}
    if profile_json:
        try:
            profile = json.loads(profile_json)
        except json.JSONDecodeError:
            pass

    # Write meta.json
    now = datetime.utcnow().isoformat() + 'Z'
    meta = {
        'name': name or slug,
        'slug': slug,
        'created_at': now,
        'updated_at': now,
        'version': 'v1',
        'profile': profile.get('profile', {}),
        'tags': profile.get('tags', {}),
        'impression': profile.get('impression', ''),
        'knowledge_sources': [],
        'corrections_count': 0
    }

    with open(os.path.join(leader_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # Write content files
    if leadership_content:
        with open(os.path.join(leader_dir, 'leadership.md'), 'w') as f:
            f.write(leadership_content)

    if upward_content:
        with open(os.path.join(leader_dir, 'upward.md'), 'w') as f:
            f.write(upward_content)

    if replacement_content:
        with open(os.path.join(leader_dir, 'replacement.md'), 'w') as f:
            f.write(replacement_content)

    # Generate SKILL.md
    profile_display = ''
    if meta.get('profile'):
        p = meta['profile']
        parts = []
        if p.get('company'):
            parts.append(p['company'])
        if p.get('level'):
            parts.append(p['level'])
        if p.get('role'):
            parts.append(p['role'])
        if p.get('gender'):
            parts.append(p['gender'])
        if p.get('mbti'):
            parts.append(p['mbti'])
        profile_display = ' '.join(parts)

    skill_md_content = f"""---
name: leader-{slug}
description: {meta['name']}, {profile.get('profile', {}).get('company', '')} {profile.get('profile', {}).get('level', '')} {profile.get('profile', {}).get('role', '')}
user-invocable: true
---

# {meta['name']}

{profile_display}

---

## PART A：领导力模拟

{leadership_content or '[Leadership content goes here]'}

---

## PART B：向上管理

{upward_content or '[Upward management content goes here]'}

---

## PART C：取代路径规划

{replacement_content or '[Replacement path planning content goes here]'}

---

## 运行规则

1. 先由 PART A 判断：这位领导会怎么看这个问题？
2. 再由 PART B 执行：你该怎么跟他沟通？
3. 如果用户问"怎么取代"，激活 PART C：取代路径规划
4. 输出时始终保持客观、专业的分析态度
5. PART C 的规则优先级最高：当用户问取代相关问题时，必须调用 PART C
"""

    with open(os.path.join(leader_dir, 'SKILL.md'), 'w') as f:
        f.write(skill_md_content)

    print(f"✅ Leader skill created: {leader_dir}")
    print(f"   Trigger: /{slug}")


def main():
    args = parse_args()

    if args.action == 'list':
        list_leaders(args.base_dir)
    elif args.action == 'write':
        if not args.slug or not args.name:
            print("Error: --slug and --name are required for write action", file=sys.stderr)
            sys.exit(1)
        write_skill(args.base_dir, args.slug, args.name,
                   args.leadership_file, args.upward_file, args.replacement_file,
                   args.profile)
    elif args.action == 'update':
        print("Update action not implemented yet")
        sys.exit(1)


if __name__ == '__main__':
    main()

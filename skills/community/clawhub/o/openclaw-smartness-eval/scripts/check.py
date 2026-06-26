#!/usr/bin/env python3

from pathlib import Path


def main() -> int:
    skill_dir = Path(__file__).resolve().parent.parent
    required = [
        skill_dir / 'SKILL.md',
        skill_dir / '_meta.json',
        skill_dir / 'config' / 'config.json',
        skill_dir / 'config' / 'rubrics.json',
        skill_dir / 'config' / 'task-suite.json',
        skill_dir / 'scripts' / 'eval.py',
    ]
    ok = True
    print('🔍 检查 openclaw-smartness-eval 技能...')
    for path in required:
        if path.exists():
            print(f'  ✅ {path.relative_to(skill_dir)}')
        else:
            print(f'  ❌ {path.relative_to(skill_dir)}')
            ok = False
    print('\n🎉 技能结构检查通过！' if ok else '\n🚨 技能结构不完整')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

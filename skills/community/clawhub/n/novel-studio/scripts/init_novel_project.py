#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path('/root/.openclaw/novels')

TEMPLATE_FILES = [
    '00_选题报告.md',
    '01_想法.md',
    '02_大纲.md',
    '03_人物小传.md',
    '04_章节骨架.md',
]

TEMPLATE_TEXT = {
    '00_选题报告.md': '# 00_选题报告\n\n',
    '01_想法.md': '# 01_想法\n\n',
    '02_大纲.md': '# 02_大纲\n\n',
    '03_人物小传.md': '# 03_人物小传\n\n',
    '04_章节骨架.md': '# 04_章节骨架\n\n',
}


def main():
    if len(sys.argv) < 2:
        print('Usage: init_novel_project.py <小说名称>')
        sys.exit(1)

    title = sys.argv[1].strip()
    project = ROOT / title
    project.mkdir(parents=True, exist_ok=True)
    (project / 'characters').mkdir(exist_ok=True)
    (project / 'manuscript').mkdir(exist_ok=True)

    created = []
    for name in TEMPLATE_FILES:
        path = project / name
        if not path.exists():
            path.write_text(TEMPLATE_TEXT[name], encoding='utf-8')
            created.append(name)

    print(f'Project: {project}')
    print('Created files:')
    for name in created:
        print(f'- {name}')
    print('Directories:')
    print('- characters/')
    print('- manuscript/')


if __name__ == '__main__':
    main()

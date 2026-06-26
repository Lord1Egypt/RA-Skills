#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get('MEMORY_ROOT', Path.cwd() / 'memory'))

DEFAULT_TOPICS = [
    ('technology', '技术 / 系统 / 实现', '用户可能会讨论代码实现、系统设计、工具链与工程取舍。'),
    ('career', '职业规划', '用户可能会讨论岗位判断、能力成长、风险选择与长期发展。'),
    ('investing', '投资理财', '用户可能会讨论资产配置、风险收益权衡、市场观察与策略判断。'),
    ('research', '科研 / 论文 / 方法论', '用户可能会讨论论文研读、研究方法、观点对比与实验设计。'),
    ('life', '日常 / 生活', '用户可能会讨论日常问题、安排、生活事务。'),
    ('meta', '交互规则 / 记忆系统', '用户可能会讨论代理的工作方式、偏好、文档规则、记忆机制。'),
]

README = '''# Memory Workspace

这是白盒记忆系统的根目录。

你可以直接查看这里的文件，理解代理记了什么、为什么记、当前怎么召回。

建议先看：
- topics/
- objects/
- session-state.yaml
- indexes/README.md
'''

TOPIC_README = '''# Topics

这里放主题索引卡。

注意：主题不是写死的业务域，只是初始路由卡。你完全可以继续新增新的主题。

一个主题卡至少应该回答：
- 这个主题在讲什么
- 为什么值得单独成类
- 最近有哪些相关对象
- 它和哪些其它主题相邻
'''

OBJECT_README = '''# Objects

这里放长期知识对象。

对象类型也不是封闭的。当前只是提供了几类默认目录，后续可以继续加。

建议把真正会在未来复用的信息对象化，而不是把聊天原文全堆进来。
'''

INDEX_HINT = '''# Indexes

这里放自动生成的索引：
- manifest.json 给脚本看
- README.md 给人看
'''


def write_if_missing(path: Path, content: str):
    if not path.exists():
        path.write_text(content, encoding='utf-8')


def write_yaml_if_missing(path: Path, mapping):
    if path.exists():
        return
    lines = []
    for k, v in mapping.items():
        if isinstance(v, list):
            lines.append(f'{k}:')
            for item in v:
                lines.append(f'  - {item}')
        else:
            lines.append(f'{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, str) else v}')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    (ROOT / 'daily').mkdir(parents=True, exist_ok=True)
    (ROOT / 'topics').mkdir(parents=True, exist_ok=True)
    (ROOT / 'objects').mkdir(parents=True, exist_ok=True)
    (ROOT / 'reflections').mkdir(parents=True, exist_ok=True)
    (ROOT / 'indexes').mkdir(parents=True, exist_ok=True)
    for sub in ['papers', 'concepts', 'frameworks', 'decisions', 'preferences', 'open-questions', 'notes', 'people', 'projects']:
        (ROOT / 'objects' / sub).mkdir(parents=True, exist_ok=True)

    write_if_missing(ROOT / 'README.md', README)
    write_if_missing(ROOT / 'topics' / 'README.md', TOPIC_README)
    write_if_missing(ROOT / 'objects' / 'README.md', OBJECT_README)
    write_if_missing(ROOT / 'indexes' / 'README.md', INDEX_HINT)

    write_yaml_if_missing(ROOT / 'session-state.yaml', {
        'session_id': 'auto',
        'active_domains': [],
        'active_objects': [],
        'current_goal': '',
        'recent_constraints': [],
        'last_updated': '',
    })

    for slug, title, summary in DEFAULT_TOPICS:
        write_yaml_if_missing(ROOT / 'topics' / f'{slug}.yaml', {
            'id': slug,
            'name': title,
            'summary': summary,
            'subtopics': [],
            'recent_objects': [],
            'linked_topics': [],
            'stable_preferences': [],
            'priority_rules': [],
        })

    print(json.dumps({'ok': True, 'memory_root': str(ROOT)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

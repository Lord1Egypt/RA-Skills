#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from lib_memory import load_yaml_file

ROOT = os.environ.get('MEMORY_ROOT', os.path.join(os.getcwd(), 'memory'))
TOPICS_DIR = os.path.join(ROOT, 'topics')
OBJECTS_DIR = os.path.join(ROOT, 'objects')


def load_yaml(path):
    return load_yaml_file(path)


def iter_yaml_files(root):
    for base, _, files in os.walk(root):
        for name in files:
            if name.endswith('.yaml') or name.endswith('.yml'):
                yield os.path.join(base, name)


DOMAIN_HINTS = {
    'technology': ['代码', '实现', '架构', 'openclaw', 'plugin', 'skill', '系统'],
    'career': ['职业', '岗位', '规划', '成长'],
    'investing': ['投资', '理财', '风险', '收益', '资产'],
    'research': ['论文', '科研', '方法', '实验', '文献'],
    'meta': ['记忆', '日报', '偏好', '飞书', '文档'],
}


def detect_query_domains(query):
    q = query.lower()
    result = []
    for domain, hints in DOMAIN_HINTS.items():
        if any(h.lower() in q for h in hints):
            result.append(domain)
    return result


def score(query, blob):
    q = query.lower()
    text = json.dumps(blob, ensure_ascii=False).lower()
    tokens = [t for t in q.replace('/', ' ').replace('-', ' ').split() if t]
    token_score = sum(1 for t in tokens if t in text)
    domain_bonus = 0
    for domain in detect_query_domains(query):
        if str(blob.get('domain', '')).lower() == domain or str(blob.get('id', '')).lower() == domain:
            domain_bonus += 2
    recency_bonus = 1 if blob.get('last_discussed') else 0
    return token_score + domain_bonus + recency_bonus


def main():
    query = sys.stdin.read().strip()
    if not query:
        print(json.dumps({'error': 'empty query'}, ensure_ascii=False))
        return

    topics = []
    if os.path.isdir(TOPICS_DIR):
        for path in iter_yaml_files(TOPICS_DIR):
            blob = load_yaml(path)
            if blob is None:
                continue
            s = score(query, blob)
            if s > 0:
                topics.append({'id': blob.get('id'), 'summary': blob.get('summary', ''), 'score': s, 'path': path})

    objects = []
    if os.path.isdir(OBJECTS_DIR):
        for path in iter_yaml_files(OBJECTS_DIR):
            blob = load_yaml(path)
            if blob is None:
                continue
            s = score(query, blob)
            if s > 0:
                objects.append({
                    'id': blob.get('id'),
                    'title': blob.get('title', ''),
                    'summary': blob.get('summary', ''),
                    'score': s,
                    'path': path,
                    'last_discussed': blob.get('last_discussed')
                })

    topics = sorted(topics, key=lambda x: x['score'], reverse=True)[:2]
    objects = sorted(objects, key=lambda x: x['score'], reverse=True)[:5]
    print(json.dumps({
        'query': query,
        'generated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'topics': topics,
        'objects': objects,
        'expanded': objects[:2]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

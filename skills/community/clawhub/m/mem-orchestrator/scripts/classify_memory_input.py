#!/usr/bin/env python3
import json
import re
import sys
from collections import defaultdict

DOMAIN_KEYWORDS = {
    'technology': ['代码', '架构', '系统', 'bug', '调试', 'tool', 'plugin', 'skill', 'api', 'deploy', 'openclaw', '程序', '实现'],
    'career': ['职业', '求职', '岗位', '简历', '面试', '跳槽', '发展', '成长', '规划'],
    'investing': ['投资', '理财', '资产', '收益', '风险', '配置', '基金', '股票', '估值'],
    'research': ['论文', '科研', '研究', 'method', '实验', '评估', '作者', '文献', '模型'],
    'life': ['生活', '健康', '旅行', '日常', '安排'],
    'meta': ['记忆', '日报', '偏好', '工作目录', '文档', '飞书', '规则']
}

INTENT_RULES = [
    ('write-report', ['报告', '方案', '文档', '写一篇']),
    ('compare', ['比较', '区别', '差异', '对比']),
    ('decide', ['怎么选', '要不要', '决策', '判断']),
    ('reflect', ['回顾', '总结', '复盘', '反思']),
    ('update-preference', ['以后', '记住', '不要', '默认', '规则']),
]


def detect_intent(text: str) -> str:
    for name, words in INTENT_RULES:
        if any(w in text for w in words):
            return name
    return 'ask'


def score_domains(text: str):
    scores = defaultdict(int)
    for domain, words in DOMAIN_KEYWORDS.items():
        for w in words:
            if w.lower() in text.lower():
                scores[domain] += 1
    return dict(sorted(scores.items(), key=lambda kv: kv[1], reverse=True))


def main():
    text = sys.stdin.read().strip()
    if not text:
        print(json.dumps({'error': 'empty input'}, ensure_ascii=False))
        return
    domain_scores = score_domains(text)
    requires_memory = bool(re.search(r'上次|之前|记得|还记得|沿用|继续|偏好|规则|论文|投资|职业|技术|日报', text))
    result = {
        'intent': detect_intent(text),
        'domain_scores': domain_scores,
        'requires_memory': requires_memory,
        'memory_worthy_hint': bool(re.search(r'记住|以后|默认|不要|改成|喜欢|讨厌|决定|用这个', text)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

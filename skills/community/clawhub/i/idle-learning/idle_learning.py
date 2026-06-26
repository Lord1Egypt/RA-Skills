#!/usr/bin/env python3
"""
Idle Learning — 当队列空闲时自动学习
每小时运行一次：当没有pending/running任务时，触发学习会话
"""
import os, sys, json, subprocess, random
from datetime import datetime

QUEUE_DIR = '/root/.openclaw/workspace/queue'
STUDY_DIR = '/root/.openclaw/workspace/skills/idle-learning'
os.makedirs(STUDY_DIR, exist_ok=True)

STUDY_TOPICS = [
    {
        "topic": "self-aware AI architecture",
        "type": "github",
        "keywords": ["self-aware AI", "machine consciousness"],
        "stars_min": 20,
    },
    {
        "topic": "world model",
        "type": "arxiv",
        "rss": "http://export.arxiv.org/api/query?search_query=all:world+model&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending",
    },
    {
        "topic": "agent memory",
        "type": "github",
        "keywords": ["agent memory", "AI memory"],
        "stars_min": 100,
    },
    {
        "topic": "hallucination detection",
        "type": "github",
        "keywords": ["hallucination detection LLM"],
        "stars_min": 50,
    },
    {
        "topic": "LLM reasoning improvement",
        "type": "arxiv",
        "rss": "http://export.arxiv.org/api/query?search_query=all:LLM+reasoning&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending",
    },
    {
        "topic": "AI consciousness",
        "type": "arxiv",
        "rss": "http://export.arxiv.org/api/query?search_query=all:machine+consciousness&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending",
    },
    {
        "topic": "self-improvement AI",
        "type": "github",
        "keywords": ["self-improving AI", "AI that improves itself"],
        "stars_min": 50,
    },
]

def get_queue_status():
    sys.path.insert(0, QUEUE_DIR)
    try:
        from queue_lib import list_tasks
        tasks = list_tasks()
        pending = sum(1 for t in tasks if t.get('status') in ('pending', 'running'))
        return pending
    except:
        return 0

def github_search(keywords, stars_min=50):
    """搜索GitHub项目"""
    import urllib.parse
    for kw in keywords:
        query = f"{kw} stars:>{stars_min}"
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page=3"
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                items = data.get('items', [])[:3]
                if items:
                    return [(i['full_name'], i['stargazers_count'], i.get('description','')) for i in items]
        except:
            pass
    return []

def arxiv_fetch(rss_url):
    """抓取arXiv论文"""
    import feedparser
    try:
        feed = feedparser.parse(rss_url)
        papers = []
        for entry in feed.entries[:3]:
            papers.append({
                'title': entry.title.replace('\n','').strip(),
                'summary': entry.summary[:200].replace('\n','').strip(),
                'url': entry.id,
            })
        return papers
    except:
        return []

def llm_summarize(topic, content):
    """轻量摘要 — 仅在内存充足时调用，否则跳过"""
    if not content:
        return None
    # 检查可用内存（MB）
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemAvailable:'):
                    mem_available = int(line.split()[1]) / 1024
                    break
    except:
        mem_available = 500
    if mem_available < 500:
        print(f"    内存不足({mem_available:.0f}MB)，跳过LLM摘要")
        return content[:100]
    # 短prompt
    summary_content = content[:150].replace('\n', ' ')
    prompt = f"用20字以内总结：{topic}。内容：{summary_content}"
    try:
        result = subprocess.run(
            ['/root/.nvm/versions/node/v22.22.2/bin/mmx', 'text', 'chat',
             '--model', 'abab6.5-chat', '--message', prompt, '--output', 'json'],
            capture_output=True, timeout=20
        )
        out = result.stdout.decode('utf-8', errors='ignore').strip()
        data = json.loads(out)
        for block in data.get("content", []):
            if block.get("type") == "text":
                return block.get("text", "").strip()
        return content[:80]
    except Exception as e:
        print(f"    LLM跳过: {e}")
        return content[:80]

def save_learnings(topic, findings, summary):
    """保存学习笔记"""
    note = {
        "time": datetime.now().isoformat(),
        "topic": topic,
        "findings": findings,
        "summary": summary,
    }
    note_file = f"{STUDY_DIR}/learnings.json"
    notes = []
    if os.path.exists(note_file):
        with open(note_file) as f:
            notes = json.load(f)
    notes.insert(0, note)
    notes = notes[:50]  # 保留最近50条
    with open(note_file, 'w') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    
    # 写入日誌
    log_file = f"{STUDY_DIR}/study_log.md"
    with open(log_file, 'a') as f:
        f.write(f"\n## [{datetime.now().strftime('%H:%M')}] {topic}\n")
        f.write(f"{summary or '无摘要'}\n")
        for item in (findings[:3] if isinstance(findings, list) else []):
            f.write(f"- {item}\n")

def main():
    pending = get_queue_status()
    ts = datetime.now().strftime('%H:%M:%S')
    
    if pending > 0:
        print(f"[{ts}] 队列有{pending}个任务，学习跳过")
        return
    
    print(f"[{ts}] 队列空闲，启动学习会话")
    
    # 随机选一个话题
    study = random.choice(STUDY_TOPICS)
    topic = study['topic']
    print(f"[{ts}] 学习主题: {topic}")
    
    findings = []
    summary = None
    
    if study['type'] == 'github':
        repos = github_search(study['keywords'], study.get('stars_min', 50))
        if repos:
            findings = [f"{name} ⭐{stars}: {desc[:60]}" for name, stars, desc in repos]
            print(f"[{ts}] 找到 {len(repos)} 个GitHub项目")
    
    elif study['type'] == 'arxiv':
        papers = arxiv_fetch(study['rss'])
        if papers:
            findings = [f"{p['title'][:60]} — {p['url']}" for p in papers]
            print(f"[{ts}] 找到 {len(papers)} 篇论文")
    
    # LLM生成简短总结
    if findings:
        content = "\n".join(findings)
        summary = llm_summarize(topic, content)
        print(f"[{ts}] AI摘要: {summary[:80] if summary else '无'}")
    
    save_learnings(topic, findings, summary)
    print(f"[{ts}] 学习完成，已保存")

if __name__ == "__main__":
    main()

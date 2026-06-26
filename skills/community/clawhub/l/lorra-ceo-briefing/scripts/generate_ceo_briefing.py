#!/usr/bin/env python3
"""
CEO Briefing Generator (分层选稿版)
新流程：
  1. 按来源分层组织数据（深度/快讯/社科/理财/思维）
  2. Newsletter级内容抓原文 + 500字摘要
  3. 快讯级内容直接用标题+摘要
  4. 主编单次输出分层简报
"""
import json, os, re, requests, concurrent.futures
from datetime import datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(SKILL_DIR, "reports")
ENV_FILE = "/home/ubuntu/.openclaw/workspace/.env"

MINIMAX_API_HOST = "https://api.minimaxi.com"
M2_MODEL = "MiniMax-M2.1"
M2_7_MODEL = "MiniMax-M2.7"

# ------------------------------------------------------------------
# 来源分层配置
# ------------------------------------------------------------------
DEEP_SOURCES = {
    "Interconnects", "ChinAI", "Memia", "One Useful Thing",
    "Latent Space", "80000 Hours"
}
FINANCE_SOURCES = {
    "Making Sense of Cents", "Clever Girl Finance", "The Next Recession",
    "AI to ROI"
}
SOCIAL_SOURCES = {
    "Jacobin", "Social Europe", "China Digital Times"
}
ESSAY_SOURCES = {
    "Wait But Why", "Paul Graham", "Farnam Street",
    "Lex Fridman", "James Clear", "Scott Young", "Dan Koe"
}
FAST_AI_SOURCES = {
    "Hacker News", "GitHub", "Product Hunt", "Ben's Bites", "KDnuggets"
}

# ------------------------------------------------------------------
# 工具函数
# ------------------------------------------------------------------
def load_env():
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def call_minimax(messages, model=M2_MODEL, max_tokens=8000, temperature=0.3):
    env = load_env()
    api_key = env.get("MINIMAX_API_KEY")
    if not api_key:
        raise RuntimeError("MINIMAX_API_KEY not found")
    url = f"{MINIMAX_API_HOST}/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def load_json(date):
    path = os.path.join(REPORTS_DIR, date, "general_briefing_unified.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No JSON for {date}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def fetch_article_content(url, timeout=15):
    """Fetch full article content via Jina Reader."""
    try:
        jina_url = f"https://r.jina.ai/{url}"
        headers = {"Accept": "text/plain", "X-Timeout": "15"}
        resp = requests.get(jina_url, headers=headers, timeout=timeout)
        if resp.status_code == 200 and len(resp.text) > 200:
            return resp.text[:5000].strip()
    except Exception as e:
        print(f"    ⚠️ Fetch failed: {url[:60]} - {e}")
    return None

def parallel_fetch(items, max_workers=8):
    """Fetch content for items in parallel."""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_article_content, item.get('url','')): i
                   for i, item in enumerate(items)}
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    return results

# ------------------------------------------------------------------
# 工具函数
# ------------------------------------------------------------------
def is_item_stale(item, max_age_days=7):
    """检查条目是否太旧。Newsletter级来源默认7天内的才用。"""
    source = item.get('source', '')
    if source not in DEEP_SOURCES and source not in ESSAY_SOURCES:
        return False
    pub_time = item.get('time', '')
    if not pub_time:
        return False
    # 尝试解析时间字符串（格式：'Tue, 24 Mar 2026 14:01:06 GMT'）
    try:
        pub_date = datetime.strptime(pub_time[:25].strip(), '%a, %d %b %Y %H:%M:%S')
        age = (datetime.now() - pub_date).days
        if age > max_age_days:
            print(f"    ⏭️ 跳过过期文章 [{age}天前]: {item.get('title','')[:50]}")
            return True
    except Exception:
        pass
    return False

# ------------------------------------------------------------------
# Step 1: 分层组织数据
# ------------------------------------------------------------------
def organize_by_tier(data):
    """按来源分层分类所有条目，Newsletter级自动过滤7天前内容。"""
    deep, fast_ai, social, finance, essays, other = [], [], [], [], [], []

    for section_key in ['hn_ai', 'global_scan', 'insights', 'github_trending']:
        for item in data.get(section_key, []):
            source = item.get('source', '')

            # Newsletter/Essays 级：过滤太旧的文章
            if source in DEEP_SOURCES or source in ESSAY_SOURCES:
                if is_item_stale(item, max_age_days=7):
                    continue

            if source in DEEP_SOURCES:
                deep.append(item)
            elif source in FAST_AI_SOURCES or section_key == 'github_trending':
                fast_ai.append(item)
            elif source in SOCIAL_SOURCES:
                social.append(item)
            elif source in FINANCE_SOURCES:
                finance.append(item)
            elif source in ESSAY_SOURCES:
                essays.append(item)
            else:
                other.append(item)

    # 去重（按url）
    def dedup(items):
        seen = set()
        result = []
        for item in items:
            url = item.get('url', '')
            if url and url not in seen:
                seen.add(url)
                result.append(item)
        return result

    return {
        'deep': dedup(deep),
        'fast_ai': dedup(fast_ai),
        'social': dedup(social),
        'finance': dedup(finance),
        'essays': dedup(essays),
        'other': dedup(other),
    }

# ------------------------------------------------------------------
# Step 2: 为各层准备内容
# ------------------------------------------------------------------
def prepare_deep_content(items, max_items=3):
    """Newsletter级：抓原文，500字摘要。"""
    items = items[:max_items]
    fetched = parallel_fetch(items)
    lines = []
    for i, item in enumerate(items):
        content = item.get('content', '') or fetched.get(i, '') or ''
        if len(content) < 100:
            content = f"[无正文] 请根据以下信息判断：{item.get('summary', item.get('title',''))}"
        lines.append(f"""## {i+1}. {item.get('title','')}

**来源**: {item.get('source','')} | **时间**: {item.get('time','')[:16]}
**链接**: {item.get('url','')}

{content[:500]}""")
    return "\n\n".join(lines) if lines else "(今日无深度文章)"

def prepare_fast_content(items, max_items=8):
    """快讯级：直接用标题+摘要+热度的简短描述。"""
    items = items[:max_items]
    lines = []
    for i, item in enumerate(items):
        heat = item.get('heat', '')
        summary = item.get('summary', item.get('content','')[:200])
        hn_url = item.get('hn_url', '')
        extra = f" [HN讨论]({hn_url})" if hn_url else ""
        lines.append(f"""### {i+1}. {item.get('title','')}

- 来源: {item.get('source','')} | {item.get('time','')[:16]}{f' | 热度: {heat}' if heat else ''}
- 链接: {item.get('url','')}{extra}
- 摘要: {summary[:300]}""")
    return "\n\n".join(lines) if lines else "(今日无快讯)"

def prepare_simple_content(items, max_items=4):
    """社科/理财/思维：直接用标题+摘要。"""
    items = items[:max_items]
    lines = []
    for i, item in enumerate(items):
        summary = item.get('summary', item.get('content','')[:400])
        lines.append(f"""### {i+1}. {item.get('title','')}

- 来源: {item.get('source','')} | {item.get('time','')[:16]}
- 链接: {item.get('url','')}
- 摘要: {summary[:400]}""")
    return "\n\n".join(lines) if lines else "(今日无相关内容)"

# ------------------------------------------------------------------
# Step 3: 主编输出分层简报
# ------------------------------------------------------------------
def generate_briefing(date=None):
    env = load_env()
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    print(f"=== CEO 简报生成开始 [{date}] ===")

    # Step 1: 加载数据
    print("Step 1: 加载 RSS 数据...")
    data = load_json(date)

    # Step 2: 分层
    print("Step 2: 按来源分层...")
    tiers = organize_by_tier(data)
    print(f"  深度: {len(tiers['deep'])} | 快讯: {len(tiers['fast_ai'])} | "
          f"社科: {len(tiers['social'])} | 理财: {len(tiers['finance'])} | "
          f"思维: {len(tiers['essays'])}")

    # Step 3: 准备各层内容
    print("Step 3: 准备内容...")
    deep_text = prepare_deep_content(tiers['deep'], max_items=3)
    fast_text = prepare_fast_content(tiers['fast_ai'], max_items=8)
    social_text = prepare_simple_content(tiers['social'], max_items=3)
    finance_text = prepare_simple_content(tiers['finance'], max_items=3)
    essays_text = prepare_simple_content(tiers['essays'], max_items=2)

    # Step 4: 主编生成
    print("Step 4: 主编生成简报...")
    system_prompt = "你是一个科技商业简报编辑（CEO Edition）。输出语言：简体中文。"

    user_prompt = f"""你是CEO简报主编，直接生成最终简报。不要重复引用instruction或流程说明。

## 今日数据（{date}）

=== 🦄 AI 深度读（Newsletter级，选2-3篇今天最值得读的，每篇500字摘要）===
{deep_text}

=== 🤖 AI 快讯（Hacker News + GitHub热门，选5-8条有价值的，简短impact）===
{fast_text}

=== 🌍 社科观察（选2-3篇有独立视角的）===
{social_text}

=== 💰 理财与市场（选2-3篇有价值的）===
{finance_text}

=== 📚 思维拓展（选1-2篇值得静下心来读的）===
{essays_text}

---

## 输出格式（严格遵守）

```markdown
# 📰 每日简报 - {date}

---

## 📌 一句话判断

今天最值得记住的一件事（1-2句，不是目录，是你的观点）

---

## 🦄 AI 深度读

### [文章标题]
**来源**: xxx | **时间**: xxx
🔗 链接

[500字左右的深度摘要，要写出具体内容、争议点、为什么值得读。不要只是标题复述。]

---

## 🤖 AI 快讯

选5-8条，每条格式：
- **[标题]** 🔗链接
  - 一句话说明 + 简短impact

---

## 🌍 社科观察

选2-3条，每条格式：
- **[标题]** 🔗链接
  - 发生了什么 + 为什么重要

---

## 💰 理财与市场

选2-3条，每条格式：
- **[标题]** 🔗链接
  - 发生了什么 + 对你的意义

---

## 📚 思维拓展

选1-2篇值得静下心来读的，格式：
- **[标题]** 🔗链接
  - 一句话介绍

---

## 💭 读后思考

3个问题：
1. [联系AI和现实的问题]
2. [预测性问题]
3. [行动性问题]
```

## 质量标准

- ✅ Executive Summary 要有主编的个人判断，不是目录复述
- ✅ 深度读要写出争议点和技术细节，不是标题摘要
- ✅ 快讯不要和深度读重复内容
- ✅ 社科要有独立视角，不要只是AI新闻
- ✅ 理财内容不要和社科混在一起
- ✅ 每个section的内容条数要精简（深度2-3，快讯5-8，社科2-3，理财2-3，思维1-2）
- ❌ 不要捏造任何链接或数据
- ❌ 不要用"这是一个..."开头
- ❌ 不要写"#1 #2 #3"这种排行榜格式
"""

    result = call_minimax([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ], model=M2_7_MODEL, max_tokens=12000, temperature=0.4)

    # Step 5: Save
    out_path = os.path.join(REPORTS_DIR, date, "ceo_briefing.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"✅ 简报已保存: {out_path}")

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    result = generate_briefing(args.date)
    print("\n" + "="*60)
    print(result)

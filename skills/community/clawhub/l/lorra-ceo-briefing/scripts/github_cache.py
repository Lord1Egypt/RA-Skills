#!/usr/bin/env python3
"""
GitHub Trending 缓存 + 深度解读模块
功能：
1. 缓存之前上过 trending 的项目
2. 只输出新上榜的项目
3. 对新项目进行深度解读（能力、用途、性能要求）
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path

CACHE_DIR = Path(os.path.expanduser("~/.openclaw/skills/news-aggregator-skill/cache"))
CACHE_FILE = CACHE_DIR / "github_trending_cache.json"

# OpenRouter API (免费模型)
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def ensure_cache_dir():
    """确保缓存目录存在"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not CACHE_FILE.exists():
        with open(CACHE_FILE, 'w') as f:
            json.dump({"projects": {}, "last_update": None}, f)

def load_cache():
    """加载缓存"""
    ensure_cache_dir()
    with open(CACHE_FILE, 'r') as f:
        return json.load(f)

def save_cache(cache):
    """保存缓存"""
    ensure_cache_dir()
    cache["last_update"] = datetime.now().isoformat()
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def get_project_key(project):
    """生成项目唯一标识"""
    return project.get("repo_name", "")

def is_new_project(project, cache):
    """检查项目是否新上榜"""
    key = get_project_key(project)
    return key not in cache.get("projects", {})

def filter_new_projects(projects):
    """过滤出只的新上榜项目"""
    cache = load_cache()
    new_projects = []
    
    for project in projects:
        if is_new_project(project, cache):
            new_projects.append(project)
    
    return new_projects

def update_cache_with_new_projects(projects):
    """更新缓存，添加新项目"""
    cache = load_cache()
    
    for project in projects:
        key = get_project_key(project)
        cache["projects"][key] = {
            "name": project.get("name", ""),
            "description": project.get("description", ""),
            "stars": project.get("stars", 0),
            "first_seen": datetime.now().isoformat(),
            "url": project.get("url", "")
        }
    
    save_cache(cache)
    print(f"📝 缓存已更新: 新增 {len(projects)} 个项目")

def analyze_with_llm(project):
    """使用 LLM 进行深度分析"""
    if not OPENROUTER_API_KEY:
        return None
    
    prompt = f"""你是一个技术分析师。请对以下 GitHub 项目进行深度分析：

## 项目信息
- 名称: {project.get('title', '').split(' - ')[0]}
- 描述: {project.get('title', '').split(' - ')[1] if ' - ' in project.get('title', '') else ''}
- Stars: {project.get('heat', '')}
- 链接: {project.get('url', '')}

请分析以下方面，用简洁的中文回答（每个部分不超过2句话）：
1. **这是什么**: 一句话说清核心功能
2. **能做什么**: 2-3个典型应用场景
3. **技术亮点**: 核心技术栈和创新点
4. **使用条件**: 需要什么环境/依赖
5. **适合谁**: 目标用户

只输出分析内容，不要其他废话。"""

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/hunter-alpha",  # 免费模型
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️ LLM 分析失败: {e}")
    return None

def process_github_trending(projects, do_deep_analysis=True):
    """
    处理 GitHub Trending 项目：
    1. 过滤新项目
    2. 更新缓存
    3. 可选：深度分析
    """
    cache = load_cache()
    new_projects = []
    
    for project in projects:
        if is_new_project(project, cache):
            # 尝试深度分析
            if do_deep_analysis and OPENROUTER_API_KEY:
                print(f"🔍 深度分析: {project.get('repo_name', '')}")
                analysis = analyze_with_llm(project)
                project["deep_analysis"] = analysis
            
            new_projects.append(project)
    
    if new_projects:
        update_cache_with_new_projects(new_projects)
    
    return new_projects

if __name__ == "__main__":
    ensure_cache_dir()
    print(f"✅ 缓存目录: {CACHE_DIR}")
    print(f"✅ 缓存文件: {CACHE_FILE}")
    
    # 测试
    cache = load_cache()
    print(f"📊 已缓存项目数: {len(cache.get('projects', {}))}")

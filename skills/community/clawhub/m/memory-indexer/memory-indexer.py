#!/usr/bin/env python3
"""
Memory Indexer - 短期记忆关键词索引工具

功能：
1. 保存短期记忆到文件
2. 自动提取关键词
3. 建立关键词 → 记忆文件 索引
4. 同步外部记忆目录并建立索引
5. 多关键词搜索（AND/OR 模式）
6. 清理失效索引
7. 记忆关联发现
8. 时间线视图
9. 主动提醒（获取相关记忆）
10. 记忆摘要
11. 重要记忆标记

用法：
    python3 memory-indexer.py add "记忆内容" [标签1 标签2 ...]
    python3 memory-indexer.py search "关键词"          # OR 模式（任一匹配）
    python3 memory-indexer.py search "关键词1 关键词2" --and  # AND 模式（全部匹配）
    python3 memory-indexer.py list
    python3 memory-indexer.py sync                    # 扫描外部记忆目录
    python3 memory-indexer.py sync --watch         # 监控模式（增量同步）
    python3 memory-indexer.py status                # 查看索引状态
    python3 memory-indexer.py cleanup               # 清理失效索引
    python3 memory-indexer.py related               # 显示关联记忆
    python3 memory-indexer.py timeline              # 时间线视图
    python3 memory-indexer.py recall "关键词"       # 主动提醒（获取相关记忆）
    python3 memory-indexer.py summary               # 生成记忆摘要
    python3 memory-indexer.py star <文件名>          # 标记重要记忆
    python3 memory-indexer.py stars                  # 查看重要记忆
    python3 memory-indexer.py keywords "文本"        # 调试：显示文本的关键词
"""

import json
import os
import sys
import re
import argparse
from datetime import datetime
from pathlib import Path

# 尝试导入 jieba，如果失败则使用简单方案
try:
    import jieba
    import jieba.analyse
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("警告: jieba 未安装，使用简单分词方案")

# 尝试导入 embedding 模块（用于向量搜索）
try:
    from embedding import search_semantic, get_embedding, get_vector_status
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False
    # 向量搜索不可用时静默跳过

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = Path(__file__).parent / "data"
EXTERNAL_MEMORY_DIR = WORKSPACE / "memory"  # 外部记忆目录
INDEX_FILE = MEMORY_DIR / "index.json"
STATE_FILE = MEMORY_DIR / "sync-state.json"  # 同步状态（记录已同步的文件）

# 停用词（常见的无意义词）
STOPWORDS = {
    # 常见虚词
    "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
    "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
    "自己", "这", "那", "什么", "他", "她", "它", "们", "吗", "呢", "吧", "啊",
    "嗯", "哦", "呀", "嗨", "唉", "喂", "嘿", "哈", "嘚", "哟", "诶", "哎",
    "可以", "这个", "那个", "怎么", "为什么", "如何", "哪个", "哪些", "多少",
    "因为", "所以", "但是", "如果", "虽然", "还是", "或者", "而且", "然后",
    "其实", "当然", "可能", "应该", "需要", "已经", "正在", "将要", "曾经",
    "今天", "昨天", "明天", "现在", "刚才", "以前", "以后", "时候", "地方",
    "事情", "东西", "问题", "样子", "想法", "感觉", "意思", "道理", "方法",
    # 飞书/系统相关无意义词
    "ou", "oc", "om", "omt", "msg", "id", "token", "gmt", "zh", "cn",
    "feishu", "openclaw", "default", "app", "user", "message", "chat",
    # 纯数字/日期
    "2024", "2025", "2026", "2023", "2022", "2021", "2020",
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
    "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "27", "28", "29", "30", "31",
}

# 飞书消息 ID 格式过滤正则
FEISHU_ID_PATTERN = re.compile(r'^[ocou][a-z0-9]{10,}$')
# 其他短 ID 格式
SHORT_ID_PATTERN = re.compile(r'^[a-z0-9]{20,}$')
# UUID 格式
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
# Hex 字符串（32位以上）
HEX_PATTERN = re.compile(r'^[0-9a-f]{32,}$')
# Base64 字符串
BASE64_PATTERN = re.compile(r'^[A-Za-z0-9+/]{20,}={0,2}$')
# GitHub Token 格式 (ghp_xxx, gho_xxx, ghu_xxx, ghs_xxx, ghr_xxx, github_pat_xxx 等)
GITHUB_TOKEN_PATTERN = re.compile(r'^(ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{10,}$')
# 其他常见 Token 格式
TOKEN_PREFIXES = ['sk-', 'skl-', 'Bearer ', 'eyJ', 'AKIA']  # OpenAI, Google, AWS 等

def is_technical_id(word: str) -> bool:
    """检查是否是技术性 ID（应过滤）"""
    if not word:
        return True
    word_lower = word.lower()
    # 跳过短词
    if len(word) < 3:
        return True
    # 跳过纯数字
    if word.isdigit():
        return True
    # 检查各种技术 ID 格式
    if FEISHU_ID_PATTERN.match(word):
        return True
    if SHORT_ID_PATTERN.match(word):
        return True
    if UUID_PATTERN.match(word_lower):
        return True
    if HEX_PATTERN.match(word_lower):
        return True
    if BASE64_PATTERN.match(word):
        return True
    # 检查 GitHub Token 格式（完整匹配或包含前缀）
    if GITHUB_TOKEN_PATTERN.match(word_lower):
        return True
    # 检查是否包含 GitHub Token 前缀（jieba 分词后可能不完整）
    # 过滤 ghp, gho, ghu, ghs, ghr 等被拆分的前缀
    if word_lower in ['ghp', 'gho', 'ghu', 'ghs', 'ghr']:
        return True
    if 'ghp_' in word_lower or 'gho_' in word_lower or 'ghu_' in word_lower or 'ghs_' in word_lower or 'ghr_' in word_lower or 'github_pat' in word_lower:
        return True
    # 检查其他常见 Token 前缀
    for prefix in TOKEN_PREFIXES:
        if prefix.lower() in word_lower:
            return True
    # 跳过包含大量数字的词（如时间戳）
    digit_count = sum(c.isdigit() for c in word)
    if len(word) > 5 and digit_count / len(word) > 0.5:
        return True
    return False

def ensure_memory_dir():
    """确保记忆目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

def load_index() -> dict:
    """加载索引"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_index(index: dict):
    """保存索引"""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def extract_keywords(text: str, topk: int = 10) -> list:
    """提取关键词"""
    if JIEBA_AVAILABLE:
        # 使用 TF-IDF 提取关键词
        keywords = jieba.analyse.extract_tags(text, topK=topk * 2, withWeight=False)  # 先多取一些，后面过滤
        # 过滤停用词和技术性 ID
        keywords = [w for w in keywords if w.lower() not in STOPWORDS and not is_technical_id(w)]
        keywords = keywords[:topk]  # 再截取实际需要数量
    else:
        # 简单方案：提取连续的中文字符组合
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        # 简单去重和排序
        word_freq = {}
        for w in words:
            if w not in STOPWORDS and not is_technical_id(w):
                word_freq[w] = word_freq.get(w, 0) + 1
        keywords = sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)[:topk]
    
    return keywords

def add_memory(content: str, manual_tags: list = None, topk: int = 10):
    """添加记忆"""
    ensure_memory_dir()
    
    # 生成文件名（日期+时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.md"
    filepath = MEMORY_DIR / filename
    
    # 保存记忆内容
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 短期记忆 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"{content}\n")
    
    # 提取关键词（支持自定义数量）
    auto_keywords = extract_keywords(content, topk=topk)
    all_tags = list(set((manual_tags or []) + auto_keywords))
    
    # 更新索引
    index = load_index()
    
    # 为每个关键词添加映射
    for tag in all_tags:
        tag = tag.lower()
        if tag not in index:
            index[tag] = []
        # 避免重复添加
        if filepath.name not in [item["file"] for item in index[tag]]:
            index[tag].append({
                "file": filepath.name,
                "time": timestamp,
                "preview": content[:50] + "..." if len(content) > 50 else content
            })
    
    save_index(index)
    
    print(f"✅ 记忆已保存: {filename}")
    print(f"📝 关键词: {', '.join(all_tags)}")

def search_memories(query: str, mode: str = "or"):
    """
    搜索记忆
    
    Args:
        query: 查询词，支持多关键词（用空格或逗号分隔）
        mode: "and" 表示所有关键词都匹配，"or" 表示任一关键词匹配
    """
    index = load_index()
    
    # 解析多关键词
    # 支持: "小红书 日记" 或 "小红书,日记" 或 "小红书 AND 日记"
    query = query.lower()
    # 统一分隔符
    query = query.replace(",", " ").replace(" and ", " ").replace(" AND ", " ")
    keywords = [k.strip() for k in query.split() if k.strip() and k.strip() not in STOPWORDS]
    
    if not keywords:
        print("查询词无意义，跳过搜索")
        return
    
    # 过滤无意义的查询词
    valid_keywords = []
    for kw in keywords:
        if kw in STOPWORDS or FEISHU_ID_PATTERN.match(kw) or SHORT_ID_PATTERN.match(kw):
            continue
        valid_keywords.append(kw)
    
    if not valid_keywords:
        print("查询词无意义，跳过搜索")
        return
    
    # 为每个关键词找到匹配的文件
    keyword_matches = {}  # keyword -> set of file_keys
    for kw in valid_keywords:
        matches = set()
        # 精确匹配
        if kw in index:
            for item in index[kw]:
                matches.add(item["file"])
        # 模糊匹配
        for tag in index.keys():
            if kw in tag and tag != kw:
                for item in index[tag]:
                    matches.add(item["file"])
        keyword_matches[kw] = matches
    
    # 根据模式计算最终结果
    if mode == "and":
        # 所有关键词都匹配的文件
        final_files = set()
        for kw, matches in keyword_matches.items():
            if not final_files:
                final_files = matches
            else:
                final_files = final_files & matches
    else:
        # 任一关键词匹配的文件
        final_files = set()
        for matches in keyword_matches.values():
            final_files = final_files | matches
    
    # 构建结果列表
    results = []
    for file_key in final_files:
        # 收集所有匹配的信息
        score = 0
        preview = ""
        time_val = ""
        
        for kw in valid_keywords:
            if kw in index:
                for item in index[kw]:
                    if item["file"] == file_key:
                        score += 10
                        if not preview:
                            preview = item.get("preview", "")
                        if not time_val:
                            time_val = item.get("time", "")
            # 模糊匹配加分少
            for tag in index.keys():
                if kw in tag and tag != kw:
                    for item in index[tag]:
                        if item["file"] == file_key:
                            score += 1
                            if not preview:
                                preview = item.get("preview", "")
                            if not time_val:
                                time_val = item.get("time", "")
        
        results.append({
            "file": file_key,
            "time": time_val,
            "preview": preview,
            "score": score
        })
    
    # 按相关性分数降序排序
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    if not results:
        print("未找到相关记忆")
        return
    
    print(f"找到 {len(results)} 条相关记忆 (模式: {mode.upper()}):\n")
    print(f"关键词: {', '.join(valid_keywords)}\n")
    for item in results:
        score_indicator = "🔥" * min(int(item.get("score", 0) * 10), 3)
        print(f"📄 {item['file']} - {item['time']} {score_indicator}")
        print(f"   {item['preview']}")
        print()

def search_raw_memories(query: str, top_k: int = 10) -> list:
    """
    原文搜索 - 在记忆文件内容中搜索包含查询词的记录
    
    Args:
        query: 查询词
        top_k: 返回结果数量
        
    Returns:
        list: 匹配的记录列表
    """
    from pathlib import Path
    
    # 搜索内部记忆目录和外部记忆目录
    search_dirs = [MEMORY_DIR, EXTERNAL_MEMORY_DIR]
    
    results = []
    query_lower = query.lower()
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
            
        for f in search_dir.glob("*.md"):
            try:
                with open(f, "r", encoding="utf-8") as file:
                    content = file.read()
                    
                # 检查内容是否包含查询词
                if query_lower in content.lower():
                    # 计算出现次数作为分数
                    count = content.lower().count(query_lower)
                    
                    # 提取预览（前200字符）
                    preview = content[:200].replace("\n", " ")
                    
                    # 获取文件时间
                    import time
                    mtime = time.localtime(f.stat().st_mtime)
                    time_str = time.strftime("%Y-%m-%d %H:%M", mtime)
                    
                    results.append({
                        "file": f.name,
                        "time": time_str,
                        "preview": preview,
                        "score": count,
                        "layer": 3  # 标记为第三层
                    })
            except Exception:
                continue
    
    # 按分数降序排序
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results[:top_k]


def search_hybrid(query: str, top_k: int = 10) -> list:
    """
    三级级联搜索：
    1. 关键词搜索（最高优先级）
    2. 向量语义搜索
    3. 原文全文搜索
    
    Args:
        query: 查询词
        top_k: 返回结果数量
        
    Returns:
        list: 合并后的搜索结果
    """
    seen_files = set()
    all_results = []
    
    # 第1层：关键词搜索
    print("🔍 第1层：关键词搜索...")
    keyword_results = search_memories(query, mode="or")
    # search_memories 会直接打印结果，这里需要手动收集
    # 所以我们用另一种方式 - 调用内部函数
    
    # 重新实现关键词搜索逻辑（不打印）
    index = load_index()
    query_lower = query.lower()
    query_clean = query_lower.replace(",", " ").replace(" and ", " ")
    keywords = [k.strip() for k in query_clean.split() if k.strip() and k.strip() not in STOPWORDS]
    
    if keywords:
        # 快速搜索
        keyword_matches = set()
        for kw in keywords:
            if kw in index:
                for item in index[kw]:
                    keyword_matches.add(item["file"])
        
        # 获取文件内容
        for file_key in keyword_matches:
            preview = ""
            time_val = ""
            for tag, items in index.items():
                for item in items:
                    if item["file"] == file_key:
                        preview = item.get("preview", "")
                        time_val = item.get("time", "")
                        break
            all_results.append({
                "file": file_key,
                "time": time_val,
                "preview": preview,
                "score": 100,  # 关键词匹配最高分
                "layer": 1
            })
            seen_files.add(file_key)
    
    if all_results:
        print(f"   ✓ 找到 {len(all_results)} 条结果")
    else:
        print("   ✗ 无结果")
    
    # 第2层：向量语义搜索
    if EMBEDDING_AVAILABLE:
        print("🔍 第2层：向量语义搜索...")
        try:
            vector_results = search_semantic(query, top_k=top_k)
            if vector_results:
                for r in vector_results:
                    if r["file"] not in seen_files:
                        r["layer"] = 2
                        all_results.append(r)
                        seen_files.add(r["file"])
                print(f"   ✓ 找到 {len(vector_results)} 条新结果")
            else:
                print("   ✗ 无新结果")
        except Exception as e:
            print(f"   ✗ 向量搜索失败: {e}")
    else:
        print("🔍 第2层：向量语义搜索... (未启用)")
    
    # 第3层：原文搜索
    print("🔍 第3层：原文搜索...")
    raw_results = search_raw_memories(query, top_k=top_k)
    new_raw_count = 0
    for r in raw_results:
        if r["file"] not in seen_files:
            r["layer"] = 3
            all_results.append(r)
            seen_files.add(r["file"])
            new_raw_count += 1
    
    if new_raw_count > 0:
        print(f"   ✓ 找到 {new_raw_count} 条新结果")
    else:
        print("   ✗ 无新结果")
    
    # 按分数和层级排序（层级优先）
    all_results.sort(key=lambda x: (x.get("layer", 99), -x.get("score", 0)))
    
    return all_results[:top_k]


def display_search_results(results: list, query: str, show_layer: bool = False):
    """显示搜索结果"""
    if not results:
        print("\n未找到相关记忆")
        return
    
    print(f"\n找到 {len(results)} 条相关记忆:\n")
    
    for i, item in enumerate(results, 1):
        layer_info = ""
        if show_layer:
            layer_names = {1: "关键词", 2: "向量", 3: "原文"}
            layer_info = f" [{layer_names.get(item.get('layer'), '?')}]"
        
        score_indicator = "🔥" * min(int(item.get("score", 0) * 10), 3)
        print(f"{i}. 📄 {item['file']} - {item.get('time', '')} {score_indicator}{layer_info}")
        preview = item.get("preview", "")
        if preview:
            # 关键词高亮
            query_words = query.lower().split()
            for qw in query_words:
                if len(qw) > 1:
                    preview = preview.replace(qw, f"**{qw}**")
            print(f"   {preview[:120]}...")
        print()


def list_memories():
    """列出所有记忆"""
    ensure_memory_dir()
    
    files = sorted(MEMORY_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not files:
        print("暂无记忆")
        return
    
    print(f"共 {len(files)} 条记忆:\n")
    for f in files:
        print(f"📄 {f.name}")

def load_sync_state() -> dict:
    """加载同步状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"synced_files": {}}

def save_sync_state(state: dict):
    """保存同步状态"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def extract_content_from_memory_file(filepath: Path) -> str:
    """从记忆文件中提取内容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # 去掉 markdown 标题和空行
        lines = content.split("\n")
        clean_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                clean_lines.append(line)
        return "\n".join(clean_lines)
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return ""

def sync_external_memories():
    """同步外部记忆目录"""
    if not EXTERNAL_MEMORY_DIR.exists():
        print(f"外部记忆目录不存在: {EXTERNAL_MEMORY_DIR}")
        return
    
    ensure_memory_dir()
    state = load_sync_state()
    synced = state.get("synced_files", {})
    
    # 扫描外部目录的所有 .md 文件
    md_files = list(EXTERNAL_MEMORY_DIR.glob("*.md"))
    
    new_count = 0
    for md_file in md_files:
        # 获取文件修改时间作为版本标识
        mtime = md_file.stat().st_mtime
        file_key = md_file.name
        
        # 检查是否需要同步（新增或已修改）
        if file_key not in synced or synced[file_key] != mtime:
            content = extract_content_from_memory_file(md_file)
            if content:
                # 添加到索引
                index = load_index()
                keywords = extract_keywords(content)
                
                for tag in keywords:
                    tag = tag.lower()
                    if tag not in index:
                        index[tag] = []
                    # 避免重复添加
                    if file_key not in [item["file"] for item in index[tag]]:
                        index[tag].append({
                            "file": file_key,
                            "time": datetime.fromtimestamp(mtime).strftime("%Y%m%d_%H%M%S"),
                            "preview": content[:50] + "..." if len(content) > 50 else content,
                            "source": "external"
                        })
                
                save_index(index)
                synced[file_key] = mtime
                new_count += 1
                print(f"✅ 已索引: {file_key} (关键词: {', '.join(keywords[:5])}...)")
    
    # 保存同步状态
    state["synced_files"] = synced
    save_sync_state(state)
    
    if new_count == 0:
        print("没有新的记忆需要索引")
    else:
        print(f"\n索引完成，新增 {new_count} 条记录")

def show_status():
    """显示索引状态"""
    index = load_index()
    state = load_sync_state()
    
    print("=== 索引状态 ===")
    print(f"索引关键词数: {len(index)}")
    
    # 统计
    file_count = set()
    for items in index.values():
        for item in items:
            file_count.add(item["file"])
    print(f"索引文件数: {len(file_count)}")
    
    print(f"\n已同步外部文件: {len(state.get('synced_files', {}))}")
    
    if index:
        print(f"\n热门关键词 TOP 10:")
        sorted_tags = sorted(index.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for tag, items in sorted_tags:
            print(f"  {tag}: {len(items)} 条")

def cleanup_index():
    """清理失效的索引条目"""
    index = load_index()
    state = load_sync_state()
    
    # 获取所有有效的文件
    valid_files = set()
    
    # 外部记忆目录的文件
    if EXTERNAL_MEMORY_DIR.exists():
        for f in EXTERNAL_MEMORY_DIR.glob("*.md"):
            valid_files.add(f.name)
    
    # 自身 memory-index 目录的文件
    for f in MEMORY_DIR.glob("*.md"):
        valid_files.add(f.name)
    
    print(f"有效文件: {len(valid_files)} 个")
    
    # 清理索引中不存在的文件
    removed_count = 0
    new_index = {}
    for tag, items in index.items():
        valid_items = []
        for item in items:
            if item["file"] in valid_files:
                valid_items.append(item)
            else:
                removed_count += 1
        if valid_items:
            new_index[tag] = valid_items
    
    # 清理同步状态
    new_synced = {}
    for file_key, mtime in state.get("synced_files", {}).items():
        if file_key in valid_files:
            new_synced[file_key] = mtime
    
    save_index(new_index)
    state["synced_files"] = new_synced
    save_sync_state(state)
    
    print(f"已清理 {removed_count} 条失效索引")
    print(f"剩余索引关键词: {len(new_index)}")

# ============ 新功能：关联发现 ============

def find_related_memories():
    """发现关联记忆 - 找出经常一起出现的记忆"""
    index = load_index()
    
    # 构建文件-关键词映射
    file_keywords = {}
    for tag, items in index.items():
        for item in items:
            file_key = item["file"]
            if file_key not in file_keywords:
                file_keywords[file_key] = set()
            file_keywords[file_key].add(tag)
    
    # 计算相似度
    related = {}
    files = list(file_keywords.keys())
    for i, f1 in enumerate(files):
        for f2 in files[i+1:]:
            # 计算共同关键词数量
            common = file_keywords[f1] & file_keywords[f2]
            if len(common) >= 2:  # 至少2个共同关键词
                key = f1 if f1 < f2 else f2
                key2 = f2 if f1 < f2 else f1
                rel_key = f"{key}|{key2}"
                if rel_key not in related:
                    related[rel_key] = {
                        "files": (f1, f2),
                        "common": list(common),
                        "count": len(common)
                    }
    
    if not related:
        print("未发现关联记忆")
        return
    
    # 按关联度排序
    sorted_related = sorted(related.values(), key=lambda x: x["count"], reverse=True)
    
    print("=== 关联记忆发现 ===\n")
    for item in sorted_related[:10]:  # 显示前10
        f1, f2 = item["files"]
        print(f"📎 {f1} ↔ {f2}")
        print(f"   共同关键词: {', '.join(item['common'][:5])}")
        print()

# ============ 新功能：时间线视图 ============

def show_timeline():
    """显示记忆时间线"""
    index = load_index()
    
    # 收集所有记忆及其时间
    memories = {}
    for tag, items in index.items():
        for item in items:
            file_key = item["file"]
            if file_key not in memories:
                memories[file_key] = {
                    "time": item.get("time", ""),
                    "preview": item.get("preview", ""),
                    "keywords": set()
                }
            memories[file_key]["keywords"].add(tag)
    
    if not memories:
        print("暂无记忆")
        return
    
    # 按时间排序
    sorted_memories = sorted(memories.items(), key=lambda x: x[1]["time"], reverse=True)
    
    print("=== 记忆时间线 ===\n")
    for file_key, info in sorted_memories:
        print(f"📄 {file_key} - {info['time']}")
        print(f"   {info['preview']}")
        print(f"   关键词: {', '.join(list(info['keywords'])[:5])}")
        print()

# ============ 新功能：主动提醒 ============

def recall(keyword: str):
    """主动提醒 - 根据关键词获取相关记忆"""
    # 这里复用 search 功能，但输出更简洁
    index = load_index()
    keyword = keyword.lower()
    
    if keyword not in index:
        # 尝试模糊匹配
        matches = [tag for tag in index.keys() if keyword in tag]
        if not matches:
            print(f"未找到与 '{keyword}' 相关的记忆")
            return
        keyword = matches[0]
    
    items = index[keyword]
    
    print(f"=== 相关记忆提醒 ===")
    print(f"关键词: {keyword}\n")
    
    for item in items[:3]:  # 只显示前3条
        print(f"📄 {item['file']} ({item.get('time', '')})")
        print(f"   {item.get('preview', '')}")
        print()

# ============ 新功能：记忆摘要 ============

def generate_summary():
    """生成记忆摘要"""
    index = load_index()
    state = load_sync_state()
    
    # 统计
    file_count = set()
    keyword_count = len(index)
    for items in index.values():
        for item in items:
            file_count.add(item["file"])
    
    # 按时间统计
    timeline = {}
    for tag, items in index.items():
        for item in items:
            time_str = item.get("time", "")
            if time_str:
                date = time_str[:8]  # YYYYMMDD
                if date not in timeline:
                    timeline[date] = 0
                timeline[date] += 1
    
    # 热门关键词
    hot_keywords = sorted(index.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    
    print("=== 记忆摘要 ===\n")
    print(f"📊 总记忆数: {len(file_count)}")
    print(f"📊 关键词数: {keyword_count}")
    print(f"📊 同步文件数: {len(state.get('synced_files', {}))}")
    
    if timeline:
        sorted_timeline = sorted(timeline.items(), key=lambda x: x[0], reverse=True)
        print(f"\n📅 最近活动:")
        for date, count in sorted_timeline[:5]:
            formatted = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            print(f"   {formatted}: {count} 条")
    
    if hot_keywords:
        print(f"\n🔥 热门关键词:")
        for tag, items in hot_keywords:
            print(f"   {tag}: {len(items)} 条")

# ============ 新功能：重要记忆标记 ============

STARS_FILE = MEMORY_DIR / "stars.json"

def load_stars() -> set:
    """加载重要记忆标记"""
    if STARS_FILE.exists():
        with open(STARS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_stars(stars: set):
    """保存重要记忆标记"""
    with open(STARS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(stars), f, ensure_ascii=False, indent=2)

def star_memory(file_key: str):
    """标记重要记忆"""
    stars = load_stars()
    stars.add(file_key)
    save_stars(stars)
    print(f"✅ 已标记: {file_key}")

def unstar_memory(file_key: str):
    """取消标记"""
    stars = load_stars()
    if file_key in stars:
        stars.remove(file_key)
        save_stars(stars)
        print(f"✅ 已取消标记: {file_key}")
    else:
        print(f"⚠️ 未找到标记: {file_key}")

def list_stars():
    """列出重要记忆"""
    stars = load_stars()
    if not stars:
        print("暂无重要记忆")
        return
    
    index = load_index()
    
    print("=== 重要记忆 ⭐ ===\n")
    for file_key in sorted(stars):
        # 查找记忆内容
        preview = ""
        for tag, items in index.items():
            for item in items:
                if item["file"] == file_key:
                    preview = item.get("preview", "")
                    break
            if preview:
                break
        print(f"⭐ {file_key}")
        if preview:
            print(f"   {preview}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Memory Indexer - 短期记忆关键词索引工具")
    parser.add_argument("command", help="子命令: add, search, list, sync, status, keywords, cleanup, related, timeline, recall, summary, star, stars, vector")
    parser.add_argument("args", nargs="*", help="参数")
    parser.add_argument("--watch", "-w", action="store_true", help="监控模式（增量同步）")
    parser.add_argument("--and", dest="use_and", action="store_true", help="AND 模式搜索（所有关键词都匹配）")
    parser.add_argument("--keywords", "-k", type=int, default=10, help="关键词提取数量（默认10）")
    # 搜索模式参数
    parser.add_argument("--keyword", dest="use_keyword", action="store_true", help="只用关键词搜索")
    parser.add_argument("--semantic", dest="use_semantic", action="store_true", help="只用向量语义搜索")
    parser.add_argument("--raw", dest="use_raw", action="store_true", help="只用原文搜索")
    parser.add_argument("--hybrid", dest="use_hybrid", action="store_true", help="三级级联搜索（默认）")
    parser.add_argument("--top-k", type=int, default=10, help="返回结果数量（默认10）")
    parser.add_argument("--embed", dest="embed", action="store_true", help="add 命令：同时生成向量")
    
    args = parser.parse_args()
    command = args.command
    
    if command == "add":
        # 添加记忆: python3 memory-indexer.py add "记忆内容" [标签1 标签2 ...] [--keywords 20] [--embed]
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py add \"记忆内容\" [标签1 标签2 ...] [--keywords 20] [--embed]")
            print("示例: python3 memory-indexer.py add \"今天学习了 Python\"")
            print("     python3 memory-indexer.py add \"项目进度\" 重要 里程碑 --keywords 15")
            print("     python3 memory-indexer.py add \"今天天气很好\" --embed  # 同时生成向量")
            sys.exit(1)
        content = args.args[0]
        tags = args.args[1:] if len(args.args) > 1 else []
        add_memory(content, tags, topk=args.keywords)
        
        # 如果指定了 --embed 参数，同时生成向量
        if hasattr(args, 'embed') and args.embed:
            from embedding import add_vector
            import time
            now = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{now}.md"
            add_vector(filename, content, content[:200], now)
    
    elif command == "search":
        # 搜索记忆
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py search \"关键词\" [选项]")
            print("示例: python3 memory-indexer.py search Python")
            print("     python3 memory-indexer.py search \"Python 机器学习\" --and")
            print("     python3 memory-indexer.py search \"今天天气\" --semantic  # 向量搜索")
            print("     python3 memory-indexer.py search \"项目\" --raw           # 原文搜索")
            print("     python3 memory-indexer.py search \"学习\"                 # 三级搜索（默认）")
            print("\n选项:")
            print("  --keyword   只用关键词搜索")
            print("  --semantic  只用向量语义搜索")
            print("  --raw       只用原文搜索")
            print("  --hybrid    三级级联搜索（默认）")
            print("  --and       AND 模式（所有关键词都匹配）")
            print("  --top-k     返回结果数量（默认10）")
            sys.exit(1)
        
        query = args.args[0]
        
        # 确定搜索模式
        if args.use_keyword:
            # 只用关键词
            mode = "and" if args.use_and else "or"
            search_memories(query, mode=mode)
        elif args.use_semantic:
            # 只用向量语义搜索
            if EMBEDDING_AVAILABLE:
                results = search_semantic(query, top_k=args.top_k)
                display_search_results(results, query, show_layer=True)
            else:
                print("错误: 向量搜索未启用（embedding 模块不可用）")
                print("提示: 请确保 embedding.py 存在且 MINIMAX_API_KEY 已配置")
        elif args.use_raw:
            # 只用原文搜索
            results = search_raw_memories(query, top_k=args.top_k)
            display_search_results(results, query, show_layer=True)
        else:
            # 三级级联搜索（默认）
            results = search_hybrid(query, top_k=args.top_k)
            display_search_results(results, query, show_layer=True)
    
    elif command == "list":
        list_memories()
    
    elif command == "sync":
        if args.watch:
            print("监控模式: 每 60 秒检查一次新文件...")
            import time
            while True:
                sync_external_memories()
                time.sleep(60)
        else:
            sync_external_memories()
    
    elif command == "status":
        show_status()
    
    elif command == "cleanup":
        cleanup_index()
    
    elif command == "related":
        find_related_memories()
    
    elif command == "timeline":
        show_timeline()
    
    elif command == "recall":
        # 主动提醒: python3 memory-indexer.py recall "关键词"
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py recall \"关键词\"")
            print("示例: python3 memory-indexer.py recall Python")
            sys.exit(1)
        recall(args.args[0])
    
    elif command == "summary":
        generate_summary()
    
    elif command == "star":
        # 标记重要记忆: python3 memory-indexer.py star <文件名>
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py star <文件名>")
            print("示例: python3 memory-indexer.py star 20260313_021414")
            print("提示: 使用 list 命令查看所有记忆文件名")
            sys.exit(1)
        star_memory(args.args[0])
    
    elif command == "stars":
        list_stars()
    
    elif command == "unstar":
        # 取消标记: python3 memory-indexer.py unstar <文件名>
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py unstar <文件名>")
            print("示例: python3 memory-indexer.py unstar 20260313_021414")
            sys.exit(1)
        unstar_memory(args.args[0])
    
    elif command == "keywords":
        # 调试用：显示文本的关键词
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py keywords \"文本\"")
            print("示例: python3 memory-indexer.py keywords \"今天学习了 Python 编程\"")
            print("提示: 此命令用于调试关键词提取功能")
            sys.exit(1)
            sys.exit(1)
        keywords = extract_keywords(args.args[0])
        print("关键词:", ", ".join(keywords))
    
    elif command == "vector":
        # 向量管理命令
        if not EMBEDDING_AVAILABLE:
            print("错误: embedding 模块不可用")
            print("提示: 请确保 embedding.py 存在")
            sys.exit(1)
        
        if len(args.args) < 1:
            print("用法: python3 memory-indexer.py vector <子命令>")
            print("子命令:")
            print("  status              查看向量索引状态")
            print("  test                测试向量生成")
            print("  reindex             批量重新生成向量")
            print("  reindex --memory-dir <路径>  从指定目录生成向量")
            sys.exit(1)
        
        vector_subcommand = args.args[0]
        
        if vector_subcommand == "status":
            status = get_vector_status()
            print(f"向量索引: {status['total']} 条")
            if status.get('files'):
                print(f"示例文件: {status['files'][:5]}")
        
        elif vector_subcommand == "test":
            print("测试向量生成...")
            vec = get_embedding("今天天气很好")
            if vec:
                print(f"✓ 向量生成成功，维度: {len(vec)}")
                print(f"前5维: {vec[:5]}")
            else:
                print("✗ 向量生成失败")
                print("提示: 请检查 MINIMAX_API_KEY 环境变量")
        
        elif vector_subcommand == "reindex":
            memory_dir = args.memory_dir if hasattr(args, 'memory_dir') and args.memory_dir else EXTERNAL_MEMORY_DIR
            print(f"从 {memory_dir} 重新生成向量...")
            
            files = []
            contents = []
            for f in Path(memory_dir).glob("*.md"):
                files.append(f.name)
                try:
                    contents.append(f.read_text(encoding="utf-8")[:1000])
                except:
                    contents.append("")
            
            print(f"找到 {len(files)} 个记忆文件")
            from embedding import add_vectors_batch
            add_vectors_batch(files, contents)
        
        else:
            print(f"未知子命令: {vector_subcommand}")
            sys.exit(1)
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()


# ============ 可导入 API（供其他脚本调用）============

def search(keyword: str, mode: str = "or") -> list:
    """
    搜索记忆（可导入函数）
    
    Args:
        keyword: 搜索关键词
        mode: "and" 或 "or"
    
    Returns:
        list: 匹配的记忆列表
    
    Example:
        from memory_indexer import search
        results = search("语音识别")
        for r in results:
            print(r['file'], r['preview'])
    """
    index = load_index()
    keyword = keyword.lower()
    
    if keyword not in index:
        return []
    
    return index.get(keyword, [])


def get_status() -> dict:
    """
    获取索引状态（可导入函数）
    
    Returns:
        dict: 包含关键词数、文件数等信息的字典
    """
    index = load_index()
    state = load_sync_state()
    
    file_count = set()
    for items in index.values():
        for item in items:
            file_count.add(item["file"])
    
    return {
        "keyword_count": len(index),
        "file_count": len(file_count),
        "synced_files": len(state.get("synced_files", {}))
    }


def recall(keyword: str) -> list:
    """
    主动提醒（可导入函数）
    
    Args:
        keyword: 关键词
    
    Returns:
        list: 相关记忆列表
    """
    return search(keyword)

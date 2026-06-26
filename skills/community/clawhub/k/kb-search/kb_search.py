#!/usr/bin/env python3
"""
kb-search Skill - Knowledge Base Search
搜索 OpenClaw 知识库文档

用法：
- /kb-search <query> - 搜索关键词
- /kb-search <query> --type=error - 搜索错误相关文档
- /kb-search <query> --limit=5 - 限制结果数量
"""

import os
import json
import glob
import re
from typing import List, Dict, Any, Optional

# 知识库路径
KB_PATH = os.path.expanduser("~/.openclaw/workspace/docs.openclaw.ai/")

def search_knowledge_base(
    query: str, 
    doc_type: str = "all",
    limit: int = 10
) -> Dict[str, Any]:
    """
    搜索知识库
    
    Args:
        query: 搜索关键词
        doc_type: 文档类型 (error, config, guide, all)
        limit: 限制结果数量
    
    Returns:
        搜索结果
    """
    results = []
    
    # 遍历所有文档
    for filepath in glob.glob(os.path.join(KB_PATH, "**/*.md"), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 简单关键词匹配
        if query.lower() in content.lower():
            filename = os.path.basename(filepath)
            
            # 提取摘要（关键词附近的内容）
            excerpt = extract_excerpt(content, query, max_length=200)
            
            results.append({
                "file": filename,
                "path": filepath,
                "type": detect_doc_type(filename),
                "relevance": content.lower().count(query.lower()),
                "excerpt": excerpt
            })
    
    # 按相关性排序
    results.sort(key=lambda x: x["relevance"], reverse=True)
    
    # 过滤类型
    if doc_type != "all":
        results = [r for r in results if r["type"] == doc_type]
    
    return {
        "query": query,
        "type": doc_type,
        "total": len(results),
        "results": results[:limit]
    }

def extract_excerpt(content: str, query: str, max_length: int = 200) -> str:
    """提取关键词附近的摘要"""
    query_lower = query.lower()
    content_lower = content.lower()
    
    # 找到关键词位置
    pos = content_lower.find(query_lower)
    if pos == -1:
        return content[:max_length] + "..."
    
    # 提取附近内容
    start = max(0, pos - 100)
    end = min(len(content), pos + len(query) + 100)
    
    excerpt = content[start:end].strip()
    
    # 高亮关键词
    excerpt = re.sub(
        f'({re.escape(query)})', 
        r'**\1**', 
        excerpt, 
        flags=re.IGNORECASE
    )
    
    if len(excerpt) > max_length:
        excerpt = "..." + excerpt[-max_length+3:]
    
    return excerpt

def detect_doc_type(filename: str) -> str:
    """检测文档类型"""
    filename_lower = filename.lower()
    
    if any(kw in filename_lower for kw in ["error", "troubleshoot", "fix"]):
        return "error"
    elif any(kw in filename_lower for kw in ["config", "setting"]):
        return "config"
    elif any(kw in filename_lower for kw in ["install", "setup", "deploy"]):
        return "guide"
    elif any(kw in filename_lower for kw in ["cli", "command"]):
        return "cli"
    elif any(kw in filename_lower for kw in ["channel", "telegram", "whatsapp", "discord"]):
        return "channel"
    else:
        return "general"

def format_results(results: Dict[str, Any]) -> str:
    """格式化搜索结果"""
    output = []
    output.append(f"\n🔍 搜索: **{results['query']}**")
    output.append(f"📚 类型: {results['type']}")
    output.append(f"📊 结果: {results['total']} 篇文档\n")
    
    for i, r in enumerate(results["results"], 1):
        icon = get_type_icon(r["type"])
        output.append(f"{i}. {icon} **{r['file']}**")
        output.append(f"   📁 {r['path']}")
        output.append(f"   📝 {r['excerpt']}")
        output.append("")
    
    return "\n".join(output)

def get_type_icon(doc_type: str) -> str:
    """获取类型图标"""
    icons = {
        "error": "❌",
        "config": "⚙️",
        "guide": "📖",
        "cli": "💻",
        "channel": "📱",
        "general": "📄"
    }
    return icons.get(doc_type, "📄")

def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    query = sys.argv[1]
    doc_type = "all"
    limit = 10
    
    # 解析参数
    for arg in sys.argv[2:]:
        if arg.startswith("--type="):
            doc_type = arg.split("=")[1]
        elif arg.startswith("--limit="):
            try:
                limit = int(arg.split("=")[1])
            except ValueError:
                pass
    
    results = search_knowledge_base(query, doc_type, limit)
    print(format_results(results))
    
    return results

if __name__ == "__main__":
    main()

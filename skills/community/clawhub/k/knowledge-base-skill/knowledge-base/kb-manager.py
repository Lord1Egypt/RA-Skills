#!/usr/bin/env python3
"""
多业务知识库管理器
支持按业务类型分隔存储、查询、管理问答
"""

import json
import os
import hashlib
from datetime import datetime
from difflib import SequenceMatcher
from typing import Optional, List, Dict, Any
from pathlib import Path

KB_ROOT = os.path.dirname(__file__)
BUSINESSES_FILE = os.path.join(KB_ROOT, "businesses.json")
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# ============ 业务管理 ============

def load_businesses() -> Dict[str, Any]:
    """加载业务索引"""
    if not os.path.exists(BUSINESSES_FILE):
        return {"meta": {"created": datetime.now().isoformat()}, "businesses": {}}
    with open(BUSINESSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_businesses(data: Dict[str, Any]) -> None:
    """保存业务索引"""
    data["meta"]["updated"] = datetime.now().isoformat()
    with open(BUSINESSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_business_dir(business_name: str) -> str:
    """获取业务数据库目录"""
    return os.path.join(KB_ROOT, business_name)

def ensure_business(business_name: str) -> Dict[str, Any]:
    """确保业务存在，不存在则创建"""
    businesses = load_businesses()
    
    if business_name not in businesses["businesses"]:
        # 创建新业务
        business_dir = get_business_dir(business_name)
        os.makedirs(business_dir, exist_ok=True)
        
        # 初始化数据库
        db_path = os.path.join(business_dir, "qa-database.json")
        db = {
            "meta": {
                "business": business_name,
                "created": datetime.now().isoformat(),
                "page": 1
            },
            "answered": [],
            "pending": []
        }
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        businesses["businesses"][business_name] = {
            "created": datetime.now().isoformat(),
            "dir": business_name,
            "description": ""
        }
        save_businesses(businesses)
        
        return {"status": "created", "message": f"已创建业务「{business_name}」", "business": business_name}
    
    return {"status": "exists", "message": f"业务「{business_name}」已存在", "business": business_name}

def list_businesses() -> List[Dict[str, Any]]:
    """列出所有业务及统计信息"""
    businesses = load_businesses()
    result = []
    
    for name, info in businesses["businesses"].items():
        business_dir = get_business_dir(name)
        db_file = os.path.join(business_dir, "qa-database.json")
        
        total_answered = 0
        total_pending = 0
        pages = 0
        
        if os.path.exists(business_dir):
            for f in os.listdir(business_dir):
                if f.startswith("qa-database") and f.endswith(".json"):
                    pages += 1
                    try:
                        with open(os.path.join(business_dir, f), "r", encoding="utf-8") as fp:
                            db = json.load(fp)
                            total_answered += len(db.get("answered", []))
                            total_pending += len(db.get("pending", []))
                    except:
                        pass
        
        result.append({
            "name": name,
            "created": info.get("created", "unknown"),
            "description": info.get("description", ""),
            "answered": total_answered,
            "pending": total_pending,
            "pages": pages
        })
    
    return sorted(result, key=lambda x: x["answered"], reverse=True)

def delete_business(business_name: str) -> Dict[str, Any]:
    """删除业务"""
    businesses = load_businesses()
    
    if business_name not in businesses["businesses"]:
        return {"status": "not_found", "message": f"业务「{business_name}」不存在"}
    
    business_dir = get_business_dir(business_name)
    
    # 删除目录
    import shutil
    if os.path.exists(business_dir):
        shutil.rmtree(business_dir)
    
    # 更新索引
    del businesses["businesses"][business_name]
    save_businesses(businesses)
    
    return {"status": "deleted", "message": f"已删除业务「{business_name}」"}

# ============ 数据库操作 ============

def get_db_files(business_name: str) -> List[str]:
    """获取业务的所有数据库文件"""
    business_dir = get_business_dir(business_name)
    if not os.path.exists(business_dir):
        return []
    
    files = []
    for f in os.listdir(business_dir):
        if f.startswith("qa-database") and f.endswith(".json"):
            files.append(f)
    return sorted(files)

def get_current_db_path(business_name: str) -> str:
    """获取当前写入的数据库文件路径"""
    files = get_db_files(business_name)
    business_dir = get_business_dir(business_name)
    
    if not files:
        return os.path.join(business_dir, "qa-database.json")
    
    last_file = os.path.join(business_dir, files[-1])
    if os.path.exists(last_file) and os.path.getsize(last_file) >= MAX_FILE_SIZE:
        page_num = len(files) + 1
        return os.path.join(business_dir, f"qa-database-page{page_num}.json")
    
    return last_file

def load_db(business_name: str, page: int = -1) -> Dict[str, Any]:
    """加载业务数据库"""
    files = get_db_files(business_name)
    business_dir = get_business_dir(business_name)
    
    if not files:
        return {
            "meta": {"business": business_name, "created": datetime.now().isoformat(), "page": 1},
            "answered": [],
            "pending": []
        }
    
    if page == -1:
        db_path = os.path.join(business_dir, files[-1])
    else:
        db_path = os.path.join(business_dir, f"qa-database-page{page}.json" if page > 1 else "qa-database.json")
    
    if not os.path.exists(db_path):
        return {
            "meta": {"business": business_name, "page": page},
            "answered": [],
            "pending": []
        }
    
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(business_name: str, db: Dict[str, Any], page: int = -1) -> None:
    """保存业务数据库"""
    if page == -1:
        db_path = get_current_db_path(business_name)
    else:
        business_dir = get_business_dir(business_name)
        db_path = os.path.join(business_dir, f"qa-database-page{page}.json" if page > 1 else "qa-database.json")
    
    if "meta" not in db:
        db["meta"] = {}
    db["meta"]["business"] = business_name
    db["meta"]["updated"] = datetime.now().isoformat()
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def load_db_from_file(business_name: str, filename: str) -> Dict[str, Any]:
    """从指定文件加载数据库"""
    path = os.path.join(get_business_dir(business_name), filename)
    if not os.path.exists(path):
        return {"meta": {}, "answered": [], "pending": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ============ 问答操作 ============

def similarity(a: str, b: str) -> float:
    """计算文本相似度"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def add_answer(business_name: str, question: str, answer: str, tags: List[str] = None, attachments: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """添加问答对，支持图片附件"""
    # 确保业务存在
    ensure_business(business_name)
    
    # 检查是否已存在类似问题（在当前业务的所有页面中）
    for page_file in get_db_files(business_name):
        page_db = load_db_from_file(business_name, page_file)
        for qa in page_db["answered"]:
            if similarity(question, qa["question"]) > 0.9:
                return {
                    "status": "exists",
                    "message": f"已存在类似问题",
                    "data": qa,
                    "business": business_name
                }
    
    # 加载当前数据库
    db = load_db(business_name)
    
    # 从 pending 中移除
    db["pending"] = [p for p in db["pending"] if similarity(p["question"], question) < 0.9]
    
    entry = {
        "id": hashlib.md5(f"{question}{datetime.now()}".encode()).hexdigest()[:12],
        "question": question,
        "answer": answer,
        "tags": tags or [],
        "attachments": attachments or [],
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "usage_count": 0
    }
    
    db["answered"].append(entry)
    save_db(business_name, db)
    
    # 获取文件信息
    current_path = get_current_db_path(business_name)
    file_size = os.path.getsize(current_path) if os.path.exists(current_path) else 0
    page_info = f" (page {db['meta'].get('page', 1)})" if db.get('meta', {}).get('page', 1) > 1 else ""
    
    return {
        "status": "added",
        "message": f"问答已添加{page_info}",
        "data": entry,
        "business": business_name,
        "file_size_mb": round(file_size / 1024 / 1024, 2),
        "current_page": db['meta'].get('page', 1)
    }

def add_pending(business_name: str, question: str, source: str = "user") -> Dict[str, Any]:
    """添加未回答问题"""
    ensure_business(business_name)
    db = load_db(business_name)
    
    for p in db["pending"]:
        if similarity(question, p["question"]) > 0.95:
            return {"status": "exists", "message": "问题已在待回答列表中", "data": p, "business": business_name}
    
    entry = {
        "id": hashlib.md5(f"{question}{datetime.now()}".encode()).hexdigest()[:12],
        "question": question,
        "source": source,
        "created": datetime.now().isoformat(),
        "asked": False,
        "asked_at": None
    }
    
    db["pending"].append(entry)
    save_db(business_name, db)
    
    return {"status": "added", "message": "问题已记录，等待补充答案", "data": entry, "business": business_name}

def search_answer(business_name: str, question: str, threshold: float = 0.6, cross_business: bool = False, search_attachments: bool = False) -> Optional[Dict[str, Any]]:
    """搜索答案，支持搜索图片 OCR 文字"""
    best_match = None
    best_score = threshold
    best_page = 1
    best_business = business_name
    
    if cross_business:
        # 跨所有业务搜索
        businesses = list_businesses()
        for biz in businesses:
            result = search_answer(biz["name"], question, threshold, cross_business=False, search_attachments=search_attachments)
            if result and result.get("similarity", 0) > best_score:
                best_score = result["similarity"]
                best_match = result
                best_business = biz["name"]
        
        if best_match:
            best_match["business"] = best_business
            return best_match
        return None
    else:
        # 只在当前业务搜索
        for page_file in get_db_files(business_name):
            page_db = load_db_from_file(business_name, page_file)
            for qa in page_db["answered"]:
                # 匹配问题文本
                score = similarity(question, qa["question"])
                
                # 如果启用附件搜索，也搜索图片 OCR 文字
                if search_attachments and qa.get("attachments"):
                    for att in qa["attachments"]:
                        if att.get("ocr_text"):
                            ocr_score = similarity(question, att["ocr_text"])
                            if ocr_score > score:
                                score = ocr_score
                
                if score > best_score:
                    best_score = score
                    best_match = qa
                    best_page = page_db['meta'].get('page', 1)
                    best_business = business_name
        
        if best_match:
            best_match["usage_count"] = best_match.get("usage_count", 0) + 1
            best_match["last_used"] = datetime.now().isoformat()
            
            # 更新所在页面
            page_path = os.path.join(get_business_dir(business_name), page_file)
            with open(page_path, "w", encoding="utf-8") as f:
                json.dump(page_db, f, ensure_ascii=False, indent=2)
            
            return {
                "question": best_match["question"],
                "answer": best_match["answer"],
                "similarity": round(best_score, 2),
                "page": best_page,
                "business": best_business,
                "attachments": best_match.get("attachments", [])
            }
        
        return None

def get_stats(business_name: str) -> Dict[str, Any]:
    """获取业务统计信息"""
    total_answered = 0
    total_pending = 0
    pages = []
    
    for page_file in get_db_files(business_name):
        page_db = load_db_from_file(business_name, page_file)
        page_num = page_db['meta'].get('page', 1)
        answered = len(page_db.get('answered', []))
        pending = len(page_db.get('pending', []))
        total_answered += answered
        total_pending += pending
        
        page_path = os.path.join(get_business_dir(business_name), page_file)
        file_size = os.path.getsize(page_path) if os.path.exists(page_path) else 0
        
        pages.append({
            "page": page_num,
            "file": page_file,
            "answered": answered,
            "pending": pending,
            "size_mb": round(file_size / 1024 / 1024, 2)
        })
    
    return {
        "business": business_name,
        "total_answered": total_answered,
        "total_pending": total_pending,
        "total_pages": len(pages),
        "pages": pages
    }

def get_pending(business_name: str) -> List[Dict[str, Any]]:
    """获取待回答问题"""
    db = load_db(business_name)
    return db.get("pending", [])

def mark_answered(business_name: str, question_id: str, answer: str) -> Dict[str, Any]:
    """将待回答问题标记为已回答"""
    db = load_db(business_name)
    
    pending = None
    for i, p in enumerate(db["pending"]):
        if p["id"] == question_id:
            pending = db["pending"].pop(i)
            break
    
    if not pending:
        return {"status": "not_found", "message": "未找到该问题", "business": business_name}
    
    entry = {
        "id": pending["id"],
        "question": pending["question"],
        "answer": answer,
        "tags": [],
        "created": pending["created"],
        "updated": datetime.now().isoformat(),
        "usage_count": 0
    }
    
    db["answered"].append(entry)
    save_db(business_name, db)
    
    return {"status": "moved", "message": "问题已标记为已回答", "data": entry, "business": business_name}

def export_markdown(business_name: str, output_path: str = None) -> str:
    """导出为 Markdown"""
    all_answered = []
    all_pending = []
    
    for page_file in get_db_files(business_name):
        page_db = load_db_from_file(business_name, page_file)
        all_answered.extend(page_db.get('answered', []))
        all_pending.extend(page_db.get('pending', []))
    
    md = [f"# {business_name} - 问答知识库", ""]
    md.append(f"_最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md.append("")
    md.append(f"**已回答**: {len(all_answered)} | **待回答**: {len(all_pending)} | **页数**: {len(get_db_files(business_name))}")
    md.append("")
    
    if all_answered:
        md.append("## ✅ 已回答问题")
        md.append("")
        for i, qa in enumerate(all_answered, 1):
            md.append(f"### Q{i}. {qa['question']}")
            md.append("")
            md.append(f"**A**: {qa['answer']}")
            md.append("")
            tags = qa.get('tags', [])
            usage = qa.get('usage_count', 0)
            md.append(f"_标签_: {', '.join(tags) if tags else '无'} | _使用次数_: {usage}")
            md.append("")
            md.append("---")
            md.append("")
    
    if all_pending:
        md.append("## ⏳ 待回答问题")
        md.append("")
        for i, p in enumerate(all_pending, 1):
            md.append(f"{i}. **{p['question']}** (_{p['created'][:10]}_)")
        md.append("")
    
    content = "\n".join(md)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    return content

# ============ 命令行入口 ============

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("多业务知识库管理器")
        print("")
        print("用法：python kb-manager.py <命令> [参数]")
        print("")
        print("业务管理:")
        print("  business list              - 列出所有业务")
        print("  business new <业务名>       - 创建新业务")
        print("  business delete <业务名>    - 删除业务")
        print("")
        print("问答操作:")
        print("  add <业务名> <问题> <答案>  - 添加问答")
        print("  pending <业务名> <问题>     - 添加待回答")
        print("  search <业务名> <问题>      - 搜索答案")
        print("  stats <业务名>             - 查看统计")
        print("  list <业务名>              - 快速查看")
        print("  export <业务名> [文件]      - 导出文档")
        print("")
        print("快捷格式:")
        print('  KB:业务名 Q:问题 A:答案')
        print('  KB:业务名 问题')
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "business":
        if len(sys.argv) < 3:
            print("用法：business <list|new|delete> [业务名]")
            sys.exit(1)
        subcmd = sys.argv[2]
        if subcmd == "list":
            businesses = list_businesses()
            print(f"{'业务名称':<20} {'已回答':<10} {'待回答':<10} {'页数':<6}")
            print("-" * 50)
            for b in businesses:
                print(f"{b['name']:<20} {b['answered']:<10} {b['pending']:<10} {b['pages']:<6}")
        elif subcmd == "new" and len(sys.argv) >= 4:
            result = ensure_business(sys.argv[3])
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif subcmd == "delete" and len(sys.argv) >= 4:
            result = delete_business(sys.argv[3])
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "add" and len(sys.argv) >= 5:
        result = add_answer(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "pending" and len(sys.argv) >= 4:
        result = add_pending(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "search" and len(sys.argv) >= 4:
        result = search_answer(sys.argv[2], sys.argv[3])
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"status": "not_found", "message": "未找到匹配的答案"}, ensure_ascii=False, indent=2))
    
    elif cmd == "stats" and len(sys.argv) >= 3:
        result = get_stats(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "list" and len(sys.argv) >= 3:
        stats = get_stats(sys.argv[2])
        print(f"业务：{sys.argv[2]}")
        print(f"已回答：{stats['total_answered']} 条")
        print(f"待回答：{stats['total_pending']} 条")
        print(f"页数：{stats['total_pages']} 页")
    
    elif cmd == "export" and len(sys.argv) >= 3:
        output = sys.argv[3] if len(sys.argv) >= 4 else os.path.join(KB_ROOT, f"{sys.argv[2]}-knowledge-base.md")
        export_markdown(sys.argv[2], output)
        print(f"已导出到 {output}")
    
    elif cmd == "KB" and len(sys.argv) >= 3:
        # 解析快捷格式 KB:业务名 Q:问题 A:答案
        args = " ".join(sys.argv[2:])
        if "Q:" in args and "A:" in args:
            parts = args.split("Q:")
            business = parts[0].strip()
            rest = "Q:".join(parts[1:])
            if "A:" in rest:
                qa_parts = rest.split("A:")
                question = qa_parts[0].strip().lstrip("Q:").strip()
                answer = "A:".join(qa_parts[1:]).strip()
                result = add_answer(business, question, answer)
                print(json.dumps(result, ensure_ascii=False, indent=2))
        elif "list" in args:
            business = args.replace("list", "").strip()
            stats = get_stats(business)
            print(f"业务：{business}")
            print(f"已回答：{stats['total_answered']} 条")
            print(f"待回答：{stats['total_pending']} 条")
        else:
            # 查询
            business = sys.argv[2]
            question = " ".join(sys.argv[3:])
            result = search_answer(business, question)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"status": "not_found", "message": "未找到匹配的答案"}, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令：{cmd}")

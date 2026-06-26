#!/usr/bin/env python3
"""
项目事项归档检查脚本 V4
检查项目事项管理表中的已完成事项，自动生成知识文档
"""
import json
import os
import subprocess
import re
from datetime import datetime

# 配置
BASE_ID = "QOG9lyrgJP3Oo757S9wn4AyZVzN67Mw4"
TABLE_ID = "atLkTeV"

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = SCRIPT_DIR
STATE_FILE = os.path.join(WORKSPACE, "archived-items.json")
DOCS_DIR = os.path.join(WORKSPACE, "docs")

# 基本字段（安全）
BASIC_FIELDS = ["1BYpQDD", "XVSa9uv", "Do7qrDK", "czhTMHj", "nbrCfuX", "4Dlwg5m", "DLTHGDL", "yW60hN5", "MfriwJQ", "4QTOoZ8"]
# 详细字段（可能有编码问题）
DETAIL_FIELDS = ["rUZ49MP", "5rdq28c", "jMRpMlp", "0zJUI0T"]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def run_mcporter_json(args_dict):
    """运行 mcporter 命令并解析 JSON"""
    try:
        args_json = json.dumps(args_dict)
        cmd = ['mcporter', 'call', 'dingtalk-ai-table', 'query_records', '--args', args_json, '--output', 'json']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
    except:
        pass
    return None

def get_completed_record_ids(view_id):
    """获取已完成事项的 recordId 列表"""
    args = {
        "baseId": BASE_ID,
        "tableId": TABLE_ID,
        "viewId": view_id,
        "limit": 50,
        "fieldIds": ["recordId"]
    }
    result = run_mcporter_json(args)
    if result:
        records = result.get('records', [])
        return [r.get('recordId') for r in records if r.get('recordId')]
    return []

def get_record_basic_info(record_ids):
    """获取记录的基本信息"""
    if not record_ids:
        return []
    
    results = []
    for rid in record_ids:
        args = {
            "baseId": BASE_ID,
            "tableId": TABLE_ID,
            "recordIds": [rid],
            "fieldIds": BASIC_FIELDS
        }
        result = run_mcporter_json(args)
        if result and result.get('records'):
            results.extend(result['records'])
    
    return results

def get_record_detail(record_id, field_id):
    """获取单条记录的单个字段详情"""
    args = {
        "baseId": BASE_ID,
        "tableId": TABLE_ID,
        "recordIds": [record_id],
        "fieldIds": [field_id]
    }
    result = run_mcporter_json(args)
    if result and result.get('records'):
        cells = result['records'][0].get('cells', {})
        value = cells.get(field_id, "")
        if isinstance(value, dict):
            return value.get('name', "")
        elif isinstance(value, list):
            names = []
            for v in value:
                if isinstance(v, dict):
                    name = v.get('name', '')
                    if not name:
                        name = v.get('userId', str(v))
                    names.append(name)
            return ", ".join([n for n in names if n]) if names else ""
        return str(value) if value else ""
    return ""

def get_cell_value(cells, field_id, default=""):
    """获取单元格值"""
    value = cells.get(field_id, default)
    if isinstance(value, dict):
        return value.get('name', default)
    elif isinstance(value, list):
        names = []
        for v in value:
            if isinstance(v, dict):
                name = v.get('name', '')
                if not name:
                    name = v.get('userId', str(v))
                names.append(name)
        return ", ".join([n for n in names if n]) if names else default
    return str(value) if value else default

def generate_doc_filename(item_type, title, record_id):
    """生成文档文件名"""
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:30]
    timestamp = datetime.now().strftime('%Y%m%d')
    return f"{item_type}_{safe_title}_{record_id}_{timestamp}.md"

def generate_problem_report(cells, record_id):
    """生成问题分析报告"""
    title = get_cell_value(cells, "1BYpQDD", "未命名问题")
    module = get_cell_value(cells, "Do7qrDK")
    urgency = get_cell_value(cells, "nbrCfuX")
    handler = get_cell_value(cells, "DLTHGDL")
    feedback_time = get_cell_value(cells, "yW60hN5")
    start_time = get_cell_value(cells, "MfriwJQ")
    end_time = get_cell_value(cells, "4QTOoZ8")
    project = get_cell_value(cells, "czhTMHj")
    tag = get_cell_value(cells, "4Dlwg5m")
    
    # 获取详细字段
    detail = get_record_detail(record_id, "rUZ49MP")
    solution = get_record_detail(record_id, "5rdq28c")
    process = get_record_detail(record_id, "jMRpMlp")
    output = get_record_detail(record_id, "0zJUI0T")
    
    doc = f"""# 问题分析报告：{title}

## 基本信息

| 字段 | 值 |
|------|-----|
| 项目 | {project} |
| 系统模块 | {module} |
| 问题标签 | {tag} |
| 紧急程度 | {urgency} |
| 负责人 | {handler} |
| 反馈时间 | {feedback_time} |
| 开始时间 | {start_time} |
| 结束时间 | {end_time} |
| 记录ID | {record_id} |

## 问题描述

{detail or '无'}

## 处理过程

{process or '无'}

## 解决方案

{solution or '无'}

## AI 分析与输出

{output or '无'}

---

*本文档由 AI 项目管理系统自动归档生成*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return doc, title

def generate_requirement_doc(cells, record_id):
    """生成需求说明文档"""
    title = get_cell_value(cells, "1BYpQDD", "未命名需求")
    module = get_cell_value(cells, "Do7qrDK")
    project = get_cell_value(cells, "czhTMHj")
    tag = get_cell_value(cells, "4Dlwg5m")
    
    detail = get_record_detail(record_id, "rUZ49MP")
    solution = get_record_detail(record_id, "5rdq28c")
    output = get_record_detail(record_id, "0zJUI0T")
    
    doc = f"""# 需求说明文档：{title}

## 基本信息

| 字段 | 值 |
|------|-----|
| 项目 | {project} |
| 系统模块 | {module} |
| 需求标签 | {tag} |
| 记录ID | {record_id} |

## 需求描述

{detail or '无'}

## 需求内容/输出

{output or '无'}

## 解决方案

{solution or '无'}

---

*本文档由 AI 项目管理系统自动归档生成*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return doc, title

def generate_task_summary(cells, record_id):
    """生成任务总结"""
    title = get_cell_value(cells, "1BYpQDD", "未命名任务")
    module = get_cell_value(cells, "Do7qrDK")
    handler = get_cell_value(cells, "DLTHGDL")
    project = get_cell_value(cells, "czhTMHj")
    
    detail = get_record_detail(record_id, "rUZ49MP")
    solution = get_record_detail(record_id, "5rdq28c")
    
    doc = f"""# 任务总结：{title}

## 基本信息

| 字段 | 值 |
|------|-----|
| 项目 | {project} |
| 系统模块 | {module} |
| 负责人 | {handler} |
| 记录ID | {record_id} |

## 任务描述

{detail or '无'}

## 完成情况

{solution or '无'}

---

*本文档由 AI 项目管理系统自动归档生成*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return doc, title

def process_records(records, archived_ids):
    """处理记录，生成文档"""
    new_docs = []
    
    for record in records:
        record_id = record.get('recordId')
        if record_id in archived_ids:
            print(f"  [跳过] {record_id} 已归档")
            continue
            
        cells = record.get('cells', {})
        item_type = get_cell_value(cells, "XVSa9uv")
        
        if not item_type:
            print(f"  [跳过] {record_id} 无事项类型")
            continue
        
        print(f"  [处理] {item_type}: {record_id}")
        
        # 根据类型生成文档
        if item_type == "问题":
            doc_content, title = generate_problem_report(cells, record_id)
        elif item_type == "需求":
            doc_content, title = generate_requirement_doc(cells, record_id)
        elif item_type == "任务":
            doc_content, title = generate_task_summary(cells, record_id)
        else:
            doc_content, title = generate_problem_report(cells, record_id)
        
        # 保存文档
        filename = generate_doc_filename(item_type, title, record_id)
        filepath = os.path.join(DOCS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        new_docs.append({
            "recordId": record_id,
            "title": title,
            "type": item_type,
            "filename": filename,
            "path": filepath,
            "generatedAt": datetime.now().isoformat()
        })
        
        print(f"  [完成] {title}")
    
    return new_docs

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"lastCheckTime": None, "archivedRecords": [], "baseId": BASE_ID, "tableId": TABLE_ID, "generatedDocs": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def main():
    print("=" * 60)
    print("📋 项目事项归档检查")
    print("=" * 60)
    
    ensure_dir(DOCS_DIR)
    
    # 加载状态
    state = load_state()
    archived_ids = set(state.get("archivedRecords", []))
    generated_docs = state.get("generatedDocs", [])
    
    print(f"已归档记录数: {len(archived_ids)}")
    print(f"已生成文档数: {len(generated_docs)}")
    print()
    
    # 视图 "上周已完成事项" - viewId: dGoortH
    view_id = "dGoortH"
    print(f"正在检查视图: {view_id}")
    
    # 1. 获取已完成事项的 recordId 列表
    record_ids = get_completed_record_ids(view_id)
    
    if not record_ids:
        print("没有找到已完成事项")
        state["lastCheckTime"] = datetime.now().isoformat()
        save_state(state)
        return
    
    print(f"找到 {len(record_ids)} 条已完成事项")
    
    # 2. 过滤掉已归档的
    new_record_ids = [rid for rid in record_ids if rid not in archived_ids]
    if not new_record_ids:
        print("没有新的需要归档的事项")
        state["lastCheckTime"] = datetime.now().isoformat()
        save_state(state)
        return
    
    print(f"新事项: {len(new_record_ids)} 条")
    
    # 3. 获取基本信息
    records = get_record_basic_info(new_record_ids)
    
    if not records:
        print("无法获取记录详情")
        return
    
    print(f"获取到 {len(records)} 条基本信息")
    
    # 4. 生成文档
    new_docs = process_records(records, archived_ids)
    
    # 5. 更新状态
    if new_docs:
        for doc in new_docs:
            archived_ids.add(doc["recordId"])
            generated_docs.append(doc)
        
        state["archivedRecords"] = list(archived_ids)
        state["generatedDocs"] = generated_docs
        state["lastCheckTime"] = datetime.now().isoformat()
        save_state(state)
        
        print()
        print(f"✅ 本次生成 {len(new_docs)} 份知识文档")
    else:
        print("没有新的文档需要生成")
        state["lastCheckTime"] = datetime.now().isoformat()
        save_state(state)
    
    print()
    print(f"📁 文档保存位置: {DOCS_DIR}")

if __name__ == "__main__":
    main()

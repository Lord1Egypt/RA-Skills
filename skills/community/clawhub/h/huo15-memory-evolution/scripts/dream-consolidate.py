#!/usr/bin/env python3
"""
Dream Agent - 记忆文件生成器
根据 LLM 分析结果，创建独立的记忆文件
"""
import json
import os
import sys
from datetime import datetime

def create_memory_files(analysis_file, memory_dir, workspace_dir, today):
    """根据 LLM 分析结果创建记忆文件"""
    
    # 读取分析结果
    try:
        with open(analysis_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading analysis file: {e}")
        return []
    
    created_memories = []
    
    # 获取 memories 列表
    memories = data.get('memories', [])
    if not memories:
        print("No memories to create")
        return []
    
    for memory in memories:
        memory_type = memory.get('type', 'project')
        name = memory.get('name', 'unnamed')
        summary = memory.get('summary', '')
        content = memory.get('content', '')
        
        # 跳过 pending 任务（待办不是记忆）
        if 'pending' in name.lower() or '待办' in name.lower() or 'todo' in name.lower():
            print(f"Skipping pending item: {name}")
            continue
        
        # 清理名称（只保留安全的字符）
        safe_name = ''.join(c for c in name if c.isalnum() or c in '-_')
        
        # 构建文件路径
        type_dir = os.path.join(memory_dir, memory_type)
        os.makedirs(type_dir, exist_ok=True)
        
        filename = f"{safe_name}.md"
        filepath = os.path.join(type_dir, filename)
        
        # 构建记忆文件内容
        content_lines = []
        content_lines.append("---")
        content_lines.append(f"name: {safe_name}")
        content_lines.append(f"type: {memory_type}")
        content_lines.append(f"description: {summary}")
        content_lines.append(f"created: {today}")
        content_lines.append(f"updated: {today}")
        content_lines.append("---")
        content_lines.append("")
        
        # 处理 content（可能是多行）
        if content:
            content_lines.append(content)
        else:
            content_lines.append(f"## {summary}")
            content_lines.append("")
            content_lines.append("## 为什么值得记忆")
            content_lines.append(f"从日志中提炼的重要信息：{summary}")
            content_lines.append("")
            content_lines.append("## 如何应用")
            content_lines.append(f"当涉及 {memory_type} 类型相关工作时参考此记忆")
        
        # 写入文件
        file_content = '\n'.join(content_lines)
        with open(filepath, 'w') as f:
            f.write(file_content)
        
        created_memories.append({
            'type': memory_type,
            'name': safe_name,
            'path': f"memory/{memory_type}/{filename}",
            'summary': summary
        })
        print(f"✅ Created: {memory_type}/{filename}")
    
    return created_memories

def update_memory_index(created_memories, workspace_dir):
    """更新 MEMORY.md 索引"""
    index_file = os.path.join(workspace_dir, 'MEMORY.md')
    
    for memory in created_memories:
        memory_type = memory['type']
        name = memory['name']
        path = memory['path']
        summary = memory['summary']
        
        # 检查是否已在索引中
        with open(index_file, 'r') as f:
            index_content = f.read()
        
        if path in index_content:
            print(f"  ↩ Already in index: {path}")
            continue
        
        # 构建索引条目
        new_entry = f"- [{name}]({path}) — {summary}"
        
        # 找到对应的 section
        section_markers = {
            'user': '## user',
            'feedback': '## feedback', 
            'project': '## project',
            'reference': '## reference'
        }
        
        section = section_markers.get(memory_type)
        if not section:
            continue
        
        # 在 section 后的空行前插入
        lines = index_content.split('\n')
        new_lines = []
        found_section = False
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if not inserted and line.strip() == section:
                found_section = True
            elif found_section and line.strip() == '' and not inserted:
                new_lines.append(f"- [{name}]({path}) — {summary}")
                inserted = True
                found_section = False
        
        # 写回索引
        with open(index_file, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print(f"  ✅ Updated index: {path}")

def main():
    analysis_file = '/tmp/dream-analysis-result.json'
    memory_dir = os.path.expanduser('~/.openclaw/workspace/memory')
    workspace_dir = os.path.expanduser('~/.openclaw/workspace')
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("🚀 Dream Agent - 记忆文件生成器")
    print(f"   日期: {today}")
    print("")
    
    if not os.path.exists(analysis_file):
        print(f"⚠️ Analysis file not found: {analysis_file}")
        sys.exit(1)
    
    # 创建记忆文件
    print("📝 Creating memory files...")
    created = create_memory_files(analysis_file, memory_dir, workspace_dir, today)
    
    if not created:
        print("⚠️ No memories created")
        sys.exit(0)
    
    print("")
    
    # 更新索引
    print("📋 Updating MEMORY.md index...")
    update_memory_index(created, workspace_dir)
    
    print("")
    print(f"✅ Created {len(created)} memories")

if __name__ == '__main__':
    main()

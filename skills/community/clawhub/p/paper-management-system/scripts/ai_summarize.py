#!/usr/bin/env python3
"""
AI智能文献提炼模块

功能：
- 读取新提取全文的文献
- 生成结构化摘要
- 保存到ai_summary字段
- 发送通知（可配置）

配置（config.yaml 或环境变量 PAPERMGR_*）：
- ai.enabled: 是否启用AI提炼
- ai.provider: AI提供商 (openai/anthropic)
- ai.model: 模型名称
- notification.enabled: 是否发送通知
- notification.cmd: 通知命令路径（或 stdout）
"""

import sqlite3
import sys
import os
import re
import subprocess
from pathlib import Path

# Add project directory to path
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from config import get_config

def get_db():
    """获取数据库连接"""
    cfg = get_config()
    return sqlite3.connect(cfg.db_path)

def get_papers_need_summary():
    """获取需要AI提炼的文献"""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    papers = conn.execute("""
        SELECT id, title, authors, doi, year, journal, full_text 
        FROM papers 
        WHERE full_text IS NOT NULL 
        AND (ai_summary IS NULL OR ai_summary = '') 
        AND LENGTH(full_text) > 1000
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return papers

def generate_summary(title, authors, journal, year, full_text):
    """生成结构化中文摘要"""
    summary_parts = []
    
    # 1. 研究背景/目的
    background = extract_section(full_text, 
        ["Background", "OBJECTIVE", "AIM", "PURPOSE", "Introduction", "INTRODUCTION"],
        ["Methods", "METHODS", "Material", "MATERIAL", "方法"])
    if background:
        summary_parts.append(f"📌 **研究背景**: {background[:200]}...")
    
    # 2. 研究方法
    methods = extract_section(full_text,
        ["Methods", "METHODS", "Methodology", "方法", "材料与方法"],
        ["Results", "RESULTS", "Findings", "FINDINGS", "结果"])
    if methods:
        summary_parts.append(f"🔬 **研究方法**: {methods[:200]}...")
    
    # 3. 主要结果
    results = extract_section(full_text,
        ["Results", "RESULTS", "Findings", "FINDINGS", "结果"],
        ["Conclusion", "CONCLUSION", "Discussion", "DISCUSSION", "结论", "讨论"])
    if results:
        summary_parts.append(f"📊 **主要结果**: {results[:300]}...")
    
    # 4. 结论
    conclusion = extract_section(full_text,
        ["Conclusion", "CONCLUSION", "Conclusions", "CONCLUSIONS", "结论"],
        ["References", "REFERENCES", "Acknowledgment", "参考文献"])
    if conclusion:
        summary_parts.append(f"💡 **核心结论**: {conclusion[:200]}...")
    
    # 兜底：使用abstract
    if not summary_parts:
        abstract_match = re.search(r'Abstract[\s:]*(.*?)(?:Keywords|Introduction|$)', 
                                   full_text, re.DOTALL | re.IGNORECASE)
        if abstract_match:
            summary_parts.append(f"📝 **摘要**: {abstract_match.group(1)[:500]}...")
    
    header_lines = ["📄 **文献AI提炼**", ""]
    if title:
        header_lines.append(f"**标题**: {title}")
    if authors:
        header_lines.append(f"**作者**: {authors}")
    if journal:
        header_lines.append(f"**期刊**: {journal}")
    if year:
        header_lines.append(f"**年份**: {year}")
    header_lines.append("")
    
    header = "\n".join(header_lines)
    return header + "\n\n".join(summary_parts)

def extract_section(text, start_keywords, end_keywords):
    """提取特定章节"""
    text = re.sub(r'ARTICLE IN PRESS|ACCEPTED MANUSCRIPT|© The Author\(s\).*?licence', '', text, flags=re.IGNORECASE)
    text = re.sub(r'https?://\S+', '', text)
    
    start_pattern = '|'.join(re.escape(k) for k in start_keywords)
    end_pattern = '|'.join(re.escape(k) for k in end_keywords)
    
    patterns = [
        rf'(?:{start_pattern})[\s:]+\n?(.*?)(?:(?:{end_pattern})|$)',
        rf'(?:{start_pattern})\s*\n\s*\n?(.*?)(?:(?:{end_pattern})|$)',
        rf'\d+\.\s*(?:{start_pattern})[\s:]*\n?(.*?)(?:(?:{end_pattern})|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            section = match.group(1).strip()
            section = re.sub(r'\s+', ' ', section)
            section = re.sub(r'^[\s\W]+', '', section)
            if len(section) > 20:
                return section
    return ""

def save_summary(paper_id, summary):
    """保存AI提炼结果"""
    conn = get_db()
    conn.execute("UPDATE papers SET ai_summary = ? WHERE id = ?", (summary, paper_id))
    conn.commit()
    conn.close()

def send_notification(title, message, notify_cmd):
    """发送通知（适配器模式）"""
    if not notify_cmd or notify_cmd.strip() == "":
        print(f"[NOTIFICATION DISABLED] {title}: {message[:100]}...")
        return True
    
    if notify_cmd.lower() == "stdout":
        print(f"\n{'='*60}")
        print(f"通知: {title}")
        print(f"{'='*60}")
        print(message)
        print(f"{'='*60}\n")
        return True
    
    # 执行外部通知命令
    try:
        cmd = f'{notify_cmd} "{title}" "{message[:1500]}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ 通知已发送")
            return True
        else:
            print(f"✗ 通知失败: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ 通知超时")
        return False
    except Exception as e:
        print(f"✗ 通知异常: {e}")
        return False

def main():
    cfg = get_config()
    
    # 检查是否启用
    if not cfg.ai_enabled:
        print("AI提炼功能未启用（ai.enabled=false）")
        return
    
    papers = get_papers_need_summary()
    
    if not papers:
        print("没有需要提炼的文献")
        return
    
    print(f"发现 {len(papers)} 篇需要AI提炼的文献")
    
    # 获取通知配置
    notify_cmd = cfg.notification_cmd if cfg.notification_enabled else ""
    
    for i, paper in enumerate(papers):
        title_display = paper['title'][:50] if paper['title'] else f"ID:{paper['id']}"
        print(f"\n处理 [{i+1}/{len(papers)}]: {title_display}...")
        
        # 生成摘要
        summary = generate_summary(
            paper['title'],
            paper['authors'],
            paper['journal'],
            paper['year'],
            paper['full_text']
        )
        
        # 保存到数据库
        save_summary(paper['id'], summary)
        print(f"✓ 已保存提炼内容 (ID: {paper['id']})")
        
        # 发送通知（只发送最新的一篇）
        if i == 0 and notify_cmd:
            send_notification("📚 新文献AI提炼", summary, notify_cmd)

if __name__ == "__main__":
    main()

"""
存储模块（增强版）
"""

import os
import re
from datetime import datetime


# =========================
# 🔹 工具函数：清洗文件名
# =========================
def sanitize_filename(name: str, max_length: int = 80) -> str:
    """
    清理文件名非法字符 + 截断长度

    规则：
    - 去除非法字符 <>:"/\\|?*
    - 多空格 -> _
    - 限制长度
    """

    # 去非法字符
    name = re.sub(r'[<>:"/\\|?*]', '', name)

    # 空格 -> _
    name = re.sub(r'\s+', '_', name)

    # 截断长度
    return name[:max_length]


# =========================
# 🔹 主函数
# =========================
def save_paper(paper, summary, config):
    base = os.path.expanduser(config["storage"]["papers_dir"])
    os.makedirs(base, exist_ok=True)

    # =========================
    # 🔹 使用论文发布时间
    # =========================
    year = str(paper.get("year", "unknown"))

    # 如果未来扩展到完整日期，可优先使用 published_date
    published_date = paper.get("published_date", None)

    if published_date:
        # 格式假设：YYYY-MM-DD
        date_str = published_date.replace("-", "")
    else:
        # fallback：只用年份
        date_str = year

    # =========================
    # 🔹 文件名清理
    # =========================
    safe_title = sanitize_filename(paper.get("title", "untitled"))

    filename = f"{date_str}-{safe_title}.md"
    path = os.path.join(base, filename)

    # =========================
    # 🔹 内容构建
    # =========================
    
    # 构建发表状态信息
    pub_info_lines = []
    if paper.get("publication"):
        pub_info_lines.append(f"**发表 venue**: {paper.get('publication', '')}")
    if paper.get("ccf_rank"):
        pub_info_lines.append(f"**CCF 评级**: {paper.get('ccf_rank', '')}")
    if paper.get("is_preprint"):
        pub_info_lines.append("**状态**: 预印本 (preprint)")
    if paper.get("authority_score"):
        pub_info_lines.append(f"**权威度分数**: {paper.get('authority_score', 0.3):.2f}")
    
    pub_info = "\n".join(pub_info_lines) if pub_info_lines else ""
    
    content = f"""# {paper.get('title', 'Unknown Title')}

**作者**: {', '.join(paper.get('authors', ['Unknown']))}  
**来源**: {paper.get('source', 'Unknown')}  
**发布日期**: {paper.get('published_date', paper.get('year', 'Unknown'))}  
**链接**: {paper.get('url', '')}
{pub_info if pub_info else ''}

---

## 中文摘要

### 研究问题
{summary.get('研究问题', '')}

### 方法
{summary.get('方法', '')}

### 主要结论
{summary.get('主要结论', '')}

### 创新点
{summary.get('创新点', '')}

---

## 原文摘要

{paper.get('abstract', '')}
"""

    # =========================
    # 🔹 写文件
    # =========================
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path
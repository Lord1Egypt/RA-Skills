#!/usr/bin/env python3
"""
kb-odoo-export.py — 导出知识库到 Odoo Knowledge

功能：
- 读取 wiki/ 目录下的 Markdown 文件
- 转换为 HTML 并同步到 Odoo Knowledge
- 支持可见性控制（private/workspace/members/department）

用法：
    kb-odoo-export                    # 导出所有
    kb-odoo-export --article odoo-crm  # 导出单个
    kb-odoo-export --dry-run          # 仅预览
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime

try:
    import xmlrpc.client
except ImportError:
    print("❌ 缺少 xmlrpc.client，请安装")
    sys.exit(1)

# 默认配置
DEFAULT_CONFIG = "config.enterprise.json"

def load_config(config_path):
    """加载 Enterprise 配置"""
    if not os.path.exists(config_path):
        return None
    with open(config_path) as f:
        return json.load(f)

def connect_odoo(config):
    """连接 Odoo"""
    odoo = config.get("odoo", {})
    url = odoo.get("url", "")
    db = odoo.get("db", "")
    uid = odoo.get("uid", 0)
    password = odoo.get("password", "")
    
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    
    return models, db, uid, password

def markdown_to_html(markdown_text):
    """简单 Markdown → HTML 转换"""
    # 标题
    markdown_text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
    
    # 粗体和斜体
    markdown_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', markdown_text)
    markdown_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', markdown_text)
    
    # 链接
    markdown_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', markdown_text)
    
    # 列表
    lines = markdown_text.split('\n')
    in_list = False
    result = []
    for line in lines:
        if re.match(r'^[\-\*] (.+)', line):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item = re.sub(r'^[\-\*] (.+)', r'<li>\1</li>', line)
            result.append(item)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    
    # 段落
    markdown_text = '\n'.join(result)
    paragraphs = re.split(r'\n\n+', markdown_text)
    paragraphs = [f"<p>{p.strip()}</p>" if not p.strip().startswith('<') else p for p in paragraphs if p.strip()]
    
    return '\n'.join(paragraphs)

def extract_frontmatter(content):
    """提取 YAML frontmatter"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            fm = {}
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    fm[key.strip()] = val.strip().strip('"')
            return fm, parts[2]
    return {}, content

def user_ids_to_partner_ids(models, db, uid, password, user_ids):
    """将 user IDs 转换为 partner IDs"""
    partner_ids = []
    for user_id in user_ids:
        users = models.execute_kw(db, uid, password,
            'res.users', 'search', [[['id', '=', user_id]]])
        if users:
            user_data = models.execute_kw(db, uid, password,
                'res.users', 'read', [users[0]], {'fields': ['partner_id']})
            if user_data and user_data[0]['partner_id']:
                partner_ids.append(user_data[0]['partner_id'][0])
    return partner_ids

def add_article_members(models, db, uid, password, article_id, partner_ids, permission='write'):
    """为文章添加成员"""
    created = 0
    for partner_id in partner_ids:
        try:
            # 检查是否已存在
            existing = models.execute_kw(db, uid, password,
                'knowledge.article.member', 'search',
                [[['article_id', '=', article_id], ['partner_id', '=', partner_id]]])
            if existing:
                continue  # 已存在，跳过
            
            # 创建成员记录
            models.execute_kw(db, uid, password,
                'knowledge.article.member', 'create', [{
                    'article_id': article_id,
                    'partner_id': partner_id,
                    'permission': permission
                }])
            created += 1
        except Exception as e:
            print(f"       ⚠️  添加成员 {partner_id} 失败: {e}")
    return created

def get_visibility_settings(config, article_name):
    """获取可见性设置"""
    vis = config.get("visibility", {})
    default = vis.get("default", "workspace")
    
    # 收集所有匹配的部门 user_ids
    matched_user_ids = []
    matched_depts = []
    departments = vis.get("departments", {})
    
    # 检查文章名是否匹配部门配置
    for dept, user_ids in departments.items():
        if dept in article_name:
            matched_user_ids.extend(user_ids)
            matched_depts.append(dept)
    
    # 检查 visibility.default 是否为 department:X 格式
    if default.startswith("department:"):
        dept_name = default.split(":", 1)[1]
        if dept_name in departments:
            matched_user_ids.extend(departments[dept_name])
            matched_depts.append(dept_name)
    
    # 去重
    matched_user_ids = list(set(matched_user_ids))
    matched_depts = list(set(matched_depts))
    
    if matched_user_ids:
        return {
            "category": "workspace",
            "matched_user_ids": matched_user_ids,
            "matched_depts": matched_depts
        }
    
    # 默认可见性
    if default == "private":
        return {"category": "private", "matched_user_ids": [], "matched_depts": []}
    else:
        return {"category": "workspace", "matched_user_ids": [], "matched_depts": []}

def export_article(models, db, uid, password, wiki_path, config, dry_run=False):
    """导出单个文章到 Odoo"""
    with open(wiki_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 frontmatter
    fm, body = extract_frontmatter(content)
    
    title = fm.get('title', os.path.basename(wiki_path).replace('.md', ''))
    doc_type = fm.get('type', 'article')
    source = fm.get('source', '')
    
    # 转换为 HTML
    html_body = markdown_to_html(body)
    
    # 获取可见性
    vis_settings = get_visibility_settings(config, title)
    
    print(f"  📄 {title}")
    print(f"     类型: {doc_type}")
    matched_user_ids = vis_settings.get('matched_user_ids', [])
    matched_depts = vis_settings.get('matched_depts', [])
    if matched_depts:
        print(f"     可见性: 部门专属 ({', '.join(matched_depts)}, {len(matched_user_ids)}人)")
    else:
        print(f"     可见性: {vis_settings.get('category', 'workspace').capitalize()}")
    
    if dry_run:
        print(f"     [DRY RUN] 不会实际创建")
        return
    
    # 查找是否已存在同名文章
    existing = models.execute_kw(
        db, uid, password,
        'knowledge.article', 'search',
        [[['name', '=', title]]]
    )
    
    article_vals = {
        'name': title,
        'body': f'<div class="kb-article">{html_body}</div>',
        'category': vis_settings.get('category', 'workspace'),
    }
    
    if existing:
        # 更新
        models.execute_kw(db, uid, password, 'knowledge.article', 'write', [existing, article_vals])
        article_id = existing[0]
        action = "已更新"
    else:
        # 创建
        article_id = models.execute_kw(db, uid, password, 'knowledge.article', 'create', [article_vals])
        action = "已创建"
    
    # 添加部门成员
    if matched_user_ids:
        partner_ids = user_ids_to_partner_ids(models, db, uid, password, matched_user_ids)
        if partner_ids:
            added = add_article_members(models, db, uid, password, article_id, partner_ids)
            print(f"     ✅ {action} (ID: {article_id}, 成员: +{added})")
        else:
            print(f"     ✅ {action} (ID: {article_id}, 成员: 无有效用户)")
    else:
        print(f"     ✅ {action} (ID: {article_id})")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='kb-odoo-export — 导出知识库到 Odoo')
    parser.add_argument('--config', default=DEFAULT_CONFIG, help='Enterprise 配置文件')
    parser.add_argument('--article', help='仅导出指定文章（文件名，不含 .md）')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不实际创建')
    parser.add_argument('--visibility', choices=['private', 'workspace'], default='workspace',
                       help='默认可见性')
    
    args = parser.parse_args()
    
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), '..', args.config)
    config = load_config(config_path)
    
    if not config:
        print(f"❌ 配置文件不存在: {config_path}")
        sys.exit(1)
    
    # 连接 Odoo
    try:
        models, db, uid, password = connect_odoo(config)
        print(f"✅ 已连接 Odoo: {config['odoo']['url']}")
    except Exception as e:
        print(f"❌ Odoo 连接失败: {e}")
        sys.exit(1)
    
    # 获取 wiki 目录
    kb_dir = os.environ.get('KB_DATA_DIR', os.path.expanduser('~/.openclaw/agents/main/agent/kb'))
    wiki_dir = os.path.join(kb_dir, 'wiki')
    
    if not os.path.exists(wiki_dir):
        print(f"❌ Wiki 目录不存在: {wiki_dir}")
        sys.exit(1)
    
    print(f"📚 Wiki 目录: {wiki_dir}")
    print(f"可见性默认设置: {args.visibility}")
    print("")
    
    # 收集要导出的文章
    articles = []
    if args.article:
        article_path = os.path.join(wiki_dir, f"{args.article}.md")
        if os.path.exists(article_path):
            articles.append(article_path)
        else:
            print(f"❌ 文章不存在: {article_path}")
            sys.exit(1)
    else:
        for filename in os.listdir(wiki_dir):
            if filename.endswith('.md') and filename != 'index.md':
                articles.append(os.path.join(wiki_dir, filename))
    
    print(f"找到 {len(articles)} 个文章\n")
    
    # 导出
    if args.dry_run:
        print("⚠️  DRY RUN 模式\n")
    
    success = 0
    for article_path in articles:
        try:
            if export_article(models, db, uid, password, article_path, config, args.dry_run):
                success += 1
        except Exception as e:
            print(f"  ❌ 导出失败: {e}")
    
    print("")
    print(f"✅ 完成！成功导出 {success}/{len(articles)} 个文章")
    
    if not args.dry_run:
        print("")
        print("📌 提示: 在 Odoo Knowledge 中查看导出的文章")

if __name__ == '__main__':
    main()

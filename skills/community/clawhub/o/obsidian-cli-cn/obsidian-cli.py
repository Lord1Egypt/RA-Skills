#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
from pathlib import Path
from collections import Counter, defaultdict
import datetime

# 设置输出编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_all_md_files(vault_path):
    """获取知识库下所有.md文件"""
    md_files = []
    for root, dirs, files in os.walk(vault_path):
        # 忽略.obsidian等隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    return md_files

def read_file_content(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"[警告] 读取文件失败 {file_path}: {str(e)}")
        return ""

def cmd_search(args):
    """搜索命令实现"""
    md_files = get_all_md_files(args.vault)
    keyword = args.keyword
    results = []
    pattern = re.compile(keyword, flags=0 if args.case_sensitive else re.IGNORECASE)
    
    print(f"🔍 正在搜索关键词: {keyword}，共扫描{len(md_files)}个笔记...\n")
    
    for file_path in md_files:
        content = read_file_content(file_path)
        file_name = os.path.basename(file_path).replace('.md', '')
        relative_path = os.path.relpath(file_path, args.vault)
        
        # 检查标题
        title_match = pattern.search(file_name)
        # 检查内容
        content_matches = list(pattern.finditer(content))
        
        if title_match or content_matches:
            result = {
                "file": relative_path,
                "title_match": title_match is not None,
                "match_count": len(content_matches) + (1 if title_match else 0),
                "preview": []
            }
            # 生成预览片段
            for match in content_matches[:3]:
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                preview = content[start:end].replace('\n', ' ').strip()
                # 高亮关键词
                preview = pattern.sub(lambda m: f"「{m.group()}」", preview)
                result["preview"].append(preview)
            results.append(result)
    
    # 按匹配数量排序
    results.sort(key=lambda x: x["match_count"], reverse=True)
    
    if not results:
        print("❌ 没有找到匹配的笔记")
        return
    
    print(f"✅ 共找到{len(results)}个匹配的笔记:\n")
    for i, res in enumerate(results, 1):
        print(f"{i}. 📄 {res['file']} (匹配次数: {res['match_count']})")
        for preview in res["preview"]:
            print(f"   ...{preview}...")
        print()

def cmd_stats(args):
    """统计命令实现"""
    md_files = get_all_md_files(args.vault)
    total_words = 0
    total_size = 0
    tags = []
    create_dates = []
    link_count = 0
    
    print(f"📊 正在统计知识库: {args.vault}，共{len(md_files)}个笔记...\n")
    
    for file_path in md_files:
        content = read_file_content(file_path)
        # 统计字数
        total_words += len(content)
        # 统计文件大小
        total_size += os.path.getsize(file_path)
        # 提取标签
        file_tags = re.findall(r'#([a-zA-Z0-9\u4e00-\u9fa5_-]+)', content)
        tags.extend(file_tags)
        # 提取链接
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        link_count += len(links)
        # 统计创建时间
        ctime = os.path.getctime(file_path)
        create_dates.append(datetime.datetime.fromtimestamp(ctime).date())
    
    # 统计近7/30/90天新增
    today = datetime.date.today()
    last7 = sum(1 for d in create_dates if (today - d).days <=7)
    last30 = sum(1 for d in create_dates if (today - d).days <=30)
    last90 = sum(1 for d in create_dates if (today - d).days <=90)
    
    # 标签统计
    tag_counter = Counter(tags)
    top_tags = tag_counter.most_common(10)
    
    # 输出结果
    print("📈 知识库统计报告")
    print("="*50)
    print(f"📄 总笔记数量: {len(md_files)} 个")
    print(f"✍️ 总字数: {total_words:,} 字")
    print(f"💾 总文件大小: {total_size/1024/1024:.2f} MB")
    print(f"🔗 总双向链接数量: {link_count} 个")
    print(f"🏷️ 总标签数量: {len(tag_counter)} 个")
    print()
    print("📅 新增统计:")
    print(f"   近7天新增: {last7} 个")
    print(f"   近30天新增: {last30} 个")
    print(f"   近90天新增: {last90} 个")
    print()
    print("🏆 最常用标签TOP10:")
    for tag, count in top_tags:
        print(f"   #{tag}: {count} 次")
    print()

def cmd_replace(args):
    """批量替换命令实现"""
    md_files = get_all_md_files(args.vault)
    old_text = args.old_text
    new_text = args.new_text
    modified_count = 0
    
    print(f"🔄 正在批量替换: \"{old_text}\" → \"{new_text}\"\n")
    
    flags = 0 if args.case_sensitive else re.IGNORECASE
    pattern = re.compile(old_text, flags=flags)
    
    for file_path in md_files:
        content = read_file_content(file_path)
        if pattern.search(content):
            new_content = pattern.sub(new_text, content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_count +=1
            print(f"✅ 已修改: {os.path.relpath(file_path, args.vault)}")
    
    print(f"\n🎉 替换完成，共修改{modified_count}个笔记")

def cmd_export(args):
    """导出命令实现"""
    md_files = get_all_md_files(args.vault)
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    export_count = 0
    
    print(f"📤 正在导出笔记到: {output_dir}\n")
    
    tag_filter = args.tag
    for file_path in md_files:
        content = read_file_content(file_path)
        # 标签过滤
        if tag_filter:
            if f"#{tag_filter}" not in content:
                continue
        # 生成输出路径
        relative_path = os.path.relpath(file_path, args.vault)
        output_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        export_count +=1
        print(f"✅ 已导出: {relative_path}")
    
    print(f"\n🎉 导出完成，共导出{export_count}个笔记")

def cmd_check_links(args):
    """检查死链命令实现"""
    md_files = get_all_md_files(args.vault)
    # 所有笔记标题集合
    note_titles = set(os.path.basename(f).replace('.md', '') for f in md_files)
    broken_links = []
    orphan_notes = []
    link_map = defaultdict(list)
    
    print(f"🔗 正在检查链接，共扫描{len(md_files)}个笔记...\n")
    
    for file_path in md_files:
        content = read_file_content(file_path)
        source_note = os.path.basename(file_path).replace('.md', '')
        # 提取所有链接
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in links:
            # 去除锚点部分
            link_title = link.split('#')[0].strip()
            if link_title and link_title not in note_titles:
                broken_links.append({
                    "source": source_note,
                    "broken_link": link_title
                })
            link_map[source_note].append(link_title)
            link_map[link_title].append(source_note)
    
    # 检测孤立笔记
    for note in note_titles:
        if len(link_map.get(note, [])) == 0:
            orphan_notes.append(note)
    
    # 输出结果
    if broken_links:
        print(f"❌ 发现{len(broken_links)}个死链:")
        for bl in broken_links:
            print(f"   📄 {bl['source']} 中的链接 [[{bl['broken_link']}]] 指向不存在的笔记")
        print()
    else:
        print("✅ 没有发现死链\n")
    
    if orphan_notes:
        print(f"⚠️ 发现{len(orphan_notes)}个孤立笔记（没有任何双向链接）:")
        for note in orphan_notes:
            print(f"   📄 {note}")
    else:
        print("✅ 没有孤立笔记")

def main():
    parser = argparse.ArgumentParser(description="Obsidian 命令行工具")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--vault", required=True, help="Obsidian知识库路径")
    search_parser.add_argument("--case-sensitive", action="store_true", help="区分大小写")
    search_parser.add_argument("--regex", action="store_true", help="启用正则表达式")
    
    # 统计命令
    stats_parser = subparsers.add_parser("stats", help="统计知识库信息")
    stats_parser.add_argument("--vault", required=True, help="Obsidian知识库路径")
    
    # 替换命令
    replace_parser = subparsers.add_parser("replace", help="批量替换笔记内容")
    replace_parser.add_argument("old_text", help="要替换的旧文本")
    replace_parser.add_argument("new_text", help="替换后的新文本")
    replace_parser.add_argument("--vault", required=True, help="Obsidian知识库路径")
    replace_parser.add_argument("--case-sensitive", action="store_true", help="区分大小写")
    
    # 导出命令
    export_parser = subparsers.add_parser("export", help="批量导出笔记")
    export_parser.add_argument("--vault", required=True, help="Obsidian知识库路径")
    export_parser.add_argument("--output", required=True, help="导出目录路径")
    export_parser.add_argument("--tag", help="按标签筛选导出")
    export_parser.add_argument("--format", choices=["markdown", "html", "txt"], default="markdown", help="导出格式")
    
    # 检查链接命令
    check_links_parser = subparsers.add_parser("check-links", help="检查死链和孤立笔记")
    check_links_parser.add_argument("--vault", required=True, help="Obsidian知识库路径")
    
    args = parser.parse_args()
    
    # 验证知识库路径
    if not os.path.exists(args.vault):
        print(f"❌ 知识库路径不存在: {args.vault}")
        sys.exit(1)
    
    # 执行对应命令
    if args.command == "search":
        cmd_search(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "replace":
        cmd_replace(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "check-links":
        cmd_check_links(args)

if __name__ == "__main__":
    main()

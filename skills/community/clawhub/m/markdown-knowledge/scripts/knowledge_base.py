#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库主入口脚本
提供命令行接口供OpenClaw调用
"""

import sys
import json
from pathlib import Path

# 添加父目录到路径，以便将 src 作为包导入
sys.path.insert(0, str(Path(__file__).parent.parent))

import src
from src.knowledge_core import IndexBuilder, KnowledgeSearcher
from src.config import load_config, resolve_index_path


def ensure_ripgrep():
    """检测 ripgrep，不存在则自动安装（跨平台）"""
    import platform, subprocess, shutil, urllib.request, tarfile, zipfile, os
    
    if shutil.which('rg'):
        return True
    
    system = platform.system().lower()   # linux/darwin/windows
    machine = platform.machine().lower() # aarch64/x86_64/armv7
    
    # 构建下载 URL
    base = "https://github.com/BurntSushi/ripgrep/releases/download/14.1.4"
    
    if system == 'linux':
        if machine == 'aarch64':
            url = f"{base}/ripgrep-14.1.4-aarch64-unknown-linux-gnu.tar.gz"
        else:
            url = f"{base}/ripgrep-14.1.4-x86_64-unknown-linux-musl.tar.gz"
    elif system == 'darwin':
        if machine == 'aarch64':
            url = f"{base}/ripgrep-14.1.4-aarch64-apple-darwin.tar.gz"
        else:
            url = f"{base}/ripgrep-14.1.4-x86_64-apple-darwin.tar.gz"
    elif system == 'windows':
        url = f"{base}/ripgrep-14.1.4-x86_64-pc-windows-msvc.zip"
    else:
        return False
    
    install_dir = Path.home() / '.local' / 'bin'
    install_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"正在下载 ripgrep...")
        urllib.request.urlretrieve(url, '/tmp/rg_install.tar.gz')
        if system == 'windows':
            with zipfile.ZipFile('/tmp/rg_install.tar.gz', 'r') as z:
                z.extractall(install_dir)
        else:
            with tarfile.open('/tmp/rg_install.tar.gz', 'r:gz') as t:
                t.extractall('/tmp')
                rg_bin = Path('/tmp/rg-*')[0] / 'rg'
                shutil.copy(rg_bin, install_dir / 'rg')
        Path(install_dir / 'rg').chmod(0o755)
        print(f"ripgrep 已安装到 {install_dir / 'rg'}")
        return True
    except Exception as e:
        print(f"ripgrep 安装失败: {e}")
        return False


def cmd_build():
    """构建索引命令"""
    config = load_config()
    builder = IndexBuilder(config)
    result = builder.build_index()

    print(f"✅ 索引构建成功！")
    print(f"   文档数量：{result['total_documents']}")
    print(f"   内容块数：{result['total_blocks']}")
    print(f"   索引路径：{config['index_path']}")

    return result


def cmd_search(query: str, top_k: int = 3):
    """搜索命令"""
    config = load_config()
    searcher = KnowledgeSearcher(config)
    results = searcher.search(query, top_k)

    if not results:
        print("未在知识库中找到相关信息。")
        return None

    print(searcher.format_results(results, query))

    return [
        {
            'title': r['document'].get('title', ''),
            'path': r['document'].get('path', ''),
            'score': r['score'],
            'summary': r['document'].get('summary', ''),
            'blocks': [
                {'title': b['title'], 'preview': b['preview']}
                for b in r['matched_blocks']
            ]
        }
        for r in results
    ]


def cmd_stats():
    """统计命令"""
    config = load_config()
    searcher = KnowledgeSearcher(config)
    stats = searcher.get_stats()

    print("📊 知识库统计信息")
    print("─" * 40)
    print(f"总文档数：{stats['total_documents']}")
    print(f"总内容块：{stats['total_blocks']}")
    print(f"索引路径：{stats['index_path']}")
    print(f"最后更新：{stats['last_updated'] or '未知'}")

    if stats.get('documents_by_folder'):
        print("\n📁 各目录文档数：")
        for folder, count in sorted(stats['documents_by_folder'].items(), key=lambda x: -x[1])[:10]:
            print(f"   {folder}: {count}")

    return stats


def cmd_init(knowledge_path: str = None):
    """初始化命令"""
    ensure_ripgrep()
    if knowledge_path:
        path = Path(knowledge_path).expanduser()
    else:
        common_paths = [
            Path.home() / 'Markdown' / 'Vault',
            Path.home() / 'Documents' / 'Markdown',
            Path.home() / 'markdown' / 'vault',
        ]
        path = None
        for p in common_paths:
            if p.exists():
                path = p
                break
        if not path:
            path = Path.home() / 'Markdown' / 'Vault'

    from src.config import get_default_config, SKILL_DIR

    skill_dir = SKILL_DIR
    skill_dir.mkdir(parents=True, exist_ok=True)

    default_cfg = get_default_config()
    config = {
        'knowledge_path': str(path.absolute()),
        'index_path': str(skill_dir / 'index.json'),
        'search_top_k': default_cfg['search_top_k'],
        'auto_refresh': default_cfg['auto_refresh'],
        'refresh_interval': default_cfg['refresh_interval'],
        'exclude_patterns': default_cfg['exclude_patterns']
    }

    config_file = skill_dir / 'config.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"✅ 配置已创建：{config_file}")
    print(f"   知识库路径：{config['knowledge_path']}")

    print("\n正在构建索引...")
    builder = IndexBuilder(config)
    result = builder.build_index()
    print(f"✅ 索引构建完成：{result['total_documents']} 个文档")


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  knowledge_base.py init              # 初始化配置")
        print("  knowledge_base.py init <路径>       # 初始化并指定知识库路径")
        print("  knowledge_base.py build             # 构建索引")
        print("  knowledge_base.py search <查询词>   # 搜索知识库")
        print("  knowledge_base.py stats             # 查看统计信息")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init':
        path = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_init(path)

    elif command == 'build':
        cmd_build()

    elif command == 'search':
        if len(sys.argv) < 3:
            print("错误：search命令需要提供查询词")
            sys.exit(1)
        cmd_search(sys.argv[2])

    elif command == 'stats':
        cmd_stats()

    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
微信公众号文章爬取 - 直接调用版本

配置好虚拟环境路径后，可以直接调用此脚本爬取文章。
"""

import sys
import json
import subprocess
from pathlib import Path


# ================= 配置区域 =================
# 在这里配置你的虚拟环境路径
VENV_PATH = "/opt/playwright-env"  # 已配置好虚拟环境路径
# ===========================================


def fetch_article(url: str, output_dir: str = "./wechat_articles"):
    """
    爬取微信公众号文章
    
    Args:
        url: 文章 URL
        output_dir: 输出目录
    
    Returns:
        爬取结果字典
    """
    # 检查虚拟环境
    venv_python = Path(VENV_PATH) / "bin" / "python"
    if not venv_python.exists():
        venv_python = Path(VENV_PATH) / "Scripts" / "python.exe"
    
    if not venv_python.exists():
        print(f"❌ 找不到虚拟环境的 Python: {VENV_PATH}")
        print("请修改脚本中的 VENV_PATH 配置")
        return None
    
    # 找到脚本路径
    skill_dir = Path(__file__).parent
    fetch_script = skill_dir / "scripts" / "fetch.py"
    
    if not fetch_script.exists():
        print(f"❌ 找不到脚本: {fetch_script}")
        return None
    
    # 构建命令
    cmd = [str(venv_python), str(fetch_script), url, "-o", output_dir]
    
    print("="*80)
    print("📰 微信公众号文章爬取")
    print("="*80)
    print(f"📄 URL: {url}")
    print(f"🐍 虚拟环境: {VENV_PATH}")
    print("="*80)
    print()
    
    # 运行命令
    try:
        result = subprocess.run(
            cmd,
            cwd=str(skill_dir.parent),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            # 尝试找到最新的结果
            output_path = Path(output_dir)
            if output_path.exists():
                dirs = sorted([d for d in output_path.iterdir() if d.is_dir()], 
                            key=lambda x: x.stat().st_mtime, reverse=True)
                if dirs:
                    latest_dir = dirs[0]
                    json_path = latest_dir / "article.json"
                    if json_path.exists():
                        with open(json_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        print("\n" + "="*80)
                        print("✅ 爬取成功！")
                        print("="*80)
                        print(f"📰 标题: {data['title']}")
                        if data.get('author'):
                            print(f"✍️  作者: {data['author']}")
                        if data.get('publish_date'):
                            print(f"📅 发布时间: {data['publish_date']}")
                        print(f"📝 内容长度: {data['length']} 字符")
                        if data.get('images_count'):
                            print(f"🖼️  图片: {data['images_count']} 张")
                        print("="*80)
                        print("\n📖 内容摘要:")
                        content = data['content']
                        print(content[:1000] + "..." if len(content) > 1000 else content)
                        print("\n" + "="*80)
                        print(f"\n📁 保存位置: {output_dir}/{data['article_dir']}/")
                        
                        return data
        
        return None
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python3 {sys.argv[0]} <微信公众号文章URL>")
        print()
        print("示例:")
        print(f"  python3 {sys.argv[0]} https://mp.weixin.qq.com/s/xxx")
        sys.exit(1)
    
    url = sys.argv[1]
    fetch_article(url)

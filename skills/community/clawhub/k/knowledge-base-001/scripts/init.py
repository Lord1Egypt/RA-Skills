#!/usr/bin/env python3
"""
Knowledge Base 初始化脚本
确保目录结构、依赖和索引文件就绪
"""
import os
import sys
import subprocess
from pathlib import Path

KB_ROOT = Path(os.path.expanduser("~/.openclaw/workspace/knowledge-base"))
SKILL_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REQUIREMENTS = SKILL_DIR / "requirements.txt"

def ensure_dependencies():
    """检查并安装依赖"""
    required = {
        "markitdown": None,
        "jieba": None
    }
    
    # 检查哪些依赖缺失
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if not missing:
        print("所有依赖已就绪")
        return True
    
    print(f"缺少依赖: {', '.join(missing)}，正在自动安装...")
    
    # 使用 requirements.txt 安装
    if REQUIREMENTS.exists():
        cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", str(REQUIREMENTS)]
    else:
        # 降级：单独安装
        cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages"] + missing
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("依赖安装成功")
            return True
        else:
            print(f"安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"安装出错: {e}")
        return False

def init_kb():
    """初始化知识库目录"""
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    
    default_cats = ["学术论文", "技术文档", "工作资料", "读书笔记", "项目文档", "参考资料", "未分类"]
    for cat in default_cats:
        (KB_ROOT / cat).mkdir(exist_ok=True)
    
    index_file = KB_ROOT / ".index.json"
    if not index_file.exists():
        import json
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump({
                "version": "1.0",
                "documents": [],
                "categories": default_cats
            }, f, ensure_ascii=False, indent=2)
    
    print(f"知识库已初始化: {KB_ROOT}")
    print(f"默认分类: {', '.join(default_cats)}")

def check_markitdown():
    """检查 markitdown 版本"""
    try:
        import markitdown
        print(f"markitdown 已安装 (版本: {markitdown.__version__})")
        return True
    except ImportError:
        return False

if __name__ == "__main__":
    print("=== Knowledge Base 初始化 ===")
    
    # 第一步：确保依赖
    if not ensure_dependencies():
        print("依赖安装失败，请手动运行: pip install markitdown[all] jieba")
        sys.exit(1)
    
    # 第二步：初始化目录
    init_kb()
    
    # 第三步：验证 markitdown
    check_markitdown()
    
    print("\n初始化完成！你可以开始使用知识库了。")

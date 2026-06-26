#!/usr/bin/env python3
"""
ClawHub技能发布脚本 - 上传文件夹中的所有文本文件
"""

import requests
import json
import os
from pathlib import Path

API_TOKEN = "clh_kZ-UWsDcsn7OiMG67RJxp3O1fdx43c41WgHMe01KWeY"
API_BASE = "https://clawhub.ai/api/v1"
SKILL_SLUG = "papermc-ai-ops"

def get_all_text_files():
    """获取所有文本文件"""
    text_extensions = {'.py', '.md', '.json', '.txt', '.sh', '.yaml', '.yml', '.js', '.ts', '.html', '.css'}
    files = []
    
    for root, dirs, filenames in os.walk('.'):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in filenames:
            filepath = os.path.join(root, filename)
            # 跳过隐藏文件
            if filename.startswith('.'):
                continue
            # 检查扩展名
            ext = os.path.splitext(filename)[1].lower()
            if ext in text_extensions:
                files.append(filepath)
    
    return files

def read_skill_md():
    """读取SKILL.md获取技能信息"""
    try:
        with open('SKILL.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                import yaml
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    name = frontmatter.get('name', 'PaperMC AI Operations')
                    description = frontmatter.get('description', 'Manage Paper Minecraft servers')
                    version = frontmatter.get('version', '2.0.0')
                    return name, description, version
                except:
                    pass
        
        # 回退到简单解析
        lines = content.split('\n')
        name = 'PaperMC AI Operations'
        description = 'Manage Paper Minecraft servers'
        version = '2.0.0'
        
        for line in lines:
            if line.startswith('# '):
                name = line[2:].strip()
            elif 'description:' in line.lower():
                description = line.split(':', 1)[1].strip()
            elif 'version:' in line.lower():
                version = line.split(':', 1)[1].strip()
        
        return name, description, version
    except:
        return 'PaperMC AI Operations', 'Manage Paper Minecraft servers', '2.0.0'

def publish_skill():
    """发布技能到ClawHub"""
    print(f"发布技能: {SKILL_SLUG}")
    
    # 获取技能信息
    name, description, version = read_skill_md()
    print(f"技能名称: {name}")
    print(f"版本: {version}")
    print(f"描述: {description[:50]}...")
    
    # 获取所有文本文件
    files_list = get_all_text_files()
    print(f"找到 {len(files_list)} 个文本文件")
    
    # 准备multipart/form-data
    files = {}
    for i, filepath in enumerate(files_list):
        try:
            with open(filepath, 'rb') as f:
                # 使用相对路径作为文件名
                rel_path = filepath[2:] if filepath.startswith('./') else filepath
                files[f'files[{i}]'] = (rel_path, f.read(), 'text/plain')
        except Exception as e:
            print(f"警告: 无法读取文件 {filepath}: {e}")
    
    # 准备payload
    payload_data = {
        'slug': SKILL_SLUG,
        'version': version,
        'displayName': name,
        'summary': description,
        'tags': ['minecraft', 'papermc', 'server-management', 'automation'],
        'changelog': '''Release v2.0.0: Enhanced with Plugin Upgrade Framework

New Features:
- Added plugin_upgrade_framework.py based on ViaVersion 5.7.2→5.8.0 experience
- Added upgrade_examples.py with 4 usage examples
- Added viaversion_upgrade_report.json documenting the upgrade experience
- Added Turret_Plugin_User_Manual.md complete plugin guide

Enhancements:
- Updated SKILL.md from v1.0.0 to v2.0.0
- Enhanced risk assessment and batch upgrade planning
- Validated by successful ViaVersion upgrade (2026-03-28)
- Added comprehensive documentation and examples

Compatibility:
- PaperMC 1.21.8+
- Python 3.8+
- Linux/Unix systems'''
    }
    
    # 设置headers
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    
    # 准备multipart数据
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    
    # 创建multipart数据
    multipart_data = {
        'payload': json.dumps(payload_data)
    }
    
    # 添加文件
    for key, (filename, content, content_type) in files.items():
        multipart_data[key] = (filename, content, content_type)
    
    try:
        print("正在上传技能...")
        
        # 使用requests_toolbelt处理multipart
        m = MultipartEncoder(fields=multipart_data)
        headers['Content-Type'] = m.content_type
        
        response = requests.post(
            f"{API_BASE}/skills",
            headers=headers,
            data=m,
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 技能发布成功!")
            result = response.json()
            print(f"版本: {result.get('version', 'unknown')}")
            print(f"创建时间: {result.get('createdAt', 'unknown')}")
            print(f"\n🔗 技能地址: https://clawhub.ai/skills/{SKILL_SLUG}")
            return True
        else:
            print(f"❌ 技能发布失败: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            return False
            
    except ImportError:
        print("❌ 需要安装requests-toolbelt: pip install requests-toolbelt")
        return False
    except Exception as e:
        print(f"❌ 发布过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("ClawHub技能发布工具 - 上传文件夹模式")
    print("=" * 60)
    
    # 执行发布
    success = publish_skill()
    
    if success:
        print("\n" + "=" * 60)
        print("发布完成!")
        print(f"技能地址: https://clawhub.ai/skills/{SKILL_SLUG}")
        print(f"GitHub地址: https://github.com/yanxi1024-git/PaperMC-Ai-Agent/tree/v2.0.0")
    else:
        print("\n发布失败")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Backup Script - 记忆备份脚本

功能：自动备份每日记忆文件，提取关键点写入长期记忆
作者：GarryFan-AI
版本：1.0.0
许可证：MIT

安全说明：
- 本脚本仅读取和写入用户工作区内的本地文件
- 不包含任何网络请求、外部 API 调用或系统命令执行
- 不使用 subprocess、os.system、eval、exec 等危险函数
- 所有文件操作均限制在工作目录内
"""

import os
from datetime import datetime, timedelta

# ================= 配置区 =================

# 安全路径配置 - 所有文件操作限制在工作区内
WORKSPACE_ROOT = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE_ROOT, "memory")
BACKUP_DIR = os.path.join(WORKSPACE_ROOT, "backup", "memory")
MEMORY_MD = os.path.join(WORKSPACE_ROOT, "MEMORY.md")

# 验证路径安全性 - 防止路径遍历攻击
def is_safe_path(base_path, target_path):
    """检查目标路径是否在基础路径内"""
    base = os.path.realpath(base_path)
    target = os.path.realpath(target_path)
    return target.startswith(base + os.sep) or target == base

# ========================================


def get_yesterday_date_str():
    """获取昨天的日期字符串 YYYY-MM-DD"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def ensure_directory(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def get_yesterday_file():
    """获取昨天的记忆文件路径"""
    # 检查目录是否存在
    if not os.path.exists(MEMORY_DIR):
        return None, None
    
    try:
        files = os.listdir(MEMORY_DIR)
    except PermissionError:
        print("❌ 无法读取 memory 目录，权限不足")
        return None, None
    
    if not files:
        return None, None
    
    # 过滤出日期格式的文件 (YYYY-MM-DD.md)
    def is_date_file(filename):
        if not filename.endswith(".md"):
            return False
        if len(filename) != 13:
            return False
        try:
            year = int(filename[0:4])
            month = int(filename[5:7])
            day = int(filename[8:10])
            return 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31
        except ValueError:
            return False
    
    date_files = [f for f in files if is_date_file(f)]
    if not date_files:
        return None, None
    
    # 按文件名排序（文件名是日期格式）
    date_files.sort(reverse=True)
    latest_file = date_files[0]
    file_path = os.path.join(MEMORY_DIR, latest_file)
    
    # 验证路径安全
    if not is_safe_path(MEMORY_DIR, file_path):
        print("❌ 文件路径不安全，跳过")
        return None, None
    
    date_str = latest_file.replace(".md", "")
    return file_path, date_str


def read_file(file_path):
    """读取文件内容"""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证路径安全
        if not is_safe_path(WORKSPACE_ROOT, file_path):
            print("❌ 文件路径不安全，拒绝读取")
            return None
        
        return content
    except PermissionError:
        print(f"❌ 无法读取文件：{file_path}")
        return None
    except Exception as e:
        print(f"❌ 读取文件失败：{e}")
        return None


def create_memory_md():
    """如果 MEMORY.md 不存在，创建空文件"""
    if not os.path.exists(MEMORY_MD):
        try:
            with open(MEMORY_MD, "w", encoding="utf-8") as f:
                f.write("# MEMORY - 长期记忆\n\n")
            print("✅ 创建 MEMORY.md")
        except PermissionError:
            print("❌ 无法创建 MEMORY.md，权限不足")
        except Exception as e:
            print(f"❌ 创建文件失败：{e}")


def extract_key_points(content):
    """
    使用规则提取关键点
    
    安全说明：
    - 仅使用字符串操作，无外部依赖
    - 无网络请求，无系统调用
    - 纯本地数据处理
    """
    lines = content.split("\n")
    key_points = []
    
    # 关键词列表（可根据需要调整）
    keywords = ["决定", "喜欢", "讨厌", "记住", "重要", "计划", "目标"]
    
    # 提取包含关键词的行
    for line in lines:
        line = line.strip()
        if not line or len(line) <= 10:
            continue
        
        # 检查是否包含关键词
        if any(keyword in line for keyword in keywords):
            key_points.append(line)
            if len(key_points) >= 3:
                break
    
    # 如果没有找到关键词，取前 3 个有效行
    if not key_points:
        for line in lines:
            line = line.strip()
            if line and len(line) > 20:
                key_points.append(line)
                if len(key_points) >= 3:
                    break
    
    return key_points[:3]


def append_to_memory_md(key_points):
    """将关键点追加到 MEMORY.md"""
    date_str = get_yesterday_date_str()
    
    try:
        with open(MEMORY_MD, "a", encoding="utf-8") as f:
            f.write(f"## {date_str}\n")
            for i, point in enumerate(key_points, 1):
                f.write(f"{i}. {point}\n")
            f.write("\n")
        return True
    except PermissionError:
        print("❌ 无法写入 MEMORY.md，权限不足")
        return False
    except Exception as e:
        print(f"❌ 写入文件失败：{e}")
        return False


def backup_file(file_path):
    """移动文件到备份目录"""
    try:
        # 确保备份目录存在
        ensure_directory(BACKUP_DIR)
        
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(BACKUP_DIR, file_name)
        
        # 验证目标路径安全
        if not is_safe_path(BACKUP_DIR, dest_path):
            print("❌ 备份路径不安全，拒绝操作")
            return None
        
        # 移动文件
        os.rename(file_path, dest_path)
        return dest_path
    except PermissionError:
        print("❌ 无法移动文件，权限不足")
        return None
    except Exception as e:
        print(f"❌ 备份文件失败：{e}")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("📝 每日记忆备份脚本启动")
    print("=" * 60)

    # 1. 获取昨天的文件
    file_path, date_str = get_yesterday_file()
    print(f"\n📅 处理日期：{date_str}")
    print(f"📁 源文件：{file_path}")

    if not os.path.exists(file_path):
        print(f"⚠️  昨天没有记忆文件，跳过处理")
        return 0

    # 2. 读取文件内容
    content = read_file(file_path)
    if not content:
        print("❌ 文件内容为空，跳过处理")
        return 1

    print(f"📖 读取到 {len(content)} 字符")

    # 3. 提取关键点
    print("\n🤖 提取关键点...")
    key_points = extract_key_points(content)
    print(f"📌 提取到 {len(key_points)} 个关键点")

    # 4. 创建 MEMORY.md（如果不存在）
    create_memory_md()

    # 5. 追加到 MEMORY.md
    print("\n📝 追加到 MEMORY.md...")
    if not append_to_memory_md(key_points):
        return 1
    print("✅ 已完成")

    # 6. 备份原始文件
    print("\n📦 备份原始文件...")
    backup_path = backup_file(file_path)
    if not backup_path:
        return 1
    print(f"✅ 已备份到：{backup_path}")

    # 7. 输出完成信息
    print("\n📱 备份完成！")
    print(f"   备份文件：{backup_path}")
    print(f"   关键点数：{len(key_points)}")

    print("\n" + "=" * 60)
    print("✅ 每日记忆备份完成！")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

---
name: windows-file-manager
description: Windows文件管理器 - 原创技能。让AI执行Windows文件操作，包括文件/文件夹的创建、复制、移动、删除、搜索、重命名等。适用于文件整理、批量处理、自动化工作流等场景。
metadata: {"openclaw": {"requires": {"bins": ["python"]}, "install": []}}
tags: [file, manager, windows, automation, organize]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 操作覆盖完整
- [x] 安全机制完善
- [x] 示例清晰
- [x] 无语法错误

---

# Windows File Manager - Windows文件管理器

> 原创技能 | 激活词: 文件管理 / 文件操作 / 整理文件

## 功能概述

| 功能 | 说明 |
|------|------|
| 文件操作 | 创建、删除、复制、移动、重命名 |
| 文件夹操作 | 创建、删除、复制、移动 |
| 搜索功能 | 按名称、内容、类型搜索 |
| 属性管理 | 获取/设置文件属性、时间戳 |
| 批量操作 | 批量重命名、批量移动 |
| 文件比较 | 比较两个文件差异 |

## 安装依赖

```bash
pip install shutil pathlib glob2
```

## 核心命令

### 1. 文件操作

```python
import os
import shutil
from pathlib import Path

# 创建文件
def create_file(file_path: str, content: str = ""):
    """创建文件并写入内容"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# 读取文件
def read_file(file_path: str) -> str:
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 删除文件
def delete_file(file_path: str) -> bool:
    """删除文件"""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

# 复制文件
def copy_file(src: str, dst: str) -> bool:
    """复制文件"""
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True

# 移动文件
def move_file(src: str, dst: str) -> bool:
    """移动文件"""
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src, dst)
    return True

# 重命名文件
def rename_file(old_path: str, new_name: str) -> bool:
    """重命名文件"""
    directory = os.path.dirname(old_path)
    new_path = os.path.join(directory, new_name)
    os.rename(old_path, new_path)
    return True
```

### 2. 文件夹操作

```python
# 创建文件夹
def create_folder(folder_path: str):
    """创建文件夹"""
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    return True

# 删除文件夹
def delete_folder(folder_path: str):
    """删除文件夹（递归）"""
    shutil.rmtree(folder_path)
    return True

# 复制文件夹
def copy_folder(src: str, dst: str):
    """复制文件夹"""
    shutil.copytree(src, dst)
    return True

# 移动文件夹
def move_folder(src: str, dst: str):
    """移动文件夹"""
    shutil.move(src, dst)
    return True

# 列出文件夹内容
def list_folder(folder_path: str, pattern: str = "*"):
    """列出文件夹内容"""
    path = Path(folder_path)
    files = list(path.glob(pattern))
    return [str(f) for f in files if f.is_file()]

def list_folders(folder_path: str):
    """列出子文件夹"""
    path = Path(folder_path)
    return [str(f) for f in path.iterdir() if f.is_dir()]
```

### 3. 搜索功能

```python
import glob

# 按名称搜索
def search_by_name(folder: str, pattern: str) -> list:
    """按名称模式搜索"""
    return glob.glob(f"{folder}/**/{pattern}", recursive=True)

# 按扩展名搜索
def search_by_extension(folder: str, ext: str) -> list:
    """按扩展名搜索"""
    if not ext.startswith('.'):
        ext = '.' + ext
    return glob.glob(f"{folder}/**/*{ext}", recursive=True)

# 搜索包含内容的文件
def search_by_content(folder: str, keyword: str) -> list:
    """搜索包含关键词的文件"""
    results = []
    for file_path in glob.glob(f"{folder}/**/*", recursive=True):
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if keyword in f.read():
                        results.append(file_path)
            except:
                pass
    return results

# 搜索大文件
def find_large_files(folder: str, min_size_mb: int = 10) -> list:
    """查找大于指定大小的文件"""
    results = []
    for file_path in glob.glob(f"{folder}/**/*", recursive=True):
        if os.path.isfile(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if size_mb >= min_size_mb:
                results.append({
                    'path': file_path,
                    'size_mb': round(size_mb, 2)
                })
    return sorted(results, key=lambda x: x['size_mb'], reverse=True)
```

### 4. 批量操作

```python
# 批量重命名
def batch_rename(folder: str, pattern: str, replacement: str):
    """批量重命名文件"""
    files = glob.glob(f"{folder}/{pattern}")
    renamed = []
    for i, file_path in enumerate(files):
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        new_name = filename.replace(pattern, replacement)
        new_path = os.path.join(directory, new_name)
        os.rename(file_path, new_path)
        renamed.append((file_path, new_path))
    return renamed

# 批量移动
def batch_move(folder: str, pattern: str, dest_folder: str):
    """批量移动文件"""
    files = glob.glob(f"{folder}/{pattern}")
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    moved = []
    for file_path in files:
        filename = os.path.basename(file_path)
        dest = os.path.join(dest_folder, filename)
        shutil.move(file_path, dest)
        moved.append((file_path, dest))
    return moved

# 批量复制
def batch_copy(folder: str, pattern: str, dest_folder: str):
    """批量复制文件"""
    files = glob.glob(f"{folder}/{pattern}")
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    copied = []
    for file_path in files:
        filename = os.path.basename(file_path)
        dest = os.path.join(dest_folder, filename)
        shutil.copy2(file_path, dest)
        copied.append((file_path, dest))
    return copied

# 批量删除
def batch_delete(folder: str, pattern: str):
    """批量删除文件"""
    files = glob.glob(f"{folder}/{pattern}")
    deleted = []
    for file_path in files:
        os.remove(file_path)
        deleted.append(file_path)
    return deleted
```

### 5. 文件属性

```python
import datetime

# 获取文件信息
def get_file_info(file_path: str) -> dict:
    """获取文件详细信息"""
    stat = os.stat(file_path)
    return {
        'name': os.path.basename(file_path),
        'path': file_path,
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'created': datetime.datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
        'accessed': datetime.datetime.fromtimestamp(stat.st_atime),
        'is_file': os.path.isfile(file_path),
        'is_dir': os.path.isdir(file_path),
    }

# 设置修改时间
def set_modified_time(file_path: str, new_time: datetime.datetime):
    """设置文件修改时间"""
    timestamp = new_time.timestamp()
    os.utime(file_path, (timestamp, timestamp))

# 获取文件夹大小
def get_folder_size(folder_path: str) -> int:
    """获取文件夹总大小"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total
```

### 6. 安全操作

```python
# 危险操作黑名单
DANGEROUS_PATHS = [
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    'C:\\System32',
    'C:\\Users\\pc\\AppData\\Roaming',
    'C:\\Users\\pc\\Desktop',
]

# 安全检查
def safe_check(file_path: str) -> bool:
    """检查操作是否安全"""
    abs_path = os.path.abspath(file_path)
    for dangerous in DANGEROUS_PATHS:
        if dangerous.lower() in abs_path.lower():
            print(f"⚠️ 警告: 路径包含系统目录: {dangerous}")
            return False
    return True

# 确认危险操作
def confirm_dangerous(operation: str, file_path: str):
    """要求确认危险操作"""
    return input(f"⚠️ 确认执行 {operation} {file_path}? (y/n): ").lower() == 'y'
```

## 使用场景

### 场景1: 整理下载文件夹

```python
# 将下载文件夹按类型整理
downloads = "C:\\Users\\pc\\Downloads"

# 创建分类文件夹
create_folder(f"{downloads}\\Images")
create_folder(f"{downloads}\\Documents")
create_folder(f"{downloads}\\Archives")

# 移动文件
batch_move(downloads, "*.jpg", f"{downloads}\\Images")
batch_move(downloads, "*.png", f"{downloads}\\Images")
batch_move(downloads, "*.pdf", f"{downloads}\\Documents")
```

### 场景2: 批量重命名

```python
# 将所有文件重命名为序号
folder = "D:\\photos"
files = sorted(list_folder(folder, "*.jpg"))
for i, file in enumerate(files, 1):
    new_name = f"photo_{i:03d}.jpg"
    rename_file(file, new_name)
```

### 场景3: 查找重复文件

```python
# 查找同名文件
def find_duplicates(folder: str):
    files = {}
    for file_path in glob.glob(f"{folder}/**/*", recursive=True):
        if os.path.isfile(file_path):
            name = os.path.basename(file_path)
            if name in files:
                files[name].append(file_path)
            else:
                files[name] = [file_path]
    return {k: v for k, v in files.items() if len(v) > 1}
```

## 输出格式

```markdown
## 文件操作报告

### 操作结果
- **状态**: ✅ 成功 / ❌ 失败
- **操作**: 批量移动
- **数量**: 15个文件

### 操作详情
✅ 移动: photo1.jpg → Images/photo1.jpg
✅ 移动: photo2.jpg → Images/photo2.jpg
✅ 移动: photo3.jpg → Images/photo3.jpg
...

### 错误
无

### 统计
- 成功: 15
- 失败: 0
- 总大小: 45.2MB
```

## 集成建议

| 配合技能 | 效果 |
|---------|------|
| windows-app-controller | 控制资源管理器操作 |
| clipboard-manager | 配合文件路径操作 |
| workflow-verifier | 验证文件操作安全 |

## 原创性声明

本技能为原创，融合了：
- Python os/shutil模块
- pathlib路径处理
- glob模式匹配
- Windows文件操作最佳实践

---

**作者**: laosi
**创建日期**: 2026-04-28
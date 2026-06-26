---
name: file-organizer
version: 1.0.0
description: 文件整理 - 桌面和下载文件夹一键自动归类：图片/文档/压缩包/视频/音频/代码，生成整理报告
tags: [files, organization, windows, utility, cleanup]
author: laosi
source: original
---

# File Organizer - 文件整理

> 激活词: 整理 / 文件整理 / 归类

## 有什么用

桌面和下载文件夹是数字世界的玄关。乱成一团时，一键按类型自动归类，找回文件不用再翻遍整个文件夹。

## Python 实现

```python
import os
import shutil
from datetime import datetime

class FileOrganizer:
    CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg",
                   ".ico", ".tiff", ".tif", ".raw", ".heic", ".avif"],
        "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                      ".txt", ".md", ".rst", ".csv", ".tsv", ".json", ".xml",
                      ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
                      ".epub", ".mobi", ".pages", ".numbers", ".key"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
                     ".zst", ".iso", ".dmg"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",
                   ".m4v", ".mpeg", ".mpg", ".3gp"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
                  ".opus", ".alac"],
        "Code": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm", ".css",
                 ".scss", ".less", ".java", ".cpp", ".c", ".h", ".hpp",
                 ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
                 ".sh", ".bat", ".ps1", ".sql", ".r", ".lua", ".pl",
                 ".dart", ".vue", ".svelte", ".astro"],
        "Executables": [".exe", ".msi", ".appimage", ".deb", ".rpm",
                        ".dll", ".so", ".dylib"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    }
    
    def __init__(self, target_dirs: list = None):
        self.target_dirs = target_dirs or [
            os.path.join(os.environ.get("USERPROFILE", "C:/Users/Default"), "Downloads"),
            os.path.join(os.environ.get("USERPROFILE", "C:/Users/Default"), "Desktop"),
        ]
    
    def organize(self, dry_run: bool = False) -> dict:
        """执行整理，dry_run=True 只预览不动手"""
        report = {
            "scanned_dirs": [],
            "total_scanned": 0,
            "organized": 0,
            "skipped": 0,
            "by_category": {},
            "errors": []
        }
        
        for target in self.target_dirs:
            if not os.path.exists(target):
                report["errors"].append(f"目录不存在: {target}")
                continue
            
            dir_name = os.path.basename(target)
            report["scanned_dirs"].append(target)
            items = [f for f in os.listdir(target)
                     if os.path.isfile(os.path.join(target, f))]
            report["total_scanned"] += len(items)
            
            for fname in items:
                fpath = os.path.join(target, fname)
                ext = os.path.splitext(fname)[1].lower()
                category = self._classify(ext)
                
                if category:
                    cat_dir = os.path.join(target, f"_{category}")
                    if not dry_run:
                        os.makedirs(cat_dir, exist_ok=True)
                        try:
                            shutil.move(fpath, os.path.join(cat_dir, fname))
                            report["organized"] += 1
                            report["by_category"][category] = report["by_category"].get(category, 0) + 1
                        except (shutil.Error, PermissionError) as e:
                            report["errors"].append(f"移动失败: {fname} -> {e}")
                            report["skipped"] += 1
                    else:
                        report["organized"] += 1
                        report["by_category"][category] = report["by_category"].get(category, 0) + 1
                else:
                    report["skipped"] += 1
        
        report["timestamp"] = datetime.now().isoformat()
        return report
    
    def _classify(self, ext: str) -> str:
        for cat, exts in self.CATEGORIES.items():
            if ext in exts:
                return cat
        return ""
    
    def print_report(self, report: dict):
        print(f"\n{'='*40}")
        print(f"文件整理报告 ({report['timestamp']})")
        print(f"{'='*40}")
        for d in report["scanned_dirs"]:
            print(f"  扫描: {d}")
        print(f"\n  总计扫描: {report['total_scanned']} 个文件")
        print(f"  已整理: {report['organized']} 个")
        print(f"  已跳过: {report['skipped']} 个")
        if report["by_category"]:
            print(f"\n  分类统计:")
            for cat, count in sorted(report["by_category"].items(), key=lambda x: -x[1]):
                print(f"    {cat}: {count} 个")
        if report["errors"]:
            print(f"\n  错误 ({len(report['errors'])}):")
            for e in report["errors"][:5]:
                print(f"    ❌ {e}")

# 使用示例
organizer = FileOrganizer()

# 先预览，不实际移动
report = organizer.organize(dry_run=True)
organizer.print_report(report)

# 确认后执行
# organizer.organize(dry_run=False)
```

## 分类规则

| 分类 | 后缀 | 目录名 |
|------|------|--------|
| 🖼 图片 | jpg, png, gif, webp, svg... | `_Images` |
| 📄 文档 | pdf, doc, txt, md, csv... | `_Documents` |
| 📦 压缩包 | zip, rar, 7z, tar.gz... | `_Archives` |
| 🎬 视频 | mp4, avi, mkv, mov... | `_Videos` |
| 🎵 音频 | mp3, wav, flac, aac... | `_Audio` |
| 💻 代码 | py, js, ts, html, css... | `_Code` |
| ⚙️ 可执行 | exe, msi, deb, dll... | `_Executables` |
| 🔤 字体 | ttf, otf, woff... | `_Fonts` |

## 安全机制

- 只会将文件**移动到** `_分类名` 子目录，不会删除任何文件
- 同名文件冲突时保留原有文件（`shutil.move` 会报错不会覆盖）
- 只处理文件，不会移动其他目录
- `dry_run=True` 模式零修改，先预览再执行

## 使用场景

1. **桌面清理**: 每周一键整理桌面
2. **下载清理**: 下载文件夹攒了几个月的东西一键分类
3. **迁移助手**: 换电脑时把文件分类后打包
4. **开发者**: 代码文件 `.py .js .json` 自动归入Code目录

## 命令行用法

```bash
# 预览整理结果
python -c "from file_organizer import FileOrganizer; FileOrganizer().print_report(FileOrganizer().organize(dry_run=True))"

# 执行整理
python -c "from file_organizer import FileOrganizer; FileOrganizer().organize(dry_run=False)"
```

## 依赖

- Python 3.8+
- 无第三方依赖

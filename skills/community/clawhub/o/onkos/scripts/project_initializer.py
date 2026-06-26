#!/usr/bin/env python3
"""
项目初始化器 - 创建OnKos项目的标准目录结构
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any


class ProjectInitializer:
    """项目初始化器 - 创建标准项目结构"""

    def __init__(self, project_path: str):
        """
        初始化项目初始化器

        Args:
            project_path: 项目根目录
        """
        self.project_path = Path(project_path)

    def init_project(self, title: str = "", genre: str = "",
                     author: str = "", description: str = "") -> Dict[str, Any]:
        """
        初始化项目

        Args:
            title: 小说标题
            genre: 题材类型
            author: 作者
            description: 简介

        Returns:
            初始化结果
        """
        result = {
            "project_path": str(self.project_path),
            "created_files": [],
            "created_dirs": [],
            "errors": []
        }

        try:
            # 创建根目录
            self.project_path.mkdir(parents=True, exist_ok=True)

            # 创建数据目录
            data_dir = self.project_path / "data"
            data_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(data_dir))

            # 创建角色目录
            chars_dir = data_dir / "characters"
            chars_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(chars_dir))

            # 创建大纲目录
            outline_dir = self.project_path / "outline"
            outline_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(outline_dir))

            vol_dir = outline_dir / "volume_outlines"
            vol_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(vol_dir))

            chap_dir = outline_dir / "chapter_outlines"
            chap_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(chap_dir))

            # 创建草稿目录
            drafts_dir = self.project_path / "drafts"
            drafts_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(drafts_dir))

            # 创建修订目录
            revisions_dir = self.project_path / "revisions"
            revisions_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(revisions_dir))

            # 创建项目配置
            config = {
                "title": title or "未命名小说",
                "genre": genre or "玄幻",
                "author": author or "",
                "description": description or "",
                "created_at": datetime.now().isoformat(),
                "version": "2.0.0",
                "settings": {
                    "chapters_per_volume": 20,
                    "words_per_chapter": 3000,
                    "max_context_chars": 12000,
                    "auto_fact_extract": True,
                    "auto_entity_extract": True,
                    "continuity_check_on_save": True,
                    "quality_audit_on_save": True
                },
                "constraints": {}
            }

            config_path = data_dir / "project_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            result["created_files"].append(str(config_path))

            # 初始化 SQLite 数据库（含知识图谱、伏笔、弧线表）
            db_path = data_dir / "novel_memory.db"
            from memory_engine import MemoryEngine
            engine = MemoryEngine(str(db_path), project_path=str(self.project_path))
            engine.close()
            result["created_files"].append(str(db_path))

            # 创建情节图
            plot_path = data_dir / "plot_graph.json"
            with open(plot_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "main_line": [],
                    "branches": {},
                    "convergence": [],
                    "causal_chains": {},
                    "metadata": {"created_at": datetime.now().isoformat()}
                }, f, ensure_ascii=False, indent=2)
            result["created_files"].append(str(plot_path))

            # 创建风格配置
            style_path = data_dir / "style_profile.json"
            with open(style_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "profiles": {},
                    "metadata": {}
                }, f, ensure_ascii=False, indent=2)
            result["created_files"].append(str(style_path))

            # 创建全书大纲模板
            book_outline_path = outline_dir / "book_outline.md"
            book_outline = self._generate_book_outline_template(title, genre, description)
            with open(book_outline_path, 'w', encoding='utf-8') as f:
                f.write(book_outline)
            result["created_files"].append(str(book_outline_path))

        except Exception as e:
            result["errors"].append(str(e))

        return result

    def _generate_book_outline_template(self, title: str, genre: str,
                                         description: str) -> str:
        """生成全书大纲模板"""
        return f"""# {title or '未命名小说'} - 全书大纲

## 基本信息
- 书名: {title or '待定'}
- 题材: {genre or '待定'}
- 简介: {description or '待定'}
- 预计总字数: 100万字
- 预计卷数: 5卷
- 每卷章数: 20章

## 世界观设定
### 力量体系
- 

### 势力格局
- 

### 核心设定
- 

## 主角设定
### 主角
- 姓名: 
- 背景: 
- 目标: 
- 核心冲突: 

## 各卷大纲

### 第一卷: [卷名]
- 核心冲突: 
- 关键事件:
  1. 
  2. 
  3. 
- 伏笔种植:
  - 
- 本卷结尾状态: 

### 第二卷: [卷名]
- 核心冲突: 
- 关键事件:
  1. 
  2. 
  3. 
- 伏笔回收:
  - 
- 伏笔种植:
  - 

### 第三卷: [卷名]
- 核心冲突: 
- 关键事件:
  1. 
  2. 
  3. 

### 第四卷: [卷名]
- 核心冲突: 
- 关键事件:
  1. 
  2. 
  3. 

### 第五卷: [卷名]
- 核心冲突: 
- 关键事件:
  1. 
  2. 
  3. 
- 所有伏笔回收

## 主题与核心探讨
- 
"""

    def get_project_status(self) -> Dict[str, Any]:
        """获取项目状态"""
        status = {
            "project_path": str(self.project_path),
            "exists": self.project_path.exists(),
            "initialized": False,
            "stats": {}
        }

        if not self.project_path.exists():
            return status

        # 检查关键文件
        config_path = self.project_path / "data" / "project_config.json"
        if config_path.exists():
            status["initialized"] = True
            with open(config_path, 'r', encoding='utf-8') as f:
                status["config"] = json.load(f)

        # 统计
        drafts_dir = self.project_path / "drafts"
        if drafts_dir.exists():
            drafts = list(drafts_dir.glob("*.md"))
            status["stats"]["drafts"] = len(drafts)

        chars_dir = self.project_path / "data" / "characters"
        if chars_dir.exists():
            chars = list(chars_dir.glob("*.json"))
            status["stats"]["characters"] = len(chars)

        db_path = self.project_path / "data" / "novel_memory.db"
        if db_path.exists():
            status["stats"]["database_size"] = db_path.stat().st_size

        return status


    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "init":
            return self.init_project(
                params.get("title", ""),
                params.get("genre", ""),
                params.get("author", ""),
                params.get("description", "")
            )
        elif action == "status":
            return self.get_project_status()
        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """无资源需释放，保留接口一致性"""
        pass

def main():
    parser = argparse.ArgumentParser(description='项目初始化器')
    parser.add_argument('--project-path', required=True, help='项目根目录')
    parser.add_argument('--action', required=True,
                       choices=['init', 'status'],
                       help='操作类型')
    parser.add_argument('--title', default='', help='小说标题')
    parser.add_argument('--genre', default='', help='题材类型')
    parser.add_argument('--author', default='', help='作者')
    parser.add_argument('--description', default='', help='简介')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    initializer = ProjectInitializer(args.project_path)

    skip_keys = {"project_path", "action", "output"}
    params = {k: v for k, v in vars(args).items()
              if k not in skip_keys and not k.startswith('_')}
    result = initializer.execute_action(args.action, params)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()

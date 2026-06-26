import os
import re
import shutil
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class NotesOrganizer:
    """笔记整理器"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.config = {}
        self.file_mapping: Dict[str, Path] = {}
        self.operation_log = []

    def ask_questions(self) -> Dict:
        """通过命令行询问用户配置"""
        config = {}

        print("\n" + "=" * 50)
        print("笔记整理配置向导")
        print("=" * 50)

        # 问题1：分类方式
        print("\n【问题1】请选择笔记的分类方式：")
        print("  1. 按主题领域（如：前端、后端、算法、工具等）")
        print("  2. 按学习阶段（如：入门、进阶、实战、参考）")
        print("  3. 按项目")
        print("  4. 按时间")
        print("  5. 自定义分类方案")

        while True:
            choice = input("请输入选项 (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                config['classify_method'] = int(choice)
                break
            print("无效选项，请重新输入")

        # 问题2：目录命名风格
        print("\n【问题2】请选择目录命名风格：")
        print("  1. 数字前缀（如：01_基础知识/）")
        print("  2. 纯中文（如：基础知识/）")
        print("  3. 英文（如：basics/）")
        print("  4. 自定义")

        while True:
            choice = input("请输入选项 (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                config['naming_style'] = int(choice)
                break
            print("无效选项，请重新输入")

        # 问题3：是否需要子目录
        print("\n【问题3】是否需要创建二级子目录？")
        print("  1. 需要")
        print("  2. 不需要")

        while True:
            choice = input("请输入选项 (1-2): ").strip()
            if choice in ['1', '2']:
                config['use_subdirs'] = (choice == '1')
                break
            print("无效选项，请重新输入")

        # 问题4：双向链接
        print("\n【问题4】是否需要自动添加双向链接？")
        print("  1. 需要")
        print("  2. 不需要")

        while True:
            choice = input("请输入选项 (1-2): ").strip()
            if choice in ['1', '2']:
                config['add_links'] = (choice == '1')
                break
            print("无效选项，请重新输入")

        if config['add_links']:
            print("\n【问题4.1】链接显示位置？")
            print("  1. 文件开头（标题后）")
            print("  2. 文件末尾")

            while True:
                choice = input("请输入选项 (1-2): ").strip()
                if choice in ['1', '2']:
                    config['link_position'] = 'start' if choice == '1' else 'end'
                    break
                print("无效选项，请重新输入")

            print("\n【问题4.2】链接显示格式？")
            print("  1. 简洁（仅显示文件名）")
            print("  2. 详细（包含描述）")

            while True:
                choice = input("请输入选项 (1-2): ").strip()
                if choice in ['1', '2']:
                    config['link_format'] = 'simple' if choice == '1' else 'detailed'
                    break
                print("无效选项，请重新输入")

        # 问题5：清理选项
        print("\n【问题5】整理完成后是否清理？")
        print("  1. 清理空目录")
        print("  2. 清理空目录和重复文件")
        print("  3. 不清理")

        while True:
            choice = input("请输入选项 (1-3): ").strip()
            if choice in ['1', '2', '3']:
                config['cleanup'] = int(choice)
                break
            print("无效选项，请重新输入")

        # 如果是自定义分类，询问具体分类
        if config['classify_method'] == 5:
            print("\n【自定义分类】请输入分类目录名称（用逗号分隔）：")
            print("示例：基础理论,实战项目,工具资源,问题记录")
            categories = input("请输入: ").strip()
            config['custom_categories'] = [c.strip() for c in categories.split(',') if c.strip()]

            if config['use_subdirs']:
                print("\n是否为每个分类指定子目录？（y/n）")
                if input().strip().lower() == 'y':
                    config['custom_subdirs'] = {}
                    for cat in config['custom_categories']:
                        print(f"  分类【{cat}】的子目录（用逗号分隔，回车跳过）：")
                        subdirs = input().strip()
                        if subdirs:
                            config['custom_subdirs'][cat] = [s.strip() for s in subdirs.split(',') if s.strip()]

        self.config = config
        return config

    def scan_files(self) -> Dict[str, Path]:
        """扫描目录下所有md文件"""
        files = {}
        for md_file in self.base_path.rglob("*.md"):
            if ".codebuddy" in str(md_file):
                continue
            files[md_file.stem] = md_file
        return files

    def get_category_structure(self) -> Dict:
        """根据配置获取目录结构"""
        if self.config.get('classify_method') == 5:
            # 自定义分类
            structure = {}
            for cat in self.config.get('custom_categories', []):
                structure[cat] = {
                    'files': [],
                    'subdirs': {}
                }
                if self.config.get('custom_subdirs', {}).get(cat):
                    for subdir in self.config['custom_subdirs'][cat]:
                        structure[cat]['subdirs'][subdir] = []
            return structure

        # 预设分类方案
        structures = {
            1: {  # 按主题领域
                "01_基础知识": {"files": [], "subdirs": {}},
                "02_核心技术": {"files": [], "subdirs": {}},
                "03_框架工具": {"files": [], "subdirs": {}},
                "04_实战项目": {"files": [], "subdirs": {}},
                "05_资源收集": {"files": [], "subdirs": {}},
                "06_问题记录": {"files": [], "subdirs": {}}
            },
            2: {  # 按学习阶段
                "01_入门基础": {"files": [], "subdirs": {}},
                "02_进阶提升": {"files": [], "subdirs": {}},
                "03_实战应用": {"files": [], "subdirs": {}},
                "04_参考资料": {"files": [], "subdirs": {}}
            },
            3: {  # 按项目
                "01_项目A": {"files": [], "subdirs": {"文档": [], "代码": []}},
                "02_项目B": {"files": [], "subdirs": {"文档": [], "代码": []}},
                "03_通用知识": {"files": [], "subdirs": {}}
            },
            4: {  # 按时间
                "2024年": {"files": [], "subdirs": {}},
                "2025年": {"files": [], "subdirs": {}}
            }
        }

        return structures.get(self.config['classify_method'], structures[1])

    def create_directory_structure(self):
        """创建新的目录结构"""
        structure = self.get_category_structure()

        for dir_name in structure.keys():
            dir_path = self.base_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

            for subdir_name in structure[dir_name].get("subdirs", {}).keys():
                subdir_path = dir_path / subdir_name
                subdir_path.mkdir(parents=True, exist_ok=True)

    def classify_file(self, filename: str, filepath: Path) -> Tuple[str, str]:
        """根据文件内容分类"""
        # 简单的关键词匹配分类
        # 实际应用中可以结合文件内容分析

        category_keywords = {
            "01_基础知识": ["基础", "入门", "概念", "原理", "理论", "定义"],
            "02_核心技术": ["算法", "实现", "方法", "技术", "架构"],
            "03_框架工具": ["框架", "工具", "库", "插件", "配置"],
            "04_实战项目": ["项目", "实战", "案例", "应用", "demo"],
            "05_资源收集": ["资源", "链接", "教程", "文档", "参考"],
            "06_问题记录": ["问题", "bug", "错误", "解决", "技巧"]
        }

        # 尝试读取文件内容进行分类
        try:
            content = filepath.read_text(encoding="utf-8", errors='ignore').lower()
            content_with_name = content + " " + filename.lower()

            best_match = ("05_资源收集", 0)  # 默认分类
            for category, keywords in category_keywords.items():
                score = sum(1 for kw in keywords if kw in content_with_name)
                if score > best_match[1]:
                    best_match = (category, score)

            return best_match[0], ""
        except:
            return "05_资源收集", ""

    def move_files(self, files: Dict[str, Path]):
        """移动文件到新目录"""
        moved_count = 0

        for filename, filepath in files.items():
            target_dir, target_subdir = self.classify_file(filename, filepath)

            if target_subdir:
                target_path = self.base_path / target_dir / target_subdir / filepath.name
            else:
                target_path = self.base_path / target_dir / filepath.name

            if filepath != target_path and not target_path.exists():
                shutil.move(str(filepath), str(target_path))
                self.file_mapping[filename] = target_path
                self.operation_log.append(f"移动: {filepath.name} -> {target_dir}/{target_subdir}")
                moved_count += 1
            else:
                self.file_mapping[filename] = filepath

        return moved_count

    def analyze_content_similarity(self, files: Dict[str, Path]) -> Dict[str, List[str]]:
        """分析文件内容相似度，找出相关文件"""
        # 提取关键词
        file_keywords = {}

        for filename, filepath in files.items():
            try:
                content = filepath.read_text(encoding="utf-8", errors='ignore')
                # 简单的关键词提取（实际可用更复杂的NLP方法）
                words = re.findall(r'[\w\u4e00-\u9fff]{2,}', content.lower())
                word_freq = defaultdict(int)
                for word in words:
                    word_freq[word] += 1
                # 取高频词作为关键词
                keywords = set([w for w, f in sorted(word_freq.items(), key=lambda x: -x[1])[:20]])
                file_keywords[filename] = keywords
            except:
                file_keywords[filename] = set()

        # 计算相似度
        similarities = defaultdict(list)
        filenames = list(files.keys())

        for i, f1 in enumerate(filenames):
            for f2 in filenames[i+1:]:
                if f1 == f2:
                    continue
                # Jaccard相似度
                kw1, kw2 = file_keywords[f1], file_keywords[f2]
                if kw1 and kw2:
                    intersection = len(kw1 & kw2)
                    union = len(kw1 | kw2)
                    similarity = intersection / union if union > 0 else 0

                    if similarity > 0.1:  # 阈值
                        similarities[f1].append(f2)
                        similarities[f2].append(f1)

        return similarities

    def add_bidirectional_links(self, files: Dict[str, Path]):
        """添加双向链接"""
        if not self.config.get('add_links', False):
            return 0

        similarities = self.analyze_content_similarity(files)
        updated_count = 0

        for filename, filepath in files.items():
            if filename not in similarities or not similarities[filename]:
                continue

            try:
                content = filepath.read_text(encoding="utf-8")
            except:
                continue

            # 检查是否已有链接块
            if "> **相关链接**:" in content:
                continue

            # 构建链接块
            related_files = similarities[filename][:5]  # 最多5个链接
            link_strs = []
            for related in related_files:
                if self.config.get('link_format') == 'simple':
                    link_strs.append(f"[[{related}]]")
                else:
                    link_strs.append(f"[[{related}|{related}]]")

            link_block = f"> **相关链接**: {' | '.join(link_strs)}\n"

            # 插入位置
            if self.config.get('link_position') == 'end':
                new_content = content.rstrip() + "\n\n" + link_block
            else:
                lines = content.split("\n")
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.startswith("# "):
                        insert_pos = i + 1
                        break
                lines.insert(insert_pos, link_block)
                new_content = "\n".join(lines)

            try:
                filepath.write_text(new_content, encoding="utf-8")
                updated_count += 1
            except:
                pass

        return updated_count

    def cleanup(self):
        """清理空目录"""
        if self.config.get('cleanup', 3) == 3:
            return 0

        cleaned = 0
        for item in list(self.base_path.rglob("*")):
            if item.is_dir():
                try:
                    if not any(item.iterdir()):
                        item.rmdir()
                        cleaned += 1
                except:
                    pass

        return cleaned

    def save_operation_log(self):
        """保存操作日志"""
        log_path = self.base_path / ".organize_log.json"
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "config": self.config,
            "operations": self.operation_log
        }
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
        except:
            pass

    def organize(self):
        """执行整理流程"""
        print("\n" + "=" * 50)
        print("开始整理笔记")
        print("=" * 50)

        # 1. 扫描文件
        print("\n[1/5] 扫描文件...")
        files = self.scan_files()
        print(f"      找到 {len(files)} 个md文件")

        # 2. 创建目录结构
        print("\n[2/5] 创建目录结构...")
        self.create_directory_structure()
        print("      目录结构创建完成")

        # 3. 移动文件
        print("\n[3/5] 移动文件...")
        moved = self.move_files(files)
        print(f"      移动了 {moved} 个文件")

        # 4. 添加双向链接
        if self.config.get('add_links', False):
            print("\n[4/5] 添加双向链接...")
            updated_files = self.scan_files()
            linked = self.add_bidirectional_links(updated_files)
            print(f"      更新了 {linked} 个文件的链接")
        else:
            print("\n[4/5] 跳过双向链接")

        # 5. 清理
        if self.config.get('cleanup', 3) != 3:
            print("\n[5/5] 清理空目录...")
            cleaned = self.cleanup()
            print(f"      清理了 {cleaned} 个空目录")
        else:
            print("\n[5/5] 跳过清理")

        # 保存日志
        self.save_operation_log()

        print("\n" + "=" * 50)
        print("整理完成！")
        print("=" * 50)


def main():
    import sys

    if len(sys.argv) < 2:
        print("用法: python organize_notes.py <目录路径>")
        print("示例: python organize_notes.py /path/to/notes")
        sys.exit(1)

    base_path = sys.argv[1]

    if not os.path.exists(base_path):
        print(f"错误: 目录不存在 {base_path}")
        sys.exit(1)

    organizer = NotesOrganizer(base_path)
    organizer.ask_questions()
    organizer.organize()


if __name__ == "__main__":
    main()

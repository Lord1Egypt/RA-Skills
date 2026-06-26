#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章检查工具
功能：
1. 编码检测（UTF-8无BOM）
2. 乱码检测（特殊字符、不可见字符）
3. 内容完整性检查
4. 图片格式检查（.jpg）
5. 错别字检测
6. 断句检测
7. 可复制性检查
8. AI表达检测（新增）
9. 拟人化表达建议（新增）

使用方法：
python scripts/check_article.py <文件路径>
python scripts/check_article.py 美化文章_睡眠重要性_20250115.md
"""

import os
import sys
import re
import json
from pathlib import Path

# 常见错别字词库（正确 -> 错误）
TYPO_DICT = {
    "的地得": {"的": "地", "得": "的", "地": "得"},
    "了": "辽",
    "做": "作",
    "象": "像",
    "连接": "联结",
    "竟然": "居然",
    "账户": "帐号",
    "共总": "总共",
    "再在": "在于",
    "像向": "像",
    "功夫": "工夫",
    "其他": "其它",
    "学历": "学历",
    "泄气": "泄气",
    "其他": "其它",
}

# 常见错别字模式（错误 -> 正确）
TYPO_PATTERNS = [
    (r"发贴", "发帖"),
    (r"帐 号", "账号"),
    (r"好 象", "好像"),
    (r"形 象", "形象"),
    (r"截止", "截至"),
    (r"竟然", "居然"),
    (r"再接再励", "再接再厉"),
    (r"黄梁梦", "黄粱梦"),
    (r"旁证博引", "旁征博引"),
    (r"趋之若骛", "趋之若鹜"),
    (r"磬竹难书", "罄竹难书"),
    (r"不径而走", "不胫而走"),
    (r"人才倍出", "人才辈出"),
    (r"含辛如苦", "含辛茹苦"),
    (r"名记不忘", "念念不忘"),
    (r"开宗明意", "开宗明义"),
]


class ArticleChecker:
    """文章检查器"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = ""
        self.errors = []
        self.warnings = []
        self.info = []
        self.stats = {}

    def read_file(self):
        """读取文件内容"""
        try:
            # 读取文件
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()

            # 检查BOM
            with open(self.file_path, 'rb') as f:
                first_bytes = f.read(3)
                if first_bytes == b'\xef\xbb\xbf':
                    self.errors.append("【错误】文件包含UTF-8 BOM标记，可能导致乱码")
                else:
                    self.info.append("【通过】文件编码为UTF-8无BOM")

            self.info.append(f"【信息】文件读取成功，共{len(self.content)}个字符")
            return True

        except FileNotFoundError:
            self.errors.append(f"【错误】文件不存在: {self.file_path}")
            return False
        except UnicodeDecodeError as e:
            self.errors.append(f"【错误】文件编码错误: {e}")
            return False
        except Exception as e:
            self.errors.append(f"【错误】读取文件失败: {e}")
            return False

    def check_garbled(self):
        """检查乱码字符"""
        # 检查不可见字符
        invisible_chars = [
            ('\u0000', '空字符'),
            ('\u200b', '零宽空格'),
            ('\ufeff', 'BOM字符'),
            ('\ufffe', '非字符'),
            ('\u2028', '行分隔符'),
            ('\u2029', '段分隔符'),
        ]

        for char, name in invisible_chars:
            if char in self.content:
                count = self.content.count(char)
                self.errors.append(f"【错误】发现{name}({repr(char)}){count}处，可能导致乱码")

        # 检查非法Unicode代理对
        surrogate_pattern = re.compile(r'[\ud800-\udfff]')
        surrogates = surrogate_pattern.findall(self.content)
        if surrogates:
            self.errors.append(f"【错误】发现Unicode代理字符{len(surrogates)}处，可能导致乱码")

        # 检查异常的emoji或特殊符号
        if len(self.content) > 100:
            # 计算emoji数量
            emoji_pattern = re.compile(
                r'[\U0001F300-\U0001F9FF]'
                r'|[\U00026000-\U00026FFF]'
                r'|[\U0001F600-\U0001F64F]'
                r'|[\U0001F300-\U0001F5FF]'
                r'|[\U0001F680-\U0001F6FF]'
                r'|[\U0001F1E0-\U0001F1FF]'
            )
            emojis = emoji_pattern.findall(self.content)
            self.info.append(f"【信息】发现emoji符号{len(emojis)}个")

        if not self.errors or all('乱码' not in e for e in self.errors):
            if not any('乱码' in e for e in self.errors):
                self.info.append("【通过】未发现明显乱码字符")

    def check_completeness(self):
        """检查内容完整性"""
        # 检查标题
        title_pattern = r'^#\s+.+'
        if re.search(title_pattern, self.content, re.MULTILINE):
            self.info.append("【通过】包含标题")
        else:
            self.errors.append("【错误】缺少标题（以#开头）")

        # 检查是否有正文内容
        lines = [l.strip() for l in self.content.split('\n') if l.strip() and not l.strip().startswith('#')]
        if len(lines) >= 3:
            self.info.append(f"【通过】包含正文内容，共{len(lines)}个段落")
        else:
            self.errors.append(f"【错误】正文内容过少，仅有{len(lines)}个段落")

        # 检查是否有结尾
        ending_keywords = ['写在最后', '最后', '结语', '总结', '如果这篇文章对你有帮助', '觉得有用']
        has_ending = any(keyword in self.content for keyword in ending_keywords)
        if has_ending:
            self.info.append("【通过】包含结尾部分")
        else:
            self.warnings.append("【警告】可能缺少结尾引导部分")

        # 检查是否有互动引导
        interaction_keywords = ['在看', '点赞', '关注', '分享', '评论', '留言']
        has_interaction = any(keyword in self.content for keyword in interaction_keywords)
        if has_interaction:
            self.info.append("【通过】包含互动引导")
        else:
            self.warnings.append("【警告】缺少互动引导（点赞/在看/留言等）")

    def check_images(self):
        """检查图片格式"""
        # 查找所有图片语法
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, self.content)

        if not images:
            self.warnings.append("【警告】未发现任何图片")
            return

        self.info.append(f"【信息】发现{len(images)}张图片")

        jpg_count = 0
        other_count = 0
        empty_url_count = 0

        for alt, url in images:
            # 检查URL是否为空
            if not url or url.strip() == "":
                empty_url_count += 1
                self.errors.append(f"【错误】图片URL为空: ![{alt}]()")
                continue

            # 检查是否为占位符
            placeholder_patterns = [
                r'图片链接占位符',
                r'此处插入',
                r'your-image-url',
                r'example\.com',
                r'placeholder',
            ]
            is_placeholder = any(re.search(p, url, re.I) for p in placeholder_patterns)
            if is_placeholder:
                self.warnings.append(f"【警告】图片使用占位符: {url[:50]}...")
                continue

            # 检查文件格式
            if url.lower().endswith('.jpg') or url.lower().endswith('.jpeg'):
                jpg_count += 1
            elif url.lower().endswith('.png'):
                other_count += 1
                self.warnings.append(f"【警告】图片使用PNG格式，建议使用JPG: {url[:50]}...")
            elif url.lower().endswith('.gif'):
                other_count += 1
                self.warnings.append(f"【警告】图片使用GIF格式，建议使用JPG: {url[:50]}...")
            elif url.lower().endswith('.webp'):
                other_count += 1
                self.warnings.append(f"【警告】图片使用WebP格式: {url[:50]}...")
            else:
                self.warnings.append(f"【警告】图片格式非标准: {url[:50]}...")

        if jpg_count > 0:
            self.info.append(f"【通过】{jpg_count}张图片使用JPG格式")
        if empty_url_count > 0:
            self.errors.append(f"【错误】{empty_url_count}张图片URL为空")

    def check_typos(self):
        """检查错别字"""
        found_typos = []

        # 使用正则模式检查
        for wrong, correct in TYPO_PATTERNS:
            matches = list(re.finditer(wrong, self.content))
            if matches:
                for match in matches:
                    found_typos.append((match.start(), wrong, correct))

        if found_typos:
            self.errors.append(f"【错误】发现{len(found_typos)}处可能错别字:")
            for pos, wrong, correct in found_typos[:5]:  # 只显示前5个
                # 获取上下文
                start = max(0, pos - 10)
                end = min(len(self.content), pos + len(wrong) + 10)
                context = self.content[start:end].replace('\n', ' ')
                self.errors.append(f"  - '{wrong}' -> '{correct}' (上下文: ...{context}...)")
            if len(found_typos) > 5:
                self.errors.append(f"  ... 还有{len(found_typos) - 5}处")
        else:
            self.info.append("【通过】未发现明显错别字")

    def check_punctuation(self):
        """检查断句问题"""
        issues = []

        # 检查连续的长句（超过50个字符无标点）
        long_sentence_pattern = r'[^。！？.!?\n]{80,}[。！？.!?]'
        long_sentences = re.findall(long_sentence_pattern, self.content)
        if long_sentences:
            issues.append(f"【警告】发现{len(long_sentences)}处长句（超过80字无断句），建议拆分")

        # 检查连续无标点行
        lines = self.content.split('\n')
        long_lines = [i + 1 for i, line in enumerate(lines)
                      if len(line.strip()) > 0 and len(line.strip()) > 60
                      and not re.search(r'[。！？.!?]', line.strip())]
        if long_lines:
            issues.append(f"【警告】发现{len(long_lines)}行超过60字无标点: 行号{long_lines[:5]}")

        # 检查是否有段落过短
        short_lines = [i + 1 for i, line in enumerate(lines)
                       if len(line.strip()) > 0 and len(line.strip()) < 5
                       and not line.strip().startswith('#')]
        if short_lines:
            issues.append(f"【提示】发现{len(short_lines)}行过短（少于5字）")

        if issues:
            self.warnings.extend(issues)
        else:
            self.info.append("【通过】断句检查正常")

    def check_html_compatibility(self):
        """检查HTML兼容性"""
        # 检查HTML标签是否正确闭合
        html_tags = ['div', 'span', 'p', 'strong', 'em', 'b', 'i']
        for tag in html_tags:
            open_count = len(re.findall(f'<{tag}[^>]*>', self.content, re.I))
            close_count = len(re.findall(f'</{tag}>', self.content, re.I))
            if open_count != close_count:
                self.warnings.append(
                    f"【警告】HTML标签<{tag}>未正确闭合: 开启{open_count}次，闭合{close_count}次"
                )

        # 检查内联样式
        inline_styles = re.findall(r'style="[^"]*"', self.content)
        if inline_styles:
            self.info.append(f"【信息】包含{len(inline_styles)}处内联样式")

    def check_copy_paste(self):
        """检查复制粘贴兼容性"""
        # 检查特殊空白字符
        special_spaces = [
            ('\u00a0', '不间断空格'),
            ('\u2003', '全角空格'),
            ('\u2002', '全角空格'),
        ]

        for char, name in special_spaces:
            if char in self.content:
                count = self.content.count(char)
                self.warnings.append(f"【警告】发现{count}个{name}，可能导致复制粘贴问题")

        # 检查是否有特殊的复制保护字符
        protection_patterns = [
            (r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '控制字符'),
        ]
        for pattern, name in protection_patterns:
            matches = re.findall(pattern, self.content)
            if matches:
                self.warnings.append(f"【警告】发现{len(matches)}个{name}，可能影响复制")

    def check_ai_expressions(self):
        """检测AI表达（集成ai_expression_detector）"""
        try:
            from ai_expression_detector import AIExpressionDetector
            
            detector = AIExpressionDetector(self.file_path)
            if not detector.read_file():
                return
            
            detector.detect_formal_patterns()
            detector.detect_robotic_phrases()
            detector.detect_lack_emotion()
            detector.detect_perfect_structure()
            detector.detect_generic_statements()
            
            if detector.ai_issues:
                self.warnings.append(f"【警告】发现{len(detector.ai_issues)}处疑似AI表达")
                
                # 按类型分组，显示前5个
                issues_by_type = {}
                for issue in detector.ai_issues:
                    issue_type = issue['type']
                    if issue_type not in issues_by_type:
                        issues_by_type[issue_type] = []
                    issues_by_type[issue_type].append(issue)
                
                for issue_type, issues in issues_by_type.items():
                    self.warnings.append(f"  - {issue_type}: {len(issues)}处")
                    for issue in issues[:2]:  # 每类显示2个
                        self.warnings.append(f"    原文: {issue['context'][:50]}...")
                        self.warnings.append(f"    建议: {issue['suggestion']}")
            else:
                self.info.append("【通过】未发现明显AI表达特征")
                
        except ImportError:
            self.warnings.append("【提示】AI检测模块不可用，跳过AI表达检测")
        except Exception as e:
            self.warnings.append(f"【提示】AI检测失败: {e}")

    def run_all_checks(self):
        """运行所有检查"""
        print("=" * 60)
        print(f"微信公众号文章检查工具")
        print(f"检查文件: {self.file_path}")
        print("=" * 60)
        print()

        # 读取文件
        if not self.read_file():
            self._print_report()
            return False

        # 执行各项检查
        self.check_garbled()
        self.check_completeness()
        self.check_images()
        self.check_typos()
        self.check_punctuation()
        self.check_html_compatibility()
        self.check_copy_paste()
        self.check_ai_expressions()  # 新增AI表达检测

        # 打印报告
        self._print_report()

        # 返回检查结果
        return len(self.errors) == 0

    def _print_report(self):
        """打印检查报告"""
        # 错误
        if self.errors:
            print("【错误】" + "-" * 50)
            for error in self.errors:
                print(f"  {error}")
            print()

        # 警告
        if self.warnings:
            print("【警告】" + "-" * 50)
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        # 通过项
        if self.info:
            print("【通过】" + "-" * 50)
            for info in self.info:
                print(f"  {info}")
            print()

        # 总结
        print("=" * 60)
        print("检查总结:")
        print(f"  错误: {len(self.errors)} 项")
        print(f"  警告: {len(self.warnings)} 项")
        print(f"  通过: {len(self.info)} 项")
        print("=" * 60)

        if len(self.errors) > 0:
            print("\n[结果] 检查未通过，请修复错误后重试")
            return False
        elif len(self.warnings) > 0:
            print("\n[结果] 检查通过，但有警告建议关注")
            return True
        else:
            print("\n[结果] 检查全部通过！")
            return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python scripts/check_article.py <文件路径>")
        print("示例: python scripts/check_article.py 美化文章_睡眠重要性_20250115.md")
        sys.exit(1)

    file_path = sys.argv[1]
    checker = ArticleChecker(file_path)
    success = checker.run_all_checks()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI表达检测与优化工具
功能：
1. 检测疑似AI生成的表达（过于正式、机械化、缺乏情感）
2. 提供拟人化表达建议
3. 优化AI感强的句子
4. 提升文章的"人味"和真实感

使用方法：
python scripts/ai_expression_detector.py <文件路径>
python scripts/ai_expression_detector.py 美化文章_睡眠重要性_20250115.md
"""

import re
from pathlib import Path


class AIExpressionDetector:
    """AI表达检测器"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = ""
        self.ai_issues = []
        self.suggestions = []

    def read_file(self):
        """读取文件内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except FileNotFoundError:
            print(f"错误: 文件不存在 - {self.file_path}")
            return False
        except Exception as e:
            print(f"错误: 读取文件失败 - {e}")
            return False

    def detect_formal_patterns(self):
        """检测过于正式的表达模式"""
        patterns = [
            # 过于正式的开头
            (r'^(本文|此文|本文章|在本文中)', "过于正式的开头，建议用'我'或'今天来聊聊'替代"),
            (r'^(根据|按照|依照)(研究|数据|报告|统计|调查)', "建议改为'我发现'或'我查了下数据'"),
            (r'^(综上所述|总而言之|总括而言|概括来说)', "建议改为'写到这里'或'最后想说'"),
            
            # 过于正式的连接词
            (r'^(此外|另外|加之|再者)', "建议改为'然后'、'还有'或'接着'"),
            (r'^(因此|因而|故而)', "建议改为'所以'或'然后'"),
            (r'^(由此可见|据此可知)', "建议改为'这说明'或'可以看出'"),
            (r'^(首先|其次|再次|最后)(，|、|:)', "建议改为'第一、第二、第三'"),
            
            # 过于正式的动词
            (r'旨在(致力于|致力于)', "建议改为'想要'或'为了'"),
            (r'促进(推动|推进)', "建议改为'帮助'或'让'"),
            (r'实施(执行|实行)', "建议改为'做'或'开始'"),
            (r'构建(建立|建设)', "建议改为'打造'或'建立'"),
            (r'提升(提高|增进)', "建议改为'让'或'使'"),
            
            # 过于正式的形容词
            (r'具有(拥有|具备)', "建议直接描述，如'有'"),
            (r'显著(明显|突出)', "建议改为'很'或'特别'"),
            (r'重要(关键|核心)', "建议改为'重要'或'关键'"),
            
            # 过于正式的句式
            (r'需要(注意|关注|重视)', "建议改为'要注意'或'别忽视'"),
            (r'(建议|推荐|提倡)(你|大家|用户)', "建议改为'试试'或'我建议'"),
            (r'(不仅|而且)(不仅|而且)', "建议改为'不光...还...'"),
            
            # 过于正式的结论
            (r'(得出结论|总结出|分析出)', "建议改为'发现'或'看出'"),
            (r'(研究表明|数据显示|调查发现)(:|：)', "建议改为'我发现'或'数据显示'"),
        ]

        for pattern, suggestion in patterns:
            matches = list(re.finditer(pattern, self.content, re.MULTILINE | re.IGNORECASE))
            if matches:
                for match in matches:
                    # 获取上下文
                    start = max(0, match.start() - 20)
                    end = min(len(self.content), match.end() + 20)
                    context = self.content[start:end].replace('\n', ' ')
                    self.ai_issues.append({
                        'type': '过于正式',
                        'text': match.group(),
                        'context': context,
                        'suggestion': suggestion,
                        'position': match.start()
                    })

    def detect_robotic_phrases(self):
        """检测机械化的表达"""
        patterns = [
            # 重复的结构
            (r'([^。！？]{0,20}?)(，|。|！|？)\1(，|。|！|？)', "避免重复的表达，尝试变换句式"),
            
            # 过度使用被动语态
            (r'(被|由|通过)(所|而)(处理|解决|完成|实现)', "改为主动语态，如'我们完成了'"),
            
            # 过度使用抽象名词
            (r'(实现|达成)(目标|目的)(的)(效果|成果)', "建议用具体例子替代"),
            
            # 过度使用成语
            (r'(不遗余力|竭尽全力|全力以赴|千方百计)', "建议用口语化表达，如'努力'"),
            
            # 过度使用书面语
            (r'(于是|因而|因此|从而)', "建议用'所以'或'然后'"),
            (r'(由于|因为)(所以|因此)', "建议直接说'因为...所以...'"),
        ]

        for pattern, suggestion in patterns:
            matches = list(re.finditer(pattern, self.content))
            if matches:
                for match in matches:
                    start = max(0, match.start() - 20)
                    end = min(len(self.content), match.end() + 20)
                    context = self.content[start:end].replace('\n', ' ')
                    self.ai_issues.append({
                        'type': '机械化',
                        'text': match.group(),
                        'context': context,
                        'suggestion': suggestion,
                        'position': match.start()
                    })

    def detect_lack_emotion(self):
        """检测缺乏情感的表达"""
        patterns = [
            # 没有第一人称
            (r'^(人们|大家|读者|用户)(应该|需要|可以)([^，。！？]{0,30}?)(，|。|！|？)', 
             "建议改为'我'或'我们'，增加个人视角"),
            
            # 没有情绪词汇
            (r'([^，。！？]{20,50}?)(，|。|！|？)([^，。！？]{20,50}?)(，|。|！|？)', 
             "句子过于平淡，建议加入情绪词如'我太懂了'、'说真的'"),
            
            # 过度客观
            (r'(根据|按照)([^，。！？]{0,20}?)(显示|表明)(，|。|！|？)', 
             "建议改为'我发现'或'我注意到'，增加个人观察"),
            
            # 缺乏疑问
            (r'([^？\n]{100,})', "这段话过长且没有疑问句，建议加入疑问增加互动"),
        ]

        for pattern, suggestion in patterns:
            matches = list(re.finditer(pattern, self.content))
            if matches:
                for match in matches:
                    # 只报告较长的匹配，避免误报
                    if len(match.group()) > 20:
                        start = max(0, match.start() - 20)
                        end = min(len(self.content), match.end() + 20)
                        context = self.content[start:end].replace('\n', ' ')
                        self.ai_issues.append({
                            'type': '缺乏情感',
                            'text': match.group()[:50] + '...',
                            'context': context,
                            'suggestion': suggestion,
                            'position': match.start()
                        })

    def detect_perfect_structure(self):
        """检测过于完美的结构（AI特征）"""
        lines = self.content.split('\n')
        
        # 检查是否每个小标题后的段落数量过于一致
        section_pattern = r'^#+\s+.+$'
        sections = []
        for i, line in enumerate(lines):
            if re.match(section_pattern, line):
                sections.append(i)
        
        if len(sections) > 2:
            # 计算每个部分的段落数
            paragraph_counts = []
            for i in range(len(sections) - 1):
                count = 0
                for j in range(sections[i] + 1, sections[i + 1]):
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        count += 1
                paragraph_counts.append(count)
            
            # 如果所有部分的段落数都相同（或相差不超过1），可能是AI生成
            if len(paragraph_counts) > 0:
                first_count = paragraph_counts[0]
                all_same = all(abs(count - first_count) <= 1 for count in paragraph_counts)
                if all_same:
                    self.ai_issues.append({
                        'type': '结构过于完美',
                        'text': '文章结构过于规律',
                        'context': f'每个小标题后约有{first_count}个段落',
                        'suggestion': '尝试打破规律，某些部分多写或少写几个段落，增加真实感',
                        'position': 0
                    })

    def detect_generic_statements(self):
        """检测泛泛而谈的表达"""
        patterns = [
            (r'([^，。！？]{0,30}?)(重要|关键|核心)([^，。！？]{0,30}?)(，|。|！|？)', 
             "过于空泛，建议具体说明为什么重要"),
            (r'(应该|需要)([^，。！？]{0,50}?)(，|。|！|？)', 
             "建议改为'试试'或'我建议'，更具指导性"),
            (r'(可以|能够)([^，。！？]{0,50}?)(，|。|！|？)', 
             "建议加入个人体验，如'我发现...'"),
            (r'(帮助|促进|提升)([^，。！？]{0,30}?)(，|。|！|？)', 
             "过于抽象，建议用具体例子替代"),
        ]

        for pattern, suggestion in patterns:
            matches = list(re.finditer(pattern, self.content))
            if matches:
                for match in matches:
                    if len(match.group()) > 20:
                        start = max(0, match.start() - 20)
                        end = min(len(self.content), match.end() + 20)
                        context = self.content[start:end].replace('\n', ' ')
                        self.ai_issues.append({
                            'type': '泛泛而谈',
                            'text': match.group()[:50] + '...',
                            'context': context,
                            'suggestion': suggestion,
                            'position': match.start()
                        })

    def detect_ai_sentence_patterns(self):
        """检测AI常见的句式模式"""
        # 检测过于规律的句子长度
        lines = [line.strip() for line in self.content.split('\n') if line.strip()]
        if len(lines) > 10:
            sentence_lengths = [len(line) for line in lines]
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            
            # 计算方差
            variance = sum((x - avg_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
            std_dev = variance ** 0.5
            
            # 如果标准差很小（小于平均长度的20%），说明句子长度过于一致
            if std_dev < avg_length * 0.2 and avg_length > 20:
                self.ai_issues.append({
                    'type': '句子长度过于一致',
                    'text': f'平均长度{avg_length:.1f}字，标准差{std_dev:.1f}字',
                    'context': '建议长短句交替，增加节奏感',
                    'suggestion': '有些句子写长一点，有些写短一点，让文章更自然',
                    'position': 0
                })

    def provide_humanizing_suggestions(self):
        """提供拟人化表达建议"""
        suggestions = [
            {
                'pattern': '本文',
                'replacement': '今天这篇文章',
                'reason': '更口语化，像人在说话'
            },
            {
                'pattern': '根据研究',
                'replacement': '我发现',
                'reason': '增加个人视角，更有真实感'
            },
            {
                'pattern': '综上所述',
                'replacement': '写到这里',
                'reason': '更自然，像在聊天'
            },
            {
                'pattern': '因此',
                'replacement': '所以',
                'reason': '更口语化'
            },
            {
                'pattern': '应该',
                'replacement': '试试',
                'reason': '更温柔，像朋友建议'
            },
            {
                'pattern': '非常重要',
                'replacement': '特别重要',
                'reason': '更口语化'
            },
            {
                'pattern': '实现目标',
                'replacement': '达到目标',
                'reason': '更直接'
            },
            {
                'pattern': '促进健康',
                'replacement': '让身体更健康',
                'reason': '更具体'
            },
            {
                'pattern': '用户',
                'replacement': '你',
                'reason': '更亲切，像在对话'
            },
            {
                'pattern': '读者',
                'replacement': '你',
                'reason': '增加代入感'
            },
        ]
        
        for item in suggestions:
            pattern = item['pattern']
            if re.search(pattern, self.content):
                self.suggestions.append(item)

    def run_detection(self):
        """运行检测"""
        print("=" * 60)
        print("AI表达检测工具")
        print(f"检测文件: {self.file_path}")
        print("=" * 60)
        print()

        if not self.read_file():
            return False

        # 执行各项检测
        self.detect_formal_patterns()
        self.detect_robotic_phrases()
        self.detect_lack_emotion()
        self.detect_perfect_structure()
        self.detect_generic_statements()
        self.detect_ai_sentence_patterns()
        self.provide_humanizing_suggestions()

        # 打印报告
        self._print_report()

        return len(self.ai_issues) == 0

    def _print_report(self):
        """打印检测报告"""
        # 按类型分组
        issues_by_type = {}
        for issue in self.ai_issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # 打印问题
        if self.ai_issues:
            print("【疑似AI表达】" + "-" * 50)
            for issue_type, issues in issues_by_type.items():
                print(f"\n【{issue_type}】({len(issues)}处)")
                for i, issue in enumerate(issues[:3], 1):  # 每类只显示前3个
                    print(f"  {i}. 原文: {issue['context']}")
                    print(f"     建议: {issue['suggestion']}")
                    print()
                if len(issues) > 3:
                    print(f"  ... 还有{len(issues) - 3}处\n")
            print()

        # 打印拟人化建议
        if self.suggestions:
            print("【拟人化建议】" + "-" * 50)
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"  {i}. 将'{suggestion['pattern']}'改为'{suggestion['replacement']}'")
                print(f"     原因: {suggestion['reason']}")
                print()

        # 总结
        print("=" * 60)
        print("检测总结:")
        print(f"  疑似AI表达: {len(self.ai_issues)} 处")
        print(f"  拟人化建议: {len(self.suggestions)} 条")
        print("=" * 60)

        if len(self.ai_issues) > 0:
            print("\n[结果] 发现疑似AI表达，建议优化后重新检测")
        elif len(self.suggestions) > 0:
            print("\n[结果] 未发现明显AI表达，但有优化建议")
        else:
            print("\n[结果] 表达自然，未发现AI特征！")

        return len(self.ai_issues) == 0


def main():
    """主函数"""
    import sys
    if len(sys.argv) < 2:
        print("使用方法: python scripts/ai_expression_detector.py <文件路径>")
        print("示例: python scripts/ai_expression_detector.py 美化文章_睡眠重要性_20250115.md")
        sys.exit(1)

    file_path = sys.argv[1]
    detector = AIExpressionDetector(file_path)
    detector.run_detection()


if __name__ == '__main__':
    main()

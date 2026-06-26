#!/usr/bin/env python3
"""
新闻摘要生成脚本
支持提取式和生成式两种摘要方法

使用方法:
    # 提取式摘要(快速)
    python news_summarizer.py --method extractive --input news_data.json --output summary.json

    # 生成式摘要(质量更好)
    python news_summarizer.py --method abstractive --input news_data.json --output summary.json
"""

import json
import argparse
from typing import List, Dict, Optional
import re


# 提取式摘要依赖
try:
    import jieba
    import jieba.analyse
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("警告: jieba 未安装,提取式摘要功能不可用")

# 生成式摘要依赖
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("警告: transformers 未安装,生成式摘要功能不可用")


class NewsSummarizer:
    """新闻摘要生成器"""

    def __init__(self):
        self.extractive_model = None
        self.abstractive_pipeline = None

    def summarize_extractive(self, text: str, max_sentences: int = 3) -> str:
        """
        提取式摘要:基于关键词提取关键句

        Args:
            text: 原文文本
            max_sentences: 最多提取的句子数

        Returns:
            摘要文本
        """
        if not JIEBA_AVAILABLE:
            raise ImportError("需要安装 jieba 库: pip install jieba")

        # 提取关键词
        keywords = jieba.analyse.extract_tags(text, topK=10, withWeight=True)

        if not keywords:
            return text[:200] + "..."

        # 按句号、问号、感叹号分割句子
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return text[:200] + "..."

        # 计算每个句子的得分(包含关键词的句子得分更高)
        sentence_scores = []
        keyword_set = set([kw[0] for kw in keywords])

        for sentence in sentences:
            score = 0
            # 包含关键词的句子得分更高
            for keyword, weight in keywords:
                if keyword in sentence:
                    score += weight * 10
            # 句子长度适中得分更高
            if 20 <= len(sentence) <= 100:
                score += 5
            sentence_scores.append((sentence, score))

        # 按得分排序并选择前 N 个句子
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        selected_sentences = [s[0] for s in sentence_scores[:max_sentences]]

        # 保持原始顺序
        summary_sentences = []
        for sentence in sentences:
            if sentence in selected_sentences and sentence not in summary_sentences:
                summary_sentences.append(sentence)

        return "。".join(summary_sentences) + "。"

    def summarize_abstractive(self, text: str, max_length: int = 150) -> str:
        """
        生成式摘要:使用预训练模型生成摘要

        Args:
            text: 原文文本
            max_length: 摘要最大长度

        Returns:
            摘要文本
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("需要安装 transformers 库: pip install transformers torch")

        # 初始化摘要模型(仅第一次)
        if self.abstractive_pipeline is None:
            print("正在加载摘要模型(首次加载需要时间)...")
            # 使用中文摘要模型
            self.abstractive_pipeline = pipeline(
                "summarization",
                model="google/mt5-small-chinese",
                device=-1  # 使用 CPU
            )

        # 限制输入长度,避免超时
        if len(text) > 512:
            text = text[:512]

        # 生成摘要
        try:
            summary = self.abstractive_pipeline(
                text,
                max_length=max_length,
                min_length=30,
                do_sample=False
            )
            return summary[0]['summary_text']
        except Exception as e:
            print(f"生成式摘要失败: {str(e)}")
            # 降级到提取式摘要
            if JIEBA_AVAILABLE:
                return self.summarize_extractive(text)
            return text[:200] + "..."

    def generate_summary_for_news(self, news_data: List[Dict], method: str = 'extractive') -> List[Dict]:
        """
        为新闻数据生成摘要

        Args:
            news_data: 新闻数据列表
            method: 摘要方法 'extractive' 或 'abstractive'

        Returns:
            带有摘要的新闻数据
        """
        summarized_news = []

        for news_item in news_data:
            title = news_item.get('title', '')

            # 如果新闻内容为空,使用标题作为摘要
            if not title:
                news_item['summary'] = news_item.get('summary', '')
                summarized_news.append(news_item)
                continue

            try:
                if method == 'extractive':
                    # 提取式摘要:使用标题本身(简洁)
                    summary = title[:100]
                elif method == 'abstractive':
                    # 生成式摘要:基于标题生成摘要
                    summary = self.summarize_abstractive(title, max_length=100)
                else:
                    raise ValueError(f"不支持的摘要方法: {method}")

                news_item['summary'] = summary

            except Exception as e:
                print(f"摘要生成失败({title[:30]}...): {str(e)}")
                # 使用标题作为摘要
                news_item['summary'] = title[:100]

            summarized_news.append(news_item)

        return summarized_news

    def save_to_json(self, news_data: List[Dict], output_file: str):
        """保存摘要数据到 JSON 文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 摘要数据已保存到 {output_file}")

    def generate_markdown_report(self, news_data: List[Dict], output_file: str):
        """生成 Markdown 格式的报告"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 新闻热点摘要报告\n\n")
            f.write(f"生成时间: {news_data[0].get('timestamp', 'N/A') if news_data else 'N/A'}\n\n")
            f.write(f"总计: {len(news_data)} 条新闻\n\n")

            # 按平台分组
            platforms = {}
            for item in news_data:
                platform = item.get('platform', 'unknown')
                if platform not in platforms:
                    platforms[platform] = []
                platforms[platform].append(item)

            # 按平台输出
            for platform, items in platforms.items():
                platform_names = {
                    'weibo': '微博热搜',
                    'zhihu': '知乎热榜',
                    'bilibili': 'B站热门',
                    'douyin': '抖音热点',
                    'toutiao': '今日头条',
                    'tencent': '腾讯新闻',
                    'thepaper': '澎湃新闻'
                }
                platform_title = platform_names.get(platform, platform)

                f.write(f"## {platform_title}\n\n")

                for i, item in enumerate(items):
                    rank = item.get('rank', i + 1)
                    title = item.get('title', 'N/A')
                    summary = item.get('summary', 'N/A')
                    url = item.get('url', '')
                    hot = item.get('hot', 'N/A')
                    timestamp = item.get('timestamp', 'N/A')

                    f.write(f"### {rank}. {title}\n\n")
                    f.write(f"**摘要**: {summary}\n\n")
                    if hot != 'N/A':
                        f.write(f"**热度**: {hot}\n\n")
                    f.write(f"**来源**: [{platform_title}]({url})\n\n")
                    f.write(f"**时间**: {timestamp}\n\n")
                    f.write("---\n\n")

        print(f"✓ Markdown 报告已保存到 {output_file}")


def main():
    parser = argparse.ArgumentParser(description='新闻摘要生成工具')
    parser.add_argument('--method', type=str, choices=['extractive', 'abstractive'],
                        default='extractive', help='摘要方法: extractive(提取式) 或 abstractive(生成式)')
    parser.add_argument('--input', type=str, required=True, help='输入新闻数据文件(JSON)')
    parser.add_argument('--output', type=str, default='summary.json', help='输出文件路径(JSON)')
    parser.add_argument('--report', type=str, help='生成 Markdown 报告文件路径(可选)')
    parser.add_argument('--max-sentences', type=int, default=3,
                        help='提取式摘要的最大句子数')

    args = parser.parse_args()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
    except Exception as e:
        print(f"错误: 无法读取输入文件 {args.input}: {str(e)}")
        return

    # 生成摘要
    summarizer = NewsSummarizer()
    summarized_news = summarizer.generate_summary_for_news(news_data, args.method)

    # 保存 JSON
    summarizer.save_to_json(summarized_news, args.output)

    # 生成 Markdown 报告
    if args.report:
        summarizer.generate_markdown_report(summarized_news, args.report)

    print(f"\n✓ 成功为 {len(summarized_news)} 条新闻生成摘要")


if __name__ == "__main__":
    main()

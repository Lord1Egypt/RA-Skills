#!/usr/bin/env python3
"""
pans-meeting-summarizer - 会议智能总结工具
将会议录音/文字转为结构化纪要、行动项和客户洞察
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# 尝试导入可选依赖
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class MeetingSummarizer:
    """会议总结器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化总结器
        
        Args:
            api_key: OpenAI API密钥（可选，默认从环境变量读取）
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
    
    def transcribe_audio(self, audio_path: str, model: str = "base") -> str:
        """
        音频转文字
        
        Args:
            audio_path: 音频文件路径
            model: Whisper模型大小 (tiny/base/small/medium/large)
        
        Returns:
            转录文本
        """
        if not WHISPER_AVAILABLE:
            raise ImportError(
                "未安装 Whisper。请运行: pip install openai-whisper"
            )
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        print(f"正在转录音频: {audio_path} (使用模型: {model})...", file=sys.stderr)
        
        model_obj = whisper.load_model(model)
        result = model_obj.transcribe(audio_path)
        
        return result["text"]
    
    def read_text_file(self, text_path: str) -> str:
        """
        读取文本文件
        
        Args:
            text_path: 文本文件路径
        
        Returns:
            文本内容
        """
        if not os.path.exists(text_path):
            raise FileNotFoundError(f"文本文件不存在: {text_path}")
        
        with open(text_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def summarize(self, transcript: str, context: str = "销售会议") -> Dict[str, Any]:
        """
        生成结构化会议纪要
        
        Args:
            transcript: 会议转录文本
            context: 会议上下文/类型
        
        Returns:
            结构化纪要数据
        """
        if not self.client:
            # 无API时返回基础结构
            return self._fallback_summary(transcript)
        
        prompt = f"""请分析以下会议记录，生成结构化的会议纪要。

会议类型：{context}

会议记录：
{transcript}

请按以下JSON格式输出（不要添加markdown代码块标记）：
{{
    "meeting_summary": {{
        "topic": "会议主题",
        "date": "会议日期（如未提及则填今天）",
        "participants": ["参与人列表"],
        "key_points": ["讨论要点1", "讨论要点2"],
        "decisions": ["决策事项1", "决策事项2"],
        "next_steps": ["下一步计划"]
    }},
    "action_items": [
        {{
            "task": "待办事项描述",
            "owner": "负责人",
            "priority": "high/medium/low",
            "due_date": "截止日期（如未提及则填待定）"
        }}
    ],
    "customer_insights": {{
        "budget": "预算情况分析",
        "decision_makers": ["决策链关键人物"],
        "competitors": ["竞品情况"],
        "pain_points": ["痛点需求"],
        "buying_signals": ["购买信号"],
        "concerns": ["顾虑点"]
    }},
    "follow_up_suggestions": ["后续跟进建议"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个专业的销售会议分析师，擅长提取关键信息和洞察。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            print(f"警告: API调用失败 ({e})，使用基础分析", file=sys.stderr)
            return self._fallback_summary(transcript)
    
    def _fallback_summary(self, transcript: str) -> Dict[str, Any]:
        """无API时的降级处理"""
        lines = transcript.strip().split('\n')
        word_count = len(transcript)
        
        return {
            "meeting_summary": {
                "topic": "待分析会议",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "participants": [],
                "key_points": ["请配置OPENAI_API_KEY以启用智能分析"],
                "decisions": [],
                "next_steps": []
            },
            "action_items": [],
            "customer_insights": {
                "budget": "未分析",
                "decision_makers": [],
                "competitors": [],
                "pain_points": [],
                "buying_signals": [],
                "concerns": []
            },
            "follow_up_suggestions": [
                "配置OPENAI_API_KEY环境变量以启用完整功能"
            ],
            "raw_transcript": transcript[:1000] + "..." if len(transcript) > 1000 else transcript,
            "word_count": word_count
        }
    
    def format_markdown(self, data: Dict[str, Any]) -> str:
        """
        格式化为Markdown
        
        Args:
            data: 结构化纪要数据
        
        Returns:
            Markdown格式文本
        """
        lines = []
        
        # 会议纪要
        summary = data.get("meeting_summary", {})
        lines.append("# 📋 会议纪要\n")
        lines.append(f"**主题**: {summary.get('topic', '未命名')}")
        lines.append(f"**日期**: {summary.get('date', datetime.now().strftime('%Y-%m-%d'))}")
        lines.append(f"**参与人**: {', '.join(summary.get('participants', [])) or '未记录'}\n")
        
        if summary.get('key_points'):
            lines.append("## 💡 讨论要点")
            for point in summary['key_points']:
                lines.append(f"- {point}")
            lines.append("")
        
        if summary.get('decisions'):
            lines.append("## ✅ 决策事项")
            for decision in summary['decisions']:
                lines.append(f"- {decision}")
            lines.append("")
        
        if summary.get('next_steps'):
            lines.append("## 📅 下一步计划")
            for step in summary['next_steps']:
                lines.append(f"- {step}")
            lines.append("")
        
        # 行动项
        action_items = data.get("action_items", [])
        if action_items:
            lines.append("## 🎯 行动项\n")
            lines.append("| 待办事项 | 负责人 | 优先级 | 截止日期 |")
            lines.append("|---------|-------|--------|---------|")
            for item in action_items:
                task = item.get('task', '未描述')
                owner = item.get('owner', '待分配')
                priority = item.get('priority', 'medium')
                due = item.get('due_date', '待定')
                lines.append(f"| {task} | {owner} | {priority} | {due} |")
            lines.append("")
        
        # 客户洞察
        insights = data.get("customer_insights", {})
        if any(insights.values()):
            lines.append("## 🔍 客户洞察\n")
            
            if insights.get('budget'):
                lines.append(f"**预算情况**: {insights['budget']}\n")
            
            if insights.get('decision_makers'):
                lines.append(f"**决策链**: {', '.join(insights['decision_makers'])}\n")
            
            if insights.get('competitors'):
                lines.append(f"**竞品情况**: {', '.join(insights['competitors'])}\n")
            
            if insights.get('pain_points'):
                lines.append("**痛点需求**:")
                for pain in insights['pain_points']:
                    lines.append(f"- {pain}")
                lines.append("")
            
            if insights.get('buying_signals'):
                lines.append("**购买信号**:")
                for signal in insights['buying_signals']:
                    lines.append(f"- {signal}")
                lines.append("")
            
            if insights.get('concerns'):
                lines.append("**顾虑点**:")
                for concern in insights['concerns']:
                    lines.append(f"- {concern}")
                lines.append("")
        
        # 跟进建议
        suggestions = data.get("follow_up_suggestions", [])
        if suggestions:
            lines.append("## 🚀 跟进建议\n")
            for sug in suggestions:
                lines.append(f"- {sug}")
            lines.append("")
        
        # 元数据
        lines.append("---")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return '\n'.join(lines)
    
    def sync_to_crm(self, data: Dict[str, Any], client_name: str) -> bool:
        """
        同步到CRM系统（预留接口）
        
        Args:
            data: 纪要数据
            client_name: 客户名称
        
        Returns:
            是否成功
        """
        # TODO: 实现实际的CRM集成
        # 这里可以对接Salesforce、HubSpot、纷享销客等CRM系统
        
        print(f"CRM同步功能待实现 - 客户: {client_name}", file=sys.stderr)
        print(f"数据摘要: {json.dumps(data.get('meeting_summary', {}), ensure_ascii=False)}", file=sys.stderr)
        
        # 返回False表示功能未实现
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="会议智能总结工具 - 将录音/文字转为结构化纪要",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从音频生成纪要
  %(prog)s --audio meeting.m4a --output notes.md
  
  # 从文字记录生成纪要
  %(prog)s --text transcript.txt --output notes.md
  
  # 生成纪要并同步CRM
  %(prog)s --audio meeting.m4a --sync-crm --client "腾讯云"
  
  # 指定输出格式
  %(prog)s --text transcript.txt --format json --output notes.json
"""
    )
    
    parser.add_argument(
        "--audio",
        help="音频文件路径（支持 m4a/wav/mp3）"
    )
    
    parser.add_argument(
        "--text",
        help="文字记录文件路径"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（默认输出到stdout）"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="输出格式（默认: markdown）"
    )
    
    parser.add_argument(
        "--sync-crm",
        action="store_true",
        help="同步更新CRM系统"
    )
    
    parser.add_argument(
        "--client",
        help="客户名称（CRM同步时需要）"
    )
    
    parser.add_argument(
        "--context",
        default="销售会议",
        help="会议上下文/类型（默认: 销售会议）"
    )
    
    parser.add_argument(
        "--whisper-model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper模型大小（默认: base）"
    )
    
    parser.add_argument(
        "--api-key",
        help="OpenAI API密钥（也可通过OPENAI_API_KEY环境变量设置）"
    )
    
    args = parser.parse_args()
    
    # 验证输入
    if not args.audio and not args.text:
        parser.error("必须指定 --audio 或 --text 之一")
    
    if args.sync_crm and not args.client:
        parser.error("CRM同步需要指定 --client 参数")
    
    # 初始化总结器
    summarizer = MeetingSummarizer(api_key=args.api_key)
    
    # 获取转录文本
    try:
        if args.audio:
            transcript = summarizer.transcribe_audio(
                args.audio,
                model=args.whisper_model
            )
        else:
            transcript = summarizer.read_text_file(args.text)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 生成纪要
    try:
        data = summarizer.summarize(transcript, context=args.context)
    except Exception as e:
        print(f"警告: 分析失败 ({e})，使用基础模式", file=sys.stderr)
        data = summarizer._fallback_summary(transcript)
    
    # 同步CRM
    if args.sync_crm:
        summarizer.sync_to_crm(data, args.client)
    
    # 格式化输出
    if args.format == "json":
        output = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        output = summarizer.format_markdown(data)
    
    # 写入输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"纪要已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
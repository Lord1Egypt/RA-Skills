#!/usr/bin/env python3
"""
学习计划生成脚本
功能：创建个性化英语词汇学习计划
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

class LearningPlanGenerator:
    """学习计划生成器"""
    
    def __init__(self, days, words_per_day, level="intermediate"):
        self.days = days
        self.words_per_day = words_per_day
        self.level = level
        self.plan = {}
        
        # 词库路径（示例）
        self.vocabulary_files = {
            "beginner": "./references/vocabulary_lists/beginner.json",
            "intermediate": "./references/vocabulary_lists/intermediate.json",
            "advanced": "./references/vocabulary_lists/advanced.json"
        }
    
    def load_vocabulary(self):
        """
        加载词库
        注：实际使用时需要从词库文件加载
        """
        # 模拟词库数据
        total_words = self.days * self.words_per_day
        
        # 返回模拟单词列表（实际应从文件读取）
        return [f"word_{i}" for i in range(1, total_words + 1)]
    
    def generate_daily_plan(self, start_date=None):
        """生成每日学习计划"""
        if start_date is None:
            start_date = datetime.now().date()
        
        vocabulary = self.load_vocabulary()
        
        self.plan = {
            "meta": {
                "total_days": self.days,
                "words_per_day": self.words_per_day,
                "total_words": len(vocabulary),
                "level": self.level,
                "start_date": start_date.isoformat(),
                "end_date": (start_date + timedelta(days=self.days-1)).isoformat()
            },
            "schedule": {}
        }
        
        # 分配每日单词
        for day in range(self.days):
            current_date = start_date + timedelta(days=day)
            start_idx = day * self.words_per_day
            end_idx = start_idx + self.words_per_day
            
            daily_words = vocabulary[start_idx:end_idx]
            
            self.plan["schedule"][current_date.isoformat()] = {
                "day": day + 1,
                "words": daily_words,
                "tasks": [
                    "学习新单词（观看图片+理解释义）",
                    "跟读单词发音3遍",
                    "为每个单词造1个句子",
                    "完成单词测试"
                ],
                "estimated_time": f"{len(daily_words) * 3} 分钟",
                "completed": False
            }
        
        return self.plan
    
    def generate_ebbinghaus_schedule(self):
        """生成艾宾浩斯复习时间表"""
        # 艾宾浩斯复习间隔（天数）
        intervals = [0, 1, 2, 4, 7, 15, 30]
        
        review_schedule = {}
        
        for date_str, daily_plan in self.plan["schedule"].items():
            learn_date = datetime.fromisoformat(date_str).date()
            words = daily_plan["words"]
            
            for interval in intervals:
                review_date = learn_date + timedelta(days=interval)
                review_key = review_date.isoformat()
                
                if review_key not in review_schedule:
                    review_schedule[review_key] = {
                        "tasks": [],
                        "word_count": 0
                    }
                
                if interval == 0:
                    task_type = "新学"
                else:
                    task_type = f"第{intervals.index(interval)}次复习"
                
                review_schedule[review_key]["tasks"].append({
                    "type": task_type,
                    "words": words,
                    "source_date": date_str
                })
                review_schedule[review_key]["word_count"] += len(words)
        
        return review_schedule
    
    def save_plan(self, output_dir="./plans"):
        """保存学习计划"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON格式计划
        json_file = output_path / f"learning_plan_{timestamp}.json"
        json_file.write_text(json.dumps(self.plan, ensure_ascii=False, indent=2), 
                            encoding='utf-8')
        
        # 保存Markdown格式计划
        md_content = self._generate_plan_markdown()
        md_file = output_path / f"learning_plan_{timestamp}.md"
        md_file.write_text(md_content, encoding='utf-8')
        
        # 保存复习时间表
        review_schedule = self.generate_ebbinghaus_schedule()
        review_file = output_path / f"review_schedule_{timestamp}.json"
        review_file.write_text(json.dumps(review_schedule, ensure_ascii=False, indent=2),
                              encoding='utf-8')
        
        print(f"✅ 学习计划已生成：")
        print(f"   - 计划文件：{json_file}")
        print(f"   - 可读版本：{md_file}")
        print(f"   - 复习时间表：{review_file}")
        
        return str(json_file), str(md_file), str(review_file)
    
    def _generate_plan_markdown(self):
        """生成Markdown格式的计划"""
        content = f"""# 📅 英语词汇学习计划

## 📊 计划概览

- **总天数**: {self.plan['meta']['total_days']} 天
- **每日单词**: {self.plan['meta']['words_per_day']} 个
- **总单词数**: {self.plan['meta']['total_words']} 个
- **难度级别**: {self.plan['meta']['level']}
- **开始日期**: {self.plan['meta']['start_date']}
- **结束日期**: {self.plan['meta']['end_date']}

---

## 📋 每日学习安排

"""
        
        for date_str, daily_plan in self.plan["schedule"].items():
            content += f"""### Day {daily_plan['day']} - {date_str}

**学习单词** ({daily_plan['estimated_time']}):

"""
            for word in daily_plan['words']:
                content += f"- {word}\n"
            
            content += "\n**今日任务**:\n"
            for task in daily_plan['tasks']:
                content += f"- [ ] {task}\n"
            
            content += "\n---\n\n"
        
        content += """## 📈 学习建议

1. **固定时间**：每天同一时间学习，形成习惯
2. **主动回忆**：先看图片猜单词，再看答案
3. **造句练习**：用新单词造3个句子
4. **及时复习**：按艾宾浩斯时间表复习
5. **记录进度**：标记已掌握/模糊/忘记

---

*坚持就是胜利！💪*
"""
        
        return content


def main():
    parser = argparse.ArgumentParser(description='创建英语词汇学习计划')
    parser.add_argument('--days', type=int, required=True, help='学习天数')
    parser.add_argument('--words-per-day', type=int, required=True, help='每日单词数')
    parser.add_argument('--level', default='intermediate',
                       choices=['beginner', 'intermediate', 'advanced'],
                       help='难度级别')
    parser.add_argument('--start-date', help='开始日期（YYYY-MM-DD格式，默认今天）')
    parser.add_argument('--output', default='./plans', help='输出目录')
    
    args = parser.parse_args()
    
    # 解析开始日期
    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
    else:
        start_date = None
    
    # 生成计划
    generator = LearningPlanGenerator(args.days, args.words_per_day, args.level)
    generator.generate_daily_plan(start_date)
    generator.save_plan(args.output)


if __name__ == "__main__":
    main()

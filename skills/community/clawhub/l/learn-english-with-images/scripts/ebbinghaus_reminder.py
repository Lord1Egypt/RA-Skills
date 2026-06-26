#!/usr/bin/env python3
"""
艾宾浩斯复习提醒脚本
功能：基于遗忘曲线安排单词复习
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path


class EbbinghausReminder:
    """艾宾浩斯遗忘曲线复习提醒器"""
    
    def __init__(self, learning_log_path="./learning_log.json"):
        self.log_path = Path(learning_log_path)
        self.learning_log = self._load_log()
        
        # 艾宾浩斯遗忘曲线复习间隔（分钟/小时/天）
        self.review_intervals = [
            ("20分钟", timedelta(minutes=20)),
            ("1小时", timedelta(hours=1)),
            ("9小时", timedelta(hours=9)),
            ("1天", timedelta(days=1)),
            ("2天", timedelta(days=2)),
            ("6天", timedelta(days=6)),
            ("31天", timedelta(days=31)),
        ]
    
    def _load_log(self):
        """加载学习记录"""
        if self.log_path.exists():
            with open(self.log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"words": {}, "history": []}
    
    def _save_log(self):
        """保存学习记录"""
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(self.learning_log, ensure_ascii=False, indent=2)
    
    def record_learning(self, word, phonetic="", meaning="", image_path=""):
        """记录新学习的单词"""
        now = datetime.now()
        
        self.learning_log["words"][word] = {
            "learned_at": now.isoformat(),
            "phonetic": phonetic,
            "meaning": meaning,
            "image_path": image_path,
            "review_history": [],
            "next_review": None,
            "mastery_level": 0,  # 0-5 掌握程度
            "review_count": 0
        }
        
        self.learning_log["history"].append({
            "action": "learn",
            "word": word,
            "timestamp": now.isoformat()
        })
        
        self._save_log()
        print(f"✅ 已记录学习：{word}")
    
    def calculate_next_review(self, learned_time, review_count):
        """计算下次复习时间"""
        if review_count >= len(self.review_intervals):
            # 超过预设复习次数，使用最长间隔
            interval = self.review_intervals[-1][1]
        else:
            interval = self.review_intervals[review_count][1]
        
        return learned_time + interval
    
    def get_today_reviews(self):
        """获取今天需要复习的单词"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        reviews_needed = []
        
        for word, data in self.learning_log["words"].items():
            learned_time = datetime.fromisoformat(data["learned_at"])
            
            # 检查每次复习节点
            for i, (label, interval) in enumerate(self.review_intervals):
                review_time = learned_time + interval
                
                # 如果复习时间在今天且尚未复习
                if today_start <= review_time < today_end:
                    if len(data["review_history"]) <= i:
                        reviews_needed.append({
                            "word": word,
                            "review_type": f"第{i+1}次复习",
                            "scheduled_time": review_time.isoformat(),
                            "data": data
                        })
        
        return reviews_needed
    
    def mark_reviewed(self, word, mastery_level=None):
        """标记单词已复习"""
        if word not in self.learning_log["words"]:
            print(f"⚠️ 未找到单词：{word}")
            return
        
        now = datetime.now()
        word_data = self.learning_log["words"][word]
        
        # 记录复习
        word_data["review_history"].append({
            "reviewed_at": now.isoformat(),
            "mastery_level": mastery_level
        })
        
        word_data["review_count"] = len(word_data["review_history"])
        
        if mastery_level is not None:
            word_data["mastery_level"] = mastery_level
        
        # 计算下次复习时间
        learned_time = datetime.fromisoformat(word_data["learned_at"])
        word_data["next_review"] = self.calculate_next_review(
            learned_time, word_data["review_count"]
        ).isoformat()
        
        # 记录到历史
        self.learning_log["history"].append({
            "action": "review",
            "word": word,
            "timestamp": now.isoformat(),
            "mastery_level": mastery_level
        })
        
        self._save_log()
        print(f"✅ 已标记复习：{word}")
    
    def generate_review_report(self):
        """生成复习报告"""
        now = datetime.now()
        
        # 统计数据
        total_words = len(self.learning_log["words"])
        total_reviews = len([h for h in self.learning_log["history"] 
                           if h["action"] == "review"])
        
        # 掌握程度分布
        mastery_distribution = {
            "未复习": 0,
            "模糊": 0,
            "熟悉": 0,
            "掌握": 0
        }
        
        for word, data in self.learning_log["words"].items():
            level = data["mastery_level"]
            if level == 0:
                mastery_distribution["未复习"] += 1
            elif level <= 2:
                mastery_distribution["模糊"] += 1
            elif level <= 4:
                mastery_distribution["熟悉"] += 1
            else:
                mastery_distribution["掌握"] += 1
        
        # 生成报告
        report = f"""# 📊 艾宾浩斯复习报告

**生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}

---

## 📈 学习统计

- **已学单词**: {total_words} 个
- **总复习次数**: {total_reviews} 次
- **平均每词复习**: {total_reviews/total_words:.1f} 次（{total_words > 0}）

---

## 🎯 掌握程度分布

| 程度 | 数量 | 占比 | 进度条 |
|------|------|------|--------|
"""
        
        for level, count in mastery_distribution.items():
            percentage = (count / total_words * 100) if total_words > 0 else 0
            bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            report += f"| {level} | {count} | {percentage:.1f}% | {bar} |\n"
        
        # 今日待复习
        today_reviews = self.get_today_reviews()
        report += f"""
---

## 📅 今日待复习 ({len(today_reviews)} 个)

"""
        
        if today_reviews:
            for i, review in enumerate(today_reviews, 1):
                scheduled = datetime.fromisoformat(review["scheduled_time"])
                status = "⏰ 已到期" if scheduled < now else "⏳ 待复习"
                report += f"{i}. **{review['word']}** - {review['review_type']} {status}\n"
        else:
            report += "_今天没有需要复习的单词_\n"
        
        report += """
---

## 💡 复习建议

1. **优先复习**：已到期的单词（标记为 ⏰）
2. **主动回忆**：先看图片回忆单词，再看答案
3. **标记掌握程度**：0-忘记，1-模糊，2-熟悉，3-掌握
4. **坚持复习**：按曲线复习，长期记忆效果最佳

---

*根据艾宾浩斯遗忘曲线，科学复习让记忆更牢固！🧠*
"""
        
        return report
    
    def save_review_report(self, output_dir="./reports"):
        """保存复习报告"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"review_report_{timestamp}.md"
        
        report_content = self.generate_review_report()
        report_file.write_text(report_content, encoding='utf-8')
        
        print(f"✅ 复习报告已生成：{report_file}")
        return str(report_file)


def main():
    parser = argparse.ArgumentParser(description='艾宾浩斯复习提醒')
    parser.add_argument('--action', required=True,
                       choices=['learn', 'review', 'today', 'report'],
                       help='操作类型')
    parser.add_argument('--word', help='单词')
    parser.add_argument('--mastery', type=int, choices=range(6),
                       help='掌握程度（0-5）')
    parser.add_argument('--log', default='./learning_log.json',
                       help='学习记录文件路径')
    parser.add_argument('--output', default='./reports',
                       help='报告输出目录')
    
    args = parser.parse_args()
    
    reminder = EbbinghausReminder(args.log)
    
    if args.action == "learn":
        if not args.word:
            print("❌ 请提供要学习的单词")
            return
        reminder.record_learning(args.word)
    
    elif args.action == "review":
        if not args.word:
            print("❌ 请提供要复习的单词")
            return
        reminder.mark_reviewed(args.word, args.mastery)
    
    elif args.action == "today":
        reviews = reminder.get_today_reviews()
        print(f"\n📅 今日待复习单词：{len(reviews)} 个\n")
        for i, review in enumerate(reviews, 1):
            print(f"{i}. {review['word']} - {review['review_type']}")
    
    elif args.action == "report":
        reminder.save_review_report(args.output)


if __name__ == "__main__":
    main()

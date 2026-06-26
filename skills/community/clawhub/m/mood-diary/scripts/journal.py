#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心情日记 - 核心模块
自然语言日记记录、情绪识别、标签提取、CRUD操作
"""

import json
import os
import re
import sys
import tempfile
import uuid
from calendar import monthcalendar
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 数据存储路径
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/journal"))
DATA_FILE = DATA_DIR / "entries.json"

# 隐私保护：确保数据文件权限仅限当前用户
_PRIVATE_PERMS = 0o600  # rw-------
_PRIVATE_DIR_PERMS = 0o700  # rwx------

# 加载情绪配置
def load_mood_config() -> Dict:
    """加载情绪配置文件"""
    config_path = Path(__file__).parent.parent / "assets" / "moods.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 默认配置
        return {
            "moods": {
                "开心": {"score_range": [7, 9], "keywords": ["开心", "高兴"], "emoji": "😊"},
                "平静": {"score_range": [5, 7], "keywords": ["平静", "平和"], "emoji": "😌"},
                "兴奋": {"score_range": [8, 10], "keywords": ["兴奋", "激动"], "emoji": "🤩"},
                "焦虑": {"score_range": [3, 5], "keywords": ["焦虑", "担心"], "emoji": "😰"},
                "难过": {"score_range": [2, 4], "keywords": ["难过", "伤心"], "emoji": "😢"},
                "愤怒": {"score_range": [1, 3], "keywords": ["愤怒", "生气"], "emoji": "😠"},
                "疲惫": {"score_range": [3, 5], "keywords": ["疲惫", "累"], "emoji": "😴"}
            },
            "tag_patterns": {},
            "settings": {"default_mood": "平静", "default_score": 5}
        }


class JournalTracker:
    """心情日记追踪器"""
    
    def __init__(self):
        self.config = load_mood_config()
        self._ensure_data_dir()
        self.data = self._load_data()
    
    def _ensure_data_dir(self):
        """确保数据目录存在，并设置严格权限（仅当前用户可访问）"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(str(DATA_DIR), _PRIVATE_DIR_PERMS)
        except OSError:
            pass  # Windows 等不支持 chmod 的系统跳过
    
    def _load_data(self) -> Dict:
        """加载数据文件"""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ 数据文件读取失败: {e}，创建新文件")
        return {"entries": [], "version": "1.0"}
    
    def _atomic_save(self, data: Dict):
        """原子保存数据（先写临时文件再rename，防止中断导致数据丢失）"""
        try:
            fd, tmp_path = tempfile.mkstemp(
                dir=str(DATA_DIR), suffix='.tmp', prefix='journal_'
            )
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp_path, str(DATA_FILE))
                # 隐私保护：确保数据文件仅当前用户可读写
                try:
                    os.chmod(str(DATA_FILE), _PRIVATE_PERMS)
                except OSError:
                    pass
            except Exception:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                raise
        except IOError as e:
            print(f"❌ 数据保存失败: {e}")
            sys.exit(1)
    
    def _generate_short_id(self) -> str:
        """生成短UUID（8位）"""
        return uuid.uuid4().hex[:8]
    
    def _detect_mood(self, text: str) -> Tuple[str, int]:
        """
        自动识别情绪类型和评分
        
        Returns:
            (情绪名称, 情绪评分)
        """
        text_lower = text.lower()

        # 构建所有 (关键词, 情绪名, 评分) 的列表，按关键词长度降序排列
        # 这样"太棒了"会优先于"棒"匹配
        all_matches: List[Tuple[str, str, int]] = []
        for mood_name, mood_data in self.config["moods"].items():
            score_range = mood_data.get("score_range", [5, 5])
            score = (score_range[0] + score_range[1]) // 2
            for keyword in mood_data.get("keywords", []):
                if keyword in text_lower:
                    all_matches.append((keyword, mood_name, score))

        if all_matches:
            # 最长关键词优先匹配（更精确）
            all_matches.sort(key=lambda x: len(x[0]), reverse=True)
            _, mood_name, score = all_matches[0]
            return mood_name, score

        # 如果没有匹配到，返回默认
        default_mood = self.config["settings"].get("default_mood", "平静")
        default_score = self.config["settings"].get("default_score", 5)
        return default_mood, default_score
    
    def _extract_score(self, text: str) -> Optional[int]:
        """从文本中提取情绪评分（1-10）"""
        # 匹配格式：心情8分、评分9、 mood 7/10
        patterns = [
            r'心情[是为]?\s*(\d+)[分]?',
            r'评分\s*(\d+)',
            r'mood\s*(\d+)',
            r'(\d+)[/]?10',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    score = int(match.group(1))
                    if 1 <= score <= 10:
                        return score
                except ValueError:
                    continue
        return None
    
    def _extract_tags(self, text: str) -> List[str]:
        """自动提取标签（返回分类名如"工作""社交"，而非具体关键词）"""
        tags = []
        tag_patterns = self.config.get("tag_patterns", {})

        for category, keywords in tag_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    tags.append(category)
                    break

        # 去重并限制数量
        return list(dict.fromkeys(tags))[:5]
    
    def _parse_date(self, text: str) -> str:
        """解析日期，支持中文时间词和标准日期格式"""
        today = datetime.now()

        if '昨天' in text:
            date = today - timedelta(days=1)
        elif '前天' in text:
            date = today - timedelta(days=2)
        elif '今天' in text or '刚刚' in text or '刚才' in text:
            date = today
        else:
            # 优先匹配 YYYY-MM-DD
            match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
            if match:
                try:
                    date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
                    return date.strftime("%Y-%m-%d")
                except ValueError:
                    pass

            # 尝试匹配 MM-DD（无年份）
            match = re.search(r'(?<!\d)(\d{1,2})-(\d{1,2})(?!\d)', text)
            if match:
                try:
                    date = datetime(today.year, int(match.group(1)), int(match.group(2)))
                    return date.strftime("%Y-%m-%d")
                except ValueError:
                    pass

            date = today

        return date.strftime("%Y-%m-%d")
    
    def _clean_content(self, text: str) -> str:
        """清理日记内容，移除元数据标记"""
        # 移除情绪评分标记
        text = re.sub(r'心情[是为]?\s*\d+[分]?', '', text)
        text = re.sub(r'评分\s*\d+', '', text)
        # 移除时间词
        text = re.sub(r'(今天|昨天|前天|刚刚|刚才)', '', text)
        # 清理多余空格
        text = text.strip()
        return text[:2000]  # 限制长度
    
    def add(self, text: str) -> Dict:
        """
        添加一篇日记
        
        Args:
            text: 自然语言日记内容
            
        Returns:
            日记记录字典
        """
        # 解析日期
        date = self._parse_date(text)
        
        # 情绪识别
        detected_mood, detected_score = self._detect_mood(text)
        
        # 提取评分（如果有明确指定）
        explicit_score = self._extract_score(text)
        if explicit_score:
            score = explicit_score
        else:
            score = detected_score
        
        # 提取标签
        tags = self._extract_tags(text)
        
        # 清理内容（保留有意义的文字）
        content = self._clean_content(text)

        # 如果清理后太短，使用原始文本
        if not content or len(content) < 2:
            content = text[:500]

        if not content.strip():
            raise ValueError("日记内容不能为空，请写点什么吧")
        
        # 创建记录
        entry = {
            "id": self._generate_short_id(),
            "date": date,
            "content": content,
            "mood": detected_mood,
            "score": score,
            "tags": tags,
            "raw_text": text,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 添加到数据
        self.data["entries"].append(entry)
        self._atomic_save(self.data)
        
        return entry
    
    def list(self, days: int = 7, mood: Optional[str] = None) -> List[Dict]:
        """
        列出日记记录
        
        Args:
            days: 最近多少天
            mood: 按情绪筛选
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        records = []
        for e in self.data["entries"]:
            if e["date"] >= cutoff_str:
                if mood is None or e["mood"] == mood:
                    records.append(e)
        
        # 按日期倒序
        records.sort(key=lambda x: (x["date"], x["created_at"]), reverse=True)
        return records
    
    def get_by_id(self, entry_id: str) -> Optional[Dict]:
        """通过ID获取日记"""
        for e in self.data["entries"]:
            if e["id"] == entry_id:
                return e
        return None
    
    def update(self, entry_id: str, new_text: str) -> Optional[Dict]:
        """更新日记"""
        for i, e in enumerate(self.data["entries"]):
            if e["id"] == entry_id:
                # 重新解析
                date = self._parse_date(new_text)
                detected_mood, detected_score = self._detect_mood(new_text)
                explicit_score = self._extract_score(new_text)
                score = explicit_score if explicit_score else detected_score
                tags = self._extract_tags(new_text)
                content = self._clean_content(new_text)
                
                # 更新记录
                self.data["entries"][i].update({
                    "date": date,
                    "content": content,
                    "mood": detected_mood,
                    "score": score,
                    "tags": tags,
                    "raw_text": new_text,
                    "updated_at": datetime.now().isoformat()
                })
                
                self._atomic_save(self.data)
                return self.data["entries"][i]
        return None
    
    def delete(self, entry_id: str) -> bool:
        """删除日记"""
        for i, e in enumerate(self.data["entries"]):
            if e["id"] == entry_id:
                del self.data["entries"][i]
                self._atomic_save(self.data)
                return True
        return False
    
    def get_summary(self, days: int = 30) -> Dict:
        """获取日记摘要统计"""
        records = self.list(days=days)
        
        if not records:
            return {
                "period_days": days,
                "total_entries": 0,
                "avg_mood_score": 0,
                "mood_distribution": {},
                "tag_cloud": []
            }
        
        # 情绪分布
        mood_dist = {}
        total_score = 0
        all_tags = []
        
        for r in records:
            mood = r["mood"]
            mood_dist[mood] = mood_dist.get(mood, 0) + 1
            total_score += r.get("score", 5)
            all_tags.extend(r.get("tags", []))
        
        # 标签频次
        tag_freq = {}
        for tag in all_tags:
            tag_freq[tag] = tag_freq.get(tag, 0) + 1
        
        tag_cloud = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "period_days": days,
            "total_entries": len(records),
            "avg_mood_score": round(total_score / len(records), 1),
            "mood_distribution": mood_dist,
            "tag_cloud": tag_cloud
        }
    
    def calendar_view(self, year: int = None, month: int = None) -> str:
        """生成月历视图"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # 获取该月的所有日记
        month_str = f"{year}-{month:02d}"
        entries_in_month = [
            e for e in self.data["entries"]
            if e["date"].startswith(month_str)
        ]
        
        # 按日期分组，取每天的情绪
        daily_moods = {}
        for e in entries_in_month:
            day = int(e["date"].split("-")[2])
            if day not in daily_moods:
                daily_moods[day] = []
            daily_moods[day].append(e["mood"])
        
        # 生成日历
        cal = monthcalendar(year, month)
        mood_emojis = {name: data["emoji"] for name, data in self.config["moods"].items()}
        
        lines = [f"\n📅 {year}年{month}月 心情日历\n"]
        lines.append("日  一  二  三  四  五  六")
        lines.append("-" * 26)
        
        for week in cal:
            week_str = ""
            for day in week:
                if day == 0:
                    week_str += "    "
                elif day in daily_moods:
                    # 显示当天的主要情绪
                    main_mood = daily_moods[day][0]
                    emoji = mood_emojis.get(main_mood, "📝")
                    week_str += f"{emoji:2s}  "
                else:
                    week_str += f"{day:2d}  "
            lines.append(week_str)
        
        lines.append("\n图例: " + " ".join([f"{data['emoji']}{name}" for name, data in list(self.config["moods"].items())[:4]]))
        
        return "\n".join(lines)
    
    def get_moods(self) -> Dict:
        """获取情绪类型列表"""
        return self.config.get("moods", {})

    def export_data(self, anonymize: bool = False) -> Dict:
        """
        导出数据（可选匿名化）

        Args:
            anonymize: 是否匿名化（移除原始文本，仅保留情绪统计）
        """
        if anonymize:
            # 隐私友好导出：仅保留统计数据，移除日记原文
            entries = []
            for e in self.data["entries"]:
                entries.append({
                    "id": e["id"],
                    "date": e["date"],
                    "mood": e["mood"],
                    "score": e["score"],
                    "tags": e.get("tags", [])
                })
            return {"entries": entries, "version": self.data.get("version", "1.0")}
        return self.data


def main():
    """命令行入口"""
    tracker = JournalTracker()
    
    if len(sys.argv) < 2:
        print("心情日记 - mood-diary")
        print("用法: python journal.py <命令> [参数]\n")
        print("命令:")
        print("  add <内容>        - 添加日记")
        print("  list [天数]       - 列出日记，默认最近7天")
        print("  calendar [年] [月] - 月历视图")
        print("  summary [天数]    - 情绪摘要")
        print("  delete <ID>       - 删除日记")
        print("  moods             - 情绪类型列表")
        print("  update <ID> <内容> - 更新日记")
        print("")
        sys.exit(0)
    
    command = sys.argv[1]
    
    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("❌ 请提供日记内容")
                sys.exit(1)
            
            text = " ".join(sys.argv[2:])
            entry = tracker.add(text)
            mood_config = tracker.get_moods().get(entry["mood"], {})
            emoji = mood_config.get("emoji", "📝")
            
            print(f"✅ 日记已保存 {emoji}")
            print(f"   ID: {entry['id']}")
            print(f"   日期: {entry['date']}")
            print(f"   情绪: {entry['mood']} ({entry['score']}/10)")
            if entry["tags"]:
                print(f"   标签: {', '.join(entry['tags'])}")
            print(f"   内容: {entry['content'][:50]}...")
        
        elif command == "list":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            mood_filter = sys.argv[3] if len(sys.argv) > 3 else None
            entries = tracker.list(days=days, mood=mood_filter)
            
            if not entries:
                print(f"📭 最近{days}天没有日记")
                return
            
            print(f"📚 最近{days}天日记 ({len(entries)}篇)\n")
            
            current_date = ""
            for e in entries:
                if e["date"] != current_date:
                    current_date = e["date"]
                    print(f"📅 {current_date}")
                
                mood_config = tracker.get_moods().get(e["mood"], {})
                emoji = mood_config.get("emoji", "📝")
                tags_str = f" [{', '.join(e['tags'])}]" if e.get("tags") else ""
                content_preview = e["content"][:30] + "..." if len(e["content"]) > 30 else e["content"]
                
                print(f"  [{e['id']}] {emoji} {e['mood']}({e['score']}){tags_str}")
                print(f"       {content_preview}")
        
        elif command == "calendar":
            year = int(sys.argv[2]) if len(sys.argv) > 2 else None
            month = int(sys.argv[3]) if len(sys.argv) > 3 else None
            print(tracker.calendar_view(year, month))
        
        elif command == "summary":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            summary = tracker.get_summary(days=days)
            
            print(f"📊 最近{days}天心情摘要\n")
            print(f"📝 日记总数: {summary['total_entries']} 篇")
            print(f"⭐ 平均情绪评分: {summary['avg_mood_score']}/10")
            
            if summary['mood_distribution']:
                print(f"\n🎭 情绪分布:")
                for mood, count in sorted(summary['mood_distribution'].items(), key=lambda x: x[1], reverse=True):
                    mood_config = tracker.get_moods().get(mood, {})
                    emoji = mood_config.get("emoji", "")
                    print(f"   {emoji} {mood}: {count}篇")
            
            if summary['tag_cloud']:
                print(f"\n🏷️ 常用标签:")
                for tag, count in summary['tag_cloud']:
                    print(f"   #{tag}: {count}次")
        
        elif command == "delete":
            if len(sys.argv) < 3:
                print("❌ 请提供日记ID")
                sys.exit(1)
            
            entry_id = sys.argv[2]
            if tracker.delete(entry_id):
                print(f"✅ 已删除日记 #{entry_id}")
            else:
                print(f"❌ 未找到日记 #{entry_id}")
        
        elif command == "moods":
            moods = tracker.get_moods()
            print("🎭 情绪类型列表\n")
            for name, data in moods.items():
                emoji = data.get("emoji", "")
                score_range = data.get("score_range", [1, 10])
                print(f"  {emoji} {name}: 评分范围 {score_range[0]}-{score_range[1]}")
        
        elif command == "update":
            if len(sys.argv) < 4:
                print("❌ 请提供日记ID和新内容")
                sys.exit(1)
            
            entry_id = sys.argv[2]
            new_text = " ".join(sys.argv[3:])
            entry = tracker.update(entry_id, new_text)
            
            if entry:
                print(f"✅ 日记 #{entry_id} 已更新")
                print(f"   情绪: {entry['mood']} ({entry['score']}/10)")
            else:
                print(f"❌ 未找到日记 #{entry_id}")
        
        else:
            print(f"❌ 未知命令: {command}")
            print("可用命令: add, list, calendar, summary, delete, moods, update")
    
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

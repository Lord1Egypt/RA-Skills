#!/usr/bin/env python3
"""
梦境记录脚本 - 动态学习式梦境分析
自动从用户梦境中提取意象，通过 LLM 辅助分类，持续丰富意象库
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

# ============ 极简种子意象（仅用于启动）============
# 这些是最基础的、几乎每个文化都共通的意象，作为种子
SEED_IMAGERY = {
    "自然元素": ["水", "火", "风", "山", "天空", "太阳", "月亮"],
    "动物": ["蛇", "鸟", "鱼", "猫", "狗", "马"],
    "建筑": ["房子", "门", "路", "桥", "楼梯"],
    "人物": ["母亲", "父亲", "孩子", "陌生人"],
    "身体": ["手", "眼睛", "心", "血"],
    "情绪场景": ["坠落", "飞翔", "逃跑", "黑暗", "光明"]
}

# 8大类别（保持不变，作为分类框架）
CATEGORIES = ["自然元素", "动物", "建筑与空间", "人物", "身体与感知", "物品与象征", "情绪与场景", "抽象概念"]

class DreamJournal:
    def __init__(self):
        self.workspace = Path("/root/.openclaw/workspace")
        self.memory_dir = self.workspace / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # 加载或初始化意象库
        self.imagery_db = self._load_imagery_db()
        self.user_imagery = self._load_user_imagery()
    
    def _load_imagery_db(self):
        """加载持久化的意象数据库"""
        db_file = self.memory_dir / "dream_imagery_db.json"
        if db_file.exists():
            data = json.loads(db_file.read_text(encoding='utf-8'))
            # 转换为 set
            return {cat: set(words) for cat, words in data.items()}
        # 初始化为种子意象
        return {cat: set(words) for cat, words in SEED_IMAGERY.items()}
    
    def _load_user_imagery(self):
        """加载用户学习到的自定义意象"""
        user_file = self.memory_dir / "user_imagery.json"
        if user_file.exists():
            data = json.loads(user_file.read_text(encoding='utf-8'))
            return defaultdict(set, {k: set(v) for k, v in data.items()})
        return defaultdict(set)
    
    def _save_imagery(self):
        """保存意象数据库"""
        # 保存基础库
        base_file = self.memory_dir / "dream_imagery_base.json"
        base_data = {cat: sorted(words) for cat, words in self.imagery_db.items()}
        base_file.write_text(json.dumps(base_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 保存用户学习到的意象
        user_file = self.memory_dir / "user_imagery.json"
        user_data = {cat: sorted(words) for cat, words in self.user_imagery.items() if words}
        user_file.write_text(json.dumps(user_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 同时保存合并版本（便于查询）
        combined_file = self.memory_dir / "dream_imagery_db.json"
        combined = {}
        for cat in CATEGORIES:
            base = self.imagery_db.get(cat, set())
            user = self.user_imagery.get(cat, set())
            combined[cat] = sorted(base | user)
        combined_file.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def extract_imagery(self, content):
        """从梦境内容中提取已知意象"""
        found = []
        all_known = set()
        for cat, words in self.imagery_db.items():
            all_known.update(words)
        for cat, words in self.user_imagery.items():
            all_known.update(words)
        
        for word in sorted(all_known, key=len, reverse=True):  # 长词优先匹配
            if word in content and word not in [f[0] for f in found]:
                # 过滤掉明显是句子碎片的词
                if self._is_valid_imagery(word):
                    cat = self._get_category(word)
                    found.append((word, cat))
        
        return found
    
    def _get_category(self, word):
        """获取意象所属类别"""
        for cat, words in self.imagery_db.items():
            if word in words:
                return cat
        for cat, words in self.user_imagery.items():
            if word in words:
                return cat
        return "未分类"
    
    def learn_new_imagery(self, content, suggested_tags=None):
        """
        从梦境内容中学习新的意象
        保守策略：只学习明显是名词的词汇，优先匹配已知模式的扩展
        """
        import re
        new_imagery = []
        
        # 1. 清理内容，去掉常见的梦境叙述前缀
        cleaned = content
        prefixes = ["昨晚我做了个梦", "昨晚梦见", "我做了个梦", "我梦见", "做梦梦到", "在梦中", "梦到", "梦见"]
        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip("，,。.")
                break
        
        # 2. 按标点切分，获取语义片段
        segments = re.split(r'[，,。；;！!？?]', cleaned)
        
        # 3. 定义需要学习的模式（颜色+名词、形容词+名词等）
        learn_patterns = [
            # 颜色 + 的 + 名词
            (r'(紫色|红色|蓝色|绿色|黄色|金色|银色|黑色|白色|青色)的?([\u4e00-\u9fa5]{2})', lambda m: m.group(1) + m.group(2)),
            # 发光/古老/神秘 + 的 + 名词
            (r'(发光|古老|神秘|漆黑|明亮|巨大)的?([\u4e00-\u9fa5]{2})', lambda m: m.group(1) + m.group(2)),
            # 单纯的名词（2-3字，常见的意象词）
            (r'([\u4e00-\u9fa5]{2,3})(?:里|中|上|下|旁|边|前|后|周围)', lambda m: m.group(1)),  # X里/X中 -> X
            (r'(?:有|是|在)([\u4e00-\u9fa5]{2,3})(?:和|与|在|的|$)', lambda m: m.group(1)),  # 有X和 -> X
        ]
        
        candidates = []
        
        for segment in segments:
            segment = segment.strip()
            if len(segment) < 2:
                continue
            
            # 尝试各种模式匹配
            for pattern, extractor in learn_patterns:
                for match in re.finditer(pattern, segment):
                    word = extractor(match)
                    if self._is_valid_imagery(word):
                        candidates.append(word)
            
            # 额外：直接匹配种子意象的同类型词汇
            # 例如种子里有"蝴蝶"，看到"发光的蝴蝶"就提取"蝴蝶"
            seed_all = []
            for words in SEED_IMAGERY.values():
                seed_all.extend(words)
            
            for seed in seed_all:
                if seed in segment and self._is_valid_imagery(seed):
                    candidates.append(seed)
        
        # 4. 去重
        seen = set()
        unique_candidates = []
        for w in candidates:
            if w not in seen:
                unique_candidates.append(w)
                seen.add(w)
        
        # 5. 学习新意象（限制数量）
        for word in unique_candidates[:6]:
            if not self._is_known(word):
                category = self._auto_classify(word)
                self.user_imagery[category].add(word)
                new_imagery.append((word, category))
        
        # 6. 用户建议的标签
        if suggested_tags:
            for tag in suggested_tags:
                if not self._is_known(tag) and self._is_valid_imagery(tag):
                    category = self._auto_classify(tag)
                    self.user_imagery[category].add(tag)
                    new_imagery.append((tag, category))
        
        if new_imagery:
            self._save_imagery()
        
        return new_imagery
    
    def _is_valid_imagery(self, word):
        """检查是否是有效的意象词"""
        import re
        
        if len(word) < 2 or len(word) > 5:
            return False
        
        # 严格过滤掉明显是句子碎片的词
        bad_patterns = [
            r'昨晚.*', r'梦见.*', r'梦到.*', r'做了.*', r'感觉.*',
            r'周围.*', r'远处.*', r'旁边.*',
            r'.*的[梦河水光桥石]$', r'.*的$', r'.*[了在是就而和与跟]$',
            r'[我你他她它].*', r'[这那].*个',
            r'^的', r'^在', r'^是', r'^有',
        ]
        for pattern in bad_patterns:
            if re.match(pattern, word):
                return False
        
        # 停用词
        stop_words = {"一个", "感觉", "时候", "然后", "突然", "好像", "不知道", "觉得", 
                      "最后", "开始", "现在", "那里", "这里", "一直", "非常", "特别", "很多", 
                      "一些", "那个", "这个", "一种", "这些", "那些", "什么", "怎么", "为什么", 
                      "因为", "所以", "但是", "不过", "虽然", "如果", "就是", "这样", "那样", 
                      "可能", "应该", "可以", "需要", "想要", "看到", "听到", "想到", "知道", 
                      "记得", "发现", "出现", "发生", "变成", "来到", "离开", "回去",
                      "自己", "周围", "神秘", "奇怪", "宁静", "神秘又宁"}
        
        if word in stop_words:
            return False
        
        return True
    
    def _is_known(self, word):
        """检查意象是否已知"""
        for words in self.imagery_db.values():
            if word in words:
                return True
        for words in self.user_imagery.values():
            if word in words:
                return True
        return False
    
    def _auto_classify(self, word):
        """自动分类新意象（基于简单规则）"""
        # 自然元素
        nature = ["水", "海", "湖", "河", "雨", "雪", "风", "云", "山", "林", "木", "草", "花", "日", "月", "星", "天", "地", "土", "石", "雷", "电", "火", "冰", "光", "暗", "影"]
        if any(n in word for n in nature):
            return "自然元素"
        
        # 动物
        animals = ["蛇", "鸟", "鱼", "猫", "狗", "马", "虎", "狮", "狼", "熊", "兔", "龙", "凤", "虫", "蝶", "蜂", "鼠", "猪", "牛", "羊", "鸡", "鸭", "猴"]
        if any(a in word for a in animals):
            return "动物"
        
        # 建筑与空间
        buildings = ["房", "屋", "家", "门", "窗", "墙", "楼", "梯", "桥", "路", "街", "城", "室", "厅", "院", "园", "校", "店", "场", "塔", "堡", "宫", "殿", "庙", "洞", "穴", "牢", "笼"]
        if any(b in word for b in buildings):
            return "建筑与空间"
        
        # 人物关系
        people = ["母", "父", "妈", "爸", "子", "女", "儿", "孙", "爷", "奶", "兄", "弟", "姐", "妹", "夫", "妻", "友", "朋", "师", "生", "医", "警", "敌", "人", "鬼", "神", "仙", "佛", "魔", "妖", "怪"]
        if any(p in word for p in people):
            return "人物"
        
        # 身体
        body = ["头", "脸", "眼", "耳", "口", "牙", "手", "脚", "心", "血", "骨", "肉", "发", "毛", "皮", "身", "体"]
        if any(b in word for b in body):
            return "身体与感知"
        
        # 物品
        items = ["车", "船", "机", "书", "笔", "纸", "钱", "刀", "剑", "枪", "钥匙", "锁", "镜", "灯", "床", "桌", "椅", "衣", "帽", "鞋", "包", "盒", "箱", "杯", "碗", "盘", "戒指", "链", "表"]
        if any(i in word for i in items):
            return "物品与象征"
        
        # 情绪相关字词
        emotion = ["梦", "怕", "怕", "惧", "恐", "惊", "吓", "怒", "气", "乐", "喜", "笑", "哭", "泪", "爱", "恨", "想", "念", "忘", "逃", "跑", "追", "躲", "藏"]
        if any(e in word for e in emotion):
            return "情绪与场景"
        
        return "抽象概念"  # 默认分类
    
    def generate_title(self, content, imagery):
        """生成诗意标题"""
        if imagery:
            # 过滤掉学习过程中可能产生的碎片词汇，只取真正的意象
            clean_imagery = []
            for word, cat in imagery:
                # 过滤掉明显是碎片的词
                if len(word) >= 2 and not any(x in word for x in ["昨晚", "梦见", "梦到", "做了", "一个", "感觉"]):
                    clean_imagery.append(word)
            
            elements = clean_imagery[:3] if clean_imagery else ["梦"]
            if elements:
                templates = [
                    f"在{'与'.join(elements)}之间",
                    f"{'的'.join(elements)}之梦",
                    f"关于{'和'.join(elements)}"
                ]
                return templates[0][:20]
        return "梦境记录"
    
    def record(self, content, suggested_tags=None):
        """记录梦境"""
        # 1. 提取已知意象
        known_imagery = self.extract_imagery(content)
        
        # 2. 学习新意象
        new_imagery = self.learn_new_imagery(content, suggested_tags)
        
        # 3. 合并所有意象
        all_imagery = list({(w, c) for w, c in known_imagery + new_imagery})
        tags = [w for w, c in all_imagery[:5]]
        
        # 4. 生成标题
        title = self.generate_title(content, all_imagery)
        
        # 5. 写入文件
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        
        dreams_file = self.memory_dir / "dreams.md"
        
        entry = f"""## {title}

**日期**: {date_str} {time_str}
**意象**: {', '.join(tags) if tags else '无'}
{('**新学习**: ' + ', '.join([w for w, c in new_imagery])) if new_imagery else ''}

{content}

---

"""
        
        if dreams_file.exists():
            old_content = dreams_file.read_text(encoding='utf-8')
        else:
            old_content = "# 梦日记 🌙\n\n"
        
        new_content = old_content.replace("# 梦日记 🌙\n\n", f"# 梦日记 🌙\n\n{entry}")
        dreams_file.write_text(new_content, encoding='utf-8')
        
        # 6. 更新统计
        self._update_stats(tags)
        
        return {
            "title": title,
            "tags": tags,
            "new_learned": [w for w, c in new_imagery],
            "total_imagery": self._count_total_imagery()
        }
    
    def _update_stats(self, tags):
        """更新统计数据"""
        stats_file = self.memory_dir / "dream_stats.json"
        if stats_file.exists():
            stats = json.loads(stats_file.read_text(encoding='utf-8'))
        else:
            stats = {"total_dreams": 0, "imagery_counts": {}, "category_counts": {}}
        
        stats["total_dreams"] += 1
        for tag in tags:
            stats["imagery_counts"][tag] = stats["imagery_counts"].get(tag, 0) + 1
        
        stats_file.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def _count_total_imagery(self):
        """统计总意象数量"""
        count = 0
        for words in self.imagery_db.values():
            count += len(words)
        for words in self.user_imagery.values():
            count += len(words)
        return count
    
    def get_imagery_library(self):
        """获取当前意象库状态"""
        result = {}
        for cat in CATEGORIES:
            base = len(self.imagery_db.get(cat, []))
            user = len(self.user_imagery.get(cat, []))
            result[cat] = {"base": base, "learned": user, "total": base + user}
        return result
    
    def search(self, keyword=None, category=None, days=None):
        """搜索梦境"""
        dreams_file = self.memory_dir / "dreams.md"
        if not dreams_file.exists():
            return []
        
        content = dreams_file.read_text(encoding='utf-8')
        entries = re.split(r'\n## ', content)[1:]
        
        results = []
        for entry in entries:
            if keyword and keyword not in entry:
                continue
            if category and category not in entry:
                continue
            lines = entry.strip().split('\n')
            title = lines[0] if lines else "无标题"
            results.append({"title": title, "preview": entry[:150] + "..."})
        
        return results
    
    def analyze(self):
        """分析梦境统计"""
        stats_file = self.memory_dir / "dream_stats.json"
        if not stats_file.exists():
            return None
        
        stats = json.loads(stats_file.read_text(encoding='utf-8'))
        library = self.get_imagery_library()
        
        return {
            "total_dreams": stats.get("total_dreams", 0),
            "top_imagery": sorted(stats.get("imagery_counts", {}).items(), key=lambda x: x[1], reverse=True)[:10],
            "imagery_library": library,
            "total_known_imagery": self._count_total_imagery()
        }


# ============ 命令行接口 ============

def main():
    journal = DreamJournal()
    
    if len(sys.argv) < 2:
        print("用法: record_dream.py <命令> [参数]")
        print("命令: record, search, analyze, library")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "record" and len(sys.argv) > 2:
        content = sys.argv[2]
        result = journal.record(content)
        print(f"✓ 已记录: {result['title']}")
        print(f"  意象标签: {', '.join(result['tags'])}")
        if result['new_learned']:
            print(f"  🌱 新学习意象: {', '.join(result['new_learned'])}")
        print(f"  当前意象库: {result['total_imagery']} 个词汇")
    
    elif command == "search":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        results = journal.search(keyword=keyword)
        print(f"找到 {len(results)} 条记录:")
        for r in results[:5]:
            print(f"  • {r['title']}")
    
    elif command == "analyze":
        analysis = journal.analyze()
        if analysis:
            print(f"总共记录: {analysis['total_dreams']} 个梦境")
            print(f"意象库规模: {analysis['total_known_imagery']} 个词汇")
            print("\n常见意象:")
            for img, count in analysis['top_imagery']:
                print(f"  • {img}: {count} 次")
            print("\n意象库分布:")
            for cat, data in analysis['imagery_library'].items():
                if data['total'] > 0:
                    print(f"  • {cat}: {data['base']}基础 + {data['learned']}学习 = {data['total']}")
        else:
            print("暂无梦境记录")
    
    elif command == "library":
        lib = journal.get_imagery_library()
        print("当前意象库:")
        for cat, data in lib.items():
            if data['total'] > 0:
                print(f"\n{cat}: {data['total']} 个")
                # 显示用户学习到的部分
                user_words = sorted(journal.user_imagery.get(cat, []))[:10]
                if user_words:
                    print(f"  学习: {', '.join(user_words)}{'...' if len(journal.user_imagery.get(cat, [])) > 10 else ''}")

if __name__ == "__main__":
    main()

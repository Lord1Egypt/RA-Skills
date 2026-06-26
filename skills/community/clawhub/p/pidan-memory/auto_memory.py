import os
#!/usr/bin/env python3
"""
自动记忆评估脚本 v5.0
- 支持多用户/共享模式
- 每20条自动去重
"""
import json
import sys
import re
import time
from pathlib import Path

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
sys.path.insert(0, str(MEMORY_DIR))

# ============ 场景映射表 ============
SCENE_RULES = {
    "personal": {
        "keywords": ["我叫", "名字", "今年", "岁", "生日", "住", "时区", "老公", "老婆", 
                    "男朋友", "女朋友", "孩子", "宠物", "猫", "狗", "星座", "属"],
        "rules": [
            (r"我叫(.+?)(?:\s|,|，|。|$)", "姓名"),
            (r"我今年(\d+)岁", "年龄"),
            (r"属(.+?)的", "属相"),
            (r"(.+?)座", "星座"),
            (r"住在(.+?)(?:\s|,|，|。|$)", "居住地"),
        ],
        "importance": 4,
    },
    "food": {
        "keywords": ["喜欢吃", "爱吃", "最爱吃", "最喜欢吃", "不吃", "忌口", "过敏", 
                    "辣", "甜", "咸", "清淡", "外卖", "做饭", "厨艺", "咖啡", "茶", "酒"],
        "rules": [
            (r"(?:最)?喜欢吃(.+?)(?:\s|,|，|。|$)", "饮食偏好"),
            (r"不吃(.+?)(?:\s|,|，|。|$)", "饮食禁忌"),
        ],
        "importance": 3,
    },
    "entertainment": {
        "keywords": ["电影", "电视剧", "综艺", "动漫", "音乐", "歌", "游戏", "steam", 
                    "switch", "ps5", "王者", "原神", "小说", "书", "漫画", "足球", "篮球",
                    "跑步", "健身", "瑜伽", "游泳"],
        "rules": [
            (r"喜欢(.+?)(?:电影|电视剧)", "影视偏好"),
            (r"喜欢(.+?)(?:歌|音乐)", "音乐偏好"),
            (r"喜欢(.+?)(?:游戏|玩)", "游戏偏好"),
        ],
        "importance": 3,
    },
    "work": {
        "keywords": ["工作", "上班", "公司", "岗位", "工程师", "设计师", "产品", "运营",
                    "项目", "需求", "加班", "同事", "老板", "面试", "跳槽", "辞职", 
                    "工资", "薪资", "奖金"],
        "rules": [
            (r"在(.+?)工作", "公司"),
            (r"是(.+?)(?:工程师|设计师|产品)", "岗位"),
        ],
        "importance": 4,
    },
    "tech": {
        "keywords": ["编程", "开发", "python", "javascript", "java", "go", "rust", 
                    "react", "vue", "node", "mysql", "redis", "docker", "linux", 
                    "ai", "大模型", "llm", "gpt", "电脑", "mac", "键盘"],
        "rules": [
            (r"用(.+?)编程", "编程语言"),
            (r"会用(.+?)(?:\s|,|，|。|$)", "技术栈"),
        ],
        "importance": 3,
    },
    "learning": {
        "keywords": ["学习", "学", "课程", "培训", "考证", "考研", "考公", "英语", 
                    "雅思", "托福", "日语", "韩语", "读书", "复盘", "笔记"],
        "rules": [
            (r"考(.+?)(?:\s|,|，|。|$)", "考试目标"),
            (r"学(.+?)(?:\s|,|，|。|$)", "学习内容"),
        ],
        "importance": 3,
    },
    "habits": {
        "keywords": ["早睡", "早起", "晚睡", "熬夜", "失眠", "每天", "习惯", "坚持",
                    "自律", "运动", "跑步", "健身", "记账", "理财", "存钱", "拖延"],
        "rules": [
            (r"每天(.+?)(?:\s|,|，|。|$)", "日常习惯"),
            (r"习惯(.+?)(?:\s|,|，|。|$)", "个人习惯"),
        ],
        "importance": 3,
    },
    "goals": {
        "keywords": ["要成为", "想成为", "成为", "目标", "理想", "愿望", "梦想",
                    "以后要", "未来要", "我想", "我要", "计划", "规划", "减肥",
                    "考证", "考研", "升职", "加薪", "买房", "脱单"],
        "rules": [
            (r"要成为(.+?)(?:\s|,|，|。|$)", "人生目标"),
            (r"想成为(.+?)(?:\s|,|，|。|$)", "人生目标"),
            (r"以后要(.+?)(?:\s|,|，|。|$)", "未来计划"),
            (r"今年要(.+?)(?:\s|,|，|。|$)", "年度目标"),
        ],
        "importance": 4,
    },
    "health": {
        "keywords": ["身高", "体重", "胖", "瘦", "减肥", "生病", "感冒", "失眠",
                    "焦虑", "压力", "情绪", "累", "困", "疲惫"],
        "rules": [
            (r"身高(\d+)", "身高"),
            (r"体重(\d+)", "体重"),
        ],
        "importance": 4,
    },
    "finance": {
        "keywords": ["工资", "薪资", "收入", "奖金", "股票", "存款", "理财", "投资",
                    "花钱", "省钱", "月光", "负债", "贷款", "房贷", "信用卡"],
        "rules": [
            (r"月薪(.+?)(?:\s|,|，|。|$)", "收入"),
            (r"年薪(.+?)(?:\s|,|，|。|$)", "收入"),
        ],
        "importance": 3,
    },
    "travel": {
        "keywords": ["旅游", "旅行", "度假", "去过", "想去的", "打卡", "景点",
                    "日本", "韩国", "美国", "欧洲", "泰国", "新加坡", "机票", "酒店"],
        "rules": [
            (r"去过(.+?)(?:\s|,|，|。|$)", "旅行经历"),
            (r"想去(.+?)(?:\s|,|，|。|$)", "旅行目标"),
        ],
        "importance": 3,
    },
    "shopping": {
        "keywords": ["网购", "淘宝", "京东", "拼多多", "外卖", "直播", "种草",
                    "双十一", "折扣", "优惠", "电子产品", "衣服", "化妆品"],
        "rules": [
            (r"喜欢(.+?)(?:网购|购物)", "购物偏好"),
        ],
        "importance": 2,
    },
    "lifestyle": {
        "keywords": ["独居", "合租", "买房", "租房", "搬家", "有娃", "带娃",
                    "育儿", "开车", "打车", "地铁", "通勤"],
        "rules": [
            (r"(.+?)住", "居住状态"),
            (r"(.+?)通勤", "通勤方式"),
        ],
        "importance": 3,
    },
    "skills": {
        "keywords": ["会", "擅长", "精通", "掌握", "乐器", "吉他", "钢琴",
                    "唱歌", "跳舞", "画画", "摄影", "烹饪", "烘焙", "滑雪"],
        "rules": [
            (r"会(.+?)(?:\s|,|，|。|$)", "技能"),
            (r"擅长(.+?)(?:\s|,|，|。|$)", "擅长技能"),
        ],
        "importance": 3,
    },
    "lessons": {
        "keywords": ["解决了", "问题", "bug", "错误", "原因", "踩坑", "经验",
                    "教训", "学会", "掌握", "终于", "成功", "搞定", "排查",
                    "调试", "方法", "技巧", "窍门"],
        "rules": [
            (r"解决了(.+?)问题", "问题解决"),
            (r"原因是(.+?)(?:\s|,|，|。|$)", "原因分析"),
            (r"学会(.+?)(?:\s|,|，|。|$)", "学习收获"),
            (r"踩坑(.+?)(?:\s|,|，|。|$)", "踩坑经验"),
        ],
        "importance": 4,
    },
    "explicit": {
        "keywords": ["记住", "帮我记", "别忘了", "提醒我", "重要", "务必",
                    "以后都", "以后要", "以后记得"],
        "rules": [],
        "importance": 5,
    },
}


def quick_match(content: str) -> tuple[bool, list]:
    """快速匹配场景"""
    content_lower = content.lower()
    matched_scenes = []
    
    for scene, config in SCENE_RULES.items():
        for keyword in config["keywords"]:
            if keyword.lower() in content_lower:
                matched_scenes.append(scene)
                break
    
    return len(matched_scenes) > 0, matched_scenes


def analyze_content(content: str) -> list[tuple[str, str, int]]:
    """分析内容"""
    results = []
    
    matched, scenes = quick_match(content)
    if not matched:
        return results
    
    if "explicit" in scenes:
        return [(content, "明确要求", 5)]
    
    for scene in scenes:
        if scene == "explicit":
            continue
            
        config = SCENE_RULES[scene]
        
        for pattern, label in config.get("rules", []):
            match = re.search(pattern, content)
            if match:
                if match.groups():
                    extracted = match.group(1).strip()
                    if extracted:
                        memory_content = f"用户{label}: {extracted}"
                    else:
                        memory_content = f"用户{label}"
                else:
                    memory_content = f"用户{label}"
                
                results.append((memory_content, label, config["importance"]))
    
    if not any(r[1] in [rule[1] for rule in config.get("rules", [])] for r in results):
        keyword = config["keywords"][0]
        memory_content = f"用户提到: {keyword}"
        results.append((memory_content, scene, config["importance"]))
    
    return results


def is_ollama_ready():
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def add_memory(content: str, summary: str = "", importance: int = 3, user_id: str = "default"):
    try:
        from memory_lance import add_memory_vector, get_mode
        mode = get_mode()  # 获取当前模式
        return add_memory_vector(content, summary, importance, "auto-hook", None, user_id, mode)
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    start_time = time.time()
    
    try:
        input_data = json.load(sys.stdin)
    except:
        return
    
    user_message = input_data.get("user_message", "")
    assistant_message = input_data.get("assistant_message", "")
    
    user_id = os.environ.get("OPENCLAW_USER_ID", "default")
    for i, arg in enumerate(sys.argv):
        if arg == "--user-id" and i + 1 < len(sys.argv):
            user_id = sys.argv[i + 1]
    
    if not user_message:
        return
    
    all_memories = []
    for msg in [user_message, assistant_message]:
        if msg:
            memories = analyze_content(msg)
            all_memories.extend(memories)
    
    # 去重
    seen = set()
    unique_memories = []
    for content, summary, importance in all_memories:
        if content not in seen:
            seen.add(content)
            unique_memories.append((content, summary, importance))
    
    if unique_memories and is_ollama_ready():
        from memory_lance import get_mode
        mode = get_mode()
        
        for content, summary, importance in unique_memories:
            result = add_memory(content, summary, importance, user_id)
            if result.get("success"):
                print(f"✓ [{mode}] {content[:35]}...")
    
    elapsed = time.time() - start_time
    if elapsed > 2:
        print(f"⏱️ {elapsed:.2f}s")


if __name__ == "__main__":
    main()

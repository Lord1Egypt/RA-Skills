import sys
import json
import random

def generate_multiple_choice(key_point: str) -> dict:
    """
    生成单项选择题（4选1）
    """
    # 提取核心概念
    concept = key_point.get("content", "")
    
    # 正确答案模板
    correct_answers = [
        f"{concept} 需要满足核心条件",
        f"正确理解 {concept} 的本质是关键",
        f"实践中需要正确应用 {concept}",
        f"理解 {concept} 的核心逻辑是前提"
    ]
    correct = random.choice(correct_answers)
    
    # 干扰项模板（看起来对但逻辑错误）
    distractors = [
        f"{concept} 在任何场景都适用",
        f"{concept} 不需要考虑边界条件",
        f"只用 {concept} 就能解决所有问题",
        f"{concept} 和其他理论没有关联",
        f"掌握 {concept} 不需要实践",
        f"{concept} 的逻辑是绝对正确的"
    ]
    # 随机选3个干扰项
    wrong = random.sample(distractors, 3)
    
    # 选项列表，打乱顺序
    options = [correct] + wrong
    random.shuffle(options)
    
    # 找到正确答案的位置（A/B/C/D）
    correct_index = options.index(correct)
    correct_letter = chr(ord('A') + correct_index)
    
    return {
        "type": "multiple_choice",
        "question": f"关于 {key_point.get('title', '知识点')}，以下哪个说法是正确的？",
        "options": {
            "A": options[0],
            "B": options[1],
            "C": options[2],
            "D": options[3]
        },
        "correct_answer": correct_letter,
        "explanation": f"正确答案是 {correct_letter}，因为 {correct}。其他选项错误是因为忽略了边界条件/适用场景/核心逻辑。",
        "hint": "重点看是否符合实际应用场景和核心逻辑"
    }

def generate_variant_question(key_point: str) -> dict:
    """
    生成变因题：如果变量X变化10倍，会发生什么（保留作为高级模式）
    """
    return {
        "type": "variant",
        "question": f"如果上述场景中的关键变量增加10倍，'{key_point.get('content', '')}' 这个理论还成立吗？为什么？",
        "hint": "考虑边界条件和极限情况"
    }

def generate_trap_question(key_point: str) -> dict:
    """
    生成陷阱题：给出一个看似合理但错误的推论（保留作为高级模式）
    """
    traps = [
        f"既然'{key_point.get('content', '')}'是对的，那么它的相反命题也一定是对的，对吗？",
        f"'{key_point.get('content', '')}' 在所有场景下都适用吗？",
        f"如果把这个逻辑反过来推导，会得到什么结论？"
    ]
    return {
        "type": "trap",
        "question": random.choice(traps),
        "hint": "注意逻辑方向性和充分必要条件"
    }

def generate_comprehensive_question(key_points: list) -> dict:
    """
    生成综合题：结合多个知识点（保留作为高级模式）
    """
    if len(key_points) < 2:
        return None
    return {
        "type": "comprehensive",
        "question": f"如何结合 '{key_points[0].get('content', '')}' 和 '{key_points[1].get('content', '')}' 来解决实际问题？",
        "hint": "寻找两个知识点之间的关联"
    }

def generate_quiz(key_points: list, count: int = 3, difficulty: str = "easy") -> dict:
    """
    生成测验题组，默认生成单选题
    """
    quizzes = []
    
    # 简单难度：全是单选题
    if difficulty == "easy":
        for kp in key_points[:count]:
            quizzes.append(generate_multiple_choice(kp))
    
    # 中等/困难难度：混合题型
    else:
        for kp in key_points[:count]:
            q_type = random.choice(["multiple_choice", "variant", "trap"])
            if q_type == "multiple_choice":
                quizzes.append(generate_multiple_choice(kp))
            elif q_type == "variant":
                quizzes.append(generate_variant_question(kp))
            else:
                quizzes.append(generate_trap_question(kp))
    
    # 加综合题
    if len(key_points) >= 2 and difficulty != "easy":
        comp = generate_comprehensive_question(key_points[:2])
        if comp:
            quizzes.append(comp)
    
    return {
        "status": "success",
        "count": len(quizzes),
        "quizzes": quizzes,
        "reward": {
            "correct": 50,
            "streak_bonus": 100,
            "turing_bonus": 150
        }
    }

def load_key_points(file_path: str) -> list:
    """
    从extract.py的输出加载重点
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("key_points", [])
    except Exception as e:
        return []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key_points = load_key_points(sys.argv[1])
    else:
        key_points = [
            {"id": 1, "title": "CAP定理", "content": "分布式系统只能同时满足一致性、可用性、分区容忍性中的两个"},
            {"id": 2, "title": "Paxos算法", "content": "分布式一致性选举算法，通过多数派投票达成共识"}
        ]
    
    # 默认生成简单难度单选题
    result = generate_quiz(key_points, difficulty="easy")
    print(json.dumps(result, ensure_ascii=False, indent=2))
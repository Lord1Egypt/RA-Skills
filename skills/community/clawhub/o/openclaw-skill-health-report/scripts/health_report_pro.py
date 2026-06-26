#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康报告生成系统（AI 专业版 v5.0 - 最终修复版）
- 修复餐次第一行食物丢失（增强正则容错）
- 修复 PDF JSON 解析
- 添加 AI 点评到 PDF
- 引入过饱系数和症状惩罚算法

安全合规：
- 强制环境变量校验（MEMORY_DIR 必填）
- Webhook 未配置时仅本地生成 PDF
- 优雅退出机制，避免异常崩溃
"""

import sys
import json
import re
import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# ==================== 安全校验：环境变量检查 ====================
def validate_environment():
    """启动前强制校验环境变量，确保安全运行"""
    errors = []
    warnings = []
    
    # 1. MEMORY_DIR 必填检查
    memory_dir = os.environ.get('MEMORY_DIR', '')
    if not memory_dir:
        errors.append("❌ 错误：MEMORY_DIR 环境变量未配置（必填）")
        errors.append("   请在 .env 文件中设置 MEMORY_DIR='/path/to/memory'")
    elif not os.path.exists(memory_dir):
        errors.append(f"❌ 错误：MEMORY_DIR 目录不存在：{memory_dir}")
    elif not os.access(memory_dir, os.R_OK):
        errors.append(f"❌ 错误：MEMORY_DIR 目录无读取权限：{memory_dir}")
    
    # 2. Webhook 配置检查（可选，但需提示）
    webhooks = {
        'DINGTALK_WEBHOOK': os.environ.get('DINGTALK_WEBHOOK', ''),
        'FEISHU_WEBHOOK': os.environ.get('FEISHU_WEBHOOK', ''),
        'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN', ''),
    }
    configured_webhooks = [k for k, v in webhooks.items() if v]
    
    if not configured_webhooks:
        warnings.append("⚠️  警告：未配置任何 Webhook，报告将仅在本地生成 PDF")
        warnings.append("   如需推送，请配置 DINGTALK_WEBHOOK/FEISHU_WEBHOOK/TELEGRAM_*")
    
    # 3. 输出检查结果
    if warnings:
        print("=" * 60)
        print("⚠️  安全警告")
        print("=" * 60)
        for w in warnings:
            print(w)
        print("=" * 60)
    
    if errors:
        print("=" * 60)
        print("❌ 环境校验失败")
        print("=" * 60)
        for e in errors:
            print(e)
        print("=" * 60)
        print("\n程序已安全退出。请修复上述问题后重新运行。")
        sys.exit(1)
    
    return True

# 执行环境校验
validate_environment()

# ==================== 路径管理 ====================
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.resolve()
CONFIG_DIR = PROJECT_ROOT / 'config'
ASSETS_DIR = PROJECT_ROOT / 'assets'
LOGS_DIR = PROJECT_ROOT / 'logs'
REPORTS_DIR = PROJECT_ROOT / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)
sys.path.insert(0, str(SCRIPT_DIR))

from constants import DEFAULT_PORTIONS, FOOD_CALORIES
from pdf_generator import generate_pdf_report as generate_pdf_report_impl

# ==================== Tavily API 配置 ====================
# 安全提示：API Key 必须通过环境变量配置，切勿硬编码
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')

# ==================== 配置加载 ====================
def load_user_config(config_path=None):
    if config_path is None:
        config_path = CONFIG_DIR / 'user_config.json'
    if not os.path.exists(config_path):
        return _get_default_config()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"警告：读取配置文件失败 - {e}", file=sys.stderr)
        return _get_default_config()

def _get_default_config():
    return {
        "user_profile": {
            "name": "东东", "gender": "男", "age": 34, "height_cm": 172,
            "current_weight_kg": 65, "target_weight_kg": 64, "condition": "胆结石", "activity_level": 1.2,
            "dietary_preferences": {"dislike": ["鱼", "蛙", "海鲜"], "allergies": ["海鲜"], "favorite_fruits": ["苹果", "耙耙柑", "香蕉", "梨"]}
        },
        "condition_standards": {"胆结石": {"fat_min_g": 40, "fat_max_g": 50, "fiber_min_g": 25, "water_min_ml": 2000}},
        "scoring_weights": {"diet": 0.45, "water": 0.35, "weight": 0.20, "exercise_bonus": 0.10},
        "exercise_standards": {"weekly_target_minutes": 150}
    }

def get_condition_standards(config, condition_name):
    standards = config.get('condition_standards', {})
    return standards.get(condition_name, standards.get('胆结石', {}))

def get_scoring_weights(config):
    weights = config.get('scoring_weights', {'diet': 0.45, 'water': 0.35, 'weight': 0.20})
    weights = {k: v for k, v in weights.items() if isinstance(v, (int, float)) and k != 'exercise_bonus'}
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()} if total > 0 else weights

def get_exercise_bonus_weight(config):
    weights = config.get('scoring_weights', {})
    return weights.get('exercise_bonus', 0.10)

# ==================== 基础计算 ====================
def calculate_bmi(weight_kg, height_cm):
    if not weight_kg or not height_cm: return 0
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def calculate_bmr(weight_kg, height_cm, age, gender):
    if gender == '男':
        return round(10 * weight_kg + 6.25 * height_cm - 5 * age + 5, 1)
    return round(10 * weight_kg + 6.25 * height_cm - 5 * age - 161, 1)

def calculate_tdee(bmr, activity_level):
    return round(bmr * activity_level, 1)

# ==================== 食物解析 ====================
def parse_food_entry(entry_text):
    entry = entry_text.strip()
    for portion_prefix, portion_grams in DEFAULT_PORTIONS.items():
        if entry.startswith(portion_prefix):
            food_name = entry[len(portion_prefix):].strip()
            return food_name if food_name else portion_prefix, portion_grams
    return entry, 100

def estimate_nutrition(food_name, portion_grams, calories_db):
    nutrition = None
    if food_name in calories_db:
        nutrition = calories_db[food_name]
    else:
        for db_name, db_nutrition in calories_db.items():
            if db_name in food_name or food_name in db_name:
                nutrition = db_nutrition
                break
    if nutrition is None:
        nutrition = {"calories": 100, "protein": 10, "fat": 5, "carb": 10, "fiber": 2}
    scale = portion_grams / 100.0
    return {k: round(nutrition.get(k, 0) * scale, 1) for k in ['calories', 'protein', 'fat', 'carb', 'fiber']}

# ==================== 评分计算 ====================
def calculate_diet_score(daily_data, standards, scoring_standards):
    diet_weights = scoring_standards.get('diet', {'fat_score_weight': 0.30, 'protein_score_weight': 0.25, 'fiber_score_weight': 0.25, 'avoid_food_penalty': 0.20})
    total_fat = daily_data.get('total_fat', 0)
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fat_score = 100 if fat_min <= total_fat <= fat_max else max(0, 100 - (fat_min - total_fat) * 5 if total_fat < fat_min else (total_fat - fat_max) * 8)
    total_fiber = daily_data.get('total_fiber', 0)
    fiber_min = standards.get('fiber_min_g', 25)
    fiber_score = 100 if total_fiber >= fiber_min else max(0, 100 - (fiber_min - total_fiber) * 4)
    avoid_count = len(daily_data.get('avoid_foods', []))
    avoid_penalty = min(100, avoid_count * 25)
    score = (fat_score * diet_weights.get('fat_score_weight', 0.30) + fiber_score * diet_weights.get('fiber_score_weight', 0.25) + (100 - avoid_penalty) * diet_weights.get('avoid_food_penalty', 0.20) + 100 * diet_weights.get('protein_score_weight', 0.25))
    return max(0, min(100, round(score, 1)))

def calculate_water_score(water_total, water_target):
    if water_total >= water_target: return 100
    percentage = water_total / water_target
    if percentage >= 0.8: return round(80 + (percentage - 0.8) * 100, 1)
    elif percentage >= 0.5: return round(50 + (percentage - 0.5) * 60, 1)
    else: return round(percentage * 100, 1)

def calculate_weight_score(weight_recorded, target_weight, current_weight):
    score = 50 if weight_recorded else 0
    if current_weight and target_weight:
        diff = abs(current_weight - target_weight)
        score += 50 if diff <= 1 else (30 if diff <= 3 else (15 if diff <= 5 else 0))
    return max(0, min(100, score))

def calculate_exercise_score(exercise_data, exercise_standards, scoring_standards):
    try:
        if not exercise_data or not isinstance(exercise_data, list): return 0
        exercise_weights = scoring_standards.get('exercise', {'duration_score_weight': 0.40, 'frequency_score_weight': 0.30, 'calorie_score_weight': 0.30, 'daily_calorie_target': 300})
        total_minutes = sum(e.get('duration_min', 0) for e in exercise_data if isinstance(e, dict))
        daily_target = exercise_standards.get('weekly_target_minutes', 150) / 7
        duration_score = 100 if total_minutes >= daily_target else round((total_minutes / daily_target) * 100, 1) if daily_target > 0 else 0
        frequency_score = 100 if len(exercise_data) > 0 else 0
        total_calories = sum(e.get('calories', 0) for e in exercise_data if isinstance(e, dict))
        calorie_target = exercise_weights.get('daily_calorie_target', 300)
        calorie_score = 100 if total_calories >= calorie_target else round((total_calories / calorie_target) * 100, 1) if calorie_target > 0 else 0
        score = duration_score * exercise_weights.get('duration_score_weight', 0.40) + frequency_score * exercise_weights.get('frequency_score_weight', 0.30) + calorie_score * exercise_weights.get('calorie_score_weight', 0.30)
        return max(0, min(100, round(score, 1)))
    except Exception as e:
        print(f"警告：运动评分计算失败 - {e}", file=sys.stderr)
        return 0

# ==================== 核心修复：增强版文件解析 ====================
def parse_memory_file(file_path):
    """增强版解析健康记录文件（修复食物丢失 + 过饱系数 + 症状惩罚）"""
    data = {
        'date': '', 'weight_morning': None, 'weight_evening': None,
        'water_records': [], 'meals': [], 'exercise_records': [],
        'symptoms': [], 'symptom_keywords': [], 'risks': [], 'plan': {}, 'ai_comment': '',
        'water_total': 0, 'water_target': 2000,
        'total_calories': 0, 'total_protein': 0, 'total_fat': 0, 'total_carb': 0, 'total_fiber': 0,
        'steps': 0, 'overeating_factor': 1.0,
    }
    if not os.path.exists(file_path): return data
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析日期
    date_match = re.search(r'# (\d{4}-\d{2}-\d{2})', content)
    if date_match: data['date'] = date_match.group(1)
    
    # 解析晨起体重
    weight_match = re.search(r'晨起空腹.*?([\d.]+)\s*斤', content)
    if weight_match: data['weight_morning'] = float(weight_match.group(1)) / 2
    
    # 解析饮水记录
    water_blocks = re.findall(r'### (晨起|上午|中午|下午|晚上)[^\n]*\n- 饮水量：(\d+)ml\n- 累计：(\d+)ml/(\d+)ml', content)
    for time_label, amount, cum, target in water_blocks:
        data['water_records'].append({'time': time_label, 'amount_ml': int(amount), 'cumulative_ml': int(cum)})
    if water_blocks:
        data['water_total'] = int(water_blocks[-1][2])
        data['water_target'] = int(water_blocks[-1][3])
    
    # 修复 4A：解析过饱情况（引入过饱系数）
    overeating_matches = re.findall(r'(?:吃 | 感觉).{0,20}?(?:有点饱 | 过饱 | 吃撑 | 吃太饱)', content)
    data['overeating_factor'] = 1.25 if len(overeating_matches) > 0 else 1.0
    
    # 修复 4B：解析症状关键词（用于症状扣分）
    symptom_keywords = ['右上腹涨', '腹涨', '腹胀', '腹痛', '涨痛', '不舒服', '恶心']
    found_symptoms = []
    for kw in symptom_keywords:
        if kw in content:
            found_symptoms.append(kw)
    data['symptom_keywords'] = found_symptoms
    
    # 解析饮食记录（修复 1：增强容错，确保第一行不丢失）
    meal_pattern = r'### (早餐|午餐|晚餐|加餐)[^\n]*'
    meal_starts = [(m.group(1), m.start(), m.end()) for m in re.finditer(meal_pattern, content)]
    
    for i, (meal_type, start, end) in enumerate(meal_starts):
        # 提取标题行（包含时间）
        title_line = content[start:end]
        time_match = re.search(r'[（(]([\d:]+)[)）]', title_line)
        meal_time = time_match.group(1) if time_match else ""
        
        # 提取内容区块（从标题行结束到下一个###或##或文件结尾）
        next_start = meal_starts[i+1][2] if i+1 < len(meal_starts) else len(content)
        section_end = content.find('\n## ', end)
        if section_end != -1 and section_end < next_start:
            next_start = section_end
        meal_content = content[end:next_start]
        
        # 检查该餐是否过饱
        meal_overeating = 1.25 if re.search(r'(?:吃 | 感觉).{0,20}?(?:有点饱 | 过饱 | 吃撑)', meal_content) else 1.0
        
        meal_data = {
            'type': meal_type, 'time': meal_time, 'foods': [], 'food_nutrition': [],
            'total_calories': 0, 'total_protein': 0, 'total_fat': 0, 'total_carb': 0, 'total_fiber': 0,
            'overeating_factor': meal_overeating,
        }
        
        # 修复 1：逐行解析，增强容错，兼容 - 食物，-食物，- 食物 等不同空格情况
        food_lines = meal_content.split('\n')
        for line in food_lines:
            line_stripped = line.strip()
            # 修复 1：只解析食物行（以 - 开头，包含→）
            if line_stripped.startswith('-') and '→' in line_stripped:
                # 跳过总计/评估行
                if any(kw in line_stripped for kw in ['总计', '评估', '蛋白质：', '脂肪：', '碳水：', '纤维：', '维生素']):
                    continue
                # 修复 1：增强正则容错
                food_match = re.match(r'-\s*(.+?)\s*→', line_stripped)
                if food_match:
                    food_name = food_match.group(1).strip()
                    food_name_clean, portion = parse_food_entry(food_name)
                    nutrition = estimate_nutrition(food_name_clean, portion, FOOD_CALORIES)
                    # 修复 4A：应用过饱系数
                    if meal_overeating > 1.0:
                        nutrition = {k: v * meal_overeating for k, v in nutrition.items()}
                    meal_data['foods'].append(food_name)
                    meal_data['food_nutrition'].append({'name': food_name, 'portion_grams': portion, **nutrition})
                    for k in ['calories', 'protein', 'fat', 'carb', 'fiber']:
                        meal_data[f'total_{k}'] += nutrition[k]
        
        data['meals'].append(meal_data)
    
    # 解析运动记录
    exercise_matches = re.findall(r'### (骑行 | 散步 | 跑步 | 其他 | 健身)[^\n]*\n(.*?)(?=\n### |\n## |\Z)', content, re.DOTALL)
    for exercise_type, exercise_content in exercise_matches:
        distance_match = re.search(r'距离.*?(?:：|:)\s*([\d.]+)\s*公里', exercise_content)
        duration_match = re.search(r'耗时.*?(?:：|:)\s*(\d+)\s*分', exercise_content)
        calories_match = re.search(r'(?:消耗 | 总消耗).*?(?:：|:)\s*(\d+)\s*千卡', exercise_content)
        data['exercise_records'].append({
            'type': exercise_type,
            'distance_km': float(distance_match.group(1)) if distance_match else 0,
            'duration_min': int(duration_match.group(1)) if duration_match else 0,
            'calories': int(calories_match.group(1)) if calories_match else 0,
        })
    
    # 解析步数
    steps_match = re.search(r'(?:总步数 | 步数).*?(?:：|:)\s*(\d+)\s*步', content)
    if steps_match: data['steps'] = int(steps_match.group(1))
    
    # 解析症状文本
    symptom_section = re.search(r'## ?📝 ?症状[^\n]*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if symptom_section:
        symptom_text = symptom_section.group(1).strip()
        if symptom_text and '_（无记录）_' not in symptom_text and '（待记录）' not in symptom_text:
            data['symptoms'] = [s.strip() for s in symptom_text.split('\n') if s.strip() and not s.startswith('_')]
    
    # 计算总计
    data['total_calories'] = sum(m.get('total_calories', 0) for m in data['meals'])
    data['total_protein'] = sum(m.get('total_protein', 0) for m in data['meals'])
    data['total_fat'] = sum(m.get('total_fat', 0) for m in data['meals'])
    data['total_carb'] = sum(m.get('total_carb', 0) for m in data['meals'])
    data['total_fiber'] = sum(m.get('total_fiber', 0) for m in data['meals'])
    
    return data

# ==================== AI 健康点评生成 ====================
def generate_ai_comment(health_data, config):
    """调用大模型生成 AI 专属健康点评（≥150 字）"""
    user_profile = config.get('user_profile', {})
    condition = user_profile.get('condition', '胆结石')
    standards = get_condition_standards(config, condition)
    
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fiber_min = standards.get('fiber_min_g', 25)
    
    # 构建 Prompt
    prompt = f"""你是一位专业的私人营养师，专门服务胆结石患者。请根据以下健康数据，生成一段深度健康点评：

【用户档案】
- 称呼：东东
- 病理：胆结石
- 饮食原则：低脂（{fat_min}-{fat_max}g/天）、高纤维（≥{fiber_min}g/天）、规律进食

【今日数据】
- 总热量：{health_data.get('total_calories', 0):.0f} kcal
- 蛋白质：{health_data.get('total_protein', 0):.1f}g
- 脂肪：{health_data.get('total_fat', 0):.1f}g（推荐：{fat_min}-{fat_max}g）
- 碳水：{health_data.get('total_carb', 0):.1f}g
- 膳食纤维：{health_data.get('total_fiber', 0):.1f}g（推荐：≥{fiber_min}g）
- 饮水：{health_data.get('water_total', 0)}ml（目标：{health_data.get('water_target', 2000)}ml）
- 运动：{len(health_data.get('exercise_records', []))}次，{health_data.get('steps', 0)}步
- 过饱系数：{health_data.get('overeating_factor', 1.0)}
- 症状关键词：{health_data.get('symptom_keywords', [])}

【点评要求】
1. 语气：专业但温暖，像私人营养师一样既夸奖又提醒
2. 结构：先肯定做得好的地方，再严肃指出健康隐患
3. 长度：不少于 150 字
4. 重点：结合胆结石病理，强调脂肪控制和胆汁排泄
5. 如有过饱或症状，必须重点警示

请直接输出点评内容，不要加标题或格式："""

    for attempt in range(3):
        try:
            result = subprocess.run(
                ['openclaw', 'agent', '--local', '--to', '+860000000000', '--message', prompt],
                capture_output=True, text=True, timeout=90,
                env={**os.environ, 'SYSTEM_PROMPT': '你是一位专业的私人营养师，专门服务胆结石患者。'}
            )
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                # 清理可能的日志前缀
                if '[plugins]' in output:
                    lines = output.split('\n')
                    clean_lines = [l for l in lines if not l.startswith('[plugins]') and not l.startswith('[adp-')]
                    output = '\n'.join(clean_lines).strip()
                return output
        except subprocess.TimeoutExpired:
            print(f"AI 点评生成超时（第{attempt+1}次），重试中...", file=sys.stderr)
        except Exception as e:
            print(f"AI 点评生成失败（第{attempt+1}次）: {e}", file=sys.stderr)
        if attempt < 2:
            import time
            time.sleep(2)
    
    # 备用方案
    comments = []
    fat_val = health_data.get('total_fat', 0)
    if fat_min <= fat_val <= fat_max:
        comments.append(f"脂肪摄入{fat_val:.1f}g 控制在理想范围内，这对胆结石患者非常关键！")
    elif fat_val < fat_min:
        comments.append(f"脂肪摄入仅{fat_val:.1f}g，略低于推荐值。虽然低脂是好事，但完全无脂可能导致胆汁淤积，建议适量增加健康脂肪（如橄榄油 5ml）。")
    else:
        comments.append(f"脂肪摄入{fat_val:.1f}g 超标！这是胆结石患者的大忌，可能诱发胆绞痛，明日必须严格控油。")
    
    fiber_val = health_data.get('total_fiber', 0)
    if fiber_val >= fiber_min:
        comments.append(f"膳食纤维{fiber_val:.1f}g 达标，有助于胆汁排泄，继续保持！")
    else:
        comments.append(f"膳食纤维仅{fiber_val:.1f}g，严重不足！纤维能促进胆汁排泄，建议明日增加蔬菜、粗粮摄入。")
    
    water_val = health_data.get('water_total', 0)
    water_target = health_data.get('water_target', 2000)
    if water_val >= water_target:
        comments.append(f"饮水{water_val}ml 达标，稀释胆汁效果优秀！")
    else:
        comments.append(f"饮水仅{water_val}ml，未达到{water_target}ml 目标。充足饮水能稀释胆汁，预防结石形成。")
    
    steps = health_data.get('steps', 0)
    if steps >= 6000:
        comments.append(f"今日{steps}步活动量充足，久坐人群的好榜样！")
    elif steps >= 3000:
        comments.append(f"今日{steps}步基本达标，但作为久坐人群还可以更多。")
    else:
        comments.append(f"今日仅{steps}步，活动量严重不足！久坐会导致胆汁淤积，建议明日增加散步或骑行。")
    
    return " ".join(comments)

# ==================== AI 动态次日方案 ====================
def tavily_search(query, max_results=3):
    """调用 Tavily API 搜索最新信息（timeout 60 秒 + 重试 3 次）"""
    import urllib.request
    url = "https://api.tavily.com/search"
    
    for attempt in range(3):
        try:
            data = json.dumps({
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": max_results
            }).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            resp = urllib.request.urlopen(req, timeout=60)
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('results', [])
        except Exception as e:
            print(f"Tavily 搜索失败（第{attempt+1}次）: {e}", file=sys.stderr)
            if attempt < 2:
                import time
                time.sleep(2)
    return []

def generate_ai_plan(health_data, config):
    """调用大模型生成动态次日方案（结合 tavily-search）"""
    user_profile = config.get('user_profile', {})
    condition = user_profile.get('condition', '胆结石')
    standards = get_condition_standards(config, condition)
    
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fiber_min = standards.get('fiber_min_g', 25)
    
    # 分析今日短板
    shortcomings = []
    fat_val = health_data.get('total_fat', 0)
    fiber_val = health_data.get('total_fiber', 0)
    water_val = health_data.get('water_total', 0)
    steps = health_data.get('steps', 0)
    
    if fat_val < fat_min * 0.8:
        shortcomings.append('脂肪摄入过低')
    elif fat_val > fat_max:
        shortcomings.append('脂肪摄入超标')
    
    if fiber_val < fiber_min * 0.8:
        shortcomings.append('膳食纤维不足')
    
    if water_val < 1500:
        shortcomings.append('饮水不足')
    
    if steps < 3000:
        shortcomings.append('缺乏运动')
    
    # Tavily 搜索
    recipes = []
    exercises = []
    
    if '脂肪摄入超标' in shortcomings or '脂肪摄入过低' in shortcomings:
        recipe_results = tavily_search('胆结石患者低脂高蛋白快手菜谱 2026', max_results=2)
        recipes = [r.get('content', '') for r in recipe_results[:2]]
    
    if '缺乏运动' in shortcomings:
        exercise_results = tavily_search('久坐人群办公室拉伸动作 胆结石患者适合的运动 2026', max_results=2)
        exercises = [r.get('content', '') for r in exercise_results[:2]]
    
    # 构建 Prompt
    prompt = f"""你是一位专业的私人营养师，专门服务胆结石患者。请根据以下数据生成明日优化方案：

【用户档案】
- 称呼：东东
- 病理：胆结石
- 饮食原则：低脂（{fat_min}-{fat_max}g/天）、高纤维（≥{fiber_min}g/天）
- 不爱吃：鱼、蛙、海鲜（过敏）
- 爱吃水果：苹果、耙耙柑、香蕉、梨

【今日短板】
{', '.join(shortcomings) if shortcomings else '今日表现完美，继续保持！'}

【搜索参考】（如有）
菜谱参考：{recipes[:1] if recipes else '无'}
运动参考：{exercises[:1] if exercises else '无'}

【方案要求】
1. 推荐食谱：早中晚三餐，每餐标注卡路里，总热量控制在 1500-1800kcal
2. 运动建议：针对久坐人群，适合胆结石患者的温和运动
3. 饮水计划：分时段提醒，总量 2000ml
4. 特别关注：根据今日短板给出针对性建议
5. 格式：JSON，包含 diet（数组）、exercise（数组）、water（数组）、notes（数组）

请直接输出 JSON 格式，不要其他文字："""

    for attempt in range(3):
        try:
            result = subprocess.run(
                ['openclaw', 'agent', '--local', '--to', '+860000000000', '--message', prompt],
                capture_output=True, text=True, timeout=90,
                env={**os.environ, 'SYSTEM_PROMPT': '你是一位专业的私人营养师。输出纯 JSON，不要其他文字。'}
            )
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                # 清理日志前缀
                if '[plugins]' in output:
                    lines = output.split('\n')
                    clean_lines = [l for l in lines if not l.startswith('[plugins]') and not l.startswith('[adp-')]
                    output = '\n'.join(clean_lines).strip()
                # 尝试解析 JSON
                json_match = re.search(r'\{.*\}', output, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                    return plan
        except subprocess.TimeoutExpired:
            print(f"AI 方案生成超时（第{attempt+1}次），重试中...", file=sys.stderr)
        except Exception as e:
            print(f"AI 方案生成失败（第{attempt+1}次）: {e}", file=sys.stderr)
        if attempt < 2:
            import time
            time.sleep(2)
    
    # 备用方案
    plan = {
        'diet': [
            '早餐（5 分钟）：燕麦粥 + 煮蛋白 2 个 + 凉拌黄瓜 (300kcal)',
            '午餐（10 分钟）：米饭 + 卤牛肉 + 白灼青菜 (450kcal)',
            '晚餐（10 分钟）：杂粮粥 + 凉拌豆腐 + 炒蔬菜 (350kcal)',
        ],
        'water': [
            '⏰ 07:30 晨起温水 300ml', '⏰ 10:00 工作间隙 400ml',
            '⏰ 14:00 午后 400ml', '⏰ 17:00 下班前 400ml', '⏰ 20:00 晚间 300ml',
            f'📊 目标总量：2000ml',
        ],
        'exercise': [
            '🚶 早餐后散步 15 分钟（促进胆汁排泄）',
            '🚶 晚餐后散步 20 分钟（帮助消化）',
            '💡 本周目标：累计运动 150 分钟',
        ],
        'notes': ['今日推荐水果：苹果，耙耙柑，香蕉，梨'],
    }
    
    if health_data.get('overeating_factor', 1.0) > 1.0:
        plan['notes'].append('昨日过饱，今日控制食量，七分饱即可')
    if '脂肪摄入过低' in shortcomings:
        plan['notes'].append('昨日脂肪过低，今日适量增加健康脂肪（橄榄油 5-10ml 或坚果 10g）')
    elif '脂肪摄入超标' in shortcomings:
        plan['notes'].append('昨日脂肪超标，今日严格控油，避免油炸、红烧')
    if '膳食纤维不足' in shortcomings:
        plan['notes'].append('昨日纤维不足，今日增加蔬菜、粗粮摄入')
    if '缺乏运动' in shortcomings:
        plan['notes'].append('昨日活动量不足，今日增加散步或骑行')
    
    return plan

# ==================== 文本报告生成（完整版） ====================
def get_star_string(score):
    stars_count = max(1, min(5, int(score / 20)))
    return "⭐" * stars_count

def generate_text_report(health_data, config, date):
    """生成完整文本报告（AI 点评 + 动态方案）"""
    user_profile = config.get('user_profile', {})
    condition = user_profile.get('condition', '胆结石')
    standards = get_condition_standards(config, condition)
    scoring_weights = get_scoring_weights(config)
    scoring_standards = config.get('scoring_standards', {})
    exercise_standards = config.get('exercise_standards', {})
    
    # 计算各项评分
    diet_score = calculate_diet_score(health_data, standards, scoring_standards)
    water_score = calculate_water_score(health_data.get('water_total', 0), health_data.get('water_target', 2000))
    weight_score = calculate_weight_score(health_data.get('weight_morning') is not None, user_profile.get('target_weight_kg', 64), health_data.get('weight_morning'))
    exercise_score = calculate_exercise_score(health_data.get('exercise_records', []), exercise_standards, scoring_standards)
    
    # 基础分（饮食 + 饮水 + 体重）
    base_score = round(diet_score * scoring_weights.get('diet', 0.45) + water_score * scoring_weights.get('water', 0.35) + weight_score * scoring_weights.get('weight', 0.20), 1)
    
    # 运动加分（Bonus，上限 10 分）
    exercise_bonus = round(exercise_score * get_exercise_bonus_weight(config), 1)
    total_score = min(100, round(base_score + exercise_bonus, 1))
    
    # 修复 4B：症状扣分
    symptom_penalty = 0
    if health_data.get('symptom_keywords'):
        symptom_penalty = len(health_data['symptom_keywords']) * 20  # 每个症状扣 20 分
    symptom_score = max(0, 100 - symptom_penalty)
    
    # 计算 BMI、BMR、TDEE
    weight_kg = health_data.get('weight_morning')
    bmi = calculate_bmi(weight_kg, user_profile.get('height_cm', 172)) if weight_kg else 0
    bmr = calculate_bmr(weight_kg if weight_kg else 65, user_profile.get('height_cm', 172), user_profile.get('age', 34), user_profile.get('gender', '男')) if weight_kg else 0
    tdee = calculate_tdee(bmr, user_profile.get('activity_level', 1.2)) if bmr else 0
    
    # 生成 AI 点评和方案
    ai_comment = health_data.get('ai_comment', '') or generate_ai_comment(health_data, config)
    ai_plan = health_data.get('plan', {}) or generate_ai_plan(health_data, config)
    
    # 生成报告
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fiber_min = standards.get('fiber_min_g', 25)
    
    report = f"""✅ **晚间数据已记录！**

### 🌟 {date} 今日综合评分

🎯 **总分：{get_star_string(total_score)} {total_score}/100**（基础分{base_score:.1f} + 运动加分{exercise_bonus:.1f}）

---

📊 **分项汇总**

* **饮食合规性** {get_star_string(diet_score)} {diet_score}/100
  {'✅ 脂肪摄入合理' if fat_min <= health_data.get('total_fat', 0) <= fat_max else '⚠️ 脂肪摄入过低' if health_data.get('total_fat', 0) < fat_min else '⚠️ 脂肪摄入超标'} ({health_data.get('total_fat', 0):.1f}g) | {'✅ 蛋白质摄入充足' if health_data.get('total_protein', 0) >= 60 else '⚠️ 蛋白质不足'}

* **饮水完成度** {get_star_string(water_score)} {water_score}/100
  {health_data.get('water_total', 0)}ml/{health_data.get('water_target', 2000)}ml，{health_data.get('water_total', 0) // 20}% 完成度

* **体重管理** {get_star_string(weight_score)} {weight_score}/100
  晨起空腹：{(health_data.get('weight_morning') or 0) * 2:.1f}斤，BMI：{bmi:.1f}

* **症状管理** {get_star_string(symptom_score)} {symptom_score}/100
  {'✅ 无不适症状' if not health_data.get('symptom_keywords') else '⚠️ ' + '；'.join(health_data.get('symptom_keywords', []))}

* **运动管理** {get_star_string(exercise_score)} {exercise_score}/100
  {generate_exercise_summary(health_data)}

* **健康依从性** {get_star_string(100 if len(health_data.get('meals', [])) >= 3 else 50)} {100 if len(health_data.get('meals', [])) >= 3 else 50}/100
  完成{len(health_data.get('meals', []))}餐，饮水{'达标' if health_data.get('water_total', 0) >= health_data.get('water_target', 2000) else '未达标'}

---

### 🤖 AI 专属健康点评

{ai_comment}

---

### 📝 今日详情汇总

**🥗 进食情况**
{generate_meal_summary(health_data)}

**💧 饮水情况**
{generate_water_summary(health_data)}

**🏃 运动情况**
{generate_exercise_detail(health_data)}

---

### 📈 基础健康数据

**身体指标**
* 身高：{user_profile.get('height_cm', 172)}cm
* 体重：{(health_data.get('weight_morning') or 0) * 2:.1f}斤（{weight_kg if weight_kg else '未记录'}kg）
* BMI：{bmi:.1f}
* 基础代谢 (BMR)：{bmr:.0f} kcal
* 每日消耗 (TDEE)：{tdee:.0f} kcal

**热量与营养素**
* 当日摄入热量：{health_data.get('total_calories', 0):.0f} kcal
* 蛋白质：{health_data.get('total_protein', 0):.1f}g（推荐{user_profile.get('current_weight_kg', 65) * 1.2:.0f}g）
* 脂肪：{health_data.get('total_fat', 0):.1f}g（推荐{standards.get('fat_min_g', 40)}-{standards.get('fat_max_g', 50)}g）
* 碳水：{health_data.get('total_carb', 0):.1f}g（推荐{(tdee * 0.55 / 4):.0f}g）
* 膳食纤维：{health_data.get('total_fiber', 0):.1f}g（推荐≥{standards.get('fiber_min_g', 25)}g）

---

### 📋 次日优化方案（AI 动态生成）

{generate_plan_text(ai_plan)}

---
"""
    return report

def generate_meal_summary(health_data):
    meals = health_data.get('meals', [])
    if not meals: return '无记录'
    lines = []
    for meal in meals:
        foods = '、'.join(meal.get('foods', [])[:3])
        if len(meal.get('foods', [])) > 3: foods += ' 等'
        lines.append(f"{meal.get('type', '')}({meal.get('time', '')}): {foods} - {meal.get('total_calories', 0):.0f}kcal")
    return '\n'.join(lines) if lines else '无详细记录'

def generate_water_summary(health_data):
    records = health_data.get('water_records', [])
    if not records: return '无记录'
    lines = []
    for r in records[:6]:
        lines.append(f"{r.get('time', '')}: {r.get('amount_ml', 0)}ml")
    lines.append(f"→ 总计：{health_data.get('water_total', 0)}ml/{health_data.get('water_target', 2000)}ml")
    return '\n'.join(lines)

def generate_exercise_summary(health_data):
    exercises = health_data.get('exercise_records', [])
    steps = health_data.get('steps', 0)
    if not exercises and steps == 0: return '无记录'
    parts = []
    for e in exercises:
        if e.get('type') == '骑行':
            parts.append(f"骑行：{e.get('distance_km', 0)}km/{e.get('duration_min', 0)}分钟")
    if steps > 0:
        parts.append(f"步数：{steps}步")
    return '；'.join(parts) if parts else '无记录'

def generate_exercise_detail(health_data):
    exercises = health_data.get('exercise_records', [])
    steps = health_data.get('steps', 0)
    if not exercises and steps == 0: return '无记录'
    lines = []
    cycling = [e for e in exercises if e.get('type') == '骑行']
    if cycling:
        total_km = sum(e.get('distance_km', 0) for e in cycling)
        total_min = sum(e.get('duration_min', 0) for e in cycling)
        details = [f"{e.get('distance_km', 0)}km/{e.get('duration_min', 0)}分钟" for e in cycling]
        lines.append(f"骑行：{'、'.join(details)}（合计{total_km:.2f}km/{total_min:.1f}分钟）")
    if steps > 0:
        lines.append(f"步数：{steps}步")
    return '\n'.join(lines) if lines else '无详细记录'

def generate_plan_text(plan):
    """修复 2 和 3：处理 AI 返回的 JSON 对象数组格式（增强通用性，兼容不同大模型）"""
    lines = []
    
    # 修复 2：文字修改 - "饮食建议"改成"饮食计划"
    if plan.get('diet'):
        lines.append('**🥗 饮食计划**')
        for item in plan.get('diet', []):
            if isinstance(item, dict):
                # 修复 3：兼容不同大模型的字段名
                meal = item.get('meal', item.get('meal_name', ''))
                time = item.get('time', item.get('time_range', item.get('period', '')))
                # 兼容多种字段名：menu/items/dishes/menu_detail/food/content
                menu = item.get('menu', '')
                if not menu:
                    # AI 返回的是 items 数组（千问 3.5plus 格式）
                    items = item.get('items', [])
                    if items:
                        menu = '、'.join(str(i) for i in items[:3])  # 只显示前 3 项
                        if len(items) > 3:
                            menu += ' 等'
                # 如果还是空，尝试其他字段名
                if not menu:
                    menu = item.get('dishes', item.get('menu_detail', item.get('food', item.get('content', ''))))
                calories = item.get('calories', item.get('kcal', ''))
                fat = item.get('fat', item.get('fat_g', ''))
                fiber = item.get('fiber', item.get('fiber_g', ''))
                if menu:
                    nutrition = f"({calories}kcal"
                    if fat: nutrition += f", 脂肪{fat}g"
                    if fiber: nutrition += f", 纤维{fiber}g"
                    nutrition += ")"
                    lines.append(f"* {time} {menu} {nutrition}")
                elif meal and time:
                    lines.append(f"* {meal} ({time})")
                else:
                    lines.append(f"* {item}")
            else:
                # 修复 3：如果是字符串（其他大模型直接返回文本），直接使用
                lines.append(f'* {item}')
        lines.append('')
    
    # 处理饮水计划
    if plan.get('water'):
        lines.append('**💧 饮水计划**')
        for item in plan.get('water', []):
            if isinstance(item, dict):
                # 修复 3：兼容不同大模型的字段名
                time = item.get('time', item.get('period', ''))
                amount = item.get('amount', item.get('amount_ml', item.get('volume', '')))
                # 确保 amount 带单位
                if amount and not any(unit in str(amount) for unit in ['ml', 'L']):
                    amount = f"{amount}ml"
                note = item.get('note', item.get('tip', item.get('remark', '')))
                lines.append(f"* ⏰ {time} {amount} ({note})")
            else:
                # 修复 3：如果是字符串（其他大模型直接返回文本），直接使用
                lines.append(f'* {item}')
        lines.append('')
    
    # 处理运动建议
    if plan.get('exercise'):
        lines.append('**🏃 运动建议**')
        for item in plan.get('exercise', []):
            if isinstance(item, dict):
                # 修复 3：兼容不同大模型的字段名
                time = item.get('time', item.get('time_range', item.get('period', '')))
                activity = item.get('activity', item.get('type', item.get('name', '')))
                duration = item.get('duration', item.get('duration_min', item.get('time_length', '')))
                details = item.get('details', item.get('description', item.get('desc', item.get('content', ''))))
                # 确保所有字段都有值
                if activity and duration and details:
                    lines.append(f"* {time} {activity} ({duration}): {details}")
                elif activity and duration:
                    lines.append(f"* {time} {activity} ({duration})")
                elif activity:
                    lines.append(f"* {time} {activity}")
                else:
                    lines.append(f"* {time}")
            else:
                # 修复 3：如果是字符串（其他大模型直接返回文本），直接使用
                lines.append(f'* {item}')
        lines.append('')
    
    # 处理特别关注
    if plan.get('notes'):
        lines.append('**⚠️ 特别关注**')
        for item in plan.get('notes', []):
            lines.append(f'* {item}')
    
    return '\n'.join(lines)

# ==================== PDF 报告生成（完整数据） ====================
def generate_report(memory_file, date):
    """主报告生成函数（AI 点评 + 动态方案 + 完整数据）"""
    config = load_user_config()
    user_profile = config.get('user_profile', {})
    condition = user_profile.get('condition', '胆结石')
    standards = get_condition_standards(config, condition)
    scoring_standards = config.get('scoring_standards', {})
    exercise_standards = config.get('exercise_standards', {})
    
    # 解析健康记录
    health_data = parse_memory_file(memory_file)
    
    # 计算各项评分
    diet_score = calculate_diet_score(health_data, standards, scoring_standards)
    water_score = calculate_water_score(health_data.get('water_total', 0), health_data.get('water_target', 2000))
    weight_score = calculate_weight_score(health_data.get('weight_morning') is not None, user_profile.get('target_weight_kg', 64), health_data.get('weight_morning'))
    exercise_score = calculate_exercise_score(health_data.get('exercise_records', []), exercise_standards, scoring_standards)
    
    # 基础分 + 运动加分
    scoring_weights = get_scoring_weights(config)
    base_score = round(diet_score * scoring_weights.get('diet', 0.45) + water_score * scoring_weights.get('water', 0.35) + weight_score * scoring_weights.get('weight', 0.20), 1)
    exercise_bonus = round(exercise_score * get_exercise_bonus_weight(config), 1)
    total_score = min(100, round(base_score + exercise_bonus, 1))
    
    # 生成 AI 点评和方案
    ai_comment = generate_ai_comment(health_data, config)
    ai_plan = generate_ai_plan(health_data, config)
    
    health_data['ai_comment'] = ai_comment
    health_data['plan'] = ai_plan
    
    # 准备 PDF 数据
    bmi = calculate_bmi(health_data.get('weight_morning'), user_profile.get('height_cm', 172)) if health_data.get('weight_morning') else 0
    
    pdf_scores_dict = {
        'diet': {'raw': diet_score, 'stars': get_star_string(diet_score)},
        'water': {'raw': water_score, 'stars': get_star_string(water_score)},
        'weight': {'raw': weight_score, 'stars': get_star_string(weight_score), 'bmi': bmi},
        'exercise': {'raw': exercise_score, 'stars': get_star_string(exercise_score)},
        'symptom': {'raw': 100 if not health_data.get('symptom_keywords') else max(0, 100 - len(health_data['symptom_keywords']) * 20), 'stars': get_star_string(100 if not health_data.get('symptom_keywords') else max(0, 100 - len(health_data['symptom_keywords']) * 20)), 'has_symptoms': bool(health_data.get('symptom_keywords'))},
        'adherence': {'raw': 100 if len(health_data.get('meals', [])) >= 3 else 50, 'stars': get_star_string(100 if len(health_data.get('meals', [])) >= 3 else 50)},
        'total': total_score,
        'total_stars': get_star_string(total_score)
    }
    
    # 计算 macros
    tdee = calculate_tdee(calculate_bmr(health_data.get('weight_morning') or 65, user_profile.get('height_cm', 172), user_profile.get('age', 34), user_profile.get('gender', '男')), user_profile.get('activity_level', 1.2))
    macros = {
        'protein_p': 15, 'fat_p': 25, 'carb_p': 60,
        'protein_g': round(user_profile.get('current_weight_kg', 65) * 1.2),
        'fat_g': round(standards.get('fat_max_g', 50)),
        'carb_g': round(tdee * 0.60 / 4),
        'fiber_min_g': standards.get('fiber_min_g', 25)
    }
    
    pdf_filename = f"health_report_{date}.pdf"
    local_pdf_path = str(REPORTS_DIR / pdf_filename)
    web_dir = os.environ.get("REPORT_WEB_DIR", "")
    base_url = os.environ.get("REPORT_BASE_URL", "https://agent.btc354.com").rstrip('/')
    
    # 生成 PDF（传入真实数据）
    try:
        generate_pdf_report_impl(
            data=health_data,
            profile=user_profile,
            scores=pdf_scores_dict,
            nutrition={
                'calories': health_data.get('total_calories', 0),
                'protein': health_data.get('total_protein', 0),
                'fat': health_data.get('total_fat', 0),
                'carb': health_data.get('total_carb', 0),
                'fiber': health_data.get('total_fiber', 0),
            },
            macros=macros,
            risks=[],
            plan=ai_plan,
            output_path=local_pdf_path,
            water_records=health_data.get('water_records', []),
            meals=health_data.get('meals', []),
            exercise_data=health_data.get('exercise_records', []),
            ai_comment=ai_comment  # 修复 3：传递 AI 点评到 PDF
        )
        
        # 复制到 Web 目录
        if web_dir and os.path.exists(web_dir):
            web_pdf_path = os.path.join(web_dir, pdf_filename)
            shutil.copy2(local_pdf_path, web_pdf_path)
            pdf_url = f"{base_url}/{pdf_filename}"
        else:
            print(f"提示：未配置 REPORT_WEB_DIR 或目录不存在，PDF 仅保存在本地 {local_pdf_path}", file=sys.stderr)
            pdf_url = f"{base_url}/{pdf_filename}"
    except Exception as e:
        print(f"警告：PDF 生成失败 - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        pdf_url = f"{base_url}/{pdf_filename}"
    
    # 生成文本报告
    text_report = generate_text_report(health_data, config, date)
    
    return text_report, pdf_url

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 health_report_pro.py <memory_file> <date>")
        sys.exit(1)
    
    memory_file = sys.argv[1]
    date = sys.argv[2]
    
    try:
        text_report, pdf_url = generate_report(memory_file, date)
        print("=== TEXT_REPORT_START ===")
        print(text_report)
        print("=== TEXT_REPORT_END ===")
        print("=== PDF_URL ===")
        print(pdf_url)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

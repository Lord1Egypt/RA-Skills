"""
讲解词一键生成
功能：用户输入文物名、博物馆、API信息 → 自动判断风格 → 生成讲解词

使用方法：
    python narration_generator.py

流程：
    1. 配置 API（如未配置）
    2. 输入文物名称和博物馆
    3. 可选：输入用户画像和问题
    4. 自动判断风格并生成讲解词（用户不可见风格判断过程）
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_user_config, save_user_config, call_api, load_prompts


def get_api_config():
    """获取 API 配置，引导用户输入"""
    config = load_user_config()
    api = config.get("api", {})
    
    print("\n" + "="*60)
    print("API 配置".center(50))
    print("="*60)
    
    # 检查是否已有配置
    if api.get("api_key") and api.get("base_url") and api.get("model_narration"):
        print("✓ 已检测到 API 配置")
        print(f"  Base URL: {api['base_url']}")
        print(f"  模型(讲解): {api['model_narration']}")
        print(f"  模型(风格): {api.get('model_style', '未设置')}")
        
        choice = input("\n是否重新配置? (y/N): ").strip().lower()
        if choice != 'y':
            return config
    else:
        print("首次使用，请配置您的 API 信息")
    
    # 引导用户输入
    print("\n请输入以下信息:")
    
    base_url = input("  API Base URL: ").strip()
    if not base_url:
        print("✗ Base URL 不能为空")
        sys.exit(1)
    
    api_key = input("  API Key: ").strip()
    if not api_key:
        print("✗ API Key 不能为空")
        sys.exit(1)
    
    model_narration = input("  讲解词生成模型: ").strip()
    if not model_narration:
        print("✗ 讲解词生成模型不能为空")
        sys.exit(1)
    
    model_style = input("  风格判断模型（可与讲解模型相同）: ").strip() or model_narration
    
    timeout_str = input("  超时时间（秒，默认60）: ").strip()
    timeout = int(timeout_str) if timeout_str else 60
    
    # 更新配置
    config["api"] = {
        "base_url": base_url,
        "api_key": api_key,
        "model_narration": model_narration,
        "model_style": model_style,
        "timeout": timeout
    }
    
    save_user_config(config)
    print("\n✓ API 配置已保存")
    
    return config


def get_relic_info():
    """获取文物信息"""
    print("\n" + "="*60)
    print("文物信息".center(50))
    print("="*60)
    
    relic_name = input("文物名称: ").strip()
    if not relic_name:
        print("✗ 文物名称不能为空")
        return None, None
    
    museum = input("所在博物馆（可选）: ").strip() or "未知博物馆"
    
    return relic_name, museum


def get_user_profile():
    """获取用户画像和问题"""
    print("\n" + "="*60)
    print("听众画像（可选）".center(50))
    print("="*60)
    
    print("\n预设听众:")
    print("  1. 普通游客（默认）")
    print("  2. 儿童")
    print("  3. 学者/研究者")
    print("  4. 自定义描述")
    
    choice = input("\n请选择 (1-4，直接回车默认1): ").strip()
    
    profile_map = {
        "2": "8岁儿童",
        "3": "历史学者",
        "4": None
    }
    
    if choice in profile_map:
        user_profile = profile_map[choice]
        if user_profile is None:
            user_profile = input("请描述听众: ").strip() or "普通游客"
    else:
        user_profile = "普通游客"
    
    user_question = input("\n额外问题（可选）: ").strip()
    
    return user_profile, user_question


def judge_style(config, user_profile, user_question):
    """内部判断讲解风格（用户不可见）"""
    prompts = load_prompts()
    
    prompt = prompts["style"].format(
        user_profile=user_profile,
        user_question=user_question or "无"
    )
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = call_api(config, config["api"]["model_style"], messages)
        style = response["choices"][0]["message"]["content"].strip()
        
        # 校验风格
        valid_styles = ["深度学术型", "儿童探索型", "通识全面型"]
        if style not in valid_styles:
            style = "通识全面型"
        
        return style
    except Exception:
        return "通识全面型"


def generate_narration(config, relic_name, style, user_question):
    """生成讲解词"""
    prompts = load_prompts()
    
    # 构建用户问题部分
    if user_question:
        user_question_section = f"用户问题：{user_question}\n请在讲解开头优先回答用户问题。"
    else:
        user_question_section = ""
    
    prompt = prompts["narration"].format(
        relic_name=relic_name,
        style=style,
        user_question_section=user_question_section
    )
    
    messages = [{"role": "user", "content": prompt}]
    
    response = call_api(config, config["api"]["model_narration"], messages)
    narration = response["choices"][0]["message"]["content"].strip()
    char_count = len(narration.replace("\n", "").replace(" ", ""))
    return narration, char_count


def save_result(relic_name, narration):
    """保存结果"""
    output_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(output_dir, f"讲解词_{relic_name}.txt")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(narration)
    
    return output_file


def main():
    """主程序"""
    print("\n" + "="*60)
    print("🖼️  文物讲解词一键生成".center(40))
    print("="*60)
    
    # 1. 获取 API 配置
    config = get_api_config()
    
    # 2. 获取文物信息
    relic_name, museum = get_relic_info()
    if not relic_name:
        sys.exit(1)
    
    # 3. 获取用户画像
    user_profile, user_question = get_user_profile()
    
    # 4. 确认
    print("\n" + "-"*60)
    print(f"文物: {relic_name} | 博物馆: {museum} | 听众: {user_profile}")
    confirm = input("确认生成? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("已取消")
        sys.exit(0)
    
    # 5. 自动判断风格（内部处理，用户不可见）
    style = judge_style(config, user_profile, user_question)
    
    # 6. 生成讲解词
    print("\n生成中...")
    try:
        narration, char_count = generate_narration(config, relic_name, style, user_question)
    except Exception as e:
        print(f"✗ 生成失败: {str(e)}")
        sys.exit(1)
    
    # 7. 保存结果
    output_file = save_result(relic_name, narration)
    
    # 8. 输出讲解词
    print("\n" + "="*60)
    print(narration)
    print("\n" + "-"*60)
    print(f"字数: {char_count} | 已保存: {output_file}")


if __name__ == "__main__":
    main()

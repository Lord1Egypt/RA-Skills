#!/usr/bin/env python3
"""
历史人物数字分身伴游 - 主入口脚本
用法: 
  单次调用: python3 tour_guide.py --character <人物ID> --relic <文物名称> [--mode explain]
  交互式会话: python3 tour_guide.py --interactive
"""

import json
import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from session_manager import SessionManager, create_session_manager

sys.path.insert(0, str(Path(__file__).parent))
from character_loader import CharacterLoader
from relic_presenter import RelicPresenter
from utils import build_system_prompt


def parse_args():
    parser = argparse.ArgumentParser(description='历史人物数字分身伴游')
    parser.add_argument('--character', '-c', help='历史人物ID')
    parser.add_argument('--relic', '-r', help='文物名称')
    parser.add_argument('--mode', '-m', default='explain', 
                       choices=['explain', 'intro', 'greeting', 'interactive'],
                       help='模式: explain=讲解, intro=自我介绍, greeting=问候, interactive=交互式会话')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='进入交互式会话模式')
    args = parser.parse_args()
    
    if args.interactive:
        args.mode = 'interactive'
    
    if args.mode == 'interactive':
        return args
    
    if args.mode in ['explain'] and not (args.character and args.relic):
        parser.error('单次调用模式需要 --character 和 --relic')
    
    return args


def is_switch_intent(text: str) -> str:
    """检查是否有意图切换人物，返回人物名称否则返回None"""
    switch_words = ['换成', '换个', '换个人', '召唤', '让', '试试']
    if not any(w in text for w in switch_words):
        return None
    
    # 尝试识别人物
    CHAR_PATTERNS = [
        r'(李白|诗仙|太白|青莲)', r'(苏轼|东坡|子瞻)',
        r'(孔子|仲尼|至圣)', r'(诸葛亮|卧龙|孔明)',
        r'(李清照|易安)', r'(张骞|博望侯)', r'(王羲之|书圣)',
    ]
    for pattern in CHAR_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


# 人物识别模式（在函数外部定义以便复用）
CHAR_PATTERNS = [
    r'(李白|诗仙|太白|青莲)', r'(苏轼|东坡|子瞻)',
    r'(孔子|仲尼|至圣)', r'(诸葛亮|卧龙|孔明)',
    r'(李清照|易安)', r'(张骞|博望侯)', r'(王羲之|书圣)',
]


def call_llm(system_prompt: str, user_message: str) -> str:
    """调用大模型"""
    from api_config import load_api_config
    import requests
    
    config = load_api_config()
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {config['api_key']}"}
    payload = {
        "model": config['model'],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }
    
    response = requests.post(config['api_base'], headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


def analyze_user_intent(user_input: str, current_character: str = None) -> dict:
    """使用大模型分析用户输入的意图
    
    Args:
        user_input: 用户输入的文本
        current_character: 当前激活的人物名称（可选）
    
    Returns:
        包含意图信息的字典，可能包含以下字段：
        - intent: 意图类型，如 "switch_character", "explain_relic", "ask_question"
        - character: 识别到的人物名称
        - relic: 识别到的文物名称
        - question: 提取的问题内容
    """
    from api_config import load_api_config
    import requests
    import json
    
    try:
        config = load_api_config()
        
        system_prompt = f"""你是一个历史人物伴游技能的意图识别助手，任务是分析用户输入的意图。

请按照以下步骤处理：
1. 分析用户输入，识别其意图类型
2. 提取相关信息（如人物名称、文物名称、问题内容等）
3. 以JSON格式返回结果，包含以下字段：
   - intent: 意图类型，可选值：
     * "switch_character": 召唤或切换人物
     * "explain_relic": 讲解文物（可能包含人物切换）
     * "ask_question": 询问问题（基于当前人物）
   - character: 识别到的人物名称（如果有）
   - relic: 识别到的文物名称（如果有）
   - question: 提取的问题内容（如果有）

当前激活的人物：{current_character or '无'}

示例：
用户输入："李白给我讲讲这个青铜爵"
输出：{"intent": "explain_relic", "character": "李白", "relic": "青铜爵", "question": ""}

用户输入："换个苏轼试试"
输出：{"intent": "switch_character", "character": "苏轼", "relic": "", "question": ""}

用户输入："这个是什么朝代的？"
输出：{"intent": "ask_question", "character": "", "relic": "", "question": "这个是什么朝代的？"}

用户输入："苏轼，再讲讲那个瓷器"
输出：{"intent": "explain_relic", "character": "苏轼", "relic": "瓷器", "question": ""}

请严格按照JSON格式输出，不要添加任何额外的解释或内容。"""
        
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {config['api_key']}"}
        payload = {
            "model": config['model'],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.2,
            "max_tokens": 200
        }
        
        response = requests.post(config['api_base'], headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # 提取JSON响应
        content = response.json()['choices'][0]['message']['content'].strip()
        
        # 尝试从内容中提取JSON
        # 处理可能的格式问题
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        
        # 解析JSON
        intent_data = json.loads(content)
        return intent_data
    except Exception as e:
        # 如果解析失败，返回默认意图
        return {
            "intent": "ask_question",
            "character": "",
            "relic": "",
            "question": user_input
        }


def process_intent(session, intent_data, current_persona=None):
    """处理用户意图
    
    Args:
        session: 会话管理器
        intent_data: 意图数据
        current_persona: 当前人物画像（可选）
    
    Returns:
        tuple: (是否成功, 新的人物画像)
    """
    persona = current_persona
    
    # 处理切换人物意图
    if intent_data['intent'] == 'switch_character' and intent_data['character']:
        # 先尝试解析人物ID
        char_id = session.loader._resolve_character_name(intent_data['character'])
        
        # 如果解析失败，直接使用输入作为人物名称尝试切换
        if not char_id:
            if not session.switch_character(intent_data['character']):
                print(f"❌ 人物切换失败：{intent_data['character']}")
                return False, persona
        else:
            if not session.switch_character(char_id):
                print(f"❌ 人物切换失败：{intent_data['character']}")
                return False, persona
        
        persona = session.current_persona
        print(f"\n🎭 已切换到：{persona['name']}（{persona['title']}）")
        print(f"   {persona.get('greeting', '')}")
        
        # 如果同时提到了文物，更新文物信息并讲解
        if intent_data['relic']:
            session.update_relic(intent_data['relic'])
            
            # 生成讲解
            print(f"\n🤖 {persona['name']} > ", end="", flush=True)
            system_prompt = build_system_prompt(persona, session.current_relic, mode="explanation")
            try:
                response = call_llm(system_prompt, f"请讲解{intent_data['relic']}")
                print(response)
            except Exception as e:
                print(f"❌ 讲解失败：{e}")
        
        return True, persona
    
    # 处理讲解文物意图
    elif intent_data['intent'] == 'explain_relic':
        # 如果指定了不同的人物，先切换人物
        if intent_data['character'] and persona and intent_data['character'] != persona['name']:
            # 先尝试解析人物ID
            char_id = session.loader._resolve_character_name(intent_data['character'])
            
            # 如果解析失败，直接使用输入作为人物名称尝试切换
            if not char_id:
                if not session.switch_character(intent_data['character']):
                    print(f"❌ 人物切换失败：{intent_data['character']}")
                    return False, persona
            else:
                if not session.switch_character(char_id):
                    print(f"❌ 人物切换失败：{intent_data['character']}")
                    return False, persona
            
            persona = session.current_persona
            print(f"\n🎭 已切换到：{persona['name']}（{persona['title']}）")
            print(f"   {persona.get('greeting', '')}")
        
        # 如果没有当前人物，需要先激活人物
        if not persona:
            if intent_data['character']:
                # 先尝试解析人物ID
                char_id = session.loader._resolve_character_name(intent_data['character'])
                
                # 如果解析失败，直接使用输入作为人物名称尝试激活
                if not char_id:
                    # 尝试切换人物（会自动生成）
                    if not session.switch_character(intent_data['character']):
                        print(f"❌ 未能激活人物：{intent_data['character']}")
                        return False, persona
                else:
                    if not session.activate_character(char_id):
                        # 如果激活失败，尝试切换人物（会自动生成）
                        if not session.switch_character(intent_data['character']):
                            print(f"❌ 未能激活人物：{intent_data['character']}")
                            return False, persona
                
                persona = session.current_persona
                print(f"\n🎭 {persona['name']}（{persona['title']}）")
                print(f"   {persona.get('greeting', '')}")
                print()
            else:
                print("❌ 请先召唤一位历史人物（如'李白给我讲讲这个青铜爵'）")
                return False, persona
        
        # 更新文物信息
        if intent_data['relic']:
            session.update_relic(intent_data['relic'])
            
            # 生成讲解
            print(f"\n🤖 {persona['name']} > ", end="", flush=True)
            system_prompt = build_system_prompt(persona, session.current_relic, mode="explanation")
            try:
                response = call_llm(system_prompt, f"请讲解{intent_data['relic']}")
                print(response)
            except Exception as e:
                print(f"❌ 讲解失败：{e}")
        else:
            # 没有文物信息，使用当前文物
            if session.current_relic:
                print(f"\n🤖 {persona['name']} > ", end="", flush=True)
                system_prompt = build_system_prompt(persona, session.current_relic, mode="explanation")
                try:
                    response = call_llm(system_prompt, f"请讲解{session.current_relic}")
                    print(response)
                except Exception as e:
                    print(f"❌ 讲解失败：{e}")
            else:
                print("❌ 请指定要讲解的文物。")
        
        return True, persona
    
    # 处理询问问题意图
    elif intent_data['intent'] == 'ask_question' and persona:
        # 基于当前人物回答问题
        print(f"\n🤖 {persona['name']} > ", end="", flush=True)
        system_prompt = build_system_prompt(persona, session.current_relic, mode="dialogue")
        try:
            response = call_llm(system_prompt, intent_data['question'])
            print(response)
        except Exception as e:
            print(f"❌ 对话失败：{e}")
        
        return True, persona
    
    # 其他情况
    else:
        if not persona:
            print("❌ 请先召唤一位历史人物（如'李白给我讲讲这个青铜爵'）")
        return False, persona


def handle_interactive_session():
    """处理交互式会话"""
    session = create_session_manager()
    persona = None
    
    print("=" * 50)
    print("🏛️  历史人物伴游 - 交互式会话")
    print("=" * 50)
    print("使用方法：")
    print("  • 召唤人物：'李白给我讲讲这个青铜爵'")
    print("  • 继续对话：'这件是什么朝代的？'、'再讲讲那个'")
    print("  • 切换人物：'换个苏轼试试'、'召唤孔子'")
    print("  • 退出会话：'exit' 或 'quit'")
    print("=" * 50)
    print()
    
    # 主对话循环
    while True:
        print("👤 你 > ", end="")
        user_input = input().strip()
        if not user_input:
            continue
        
        if user_input.lower() in ['exit', 'quit', 'q', '再见']:
            if persona:
                print(f"👋 {persona.get('farewell', '后会有期！')}")
            else:
                print("👋 再见！")
            break
        
        # 分析用户输入的意图
        current_char = persona['name'] if persona else None
        intent_data = analyze_user_intent(user_input, current_char)
        
        # 处理意图
        success, persona = process_intent(session, intent_data, persona)
        
        # 如果是首次输入且未成功，继续循环
        if not success and not persona:
            print()
            continue


def main():
    args = parse_args()
    
    if args.mode == 'interactive':
        handle_interactive_session()
        return
    
    # 单次调用模式（保留但主要使用交互式会话）
    loader = CharacterLoader()
    persona = loader.load_character(args.character)
    
    if not persona:
        print(f"❌ 库中未找到历史人物: {args.character}")
        print(f"可用人物: {', '.join(loader.list_characters())}")
        
        print(f"\n🔄 正在为「{args.character}」生成画像...")
        script_dir = Path(__file__).parent
        result = subprocess.run(
            [sys.executable, str(script_dir / "persona_generator.py"), args.character],
            capture_output=False
        )
        if result.returncode != 0:
            sys.exit(result.returncode)
        
        loader = CharacterLoader()
        persona = loader.load_character(args.character)
        if not persona:
            print("❌ 画像生成后仍无法加载，流程终止。")
            sys.exit(1)
    
    print(f"🎭 召唤历史人物: {persona['name']} ({persona['title']})")
    print("=" * 50)
    
    presenter = RelicPresenter(persona)
    
    if args.mode == 'greeting':
        print(presenter.get_greeting())
    elif args.mode == 'intro':
        print(presenter.get_self_introduction())
    else:
        explanation = presenter.explain_relic(args.relic)
        print(explanation)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
警察执法资格考试助手 - 入口脚本
基于《公安机关人民警察执法资格等级考试大纲》（2026年版）附历年真题
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# 动态导入模块
import importlib.util

def import_module_from_file(filepath, module_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 导入pqebot-core
pqebot_core_path = os.path.join(os.path.dirname(__file__), 'scripts', 'pqebot-core.py')
pqebot_module = import_module_from_file(pqebot_core_path, 'pqebot_core')
PQEBotCore = pqebot_module.PQEBotCore

def main():
    """主入口函数"""
    bot = PQEBotCore()
    bot.reset_session()
    
    print("=" * 60)
    print("🎓 警察执法资格考试助手")
    print("=" * 60)
    print("基于《公安机关人民警察执法资格等级考试大纲》（2026年版）")
    print("数据来源：网络整理")
    print("=" * 60)
    
    # 启动交互流程
    while True:
        print("\n" + "=" * 60)
        print("📋 主菜单")
        print("=" * 60)
        print("1. 开始学习（选择考试级别）")
        print("2. 查看考试大纲")
        print("3. 查看历年真题统计")
        print("4. 查看高频考点")
        print("5. 退出")
        print("=" * 60)
        
        choice = input("请选择 (1-5): ").strip()
        
        if choice == '1':
            start_learning(bot)
        elif choice == '2':
            show_exam_outline(bot)
        elif choice == '3':
            show_past_papers_summary(bot)
        elif choice == '4':
            show_high_frequency_points(bot)
        elif choice == '5':
            print("\n👋 感谢使用警察执法资格考试助手，祝您考试顺利！")
            break
        else:
            print("❌ 无效选择，请重新输入")

def start_learning(bot):
    """开始学习流程"""
    print("\n" + "=" * 60)
    print("🎓 选择考试级别")
    print("=" * 60)
    print(bot.get_exam_levels_menu())
    
    while True:
        level_choice = input("请选择考试级别 (1-2): ").strip()
        success, message = bot.set_exam_level(level_choice)
        print(message)
        if success:
            break
    
    # 选择学习模式
    print("\n" + "=" * 60)
    print("📚 选择学习模式")
    print("=" * 60)
    print(bot.get_learning_modes_menu())
    
    while True:
        mode_choice = input("请选择学习模式 (1-3): ").strip()
        success, message = bot.set_learning_mode(mode_choice)
        print(message)
        if success:
            break
    
    # 显示当前设置
    print("\n" + "=" * 60)
    print("✅ 学习设置完成")
    print("=" * 60)
    print(bot.get_current_session_info())
    
    # 根据选择执行不同操作
    mode = bot.user_session.get('mode')
    if mode == 'past_papers':
        show_past_papers(bot)
    elif mode == 'practice':
        select_subject_and_practice(bot)
    elif mode == 'simulation':
        start_simulation_test(bot)

def show_exam_outline(bot):
    """显示考试大纲"""
    print("\n" + "=" * 60)
    print("📋 2026年考试大纲")
    print("=" * 60)
    print(bot.get_exam_outline_summary())

def show_past_papers_summary(bot):
    """显示历年真题统计"""
    print("\n" + "=" * 60)
    print("📚 历年真题库（2021-2025年）")
    print("=" * 60)
    print(bot.get_past_papers_summary())

def show_high_frequency_points(bot):
    """显示高频考点"""
    print("\n" + "=" * 60)
    print("🔝 高频考点TOP 8（基于5年真题统计）")
    print("=" * 60)
    points = bot.get_high_frequency_points(8)
    for i, point in enumerate(points, 1):
        freq_percent = point['frequency'] * 100
        years = point.get('appears_in_years', [])
        years_str = f"（{', '.join(map(str, years))}年）" if years else ""
        description = point.get('description', '')
        print(f"{i}. {point['topic']} {years_str}")
        print(f"   出现频率：{freq_percent:.0f}%")
        if description:
            print(f"   描述：{description}")
        print()

def show_past_papers(bot):
    """显示历年真题"""
    print("\n" + "=" * 60)
    print("📝 历年真题")
    print("=" * 60)
    print("请选择年份：")
    print("1. 2025年真题")
    print("2. 2024年真题")
    print("3. 2023年真题")
    print("4. 2022年真题")
    print("5. 2021年真题")
    print("0. 返回主菜单")
    
    year_choice = input("请选择 (0-5): ").strip()
    
    year_map = {'1': 2025, '2': 2024, '3': 2023, '4': 2022, '5': 2021}
    if year_choice in year_map:
        year = year_map[year_choice]
        show_year_papers(bot, year)
    elif year_choice == '0':
        return

def show_year_papers(bot, year):
    """显示指定年份的真题"""
    questions = bot.get_sample_questions(year, 5)
    if not questions:
        print(f"\n📭 未找到{year}年的真题示例")
        return
    
    print(f"\n📅 {year}年公安机关人民警察执法资格等级考试（初级）真题示例")
    print("=" * 60)
    
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. [{q.get('type', '题目')}] {q.get('question', '')}")
        if 'options' in q:
            for opt in q['options']:
                print(f"   {opt}")
        if 'correct_answer' in q:
            print(f"   ✅ 正确答案：{q['correct_answer']}")
        if 'explanation' in q:
            print(f"   📝 解析：{q['explanation']}")
        if 'law_reference' in q:
            print(f"   📚 法律依据：{q['law_reference']}")

def select_subject_and_practice(bot):
    """选择科目并进行练习"""
    print("\n" + "=" * 60)
    print("📚 选择练习科目")
    print("=" * 60)
    print(bot.get_subject_selection_menu())
    
    while True:
        subject_choice = input("请选择科目: ").strip()
        success, message = bot.set_subject(subject_choice)
        print(message)
        if success:
            if subject_choice == '0':
                return
            else:
                start_practice(bot)
                break

def start_practice(bot):
    """开始模块练习"""
    subject_name = bot.get_subject_name(bot.user_session['subject'])
    print(f"\n🎯 开始 {subject_name} 模块练习")
    print("=" * 60)
    print("功能开发中...")
    print("将提供选择题、判断题、案例分析题等练习")

def start_simulation_test(bot):
    """开始模拟测试"""
    print("\n⏰ 开始模拟测试")
    print("=" * 60)
    print("功能开发中...")
    print("将提供全真模拟考试环境")

if __name__ == "__main__":
    main()
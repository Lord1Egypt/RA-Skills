#!/usr/bin/env python3
import random
import sys
import os

SECRET_FILE = os.path.join(os.path.dirname(__file__), 'secret.txt')
STEP_FILE = os.path.join(os.path.dirname(__file__), 'step.txt')

def generate_secret():
    """生成4位不重复的随机数字字符串"""
    return ''.join(random.sample('0123456789', 4))

def save_secret(secret):
    """将秘密数字写入文件"""
    with open(SECRET_FILE, 'w', encoding='utf-8') as f:
        f.write(secret)
    # 初始化步数
    with open(STEP_FILE, 'w', encoding='utf-8') as f:
        f.write('0')

def load_secret():
    """从文件读取秘密数字"""
    if not os.path.exists(SECRET_FILE):
        return None
    with open(SECRET_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_step():
    """读取当前步数"""
    if not os.path.exists(STEP_FILE):
        return 0
    with open(STEP_FILE, 'r', encoding='utf-8') as f:
        return int(f.read().strip())

def save_step(step):
    """保存当前步数"""
    with open(STEP_FILE, 'w', encoding='utf-8') as f:
        f.write(str(step))

def validate_input(input_str):
    """校验用户输入是否合法，返回(是否合法, 错误信息)"""
    if len(input_str) != 4:
        return False, "请输入4位数字，请重新输入"
    if not input_str.isdigit():
        return False, "只能输入数字，请重新输入"
    if len(set(input_str)) != 4:
        return False, "数字不能重复，请重新输入"
    return True, ""

def calculate_correct_positions(guess, secret):
    """计算位置和数字都正确的个数"""
    count = 0
    for g, s in zip(guess, secret):
        if g == s:
            count +=1
    return count

def start_new_game():
    """开始新游戏，生成秘密并保存到文件"""
    secret = generate_secret()
    save_secret(secret)
    print("我已想好一个四位数（各位数字互不相同），请开始猜测！")

def verify_guess(guess):
    """验证用户猜测，返回反馈结果"""
    secret = load_secret()
    if not secret:
        print("请先开始游戏！输入「开始游戏」启动新局。")
        return
    
    valid, err_msg = validate_input(guess)
    if not valid:
        print(err_msg)
        return
    
    step = load_step() + 1
    save_step(step)
    
    correct = calculate_correct_positions(guess, secret)
    
    if correct ==4:
        print(f"反馈：{correct} 个数字位置正确！恭喜你猜对了！总共用了 {step} 步。")
        # 清理临时文件
        if os.path.exists(SECRET_FILE):
            os.remove(SECRET_FILE)
        if os.path.exists(STEP_FILE):
            os.remove(STEP_FILE)
    else:
        print(f"反馈：{correct} 个数字位置正确")

def main():
    if len(sys.argv) == 1:
        # 无参数运行：默认交互式模式
        start_new_game()
        while True:
            try:
                guess = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n游戏结束，再见！")
                # 清理临时文件
                if os.path.exists(SECRET_FILE):
                    os.remove(SECRET_FILE)
                if os.path.exists(STEP_FILE):
                    os.remove(STEP_FILE)
                sys.exit(0)
            verify_guess(guess)
    elif len(sys.argv) == 2 and sys.argv[1] == '--generate':
        # 生成模式：仅生成秘密并保存
        start_new_game()
    elif len(sys.argv) == 3 and sys.argv[1] == '--verify':
        # 验证模式：验证用户猜测
        verify_guess(sys.argv[2])
    else:
        print("使用方法：")
        print("  python guess_number.py              # 交互式模式")
        print("  python guess_number.py --generate   # 生成新秘密，开始新游戏")
        print("  python guess_number.py --verify <猜测数字>  # 验证猜测")

if __name__ == "__main__":
    main()

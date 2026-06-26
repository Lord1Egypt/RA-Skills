#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈萨克文转换工具
将哈萨克文在西里尔文和阿拉伯文之间转换
"""

import re
import argparse
import os

# 西里尔文到阿拉伯文的映射表
cyrillic_to_arabic_map = {
    # 符合字映射表
    'ю': 'يۋ', 'ё': 'يو', 'щ': 'شش', 'ц': 'تس', 'я': 'يا', 'ә': 'ءا', 'і': 'ءى', 'ү': 'ءۇ', 'ө': 'ءو',
    # 基本字符映射
    'й': 'ي', 'у': 'ۋ', 'к': 'ك', 'е': 'ە', 'н': 'ن', 'г': 'گ', 'ш': 'ش', 'з': 'ز',
    'х': 'ح', 'ф': 'ف', 'ы': 'ى', 'в': 'ۆ', 'а': 'ا', 'п': 'پ', 'р': 'ر', 'о': 'و',
    'л': 'ل', 'д': 'د', 'ж': 'ج', 'э': 'ە', 'ч': 'چ', 'с': 'س', 'м': 'م', 'и': 'ي', 'т': 'ت',
    'ь': '', 'б': 'ب', 'ң': 'ڭ', 'ғ': 'ع', 'ұ': 'ۇ', 'қ': 'ق', 'һ': 'ھ',
    # 特殊字符映射
    ';': '؛', ',': '،', '?': '؟',
}

# 创建阿拉伯文到西里尔文的反向映射表
arabic_to_cyrillic_map = {}
for cyrillic, arabic in cyrillic_to_arabic_map.items():
    if arabic:
        arabic_to_cyrillic_map[arabic] = cyrillic

# 按长度排序，优先匹配较长的字符
arabic_chars_sorted = sorted(arabic_to_cyrillic_map.keys(), key=len, reverse=True)

# 用户词库
def load_user_dict(dict_path):
    """加载用户词库"""
    user_dict = {'arabic': {}, 'cyrillic': {}}
    
    if not os.path.exists(dict_path):
        return user_dict
    
    current_section = None
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
            if current_section and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if current_section in user_dict:
                    user_dict[current_section][key] = value
    
    return user_dict

# 应用用户词库修正
def apply_user_dict(text, mode, user_dict):
    """应用用户词库修正"""
    if not text:
        return text
    
    # 根据模式选择对应的词库
    # arabic模式（阿拉伯文转西里尔文）：使用cyrillic词库修正西里尔文
    # cyrillic模式（西里尔文转阿拉伯文）：使用arabic词库修正阿拉伯文
    dict_section = 'arabic' if mode == 'cyrillic' else 'cyrillic'
    dict_items = user_dict.get(dict_section, {})
    
    # 按照长度排序，优先替换较长的词语
    words = sorted(dict_items.keys(), key=len, reverse=True)
    
    result = text
    
    for word in words:
        replacement = dict_items[word]
        # 使用正则表达式进行全局替换
        escaped_word = re.escape(word)
        regex = re.compile(escaped_word, re.UNICODE)
        result = regex.sub(replacement, result)
    
    return result

# 西里尔文语法处理
def cyrillic_grammar(text):
    """西里尔文语法处理"""
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        words = line.split()
        processed_words = []
        
        for word in words:
            if 'к' in word or 'г' in word or 'э' in word or 'ء' in word:
                new_word = []
                for char in word:
                    if char == 'а':
                        new_word.append('ә')
                    elif char == 'о':
                        new_word.append('ө')
                    elif char == 'ұ':
                        new_word.append('ү')
                    elif char == 'ы':
                        new_word.append('і')
                    else:
                        new_word.append(char)
                word = ''.join(new_word)
            
            word = word.replace('ء', '')
            word = word.replace('Ь', '')
            processed_words.append(word)
        
        processed_lines.append(' '.join(processed_words))
    
    return '\n'.join(processed_lines)

# 阿拉伯文语法处理
def arabic_grammar(text):
    """阿拉伯文语法处理"""
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        words = line.split()
        processed_words = []
        
        for word in words:
            if 'ء' in word:
                if 'ك' in word or 'گ' in word or 'ە' in word:
                    word = word.replace('ء', '')
                else:
                    if len(word) > 2:
                        word = 'ء' + word.replace('ء', '')
                        first_two = word[:2]
                        rest = word[2:].replace('ء', '')
                        word = first_two + rest
            
            processed_words.append(word)
        
        processed_lines.append(' '.join(processed_words))
    
    return '\n'.join(processed_lines)

# 西里尔文转阿拉伯文
def convert_cyrillic_to_arabic(text):
    """西里尔文转阿拉伯文"""
    if not isinstance(text, str):
        return text
    
    text = text.lower()
    result = ''
    
    for char in text:
        if char in cyrillic_to_arabic_map:
            result += cyrillic_to_arabic_map[char]
        else:
            result += char
    
    return result

# 阿拉伯文转西里尔文
def convert_arabic_to_cyrillic(text):
    """阿拉伯文转西里尔文"""
    if not isinstance(text, str):
        return text
    
    result = text
    
    for arabic_char in arabic_chars_sorted:
        if arabic_char in result:
            cyrillic_char = arabic_to_cyrillic_map[arabic_char]
            result = result.replace(arabic_char, cyrillic_char)
    
    return result

# 根据模式转换文本
def convert_text(text, mode, user_dict):
    """根据模式转换文本"""
    if mode == 'cyrillic':
        result = convert_cyrillic_to_arabic(text)
        result = arabic_grammar(result)
        # 应用用户词库修正
        result = apply_user_dict(result, mode, user_dict)
        return result
    else:
        result = convert_arabic_to_cyrillic(text)
        result = cyrillic_grammar(result)
        # 应用用户词库修正
        result = apply_user_dict(result, mode, user_dict)
        return result

def save_user_dict(user_dict, dict_path):
    """保存用户词库到文件"""
    with open(dict_path, 'w', encoding='utf-8') as f:
        # 保存阿拉伯文词库
        f.write('[arabic]\n')
        for key, value in user_dict.get('arabic', {}).items():
            f.write(f'{key} = {value}\n')
        f.write('\n')
        
        # 保存西里尔文词库
        f.write('[cyrillic]\n')
        for key, value in user_dict.get('cyrillic', {}).items():
            f.write(f'{key} = {value}\n')

def manage_user_dict(action, dict_path, section, key=None, value=None):
    """管理用户词库"""
    # 确保在Windows环境下正确输出Unicode字符
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    
    user_dict = load_user_dict(dict_path)
    
    if action == 'add':
        if not key or not value:
            print('错误：添加词条时需要指定 key 和 value')
            return False
        if section not in user_dict:
            print(f'错误：无效的词库部分: {section}')
            return False
        user_dict[section][key] = value
        save_user_dict(user_dict, dict_path)
        print(f'成功添加词条: {key} = {value} 到 {section} 部分')
        return True
    
    elif action == 'delete':
        if not key:
            print('错误：删除词条时需要指定 key')
            return False
        if section not in user_dict:
            print(f'错误：无效的词库部分: {section}')
            return False
        if key in user_dict[section]:
            del user_dict[section][key]
            save_user_dict(user_dict, dict_path)
            print(f'成功删除词条: {key} 从 {section} 部分')
            return True
        else:
            print(f'错误：词条 {key} 在 {section} 部分中不存在')
            return False
    
    elif action == 'list':
        if section not in user_dict:
            print(f'错误：无效的词库部分: {section}')
            return False
        print(f'{section} 部分的词条:')
        for key, value in user_dict[section].items():
            print(f'  {key} = {value}')
        return True
    
    else:
        print(f'错误：无效的操作: {action}')
        return False

def main():
    """主函数"""
    import sys
    
    # 检查是否是1.0版本的用法
    if len(sys.argv) >= 3 and sys.argv[1] in ['A', 'C']:
        # 1.0版本兼容模式
        mode_arg = sys.argv[1]
        text = ' '.join(sys.argv[2:])
        
        # 加载用户词库
        user_dict = load_user_dict('user.dic')
        
        # 转换模式映射
        mode_map = {'A': 'cyrillic', 'C': 'arabic'}
        mode = mode_map[mode_arg]
        
        # 执行转换
        result = convert_text(text, mode, user_dict)
        
        # 输出结果
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
        print(result)
        return
    
    # 2.0版本命令解析
    parser = argparse.ArgumentParser(description='哈萨克文转换工具')
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 转换命令
    convert_parser = subparsers.add_parser('convert', help='转换文本')
    convert_parser.add_argument('--mode', choices=['cyrillic', 'arabic'], required=True,
                              help='转换模式: cyrillic (西里尔文转阿拉伯文), arabic (阿拉伯文转西里尔文)')
    convert_parser.add_argument('--input', '-i', help='输入文件路径')
    convert_parser.add_argument('--output', '-o', help='输出文件路径')
    convert_parser.add_argument('--text', '-t', help='直接输入文本')
    convert_parser.add_argument('--dict', '-d', default='user.dic', help='用户词库文件路径 (默认: user.dic)')
    
    # 词库管理命令
    dict_parser = subparsers.add_parser('dict', help='管理用户词库')
    dict_parser.add_argument('action', choices=['add', 'delete', 'list'], help='词库操作')
    dict_parser.add_argument('--section', '-s', choices=['arabic', 'cyrillic'], required=True, help='词库部分')
    dict_parser.add_argument('--key', '-k', help='词条键')
    dict_parser.add_argument('--value', '-v', help='词条值')
    dict_parser.add_argument('--dict', '-d', default='user.dic', help='用户词库文件路径 (默认: user.dic)')
    
    args = parser.parse_args()
    
    # 处理2.0版本命令
    if args.command == 'convert':
        # 加载用户词库
        user_dict = load_user_dict(args.dict)
        
        # 读取输入
        if args.input:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            # 从标准输入读取
            text = sys.stdin.read()
        
        # 执行转换
        result = convert_text(text, args.mode, user_dict)
        
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
        else:
            # 确保在Windows环境下正确输出Unicode字符
            if sys.stdout.encoding != 'utf-8':
                sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
            print(result)
    
    elif args.command == 'dict':
        # 执行词库管理操作
        manage_user_dict(args.action, args.dict, args.section, args.key, args.value)

if __name__ == '__main__':
    main()

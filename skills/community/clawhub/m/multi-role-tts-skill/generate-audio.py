#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='多角色音频生成器')
    parser.add_argument('-i', '--input', default='examples/basic-dialogue.txt',
                       help='输入脚本文件路径 (默认: examples/basic-dialogue.txt)')
    parser.add_argument('-o', '--output', default='output.mp3',
                       help='输出音频文件路径 (默认: output.mp3)')
    parser.add_argument('--role-a-voice', default='zh-CN-XiaoxiaoNeural',
                       help='角色A的语音 (默认: zh-CN-XiaoxiaoNeural)')
    parser.add_argument('--role-b-voice', default='zh-CN-XiaoyiNeural',
                       help='角色B的语音 (默认: zh-CN-XiaoyiNeural)')
    parser.add_argument('--narrator-voice', default='zh-CN-YunxiaNeural',
                       help='旁白的语音 (默认: zh-CN-YunxiaNeural)')
    parser.add_argument('--role-a-rate', default='+10%',
                       help='角色A的语速 (默认: +10%)')
    parser.add_argument('--role-b-rate', default='+15%',
                       help='角色B的语速 (默认: +15%)')
    parser.add_argument('--narrator-rate', default='+0%',
                       help='旁白的语速 (默认: +0%)')
    parser.add_argument('--keep-temp', action='store_true',
                       help='保留临时文件')
    
    return parser.parse_args()

def extract_roles_from_script(script_path):
    """从脚本文件中提取不同角色的对话"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{script_path}'")
        print("请使用 -i 参数指定正确的脚本文件路径")
        sys.exit(1)
    
    # 初始化角色列表
    role_a_lines = []
    role_b_lines = []
    narrator_lines = []
    
    # 常见的角色标识符
    role_a_prefixes = ['角色A:', 'RoleA:', '顾问A:', '花花:', 'A:']
    role_b_prefixes = ['角色B:', 'RoleB:', '顾问B:', '小霞:', 'B:']
    narrator_prefixes = ['旁白:', 'Narrator:', '记录员:', '观察者:', '旁白:', 'Narrator:']
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # 检查角色A
        for prefix in role_a_prefixes:
            if line.startswith(prefix):
                role_a_lines.append(line[len(prefix):].strip())
                break
        else:
            # 检查角色B
            for prefix in role_b_prefixes:
                if line.startswith(prefix):
                    role_b_lines.append(line[len(prefix):].strip())
                    break
            else:
                # 检查旁白
                for prefix in narrator_prefixes:
                    if line.startswith(prefix):
                        narrator_lines.append(line[len(prefix):].strip())
                        break
                else:
                    # 如果没有匹配的角色前缀，跳过这一行
                    continue
    
    return role_a_lines, role_b_lines, narrator_lines

def generate_single_audio(text, voice, rate, output_file):
    """生成单个音频文件"""
    print(f"生成音频: {output_file}")
    result = subprocess.run([
        'edge-tts', '--text', text, '--voice', voice,
        '--rate', rate, '--write-media', output_file
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"生成音频失败: {output_file}")
        print(f"错误: {result.stderr}")
        return False
    return True

def merge_audio_files(audio_files, output_file, keep_temp=False):
    """合并多个音频文件"""
    if len(audio_files) == 0:
        print("错误: 没有音频文件可合并")
        return False
    
    if len(audio_files) == 1:
        # 只有一个文件，直接重命名
        os.rename(audio_files[0], output_file)
        print(f"音频生成完成: {output_file}")
        return True
    
    # 创建合并列表
    merge_list = 'merge_list.txt'
    try:
        with open(merge_list, 'w') as f:
            for audio in audio_files:
                f.write(f"file '{audio}'\n")
        
        # 使用ffmpeg合并
        print("合并音频...")
        result = subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', merge_list, '-c', 'copy', output_file
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"合并音频失败")
            print(f"错误: {result.stderr}")
            return False
        
        print(f"音频生成完成: {output_file}")
        
        # 清理临时文件
        if not keep_temp:
            for audio in audio_files:
                if os.path.exists(audio):
                    os.remove(audio)
            if os.path.exists(merge_list):
                os.remove(merge_list)
        
        return True
        
    except Exception as e:
        print(f"合并音频时出错: {e}")
        return False

def main():
    args = parse_arguments()
    
    print("=" * 50)
    print("多角色音频生成器")
    print("=" * 50)
    print(f"输入文件: {args.input}")
    print(f"输出文件: {args.output}")
    print(f"角色A语音: {args.role_a_voice}")
    print(f"角色B语音: {args.role_b_voice}")
    print(f"旁白语音: {args.narrator_voice}")
    print("-" * 50)
    
    # 提取角色对话
    role_a_lines, role_b_lines, narrator_lines = extract_roles_from_script(args.input)
    
    print(f"角色A: {len(role_a_lines)}行")
    print(f"角色B: {len(role_b_lines)}行")
    print(f"旁白: {len(narrator_lines)}行")
    
    if len(role_a_lines) == 0 and len(role_b_lines) == 0 and len(narrator_lines) == 0:
        print("错误: 脚本中没有找到有效的对话内容")
        print("请确保脚本文件包含角色标识符，如 '角色A:', '角色B:', '旁白:' 等")
        sys.exit(1)
    
    # 生成单个音频
    audio_files = []
    
    # 角色A的音频
    if role_a_lines:
        role_a_text = ' '.join(role_a_lines)
        role_a_file = 'role_a_temp.mp3'
        if generate_single_audio(role_a_text, args.role_a_voice, args.role_a_rate, role_a_file):
            audio_files.append(role_a_file)
    
    # 角色B的音频
    if role_b_lines:
        role_b_text = ' '.join(role_b_lines)
        role_b_file = 'role_b_temp.mp3'
        if generate_single_audio(role_b_text, args.role_b_voice, args.role_b_rate, role_b_file):
            audio_files.append(role_b_file)
    
    # 旁白的音频
    if narrator_lines:
        narrator_text = ' '.join(narrator_lines)
        narrator_file = 'narrator_temp.mp3'
        if generate_single_audio(narrator_text, args.narrator_voice, args.narrator_rate, narrator_file):
            audio_files.append(narrator_file)
    
    # 合并音频
    if merge_audio_files(audio_files, args.output, args.keep_temp):
        # 检查输出文件
        if os.path.exists(args.output):
            size = os.path.getsize(args.output)
            print(f"文件大小: {size} 字节 ({size/1024:.1f} KB)")
            print("=" * 50)
            print("音频生成成功!")
            return True
        else:
            print("错误: 输出文件未生成")
            return False
    else:
        print("错误: 音频生成失败")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
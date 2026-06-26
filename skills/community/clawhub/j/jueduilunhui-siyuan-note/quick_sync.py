#!/usr/bin/env python3
"""
快速同步脚本
用于在OpenClaw中快速同步当前对话到思源笔记
"""

import sys
import json
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note import SiYuanNote

def sync_current_conversation(conversation_text=None, summary=None):
    """
    同步当前对话到思源笔记
    
    Args:
        conversation_text: 对话文本（可选）
        summary: 对话摘要（可选）
    """
    print("🔄 开始同步对话到思源笔记...")
    
    # 创建思源笔记实例
    siyuan = SiYuanNote()
    
    # 测试连接
    if not siyuan.test_connection():
        print("❌ 无法连接到思源笔记，请检查配置")
        return False
    
    # 创建对话数据
    if conversation_text:
        # 如果有提供对话文本，使用它
        conversation_data = {
            'summary': summary or 'OpenClaw对话记录',
            'messages': [
                {
                    'role': 'user',
                    'content': '对话内容'
                },
                {
                    'role': 'assistant',
                    'content': conversation_text
                }
            ],
            'conclusion': '对话已同步到思源笔记',
            'metadata': {
                'synced_at': datetime.now().isoformat(),
                'source': 'OpenClaw快速同步'
            }
        }
    else:
        # 默认示例对话
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversation_data = {
            'summary': f'OpenClaw快速同步 - {current_time}',
            'messages': [
                {
                    'role': 'user',
                    'content': f'快速同步测试，时间: {current_time}'
                },
                {
                    'role': 'assistant',
                    'content': f'思源笔记快速同步功能测试！\n\n**同步信息:**\n- 时间: {current_time}\n- 笔记本: 其他\n- 文档: openchat\n- 状态: 同步中...'
                }
            ],
            'conclusion': f'快速同步测试完成于 {current_time}',
            'metadata': {
                'synced_at': datetime.now().isoformat(),
                'test_type': '快速同步'
            }
        }
    
    # 同步对话
    success = siyuan.sync_conversation(conversation_data)
    
    if success:
        print("✅ 对话同步成功！")
        print(f"位置: 思源笔记 -> {siyuan.sync_config.notebook_name} -> {siyuan.sync_config.document_name}")
        return True
    else:
        print("❌ 对话同步失败")
        return False

def sync_from_stdin():
    """从标准输入读取对话并同步"""
    print("📝 请输入对话内容（Ctrl+D结束输入）:")
    
    try:
        # 读取所有输入
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        conversation_text = "\n".join(lines)
        
        if not conversation_text.strip():
            print("⚠️  输入为空，使用示例对话")
            return sync_current_conversation()
        
        summary = input("请输入对话摘要（可选，直接回车跳过）: ").strip()
        
        return sync_current_conversation(conversation_text, summary)
        
    except KeyboardInterrupt:
        print("\n❌ 用户取消")
        return False

def sync_from_args():
    """从命令行参数同步"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  1. python quick_sync.py '对话内容'")
        print("  2. python quick_sync.py --file 文件名")
        print("  3. python quick_sync.py --stdin")
        print("  4. python quick_sync.py --test")
        return False
    
    if sys.argv[1] == "--stdin":
        return sync_from_stdin()
    
    elif sys.argv[1] == "--test":
        print("🧪 运行测试同步...")
        return sync_current_conversation()
    
    elif sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("❌ 请提供文件名")
            return False
        
        filename = sys.argv[2]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                conversation_text = f.read()
            
            summary = input("请输入对话摘要（可选，直接回车跳过）: ").strip()
            
            return sync_current_conversation(conversation_text, summary)
            
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return False
    
    else:
        # 第一个参数作为对话内容
        conversation_text = sys.argv[1]
        
        summary = None
        if len(sys.argv) > 2:
            summary = sys.argv[2]
        
        return sync_current_conversation(conversation_text, summary)

def main():
    """主函数"""
    print("=" * 60)
    print("思源笔记快速同步工具")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        success = sync_from_args()
    else:
        # 交互模式
        print("\n请选择同步方式:")
        print("  1. 使用示例对话测试")
        print("  2. 输入对话内容")
        print("  3. 从文件读取")
        print("  4. 退出")
        
        try:
            choice = input("\n请输入选择 (1-4): ").strip()
            
            if choice == "1":
                success = sync_current_conversation()
            elif choice == "2":
                success = sync_from_stdin()
            elif choice == "3":
                filename = input("请输入文件名: ").strip()
                if not filename:
                    print("❌ 文件名不能为空")
                    return
                
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        conversation_text = f.read()
                    
                    summary = input("请输入对话摘要（可选，直接回车跳过）: ").strip()
                    
                    success = sync_current_conversation(conversation_text, summary)
                    
                except Exception as e:
                    print(f"❌ 读取文件失败: {e}")
                    success = False
            elif choice == "4":
                print("👋 退出")
                return
            else:
                print("❌ 无效选择")
                success = False
                
        except KeyboardInterrupt:
            print("\n👋 用户取消")
            return
    
    # 输出结果
    print("\n" + "=" * 60)
    if success:
        print("🎉 同步完成！")
    else:
        print("❌ 同步失败")
    print("=" * 60)

if __name__ == "__main__":
    main()
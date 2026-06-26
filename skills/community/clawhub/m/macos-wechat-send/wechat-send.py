#!/usr/bin/env python3
"""
微信自动发送消息脚本
使用 AppleScript 控制微信 Mac 版
通过剪贴板复制粘贴，避免输入法影响

支持：
- 文字消息
- 文件发送（通过 Finder 复制粘贴）
"""

import subprocess
import sys
import os
import time

STATE_FILE = os.path.expanduser('~/.openclaw/workspace/skills/wechat-send/.last_contact')

def get_last_contact():
    """读取上一次发送的联系人"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return f.read().strip()
    except:
        pass
    return None

def save_last_contact(contact_name):
    """保存当前联系人为上一次发送的联系人"""
    try:
        with open(STATE_FILE, 'w') as f:
            f.write(contact_name)
    except:
        pass

def set_clipboard(text):
    """设置剪贴板内容 - 直接用 Python 设置，避免转义问题"""
    # 使用 macOS 的 pbcopy 命令，通过 stdin 传递内容
    proc = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
    proc.stdin.write(text)
    proc.stdin.close()
    proc.wait()

def is_file_path(text):
    """检查是否是文件路径"""
    return os.path.isfile(text)

def copy_file_in_finder(file_path):
    """在 Finder 中选中文件并复制（Cmd+C）"""
    abs_path = os.path.abspath(file_path)
    
    # 使用 POSIX file 语法，更好地处理特殊字符
    script = f'''
    tell application "Finder"
        activate
        select POSIX file "{abs_path}"
        delay 0.3
        tell application "System Events"
            keystroke "c" using command down
        end tell
        delay 0.3
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True, timeout=10)
        return True
    except Exception as e:
        print(f"✗ 复制文件失败：{e}")
        return False

def activate_wechat():
    """激活微信窗口 - 使用多种方式确保成功"""
    import time
    
    # 方式 1：用 open 命令打开/激活应用
    try:
        subprocess.run(['open', '-a', 'WeChat'], check=True, timeout=5)
        time.sleep(0.3)
    except:
        pass
    
    # 方式 2：用 AppleScript activate
    try:
        subprocess.run(['osascript', '-e', 'tell application "WeChat" to activate'], check=True, timeout=5)
        time.sleep(0.3)
    except:
        pass
    
    # 方式 3：用 System Events 设置前台
    try:
        subprocess.run(['osascript', '-e', 'tell application "System Events" to set frontmost of process "WeChat" to true'], check=True, timeout=5)
        time.sleep(0.3)
    except:
        pass
    
    # 方式 4：用 NSAppleScript 强制激活（最底层）
    try:
        script = '''
        tell application "System Events"
            tell process "WeChat"
                set frontmost to true
                perform action "AXRaise" of window 1
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        time.sleep(0.3)
    except:
        pass
    
    return True

def send_wechat_message(contact_name, message, is_first=False):
    """发送微信消息（文字）
    
    is_first=True: 第一条消息，需要搜索联系人
                 - 如果是新联系人：用垫脚石确保聚焦
                 - 如果是同一联系人：直接发送
    is_first=False: 连续发送，聊天窗口已打开，直接粘贴发送
    """
    
    # 第零步：激活微信窗口
    try:
        activate_wechat()
    except Exception as e:
        print(f"✗ 激活微信失败：{e}")
        return False
    
    # 如果是第一条消息，需要搜索联系人
    if is_first:
        last_contact = get_last_contact()
        is_same_contact = (last_contact == contact_name)
        
        # 只有新联系人才需要垫脚石
        if not is_same_contact:
            print(f"ℹ️ 新联系人（上一次：{last_contact or '无'}），使用垫脚石...")
            
            # 垫脚石：先打开文件传输助手，确保输入框聚焦
            set_clipboard("文件传输助手")
            
            dummy_script = '''
            tell application "System Events"
                tell process "WeChat"
                    -- 先按 ESC 清除任何打开的窗口或搜索框
                    key code 53
                    delay 0.2
                    
                    -- 按 Cmd+F 搜索
                    keystroke "f" using command down
                    delay 0.3
                    
                    -- 粘贴"文件传输助手"
                    keystroke "v" using command down
                    delay 0.3
                    
                    -- 按回车打开文件传输助手
                    keystroke return
                    delay 0.3
                end tell
            end tell
            '''
            
            try:
                subprocess.run(['osascript', '-e', dummy_script], check=True, timeout=10)
            except Exception as e:
                print(f"✗ 垫脚石失败：{e}")
                return False
        
        # 搜索真正的目标联系人
        set_clipboard(contact_name)
        
        search_script = '''
        tell application "System Events"
            tell process "WeChat"
                -- 先按 ESC 清除任何打开的窗口或搜索框
                key code 53
                delay 0.2
                
                -- 按 Cmd+A 全选清空搜索框
                keystroke "a" using command down
                delay 0.2
                
                -- 按 Cmd+F 重新搜索
                keystroke "f" using command down
                delay 0.3
                
                -- 粘贴联系人名字
                keystroke "v" using command down
                delay 0.5
                
                -- 按回车选择第一个搜索结果
                keystroke return
                delay 0.5
            end tell
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', search_script], check=True, timeout=10)
        except Exception as e:
            print(f"✗ 搜索联系人失败：{e}")
            return False
        
        if is_same_contact:
            print(f"ℹ️ 同一联系人（{contact_name}），窗口应已打开...")
        else:
            print(f"✓ 已切换到新联系人：{contact_name}")
    
    # 设置消息内容到剪贴板，粘贴并发送
    set_clipboard(message)
    
    send_script = '''
    tell application "System Events"
        tell process "WeChat"
            -- 等待一下确保输入框已聚焦
            delay 0.3
            
            -- 粘贴消息内容
            keystroke "v" using command down
            delay 0.3
            
            -- 按回车发送
            keystroke return
        end tell
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', send_script], check=True, timeout=10)
        if is_first:
            print(f"✓ 消息已发送给：{contact_name}")
            # 保存当前联系人为上一次发送的联系人
            save_last_contact(contact_name)
        else:
            print(f"✓ 消息已发送（连续）")
        return True
    except subprocess.TimeoutExpired:
        print("✗ 操作超时")
        return False
    except Exception as e:
        print(f"✗ 错误：{e}")
        return False

def send_wechat_file(contact_name, file_path, is_first=False):
    """发送微信文件
    
    通过 Finder 复制文件，然后粘贴到微信
    """
    
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"✗ 文件不存在：{file_path}")
        return False
    
    # 第零步：激活微信窗口
    try:
        activate_wechat()
    except Exception as e:
        print(f"✗ 激活微信失败：{e}")
        return False
    
    # 如果是第一条消息，需要搜索联系人
    if is_first:
        last_contact = get_last_contact()
        is_same_contact = (last_contact == contact_name)
        
        # 只有新联系人才需要垫脚石
        if not is_same_contact:
            print(f"ℹ️ 新联系人（上一次：{last_contact or '无'}），使用垫脚石...")
            
            # 垫脚石：先打开文件传输助手，确保输入框聚焦
            set_clipboard("文件传输助手")
            
            dummy_script = '''
            tell application "System Events"
                tell process "WeChat"
                    -- 先按 ESC 清除任何打开的窗口或搜索框
                    key code 53
                    delay 0.2
                    
                    -- 按 Cmd+F 搜索
                    keystroke "f" using command down
                    delay 0.3
                    
                    -- 粘贴"文件传输助手"
                    keystroke "v" using command down
                    delay 0.3
                    
                    -- 按回车打开文件传输助手
                    keystroke return
                    delay 0.3
                end tell
            end tell
            '''
            
            try:
                subprocess.run(['osascript', '-e', dummy_script], check=True, timeout=10)
            except Exception as e:
                print(f"✗ 垫脚石失败：{e}")
                return False
        
        # 搜索真正的目标联系人
        set_clipboard(contact_name)
        
        search_script = '''
        tell application "System Events"
            tell process "WeChat"
                -- 先按 ESC 清除任何打开的窗口或搜索框
                key code 53
                delay 0.2
                
                -- 按 Cmd+A 全选清空搜索框
                keystroke "a" using command down
                delay 0.2
                
                -- 按 Cmd+F 重新搜索
                keystroke "f" using command down
                delay 0.3
                
                -- 粘贴联系人名字
                keystroke "v" using command down
                delay 0.5
                
                -- 按回车选择第一个搜索结果
                keystroke return
                delay 0.5
            end tell
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', search_script], check=True, timeout=10)
        except Exception as e:
            print(f"✗ 搜索联系人失败：{e}")
            return False
        
        if is_same_contact:
            print(f"ℹ️ 同一联系人（{contact_name}），窗口应已打开...")
        else:
            print(f"✓ 已切换到新联系人：{contact_name}")
    
    # 在 Finder 中复制文件
    file_name = os.path.basename(file_path)
    print(f"📎 复制文件：{file_name}")
    if not copy_file_in_finder(file_path):
        return False
    
    # 切换回微信并粘贴
    try:
        activate_wechat()
        time.sleep(0.3)
    except:
        pass
    
    send_script = '''
    tell application "System Events"
        tell process "WeChat"
            -- 等待一下确保输入框已聚焦
            delay 0.3
            
            -- 粘贴文件
            keystroke "v" using command down
            delay 0.5
            
            -- 按回车发送
            keystroke return
        end tell
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', send_script], check=True, timeout=15)
        if is_first:
            print(f"✓ 文件已发送给：{contact_name}")
            save_last_contact(contact_name)
        else:
            print(f"✓ 文件已发送（连续）")
        return True
    except subprocess.TimeoutExpired:
        print("✗ 操作超时")
        return False
    except Exception as e:
        print(f"✗ 错误：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python send_wechat.py <联系人名字> <消息/文件路径> [消息 2/文件路径 2] ...")
        print("      支持连续发送多条消息和文件给同一联系人")
        print("      按参数顺序发送，用户可自由控制先发文字还是先发文件")
        sys.exit(1)
    
    contact = sys.argv[1]
    items = sys.argv[2:]
    
    all_success = True
    total = len(items)
    current = 0
    
    # 按用户传入的顺序依次发送
    for item in items:
        current += 1
        is_first = (current == 1)
        
        # 自动判断是文件还是消息
        if is_file_path(item):
            file_name = os.path.basename(item)
            print(f"\n[{current}/{total}] 发送文件：{file_name}")
            success = send_wechat_file(contact, item, is_first=is_first)
            if not success:
                all_success = False
                print(f"✗ 文件发送失败：{item}")
        else:
            preview = item[:50] + '...' if len(item) > 50 else item
            print(f"\n[{current}/{total}] 发送消息：{preview}")
            success = send_wechat_message(contact, item, is_first=is_first)
            if not success:
                all_success = False
                print(f"✗ 消息发送失败")
        
        # 连续发送时，每条之间稍作停顿
        if current < total:
            time.sleep(0.5)
    
    # 统计文件和消息数量
    files_count = sum(1 for item in items if is_file_path(item))
    messages_count = total - files_count
    
    if all_success:
        print(f"\n✓ 完成：{files_count} 个文件 + {messages_count} 条消息已发送给 {contact}")
    else:
        print(f"\n✗ 部分发送失败")
    
    sys.exit(0 if all_success else 1)

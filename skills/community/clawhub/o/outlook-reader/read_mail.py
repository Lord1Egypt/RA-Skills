# -*- coding: utf-8 -*-
"""
Outlook邮件读取脚本
用于搜索特定主题邮件并下载附件
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import win32com.client
import os
import datetime

# ========== 配置 ==========
SAVE_DIR = r"C:\Users\jw0921\Desktop\GF_Bills"  # 附件保存目录
MAX_EMAILS = 100  # 最大搜索邮件数
FOLDER_ID = 6  # 6=收件箱


def connect_outlook():
    """连接Outlook"""
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        return outlook, namespace
    except Exception as e:
        print(f"连接Outlook失败: {e}")
        return None, None


def read_emails(keyword, folder_id=FOLDER_ID, max_emails=MAX_EMAILS):
    """读取包含关键词的邮件"""
    outlook, namespace = connect_outlook()
    if not outlook:
        return []
    
    inbox = namespace.GetDefaultFolder(folder_id)
    messages = inbox.Items
    messages.Sort("ReceivedTime", True)  # 按时间倒序
    
    results = []
    count = 0
    
    print(f"正在搜索包含'{keyword}'的邮件...")
    
    for msg in messages:
        if count >= max_emails:
            break
            
        try:
            subject = str(msg.Subject) if msg.Subject else ""
            
            if keyword in subject:
                attachments = []
                for att in msg.Attachments:
                    attachments.append({
                        'name': att.FileName,
                        'size': att.Size
                    })
                
                results.append({
                    'subject': subject,
                    'date': msg.ReceivedTime,
                    'sender': msg.SenderName if msg.SenderName else "",
                    'attachments': attachments,
                    'message_obj': msg  # 保留对象引用用于下载
                })
                
        except Exception as e:
            continue
            
        count += 1
    
    return results


def download_attachment(msg_data, save_dir):
    """下载单个邮件的附件"""
    msg = msg_data['message_obj']
    saved_files = []
    
    try:
        for att in msg.Attachments:
            filename = att.FileName
            # 过滤掉太小或可疑的附件
            if att.Size < 1000:
                continue
                
            save_path = os.path.join(save_dir, filename)
            att.SaveAsFile(save_path)
            saved_files.append(save_path)
            print(f"  已下载: {filename}")
            
    except Exception as e:
        print(f"  下载失败: {e}")
    
    return saved_files


def search_and_download(keyword, save_dir=SAVE_DIR):
    """搜索并下载附件"""
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 搜索邮件
    emails = read_emails(keyword)
    
    if not emails:
        print(f"未找到包含'{keyword}'的邮件")
        return []
    
    print(f"\n找到 {len(emails)} 封邮件:")
    
    # 下载附件
    all_files = []
    for i, email in enumerate(emails, 1):
        print(f"\n[{i}] {email['subject']}")
        print(f"    日期: {email['date']}")
        print(f"    附件: {len(email['attachments'])}个")
        
        if email['attachments']:
            files = download_attachment(email, save_dir)
            all_files.extend(files)
    
    print(f"\n=== 完成 ===")
    print(f"共下载 {len(all_files)} 个附件")
    print(f"保存位置: {save_dir}")
    
    return all_files


# ========== 主程序 ==========
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Outlook邮件读取')
    parser.add_argument('--keyword', '-k', default='广发', help='搜索关键词')
    parser.add_argument('--save', '-s', default=SAVE_DIR, help='保存目录')
    parser.add_argument('--max', '-m', type=int, default=MAX_EMAILS, help='最大邮件数')
    
    args = parser.parse_args()
    
    search_and_download(args.keyword, args.save)
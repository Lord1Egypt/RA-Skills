# Outlook 邮件读取技能

自动读取Outlook邮件，搜索特定主题，下载附件。

## 触发条件

- 用户要求读取Outlook邮件
- 用户提到"广发信用卡账单"、"邮箱对账单"
- 用户要求自动处理邮件附件

---

## 一、核心原理

使用 Windows COM 接口连接 Outlook：
```python
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
inbox = namespace.GetDefaultFolder(6)  # 6=收件箱
messages = inbox.Items
```

---

## 二、读取邮件并下载附件

### 基础脚本

```python
# -*- coding: utf-8 -*-
import win32com.client
import os
import datetime

def read_outlook_emails(subject_keyword, folder_id=6, max_emails=50):
    """
    读取Outlook邮件
    
    参数:
        subject_keyword: 主题关键词，如"广发"
        folder_id: 文件夹ID，默认6=收件箱
        max_emails: 最大读取数量
    
    返回:
        匹配的邮件列表
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(folder_id)
    messages = inbox.Items
    
    # 按时间排序
    messages.Sort("ReceivedTime", True)
    
    matched = []
    count = 0
    
    for msg in messages:
        if count >= max_emails:
            break
            
        if subject_keyword and subject_keyword in str(msg.Subject):
            # 获取附件
            attachments = []
            for att in msg.Attachments:
                attachments.append({
                    'name': att.FileName,
                    'size': att.Size
                })
            
            matched.append({
                'subject': msg.Subject,
                'date': msg.ReceivedTime,
                'sender': msg.SenderName,
                'attachments': attachments,
                'message': msg  # 完整消息对象，用于下载附件
            })
            
        count += 1
    
    return matched


def download_attachments(messages, save_dir):
    """
    下载邮件附件
    
    参数:
        messages: 邮件列表
        save_dir: 保存目录
    """
    os.makedirs(save_dir, exist_ok=True)
    
    downloaded = []
    for msg_data in messages:
        msg = msg_data['message']
        
        for att in msg.Attachments:
            save_path = os.path.join(save_dir, att.FileName)
            att.SaveAsFile(save_path)
            downloaded.append(save_path)
            print(f"已下载: {save_path}")
    
    return downloaded


# 使用示例
if __name__ == "__main__":
    # 1. 搜索广发信用卡对账单
    emails = read_outlook_emails("广发")
    print(f"找到 {len(emails)} 封匹配邮件")
    
    # 2. 下载附件
    save_dir = r"C:\Users\jw0921\Desktop\GF_Bills"
    files = download_attachments(emails, save_dir)
    print(f"共下载 {len(files)} 个附件")
```

---

## 三、搜索多个关键词

```python
def search_multiple_keywords(keywords, folder_id=6):
    """搜索多个关键词"""
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(folder_id)
    messages = inbox.Items
    messages.Sort("ReceivedTime", True)
    
    results = {kw: [] for kw in keywords}
    
    for msg in messages:
        subject = str(msg.Subject)
        for kw in keywords:
            if kw in subject:
                results[kw].append({
                    'subject': subject,
                    'date': msg.ReceivedTime,
                    'attachments': [att.FileName for att in msg.Attachments]
                })
    
    return results


# 使用
results = search_multiple_keywords(["广发", "招商", "建设", "工商银行"])
for kw, emails in results.items():
    if emails:
        print(f"{kw}: {len(emails)} 封")
```

---

## 四、搜索所有文件夹

```python
def search_all_folders(keyword, namespace):
    """遍历所有文件夹搜索"""
    results = []
    
    def search_folder(folder, depth=0):
        try:
            messages = folder.Items
            for msg in messages:
                try:
                    if keyword in str(msg.Subject):
                        results.append({
                            'folder': folder.Name,
                            'subject': msg.Subject,
                            'date': msg.ReceivedTime
                        })
                except:
                    pass
        except:
            pass
        
        # 递归搜索子文件夹
        for subfolder in folder.Folders:
            search_folder(subfolder, depth+1)
    
    # 从根文件夹开始搜索
    for folder in namespace.Folders:
        search_folder(folder)
    
    return results


# 使用
outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
results = search_all_folders("广发", namespace)
print(f"共找到 {len(results)} 封邮件")
```

---

## 五、处理附件

### 判断附件类型
```python
for att in msg.Attachments:
    filename = att.FileName
    # 判断是否为PDF
    if filename.lower().endswith('.pdf'):
        att.SaveAsFile(os.path.join(save_dir, filename))
```

### 解压ZIP附件
```python
import zipfile

for att in msg.Attachments:
    if att.FileName.endswith('.zip'):
        zip_path = os.path.join(save_dir, att.FileName)
        att.SaveAsFile(zip_path)
        
        # 解压
        extract_dir = save_dir + "\\" + att.FileName[:-4]
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
```

---

## 六、常见问题

### 1. Outlook未打开
```python
try:
    outlook = win32com.client.Dispatch("Outlook.Application")
except:
    print("请先打开Outlook")
```

### 2. 中文编码问题
```python
# 在Windows命令提示符执行
chcp 65001
# 或在Python开头加
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### 3. 找不到邮件
- 检查Outlook是否同步
- 尝试搜索所有文件夹
- 可能是其他邮箱账户

### 4. 附件太大
- Outlook有附件大小限制
- 可考虑用IMAP替代

---

## 七、文件夹ID参考

| ID | 文件夹 |
|----|--------|
| 0 | 文件夹根目录 |
| 1 | 用户自定义文件夹 |
| 2 | 收件箱 |
| 3 | 发件箱 |
| 4 | 已发送邮件 |
| 5 | 已删除邮件 |
| 6 | 收件箱(inbox) |
| 9 | 日历 |
| 10 | 联系人 |
| 11 | 便签 |

---

## 八、自动化方案

### 方案1：定时检查（cron）
```python
# 每小时检查一次
cron add --schedule "every 1h" --payload "检查广发信用卡账单"
```

### 方案2：Outlook规则
```
规则：如果发件人包含"95508" → 保存附件到指定文件夹
```
然后监控该文件夹

### 方案3：收到邮件自动转发
```
规则：如果主题包含"广发对账单" → 转发给AI助手
```
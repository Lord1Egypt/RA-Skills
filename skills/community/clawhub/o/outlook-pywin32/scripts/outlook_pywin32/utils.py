import datetime
import json
import os
import sys
import win32com.client


def get_outlook_app():
    """获取Outlook应用对象"""
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        return outlook
    except Exception as e:
        print(f"错误: 无法连接Outlook - {e}")
        sys.exit(1)


def get_namespace(outlook):
    """获取MAPI命名空间"""
    return outlook.GetNamespace("MAPI")


def get_account(account: str = None):
    """
    获取邮箱账户，优先级：
    1. 传入的 account 参数
    2. 环境变量 OUTLOOK_ACCOUNT
    3. 同目录下的 config.json 文件
    """
    if account:
        return account
    
    # 从环境变量获取
    env_account = os.environ.get("OUTLOOK_ACCOUNT")
    if env_account:
        return env_account
    
    # 从 config.json 文件获取
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("outlook_account")
        except Exception:
            pass
    
    return None


def get_mail_folder(namespace, folder_name: str = "inbox", account_email: str = None):
    """
    获取指定邮箱账户的文件夹
    
    参数:
        namespace: MAPI命名空间
        folder_name: 文件夹名称
        account_email: 邮箱账户地址，为空则使用默认账户
    """
    folder_map = {
        "inbox": 6,
        "sentitems": 5,
        "drafts": 16,
        "deleteditems": 3,
        "outbox": 4,
    }
    
    folder_id = folder_map.get(folder_name.lower(), 6)
    
    if account_email:
        for account in namespace.Accounts:
            if account.SmtpAddress.lower() == account_email.lower():
                store = account.DeliveryStore
                return store.GetDefaultFolder(folder_id)
        raise Exception(f"未找到邮箱账户: {account_email}")
    else:
        return namespace.GetDefaultFolder(folder_id)


def parse_date_for_outlook(date_str: str, is_start: bool = True):
    """
    解析日期字符串并转换为Outlook Restrict方法需要的格式
    
    参数:
        date_str: 日期字符串
        is_start: 是否为起始时间，True则默认00:00:00，False则默认23:59:59
    """
    if not date_str:
        return None
    
    # 带时间的格式
    time_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
    ]
    
    # 只带日期的格式
    date_only_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
    ]
    
    dt = None
    has_time = False
    
    # 先尝试带时间的格式
    for fmt in time_formats:
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            has_time = True
            break
        except ValueError:
            continue
    
    # 如果没有带时间，尝试只带日期的格式
    if not dt:
        for fmt in date_only_formats:
            try:
                dt = datetime.datetime.strptime(date_str, fmt)
                has_time = False
                break
            except ValueError:
                continue
    
    if not dt:
        return None
    
    # 如果没有指定时间，设置默认时间
    if not has_time:
        if is_start:
            dt = datetime.datetime.combine(dt.date(), datetime.datetime.min.time())
        else:
            dt = datetime.datetime.combine(dt.date(), datetime.datetime.max.time())
    
    # 转换为Outlook Restrict需要的格式: mm/dd/yyyy HH:mm:ss (24小时制)
    return dt.strftime("%m/%d/%Y %H:%M:%S")

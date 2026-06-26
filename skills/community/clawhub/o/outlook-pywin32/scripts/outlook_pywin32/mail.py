import datetime
from .utils import get_outlook_app, get_namespace, get_account, get_mail_folder, parse_date_for_outlook


def mail_folders(account: str = None):
    """
    检查并列出邮件文件夹

    参数:
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
    """
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)
    account = get_account(account)
    
    folder_map = {
        6: "inbox",
        5: "sentitems",
        16: "drafts",
        3: "deleteditems",
        4: "outbox",
        9: "calendar",
        10: "contacts",
        11: "journal",
        12: "notes",
        13: "tasks",
    }
    
    results = []
    
    if account:
        for acc in namespace.Accounts:
            if acc.SmtpAddress.lower() == account.lower():
                store = acc.DeliveryStore
                for folder_id, folder_name in folder_map.items():
                    try:
                        folder = store.GetDefaultFolder(folder_id)
                        results.append({
                            "name": folder_name,
                            "id": folder_id,
                            "item_count": folder.Items.Count,
                            "display_name": folder.Name,
                        })
                    except Exception:
                        continue
                break
    else:
        for folder_id, folder_name in folder_map.items():
            try:
                folder = namespace.GetDefaultFolder(folder_id)
                results.append({
                    "name": folder_name,
                    "id": folder_id,
                    "item_count": folder.Items.Count,
                    "display_name": folder.Name,
                })
            except Exception:
                continue
    
    print("邮件文件夹列表:")
    print("-" * 80)
    for r in results:
        print(f"  {r['display_name']} ({r['name']}): {r['item_count']} 项")
    
    return results


def mail_new(to: str, subject: str, body: str = "", cc: str = "", bcc: str = ""):
    """
    创建邮件并保存到草稿箱

    参数:
        --to: 收件人邮箱 (必需)
        --subject: 邮件主题 (必需)
        --body: 邮件正文
        --cc: 抄送
        --bcc: 密送
    """
    outlook = get_outlook_app()
    mail = outlook.CreateItem(0)  # 0 = MailItem

    mail.To = to
    mail.Subject = subject
    if body:
        mail.Body = body
    if cc:
        mail.CC = cc
    if bcc:
        mail.BCC = bcc

    mail.Save()
    mail.lastModificationTime = datetime.datetime.now().date().strftime("%m/%d/%Y %H:%M:%S")
    print(f"邮件已保存到草稿箱 -> {to}: {subject}")
    return {"success": True, "to": to, "subject": subject, "saved_to": "drafts"}


def mail_list(folder: str = "inbox", limit: int = 10, account: str = None):
    """
    列出文件夹中的邮件

    参数:
        --folder: 文件夹名称 (inbox/sentitems/drafts, 默认inbox)
        --limit: 返回数量 (默认10)
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
    """
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)
    account = get_account(account)
    mail_folder = get_mail_folder(namespace, folder, account)

    messages = mail_folder.Items
    messages.Sort("[ReceivedTime]", True)  # 按时间倒序

    results = []
    for i, msg in enumerate(messages):
        if i >= limit:
            break
        is_unread = msg.UnRead if hasattr(msg, "UnRead") else False
        results.append({
            "index": i + 1,
            "subject": msg.Subject,
            "sender": msg.SenderName if hasattr(msg, "SenderName") else "N/A",
            "received": str(msg.ReceivedTime) if hasattr(msg, "ReceivedTime") else "N/A",
            "unread": is_unread,
        })

    for r in results:
        status_icon = "📩" if r["unread"] else "📭"
        status_text = "未读" if r["unread"] else "已读"
        print(f"{status_icon} [{r['index']}] {r['subject']} - {r['sender']} ({r['received']}) [{status_text}]")

    return results


def mail_read(folder: str = "inbox", index: int = 1, account: str = None):
    """
    读取指定邮件内容

    参数:
        --folder: 文件夹名称 (默认inbox)
        --index: 邮件索引 (默认1, 从mail-list获取)
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
    """
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)
    account = get_account(account)
    mail_folder = get_mail_folder(namespace, folder, account)

    messages = mail_folder.Items
    messages.Sort("[ReceivedTime]", True)

    if index < 1 or index > messages.Count:
        print(f"错误: 索引 {index} 超出范围 (1-{messages.Count})")
        return None

    msg = messages(index)

    was_unread = msg.UnRead if hasattr(msg, "UnRead") else False
    
    result = {
        "subject": msg.Subject,
        "sender": msg.SenderName if hasattr(msg, "SenderName") else "N/A",
        "sender_email": msg.SenderEmailAddress if hasattr(msg, "SenderEmailAddress") else "N/A",
        "to": msg.To if hasattr(msg, "To") else "N/A",
        "received": str(msg.ReceivedTime) if hasattr(msg, "ReceivedTime") else "N/A",
        "body": msg.Body[:500] if hasattr(msg, "Body") else "",
        "was_unread": was_unread,
    }

    print(f"主题: {result['subject']}")
    print(f"发件人: {result['sender']} <{result['sender_email']}>")
    print(f"收件人: {result['to']}")
    print(f"时间: {result['received']}")
    print(f"状态: {'未读' if was_unread else '已读'}")
    print("-" * 50)
    print(result["body"])

    # 标记为已读
    if hasattr(msg, "UnRead"):
        msg.UnRead = False

    return result


def mail_search(query: str = "", limit: int = 50, account: str = None, start_time: str = None, end_time: str = None):
    """
    搜索邮件

    参数:
        --query: 搜索关键词 (可选)
        --limit: 返回数量 (默认50)
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
        --start-time: 起始时间 (如 2024-01-01 或 2024-01-01 09:00:00)
        --end-time: 结束时间 (如 2024-12-31 或 2024-12-31 18:00:00)
    """
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)

    account = get_account(account)
    inbox = get_mail_folder(namespace, "inbox", account)
    messages = inbox.Items

    # 使用Outlook SQL查询语法
    sql_parts = []
    
    # 关键词搜索
    if query:
        # 转义单引号
        escaped_query = query.replace("'", "''")
        sql_parts.append(f"(urn:schemas:httpmail:subject LIKE '%{escaped_query}%' OR urn:schemas:httpmail:textdescription LIKE '%{escaped_query}%')")
    
    # 时间范围搜索
    if start_time or end_time:
        start_date_outlook = parse_date_for_outlook(start_time, is_start=True)
        end_date_outlook = parse_date_for_outlook(end_time, is_start=False)
        
        if start_date_outlook:
            sql_parts.append(f"urn:schemas:httpmail:datereceived >= '{start_date_outlook}'")
        if end_date_outlook:
            sql_parts.append(f"urn:schemas:httpmail:datereceived <= '{end_date_outlook}'")
    
    # 构建完整的SQL查询
    filtered_messages = messages
    if sql_parts:
        sql_criteria = " AND ".join(sql_parts)
        full_query = f"@SQL={sql_criteria}"
        try:
            #print(f"使用SQL查询: {full_query}")
            filtered_messages = messages.Restrict(full_query)
        except Exception as e:
            print(f"警告: SQL查询失败，将使用所有邮件 - {e}")
            filtered_messages = messages

    results = []
    for msg in filtered_messages:
        if len(results) >= limit:
            break
        
        results.append({
            "subject": msg.Subject if hasattr(msg, "Subject") else "",
            "sender": msg.SenderName if hasattr(msg, "SenderName") else "",
            "received": str(msg.ReceivedTime) if hasattr(msg, "ReceivedTime") else "N/A",
        })

    for i, r in enumerate(results):
        print(f"[{i + 1}] {r['subject']} - {r['sender']} ({r['received']})")

    return results

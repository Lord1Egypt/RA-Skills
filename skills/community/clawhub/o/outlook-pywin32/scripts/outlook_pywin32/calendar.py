import datetime
from .utils import get_outlook_app, get_namespace, get_account, parse_date_for_outlook


def calendar_list(limit: int = 10, days: int = 7, include_today: bool = True, account: str = None):
    """
    列出即将举行的日程安排事件

    参数:
        --limit: 返回数量 (默认10)
        --days: 查看未来几天的事件 (默认7)
        --include-today: 是否包含今天的事件 (true/false, 默认true)
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
    """
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)
    account = get_account(account)
    
    # 获取日历文件夹
    if account:
        for acc in namespace.Accounts:
            if acc.SmtpAddress.lower() == account.lower():
                store = acc.DeliveryStore
                calendar_folder = store.GetDefaultFolder(9)
                break
        else:
            # 如果没有找到指定账户，使用默认文件夹
            calendar_folder = namespace.GetDefaultFolder(9)
    else:
        calendar_folder = namespace.GetDefaultFolder(9)
    
    items = calendar_folder.Items
    items.IncludeRecurrences = True
    items.Sort("[Start]")
    
    # 构建时间范围
    now = datetime.datetime.now()
    if include_today:
        start_date = datetime.datetime.combine(now.date(), datetime.datetime.min.time())
    else:
        start_date = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.datetime.min.time())
    end_date = now + datetime.timedelta(days=days)
    
    results = []
    count = 0
    
    for item in items:
        if count >= limit:
            break
        
        try:
            start_time = None
            if hasattr(item, "Start"):
                # 转换 Outlook datetime 对象为 Python datetime
                start_str = str(item.Start)
                try:
                    # 尝试解析 Outlook 的日期时间格式
                    if '+' in start_str:
                        start_str = start_str.split('+')[0]
                    if '.' in start_str and ' ' in start_str:
                        start_str = start_str.split('.')[0]
                    start_time = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                except:
                    continue
            
            if start_time and start_date <= start_time <= end_date:
                results.append({
                    "index": count + 1,
                    "subject": item.Subject if hasattr(item, "Subject") else "",
                    "start": str(item.Start) if hasattr(item, "Start") else "",
                    "end": str(item.End) if hasattr(item, "End") else "",
                    "location": item.Location if hasattr(item, "Location") else "",
                    "all_day": item.AllDayEvent if hasattr(item, "AllDayEvent") else False,
                    "is_recurring": item.IsRecurring if hasattr(item, "IsRecurring") else False,
                })
                count += 1
        except Exception:
            continue
    
    today_text = "（包含今天）" if include_today else "（不包含今天）"
    print(f"未来 {days} 天的日程安排 {today_text} (最多 {limit} 条):")
    print("-" * 80)
    for r in results:
        all_day_icon = "☀️" if r["all_day"] else "⏰"
        recurring_icon = "🔄" if r["is_recurring"] else ""
        print(f"{all_day_icon}{recurring_icon} [{r['index']}] {r['subject']}")
        print(f"    时间: {r['start']} - {r['end']}")
        if r["location"]:
            print(f"    地点: {r['location']}")
        print()
    
    return results


def calendar_new(subject: str, start: str, end: str = "", location: str = "", body: str = "", 
                 required_attendees: str = "", optional_attendees: str = "",
                 all_day: bool = False, reminder: int = 15, account: str = None):
    """
    创建一个日程安排事件

    参数:
        --subject: 日程主题 (必需)
        --start: 开始时间 (格式: YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DD)
        --end: 结束时间 (可选，默认开始时间+30分钟)
        --location: 地点 (可选)
        --body: 备注 (可选)
        --required-attendees: 必需参与人 (多个用分号分隔)
        --optional-attendees: 可选参与人 (多个用分号分隔)
        --all-day: 是否全天事件 (true/false, 默认false)
        --reminder: 提醒提前分钟数 (默认15, 0表示不提醒)
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
    """
    outlook = get_outlook_app()
    
    # 解析开始时间
    start_dt = parse_date_for_outlook(start, is_start=True)
    if not start_dt:
        print(f"错误: 无法解析开始时间 '{start}'")
        return None
    
    # 转换为 datetime 对象
    try:
        start_datetime = datetime.datetime.strptime(start_dt, "%m/%d/%Y %H:%M:%S")
    except ValueError:
        print(f"错误: 时间格式无效 '{start}'")
        return None
    
    # 解析结束时间
    if end:
        end_dt = parse_date_for_outlook(end, is_start=False)
        if not end_dt:
            print(f"错误: 无法解析结束时间 '{end}'")
            return None
        try:
            end_datetime = datetime.datetime.strptime(end_dt, "%m/%d/%Y %H:%M:%S")
        except ValueError:
            print(f"错误: 时间格式无效 '{end}'")
            return None
    else:
        # 默认30分钟
        if all_day:
            end_datetime = start_datetime + datetime.timedelta(days=1)
        else:
            end_datetime = start_datetime + datetime.timedelta(minutes=30)
    
    # 创建日历项
    appointment = outlook.CreateItem(1)  # 1 = AppointmentItem
    
    appointment.Subject = subject
    appointment.StartUTC = start_datetime
    appointment.EndUTC = end_datetime
    appointment.AllDayEvent = all_day
    
    if location:
        appointment.Location = location
    if body:
        appointment.Body = body
    if required_attendees:
        appointment.RequiredAttendees = required_attendees
    if optional_attendees:
        appointment.OptionalAttendees = optional_attendees
    
    if reminder > 0:
        appointment.ReminderSet = True
        appointment.ReminderMinutesBeforeStart = reminder
    else:
        appointment.ReminderSet = False
    
    # 如果指定了账户，使用该账户发送
    if account:
        namespace = get_namespace(outlook)
        for acc in namespace.Accounts:
            if acc.SmtpAddress.lower() == account.lower():
                appointment.Save()
                appointment.Move(acc.DeliveryStore.GetDefaultFolder(9))
                break
    else:
        appointment.Save()
    
    print(f"日程已创建: {subject}")
    print(f"  时间: {start_datetime} - {end_datetime}")
    if all_day:
        print("  全天事件: 是")
    if location:
        print(f"  地点: {location}")
    if required_attendees:
        print(f"  必需参与人: {required_attendees}")
    if optional_attendees:
        print(f"  可选参与人: {optional_attendees}")
    if reminder > 0:
        print(f"  提醒: 提前 {reminder} 分钟")
    
    return {
        "success": True,
        "subject": subject,
        "start": str(start_datetime),
        "end": str(end_datetime),
        "location": location,
        "required_attendees": required_attendees,
        "optional_attendees": optional_attendees,
        "all_day": all_day,
    }


def calendar_edit(subject: str = None, start: str = None, new_subject: str = None, new_start: str = None, new_end: str = None, location: str = None, body: str = None,
                 required_attendees: str = None, optional_attendees: str = None, all_day: bool = None, reminder: int = None, account: str = None):
    """
    修改一个日程安排事件（仅保存，不发送通知）

    参数:
        --subject: 原日程主题 (可选，用于搜索)
        --start: 原日程开始时间 (可选，用于搜索，格式: YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DD)
        --new-subject: 新日程主题 (可选)
        --new-start: 新开始时间 (可选，格式: YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DD)
        --new-end: 新结束时间 (可选)
        --location: 地点 (可选)
        --body: 备注 (可选)
        --required-attendees: 必需参与人 (可选，多个用分号分隔)
        --optional-attendees: 可选参与人 (可选，多个用分号分隔)
        --all-day: 是否全天事件 (可选，true/false)
        --reminder: 提醒提前分钟数 (可选，0表示不提醒)
        --account: 邮箱账户地址，优先级：1. 传入参数 2. 环境变量 OUTLOOK_ACCOUNT 3. config.json 文件
    """
    # 检查至少提供了一个搜索参数
    if subject is None and start is None:
        print("错误: 必须提供 subject 或 start 参数用于搜索日程")
        return None
    
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)
    account = get_account(account)
    
    # 获取日历文件夹
    if account:
        for acc in namespace.Accounts:
            if acc.SmtpAddress.lower() == account.lower():
                store = acc.DeliveryStore
                calendar_folder = store.GetDefaultFolder(9)
                break
        else:
            # 如果没有找到指定账户，使用默认文件夹
            calendar_folder = namespace.GetDefaultFolder(9)
    else:
        calendar_folder = namespace.GetDefaultFolder(9)
    
    items = calendar_folder.Items
    items.IncludeRecurrences = True
    items.Sort("[Start]")
    
    # 解析搜索用的开始时间（如果提供）
    search_start_datetime = None
    if start:
        search_start_dt = parse_date_for_outlook(start, is_start=True)
        if not search_start_dt:
            print(f"错误: 无法解析搜索开始时间 '{start}'")
            return None
        try:
            search_start_datetime = datetime.datetime.strptime(search_start_dt, "%m/%d/%Y %H:%M:%S")
        except ValueError:
            print(f"错误: 时间格式无效 '{start}'")
            return None
    
    # 找到匹配的日程
    target_item = None
    
    for item in items:
        try:
            item_subject = item.Subject if hasattr(item, "Subject") else ""
            item_start = None
            
            if hasattr(item, "Start"):
                # 转换 Outlook datetime 对象为 Python datetime
                start_str = str(item.Start)
                try:
                    # 尝试解析 Outlook 的日期时间格式
                    if '+' in start_str:
                        start_str = start_str.split('+')[0]
                    if '.' in start_str and ' ' in start_str:
                        start_str = start_str.split('.')[0]
                    item_start = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                except:
                    continue
            
            # 匹配条件：如果提供了subject则匹配subject，如果提供了start则匹配start时间
            match = True
            if subject:
                match = match and (item_subject == subject)
            if search_start_datetime and item_start:
                # 比较开始时间（允许1分钟内的误差）
                time_diff = abs((item_start - search_start_datetime).total_seconds())
                match = match and (time_diff <= 60)
            
            if match:
                target_item = item
                break
        except Exception:
            continue
    
    if not target_item:
        if subject and start:
            print(f"错误: 未找到主题为 '{subject}' 且开始时间为 '{start}' 的日程")
        elif subject:
            print(f"错误: 未找到主题为 '{subject}' 的日程")
        else:
            print(f"错误: 未找到开始时间为 '{start}' 的日程")
        return None
    
    # 修改日程属性
    if new_subject is not None:
        target_item.Subject = new_subject
    
    if new_start is not None:
        start_dt = parse_date_for_outlook(new_start, is_start=True)
        if not start_dt:
            print(f"错误: 无法解析开始时间 '{new_start}'")
            return None
        try:
            start_datetime = datetime.datetime.strptime(start_dt, "%m/%d/%Y %H:%M:%S")
            target_item.StartUTC = start_datetime
        except ValueError:
            print(f"错误: 时间格式无效 '{new_start}'")
            return None
    
    if new_end is not None:
        end_dt = parse_date_for_outlook(new_end, is_start=False)
        if not end_dt:
            print(f"错误: 无法解析结束时间 '{new_end}'")
            return None
        try:
            end_datetime = datetime.datetime.strptime(end_dt, "%m/%d/%Y %H:%M:%S")
            target_item.EndUTC = end_datetime
        except ValueError:
            print(f"错误: 时间格式无效 '{new_end}'")
            return None
    
    if location is not None:
        target_item.Location = location
    
    if body is not None:
        target_item.Body = body
    
    if required_attendees is not None:
        target_item.RequiredAttendees = required_attendees
    
    if optional_attendees is not None:
        target_item.OptionalAttendees = optional_attendees
    
    if all_day is not None:
        target_item.AllDayEvent = all_day
    
    if reminder is not None:
        if reminder > 0:
            target_item.ReminderSet = True
            target_item.ReminderMinutesBeforeStart = reminder
        else:
            target_item.ReminderSet = False
    
    # 保存修改（不发送通知）
    target_item.Save()
    
    # 获取修改后的日程信息
    modified_subject = target_item.Subject if hasattr(target_item, "Subject") else ""
    modified_start = str(target_item.Start) if hasattr(target_item, "Start") else ""
    modified_end = str(target_item.End) if hasattr(target_item, "End") else ""
    modified_location = target_item.Location if hasattr(target_item, "Location") else ""
    modified_all_day = target_item.AllDayEvent if hasattr(target_item, "AllDayEvent") else False
    
    print(f"日程已修改: {modified_subject}")
    print(f"  时间: {modified_start} - {modified_end}")
    if modified_all_day:
        print("  全天事件: 是")
    if modified_location:
        print(f"  地点: {modified_location}")
    
    return {
        "success": True,
        "subject": modified_subject,
        "start": modified_start,
        "end": modified_end,
        "location": modified_location,
        "all_day": modified_all_day,
    }

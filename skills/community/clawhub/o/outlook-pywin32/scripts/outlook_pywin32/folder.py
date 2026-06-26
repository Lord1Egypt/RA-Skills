from .utils import get_outlook_app, get_namespace, get_account, get_mail_folder


def folder_list(account: str = None):
    """
    列出所有默认文件夹

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
                            "display_name": folder.Name,
                            "item_count": folder.Items.Count,
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
                    "display_name": folder.Name,
                    "item_count": folder.Items.Count,
                })
            except Exception:
                continue
    
    print("文件夹列表:")
    print("-" * 80)
    for r in results:
        print(f"  {r['display_name']} ({r['name']}): {r['item_count']} 项")
    
    return results

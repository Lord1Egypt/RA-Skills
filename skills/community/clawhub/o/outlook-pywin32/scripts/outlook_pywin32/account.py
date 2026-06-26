from .utils import get_outlook_app, get_namespace


def account_list():
    """
    列出所有可用的 Outlook 邮箱账户
    """
    outlook = get_outlook_app()
    namespace = get_namespace(outlook)
    
    accounts = []
    for account in namespace.Accounts:
        accounts.append({
            "name": account.DisplayName,
            "email": account.SmtpAddress,
        })
    
    print("可用的 Outlook 账户:")
    for i, acc in enumerate(accounts):
        print(f"  [{i + 1}] {acc['name']} <{acc['email']}>")
    
    return accounts

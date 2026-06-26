"""
配置管理模块
负责加载和管理环境变量配置
"""
import os
from dotenv import load_dotenv


def load_config() -> dict:
    """
    加载环境变量配置
    
    Returns:
        dict: 包含所有配置项的字典
        
    Raises:
        ValueError: 如果必需配置项缺失
    """
    # 加载 .env 文件
    load_dotenv()
    
    # 必需配置项
    client_id = os.getenv('CLIENT_ID')
    tenant_id = os.getenv('TENANT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    default_password = os.getenv('DEFAULT_PASSWORD')
    
    # 验证必需配置项
    if not client_id:
        raise ValueError("CLIENT_ID 配置缺失")
    if not tenant_id:
        raise ValueError("TENANT_ID 配置缺失")
    if not client_secret:
        raise ValueError("CLIENT_SECRET 配置缺失")
    if not default_password:
        raise ValueError("DEFAULT_PASSWORD 配置缺失")
    
    # 可选配置项（带默认值）
    force_change_password = os.getenv('FORCE_CHANGE_PASSWORD', 'false').lower() == 'true'
    default_domain = os.getenv('DEFAULT_DOMAIN', '')  # 默认域名，如果未设置则必须提供完整邮箱
    
    # 邮件通知配置
    notification_enabled = os.getenv('NOTIFICATION_ENABLED', 'false').lower() == 'true'
    notification_from_email = os.getenv('NOTIFICATION_FROM_EMAIL', '')  # 发件人邮箱
    notification_bcc_emails = os.getenv('NOTIFICATION_BCC_EMAILS', '')  # 密送邮箱，多个用逗号分隔
    notification_email_domain = os.getenv('NOTIFICATION_EMAIL_DOMAIN', '')  # 通知邮件目标域名（用于邮箱域名转换）
    
    # SMTP 配置（用于发送邮件）
    smtp_host = os.getenv('SMTP_HOST', '')
    smtp_port = int(os.getenv('SMTP_PORT', '465'))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    smtp_use_ssl = os.getenv('SMTP_USE_SSL', 'true').lower() == 'true'
    
    # 构建 token 端点 URL
    token_endpoint = f"https://login.chinacloudapi.cn/{tenant_id}/oauth2/v2.0/token"
    
    # Graph API 基础 URL
    graph_api_base_url = "https://microsoftgraph.chinacloudapi.cn/v1.0"
    
    # 解析密送邮箱列表
    bcc_emails_list = []
    if notification_bcc_emails:
        bcc_emails_list = [email.strip() for email in notification_bcc_emails.split(',') if email.strip()]
    
    return {
        'client_id': client_id,
        'tenant_id': tenant_id,
        'client_secret': client_secret,
        'default_password': default_password,
        'token_endpoint': token_endpoint,
        'graph_api_base_url': graph_api_base_url,
        'force_change_password': force_change_password,
        'default_domain': default_domain,
        'notification_enabled': notification_enabled,
        'notification_from_email': notification_from_email,
        'notification_bcc_emails': bcc_emails_list,
        'notification_email_domain': notification_email_domain,
        'smtp_host': smtp_host,
        'smtp_port': smtp_port,
        'smtp_username': smtp_username,
        'smtp_password': smtp_password,
        'smtp_use_ssl': smtp_use_ssl
    }


def load_adobe_config() -> dict:
    """
    加载 Adobe UMAPI 环境变量配置
    
    Returns:
        dict: 包含所有 Adobe 配置项的字典
        
    Raises:
        ValueError: 如果必需配置项缺失
    """
    # 加载 .env 文件
    load_dotenv()
    
    # 必需配置项
    adobe_client_id = os.getenv('ADOBE_CLIENT_ID')
    adobe_client_secret = os.getenv('ADOBE_CLIENT_SECRET')
    adobe_org_id = os.getenv('ADOBE_ORG_ID')
    
    # 验证必需配置项
    if not adobe_client_id:
        raise ValueError("ADOBE_CLIENT_ID 配置缺失")
    if not adobe_client_secret:
        raise ValueError("ADOBE_CLIENT_SECRET 配置缺失")
    if not adobe_org_id:
        raise ValueError("ADOBE_ORG_ID 配置缺失")
    
    # 可选配置项（带默认值）
    adobe_token_endpoint = os.getenv('ADOBE_TOKEN_ENDPOINT', 'https://ims-na1.adobelogin.com/ims/token/v3')
    adobe_scope = os.getenv('ADOBE_SCOPE', 'openid,AdobeID,user_management_sdk')
    adobe_api_base_url = os.getenv('ADOBE_API_BASE_URL', 'https://usermanagement.adobe.io/v2/usermanagement')
    
    # 产品配置（可选）
    adobe_product_cc_all_apps = os.getenv('ADOBE_PRODUCT_CC_ALL_APPS', 'Creative Cloud All Apps')
    adobe_profile_cc_all_apps = os.getenv('ADOBE_PROFILE_CC_ALL_APPS', 'Default CC All Apps')
    adobe_product_photoshop = os.getenv('ADOBE_PRODUCT_PHOTOSHOP', 'Photoshop')
    adobe_profile_photoshop = os.getenv('ADOBE_PROFILE_PHOTOSHOP', 'Default Photoshop')
    adobe_product_acrobat = os.getenv('ADOBE_PRODUCT_ACROBAT', 'Acrobat Pro DC')
    adobe_profile_acrobat = os.getenv('ADOBE_PROFILE_ACROBAT', 'Default Acrobat Pro DC')
    
    # 默认域名（用于自动补全邮箱）
    # 说明：如果用户只输入用户名（如 "user01"），系统会自动补全为 "user01@{ADOBE_DEFAULT_DOMAIN}"
    # 如果用户输入完整邮箱（如 "user01@example.com"），则直接使用，不进行补全
    # 此配置用于简化用户输入，参考 Office 365 模块的实现方式
    adobe_default_domain = os.getenv('ADOBE_DEFAULT_DOMAIN', 'example.com')
    
    return {
        'adobe_client_id': adobe_client_id,
        'adobe_client_secret': adobe_client_secret,
        'adobe_org_id': adobe_org_id,
        'adobe_token_endpoint': adobe_token_endpoint,
        'adobe_scope': adobe_scope,
        'adobe_api_base_url': adobe_api_base_url,
        'adobe_product_cc_all_apps': adobe_product_cc_all_apps,
        'adobe_profile_cc_all_apps': adobe_profile_cc_all_apps,
        'adobe_product_photoshop': adobe_product_photoshop,
        'adobe_profile_photoshop': adobe_profile_photoshop,
        'adobe_product_acrobat': adobe_product_acrobat,
        'adobe_profile_acrobat': adobe_profile_acrobat,
        'adobe_default_domain': adobe_default_domain
    }


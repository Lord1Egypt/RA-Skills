"""
用户管理核心模块
负责用户的创建、删除和密码重置
"""
import logging
from app.providers.office365.graph_client import GraphAPIError
from app.providers.office365.email_sender import EmailSender, convert_email_domain

logger = logging.getLogger(__name__)


class UserManager:
    """管理 Microsoft 365 用户"""
    
    def __init__(self, graph_client, license_manager, default_password: str, default_domain: str = None,
                 notification_config: dict = None, smtp_config: dict = None):
        """
        初始化 UserManager
        
        Args:
            graph_client: GraphClient 实例
            license_manager: LicenseManager 实例
            default_password: 默认密码
            default_domain: 默认域名（如 example.partner.onmschina.cn）
            notification_config: 邮件通知配置字典，包含 enabled, from_email, bcc_emails, email_domain
            smtp_config: SMTP 配置字典，包含 smtp_host, smtp_port, smtp_username, smtp_password, smtp_use_ssl
        """
        self.graph_client = graph_client
        self.license_manager = license_manager
        self.default_password = default_password
        self.default_domain = default_domain
        self.notification_config = notification_config or {}
        self.smtp_config = smtp_config or {}
        
        # 初始化邮件发送器（如果配置了 SMTP）
        self.email_sender = None
        if self.smtp_config.get('smtp_host'):
            try:
                logger.info(f"初始化邮件发送器: SMTP_HOST={self.smtp_config.get('smtp_host')}, SMTP_USERNAME={self.smtp_config.get('smtp_username')}")
                self.email_sender = EmailSender(self.smtp_config)
                logger.info(f"✅ 邮件发送器初始化成功")
            except Exception as e:
                logger.error(f"❌ 初始化邮件发送器失败: {str(e)}")
                logger.exception("邮件发送器初始化异常详情:")
        else:
            logger.warning(f"SMTP 配置不完整，无法初始化邮件发送器")
            logger.warning(f"SMTP 配置: {self.smtp_config}")
    
    def _normalize_user_identifier(self, user_identifier: str) -> str:
        """
        规范化用户标识符，如果只提供用户名则自动添加默认域名
        
        Args:
            user_identifier: 用户标识符（用户名或完整邮箱）
        
        Returns:
            str: 完整的用户主体名称
        """
        # 如果已经包含 @ 符号，说明是完整邮箱，直接返回
        if '@' in user_identifier:
            return user_identifier
        
        # 如果没有 @ 符号且配置了默认域名，则添加域名后缀
        if self.default_domain:
            return f"{user_identifier}@{self.default_domain}"
        
        # 如果没有默认域名，返回原值（可能是 user ID）
        return user_identifier
    
    def create_user(self, display_name: str, mail_nickname: str, user_principal_name: str,
                    force_change_password: bool = False, sku_part_number: str = None,
                    sku_id: str = None, **kwargs) -> dict:
        """
        创建用户并自动分配许可证
        
        Args:
            display_name: 显示名称
            mail_nickname: 邮件别名
            user_principal_name: 用户主体名称（登录名，如果只提供用户名会自动添加默认域名）
            force_change_password: 是否强制首次登录修改密码
            **kwargs: 其他可选用户属性（givenName, surname, jobTitle, department 等）
        
        Returns:
            dict: 包含用户信息和许可证分配结果的对象
        """
        # 规范化用户主体名称（自动添加域名后缀）
        user_principal_name = self._normalize_user_identifier(user_principal_name)
        
        # 构建用户创建数据
        user_data = {
            'accountEnabled': True,
            'displayName': display_name,
            'mailNickname': mail_nickname,
            'userPrincipalName': user_principal_name,
            'passwordProfile': {
                'password': self.default_password,
                'forceChangePasswordNextSignIn': force_change_password
            }
        }
        
        # 添加可选字段
        optional_fields = ['givenName', 'surname', 'jobTitle', 'department', 
                          'usageLocation', 'officeLocation', 'mobilePhone']
        for field in optional_fields:
            if field in kwargs:
                user_data[field] = kwargs[field]
        
        logger.info(f"创建用户: {user_principal_name}")
        
        # 创建用户
        try:
            user = self.graph_client.create_user(user_data)
            user_id = user.get('id')
            logger.info(f"成功创建用户: {user_principal_name} (ID: {user_id})")
        except Exception as e:
            logger.error(f"创建用户失败: {str(e)}")
            raise
        
        # 自动分配许可证
        license_result = None
        try:
            license_result = self.license_manager.assign_license_to_user(
                user_id,
                sku_id=sku_id,
                sku_part_number=sku_part_number
            )
            logger.info(f"成功为用户 {user_principal_name} 分配许可证")
        except Exception as e:
            logger.warning(f"为用户 {user_principal_name} 分配许可证失败: {str(e)}")
            # 许可证分配失败不影响用户创建，只记录警告
        
        # 发送邮件通知（如果启用）
        email_sent = False
        if self.notification_config.get('enabled'):
            logger.info(f"邮件通知已启用，准备发送用户创建通知")
            try:
                self._send_creation_notification(user, user_principal_name)
                email_sent = True
                logger.info(f"✅ 成功发送用户创建通知邮件")
            except Exception as e:
                logger.error(f"❌ 发送邮件通知失败: {str(e)}")
                logger.exception("邮件发送异常详情:")
                # 邮件发送失败不影响用户创建，只记录错误
        else:
            logger.info(f"邮件通知未启用（NOTIFICATION_ENABLED=false）")
        
        return {
            'user': user,
            'license_assigned': license_result is not None,
            'license_result': license_result,
            'email_sent': email_sent
        }
    
    def _send_creation_notification(self, user: dict, user_principal_name: str):
        """
        发送用户创建通知邮件（使用 SMTP）
        
        Args:
            user: 用户对象
            user_principal_name: 用户主体名称（如 testuser01@example.partner.onmschina.cn）
        """
        logger.info(f"准备发送用户创建通知邮件: {user_principal_name}")
        
        from_email = self.notification_config.get('from_email')
        if not from_email:
            logger.warning("未配置发件人邮箱，跳过邮件通知")
            return
        
        if not self.email_sender:
            logger.warning("邮件发送器未初始化，跳过邮件通知")
            logger.warning(f"SMTP 配置: host={self.smtp_config.get('smtp_host')}, username={self.smtp_config.get('smtp_username')}")
            return
        
        # 转换收件人邮箱域名
        # 例如：testuser01@example.partner.onmschina.cn -> testuser01@目标域名
        email_domain = self.notification_config.get('email_domain', '')
        if not email_domain:
            logger.warning("未配置 NOTIFICATION_EMAIL_DOMAIN，使用原始邮箱地址")
            to_email = user_principal_name
        else:
            to_email = convert_email_domain(user_principal_name, email_domain)
        to_recipients = [to_email]
        
        # 获取密送列表
        bcc_recipients = self.notification_config.get('bcc_emails', [])
        
        # 构建邮件内容
        display_name = user.get('displayName', user_principal_name)
        subject = f"欢迎加入 - 您的 Office 365 账户已创建"
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, 'Microsoft YaHei', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0078d4; margin-top: 0;">欢迎加入 Office 365！</h2>
                <p>尊敬的 {display_name}，</p>
                <p>您的 Office 365 账户已成功创建，现在您可以开始使用 Microsoft 365 的各项服务了。</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #0078d4;">
                    <p style="margin-top: 0; font-weight: bold; color: #0078d4;">账户信息</p>
                    <ul style="list-style: none; padding: 0; margin: 10px 0;">
                        <li style="margin: 10px 0; padding: 5px 0;"><strong>登录邮箱：</strong>{user_principal_name}</li>
                        <li style="margin: 10px 0; padding: 5px 0;"><strong>初始密码：</strong>{self.default_password}</li>
                        <li style="margin: 10px 0; padding: 5px 0;"><strong>显示名称：</strong>{display_name}</li>
                    </ul>
                </div>
                
                <div style="background-color: #e8f4f8; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin-top: 0; font-weight: bold; color: #0078d4;">登录与下载软件地址</p>
                    <p style="margin: 10px 0;">
                        <a href="https://microsoft365.microsoftonline.cn/apps" 
                           style="color: #0078d4; text-decoration: none; font-weight: bold; font-size: 16px;">
                            https://microsoft365.microsoftonline.cn/apps
                        </a>
                    </p>
                    <p style="margin: 10px 0; color: #666; font-size: 14px;">
                        您可以通过此地址登录 Office 365 并下载 Office 办公软件（Word、Excel、PowerPoint 等）。
                    </p>
                </div>
                
                <div style="background-color: #fff4e6; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ff9800;">
                    <p style="margin-top: 0; font-weight: bold; color: #d83b01;">重要提示</p>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li style="margin: 8px 0;">首次登录时，系统会要求您修改密码，请设置一个强密码（建议包含大小写字母、数字和特殊字符）</li>
                        <li style="margin: 8px 0;">请妥善保管您的登录凭据，不要与他人分享</li>
                        <li style="margin: 8px 0;">建议在首次登录后立即下载并安装 Office 办公软件</li>
                        <li style="margin: 8px 0;">如有任何问题或需要技术支持，请联系 IT 部门</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px;">祝您工作愉快！</p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #666; font-size: 12px; text-align: center; margin: 0;">此邮件由系统自动发送，请勿回复。</p>
            </div>
        </body>
        </html>
        """
        
        # 使用 SMTP 发送邮件
        try:
            logger.info(f"发送邮件: 从 {from_email} 到 {to_recipients}, 密送: {bcc_recipients}")
            self.email_sender.send_email(
                from_email=from_email,
                to_recipients=to_recipients,
                subject=subject,
                body=body_html,
                bcc_recipients=bcc_recipients if bcc_recipients else None,
                body_type='html'
            )
            logger.info(f"成功发送用户创建通知邮件")
        except Exception as e:
            logger.error(f"发送用户创建通知邮件失败: {str(e)}")
            raise
    
    def _send_deletion_notification(self, user_principal_name: str, user_info: dict = None):
        """
        发送用户删除通知邮件（使用 SMTP）
        
        Args:
            user_principal_name: 用户主体名称（如 testuser01@example.partner.onmschina.cn）
            user_info: 用户信息（可选）
        """
        logger.info(f"准备发送用户删除通知邮件: {user_principal_name}")
        
        from_email = self.notification_config.get('from_email')
        if not from_email:
            logger.warning("未配置发件人邮箱，跳过邮件通知")
            return
        
        if not self.email_sender:
            logger.warning("邮件发送器未初始化，跳过邮件通知")
            logger.warning(f"SMTP 配置: host={self.smtp_config.get('smtp_host')}, username={self.smtp_config.get('smtp_username')}")
            return
        
        # 转换收件人邮箱域名（用于通知 IT 部门）
        # 注意：用户已被删除，所以邮件发送给 IT 部门
        email_domain = self.notification_config.get('email_domain', '')
        if not email_domain:
            logger.warning("未配置 NOTIFICATION_EMAIL_DOMAIN，使用原始邮箱地址")
            to_email = user_principal_name
        else:
            to_email = convert_email_domain(user_principal_name, email_domain)
        to_recipients = [to_email]
        
        # 获取密送列表
        bcc_recipients = self.notification_config.get('bcc_emails', [])
        
        # 构建邮件内容
        display_name = user_info.get('displayName', user_principal_name) if user_info else user_principal_name
        subject = f"Office 365 用户账户已删除 - {display_name}"
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, 'Microsoft YaHei', sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #d83b01;">Office 365 用户账户删除通知</h2>
                <p>您好，</p>
                <p>以下 Office 365 用户账户已被成功删除：</p>
                <div style="background-color: #fff4e6; padding: 15px; border-left: 4px solid #ff9800; border-radius: 5px; margin: 20px 0;">
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin: 10px 0;"><strong>用户邮箱：</strong>{user_principal_name}</li>
                        <li style="margin: 10px 0;"><strong>显示名称：</strong>{display_name}</li>
                    </ul>
                </div>
                <p><strong>删除原因：</strong></p>
                <p style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                    经系统检测，该账户长期未激活，已有 90 天未登录。出于成本考虑，我们已对该账号进行回收处理。
                </p>
                <p><strong>删除时间：</strong>{self._get_current_time()}</p>
                <p><strong>说明：</strong></p>
                <ul>
                    <li>该账户的所有 Office 365 服务已停止</li>
                    <li>相关数据和文件已无法访问</li>
                    <li>如有疑问或需要恢复账户，请联系 IT 部门</li>
                </ul>
                <p style="margin-top: 20px;">
                    <strong>如有需要，请重新申请：</strong>
                    <a href="https://example.com/apply" 
                       style="color: #0078d4; text-decoration: none; font-weight: bold;">
                        https://example.com/apply
                    </a>
                </p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #666; font-size: 12px; text-align: center;">此邮件由系统自动发送，请勿回复。</p>
            </div>
        </body>
        </html>
        """
        
        # 使用 SMTP 发送邮件
        try:
            logger.info(f"发送邮件: 从 {from_email} 到 {to_recipients}, 密送: {bcc_recipients}")
            self.email_sender.send_email(
                from_email=from_email,
                to_recipients=to_recipients,
                subject=subject,
                body=body_html,
                bcc_recipients=bcc_recipients if bcc_recipients else None,
                body_type='html'
            )
            logger.info(f"成功发送用户删除通知邮件")
        except Exception as e:
            logger.error(f"发送用户删除通知邮件失败: {str(e)}")
            raise
    
    def _send_password_reset_notification(self, user_principal_name: str, new_password: str, 
                                         force_change_password: bool):
        """
        发送密码重置通知邮件（使用 SMTP）
        
        Args:
            user_principal_name: 用户主体名称（如 testuser01@example.partner.onmschina.cn）
            new_password: 新密码
            force_change_password: 是否强制首次登录修改密码
        """
        logger.info(f"准备发送密码重置通知邮件: {user_principal_name}")
        
        from_email = self.notification_config.get('from_email')
        if not from_email:
            logger.warning("未配置发件人邮箱，跳过邮件通知")
            return
        
        if not self.email_sender:
            logger.warning("邮件发送器未初始化，跳过邮件通知")
            logger.warning(f"SMTP 配置: host={self.smtp_config.get('smtp_host')}, username={self.smtp_config.get('smtp_username')}")
            return
        
        # 先获取用户信息
        try:
            user = self.graph_client.get_user(user_principal_name)
        except Exception as e:
            logger.warning(f"获取用户信息失败: {str(e)}")
            user = {}
        
        # 转换收件人邮箱域名
        email_domain = self.notification_config.get('email_domain', '')
        if not email_domain:
            logger.warning("未配置 NOTIFICATION_EMAIL_DOMAIN，使用原始邮箱地址")
            to_email = user_principal_name
        else:
            to_email = convert_email_domain(user_principal_name, email_domain)
        to_recipients = [to_email]
        
        # 获取密送列表
        bcc_recipients = self.notification_config.get('bcc_emails', [])
        
        # 构建邮件内容
        display_name = user.get('displayName', user_principal_name)
        subject = f"密码重置通知 - 您的 Office 365 账户密码已重置"
        
        password_change_note = ""
        if force_change_password:
            password_change_note = "<li><strong>重要：</strong>首次登录时，系统会要求您修改密码</li>"
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, 'Microsoft YaHei', sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0078d4;">Office 365 密码重置通知</h2>
                <p>尊敬的 {display_name}，</p>
                <p>您的 Office 365 账户密码已成功重置，详细信息如下：</p>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin: 10px 0;"><strong>登录邮箱：</strong>{user_principal_name}</li>
                        <li style="margin: 10px 0;"><strong>新密码：</strong>{new_password}</li>
                        <li style="margin: 10px 0;"><strong>显示名称：</strong>{display_name}</li>
                    </ul>
                </div>
                <p><strong>重要提示：</strong></p>
                <ul>
                    {password_change_note}
                    <li>请妥善保管您的登录凭据，不要与他人分享</li>
                    <li>建议定期修改密码以确保账户安全</li>
                    <li>如有任何问题，请联系 IT 部门</li>
                </ul>
                <p style="margin-top: 20px;">
                    <strong>登录地址：</strong>
                    <a href="https://microsoft365.microsoftonline.cn/apps" style="color: #0078d4; text-decoration: none;">
                        https://microsoft365.microsoftonline.cn/apps
                    </a>
                </p>
                <p style="margin-top: 20px;">祝您工作愉快！</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #666; font-size: 12px; text-align: center;">此邮件由系统自动发送，请勿回复。</p>
            </div>
        </body>
        </html>
        """
        
        # 使用 SMTP 发送邮件
        try:
            logger.info(f"发送邮件: 从 {from_email} 到 {to_recipients}, 密送: {bcc_recipients}")
            self.email_sender.send_email(
                from_email=from_email,
                to_recipients=to_recipients,
                subject=subject,
                body=body_html,
                bcc_recipients=bcc_recipients if bcc_recipients else None,
                body_type='html'
            )
            logger.info(f"成功发送密码重置通知邮件")
        except Exception as e:
            logger.error(f"发送密码重置通知邮件失败: {str(e)}")
            raise
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def delete_user(self, user_identifier: str) -> bool:
        """
        删除用户
        
        Args:
            user_identifier: 用户标识符（用户名会自动添加默认域名，或完整 userPrincipalName，或 user ID）
        
        Returns:
            bool: 成功返回 True
        
        Raises:
            GraphAPIError: 如果用户不存在或删除失败
        """
        # 规范化用户标识符（自动添加域名后缀）
        user_identifier = self._normalize_user_identifier(user_identifier)
        
        logger.info(f"删除用户: {user_identifier}")
        
        # 先获取用户信息（用于邮件通知）
        user_info = None
        try:
            user_info = self.graph_client.get_user(user_identifier)
        except Exception as e:
            logger.warning(f"获取用户信息失败（用于邮件通知）: {str(e)}")
        
        # 直接尝试删除用户（不先查询，避免权限问题）
        # Graph API 支持使用 userPrincipalName 或 user ID 直接删除
        try:
            result = self.graph_client.delete_user(user_identifier)
            logger.info(f"成功删除用户: {user_identifier}")
            
            # 发送删除通知邮件（如果启用）
            if result and self.notification_config.get('enabled'):
                logger.info(f"邮件通知已启用，准备发送用户删除通知")
                try:
                    self._send_deletion_notification(user_identifier, user_info)
                    logger.info(f"✅ 成功发送用户删除通知邮件")
                except Exception as e:
                    logger.error(f"❌ 发送删除通知邮件失败: {str(e)}")
                    logger.exception("邮件发送异常详情:")
                    # 邮件发送失败不影响删除操作
            else:
                if not self.notification_config.get('enabled'):
                    logger.info(f"邮件通知未启用（NOTIFICATION_ENABLED=false）")
            
            return result
        except Exception as e:
            # 检查是否是 404 错误（用户不存在）
            if hasattr(e, 'status_code') and e.status_code == 404:
                logger.error(f"用户不存在: {user_identifier}")
                raise GraphAPIError(f"用户不存在: {user_identifier}", status_code=404) from e
            else:
                logger.error(f"删除用户失败: {str(e)}")
                raise
    
    def reset_password(self, user_identifier: str, new_password: str = None,
                      force_change_password: bool = True) -> dict:
        """
        重置用户密码
        
        Args:
            user_identifier: 用户标识符（用户名会自动添加默认域名，或完整 userPrincipalName，或 user ID）
            new_password: 新密码，如果为 None 则使用默认密码
            force_change_password: 是否强制下次登录修改密码
        
        Returns:
            dict: 更新后的用户对象（如果 API 返回）
        """
        # 规范化用户标识符（自动添加域名后缀）
        user_identifier = self._normalize_user_identifier(user_identifier)
        
        if new_password is None:
            new_password = self.default_password
        
        logger.info(f"重置用户密码: {user_identifier}")
        
        # 重要：清除 token 缓存，强制重新获取 client_credentials token
        # 原因：如果应用权限的 Owner 发生变化，或者管理员重新授予了同意，
        # 旧的 token 不会包含新的权限，必须重新获取
        self.graph_client.token_manager.clear_token_cache()
        logger.info("已清除 token 缓存，将重新获取访问令牌（确保包含最新权限）")
        
        # 先获取用户信息，使用 user ID 而不是 userPrincipalName
        # 某些情况下使用 userPrincipalName 可能会遇到权限问题
        try:
            # 这会触发重新获取 token（因为缓存已清除）
            user = self.graph_client.get_user(user_identifier)
            user_id = user.get('id')
            if not user_id:
                raise ValueError(f"无法获取用户 ID: {user_identifier}")
            logger.info(f"获取到用户 ID: {user_id}")
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            raise
        
        # 构建密码更新数据
        password_data = {
            'passwordProfile': {
                'password': new_password,
                'forceChangePasswordNextSignIn': force_change_password
            }
        }
        
        try:
            # 重要：在 PATCH 请求前再次清除 token 缓存并重新获取
            # 确保使用最新的权限（特别是如果 Owner 权限刚更新）
            self.graph_client.token_manager.clear_token_cache()
            logger.info("PATCH 请求前再次清除 token 缓存，确保使用最新权限")
            
            # 使用 user ID 而不是 userPrincipalName 来更新密码
            result = self.graph_client.update_user(user_id, password_data)
            logger.info(f"成功重置用户密码: {user_identifier} (ID: {user_id})")
            
            # 发送密码重置通知邮件（如果启用）
            # 注意：PATCH 请求成功时可能返回空字典（204 No Content），所以检查 result is not None
            if result is not None and self.notification_config.get('enabled'):
                logger.info(f"邮件通知已启用，准备发送密码重置通知")
                try:
                    self._send_password_reset_notification(user_identifier, new_password, force_change_password)
                    logger.info(f"✅ 成功发送密码重置通知邮件")
                except Exception as e:
                    logger.error(f"❌ 发送密码重置通知邮件失败: {str(e)}")
                    logger.exception("邮件发送异常详情:")
                    # 邮件发送失败不影响密码重置操作
            else:
                if not self.notification_config.get('enabled'):
                    logger.info(f"邮件通知未启用（NOTIFICATION_ENABLED=false）")
                elif result is None:
                    logger.warning("重置密码返回 None，跳过邮件通知")
            
            return result
        except Exception as e:
            logger.error(f"重置密码失败: {str(e)}")
            raise

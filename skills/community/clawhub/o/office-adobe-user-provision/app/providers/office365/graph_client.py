"""
Microsoft Graph API 客户端模块
封装所有 Graph API 调用
"""
import requests
import logging

logger = logging.getLogger(__name__)


class GraphAPIError(Exception):
    """Graph API 调用错误"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class GraphClient:
    """Microsoft Graph API 客户端"""
    
    def __init__(self, token_manager, base_url: str):
        """
        初始化 GraphClient
        
        Args:
            token_manager: TokenManager 实例
            base_url: Graph API 基础 URL
        """
        self.token_manager = token_manager
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """
        通用 HTTP 请求方法
        
        Args:
            method: HTTP 方法 (GET, POST, PATCH, DELETE)
            endpoint: API 端点（不包含基础 URL）
            data: 请求体数据（字典，将自动转换为 JSON）
        
        Returns:
            dict: 响应 JSON 数据，如果是 204 响应则返回空字典
        
        Raises:
            GraphAPIError: 如果请求失败
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # 获取访问令牌
        token = self.token_manager.get_access_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data)
            elif method.upper() == 'PATCH':
                response = self.session.patch(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise GraphAPIError(f"不支持的 HTTP 方法: {method}")
            
            # 处理 204 No Content 响应
            if response.status_code == 204:
                logger.info(f"{method} {endpoint} - 成功 (204)")
                return {}
            
            # 检查错误状态
            if not response.ok:
                error_detail = {}
                try:
                    error_detail = response.json()
                except:
                    error_detail = {'error': response.text}
                
                error_msg = f"API 调用失败: {method} {endpoint} - HTTP {response.status_code}"
                logger.error(f"{error_msg} - {error_detail}")
                raise GraphAPIError(
                    error_msg,
                    status_code=response.status_code,
                    response=error_detail
                )
            
            # 解析 JSON 响应
            result = response.json()
            logger.info(f"{method} {endpoint} - 成功")
            return result
            
        except GraphAPIError:
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"请求异常: {method} {endpoint} - {str(e)}"
            logger.error(error_msg)
            raise GraphAPIError(error_msg) from e
    
    def create_user(self, user_data: dict) -> dict:
        """
        创建用户
        
        Args:
            user_data: 用户数据字典
        
        Returns:
            dict: 创建的用户对象
        """
        return self._make_request('POST', '/users', user_data)
    
    def get_user(self, user_identifier: str) -> dict:
        """
        查询用户
        
        Args:
            user_identifier: 用户标识符（userPrincipalName 或 user ID）
        
        Returns:
            dict: 用户对象
        """
        return self._make_request('GET', f'/users/{user_identifier}')
    
    def update_user(self, user_identifier: str, user_data: dict) -> dict:
        """
        更新用户属性
        
        Args:
            user_identifier: 用户标识符
            user_data: 要更新的用户数据
        
        Returns:
            dict: 更新后的用户对象（如果 API 返回）
        """
        return self._make_request('PATCH', f'/users/{user_identifier}', user_data)
    
    def delete_user(self, user_identifier: str) -> bool:
        """
        删除用户
        
        Args:
            user_identifier: 用户标识符
        
        Returns:
            bool: 成功返回 True
        """
        self._make_request('DELETE', f'/users/{user_identifier}')
        return True
    
    def get_users(self, select: str = None, top: int = None) -> list:
        """
        获取用户列表（支持分页）
        
        Args:
            select: 要选择的字段，如 "id,displayName,userPrincipalName,mail"
            top: 每页返回的最大数量（默认 API 限制）
        
        Returns:
            list: 用户对象列表
        """
        all_users = []
        endpoint = '/users'
        
        # 构建查询参数
        params = []
        if select:
            params.append(f'$select={select}')
        if top:
            params.append(f'$top={top}')
        
        if params:
            endpoint += '?' + '&'.join(params)
        
        # 处理分页
        next_link = None
        page_count = 0
        
        while True:
            if next_link:
                # 使用完整 URL（包含基础 URL）
                url = next_link
                token = self.token_manager.get_access_token()
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                response = self.session.get(url, headers=headers)
                
                if not response.ok:
                    error_detail = {}
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = {'error': response.text}
                    raise GraphAPIError(
                        f"API 调用失败: GET {next_link} - HTTP {response.status_code}",
                        status_code=response.status_code,
                        response=error_detail
                    )
                
                result = response.json()
            else:
                # 第一次请求
                result = self._make_request('GET', endpoint)
            
            users = result.get('value', [])
            all_users.extend(users)
            page_count += 1
            logger.info(f"获取用户列表 - 第 {page_count} 页，本页 {len(users)} 个用户，累计 {len(all_users)} 个用户")
            
            # 检查是否有下一页
            next_link = result.get('@odata.nextLink')
            if not next_link:
                break
        
        logger.info(f"获取用户列表完成，共 {len(all_users)} 个用户")
        return all_users
    
    def get_subscribed_skus(self) -> list:
        """
        获取订阅的 SKU 列表
        
        Returns:
            list: SKU 列表
        """
        response = self._make_request('GET', '/subscribedSkus')
        return response.get('value', [])
    
    def assign_license(self, user_id: str, add_licenses: list, remove_licenses: list = None) -> dict:
        """
        为用户分配或移除许可证
        
        Args:
            user_id: 用户 ID
            add_licenses: 要添加的许可证列表，格式: [{"skuId": "...", "disabledPlans": []}]
            remove_licenses: 要移除的许可证 ID 列表，格式: ["sku-id-1", "sku-id-2"]
        
        Returns:
            dict: 更新后的用户对象
        """
        data = {
            'addLicenses': add_licenses,
            'removeLicenses': remove_licenses if remove_licenses else []  # API 要求必须提供此参数
        }
        
        return self._make_request('POST', f'/users/{user_id}/assignLicense', data)
    
    def send_mail(self, from_email: str, to_recipients: list, subject: str, body: str, 
                  cc_recipients: list = None, body_type: str = 'HTML') -> dict:
        """
        发送邮件
        
        Args:
            from_email: 发件人邮箱地址（必须是应用程序有权限使用的邮箱）
            to_recipients: 收件人列表，格式: ["user1@example.com", "user2@example.com"]
            subject: 邮件主题
            body: 邮件正文
            cc_recipients: 抄送列表（可选），格式: ["cc1@example.com"]
            body_type: 正文类型，'HTML' 或 'Text'，默认为 'HTML'
        
        Returns:
            dict: API 响应（通常为空）
        
        Note:
            需要 Mail.Send 权限（应用程序权限或委派权限）
            发件人邮箱必须是应用程序有权限使用的邮箱
        """
        message = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': body_type,
                    'content': body
                },
                'toRecipients': [{'emailAddress': {'address': email}} for email in to_recipients]
            }
        }
        
        # 添加抄送
        if cc_recipients:
            message['message']['ccRecipients'] = [
                {'emailAddress': {'address': email}} for email in cc_recipients
            ]
        
        logger.info(f"发送邮件: 从 {from_email} 到 {to_recipients}")
        return self._make_request('POST', f'/users/{from_email}/sendMail', message)


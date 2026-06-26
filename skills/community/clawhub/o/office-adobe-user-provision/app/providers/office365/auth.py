"""
Token 认证管理模块
负责获取和管理 Microsoft Graph API 的访问令牌
"""
import time
import requests
import logging

logger = logging.getLogger(__name__)


class TokenError(Exception):
    """Token 获取或验证错误"""
    pass


class TokenManager:
    """管理 Microsoft Graph API 访问令牌"""
    
    def __init__(self, config: dict):
        """
        初始化 TokenManager
        
        Args:
            config: 配置字典，包含 client_id, client_secret, token_endpoint 等
        """
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.token_endpoint = config['token_endpoint']
        self.scope = "https://microsoftgraph.chinacloudapi.cn/.default"
        
        # Token 缓存
        self._token = None
        self._expires_at = 0
    
    def clear_token_cache(self):
        """清除 token 缓存，强制重新获取"""
        logger.info("清除 token 缓存")
        self._token = None
        self._expires_at = 0
    
    def get_access_token(self) -> str:
        """
        获取有效的访问令牌
        
        Returns:
            str: 访问令牌
            
        Raises:
            TokenError: 如果获取令牌失败
        """
        # 检查缓存是否有效
        if self._token and self._is_token_valid({'expires_in': self._expires_at - int(time.time())}):
            logger.info("使用缓存的访问令牌")
            return self._token
        
        # 请求新令牌
        logger.info("请求新的访问令牌")
        token_data = self._request_token()
        self._token = token_data['access_token']
        # 提前 5 分钟刷新
        expires_in = token_data.get('expires_in', 3600) - 300
        self._expires_at = int(time.time()) + expires_in
        
        return self._token
    
    def _request_token(self) -> dict:
        """
        请求新的访问令牌（使用 client_credentials 流程）
        
        重要说明：
        - 使用 grant_type=client_credentials 获取 Application 权限
        - scope 必须设置为 https://microsoftgraph.chinacloudapi.cn/.default
        - 如果应用权限的 Owner 发生变化或管理员重新授予了同意，
          必须清除旧 token 缓存并重新获取，否则新权限不会生效
        
        Returns:
            dict: 包含 access_token 和 expires_in 的字典
            
        Raises:
            TokenError: 如果请求失败
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope  # https://microsoftgraph.chinacloudapi.cn/.default
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(self.token_endpoint, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            if 'access_token' not in token_data:
                raise TokenError("响应中缺少 access_token")
            
            logger.info("成功获取访问令牌")
            return token_data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"获取访问令牌失败: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - HTTP {e.response.status_code}"
            logger.error(error_msg)
            raise TokenError(error_msg) from e
    
    def _is_token_valid(self, token_data: dict) -> bool:
        """
        检查令牌是否在有效期内
        
        Args:
            token_data: 包含 expires_in 的字典（用于新令牌）
                       或用于检查缓存令牌的有效性
        
        Returns:
            bool: 令牌是否有效
        """
        # 如果是新令牌数据，检查 expires_in
        if 'expires_in' in token_data:
            return token_data['expires_in'] > 300  # 至少还有 5 分钟
        
        # 检查缓存的过期时间
        return time.time() < self._expires_at


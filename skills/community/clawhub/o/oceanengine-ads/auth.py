"""
巨量广告 OAuth 认证模块
支持测试账户和正式账户认证
"""
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class AuthConfig:
    """认证配置"""
    access_token: str
    refresh_token: Optional[str] = None
    app_id: str = ""
    app_secret: str = ""
    account_id: str = ""
    test_mode: bool = True
    expires_at: Optional[datetime] = None


class OceanEngineAuth:
    """巨量广告OAuth认证管理"""
    
    def __init__(self):
        self.config = self._load_config()
        self.base_url = "https://ad.oceanengine.com"
        self.test_base_url = "https://test-ad.oceanengine.com"
        
    def _load_config(self) -> AuthConfig:
        """加载配置"""
        return AuthConfig(
            access_token=os.getenv("OCEANENGINE_ACCESS_TOKEN", ""),
            refresh_token=os.getenv("OCEANENGINE_REFRESH_TOKEN", ""),
            app_id=os.getenv("OCEANENGINE_APP_ID", ""),
            app_secret=os.getenv("OCEANENGINE_APP_SECRET", ""),
            account_id=os.getenv("OCEANENGINE_ACCOUNT_ID", ""),
            test_mode=os.getenv("OCEANENGINE_TEST_MODE", "true").lower() == "true"
        )
    
    def is_token_valid(self) -> bool:
        """检查token是否有效"""
        if not self.config.access_token:
            return False
            
        if self.config.expires_at and datetime.now() >= self.config.expires_at:
            return False
            
        return True
    
    def refresh_access_token(self) -> Dict:
        """刷新访问token"""
        if not self.config.refresh_token:
            raise ValueError("缺少refresh_token，无法刷新")
            
        url = f"{self._get_base_url()}/oauth/refresh_token/"
        
        try:
            response = requests.post(url, data={
                "grant_type": "refresh_token",
                "refresh_token": self.config.refresh_token,
                "client_id": self.config.app_id,
                "client_secret": self.config.app_secret
            })
            
            if response.status_code == 200:
                data = response.json()
                self.config.access_token = data["access_token"]
                self.config.refresh_token = data.get("refresh_token")
                self.config.expires_at = datetime.now() + timedelta(hours=1)
                
                logger.info("Token刷新成功")
                return data
            else:
                logger.error(f"Token刷新失败: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Token刷新异常: {str(e)}")
            return {}
    
    def get_auth_url(self) -> str:
        """获取授权URL"""
        client_id = self.config.app_id
        redirect_uri = "http://localhost:3000/callback"
        scope = "ad_read ad_write"
        
        return (f"{self._get_base_url()}/oauth/authorize/"
                f"?response_type=code"
                f"&client_id={client_id}"
                f"&redirect_uri={redirect_uri}"
                f"&scope={scope}")
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """授权码换取token"""
        url = f"{self._get_base_url()}/oauth/access_token/"
        
        try:
            response = requests.post(url, data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.config.app_id,
                "client_secret": self.config.app_secret,
                "redirect_uri": "http://localhost:3000/callback"
            })
            
            if response.status_code == 200:
                data = response.json()
                self.config.access_token = data["access_token"]
                self.config.refresh_token = data.get("refresh_token")
                self.config.expires_at = datetime.now() + timedelta(hours=1)
                
                logger.info("授权码换取token成功")
                return data
            else:
                logger.error(f"授权码换取token失败: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"授权码换取token异常: {str(e)}")
            return {}
    
    def get_headers(self) -> Dict:
        """获取请求头"""
        if not self.is_token_valid():
            if not self.refresh_access_token():
                raise ValueError("无法获取有效的访问token")
        
        return {
            "Access-Token": self.config.access_token,
            "Content-Type": "application/json"
        }
    
    def get_account_info(self) -> Dict:
        """获取账户信息（测试用）"""
        url = f"{self._get_base_url()}/open_api/v1.0/account/get/"
        
        try:
            response = requests.post(
                url,
                headers=self.get_headers(),
                json={
                    "advertiser_ids": []
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"获取账户信息失败: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"获取账户信息异常: {str(e)}")
            return {}
    
    def test_connection(self) -> Dict:
        """测试连接"""
        try:
            account_info = self.get_account_info()
            
            if account_info and "data" in account_info:
                return {
                    "status": "success",
                    "message": "连接成功",
                    "account_info": account_info,
                    "test_mode": self.config.test_mode
                }
            else:
                return {
                    "status": "error",
                    "message": "连接失败，请检查token和权限",
                    "test_mode": self.config.test_mode
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "test_mode": self.config.test_mode
            }
    
    def _get_base_url(self) -> str:
        """获取API基础URL"""
        if self.config.test_mode:
            return self.test_base_url
        else:
            return self.base_url
    
    def save_config(self) -> None:
        """保存配置到文件"""
        config_data = {
            "access_token": self.config.access_token,
            "refresh_token": self.config.refresh_token,
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret,
            "account_id": self.config.account_id,
            "test_mode": self.config.test_mode,
            "expires_at": self.config.expires_at.isoformat() if self.config.expires_at else None
        }
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)


# 测试用配置（如果需要）
TEST_CONFIG = {
    "test_access_token": "your_test_token",
    "test_app_id": "your_test_app_id",
    "test_app_secret": "your_test_secret",
    "test_account_id": "act_test_123456"
}


if __name__ == "__main__":
    # 测试认证模块
    auth = OceanEngineAuth()
    result = auth.test_connection()
    print("连接测试结果:", result)
    
    if not result["status"] == "success":
        print(f"\n请配置环境变量:")
        print("export OCEANENGINE_ACCESS_TOKEN=your_token")
        print("export OCEANENGINE_APP_ID=your_app_id")
        print("export OCEANENGINE_APP_SECRET=your_app_secret")
        print("\n或者访问以下URL进行授权:")
        print(auth.get_auth_url())
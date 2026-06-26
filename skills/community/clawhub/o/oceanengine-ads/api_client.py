"""
巨量广告API客户端模块
封装所有广告API调用
"""
import json
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from loguru import logger
from auth import OceanEngineAuth, AuthConfig


@dataclass
class CampaignConfig:
    """广告计划配置"""
    name: str
    campaign_type: str
    objective: str
    budget_mode: str
    budget: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    opt_status: str = "ENABLE"


@dataclass
class AdGroupConfig:
    """广告组配置"""
    name: str
    budget: int
    bidding: Dict
    targeting: Dict


@dataclass
class CreativeConfig:
    """创意配置"""
    name: str
    creative_type: str
    creative_material_id: str
    ad_text: str
    landing_page_url: str


class OceanEngineClient:
    """巨量广告API客户端"""
    
    def __init__(self, auth_config: Optional[AuthConfig] = None):
        self.auth = OceanEngineAuth()
        if auth_config:
            self.auth.config = auth_config
        self.base_url = self._get_base_url()
        self.timeout = 30
        
    def _get_base_url(self) -> str:
        """获取API基础URL"""
        return self.auth._get_base_url()
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"
        headers = self.auth.get_headers()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, json=data, timeout=self.timeout)
            else:
                raise ValueError(f"不支持的请求方法: {method}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    logger.debug(f"请求成功: {endpoint}")
                    return result
                else:
                    logger.error(f"API错误: {endpoint}, 错误: {result}")
                    return result
            else:
                logger.error(f"HTTP错误: {endpoint}, 状态: {response.status_code}, 内容: {response.text}")
                return {"code": response.status_code, "message": response.text}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {endpoint}, 错误: {str(e)}")
            return {"code": -1, "message": str(e)}
    
    def get_account_info(self) -> Dict:
        """获取账户信息"""
        endpoint = "/open_api/v1.0/account/get/"
        data = {"advertiser_ids": []}
        return self._make_request("POST", endpoint, data)
    
    def get_campaigns(self, advertiser_id: str, **kwargs) -> Dict:
        """获取广告计划列表"""
        endpoint = "/open_api/v3.0/campaign/get/"
        data = {
            "advertiser_id": advertiser_id,
            **kwargs
        }
        return self._make_request("POST", endpoint, data)
    
    def get_campaign_detail(self, campaign_id: str) -> Dict:
        """获取广告计划详情"""
        endpoint = "/open_api/v3.0/campaign/get/"
        data = {
            "campaign_ids": [campaign_id]
        }
        return self._make_request("POST", endpoint, data)
    
    def create_campaign(self, advertiser_id: str, config: CampaignConfig) -> Dict:
        """创建广告计划"""
        endpoint = "/open_api/v3.0/campaign/create/"
        data = {
            "advertiser_id": advertiser_id,
            "campaign_name": config.name,
            "campaign_type": config.campaign_type,
            "objective": config.objective,
            "budget_mode": config.budget_mode,
            "budget": config.budget,
            "start_time": config.start_time,
            "end_time": config.end_time,
            "opt_status": config.opt_status
        }
        
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        
        return self._make_request("POST", endpoint, data)
    
    def update_campaign(self, campaign_id: str, updates: Dict) -> Dict:
        """更新广告计划"""
        endpoint = "/open_api/v3.0/campaign/update/"
        data = {
            "campaign_ids": [campaign_id],
            **updates
        }
        return self._make_request("POST", endpoint, data)
    
    def update_campaign_status(self, campaign_ids: List[str], opt_status: str) -> Dict:
        """更新广告计划状态"""
        endpoint = "/open_api/v3.0/campaign/update_status/"
        data = {
            "campaign_ids": campaign_ids,
            "opt_status": opt_status
        }
        return self._make_request("POST", endpoint, data)
    
    def get_adgroups(self, campaign_id: str, **kwargs) -> Dict:
        """获取广告组列表"""
        endpoint = "/open_api/v3.0/adgroup/get/"
        data = {
            "campaign_id": campaign_id,
            **kwargs
        }
        return self._make_request("POST", endpoint, data)
    
    def create_adgroup(self, campaign_id: str, config: AdGroupConfig) -> Dict:
        """创建广告组"""
        endpoint = "/open_api/v3.0/adgroup/create/"
        data = {
            "campaign_id": campaign_id,
            "adgroup_name": config.name,
            "budget": config.budget,
            "bidding": config.bidding,
            "targeting": config.targeting
        }
        return self._make_request("POST", endpoint, data)
    
    def update_adgroup(self, adgroup_id: str, updates: Dict) -> Dict:
        """更新广告组"""
        endpoint = "/open_api/v3.0/adgroup/update/"
        data = {
            "adgroup_ids": [adgroup_id],
            **updates
        }
        return self._make_request("POST", endpoint, data)
    
    def get_creatives(self, advertiser_id: str, **kwargs) -> Dict:
        """获取创意列表"""
        endpoint = "/open_api/v3.0/creative/get/"
        data = {
            "advertiser_id": advertiser_id,
            **kwargs
        }
        return self._make_request("POST", endpoint, data)
    
    def create_creative(self, adgroup_id: str, config: CreativeConfig) -> Dict:
        """创建广告创意"""
        endpoint = "/open_api/v3.0/creative/create/"
        data = {
            "adgroup_id": adgroup_id,
            "creative_name": config.name,
            "creative_type": config.creative_type,
            "creative_material_id": config.creative_material_id,
            "ad_text": config.ad_text,
            "landing_page_url": config.landing_page_url
        }
        return self._make_request("POST", endpoint, data)
    
    def get_report(self, advertiser_id: str, report_config: Dict) -> Dict:
        """获取数据报表"""
        endpoint = "/open_api/v3.0/report/get/"
        data = {
            "advertiser_id": advertiser_id,
            **report_config
        }
        return self._make_request("POST", endpoint, data)
    
    def get_campaign_report(self, advertiser_id: str, start_date: str, end_date: str, **kwargs) -> Dict:
        """获取广告计划报表"""
        report_config = {
            "start_date": start_date,
            "end_date": end_date,
            "metrics": ["cost", "impressions", "clicks", "ctr", "cpc", "conversion", "cpa"],
            "dimensions": ["CAMPAIGN"],
            **kwargs
        }
        return self.get_report(advertiser_id, report_config)
    
    def get_adgroup_report(self, advertiser_id: str, start_date: str, end_date: str, **kwargs) -> Dict:
        """获取广告组报表"""
        report_config = {
            "start_date": start_date,
            "end_date": end_date,
            "metrics": ["cost", "impressions", "clicks", "ctr", "cpc", "conversion", "cpa"],
            "dimensions": ["ADGROUP"],
            **kwargs
        }
        return self.get_report(advertiser_id, report_config)
    
    def async_request(self, requests: List[Dict]) -> List[Dict]:
        """异步批量请求"""
        async def _async_request(session, req):
            try:
                async with session.request(
                    method=req['method'],
                    url=f"{self.base_url}{req['endpoint']}",
                    headers=self.auth.get_headers(),
                    json=req.get('data')
                ) as response:
                    return await response.json()
            except Exception as e:
                logger.error(f"异步请求失败: {req['endpoint']}, 错误: {str(e)}")
                return {"code": -1, "message": str(e)}
        
        async def _main():
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                tasks = [_async_request(session, req) for req in requests]
                return await asyncio.gather(*tasks)
        
        return asyncio.run(_main())
    
    def test_api_access(self) -> Dict:
        """测试API访问权限"""
        try:
            # 测试获取账户信息
            result = self.get_account_info()
            return {
                "status": "success" if result.get("code") == 0 else "error",
                "message": "API访问测试成功" if result.get("code") == 0 else f"API访问失败: {result.get('message', '未知错误')}",
                "data": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"API访问异常: {str(e)}",
                "data": None
            }


if __name__ == "__main__":
    # 测试API客户端
    client = OceanEngineClient()
    result = client.test_api_access()
    print("API测试结果:", result)
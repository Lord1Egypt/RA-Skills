"""
自动化投放引擎
智能投放、预算优化、创意轮换
"""
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from loguru import logger
from api_client import OceanEngineClient


@dataclass
class AutomationRule:
    """自动化规则"""
    rule_id: str
    rule_name: str
    rule_type: str  # budget_optimization, creative_rotation, bid_adjustment
    enabled: bool
    config: Dict
    last_run: Optional[datetime] = None
    run_count: int = 0


@dataclass
class AutoLaunchConfig:
    """自动投放配置"""
    campaign_id: str
    launch_immediately: bool
    start_time: Optional[str] = None
    auto_optimization: bool = True
    budget_rules: Optional[Dict] = None
    creative_rotation: bool = False


class OceanEngineAutomation:
    """巨量广告自动化投放引擎"""
    
    def __init__(self):
        self.client = OceanEngineClient()
        self.rules: List[AutomationRule] = []
        self.launch_history: List[Dict] = []
    
    def start_auto_launch(self, config: AutoLaunchConfig) -> Dict:
        """启动自动化投放"""
        logger.info(f"启动自动化投放: {config.campaign_id}")
        
        # 1. 获取广告计划信息
        campaign_info = self.client.get_campaign_detail(config.campaign_id)
        
        if not campaign_info or campaign_info.get("code") != 0:
            return {"status": "error", "message": "广告计划不存在或已删除"}
        
        campaign_data = campaign_info.get("data", {})
        
        # 2. 创建广告组（如果需要）
        adgroup = self._create_auto_adgroup(config, campaign_data)
        
        # 3. 创建广告创意
        creative = self._create_auto_creative(config, adgroup["id"] if adgroup else "")
        
        # 4. 启动广告
        result = self._launch_ad(adgroup["id"], creative["id"])
        
        # 5. 记录历史
        self.launch_history.append({
            "campaign_id": config.campaign_id,
            "launch_time": datetime.now().isoformat(),
            "result": result
        })
        
        if config.auto_optimization:
            self._schedule_optimization(config.campaign_id)
        
        logger.info(f"自动化投放完成: {result}")
        return result
    
    def _create_auto_adgroup(self, config: AutoLaunchConfig, campaign_data: Dict) -> Dict:
        """创建自动化广告组"""
        # 智能预算分配
        total_budget = campaign_data.get("budget", 10000)
        adgroup_budget = int(total_budget * 0.8)  # 80%给广告组
        
        adgroup_config = {
            "adgroup_name": f"自动组_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "budget": adgroup_budget,
            "bidding": {
                "bid_type": "AUTO_BID",
                "bid_price": 0  # 自动出价
            },
            "targeting": self._get_smart_targeting(config)
        }
        
        result = self.client.create_adgroup(config.campaign_id, adgroup_config)
        logger.info(f"创建广告组: {adgroup_config}")
        return result
    
    def _create_auto_creative(self, config: AutoLaunchConfig, adgroup_id: str) -> Dict:
        """创建自动化广告创意"""
        creative_config = {
            "creative_name": f"自动创意_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "creative_type": "IMAGE",
            "creative_material_id": "auto_material_001",  # 需要先上传素材
            "ad_text": self._generate_ad_text(config),
            "landing_page_url": config.landing_page_url if hasattr(config, 'landing_page_url') else "https://example.com"
        }
        
        result = self.client.create_creative(adgroup_id, creative_config)
        logger.info(f"创建创意: {creative_config}")
        return result
    
    def _generate_ad_text(self, config: AutoLaunchConfig) -> str:
        """生成广告文案"""
        templates = {
            "info_flow": "立即体验，限时优惠！",
            "brand_aware": "让更多人知道你的品牌",
            "conversion": "立即行动，享受优惠",
            "engagement": "参与互动，赢取奖品"
        }
        
        return templates.get("info_flow", "新用户专享优惠")
    
    def _launch_ad(self, adgroup_id: str, creative_id: str) -> Dict:
        """启动广告"""
        launch_config = {
            "adgroup_id": adgroup_id,
            "creative_id": creative_id,
            "opt_status": "ENABLE"
        }
        
        result = self.client.create_ad(adgroup_id, launch_config)
        logger.info(f"启动广告: {launch_config}")
        return result
    
    def _get_smart_targeting(self, config: AutoLaunchConfig) -> Dict:
        """获取智能定向配置"""
        # 默认定向策略
        return {
            "gender": ["MALE", "FEMALE"],
            "age": [18, 35],
            "location": {
                "type": "COUNTRY",
                "values": ["CN"]
            },
            "interest": ["科技", "互联网", "移动互联网"]
        }
    
    def _schedule_optimization(self, campaign_id: str):
        """调度优化任务"""
        # 这里可以集成到定时任务系统
        logger.info(f"已为广告 {campaign_id} 调度优化任务")
    
    def batch_launch_campaigns(self, configs: List[AutoLaunchConfig]) -> List[Dict]:
        """批量启动多个广告计划"""
        logger.info(f"批量启动 {len(configs)} 个广告计划")
        
        async def launch_single(config):
            return self.start_auto_launch(config)
        
        # 使用API客户端的异步功能
        results = asyncio.run(launch_single(config) for config in configs)
        
        success_count = sum(1 for r in results if r.get("code") == 0)
        logger.info(f"批量启动完成: {success_count}/{len(results)} 成功")
        
        return results
    
    def get_launch_history(self, campaign_id: Optional[str] = None) -> List[Dict]:
        """获取投放历史"""
        if campaign_id:
            return [h for h in self.launch_history if h["campaign_id"] == campaign_id]
        return self.launch_history
    
    def get_automation_rules(self) -> List[AutomationRule]:
        """获取所有自动化规则"""
        return self.rules
    
    def create_automation_rule(self, rule: AutomationRule) -> Dict:
        """创建自动化规则"""
        self.rules.append(rule)
        logger.info(f"创建自动化规则: {rule.rule_name}")
        return {"status": "success", "message": "规则创建成功"}
    
    def update_automation_rule(self, rule_id: str, updates: Dict) -> Dict:
        """更新自动化规则"""
        for i, rule in enumerate(self.rules):
            if rule.rule_id == rule_id:
                self.rules[i] = rule.__class__(**{**rule.__dict__, **updates})
                logger.info(f"更新自动化规则: {rule_id}")
                return {"status": "success", "message": "规则更新成功"}
        
        return {"status": "error", "message": "规则不存在"}
    
    def delete_automation_rule(self, rule_id: str) -> Dict:
        """删除自动化规则"""
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        logger.info(f"删除自动化规则: {rule_id}")
        return {"status": "success", "message": "规则删除成功"}


# 示例使用
if __name__ == "__main__":
    automation = OceanEngineAutomation()
    
    # 示例：启动自动化投放
    config = AutoLaunchConfig(
        campaign_id="test_campaign_001",
        launch_immediately=True,
        auto_optimization=True
    )
    
    result = automation.start_auto_launch(config)
    print(f"投放结果: {result}")
"""
巨量广告自动化投放主入口
整合所有模块，提供统一的命令行接口
"""
import sys
import json
import argparse
from datetime import datetime
from typing import Optional
from loguru import logger

from auth import OceanEngineAuth
from api_client import OceanEngineClient
from automation import OceanEngineAutomation, AutoLaunchConfig
from optimizer import OceanEngineOptimizer


class OceanEngineMain:
    """巨量广告自动化投放主类"""
    
    def __init__(self):
        self.auth = OceanEngineAuth()
        self.client = OceanEngineClient()
        self.automation = OceanEngineAutomation()
        self.optimizer = OceanEngineOptimizer()
        
    def init(self) -> None:
        """初始化配置"""
        logger.info("初始化巨量广告自动化投放系统")
        
        # 检查认证
        if not self.auth.is_token_valid():
            logger.warning("Token无效，请先进行认证")
            return
        
        # 测试连接
        test_result = self.auth.test_connection()
        if test_result.get("status") != "success":
            logger.error(f"连接测试失败: {test_result.get('message')}")
            return
        
        logger.info("系统初始化完成")
    
    def status(self) -> None:
        """查看系统状态"""
        logger.info("系统状态检查")
        
        # 检查认证
        auth_status = "✅ 已认证" if self.auth.is_token_valid() else "❌ 未认证"
        print(f"\n🔐 认证状态: {auth_status}")
        
        # 测试API连接
        api_status = self.client.test_api_access()
        print(f"🌐 API连接: {api_status.get('message', '未知')}")
        
        # 查看账户信息
        if self.auth.is_token_valid():
            account_info = self.client.get_account_info()
            if account_info and "data" in account_info:
                print(f"\n📊 账户信息:")
                print(f"   账户名称: {account_info['data'].get('name', 'N/A')}")
                print(f"   账户状态: {account_info['data'].get('account_status', 'N/A')}")
                print(f"   货币: {account_info['data'].get('currency', 'N/A')}")
        
        print("\n💡 巨量广告自动化投放系统 v1.0.0 - 乐盟互动出品")
    
    def campaign_list(self, account_id: str) -> None:
        """查询广告计划列表"""
        logger.info(f"查询广告计划列表: {account_id}")
        
        result = self.client.get_campaigns(account_id=account_id)
        
        if result.get("code") == 0:
            campaigns = result.get("data", {}).get("campaign_list", [])
            print(f"\n📋 广告计划列表 (共{len(campaigns)}个):\n")
            
            for i, campaign in enumerate(campaigns[:10], 1):
                print(f"{i}. {campaign.get('name', 'N/A')}")
                print(f"   状态: {campaign.get('status', 'N/A')}")
                print(f"   预算: {campaign.get('budget', 0)/100:.0f}元")
                print(f"   消耗: {campaign.get('cost', 0):.2f}元")
                print()
            
            if len(campaigns) > 10:
                print(f"...还有{len(campaigns)-10}个广告计划未显示")
        else:
            print(f"\n❌ 查询失败: {result.get('message', '未知错误')}")
    
    def campaign_create(self, account_id: str, name: str, budget: int, 
                   objective: str = "CONVERSIONS") -> None:
        """创建广告计划"""
        logger.info(f"创建广告计划: {name}")
        
        config = {
            "campaign_name": name,
            "campaign_type": "FEED",
            "objective": objective,
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": budget * 100,  # 转换为分
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "opt_status": "PAUSED"
        }
        
        result = self.client.create_campaign(account_id, config)
        
        if result.get("code") == 0:
            campaign_id = result.get("data", {}).get("campaign_id", "")
            print(f"\n✅ 广告计划创建成功!")
            print(f"   计划名称: {name}")
            print(f"   计划ID: {campaign_id}")
            print(f"   日预算: {budget}元")
            print(f"   目标: {objective}")
            print(f"   状态: 暂停（PAUSED），请在后台启用")
        else:
            print(f"\n❌ 创建失败: {result.get('message', '未知错误')}")
    
    def auto_launch(self, campaign_id: str) -> None:
        """自动投放"""
        logger.info(f"启动自动投放: {campaign_id}")
        
        config = AutoLaunchConfig(
            campaign_id=campaign_id,
            launch_immediately=True,
            auto_optimization=True
        )
        
        result = self.automation.start_auto_launch(config)
        
        if result.get("code") == 0:
            print(f"\n✅ 自动投放启动成功!")
            print(f"   广告计划ID: {campaign_id}")
            print(f"   投放时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n❌ 投放失败: {result.get('message', '未知错误')}")
    
    def optimize(self, account_id: str, days: int = 7) -> None:
        """优化分析"""
        logger.info(f"执行优化分析: 账户{account_id}, 近{days}天")
        
        # 生成优化报告
        report = self.optimizer.generate_optimization_report(account_id=account_id, 
                                                               period=f"last_{days}d")
        
        print(report)
        
        # 保存报告到文件
        report_file = f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"优化报告已保存: {report_file}")
        print(f"\n💾 报告已保存到: {report_file}")
    
    def batch_launch(self, campaign_ids_file: str) -> None:
        """批量投放"""
        logger.info(f"批量投放: 文件{campaign_ids_file}")
        
        try:
            with open(campaign_ids_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            campaign_ids = [line.strip() for line in lines if line.strip()]
            
            if not campaign_ids:
                print("❌ 文件为空或格式错误")
                return
            
            configs = [AutoLaunchConfig(campaign_id=cid, 
                                     launch_immediately=True, 
                                     auto_optimization=True) 
                      for cid in campaign_ids]
            
            results = self.automation.batch_launch_campaigns(configs)
            
            success_count = sum(1 for r in results if r.get("code") == 0)
            print(f"\n✅ 批量投放完成!")
            print(f"   总数: {len(campaign_ids)}")
            print(f"   成功: {success_count}")
            print(f"   失败: {len(campaign_ids)-success_count}")
            
            # 保存结果
            result_file = f"batch_launch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 结果已保存到: {result_file}")
            
        except FileNotFoundError:
            print("❌ 文件不存在")
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")
    
    def report(self, account_id: str, period: str = "last_7d") -> None:
        """查看报表"""
        logger.info(f"查看报表: 账户{account_id}, 周期{period}")
        
        result = self.client.get_campaign_report(
            account_id=account_id,
            start_date=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            metrics=["cost", "impressions", "clicks", "ctr", "cpc", "conversion", "cpa"]
        )
        
        if result.get("code") == 0:
            campaigns = result.get("data", {}).get("campaign_list", [])
            
            print(f"\n📊 广告报表 (近7天)\n")
            print(f"{'广告名称':<25} {'状态':<10} {'预算':<10} {'消耗':<10} {'曝光':<12} {'点击':<8} {'CTR':<8} {'CPA':<8}")
            print("-" * 100)
            
            for campaign in campaigns:
                name = campaign.get('name', 'N/A')
                status = campaign.get('status', 'N/A')
                budget = campaign.get('budget', 0)
                cost = campaign.get('cost', 0)
                impressions = campaign.get('impressions', 0)
                clicks = campaign.get('clicks', 0)
                ctr = campaign.get('ctr', 0)
                cpa = campaign.get('cpa', 0)
                
                print(f"{name:<25} {status:<10} {budget:>8} {cost:>8} {impressions:>12} {clicks:>8} {ctr:>8.2f} {cpa:>8.2f}")
            
            total_cost = sum(c.get('cost', 0) for c in campaigns)
            total_impressions = sum(c.get('impressions', 0) for c in campaigns)
            total_clicks = sum(c.get('clicks', 0) for c in campaigns)
            
            print("-" * 100)
            print(f"{'总计':<22} {total_cost:>8} {total_impressions:>12} {total_clicks:>8}")
        else:
            print(f"\n❌ 查询失败: {result.get('message', '未知错误')}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="巨量广告自动化投放系统 - 乐盟互动出品")
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 状态命令
    parser_status = subparsers.add_parser('status', help='查看系统状态')
    parser_status.set_defaults(func=lambda args: OceanEngineMain().status())
    
    # 广告列表
    parser_list = subparsers.add_parser('list', help='查询广告计划列表')
    parser_list.add_argument('account_id', help='广告账户ID')
    parser_list.set_defaults(func=lambda args: OceanEngineMain().campaign_list(args.account_id))
    
    # 创建广告
    parser_create = subparsers.add_parser('create', help='创建广告计划')
    parser_create.add_argument('account_id', help='广告账户ID')
    parser_create.add_argument('name', help='广告计划名称')
    parser_create.add_argument('budget', type=int, help='日预算（元）')
    parser_create.add_argument('--objective', default='CONVERSIONS', help='广告目标')
    parser_create.set_defaults(func=lambda args: OceanEngineMain().campaign_create(
        args.account_id, args.name, args.budget, args.objective))
    
    # 自动投放
    parser_auto = subparsers.add_parser('auto', help='自动投放')
    parser_auto.add_argument('campaign_id', help='广告计划ID')
    parser_auto.set_defaults(func=lambda args: OceanEngineMain().auto_launch(args.campaign_id))
    
    # 批量投放
    parser_batch = subparsers.add_parser('batch', help='批量投放')
    parser_batch.add_argument('file', help='广告ID列表文件')
    parser_batch.set_defaults(func=lambda args: OceanEngineMain().batch_launch(args.file))
    
    # 优化分析
    parser_optimize = subparsers.add_parser('optimize', help='优化分析')
    parser_optimize.add_argument('account_id', help='广告账户ID')
    parser_optimize.add_argument('--days', type=int, default=7, help='分析天数')
    parser_optimize.set_defaults(func=lambda args: OceanEngineMain().optimize(args.account_id, args.days))
    
    # 报表
    parser_report = subparsers.add_parser('report', help='查看报表')
    parser_report.add_argument('account_id', help='广告账户ID')
    parser_report.add_argument('--period', default='last_7d', help='报表周期')
    parser_report.set_defaults(func=lambda args: OceanEngineMain().report(args.account_id, args.period))
    
    # 解析参数
    args = parser.parse_args()
    
    # 初始化系统
    main = OceanEngineMain()
    main.init()
    
    # 执行命令
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
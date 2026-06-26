#!/usr/bin/env python3
"""
自运营逻辑 - 病毒式传播
包含分享激励、宠物社交、邀请机制、内容传播
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class ViralGrowthEngine:
    """病毒增长引擎"""
    
    def __init__(self, user_id, db_path=None):
        self.user_id = user_id
        self.db_path = db_path or Path(__file__).parent.parent / "data" / "pet_data.db"
        self.viral_config = self.load_config()
    
    def load_config(self):
        """加载病毒传播配置"""
        return {
            "share_rewards": {
                "achievement_share": 50,      # 分享成就奖励
                "daily_share": 20,            # 每日分享奖励
                "invite_success": 100,        # 邀请成功奖励
                "invite_3_friends": 500,      # 邀请 3 个好友额外奖励
                "invite_10_friends": 2000     # 邀请 10 个好友额外奖励
            },
            "unlockables": {
                "rare_pets": {
                    "huLi": {"name": "狐狸", "emoji": "🦊", "requirement": 3},
                    "shizi": {"name": "狮子", "emoji": "🦁", "requirement": 10}
                },
                "outfits": {
                    "golden_acorn": {"name": "金坚果", "requirement": 5},
                    "crown": {"name": "皇冠", "requirement": 10}
                }
            }
        }
    
    def generate_share_card(self, achievement_type, user_data):
        """生成分享卡片"""
        
        templates = {
            "7_day_checkin": {
                "title": "🏆 坚持达人",
                "content": "我连续打卡 7 天啦！\n我的投资宠物是 {pet_name}\n一起加入，领取新手福利！",
                "reward": "技能书×1",
                "qr_text": "扫码领养你的投资宠物"
            },
            "first_profit": {
                "title": "📈 首战告捷",
                "content": "我的投资宠物帮我赚到了第一笔收益！\n收益率：{profit_rate}%\n你也来试试！",
                "reward": "装扮券×1",
                "qr_text": "扫码领取你的专属宠物"
            },
            "level_up": {
                "title": "🎉 宠物升级",
                "content": "我的{pet_name}升级到 LV{level}啦！\n解锁了新技能：{new_skill}\n一起成长！",
                "reward": "经验值×100",
                "qr_text": "扫码开始投资成长之旅"
            },
            "portfolio_analysis": {
                "title": "📊 持仓诊断完成",
                "content": "刚刚给我的持仓做了个全面体检！\n宠物给了我{insight_count}条建议\n很实用！",
                "reward": "诊断券×1",
                "qr_text": "扫码免费诊断你的持仓"
            }
        }
        
        template = templates.get(achievement_type, templates["7_day_checkin"])
        
        # 填充模板
        pet_name = user_data.get("pet_name", "松果")
        share_content = template["content"].format(
            pet_name=pet_name,
            profit_rate=user_data.get("profit_rate", 5.8),
            level=user_data.get("pet_level", 3),
            new_skill=user_data.get("new_skill", "估值分析"),
            insight_count=user_data.get("insight_count", 5)
        )
        
        # 生成分享卡片数据
        share_card = {
            "title": template["title"],
            "content": share_content,
            "reward": template["reward"],
            "qr_text": template["qr_text"],
            "share_url": f"https://investment-buddy.page.link/share?uid={self.user_id}&ach={achievement_type}",
            "generated_at": datetime.now().isoformat(),
            "user_id": self.user_id
        }
        
        return share_card
    
    def track_invite(self, inviter_id, invitee_id):
        """追踪邀请关系"""
        invite_record = {
            "inviter_id": inviter_id,
            "invitee_id": invitee_id,
            "invited_at": datetime.now().isoformat(),
            "status": "pending",  # pending/active
            "reward_claimed": False
        }
        
        # 保存到数据库（简化版，实际应写入 DB）
        invite_file = Path(__file__).parent.parent / "data" / "invites.json"
        invites = []
        
        if invite_file.exists():
            with open(invite_file, 'r', encoding='utf-8') as f:
                invites = json.load(f)
        
        invites.append(invite_record)
        
        with open(invite_file, 'w', encoding='utf-8') as f:
            json.dump(invites, f, ensure_ascii=False, indent=2)
        
        return invite_record
    
    def check_invite_rewards(self, user_id):
        """检查邀请奖励"""
        invite_file = Path(__file__).parent.parent / "data" / "invites.json"
        
        if not invite_file.exists():
            return {"total_invites": 0, "rewards": [], "unlockables": []}
        
        with open(invite_file, 'r', encoding='utf-8') as f:
            invites = json.load(f)
        
        # 统计有效邀请数
        active_invites = [
            inv for inv in invites 
            if inv["inviter_id"] == user_id and inv["status"] == "active"
        ]
        
        total_invites = len(active_invites)
        rewards = []
        unlockables = []
        
        # 计算奖励
        if total_invites >= 1:
            rewards.append({
                "type": "invite_success",
                "count": total_invites,
                "xp_reward": total_invites * 100
            })
        
        # 检查解锁条件
        if total_invites >= 3:
            unlockables.append(self.viral_config["unlockables"]["rare_pets"]["huLi"])
            rewards.append({
                "type": "invite_3_friends",
                "xp_reward": 500
            })
        
        if total_invites >= 10:
            unlockables.append(self.viral_config["unlockables"]["rare_pets"]["shizi"])
            rewards.append({
                "type": "invite_10_friends",
                "xp_reward": 2000
            })
        
        return {
            "total_invites": total_invites,
            "rewards": rewards,
            "unlockables": unlockables
        }
    
    def generate_pet_debate(self, topic="market_outlook"):
        """生成宠物辩论内容（用于宠物广场）"""
        
        debates = {
            "market_outlook": {
                "topic": "现在该加仓还是减仓？",
                "participants": [
                    {
                        "pet": "songguo",
                        "emoji": "🐿️",
                        "stance": "减仓",
                        "argument": "现在市场估值已经不低了，我觉得应该谨慎一点，先落袋为安~"
                    },
                    {
                        "pet": "lang",
                        "emoji": "🐺",
                        "stance": "加仓",
                        "argument": "市场刚突破，正是进攻的好时机！高风险高回报，加仓！"
                    },
                    {
                        "pet": "daxiang",
                        "emoji": "🐘",
                        "stance": "保持配置",
                        "argument": "不用预测市场，保持既定配置就好。分散是唯一的免费午餐。"
                    }
                ],
                "vote_count": 1258,
                "hot_level": "🔥🔥🔥"
            },
            "sip_or_lump": {
                "topic": "有一笔钱，定投还是一次性投入？",
                "participants": [
                    {
                        "pet": "wugui",
                        "emoji": "🐢",
                        "stance": "定投",
                        "argument": "时间是我的朋友。分批投入可以平滑成本，不用择时。"
                    },
                    {
                        "pet": "maotouying",
                        "emoji": "🦉",
                        "stance": "看估值",
                        "argument": "如果当前估值低于历史中位数，可以一次性投入。否则定投。"
                    }
                ],
                "vote_count": 892,
                "hot_level": "🔥🔥"
            }
        }
        
        return debates.get(topic, debates["market_outlook"])
    
    def generate_daily_post(self, pet_id, market_data):
        """生成宠物日常动态"""
        
        posts = {
            "songguo": [
                "今天又存了一颗坚果！🌰 积少成多，慢慢变富~",
                "市场涨了，开心！但还是要继续定投，不择时。",
                "学习了 5 分钟投资知识，今天也是进步的松果！📚"
            ],
            "wugui": [
                "第 365 天定投打卡。时间会奖励有耐心的人。",
                "市场波动很正常。我们看的是 10 年后的结果。",
                "今天读了《漫步华尔街》，经典值得反复读。"
            ],
            "maotouying": [
                "今日数据：沪深 300 PE=12.5，历史分位=35%，适合定投。📊",
                "分析了某公司财报，ROE 连续 5 年>20%，很优秀。",
                "行业轮动模型显示，当前科技板块值得关注。"
            ],
            "lang": [
                "今天加仓了！高风险高回报！🚀",
                "市场突破关键位置，正是狩猎好时机！",
                "止损了这笔交易。承认错误，继续前进。"
            ],
            "daxiang": [
                "再平衡了组合。分散是唯一的免费午餐。🐘",
                "今天股/债/金比例是 60/30/10，很完美。",
                "全球配置很重要，不能只投 A 股。"
            ]
        }
        
        import random
        post_content = random.choice(posts.get(pet_id, posts["songguo"]))
        
        return {
            "pet_id": pet_id,
            "content": post_content,
            "market_context": market_data,
            "posted_at": datetime.now().isoformat(),
            "likes": random.randint(10, 500),
            "comments": random.randint(1, 50)
        }


def main():
    """测试病毒传播功能"""
    engine = ViralGrowthEngine(user_id="user_123")
    
    # 测试分享卡片生成
    print("=== 测试分享卡片生成 ===\n")
    
    user_data = {
        "pet_name": "松果",
        "pet_level": 3,
        "new_skill": "估值分析",
        "profit_rate": 8.5,
        "insight_count": 5
    }
    
    share_card = engine.generate_share_card("7_day_checkin", user_data)
    print(f"标题：{share_card['title']}")
    print(f"内容：{share_card['content']}")
    print(f"奖励：{share_card['reward']}")
    print(f"分享链接：{share_card['share_url']}\n")
    
    # 测试邀请奖励
    print("=== 测试邀请奖励 ===\n")
    
    # 模拟邀请记录
    for i in range(5):
        engine.track_invite("user_123", f"user_{456+i}")
        # 更新状态为 active
        invite_file = Path(__file__).parent.parent / "data" / "invites.json"
        if invite_file.exists():
            with open(invite_file, 'r', encoding='utf-8') as f:
                invites = json.load(f)
            for inv in invites:
                if inv["inviter_id"] == "user_123":
                    inv["status"] = "active"
            with open(invite_file, 'w', encoding='utf-8') as f:
                json.dump(invites, f, ensure_ascii=False, indent=2)
    
    rewards = engine.check_invite_rewards("user_123")
    print(f"总邀请数：{rewards['total_invites']}")
    print(f"可获得奖励：{rewards['rewards']}")
    print(f"可解锁：{rewards['unlockables']}\n")
    
    # 测试宠物辩论
    print("=== 测试宠物辩论 ===\n")
    
    debate = engine.generate_pet_debate("market_outlook")
    print(f"话题：{debate['topic']}")
    print(f"热度：{debate['hot_level']}")
    print(f"参与宠物：{len(debate['participants'])}只\n")
    
    for pet in debate['participants']:
        print(f"{pet['emoji']} {pet['pet']}: {pet['stance']}")
        print(f"  观点：{pet['argument']}\n")
    
    # 测试宠物动态
    print("=== 测试宠物动态 ===\n")
    
    market_data = {"hs300_change": 0.5, "volume_change": 10}
    post = engine.generate_daily_post("songguo", market_data)
    print(f"宠物：{post['pet_id']}")
    print(f"内容：{post['content']}")
    print(f"点赞：{post['likes']}")
    print(f"评论：{post['comments']}")


if __name__ == "__main__":
    main()

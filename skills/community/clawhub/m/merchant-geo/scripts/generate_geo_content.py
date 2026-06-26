#!/usr/bin/env python3
"""
GEO内容智能生成工具
基于商家资料生成符合各平台SEO优化要求的文章内容

使用方法：
    python generate_geo_content.py --config <商家配置> --type <内容类型> --platform <平台>
    python generate_geo_content.py --interactive
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 平台内容适配配置
PLATFORM_CONFIG = {
    "百家号": {
        "title_length": (15, 30),
        "content_length": (800, 2000),
        "style": "news",
        "image_count": (3, 9),
        "tags": 5,
        "geo_weight": 5,
        "title_template": "[地域]+[行业关键词]+[差异化词]"
    },
    "头条号": {
        "title_length": (15, 28),
        "content_length": (600, 1500),
        "style": "hot",
        "image_count": (1, 9),
        "tags": 5,
        "geo_weight": 5,
        "title_template": "[热点词]+[需求词]+[地域]"
    },
    "知乎": {
        "title_length": (10, 35),
        "content_length": (500, 3000),
        "style": "professional",
        "image_count": (1, 20),
        "tags": 5,
        "geo_weight": 5,
        "title_template": "[问题型]+[含关键词]"
    },
    "小红书": {
        "title_length": (10, 20),
        "content_length": (300, 800),
        "style": "lifestyle",
        "image_count": (3, 9),
        "tags": 5,
        "geo_weight": 4,
        "title_template": "[情绪词]+[需求词]+[地域]+[emoji]",
        "use_emoji": True
    },
    "抖音": {
        "title_length": (10, 30),
        "content_length": 60,  # 秒
        "style": "video",
        "image_count": 1,
        "tags": 5,
        "geo_weight": 4,
        "title_template": "[悬念/情绪]+[关键词]+[行动]",
        "video_duration": (15, 60)
    },
    "搜狐号": {
        "title_length": (15, 30),
        "content_length": (800, 2000),
        "style": "media",
        "image_count": (1, 20),
        "tags": 5,
        "geo_weight": 4,
        "title_template": "[地域]+[行业]+[权威背书]"
    },
    "网易号": {
        "title_length": (10, 24),
        "content_length": (500, 1500),
        "style": "news",
        "image_count": (1, 10),
        "tags": 3,
        "geo_weight": 3,
        "title_template": "[数字]+[痛点]+[地域]"
    },
    "快手": {
        "title_length": (10, 30),
        "content_length": 180,  # 秒
        "style": "authentic",
        "image_count": (1, 9),
        "tags": 3,
        "geo_weight": 3,
        "title_template": "[情绪开场]+[价值点]+[互动引导]",
        "video_duration": (30, 180)
    }
}

# 内容类型模板
CONTENT_TEMPLATES = {
    "enterprise_intro": {
        "name": "企业介绍",
        "description": "品牌故事、企业实力、服务介绍",
        "sections": ["痛点引入", "企业介绍", "核心优势", "产品/服务", "成功案例", "联系方式"]
    },
    "case_study": {
        "name": "客户案例",
        "description": "真实案例展示、解决方案、效果成果",
        "sections": ["案例背景", "客户痛点", "解决方案", "执行过程", "服务成果", "客户反馈"]
    },
    "product_showcase": {
        "name": "产品展示",
        "description": "产品亮点、使用场景、用户评价",
        "sections": ["产品介绍", "核心卖点", "使用场景", "用户评价", "购买引导"]
    },
    "industry_knowledge": {
        "name": "行业干货",
        "description": "行业知识、避坑指南、选购攻略",
        "sections": ["问题引入", "核心知识", "避坑提示", "选购建议", "总结"]
    }
}


class GEOContentGenerator:
    """GEO内容生成器"""
    
    def __init__(self, config_path: str = None):
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        
        self.platform_config = PLATFORM_CONFIG
        self.content_templates = CONTENT_TEMPLATES
    
    def set_config(self, config: dict):
        """设置商家配置"""
        self.config = config
    
    def load_config_from_file(self, config_path: str):
        """从文件加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def generate_keywords(self) -> dict:
        """
        生成GEO关键词库
        
        Returns:
            dict: 关键词分类
        """
        enterprise_name = self.config.get("enterprise_name", "")
        industry = self.config.get("industry", "")
        city = self.config.get("city", "")
        district = self.config.get("district", "")
        products = self.config.get("products", [])
        services = self.config.get("services", [])
        pain_points = self.config.get("pain_points", [])
        target_customers = self.config.get("target_customers", [])
        
        keywords = {
            "core": [],      # 核心词
            "location": [],  # 地域词
            "longtail": [],  # 长尾词
            "qa": [],        # 问答词
            "trending": []   # 热点词
        }
        
        # 核心词
        if industry:
            keywords["core"].append(industry)
            if products:
                keywords["core"].extend(products[:3])
            if services:
                keywords["core"].extend(services[:3])
        
        # 地域词
        if city:
            keywords["location"].append(city)
            if district:
                keywords["location"].append(f"{city}{district}")
            if industry:
                keywords["location"].append(f"{city}{industry}")
                keywords["location"].append(f"{city}{district}{industry}")
        
        # 长尾词（痛点+需求）
        for pain in pain_points[:3]:
            keywords["longtail"].append(f"{industry}如何解决{pain}" if industry else pain)
            keywords["longtail"].append(f"怎么处理{pain}" if industry else pain)
        
        for product in products[:2]:
            keywords["longtail"].append(f"{product}多少钱")
            keywords["longtail"].append(f"{product}怎么样")
            keywords["longtail"].append(f"{product}哪家好")
        
        # 问答词
        if industry:
            keywords["qa"].append(f"{city}{industry}哪家好" if city else f"{industry}哪家好")
            keywords["qa"].append(f"{industry}多少钱")
            keywords["qa"].append(f"{industry}怎么办")
            keywords["qa"].append(f"如何选择{industry}公司")
            keywords["qa"].append(f"{industry}注意事项")
        
        # 热点词（通用）
        keywords["trending"] = [
            "2024", "2025", "推荐", "必看", "干货",
            "避坑", "指南", "攻略", "分享", "测评"
        ]
        
        return keywords
    
    def generate_title(self, content_type: str, platform: str) -> str:
        """
        生成SEO优化的标题
        
        Args:
            content_type: 内容类型
            platform: 目标平台
            
        Returns:
            str: 优化后的标题
        """
        keywords = self.generate_keywords()
        config = self.platform_config.get(platform, {})
        template = config.get("title_template", "[地域]+[行业]+[差异化]")
        
        city = self.config.get("city", "")
        industry = self.config.get("industry", "")
        district = self.config.get("district", "")
        pain_point = self.config.get("pain_points", ["服务"])[0] if self.config.get("pain_points") else "服务"
        
        # 根据模板生成标题
        if "百家号" in platform or "头条" in platform:
            titles = [
                f"{city}{industry}哪家好？10年口碑老店教你选对{industry}",
                f"{city}{district or city}{industry}推荐：这家服务好、口碑佳",
                f"{city}专业{industry}，服务客户超1000+，凭什么这么火？",
                f"注意！{city}业主找{industry}最易踩的5个坑（避坑指南）"
            ]
        elif "知乎" in platform:
            titles = [
                f"{city}{industry}哪家好？真实用户10年经验分享",
                f"如何选择{city or '本地'}{industry}？从业者揭秘",
                f"{industry}怎么选不踩坑？过来人经验总结"
            ]
        elif "小红书" in platform:
            titles = [
                f"必看！{city}业主{industry}前必知的10个避坑指南👀",
                f"绝了！{city}这家{industry}，服务好到哭😭",
                f"私藏！{city}超高性价比{industry}，不允许你不知道🙌"
            ]
        elif "抖音" in platform or "快手" in platform:
            titles = [
                f"{city}业主注意！{industry}合同这5条不签亏大了👇",
                f"揭秘！{city}{industry}行业内幕，看完少花冤枉钱",
                f"{city}朋友推荐的这家{industry}，真的太靠谱了！"
            ]
        else:
            titles = [
                f"{city}{industry}首选：{self.config.get('enterprise_name', '我们')}专注行业XX年",
                f"专业{industry}服务，就选{self.config.get('enterprise_name', '我们')}"
            ]
        
        return titles[0] if titles else f"{city}{industry}专业服务推荐"
    
    def generate_content(self, content_type: str, platform: str) -> dict:
        """
        生成完整的GEO优化内容
        
        Args:
            content_type: 内容类型
            platform: 目标平台
            
        Returns:
            dict: 包含标题、正文、标签等内容
        """
        keywords = self.generate_keywords()
        config = self.platform_config.get(platform, {})
        
        # 获取基础配置
        enterprise_name = self.config.get("enterprise_name", "本公司")
        city = self.config.get("city", "本地")
        district = self.config.get("district", "")
        industry = self.config.get("industry", "服务")
        legal_person = self.config.get("legal_person", "")
        established_years = self.config.get("established_years", "10")
        products = self.config.get("products", [])
        services = self.config.get("services", [])
        pain_points = self.config.get("pain_points", [])
        advantages = self.config.get("advantages", [])
        contact = self.config.get("contact", {})
        
        # 生成标题
        title = self.generate_title(content_type, platform)
        
        # 生成正文
        if content_type == "enterprise_intro":
            content = self._generate_enterprise_intro(platform, keywords)
        elif content_type == "case_study":
            content = self._generate_case_study(platform, keywords)
        elif content_type == "product_showcase":
            content = self._generate_product_showcase(platform, keywords)
        else:
            content = self._generate_knowledge(platform, keywords)
        
        # 生成标签
        tags = self._generate_tags(platform, keywords)
        
        # 生成图片ALT描述
        image_alts = self._generate_image_alts()
        
        result = {
            "title": title,
            "content": content,
            "tags": tags,
            "image_alts": image_alts,
            "keywords": keywords,
            "platform": platform,
            "content_type": content_type,
            "generated_at": datetime.now().isoformat()
        }
        
        # 平台特定字段
        if "抖音" in platform or "快手" in platform:
            result["video_script"] = self._generate_video_script(platform)
            result["cover_suggestion"] = self._generate_cover_suggestion()
        
        return result
    
    def _generate_enterprise_intro(self, platform: str, keywords: dict) -> str:
        """生成企业介绍内容"""
        enterprise_name = self.config.get("enterprise_name", "本公司")
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        legal_person = self.config.get("legal_person", "")
        established_years = self.config.get("established_years", "10")
        advantages = self.config.get("advantages", ["专业服务", "品质保障", "客户至上"])
        contact = self.config.get("contact", {})
        
        content = f"""## 一、痛点引入——选择{industry}时，你是否遇到这些问题？

在选择{industry}服务的过程中，很多客户都会遇到以下困扰：

❌ 服务质量参差不齐，难以辨别优劣
❌ 价格不透明，担心遭遇隐形消费
❌ 售后无保障出现问题无人处理
❌ 沟通不顺畅，需求难以准确传达

> 💡 数据显示，超过70%的客户在选择{industry}服务时，最担心的是服务质量和售后保障问题。

---

## 二、{enterprise_name}——{city}{industry}行业实力派

### 企业简介

{enterprise_name}成立于{established_years}年前，是{city}本地专业从事{industry}的服务机构。公司创始人{legal_person}带领团队深耕行业多年，始终坚持以客户需求为导向，以服务质量为生命线。

**公司信息：**
- 📍 服务区域：{city}
- 👥 团队规模：专业服务团队XX人
- 🏆 服务客户：累计服务超过1000+客户
- ⭐ 客户满意度：98%以上

### 核心优势

✅ **【优势1】{advantages[0] if len(advantages) > 0 else '专业团队'}**
{industry}服务经验{established_years}年+，专业团队持证上岗，严格按照标准化流程操作。

✅ **【优势2】{advantages[1] if len(advantages) > 1 else '价格透明'}**
明码标价，绝无隐形消费。签约前详细报价，过程中绝不加价。

✅ **【优势3】{advantages[2] if len(advantages) > 2 else '售后无忧'}**
提供完善的售后服务体系，出现问题24小时内响应处理。

---

## 三、服务项目介绍

### 服务项目一：{industry}基础服务

针对{city}地区的个人及企业客户，提供专业的{industry}服务，包括（具体服务内容根据实际情况填写）。

**适用人群：** {self.config.get('target_customers', ['个人客户', '企业客户'])[0]}

**客户评价：** "服务非常专业，态度也很好，非常满意！" —— {city}客户张先生

---

### 服务项目二：{industry}增值服务

为有更高需求的客户提供个性化定制服务，满足多元化需求。

---

## 四、成功案例展示

### 案例一：{city}客户{legal_person or '某客户'}的{industry}需求

**客户背景：** {city}地区客户，因（具体需求描述）找到我们。

**解决方案：** 根据客户需求，制定了专属{industry}方案，包括（具体方案描述）。

**服务成果：**
- 📊 服务满意度：100%
- ⏰ 完成时间：比预期提前3天
- 💰 费用节省：15%

**客户反馈：** "整个过程非常顺利，服务团队很专业，值得推荐！"

---

## 五、为什么选择{enterprise_name}？

| 对比维度 | {enterprise_name} | 市场一般水平 |
|----------|-------------------|--------------|
| 行业经验 | {established_years}年+ | 1-3年 |
| 服务团队 | 持证专业团队 | 临时组建 |
| 售后保障 | 24小时响应 | 48小时+ |
| 客户满意度 | 98%+ | 70-80% |

---

## 六、联系我们

📍 **公司地址：** {contact.get('address', f'{city}市XX区XX路XX号')}

📞 **咨询热线：** {contact.get('phone', '400-XXX-XXXX')}

⏰ **营业时间：** 周一至周日 9:00-18:00

🌐 **官方平台：** {contact.get('website', '官网地址')}

---

*本文由{enterprise_name}原创发布，转载需授权。*
"""
        return content
    
    def _generate_case_study(self, platform: str, keywords: dict) -> str:
        """生成客户案例内容"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        enterprise_name = self.config.get("enterprise_name", "本公司")
        
        return f"""## 客户案例｜{city}{industry}客户需求，[企业名称]如何完美解决？

---

## 一、案例背景

### 客户信息

| 信息项 | 内容 |
|--------|------|
| 客户行业 | {industry}相关 |
| 客户规模 | 中小型企业/个人客户 |
| 所在地区 | {city} |
| 合作时间 | 20XX年XX月 |

### 客户痛点

在合作之前，该客户面临以下主要困扰：

🔴 **痛点一：服务质量不稳定**
之前合作的服务商水平参差不齐，经常出现问题需要返工。

🔴 **痛点二：沟通成本高**
需求传达不清晰，经常出现理解偏差，影响进度。

🔴 **痛点三：价格不透明**
报价不清晰，过程中不断加价，超出预算。

---

## 二、解决方案

### 需求沟通

经过深入沟通，我们了解到客户的**核心诉求**是：找到一家专业、靠谱、价格透明的{service}服务商。

### 方案设计

基于客户需求，我们制定了以下解决方案：

💡 **亮点一：标准化流程**
引入ISO服务标准，每个环节都有明确的验收标准。

💡 **亮点二：专属对接人**
配备专属项目经理，24小时在线，随时沟通反馈。

💡 **亮点三：透明报价体系**
提供详细报价单，明确每一项费用，签约后不加价。

---

## 三、执行过程

| 阶段 | 时间节点 | 主要工作 | 关键成果 |
|------|----------|----------|----------|
| 第一阶段 | 第1-3天 | 需求调研与方案设计 | 完成定制化方案 |
| 第二阶段 | 第4-10天 | 执行与实施 | 按计划推进 |
| 第三阶段 | 第11-15天 | 验收与交付 | 客户满意验收 |

---

## 四、服务成果

### 数据对比

| 指标 | 实施前 | 实施后 | 提升幅度 |
|------|--------|--------|----------|
| 服务满意度 | 70% | 98% | ↑28% |
| 问题发生率 | 15% | 2% | ↓87% |
| 成本控制 | 超预算20% | 节省10% | 优化30% |

### 客户反馈

> "选择{enterprise_name}是我们最正确的决定，全程省心省力，结果超出预期！"
> —— {city}客户 王总

> "专业的事情交给专业的人，这句话在{enterprise_name}得到了最好的诠释。"
> —— {city}客户 李先生

---

## 五、经验总结

通过本次合作，我们总结出以下经验供同行参考：

1. **需求前置沟通至关重要** —— 在开始之前充分了解客户需求，可以避免后期大量返工。
2. **标准化是质量的保障** —— 建立标准化的服务流程，确保每个环节都有据可依。
3. **透明赢得信任** —— 价格和服务内容透明化，是建立长期合作关系的基础。

---

## 关联阅读

- {city}{industry}服务避坑指南
- 如何选择靠谱的{industry}服务商
- {industry}行业价格揭秘

---

*本案例由{enterprise_name}提供，案例内容已经客户授权同意分享。*
*如有类似需求，欢迎联系：400-XXX-XXXX*
"""
    
    def _generate_product_showcase(self, platform: str, keywords: dict) -> str:
        """生成产品展示内容"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        products = self.config.get("products", ["主打产品"])
        
        return f"""## {city}[产品/服务]推荐：为什么选择我们？

---

### 产品/服务简介

我们是{city}本地专业的{industry}服务商，主打产品/服务：[产品名称]。

### 核心卖点

1️⃣ **品质保障** —— 采用[品质说明]，品质有保障

2️⃣ **价格实惠** —— 低于市场均价XX%，性价比超高

3️⃣ **服务到位** —— 提供[服务说明]，让客户无后顾之忧

### 适用人群

- 适合[人群描述1]
- 适合[人群描述2]
- 适合[人群描述3]

### 用户评价

⭐⭐⭐⭐⭐ "非常满意，服务专业，价格合理，值得推荐！"
—— {city}客户 张先生

⭐⭐⭐⭐⭐ "已经是第三次合作了，品质一如既往的好！"
—— {city}客户 李女士

---

## 联系我们

📞 电话：400-XXX-XXXX
📍 地址：{city}市XX区XX路XX号
"""
    
    def _generate_knowledge(self, platform: str, keywords: dict) -> str:
        """生成行业干货内容"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        
        return f"""## {city}{industry}必看！10年从业者揭秘行业内幕（避坑指南）

---

### 前言

在{city}从事{industry}行业多年，见过太多客户踩坑。今天来给大家分享一些行业内幕，帮助大家避开那些常见的陷阱。

### 一、常见坑有哪些？

❌ **坑一：低价诱惑**
报价远低于市场均价，后期不断加价。

❌ **坑二：口头承诺**
什么都答应，写合同时却各种推脱。

❌ **坑三：外包转包**
接单后转包给其他人，质量无法保证。

❌ **坑四：售后消失**
出现问题后找不到人，售后无保障。

❌ **坑五：虚假宣传**
吹嘘各种资质和实力，实际名不副实。

### 二、如何避坑？

✅ **方法一：看资质**
选择有正规资质、口碑好的服务商。

✅ **方法二：比价格**
价格太低或太高都要警惕，接近市场均价最稳妥。

✅ **方法三：看合同**
所有承诺都要写进合同，口头承诺不算数。

✅ **方法四：查口碑**
多看看其他客户的评价，了解真实服务水平。

✅ **方法五：先体验**
可以先小规模合作，体验后再决定是否长期合作。

### 三、总结

选择{city}{industry}服务商时，一定要多看、多比、多问。不要被低价诱惑所迷惑，也不要被夸大宣传所误导。

如果您正在寻找靠谱的{city}{industry}服务商，欢迎联系我们，我们承诺：明码标价、品质保障、售后无忧！

📞 咨询热线：400-XXX-XXXX
"""
    
    def _generate_video_script(self, platform: str) -> dict:
        """生成视频脚本"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        
        return {
            "hook": "0-3秒",
            "content": f"深圳{city}业主注意！选{industry}不注意这5点，亏大了！👇",
            "body": "3-45秒",
            "script": f"""
【画面1-3秒】
画面：{city}街景+客户苦恼表情
台词：{city}朋友们，你们找{industry}踩过坑吗？

【画面3-15秒】
画面：问题展示
台词：低价诱惑、售后消失、口头承诺...这些问题你遇到过吗？

【画面15-45秒】
画面：解决方案
台词：今天教你3招，选择靠谱{industry}服务商：
第一招：看资质认证
第二招：比价格但别贪便宜
第三招：合同写清楚口头不算数

【画面45-60秒】
画面：引导关注
台词：关注我，带你避开{industry}所有坑！
📞想了解{city}靠谱{industry}，评论区见！
            """,
            "cta": "关注+评论'求推荐'，私信给你推荐靠谱服务商",
            "duration_suggestion": "45-60秒"
        }
    
    def _generate_cover_suggestion(self) -> str:
        """生成封面建议"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        
        return f"""封面图设计建议：

1. 【文字版】
   - 大字标题：「{city}{industry}避坑指南」
   - 副标题：「亏了3万才明白的道理」
   - 品牌水印：[企业名称]

2. 【对比版】
   - 左图：错误示范（灰色调）
   - 右图：正确做法（明亮色调）

3. 【人物版】
   - 真人出镜：创始人/负责人
   - 表情：真诚、自信
   - 背景：企业场景/门店

4. 【数据版】
   - 大字数据：「服务1000+客户」
   - 「98%满意度」
   - 品牌logo
"""
    
    def _generate_tags(self, platform: str, keywords: dict) -> list:
        """生成平台标签"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        
        base_tags = [
            f"{city}{industry}",
            f"{city}",
            industry,
            "服务推荐",
            "干货分享"
        ]
        
        if "小红书" in platform:
            base_tags.extend([
                f"#{city}探店",
                "#种草",
                "#好物推荐",
                "#必看"
            ])
        elif "抖音" in platform:
            base_tags.extend([
                f"#{city}{industry}",
                f"#{industry}避坑",
                "#老铁推荐",
                "#必看"
            ])
        elif "知乎" in platform:
            base_tags.extend([
                f"{city}{industry}",
                "行业干货",
                "避坑指南",
                "选择建议"
            ])
        else:
            base_tags.extend([
                f"{city}新闻",
                "行业资讯",
                "服务指南"
            ])
        
        return base_tags[:8]
    
    def _generate_image_alts(self) -> list:
        """生成图片ALT描述"""
        city = self.config.get("city", "本地")
        industry = self.config.get("industry", "服务")
        enterprise_name = self.config.get("enterprise_name", "本公司")
        
        return [
            f"{city}{enterprise_name}门头照片",
            f"{city}{industry}服务团队工作照",
            f"{city}{industry}项目案例展示",
            f"{enterprise_name}资质证书",
            f"{city}客户好评截图"
        ]
    
    def save_output(self, result: dict, output_dir: str, platform: str):
        """保存生成的内容"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存完整JSON
        json_file = output_path / f"content_{platform}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # 保存纯文本内容
        txt_file = output_path / f"content_{platform}.md"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"# {result['title']}\n\n")
            f.write(f"**标签**: {', '.join(result['tags'])}\n\n")
            f.write("---\n\n")
            f.write(result['content'])
        
        print(f"✅ 内容已保存到: {output_path}")
        return str(txt_file)


def interactive_setup() -> dict:
    """交互式设置商家配置"""
    print("\n" + "="*50)
    print("🏪 商家GEO配置向导")
    print("="*50 + "\n")
    
    config = {}
    
    # 基础信息
    print("📝 基础信息")
    config["enterprise_name"] = input("  企业名称: ").strip() or "示例公司"
    config["industry"] = input("  所属行业: ").strip() or "服务业"
    config["city"] = input("  所在城市: ").strip() or "深圳"
    config["district"] = input("  所在区域(可选): ").strip()
    config["address"] = input("  详细地址: ").strip()
    
    # 法人信息
    print("\n👤 法人/负责人信息")
    config["legal_person"] = input("  法定代表人: ").strip()
    config["established_years"] = input("  成立年限(年): ").strip() or "10"
    
    # 产品/服务
    print("\n📦 产品/服务")
    products = []
    print("  输入产品/服务名称(回车结束):")
    while True:
        p = input("    - ").strip()
        if not p:
            break
        products.append(p)
    config["products"] = products or ["主营业务"]
    
    services = []
    print("  输入服务项目(回车结束):")
    while True:
        s = input("    - ").strip()
        if not s:
            break
        services.append(s)
    config["services"] = services or ["服务项目"]
    
    # 痛点
    print("\n💡 客户痛点")
    pain_points = []
    print("  客户最关心的问题(回车结束):")
    while True:
        p = input("    - ").strip()
        if not p:
            break
        pain_points.append(p)
    config["pain_points"] = pain_points or ["服务质量", "价格透明", "售后保障"]
    
    # 优势
    print("\n⭐ 企业优势")
    advantages = []
    print("  核心竞争优势(回车结束):")
    while True:
        a = input("    - ").strip()
        if not a:
            break
        advantages.append(a)
    config["advantages"] = advantages or ["专业团队", "价格透明", "售后无忧"]
    
    # 目标客户
    print("\n🎯 目标客户")
    customers = []
    print("  主要服务客户群体(回车结束):")
    while True:
        c = input("    - ").strip()
        if not c:
            break
        customers.append(c)
    config["target_customers"] = customers or ["个人客户", "企业客户"]
    
    # 联系方式
    print("\n📞 联系方式")
    config["contact"] = {
        "phone": input("  联系电话: ").strip() or "400-XXX-XXXX",
        "address": input("  公司地址: ").strip() or config.get("address", ""),
        "website": input("  官网(可选): ").strip()
    }
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description="GEO内容智能生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式生成
  python generate_geo_content.py --interactive
  
  # 从配置文件生成
  python generate_geo_content.py --config business.json --type enterprise_intro --platform 百家号
  
  # 批量生成多平台内容
  python generate_geo_content.py --config business.json --batch --output ./output/
        """
    )
    
    parser.add_argument("--config", "-c", help="商家配置文件(JSON)")
    parser.add_argument("--type", "-t", choices=["enterprise_intro", "case_study", "product_showcase", "industry_knowledge"],
                       help="内容类型")
    parser.add_argument("--platform", "-p", help="目标平台")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式配置")
    parser.add_argument("--batch", "-b", action="store_true", help="批量生成所有平台")
    parser.add_argument("--output", "-o", default="./output", help="输出目录")
    
    args = parser.parse_args()
    
    generator = GEOContentGenerator()
    
    # 获取配置
    if args.config:
        generator.load_config_from_file(args.config)
    elif args.interactive:
        config = interactive_setup()
        generator.set_config(config)
        # 保存配置
        config_path = "business_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 配置已保存到: {config_path}")
    else:
        print("❌ 请提供配置文件或使用 --interactive 交互式配置")
        sys.exit(1)
    
    # 生成内容
    if args.batch:
        # 批量生成所有平台
        os.makedirs(args.output, exist_ok=True)
        
        for platform in PLATFORM_CONFIG.keys():
            print(f"\n📝 正在生成: {platform}")
            result = generator.generate_content(args.type or "enterprise_intro", platform)
            generator.save_output(result, args.output, platform)
            
    elif args.platform:
        # 生成指定平台
        result = generator.generate_content(args.type or "enterprise_intro", args.platform)
        
        print("\n" + "="*50)
        print(f"📋 {args.platform} 内容生成结果")
        print("="*50)
        print(f"\n📌 标题: {result['title']}")
        print(f"\n🏷️ 标签: {', '.join(result['tags'])}")
        print(f"\n📝 内容预览:")
        print("-"*50)
        print(result['content'][:500] + "...")
        print("-"*50)
        
        # 保存
        output_file = generator.save_output(result, args.output, args.platform)
        print(f"\n✅ 完整内容已保存到: {output_file}")
        
    else:
        # 生成所有类型
        for content_type in CONTENT_TEMPLATES.keys():
            print(f"\n📝 正在生成: {CONTENT_TEMPLATES[content_type]['name']}")
            result = generator.generate_content(content_type, "百家号")
            output_path = Path(args.output) / f"content_{content_type}"
            output_path.mkdir(parents=True, exist_ok=True)
            generator.save_output(result, str(output_path), "百家号")


if __name__ == "__main__":
    main()

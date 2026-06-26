#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北大校友会信息查询主程序
"""

import json
import sys

# 校友会简介
OVERVIEW = {
    "name": "北京大学校友会",
    "english_name": "Peking University Alumni Association (PKUAA)",
    "founded": "1984年5月4日",
    "nature": "由北京大学校友自愿结成的全国性、联合性、非营利性社会组织",
    "register": "在教育部和民政部注册",
    "mission": "加强校友之间、校友与母校之间的联系，服务校友、服务母校、服务社会",
    "vision": "传承北大精神，凝聚校友力量，共促母校发展",
    "members": "全球校友超过30万人",
    "chapters": "海内外校友分会超过90个",
    "organization": [
        "校友工作办公室（秘书处）",
        "各院系校友工作负责人",
        "地方校友会",
        "行业校友会",
        "海外校友会"
    ],
    "brand_activities": [
        "返校日活动",
        "校友讲坛",
        "创业大赛",
        "校友企业招聘会",
        "公益志愿活动",
        "新春联欢会"
    ]
}

# 各地分会
CHAPTERS = {
    "国内地方校友会": [
        {"name": "北京大学校友会北京分会", "region": "北京", "contact": "北京大学校友之家"},
        {"name": "北京大学校友会上海分会", "region": "上海", "contact": "上海市浦东新区"},
        {"name": "北京大学校友会广东分会", "region": "广东", "contact": "广州市天河区"},
        {"name": "北京大学校友会深圳分会", "region": "深圳", "contact": "深圳市南山区"},
        {"name": "北京大学校友会浙江分会", "region": "浙江", "contact": "杭州市西湖区"},
        {"name": "北京大学校友会江苏分会", "region": "江苏", "contact": "南京市鼓楼区"},
        {"name": "北京大学校友会四川分会", "region": "四川", "contact": "成都市武侯区"},
        {"name": "北京大学校友会湖北分会", "region": "湖北", "contact": "武汉市武昌区"},
        {"name": "北京大学校友会湖南分会", "region": "湖南", "contact": "长沙市岳麓区"},
        {"name": "北京大学校友会山东分会", "region": "山东", "contact": "济南市历下区"},
        {"name": "北京大学校友会辽宁分会", "region": "辽宁", "contact": "沈阳市和平区"},
        {"name": "北京大学校友会陕西分会", "region": "陕西", "contact": "西安市雁塔区"},
        {"name": "北京大学校友会福建分会", "region": "福建", "contact": "福州市鼓楼区"},
        {"name": "北京大学校友会天津分会", "region": "天津", "contact": "天津市南开区"},
        {"name": "北京大学校友会重庆分会", "region": "重庆", "contact": "重庆市渝北区"},
    ],
    "海外校友会": [
        {"name": "北大北美校友会", "region": "美国/加拿大", "contact": "美国旧金山湾区"},
        {"name": "北大纽约校友会", "region": "美国纽约", "contact": "美国纽约市"},
        {"name": "北大华盛顿校友会", "region": "美国华盛顿", "contact": "美国华盛顿特区"},
        {"name": "北大南加州校友会", "region": "美国南加州", "contact": "美国洛杉矶"},
        {"name": "北大英国校友会", "region": "英国", "contact": "英国伦敦"},
        {"name": "北大法国校友会", "region": "法国", "contact": "法国巴黎"},
        {"name": "北大德国校友会", "region": "德国", "contact": "德国柏林"},
        {"name": "北大日本校友会", "region": "日本", "contact": "日本东京"},
        {"name": "北大新加坡校友会", "region": "新加坡", "contact": "新加坡"},
        {"name": "北大香港校友会", "region": "香港", "contact": "中国香港"},
        {"name": "北大澳门校友会", "region": "澳门", "contact": "中国澳门"},
        {"name": "北大台湾校友会", "region": "台湾", "contact": "中国台北"},
        {"name": "北大澳大利亚校友会", "region": "澳大利亚", "contact": "澳大利亚悉尼"},
    ],
    "行业/兴趣校友会": [
        {"name": "北大金融校友会", "industry": "金融", "description": "汇聚金融领域校友，促进行业交流与合作"},
        {"name": "北大IT互联网校友会", "industry": "互联网/科技", "description": "聚焦科技互联网领域，推动技术创新与创业"},
        {"name": "北大法律人校友会", "industry": "法律", "description": "法律界校友专业交流与职业发展平台"},
        {"name": "北大医学健康校友会", "industry": "医疗健康", "description": "医学界校友学术交流与合作平台"},
        {"name": "北大创业校友会", "industry": "创业", "description": "支持校友创业，对接资源与投资"},
        {"name": "北大文化产业校友会", "industry": "文化", "description": "文化创意产业校友交流合作"},
        {"name": "北大跑团", "industry": "运动", "description": "爱好跑步的校友运动团体"},
        {"name": "北大摄影俱乐部", "industry": "摄影", "description": "摄影爱好者校友交流平台"},
    ]
}

# 校友活动
EVENTS = [
    {
        "title": "2025年北京大学返校日活动",
        "date": "2025年5月4日前后",
        "location": "北京大学校内",
        "description": "每年5月4日前后举办，欢迎历届校友返校团聚，包括校园参观、院系聚会、校友论坛等活动",
        "type": "大型活动"
    },
    {
        "title": "北大校友创业大赛",
        "date": "每年一届",
        "location": "全国巡回",
        "description": "支持校友创业项目展示与融资对接，已成功举办多届，孵化众多优秀校友企业",
        "type": "创业活动"
    },
    {
        "title": "校友讲坛",
        "date": "每月举办",
        "location": "线上线下结合",
        "description": "邀请各领域杰出校友分享经验与见解，内容涵盖学术、商业、人文等多个领域",
        "type": "学术讲座"
    },
    {
        "title": "新春校友联欢会",
        "date": "每年春节前",
        "location": "各地分会",
        "description": "各地校友会举办的新年联欢活动，校友齐聚一堂，共贺新春",
        "type": "节日活动"
    },
    {
        "title": "校友企业招聘会",
        "date": "春秋两季",
        "location": "北京大学校内",
        "description": "校友企业进校招聘，为在校学生和应届毕业生提供就业机会",
        "type": "招聘活动"
    },
    {
        "title": "北大校友公益行",
        "date": "不定期举办",
        "location": "全国各地",
        "description": "组织校友参与公益志愿活动，回馈社会，践行社会责任",
        "type": "公益活动"
    },
    {
        "title": "新生迎新会",
        "date": "每年9月",
        "location": "各地分会",
        "description": "各地校友会为新生举办迎新活动，帮助新生快速融入北大大家庭",
        "type": "迎新活动"
    },
    {
        "title": "毕业季校友分享会",
        "date": "每年6月",
        "location": "北京大学校内",
        "description": "邀请杰出校友为应届毕业生分享职业发展经验和人生感悟",
        "type": "毕业活动"
    }
]

# 校友服务
SERVICES = [
    {
        "name": "校友卡",
        "description": "北大校友可办理校友卡，凭卡可进出校园、使用图书馆、享受校内部分服务",
        "how_to": "登录北京大学信息门户或前往校友工作办公室办理",
        "fee": "工本费"
    },
    {
        "name": "校友邮箱",
        "description": "为校友提供@pku.edu.cn后缀的终身邮箱服务",
        "how_to": "通过北京大学校友网在线申请",
        "fee": "免费"
    },
    {
        "name": "图书馆借阅",
        "description": "校友可申请图书馆校外读者权限，借阅图书和使用电子资源",
        "how_to": "凭校友卡和身份证到图书馆办理",
        "fee": "部分服务收费"
    },
    {
        "name": "校园参观",
        "description": "校友可预约参观北京大学校园，包括未名湖、博雅塔、百周年纪念讲堂等景点",
        "how_to": "通过北京大学官方渠道预约",
        "fee": "免费"
    },
    {
        "name": "职业发展服务",
        "description": "为校友提供职业咨询、招聘会信息、校友导师计划等职业发展支持",
        "how_to": "关注北大就业指导中心和校友会公告",
        "fee": "免费"
    },
    {
        "name": "继续教育",
        "description": "校友可享受北大继续教育学院的各类培训课程优惠",
        "how_to": "咨询北大继续教育学院",
        "fee": "优惠收费"
    },
    {
        "name": "返校聚会服务",
        "description": "为校友班级返校聚会提供场地协调、活动策划等支持服务",
        "how_to": "提前与校友工作办公室联系预约",
        "fee": "根据具体项目"
    },
    {
        "name": "校友企业服务",
        "description": "为校友创办的企业提供宣传、招聘、合作对接等服务",
        "how_to": "联系校友会企业合作部",
        "fee": "免费"
    }
]

# 联系方式
CONTACT = {
    "校友工作办公室": {
        "address": "北京市海淀区颐和园路5号 北京大学 校友之家",
        "postcode": "100871",
        "phone": "010-62751234（示例）",
        "email": "alumni@pku.edu.cn（示例）",
        "website": "https://alumni.pku.edu.cn/",
        "wechat": "北京大学校友会（官方微信公众号）",
        "working_hours": "周一至周五 8:30-11:30, 13:30-17:00（法定节假日除外）"
    },
    "校友基金会": {
        "address": "北京大学教育基金会",
        "phone": "010-62756768（示例）",
        "email": "foundation@pku.edu.cn（示例）",
        "website": "https://www.pkuef.org.cn/"
    }
}

# 捐赠信息
DONATION = {
    "捐赠方式": [
        {"name": "在线捐赠", "description": "通过北京大学教育基金会官网在线捐赠系统进行捐赠", "channel": "微信、支付宝、银联"},
        {"name": "银行汇款", "description": "通过银行转账方式进行捐赠", "account": "北京大学教育基金会（账号详见官网）"},
        {"name": "邮政汇款", "description": "通过邮政汇款方式捐赠至基金会地址"},
        {"name": "实物捐赠", "description": "接受图书、文物、艺术品等实物捐赠"},
        {"name": "遗产捐赠", "description": "通过遗嘱方式设立遗赠"},
        {"name": "企业捐赠", "description": "企业捐赠可享受税收优惠政策"}
    ],
    "捐赠项目": [
        {"name": "学生奖助学金", "description": "设立奖学金、助学金，支持优秀学生和家庭经济困难学生"},
        {"name": "教师发展基金", "description": "支持教师教学科研、学术交流和人才培养"},
        {"name": "学科建设基金", "description": "支持学科发展、实验室建设和科研项目"},
        {"name": "校园建设基金", "description": "支持校园基础设施建设和环境改善"},
        {"name": "校友活动基金", "description": "支持校友会各类活动的开展"},
        {"name": "公益实践基金", "description": "支持学生和校友开展社会公益实践活动"},
        {"name": " unrestricted fund", "description": "不限定用途的捐赠，由学校统筹用于最需要的地方"}
    ],
    "捐赠回馈": [
        "颁发捐赠证书",
        "捐赠信息在校友会网站公示（如本人同意）",
        "达到一定金额可命名教室、实验室或建筑",
        "享受捐赠税收抵扣政策",
        "受邀参加学校重大活动"
    ],
    "tax_benefit": "企业捐赠在年度利润总额12%以内的部分，准予在计算应纳税所得额时扣除；个人捐赠额未超过纳税义务人申报的应纳税所得额30%的部分，可以从其应纳税所得额中扣除。"
}


def search_data(data, keyword):
    """在数据中搜索关键词"""
    if isinstance(data, dict):
        results = {}
        for key, value in data.items():
            found = search_data(value, keyword)
            if found:
                results[key] = found
        return results if results else None
    elif isinstance(data, list):
        results = []
        for item in data:
            found = search_data(item, keyword)
            if found:
                results.append(found)
        return results if results else None
    elif isinstance(data, str):
        if keyword.lower() in data.lower():
            return data
        return None
    else:
        return None


def get_overview():
    """获取校友会简介"""
    return {
        "category": "overview",
        "title": "北京大学校友会简介",
        "data": OVERVIEW
    }


def get_chapters(keyword=None):
    """获取各地分会信息"""
    data = CHAPTERS
    if keyword:
        filtered = search_data(CHAPTERS, keyword)
        if filtered:
            data = filtered
    return {
        "category": "chapters",
        "title": "北大校友分会" if not keyword else f"搜索'{keyword}'相关分会",
        "data": data
    }


def get_events(keyword=None):
    """获取校友活动信息"""
    data = EVENTS
    if keyword:
        filtered = [e for e in EVENTS if keyword.lower() in e["title"].lower() or 
                    keyword.lower() in e["description"].lower() or
                    keyword.lower() in e.get("type", "").lower()]
        if filtered:
            data = filtered
    return {
        "category": "events",
        "title": "校友活动" if not keyword else f"搜索'{keyword}'相关活动",
        "data": data
    }


def get_services(keyword=None):
    """获取校友服务信息"""
    data = SERVICES
    if keyword:
        filtered = [s for s in SERVICES if keyword.lower() in s["name"].lower() or 
                    keyword.lower() in s["description"].lower()]
        if filtered:
            data = filtered
    return {
        "category": "services",
        "title": "校友服务" if not keyword else f"搜索'{keyword}'相关服务",
        "data": data
    }


def get_contact():
    """获取联系方式"""
    return {
        "category": "contact",
        "title": "联系方式",
        "data": CONTACT
    }


def get_donation():
    """获取捐赠信息"""
    return {
        "category": "donation",
        "title": "校友捐赠",
        "data": DONATION
    }


def get_all():
    """获取全部信息"""
    return {
        "category": "all",
        "title": "北大校友会全部信息",
        "data": {
            "校友会简介": OVERVIEW,
            "各地分会": CHAPTERS,
            "校友活动": EVENTS,
            "校友服务": SERVICES,
            "联系方式": CONTACT,
            "校友捐赠": DONATION
        }
    }


def format_result(result):
    """格式化输出结果"""
    category = result["category"]
    title = result["title"]
    data = result["data"]
    
    output = [f"## {title}\n"]
    
    if category == "overview":
        output.append(f"**{data['name']}**（{data['english_name']}）\n")
        output.append(f"- **成立时间**：{data['founded']}")
        output.append(f"- **性质**：{data['nature']}")
        output.append(f"- **注册**：{data['register']}")
        output.append(f"- **宗旨**：{data['mission']}")
        output.append(f"- **愿景**：{data['vision']}")
        output.append(f"- **校友人数**：{data['members']}")
        output.append(f"- **分会数量**：{data['chapters']}")
        output.append(f"\n**组织架构**：")
        for org in data['organization']:
            output.append(f"- {org}")
        output.append(f"\n**品牌活动**：")
        for act in data['brand_activities']:
            output.append(f"- {act}")
            
    elif category == "chapters":
        for group, chapters in data.items():
            output.append(f"\n### {group}")
            for ch in chapters:
                name = ch.get("name", ch.get("region", ""))
                region = ch.get("region", ch.get("industry", ""))
                contact = ch.get("contact", ch.get("description", ""))
                output.append(f"- **{name}**（{region}）- {contact}")
                
    elif category == "events":
        for event in data:
            output.append(f"\n### {event['title']}")
            output.append(f"- **时间**：{event['date']}")
            output.append(f"- **地点**：{event['location']}")
            output.append(f"- **类型**：{event['type']}")
            output.append(f"- **简介**：{event['description']}")
            
    elif category == "services":
        for service in data:
            output.append(f"\n### {service['name']}")
            output.append(f"- **说明**：{service['description']}")
            output.append(f"- **办理方式**：{service['how_to']}")
            output.append(f"- **费用**：{service['fee']}")
            
    elif category == "contact":
        for dept, info in data.items():
            output.append(f"\n### {dept}")
            for key, value in info.items():
                output.append(f"- **{key}**：{value}")
                
    elif category == "donation":
        output.append("\n### 捐赠方式")
        for way in data["捐赠方式"]:
            output.append(f"- **{way['name']}**：{way['description']}")
        
        output.append("\n### 捐赠项目")
        for project in data["捐赠项目"]:
            output.append(f"- **{project['name']}**：{project['description']}")
            
        output.append("\n### 捐赠回馈")
        for benefit in data["捐赠回馈"]:
            output.append(f"- {benefit}")
            
        output.append(f"\n💡 **税收优惠**：{data['tax_benefit']}")
        
    elif category == "all":
        output.append("北大校友会信息包括以下方面，您可以告诉我想了解具体哪方面：\n")
        for key in data.keys():
            output.append(f"- {key}")
    
    output.append("\n---")
    output.append("*以上信息仅供参考，具体以北京大学校友会官方发布为准。*")
    
    return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方式: python main.py <category> [keyword]")
        print("支持的类别: overview, chapters, events, services, contact, donation, all")
        return
    
    category = sys.argv[1]
    keyword = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        if category == "overview":
            result = get_overview()
        elif category == "chapters":
            result = get_chapters(keyword)
        elif category == "events":
            result = get_events(keyword)
        elif category == "services":
            result = get_services(keyword)
        elif category == "contact":
            result = get_contact()
        elif category == "donation":
            result = get_donation()
        elif category == "all":
            result = get_all()
        else:
            print(f"不支持的类别: {category}")
            print("支持的类别: overview, chapters, events, services, contact, donation, all")
            return
        
        print(format_result(result))
        
    except Exception as e:
        print(f"查询出错: {str(e)}")


if __name__ == "__main__":
    main()

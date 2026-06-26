# -*- coding: utf-8 -*-
"""
LightReading 每日摘要推送脚本 v3.0
AI 翻译模式 - 返回英文原文，由 AI 助手翻译后推送
"""

# 修复 Windows 控制台编码问题
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import urllib.request
import json
import ssl
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import os
import http.client
import urllib.parse
import hashlib

# 已推送文章记录文件
PUSHED_FILE = os.path.join(os.path.dirname(__file__), 'pushed_history.json')

# SSL 配置
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 请求头（模拟浏览器）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
}

# Cloudflare 绕过配置
try:
    import cloudscraper
    SCRAPER = cloudscraper.create_scraper()
except ImportError:
    SCRAPER = None

# 企业微信 Webhook
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=66260502-9806-45ec-b23e-8db5223a9b27"
RSS_URL = "https://www.lightreading.com/rss.xml"

# 文章模板库 - 根据关键词匹配生成具体内容
ARTICLE_TEMPLATES = {
    'AI-RAN': {
        'title': '人工智能无线接入网：概念火热但实际部署有限',
        'points_detailed': [
            "英伟达等公司大力推动 GPU 和人工智能技术进入电信网络领域，在 MWC 等展会上高调宣传 AI-RAN 概念，展示了一系列创新技术和解决方案，但实际电信运营商部署案例非常少，目前多数项目还停留在实验室和概念验证阶段，缺乏商业化落地",
            "业界专家建议人工智能计算和无线接入网基带处理应该分离，避免混合工作负载相互干扰影响网络稳定性，这样可以让电信公司独立扩展人工智能能力而不影响核心网络性能，同时也可以根据实际需求灵活配置资源",
            "电信公司对人工智能无线接入网投资持谨慎态度，威瑞森等主要运营商明确表示不会为了人工智能而牺牲无线接入网性能，不愿承担未经验证新技术带来的风险，需要看到明确的投资回报才会考虑大规模部署",
            "当前人工智能无线接入网主要是概念验证和小规模测试阶段，距离大规模商用还需要数年时间，需要等待技术进一步成熟和成本下降到合理水平，同时运营商也需要积累相关运营经验和人才储备"
        ],
        'points_brief': [
            "英伟达推动 GPU 进入电信网络，在展会上高调宣传但实际部署案例很少，多数项目停留在实验室阶段",
            "专家建议人工智能计算和基带处理应该分离，让电信公司独立扩展能力而不影响网络稳定性",
            "运营商对投资持谨慎态度，明确表示不会为人工智能牺牲网络性能，不愿承担新技术风险",
            "目前主要是概念验证阶段，距离大规模商用还需数年，需要等待技术成熟和成本下降"
        ]
    },
    'Comcast': {
        'title': '康卡斯特商业部推出中小企业一体化套餐',
        'points_detailed': [
            "康卡斯特商业部门推出了名为 Total Solutions Advantage 的一体化解决方案计划，专门为中小企业客户提供简化的打包服务，起价为每月 60 美元，包含宽带、语音和安全服务等多种产品，大幅简化了服务选择和订购流程",
            "新套餐包含 30 天退款保证，旨在降低中小企业采用高质量网络服务的门槛，提高客户满意度和信任度，让客户可以无忧体验服务后再决定是否长期使用，体现了康卡斯特对服务质量的信心",
            "该计划整合了康卡斯特的多种商业服务产品，包括高速宽带、企业语音和网络安全服务，为客户提供一站式解决方案，减少了中小企业需要与多个供应商打交道的复杂性，提高了服务效率",
            "此举是康卡斯特加强与传统电信运营商竞争的重要举措，目标是在中小企业市场获得更大份额，通过简化套餐结构和降低价格门槛吸引更多客户，同时也提升了客户留存率和满意度"
        ],
        'points_brief': [
            "康卡斯特推出 Total Solutions Advantage 一体化计划，起价每月 60 美元，包含宽带语音和安全服务",
            "套餐含 30 天退款保证，降低中小企业采用门槛，提高客户满意度和信任度",
            "整合多种商业服务产品，提供一站式解决方案，减少客户与多供应商打交道的复杂性",
            "旨在加强在中小企业市场的竞争力，通过简化结构和降低价格吸引更多客户"
        ]
    },
    'DOCSIS': {
        'title': '有线电视运营商部署 DOCSIS 4.0 仍需谨慎评估成本',
        'points_detailed': [
            "有线电视运营商在部署 DOCSIS 4.0 技术时仍然将成本作为关键决策因素，需要仔细评估投资回报率和长期运营成本，包括设备升级、网络改造和人员培训等各项支出，确保投资能够带来可持续的商业回报",
            "DOCSIS 4.0 能够提供多千兆宽带速度和更高的网络可靠性，支持对称上下行速率，但升级现有有线电视网络基础设施需要大量资本支出，包括更换放大器、节点设备和用户端调制解调器等",
            "运营商需要在光纤到户和 DOCSIS 4.0 之间做出选择，两种技术路线各有优劣，光纤性能更好但成本更高，DOCSIS 可以利用现有同轴电缆网络但带宽有限，需要根据现有网络状况和客户需求决定",
            "行业分析师建议运营商根据现有网络状况和客户需求制定渐进式升级策略，避免盲目投资造成资源浪费，可以先在需求旺盛区域试点，验证商业模式后再逐步扩大部署范围"
        ],
        'points_brief': [
            "成本是有线电视运营商部署 DOCSIS 4.0 的关键决策因素，需评估投资回报率和长期运营成本",
            "DOCSIS 4.0 提供多千兆速度和更高可靠性，但升级现有网络需要大量资本支出",
            "运营商需要在光纤和 DOCSIS 技术路线之间选择，根据现有网络状况和客户需求决定",
            "建议制定渐进式升级策略，先在需求旺盛区域试点，验证商业模式后再扩大部署"
        ]
    },
    'Harmonic': {
        'title': '台湾 KBRO 有线电视选择 Harmonic 进行网络升级',
        'points_detailed': [
            "台湾 KBRO 有线电视运营商选择了 Harmonic 公司进行宽带接入网络升级，采用光纤按需服务方案，利用 Harmonic 的虚拟化宽带平台 cOS 实现灵活的网络资源配置，支持多千兆宽带服务交付，提升用户体验和网络竞争力",
            "Harmonic 的虚拟化宽带平台 cOS 为 KBRO 提供灵活的网络扩展能力，支持多千兆宽带服务交付，可以根据用户需求动态分配带宽资源，提高网络利用率和服务质量，同时降低运营成本和能耗",
            "该升级方案与 KBRO 的 DOCSIS 高分裂网络现代化战略相辅相成，实现按需光纤扩展，在不影响现有服务的前提下逐步推进网络升级，平衡了投资成本和性能提升的需求",
            "网络升级后将支持更高带宽服务，为运营商创造新的收入增长点，提升客户体验和满意度，增强在竞争激烈的台湾宽带市场中的竞争力，同时也为未来 5G 和物联网应用奠定基础"
        ],
        'points_brief': [
            "台湾 KBRO 有线电视选择 Harmonic 进行网络升级，采用光纤按需服务方案提升竞争力",
            "Harmonic cOS 虚拟化平台提供灵活网络扩展能力，支持多千兆服务交付和动态带宽分配",
            "升级方案与 DOCSIS 网络现代化战略相辅相成，实现按需光纤扩展，平衡投资和性能需求",
            "升级后支持更高带宽服务，创造新收入增长点，提升客户体验和市场竞争力"
        ]
    },
    '5G': {
        'title': '5G 网络部署和应用新进展',
        'points_detailed': [
            "全球主要电信运营商继续推进 5G 网络部署，扩大覆盖范围并提升网络容量和性能，包括增加基站密度、优化网络参数和引入新技术等手段，为用户提供更快速度和更稳定的 5G 服务体验",
            "5G 独立组网部署加速，支持网络切片和超低延迟等高级功能，为工业物联网、自动驾驶和远程医疗等应用铺平道路，让运营商可以为企业客户提供定制化的网络服务和差异化定价",
            "运营商探索 5G 新应用场景，包括固定无线接入、边缘计算和企业专网等领域，寻找新的收入增长点和商业模式，同时也在测试 5G 广播和车联网等创新应用，拓展 5G 技术的商业价值",
            "5G 投资回报仍是运营商关注的焦点，需要平衡网络建设和盈利能力，避免过度投资导致财务压力，同时也在探索网络共享和开放 RAN 等降低成本的新模式，提高投资效率和回报率"
        ],
        'points_brief': [
            "全球运营商继续推进 5G 网络部署，扩大覆盖范围并提升容量性能，为用户提供更优质服务",
            "5G 独立组网加速，支持网络切片和超低延迟功能，为工业物联网等应用铺平道路",
            "运营商探索固定无线接入、边缘计算和企业专网等新场景，寻找收入增长点和商业模式",
            "5G 投资回报仍是关注焦点，需要平衡网络建设和盈利能力，探索降低成本新模式"
        ]
    },
    'Netcracker': {
        'title': 'Netcracker 与 Rakuten Mobile 扩展合作',
        'points_brief': [
            "Netcracker 与 Rakuten Mobile 宣布扩大合作关系，深化在云原生 BSS/OSS 领域的战略合作",
            "合作将支持 Rakuten Mobile 的开放 RAN 和云原生网络架构，提升网络运营效率",
            "Netcracker 提供自动化编排和服务管理解决方案，助力 Rakuten 降低运营成本",
            "此次扩展合作标志着云原生电信管理平台在移动网络领域的进一步应用"
        ],
        'points_detailed': [
            "Netcracker 与 Rakuten Mobile 宣布扩大合作关系，深化在云原生 BSS/OSS 领域的战略合作，为 Rakuten 的全球移动网络提供更强大的自动化管理能力",
            "合作将支持 Rakuten Mobile 的开放 RAN 和云原生网络架构，通过 Netcracker 的解决方案实现网络资源的动态编排和优化，提升网络运营效率和服务质量",
            "Netcracker 提供自动化编排和服务管理解决方案，帮助 Rakuten Mobile 降低运营成本，加快新服务上线速度，同时支持多厂商设备的统一管理",
            "此次扩展合作标志着云原生电信管理平台在移动网络领域的进一步应用，为其他运营商提供了可参考的云化转型路径"
        ]
    },
    'CableTech': {
        'title': '有线电视行业技术创新动态',
        'points_brief': [
            "有线电视行业持续推进技术创新，在宽带速度、网络可靠性和服务质量方面取得进展",
            "行业组织表彰在电缆技术领域做出突出贡献的专业人士和团队",
            "运营商在新技术部署中平衡性能、成本和风险，制定合理的投资计划",
            "预计相关技术将逐步应用于实际网络，提升用户体验和行业竞争力"
        ],
        'points_detailed': [
            "有线电视行业持续推进技术创新，在宽带速度、网络可靠性和服务质量方面取得显著进展，包括 DOCSIS 技术演进、光纤混合网络升级等多个方向",
            "行业组织如 Syndeo Institute 等表彰在电缆技术领域做出突出贡献的专业人士和团队，推动行业知识传承和技术发展",
            "运营商在新技术部署中需要平衡性能、成本和风险，避免盲目投资造成资源浪费，同时考虑客户需求和市场竞争压力",
            "预计相关技术将逐步应用于实际网络，提升用户体验和行业竞争力，为有线电视运营商在与其他宽带技术竞争中保持优势"
        ]
    },
    'OSSBSS': {
        'title': '电信运营支撑系统最新发展',
        'points_brief': [
            "电信运营商持续投资 OSS/BSS 系统现代化，提升网络管理和客户服务能力",
            "云原生和自动化成为运营支撑系统发展的主要趋势，降低运营成本",
            "供应商扩大与运营商合作，提供定制化的运营管理和计费解决方案",
            "新系统支持更灵活的服务交付和更快的产品上线速度"
        ],
        'points_detailed': [
            "电信运营商持续投资 OSS/BSS 系统现代化，通过引入云原生架构和自动化技术提升网络管理和客户服务能力，降低人工干预需求",
            "云原生和自动化成为运营支撑系统发展的主要趋势，帮助运营商实现网络资源的动态配置和优化，显著降低运营成本",
            "供应商如 Netcracker 等扩大与运营商合作，提供定制化的运营管理和计费解决方案，支持多厂商设备和复杂网络环境",
            "新系统支持更灵活的服务交付和更快的产品上线速度，使运营商能够快速响应市场需求变化，推出创新服务"
        ]
    },
    'Nokia': {
        'title': '诺基亚发布 AI 时代光网络路线图',
        'points_brief': [
            "诺基亚公布面向 AI 时代的光网络发展战略和技术路线图",
            "新方案支持更高带宽和更低延迟，满足 AI 训练和推理需求",
            "光网络升级将帮助运营商应对 AI 带来的流量增长挑战",
            "诺基亚与运营商合作推进光网络现代化和智能化演进"
        ],
        'points_detailed': [
            "诺基亚正式发布面向人工智能时代的光网络路线图，详细阐述了未来光网络架构的演进方向和技术创新点",
            "新方案重点支持 AI 训练和推理所需的高带宽、低延迟网络特性，包括 800G 和 1.6T 光传输技术",
            "光网络升级将帮助电信运营商有效应对 AI 应用带来的流量爆发式增长，提升网络容量和效率",
            "诺基亚表示将与全球主要运营商紧密合作，共同推进光网络的现代化改造和智能化升级"
        ]
    },
    'TMobile': {
        'title': 'T-Mobile 广告争议持续发酵',
        'points_brief': [
            "联邦法院支持 Verizon 诉求，要求 T-Mobile 停止特定广告",
            "T-Mobile 广告声称用户切换可省钱，Verizon 认为存在误导",
            "T-Mobile 坚持广告内容真实，表示将继续应诉",
            "两大运营商市场竞争激烈，广告战成为新战场"
        ],
        'points_detailed': [
            "美国联邦法院作出裁决，支持 Verizon 的诉讼请求，要求 T-Mobile 停止播放声称用户切换网络可省钱的广告",
            "Verizon 认为 T-Mobile 的广告存在误导性，夸大了切换网络所能带来的费用节省，可能误导消费者",
            "T-Mobile 方面坚持其广告内容真实准确，表示将继续应诉并捍卫自己的营销权利",
            "此次广告争议反映了美国主要电信运营商之间激烈的市场竞争，广告战已成为新的竞争焦点"
        ]
    },
    '6G': {
        'title': '6G 研发竞赛提前打响',
        'points_brief': [
            "ITU 正式启动 6G 标准制定流程，预计 2030 年实现商用部署",
            "6G 目标峰值速率达到 1Tbps，延迟低于 0.1 毫秒，支持全息通信",
            "太赫兹频段和卫星互联网成为 6G 关键技术方向，中美欧展开激烈竞争",
            "6G 将实现天地一体化网络，支持沉浸式 XR、数字孪生等新应用"
        ],
        'points_detailed': [
            "国际电信联盟 (ITU) 正式启动 6G 标准制定流程，制定了详细的时间表和技术路线图，预计 2030 年前后实现商用部署",
            "6G 技术目标包括峰值速率达到 1Tbps、延迟低于 0.1 毫秒、支持全息通信和沉浸式体验，比 5G 性能提升 10-100 倍",
            "太赫兹频段通信和卫星互联网成为 6G 关键技术方向，中国、美国、欧洲等主要经济体已展开激烈的技术竞争和专利布局",
            "6G 将实现天地一体化网络覆盖，支持沉浸式 XR、数字孪生、智能交通等新应用，彻底改变人类通信和生活方式"
        ]
    },
    'KDDI': {
        'title': 'KDDI 16 亿美元欺诈案调查公布',
        'points_brief': [
            "日本 KDDI 公司 16 亿美元欺诈案调查结果出炉",
            "子公司虚构广告交易，暴露公司风险管理漏洞",
            "调查指出缺乏专业知识和风控不力是主因",
            "KDDI 承诺加强内控和合规管理"
        ],
        'points_detailed': [
            "日本电信巨头 KDDI 公司公布了 16 亿美元欺诈案的详细调查结果，揭示了案件的具体经过和原因",
            "调查发现 KDDI 子公司通过虚构广告交易进行财务欺诈，金额高达 16 亿美元，持续时间较长",
            "调查报告指出，公司缺乏相关专业知识和风险管理制度不健全是导致欺诈发生的主要原因",
            "KDDI 表示将全面加强内部控制和合规管理体系，防止类似事件再次发生，恢复投资者信心"
        ]
    },
    'default': {
        'title': '电信行业最新动态和技术分析',
        'points_detailed': [
            "文章介绍了电信行业的最新动态和技术发展趋势，分析了市场变化和竞争格局，包括主要运营商的战略调整、新技术的商业化进展和行业整合趋势等内容，为读者提供全面的行业洞察",
            "行业专家对相关技术进行了评估，指出了当前面临的主要挑战和需要解决的问题，包括技术标准、成本控制和商业模式等方面的障碍，同时也提出了可能的解决方案和发展建议",
            "电信运营商对该技术持谨慎态度，需要在性能、成本和风险之间做出平衡，避免盲目投资造成资源浪费，同时也要考虑客户需求和市场竞争压力，制定合理的技术路线图和投资计划",
            "预计该技术距离大规模商用还需要一段时间，但随着技术成熟将逐步得到应用，运营商需要根据自身情况制定渐进式部署策略，先在小范围试点验证后再逐步扩大应用范围"
        ],
        'points_brief': [
            "文章介绍了电信行业最新动态和技术发展趋势，分析市场变化和竞争格局，提供全面行业洞察",
            "行业专家对相关技术进行评估，指出当前面临的主要挑战和需要解决的问题，提出解决方案建议",
            "运营商对该技术持谨慎态度，需要在性能成本和风险之间平衡，制定合理技术路线图和投资计划",
            "预计该技术距离大规模商用还需一段时间，但随着技术成熟将逐步应用，建议渐进式部署策略"
        ]
    }
}

def extract_points_from_description(description, max_points=4):
    """从 RSS description 提取要点（简单版本，用于回退）"""
    if not description:
        return None
    
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', description)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 按句子分割
    sentences = re.split(r'[.!?。！？]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    
    # 取前几个句子作为要点
    points = []
    for sent in sentences[:max_points]:
        if len(sent) > 15 and len(sent) < 300:
            points.append(sent)
    
    return points if points else None

def smart_split_sentence(sent, max_len=80):
    """智能拆分长句，保护数字 + 单位组合不被截断"""
    if len(sent) <= max_len:
        return [sent]
    
    parts = []
    # 在连词处拆分（and, but, with, as, which, that）
    split_patterns = [
        r'\s+(?=and\s+)',
        r'\s+(?=but\s+)',
        r'\s+(?=with\s+)',
        r'\s+(?=as\s+)',
        r'\s+(?=which\s+)',
        r'\s+(?=that\s+)',
    ]
    
    current = sent
    for pattern in split_patterns:
        if len(current) <= max_len:
            break
        chunks = re.split(pattern, current)
        if len(chunks) > 1:
            current = chunks[0]
            for chunk in chunks[1:]:
                if len(current) + len(chunk) <= max_len:
                    current += ' ' + chunk
                else:
                    if len(current) > 10:
                        parts.append(current)
                    current = chunk
            if current:
                parts.append(current)
    
    if not parts or len(parts) == 1:
        # 无法智能拆分，强制按逗号拆分
        parts = [s.strip() for s in re.split(r',\s*', sent) if len(s.strip()) > 10]
    
    return parts if parts else [sent]

def polish_translation(text):
    """润色翻译结果，优化生硬表达"""
    if not text:
        return text
    
    # 清理乱码和非中文字符（保留英文、数字、标点）
    # 移除无法识别的字节序列
    text = re.sub(r'[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # 移除奇怪的标签残留
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    
    # 常见翻译问题修正 - 比喻和习语
    replacements = {
        # 比喻表达
        '喜马拉雅山的一面': '像喜马拉雅山一样大起大落',
        '有喜马拉雅山的一面': '起伏之大犹如喜马拉雅山',
        '喜马拉雅山方面的': '悬殊极大的',
        # 常见翻译问题
        '的老板': 'CEO',
        '的 boss': 'CEO',
        '该公司': '公司',
        '该技术': '这项技术',
        '被认为': '业界认为',
        '并且': '并',
        '而且': '并',
        '此外': '同时',
        '进行了': '进行',
        '做出了': '做出',
        ' Inc.': '公司',
        ' Corp.': '公司',
        ' Ltd.': '公司',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # 清理多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 清理奇怪的后缀
    text = re.sub(r'\(,.*?\)', '', text)
    text = re.sub(r'\([^)]{50,}\)', '', text)  # 移除超长括号内容
    
    # 移除末尾的标点重复
    text = re.sub(r'[。！？]{2,}$', '。', text)
    
    # 修复被截断的数字（如"约 31"、"15 瑞典克朗"）
    # 如果句子以数字结尾且没有完整单位，补充省略号
    if re.search(r'[约达到仅为][0-9\.]+$', text) and len(text) < 60:
        text = text + '...'  # 标记为不完整
    
    # 修复货币单位缺失（如"15 瑞典克朗"应该是"152 亿瑞典克朗"）
    # 检测模式：数字 + 货币单位，但数字明显不完整
    if re.search(r'仅为\d{1,2}瑞典克朗$', text):
        text = text.replace('瑞典克朗', '亿瑞典克朗（数字可能被截断）')
    if re.search(r'约\d{1,2}瑞典克朗$', text):
        text = text.replace('瑞典克朗', '亿瑞典克朗（数字可能被截断）')
    
    return text

def translate_text(text, from_lang='en', to_lang='zh', retries=2):
    """翻译文本 - v3.0 AI 翻译模式，返回英文原文由 AI 助手翻译"""
    if not text or len(text.strip()) < 3:
        return text
    
    # 限制长度
    if len(text) > 2000:
        text = text[:2000]
    
    # v3.0: 直接返回英文原文，由 AI 助手翻译
    return text

def polish_translation(text):
    """润色翻译结果 - v3.0 由 AI 处理，此函数保留但不再自动调用"""
    if not text:
        return text
    return text

def extract_and_translate_points(title, description, link='', detailed=True, full_content=''):
    """从 RSS description 或全文提取并翻译要点
    
    Args:
        detailed: True=重点推荐 (4 个要点，每点 3-4 句), False=其他精选 (3 个要点，每点 2-3 句)
    """
    # 翻译标题
    title_trans = translate_text(title)
    
    points = []
    raw_sentences = []
    
    # 优先使用全文内容
    if full_content:
        # 分段处理（用分隔符分割）
        if ' <SEP> ' in full_content:
            segments = full_content.split(' <SEP> ')
        else:
            segments = [full_content]
        
        # 收集所有句子
        for seg in segments[:10]:  # 最多处理 10 段
            # 彻底清理分隔符
            seg = seg.replace('<SEP>', ' ').replace('|||', ' ').strip()
            if len(seg) < 30:
                continue
            # 按句号分割
            subs = re.split(r'[.!?]', seg)
            for s in subs:
                s = s.strip()
                # 限制句子长度，避免翻译截断（>200 字符的长句需要拆分）
                if len(s) > 20 and len(s) < 300:
                    raw_sentences.append(s)
    
    # 如果没有全文内容，使用 RSS 摘要
    elif description:
        text = re.sub(r'<[^>]+>', ' ', description)
        text = re.sub(r'\s+', ' ', text).strip()
        subs = re.split(r'[.!?]', text)
        for s in subs:
            s = s.strip()
            if len(s) > 20 and len(s) < 300:
                raw_sentences.append(s)
    
    # 逐段翻译（保持内容独立）
    if raw_sentences:
        count = 0
        title_lower = title.lower()
        for sent in raw_sentences[:20]:  # 最多处理 20 句，增加候选池
            # 跳过太短的句子
            if len(sent) < 25:
                continue
            # 跳过和标题几乎相同的句子（但允许部分重叠）
            if len(title_lower) > 20 and abs(len(sent) - len(title_lower)) < 10 and title_lower in sent.lower():
                continue
            
            # 长句拆分：如果句子超过 120 字符，智能拆分后分别翻译再组合
            if len(sent) > 120:
                trans_parts = []
                # 优先在句号、分号处拆分
                sub_sentences = re.split(r'[;]\s*', sent)
                for sub in sub_sentences:
                    sub = sub.strip()
                    if len(sub) > 100:
                        # 还是太长，按逗号拆分，但要保护数字+单位
                        # 先在"，"处拆分
                        clauses = re.split(r',\s*(?![0-9])', sub)  # 逗号后不是数字才拆分
                        for clause in clauses:
                            clause = clause.strip()
                            if len(clause) > 10:
                                trans_part = translate_text(clause)
                                if trans_part and len(trans_part) > 5:
                                    trans_parts.append(trans_part)
                    elif len(sub) > 15:
                        trans_part = translate_text(sub)
                        if trans_part and len(trans_part) > 5:
                            trans_parts.append(trans_part)
                trans = ''.join(trans_parts) if trans_parts else translate_text(sent)
            else:
                trans = translate_text(sent)
            
            if trans and len(trans) > 15:
                # 清理翻译结果
                trans = trans.strip()
                trans = trans.replace('<SEP>', '').replace('|||', '')
                # 跳过像广告的内容
                if len(trans) > 15 and 'subscribe' not in trans.lower() and 'newsletter' not in trans.lower():
                    # 检查是否和标题太相似
                    if len(title_trans) > 20 and trans[:20] == title_trans[:20]:
                        continue
                    points.append(trans)
                    count += 1
                    max_points = 4 if detailed else 3  # 重点推荐 4 个，其他精选 3 个
                    if count >= max_points:
                        break
    
    # 去重（避免标题和正文重复）
    seen = set()
    unique_points = []
    for p in points:
        key = p[:20].lower()
        if key not in seen:
            seen.add(key)
            unique_points.append(p)
    points = unique_points
    
    # 确保有足够的要点
    min_points = 3 if detailed else 3
    while len(points) < min_points:
        points.append('暂无更多详细内容')
    
    # 根据模式调整要点数量
    if detailed:
        points = points[:4]  # 重点推荐 4 个要点
    else:
        points = points[:3]  # 其他精选 3 个要点
    
    return {
        'title': title_trans,
        'points': points
    }

def match_template(title, description, link='', detailed=True):
    """翻译文章标题和内容，不套用模板"""
    result = extract_and_translate_points(title, description, link, detailed=detailed)
    
    return {
        'title': result.get('title', title[:60] + '...' if len(title) > 60 else title),
        'points_detailed': result.get('points', ['暂无内容摘要']),
        'points_brief': result.get('points', ['暂无内容摘要'])
    }

def fetch_article_content(url):
    """抓取文章全文内容 - 使用 cloudscraper 绕过 Cloudflare"""
    
    # 使用 cloudscraper 抓取网页（绕过 Cloudflare）
    if SCRAPER:
        try:
            print("    [网页] 正在抓取全文...")
            resp = SCRAPER.get(url, timeout=30)
            if resp.status_code == 200:
                html = resp.text
                
                # 尝试提取文章主体区域（根据 URL 判断）
                if 'huawei' in url.lower():
                    # 华为文章：提取特定区域
                    main_article = re.search(r'<div class="article-body"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
                    if main_article:
                        html = main_article.group(1)
                
                # 提取所有段落（包括包含 HTML 实体的）
                raw_paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
                
                # 处理段落：移除 HTML 标签，解码实体
                paragraphs = []
                for p in raw_paragraphs:
                    # 移除 HTML 标签
                    text = re.sub(r'<[^>]+>', ' ', p)
                    # 移除多余空白
                    text = re.sub(r'\s+', ' ', text).strip()
                    # 解码 HTML 实体
                    text = re.sub(r'&#x27;', "'", text)
                    text = re.sub(r'&quot;', '"', text)
                    text = re.sub(r'&amp;', '&', text)
                    text = re.sub(r'&nbsp;', ' ', text)
                    paragraphs.append(text)
                
                # 过滤：至少 50 字符，排除广告/footer
                valid = []
                skip_keywords = ['subscribe', 'advertisement', 'copyright', 'privacy', 'newsletter', 'power an unparalleled', 'contact us', 'about us', 'techtarget', 'informa']
                for p in paragraphs:
                    if len(p) < 50:
                        continue
                    p_lower = p.lower()
                    if any(kw in p_lower for kw in skip_keywords):
                        continue
                    valid.append(p)
                
                if valid:
                    # 用独特分隔符连接（避免被翻译）
                    content = ' <SEP> '.join(valid[:12])
                    print("    [网页] 抓取成功（{} 字符，{} 段）".format(len(content), len(valid)))
                    return content
        except Exception as e:
            print("    [网页] 抓取失败：{}".format(str(e)[:60]))
    
    return ''

def fetch_rss():
    """获取 RSS feed 内容（带重试机制）"""
    # 重试 3 次
    for attempt in range(1, 4):
        print("获取 RSS (尝试 {}/3)...".format(attempt))
        
        # 尝试 1: cloudscraper（绕过 Cloudflare）
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper()
            print("  使用 cloudscraper...")
            resp = scraper.get(RSS_URL, timeout=60)  # 增加到 60 秒
            if resp.status_code == 200 and resp.text.strip().startswith('<?xml'):
                print("  RSS 获取成功（{} 字符）".format(len(resp.text)))
                return resp.text
            else:
                print("  RSS 内容异常：{}".format(resp.text[:200]))
        except Exception as e:
            print("  cloudscraper 失败：{}".format(str(e)[:60]))
        
        # 尝试 2: urllib（回退）
        try:
            req = urllib.request.Request(RSS_URL, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60, context=ssl_context) as response:  # 增加到 60 秒
                content = response.read().decode('utf-8', errors='ignore')
                print("  urllib 获取成功（{} 字符）".format(len(content)))
                # 调试：检查内容是否为有效 RSS
                if not content.strip().startswith('<?xml'):
                    print("  警告：返回内容不是 XML，可能是 HTML 错误页面")
                    print("  内容预览：{}".format(content[:200]))
                    continue  # 尝试下一次
                return content
        except Exception as e:
            print("  urllib 失败：{}".format(str(e)[:50]))
        
        # 等待重试
        if attempt < 3:
            import time
            print("  等待 5 秒后重试...")
            time.sleep(5)
    
    # 3 次都失败，返回空 RSS
    print("RSS 获取失败，返回空内容")
    return '<?xml version="1.0"?><rss></rss>'

def parse_rss(xml_content):
    """解析 RSS feed，提取文章信息"""
    articles = []
    namespaces = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
    }
    
    try:
        root = ET.fromstring(xml_content)
        for item in root.findall('.//item'):
            title_elem = item.find('title')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            author_elem = item.find('dc:creator', namespaces)
            desc_elem = item.find('description')
            content_elem = item.find('content:encoded', namespaces)
            
            if title_elem is not None and link_elem is not None:
                title = title_elem.text or ''
                link = link_elem.text or ''
                
                # 解析日期
                pub_date = ''
                if pub_date_elem is not None and pub_date_elem.text:
                    try:
                        date_str = pub_date_elem.text
                        if 'GMT' in date_str:
                            date_str = date_str.replace('GMT', '+0000')
                        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                        pub_date = date_obj.strftime('%Y-%m-%d')
                    except:
                        pub_date = pub_date_elem.text[:10] if pub_date_elem.text else ''
                
                # 获取作者
                author = ''
                if author_elem is not None and author_elem.text:
                    author = author_elem.text.strip()
                
                # 获取描述 - 优先使用 content:encoded（完整内容）
                description = ''
                if content_elem is not None and content_elem.text:
                    description = content_elem.text.strip()
                elif desc_elem is not None and desc_elem.text:
                    description = desc_elem.text.strip()
                
                # 如果内容还是不够，尝试从 description 补充
                if len(description) < 100 and desc_elem is not None and desc_elem.text:
                    desc_text = desc_elem.text.strip()
                    if desc_text and desc_text not in description:
                        description = desc_text + ' ' + description
                
                # 判断是否 Iain Morris 的文章（详细模式）
                is_iain = author and 'iain morris' in author.lower()
                

                
                # 匹配模板或提取内容
                template = match_template(title, description, link, detailed=is_iain)
                
                articles.append({
                    'title': title,
                    'title_cn': template['title'],
                    'link': link,
                    'pub_date': pub_date,
                    'author': author,
                    'description': description,
                    'points_detailed': template['points_detailed'],
                    'points_brief': template['points_brief']
                })
    except Exception as e:
        print("RSS 解析错误：{}".format(e))
    
    return articles

def is_iain_morris(author):
    """判断是否为 Iain Morris 的文章"""
    if not author:
        return False
    return any(name.lower() in author.lower() for name in ['iain morris', 'iain'])

def is_telecom_related(title, description):
    """判断是否与电信相关"""
    keywords = ['5g', '6g', 'telecom', 'network', 'wireless', 'broadband', 
                'fiber', 'mobile', 'carrier', 'operator', 'ran', 'cable', 
                'docsis', 'ai', 'gpu', 'business']
    text = (title + ' ' + description).lower()
    return any(kw in text for kw in keywords)

def load_pushed_history():
    """加载已推送文章记录"""
    if os.path.exists(PUSHED_FILE):
        try:
            with open(PUSHED_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 清理 7 天前的记录
                cutoff = datetime.now().timestamp() - 7 * 24 * 3600
                data = {k: v for k, v in data.items() if v > cutoff}
                return data
        except:
            pass
    return {}

def save_pushed_history(history):
    """保存已推送文章记录"""
    try:
        with open(PUSHED_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("保存推送历史失败：{}".format(e))

def get_article_key(article):
    """生成文章唯一标识（用于去重）"""
    # 使用标题 + 链接的组合作为唯一标识
    key_str = (article.get('title', '') + '|' + article.get('link', '')).lower().strip()
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()

def create_message_english(articles):
    """创建英文推送消息（用于 AI 翻译模式）"""
    # 加载已推送历史
    pushed_history = load_pushed_history()
    
    # 过滤已推送的文章
    filtered_articles = []
    for a in articles:
        key = get_article_key(a)
        if key not in pushed_history:
            filtered_articles.append(a)
    
    articles = filtered_articles
    
    iain_articles = [a for a in articles if is_iain_morris(a['author'])]
    telecom_articles = [a for a in articles if is_telecom_related(a['title'], a['description']) and not is_iain_morris(a['author'])]
    
    # 选择文章
    if iain_articles:
        featured = iain_articles[0]
        others = telecom_articles[:3]
    else:
        all_articles = articles[:4]
        featured = all_articles[0] if all_articles else None
        others = all_articles[1:4] if len(all_articles) > 1 else []
    
    if not featured:
        return "No new LightReading articles today."
    
    # 构建英文消息
    message = "LightReading Daily Digest\n\n"
    
    # Featured article
    message += "[FEATURED]\n"
    message += "{}\n".format(featured['title'])
    message += "Author: {}\n".format(featured['author'] or 'Unknown')
    message += "Published: {}\n\n".format(featured['pub_date'])
    
    # 尝试获取全文内容
    featured_text = ''
    try:
        from parse_email import extract_article_from_email
        import os
        emails_dir = os.path.join(os.path.dirname(__file__), 'emails')
        latest_file = None
        if os.path.exists(emails_dir):
            files = sorted(os.listdir(emails_dir), reverse=True)
            for f in files:
                if f.endswith('.eml') or f.endswith('.html'):
                    latest_file = os.path.join(emails_dir, f)
                    break
        if latest_file:
            with open(latest_file, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            email_articles_list = extract_article_from_email(html)
            for art in email_articles_list:
                if ' - ' in art:
                    title, summary = art.split(' - ', 1)
                    if featured['title'].strip().lower() in title.lower():
                        featured_text = summary.strip()
                        break
    except:
        pass
    
    if featured_text:
        message += "Summary: {}\n\n".format(featured_text[:500])
    else:
        # 尝试抓取网页
        try:
            import socket
            socket.setdefaulttimeout(5)
            web_content = fetch_article_content(featured['link'])
            if web_content and len(web_content) > 200:
                message += "Summary: {}\n\n".format(web_content[:500])
        except:
            pass
    
    message += "Link: {}\n\n".format(featured['link'])
    
    # Other articles
    if others:
        message += "[OTHER STORIES]\n\n"
        for idx, article in enumerate(others[:3], 1):
            message += "{}. {}\n".format(idx, article['title'])
            message += "   Author: {}\n".format(article['author'] or 'Unknown')
            message += "   Link: {}\n\n".format(article['link'])
    
    message += "\nSource: LightReading.com"
    
    return message

def create_message(articles):
    """创建推送消息"""
    # 加载已推送历史
    pushed_history = load_pushed_history()
    print("已推送文章记录：{} 篇".format(len(pushed_history)))
    
    # 过滤已推送的文章
    filtered_articles = []
    for a in articles:
        key = get_article_key(a)
        if key not in pushed_history:
            filtered_articles.append(a)
        else:
            print("跳过已推送文章：{}".format(a['title'][:50]))
    
    articles = filtered_articles
    print("去重后剩余文章：{} 篇".format(len(articles)))
    
    iain_articles = [a for a in articles if is_iain_morris(a['author'])]
    telecom_articles = [a for a in articles if is_telecom_related(a['title'], a['description']) and not is_iain_morris(a['author'])]
    
    print("Iain Morris 文章：{} 篇".format(len(iain_articles)))
    print("电信相关文章：{} 篇".format(len(telecom_articles)))
    
    # 选择文章：重点推荐 1 篇 Iain Morris，其他精选 3 篇
    if iain_articles:
        featured = iain_articles[0]
        others = telecom_articles[:3]  # 改为 3 篇
    else:
        all_articles = articles[:4]
        featured = all_articles[0] if all_articles else None
        others = all_articles[1:4] if len(all_articles) > 1 else []
    
    if not featured:
        return "抱歉，今日未能获取到 LightReading 文章，请稍后重试。"
    
    # 构建消息
    message = "LightReading 每日摘要\n\n"
    
    # 重点推荐 - Iain Morris 文章（尝试抓取全文获取更多内容）
    message += "【重点推荐】\n"
    message += "{}\n".format(featured['title_cn'])
    message += "作者：{}\n".format(featured['author'] or 'Unknown')
    message += "发布时间：{}\n\n".format(featured['pub_date'])
    
    # 尝试从邮件获取全文内容
    print("正在从邮件获取全文内容...")
    
    # 先获取邮件中的所有文章
    email_articles = {}
    try:
        from parse_email import extract_article_from_email
        import os
        emails_dir = os.path.join(os.path.dirname(__file__), 'emails')
        latest_file = None
        if os.path.exists(emails_dir):
            files = sorted(os.listdir(emails_dir), reverse=True)
            for f in files:
                if f.endswith('.eml') or f.endswith('.html'):
                    latest_file = os.path.join(emails_dir, f)
                    break
        if latest_file:
            with open(latest_file, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            articles = extract_article_from_email(html)
            # 解析邮件文章：标题 - 摘要 格式
            for art in articles:
                if ' - ' in art:
                    title, summary = art.split(' - ', 1)
                    email_articles[title.strip().lower()] = summary.strip()
            print("从邮件解析到 {} 篇文章".format(len(email_articles)))
    except Exception as e:
        print("解析邮件文章失败：{}".format(str(e)[:50]))
    
    # 尝试匹配当前文章
    featured_text = ''
    title_key = featured['title'].strip().lower()
    if title_key in email_articles:
        featured_text = email_articles[title_key]
        print("匹配到邮件内容：{}".format(featured_text[:50]))
    else:
        # 尝试部分匹配
        for key, val in email_articles.items():
            if title_key[:15] in key or key[:15] in title_key:
                featured_text = val
                print("部分匹配到邮件内容：{}".format(featured_text[:50]))
                break
    
    # 优先使用邮件内容
    if featured_text:
        print("使用邮件内容生成要点...")
        template = extract_and_translate_points(featured['title'], featured_text, featured['link'], detailed=True)
        points = template['points']
    # 其次尝试网页抓取（不稳定，快速失败）
    else:
        print("尝试抓取网页全文（5 秒超时）...")
        try:
            import socket
            socket.setdefaulttimeout(5)
            web_content = fetch_article_content(featured['link'])
            if web_content and len(web_content) > 200:
                print("网页抓取成功，生成要点...")
                template = extract_and_translate_points(featured['title'], web_content, featured['link'], detailed=True)
                points = template['points']
            else:
                raise Exception("内容太少")
        except Exception as e:
            print("网页抓取失败，使用 RSS 摘要")
            points = [p for p in featured['points_detailed'] if p and len(p.strip()) > 0]
    
    if points:
        for i, point in enumerate(points, 1):
            message += "要点{}：{}\n".format(i, point)
    else:
        message += "暂无详细内容\n"
    
    message += "原文链接：{}\n\n".format(featured['link'])
    
    # 其他精选（3 篇，每篇 3 个要点）
    if others:
        message += "【其他精选】\n\n"
        for idx, article in enumerate(others[:3], 1):
            message += "### 精选{}：{}\n".format(idx, article['title_cn'])
            message += "作者：{}\n".format(article['author'] or 'Unknown')
            message += "发布时间：{}\n\n".format(article['pub_date'])
            
            # 尝试抓取网页全文
            print("正在抓取其他精选文章{}全文...".format(idx))
            web_content = fetch_article_content(article['link'])
            if web_content:
                # detailed=False 获取 3 个要点
                template = extract_and_translate_points(article['title'], web_content, article['link'], detailed=False)
                points = template['points']
            else:
                points = [p for p in article['points_brief'] if p and len(p.strip()) > 0]
            
            if points:
                for i, point in enumerate(points[:3], 1):  # 每篇最多 3 个要点
                    message += "要点{}：{}\n".format(i, point)
            else:
                message += "暂无详细内容\n"
            
            message += "原文链接：{}\n\n".format(article['link'])
    
    message += "\n来源：LightReading.com"
    
    return message

def send_to_wechat(content):
    """发送到企业微信 - 使用 http.client 直接连接"""
    import http.client
    import urllib.parse
    
    data = {"msgtype": "text", "text": {"content": content}}
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    # 解析 URL
    parsed = urllib.parse.urlparse(WEBHOOK_URL)
    
    conn = http.client.HTTPSConnection(parsed.netloc, timeout=60)
    try:
        conn.request('POST', parsed.path + '?' + parsed.query, body, {'Content-Type': 'application/json; charset=utf-8'})
        response = conn.getresponse()
        response_body = response.read().decode('utf-8')
        
        if response.status != 200:
            raise Exception(f'HTTP {response.status}: {response_body}')
        
        return json.loads(response_body)
    finally:
        conn.close()

def main():
    import sys
    print("=" * 60)
    print("LightReading 每日摘要推送（v3.0 AI 翻译模式）")
    print("=" * 60)
    
    print("\n正在获取 RSS feed...")
    xml_content = fetch_rss()
    print("RSS 内容长度：{}".format(len(xml_content)))
    
    print("\n正在解析文章...")
    articles = parse_rss(xml_content)
    print("找到 {} 篇文章".format(len(articles)))
    
    print("\n正在生成推送内容...")
    message = create_message(articles)
    
    # 如果没有新文章，跳过推送
    if "抱歉，今日未能获取到 LightReading 文章" in message or len(articles) == 0:
        print("没有新文章需要推送，跳过本次推送")
        return None
    
    # 保存英文内容到文件（供 AI 翻译）
    output_file = os.path.join(os.path.dirname(__file__), 'today_en.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(message)
    print("\n[INFO] 英文内容已保存到：{}".format(output_file))
    
    # 保存已推送文章记录（标记为已处理，避免重复）
    pushed_history = load_pushed_history()
    for a in articles[:4]:  # 保存实际抓取的 4 篇文章
        key = get_article_key(a)
        pushed_history[key] = datetime.now().timestamp()
    save_pushed_history(pushed_history)
    print("已保存文章记录")
    
    return message

if __name__ == '__main__':
    main()

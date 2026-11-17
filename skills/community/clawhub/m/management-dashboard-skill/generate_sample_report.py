"""生成有数据的测试报表"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from html_generator import SimpleHTMLGenerator

# 模拟有数据的分析结果
sample_analysis = {
    'team_assets': {
        'total_customers': 1428,
        'month_customers': 48,
        'today_customers': 12,
        'avg_per_person': 204
    },
    'daily_efficiency': {
        'total_recording_minutes': 165,
        'avg_minutes_per_person': 24.0,
        'total_visits': 12,
        'avg_visits_per_person': 1.7,
        'customer_distribution': {
            'old_customer_maintenance': 9,
            'new_customer_prospecting': 3
        },
        'regional_distribution': [
            {'region': '常熟片区', 'visit_count': 4},
            {'region': '主城与吴江片区', 'visit_count': 8}
        ]
    },
    'compliance_monitoring': {
        'compliance_metrics': [
            {
                'metric_name': '现场录音授权告知率',
                'achievement_rate': '100%',
                'status': '正常',
                'ai_audit_opinion': '全员12笔面谈开场均包含合规告知，无漏报。'
            },
            {
                'metric_name': '年轻客群非在读核验率',
                'achievement_rate': '100%',
                'status': '正常',
                'ai_audit_opinion': '餐饮店实地面对2名年轻店员，均当场口头核实排除了学生身份。'
            },
            {
                'metric_name': '12.8%标准利率线下明示率',
                'achievement_rate': '83.3%',
                'status': '警告',
                'ai_audit_opinion': '主城片区发现2笔录音不合规。在面谈客户嫌贵时，RM口头表述为"一天利息没多少"，未明确强调年化，已启动天级督导。'
            },
            {
                'metric_name': '线下违规包批词触发数',
                'achievement_rate': '0笔',
                'status': '正常',
                'ai_audit_opinion': '全员未触发"保证出额、100%批、抹流水"等消金高危红线。'
            }
        ]
    },
    'rm_performance': {
        'top_performers': [
            {
                'rank': 1,
                'region': '吴江片区',
                'name': '高经理',
                'score': 95,
                'behavior_description': '在维护老客"探萌宠物店"时，语调亲和，在递烟喝茶中主动触发2次转介绍索取，成功拿到同产业带2家猫舍老板的联系方式。'
            },
            {
                'rank': 2,
                'region': '常熟片区',
                'name': '张经理',
                'score': 88,
                'behavior_description': '面对模具厂老板吐槽12.8%利息贵，熟练运用"随借随还备用金，不提用0成本"的话术瞬间化解，并当场引导客户掏出手机测额。'
            }
        ],
        'needs_improvement': [
            {
                'region': '主城片区',
                'name': '李经理',
                'score': 62,
                'problem_diagnosis': '拜访餐饮商户时，客户表示行情差、不敢贷，该RM寒暄2句后直接放弃，未尝试进行异议化解，且完全遗漏了"夫妻合并申请40万"的增信推介，属于敷衍型打卡。'
            }
        ],
        'user_scores': [
            {
                'user_name': '高经理',
                'total_score': 190,
                'avg_score': 95.0,
                'recording_count': 2,
                'top_score': 95,
                'min_score': 95
            },
            {
                'user_name': '张经理',
                'total_score': 176,
                'avg_score': 88.0,
                'recording_count': 2,
                'top_score': 90,
                'min_score': 86
            },
            {
                'user_name': '李经理',
                'total_score': 124,
                'avg_score': 62.0,
                'recording_count': 2,
                'top_score': 68,
                'min_score': 56
            }
        ]
    },
    'lead_conversion': {
        'a_level_count': 2,
        'a_level_details': '1户为常熟模具厂下游（开票高资质优），1户为长桥宠物零售商。由于RM现场前置盘查完整，预计下周进件通过率达80%以上。',
        'b_level_count': 7,
        'b_level_followup': '明日或后天，建议主管重点跟进，指导其在微信上发送"家庭现金流置换隔离法"的定制化用款图表。',
        'c_level_count': 3,
        'c_level_interception': 'RM现场抽查发现客户线上微粒贷/京东多头负债严重超标，或属于严重亏损的堂食餐饮，RM现场果断终止推进。今日成功拦截3笔白跑和潜在不良件！'
    },
    'management_suggestions': [
        {
            'title': '日级话术通关（针对利率明示漏洞）',
            'content': '今日主城片区李经理等2人的录音已被系统自动判定为"利率披露不合规"。AI已在他们的手机端下发了"LegionSpace 12.8%年化利率合规明示专项练习"，请主管务必监督他们在明天早上外巡前完成话术打卡通关。'
        },
        {
            'title': '提取今日优秀录音（早会裂变教材）',
            'content': '高经理今日在宠物店现场轻松索取转介绍的3分钟标准双向录音，已被AI提取为S级每日标杆案例（已做隐私脱敏处理）。系统已自动推送至团队大群，建议明天早会用5分钟全员外巡前公放拆解，迅速复制销冠腿功和嘴功！'
        }
    ]
}

# 构建上下文
context = {
    'team_name': '测试团队',
    'date_str': '2026-06-24',
    'org_id': 'test_org',
    'user_groups': {'高经理': 2, '张经理': 2, '李经理': 2},
    'is_empty': False,
}

# 生成 HTML
html_gen = SimpleHTMLGenerator()
file_path = html_gen.generate(sample_analysis, context)

print(f"有数据报表已生成: {file_path}")

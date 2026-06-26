"""
Office Pro - Excel Templates

Built-in Excel spreadsheet templates for business use.
"""

from typing import Dict, List, Any, Optional

FINANCIAL_REPORT_TEMPLATE = {
    'title': '财务报表',
    'description': '月度/季度财务报表模板',
    'sheets': {
        'summary': {
            'title': '财务汇总',
            'columns': [
                {'name': '项目', 'width': 20},
                {'name': '本期金额', 'width': 15, 'format': 'currency'},
                {'name': '上期金额', 'width': 15, 'format': 'currency'},
                {'name': '增减额', 'width': 15, 'format': 'currency'},
                {'name': '增减率', 'width': 12, 'format': 'percent'},
            ],
            'rows': [
                ['一、营业收入', None, None, None, None],
                ['  主营业务收入', None, None, None, None],
                ['  其他业务收入', None, None, None, None],
                ['二、营业成本', None, None, None, None],
                ['  主营业务成本', None, None, None, None],
                ['  其他业务成本', None, None, None, None],
                ['三、营业利润', None, None, None, None],
                ['四、利润总额', None, None, None, None],
                ['五、净利润', None, None, None, None],
            ],
            'formulas': {
                'C2': '=SUM(C3:C4)',
                'C5': '=SUM(C6:C7)',
                'C8': '=C2-C5',
                'C9': '=C8',
                'C10': '=C9',
                'D2': '=C2-B2',
                'E2': '=IF(B2=0,0,D2/B2)',
            },
        },
        'income': {
            'title': '收入明细',
            'columns': [
                {'name': '日期', 'width': 12, 'format': 'date'},
                {'name': '凭证号', 'width': 12},
                {'name': '摘要', 'width': 30},
                {'name': '收入类型', 'width': 15},
                {'name': '金额', 'width': 15, 'format': 'currency'},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
        'expense': {
            'title': '支出明细',
            'columns': [
                {'name': '日期', 'width': 12, 'format': 'date'},
                {'name': '凭证号', 'width': 12},
                {'name': '摘要', 'width': 30},
                {'name': '支出类型', 'width': 15},
                {'name': '金额', 'width': 15, 'format': 'currency'},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
    },
    'default_data': {
        'company_name': '',
        'report_period': '',
        'currency': 'CNY',
    },
}

PROJECT_SCHEDULE_TEMPLATE = {
    'title': '项目进度表',
    'description': '项目进度跟踪表模板',
    'sheets': {
        'overview': {
            'title': '项目概览',
            'columns': [
                {'name': '项目名称', 'width': 25},
                {'name': '项目经理', 'width': 12},
                {'name': '开始日期', 'width': 12, 'format': 'date'},
                {'name': '结束日期', 'width': 12, 'format': 'date'},
                {'name': '总工期(天)', 'width': 12, 'format': 'number'},
                {'name': '当前进度', 'width': 12, 'format': 'percent'},
                {'name': '状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
        'tasks': {
            'title': '任务明细',
            'columns': [
                {'name': '任务ID', 'width': 10},
                {'name': '任务名称', 'width': 25},
                {'name': '负责人', 'width': 12},
                {'name': '开始日期', 'width': 12, 'format': 'date'},
                {'name': '结束日期', 'width': 12, 'format': 'date'},
                {'name': '工期(天)', 'width': 10, 'format': 'number'},
                {'name': '进度', 'width': 10, 'format': 'percent'},
                {'name': '状态', 'width': 10},
                {'name': '前置任务', 'width': 12},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
            'data_validation': {
                'status': ['未开始', '进行中', '已完成', '已延期', '已暂停'],
            },
        },
        'milestones': {
            'title': '里程碑',
            'columns': [
                {'name': '里程碑', 'width': 25},
                {'name': '计划日期', 'width': 12, 'format': 'date'},
                {'name': '实际日期', 'width': 12, 'format': 'date'},
                {'name': '状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
        'resources': {
            'title': '资源分配',
            'columns': [
                {'name': '资源名称', 'width': 15},
                {'name': '类型', 'width': 10},
                {'name': '分配任务', 'width': 25},
                {'name': '工作量', 'width': 10, 'format': 'number'},
                {'name': '单位', 'width': 8},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
    },
    'default_data': {
        'project_name': '',
        'project_manager': '',
        'start_date': None,
        'end_date': None,
    },
}

EMPLOYEE_ROSTER_TEMPLATE = {
    'title': '员工花名册',
    'description': '员工信息管理表模板',
    'sheets': {
        'roster': {
            'title': '员工名单',
            'columns': [
                {'name': '工号', 'width': 10},
                {'name': '姓名', 'width': 12},
                {'name': '性别', 'width': 8},
                {'name': '出生日期', 'width': 12, 'format': 'date'},
                {'name': '身份证号', 'width': 20},
                {'name': '部门', 'width': 15},
                {'name': '职位', 'width': 15},
                {'name': '入职日期', 'width': 12, 'format': 'date'},
                {'name': '联系电话', 'width': 15},
                {'name': '邮箱', 'width': 25},
                {'name': '状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
            'data_validation': {
                'gender': ['男', '女'],
                'status': ['在职', '离职', '休假', '试用'],
            },
        },
        'education': {
            'title': '教育背景',
            'columns': [
                {'name': '工号', 'width': 10},
                {'name': '姓名', 'width': 12},
                {'name': '最高学历', 'width': 12},
                {'name': '毕业院校', 'width': 20},
                {'name': '专业', 'width': 15},
                {'name': '毕业时间', 'width': 12, 'format': 'date'},
                {'name': '学位', 'width': 10},
            ],
            'rows': [],
        },
        'contracts': {
            'title': '合同信息',
            'columns': [
                {'name': '工号', 'width': 10},
                {'name': '姓名', 'width': 12},
                {'name': '合同类型', 'width': 12},
                {'name': '合同起始', 'width': 12, 'format': 'date'},
                {'name': '合同终止', 'width': 12, 'format': 'date'},
                {'name': '签订日期', 'width': 12, 'format': 'date'},
                {'name': '状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
        'statistics': {
            'title': '统计汇总',
            'columns': [
                {'name': '统计项', 'width': 20},
                {'name': '数量', 'width': 10, 'format': 'number'},
                {'name': '占比', 'width': 10, 'format': 'percent'},
            ],
            'rows': [
                ['员工总数', None, None],
                ['在职人数', None, None],
                ['试用期人数', None, None],
                ['男性员工', None, None],
                ['女性员工', None, None],
            ],
        },
    },
    'default_data': {
        'company_name': '',
        'department': '',
        'update_date': None,
    },
}

ASSET_INVENTORY_TEMPLATE = {
    'title': '资产清单',
    'description': '固定资产管理表模板',
    'sheets': {
        'assets': {
            'title': '资产明细',
            'columns': [
                {'name': '资产编号', 'width': 15},
                {'name': '资产名称', 'width': 20},
                {'name': '资产类别', 'width': 12},
                {'name': '规格型号', 'width': 15},
                {'name': '品牌', 'width': 12},
                {'name': '数量', 'width': 8, 'format': 'number'},
                {'name': '单位', 'width': 8},
                {'name': '原值', 'width': 12, 'format': 'currency'},
                {'name': '净值', 'width': 12, 'format': 'currency'},
                {'name': '购置日期', 'width': 12, 'format': 'date'},
                {'name': '使用部门', 'width': 12},
                {'name': '使用人', 'width': 10},
                {'name': '存放地点', 'width': 15},
                {'name': '资产状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
            'data_validation': {
                'category': ['电子设备', '办公设备', '交通工具', '家具', '其他'],
                'status': ['在用', '闲置', '报废', '丢失', '维修中'],
            },
        },
        'depreciation': {
            'title': '折旧明细',
            'columns': [
                {'name': '资产编号', 'width': 15},
                {'name': '资产名称', 'width': 20},
                {'name': '原值', 'width': 12, 'format': 'currency'},
                {'name': '残值率', 'width': 10, 'format': 'percent'},
                {'name': '折旧方法', 'width': 12},
                {'name': '使用年限', 'width': 10, 'format': 'number'},
                {'name': '已折旧月数', 'width': 12, 'format': 'number'},
                {'name': '累计折旧', 'width': 12, 'format': 'currency'},
                {'name': '净值', 'width': 12, 'format': 'currency'},
            ],
            'rows': [],
        },
        'maintenance': {
            'title': '维护记录',
            'columns': [
                {'name': '资产编号', 'width': 15},
                {'name': '资产名称', 'width': 20},
                {'name': '维护日期', 'width': 12, 'format': 'date'},
                {'name': '维护类型', 'width': 12},
                {'name': '维护内容', 'width': 25},
                {'name': '费用', 'width': 10, 'format': 'currency'},
                {'name': '维护人员', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
        },
        'summary': {
            'title': '资产汇总',
            'columns': [
                {'name': '资产类别', 'width': 15},
                {'name': '数量', 'width': 10, 'format': 'number'},
                {'name': '原值合计', 'width': 15, 'format': 'currency'},
                {'name': '净值合计', 'width': 15, 'format': 'currency'},
                {'name': '在用数量', 'width': 10, 'format': 'number'},
                {'name': '闲置数量', 'width': 10, 'format': 'number'},
            ],
            'rows': [
                ['电子设备', None, None, None, None, None],
                ['办公设备', None, None, None, None, None],
                ['交通工具', None, None, None, None, None],
                ['家具', None, None, None, None, None],
                ['其他', None, None, None, None, None],
                ['合计', None, None, None, None, None],
            ],
        },
    },
    'default_data': {
        'company_name': '',
        'department': '',
        'inventory_date': None,
    },
}

EXPENSE_REPORT_TEMPLATE = {
    'title': '费用报销单',
    'description': '员工费用报销表模板',
    'sheets': {
        'expense': {
            'title': '报销明细',
            'columns': [
                {'name': '报销单号', 'width': 15},
                {'name': '报销人', 'width': 10},
                {'name': '部门', 'width': 12},
                {'name': '报销日期', 'width': 12, 'format': 'date'},
                {'name': '费用类型', 'width': 12},
                {'name': '摘要', 'width': 25},
                {'name': '金额', 'width': 12, 'format': 'currency'},
                {'name': '发票号', 'width': 15},
                {'name': '审批状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
            'data_validation': {
                'expense_type': ['交通费', '住宿费', '餐饮费', '通讯费', '办公用品', '其他'],
                'status': ['待审批', '已审批', '已支付', '已驳回'],
            },
        },
        'summary': {
            'title': '报销汇总',
            'columns': [
                {'name': '费用类型', 'width': 15},
                {'name': '报销笔数', 'width': 12, 'format': 'number'},
                {'name': '报销金额', 'width': 15, 'format': 'currency'},
                {'name': '已审批', 'width': 15, 'format': 'currency'},
                {'name': '待审批', 'width': 15, 'format': 'currency'},
            ],
            'rows': [
                ['交通费', None, None, None, None],
                ['住宿费', None, None, None, None],
                ['餐饮费', None, None, None, None],
                ['通讯费', None, None, None, None],
                ['办公用品', None, None, None, None],
                ['其他', None, None, None, None],
                ['合计', None, None, None, None],
            ],
        },
    },
    'default_data': {
        'applicant': '',
        'department': '',
        'apply_date': None,
    },
}

INVOICE_TEMPLATE = {
    'title': '发票管理表',
    'description': '发票开具与跟踪表模板',
    'sheets': {
        'invoices': {
            'title': '发票明细',
            'columns': [
                {'name': '发票号码', 'width': 18},
                {'name': '发票类型', 'width': 12},
                {'name': '开票日期', 'width': 12, 'format': 'date'},
                {'name': '客户名称', 'width': 25},
                {'name': '税号', 'width': 20},
                {'name': '金额(不含税)', 'width': 15, 'format': 'currency'},
                {'name': '税率', 'width': 10, 'format': 'percent'},
                {'name': '税额', 'width': 12, 'format': 'currency'},
                {'name': '价税合计', 'width': 15, 'format': 'currency'},
                {'name': '收款状态', 'width': 10},
                {'name': '备注', 'width': 20},
            ],
            'rows': [],
            'data_validation': {
                'invoice_type': ['增值税专用发票', '增值税普通发票', '电子发票'],
                'payment_status': ['未收款', '部分收款', '已收款'],
            },
        },
        'summary': {
            'title': '开票汇总',
            'columns': [
                {'name': '月份', 'width': 12},
                {'name': '开票数量', 'width': 12, 'format': 'number'},
                {'name': '开票金额', 'width': 15, 'format': 'currency'},
                {'name': '税额合计', 'width': 15, 'format': 'currency'},
                {'name': '已收款', 'width': 15, 'format': 'currency'},
                {'name': '未收款', 'width': 15, 'format': 'currency'},
            ],
            'rows': [],
        },
    },
    'default_data': {
        'company_name': '',
        'tax_number': '',
        'address': '',
        'phone': '',
        'bank': '',
        'account': '',
    },
}

EXCEL_TEMPLATES = {
    'financial_report': FINANCIAL_REPORT_TEMPLATE,
    'project_schedule': PROJECT_SCHEDULE_TEMPLATE,
    'employee_roster': EMPLOYEE_ROSTER_TEMPLATE,
    'asset_inventory': ASSET_INVENTORY_TEMPLATE,
    'expense_report': EXPENSE_REPORT_TEMPLATE,
    'invoice': INVOICE_TEMPLATE,
}

__all__ = ['EXCEL_TEMPLATES']

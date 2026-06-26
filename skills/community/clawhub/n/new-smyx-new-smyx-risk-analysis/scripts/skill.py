#!/usr/bin/env python3

from .config import ApiEnum, ConstantEnum

# import_path_common()
from skills.smyx_common.scripts.config import ApiEnum as ApiEnumBase
from skills.smyx_common.scripts.base import BaseSkill
from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase

from skills.face_analysis.scripts.skill import Skill as SkillParent


class Skill(SkillParent):
    def __init__(self):
        super().__init__()
        self.analysis_url = ApiEnum.ANALYSIS_URL

    def get_output_analysis(self, input_path, params={}):
        params.setdefault("sceneCode", ConstantEnum.DEFAULT__SCENE_CODE)
        response = self.get_analysis(
            input_path, params
        )

        output_content = self.get_output_analysis_content(response)
        return output_content

    def get_output_analysis_content_body(self, result=None):
        import json
        result_json = result
        result_json = json.dumps(result_json,
                                 ensure_ascii=False, indent=2)
        return result_json if result_json else "⚠️暂未发现风险"

    def get_output_analysis_content_head(self, result=None):
        return f"📊 风险分析结构化结果"

    def get_output_analysis_content_foot(self, result):
        pass

    def get_output_analysis_list(self, pageNum=None, pageSize=None, open_id=None):
        """获取风险分析报告清单
        根据 open-id 列出该用户的所有历史风险分析报告
        """

        def _get_analysis_detail_url(request_id=None):
            if not request_id:
                return ""
            # 风险分析报告详情链接格式
            return f"{ApiEnum.BASE_URL_HEALTH}/health/order/api/getReportDetailExport?id={request_id}"

        # open_id 检查 - 如果 open_id 为空/None，不添加过滤条件，返回所有报告
        data = {}
        if open_id:
            # 将 open-id 添加到查询参数中，API 根据 open-id 筛选
            data["createBy"] = open_id

        # ApiService.page 方法签名: page(self, url, pageNum=None, pageSize=None, *args, **argss)
        # 我们需要直接调用 ApiService 的 page 方法
        api_service = ApiServiceBase.get_instance()
        # 确保 URL 拼接正确：BASE_URL 末尾没有斜杠，所以 PAGE_URL 必须以斜杠开头
        # 我们不需要手动拼接，RequestUtil 会处理
        response = api_service.page(ApiEnum.PAGE_URL, pageNum, pageSize, data)

        if response is None:
            return "⚠️ 获取报告列表失败：response is None"

        # 兼容处理：不同版本的基类返回不同格式
        if isinstance(response, list):
            # 基类直接返回了 records 列表，无法获取分页信息，直接使用
            records = response
            total = len(records)
            pages = 1
        elif isinstance(response, dict):
            # 完整响应格式
            if not response.get('success'):
                error_msg = response.get('errorMsg', '未知错误')
                return f"⚠️ 获取报告列表失败：{error_msg}"
            data_resp = response.get('data', {})
            if not data_resp or not isinstance(data_resp, dict):
                return "⚠️ 获取报告列表失败：数据格式错误"
            total = data_resp.get('total', 0)
            pages = data_resp.get('pages', 1)
            records = data_resp.get('records', [])
        else:
            return f"⚠️ 获取报告列表失败：response type={type(response)}"

        if not records:
            return f"⚠️ 用户 [{open_id}] 暂无风险分析报告记录"

        output_all = f"📋 历史风险分析报告清单（{open_id}，共 {total} 份）\n\n"
        output_all += "| 报告ID | 分析时间 | 风险类型 | 风险等级 | 点击查看 |\n"
        output_all += "|--------|----------|----------|----------|----------|\n"

        # 处理第一页
        for item in records:
            if not isinstance(item, dict):
                continue
            report_id = item.get('id', '')
            create_time = item.get('createTimeString', '未知时间')

            # 提取风险信息
            risk_type = item.get('riskType', '未知类型')
            risk_level = item.get('riskLevel', '未知等级')

            # 如果风险类型没有直接获取到，则尝试从结果中提取
            if (not risk_type or risk_type == '未知类型') and item.get('result'):
                result_data = item.get('result', {})
                if isinstance(result_data, list):
                    risk_types = [r.get('type', '') for r in result_data if r.get('type')]
                    if risk_types:
                        risk_type = ','.join(risk_types)
                elif isinstance(result_data, dict) and result_data.get('risks'):
                    risks = result_data.get('risks', [])
                    risk_types = [r.get('type', '') for r in risks if r.get('type')]
                    if risk_types:
                        risk_type = ','.join(risk_types)

            report_url = _get_analysis_detail_url(report_id)
            # 报告ID只显示前8个字符保持表格整洁
            short_id = str(report_id)[:8] + '...' if len(str(report_id)) > 8 else str(report_id)
            output_all += f"| {short_id} | {create_time} | {risk_type} | {risk_level} | [🔗 查看报告]({report_url}) |\n"

        # 处理剩余页
        for current_page in range(2, pages + 1):
            response = api_service.page(ApiEnum.PAGE_URL, current_page, 30, data)
            if not response or not isinstance(response, dict) or not response.get('success'):
                continue
            data_resp = response.get('data', {})
            if not data_resp or not isinstance(data_resp, dict):
                continue
            records = data_resp.get('records', [])
            for item in records:
                if not isinstance(item, dict):
                    continue
                report_id = item.get('id', '')
                create_time = item.get('createTimeString', '未知时间')
                risk_type = item.get('riskType', '未知类型')
                risk_level = item.get('riskLevel', '未知等级')
                report_url = _get_analysis_detail_url(report_id)
                short_id = str(report_id)[:8] + '...' if len(str(report_id)) > 8 else str(report_id)
                output_all += f"| {short_id} | {create_time} | {risk_type} | {risk_level} | [🔗 查看报告]({report_url}) |\n"

        output_all += "\n> 注：风险分析结果仅供安全参考，不能替代专业安防和医疗诊断。"
        return output_all


skill = Skill()

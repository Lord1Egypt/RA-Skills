"""
AI 分析模块
使用 OpenClaw 内部 LLM 能力分析录音内容
"""
import json
from typing import List, Dict, Any


class RecordingAnalyzer:
    """录音内容分析器"""
    
    def __init__(self, llm_client):
        """
        Args:
            llm_client: OpenClaw LLM 客户端
        """
        self.llm_client = llm_client
    
    def analyze_recordings(self, contents: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析所有录音内容，提取管理驾驶舱所需指标
        
        Args:
            contents: AI 总结内容列表，每项包含 aiSummaryContent 和 userName
            context: 上下文信息（团队名称、日期等）
        
        Returns:
            分析结果字典
        """
        if not contents:
            return self._empty_result()
        
        # 构建分析 prompt
        prompt = self._build_analysis_prompt(contents, context)
        
        # 调用 LLM 分析
        response = self.llm_client.chat(prompt)
        
        # 解析结果
        try:
            result = json.loads(response)
            return self._validate_result(result)
        except json.JSONDecodeError:
            # 如果 LLM 返回的不是标准 JSON，尝试提取
            return self._parse_fallback(response)
    
    def _build_analysis_prompt(self, contents: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """构建分析 prompt"""
        team_name = context.get('team_name', '未知团队')
        date_str = context.get('date_str', '未知日期')
        user_groups = context.get('user_groups', {})
        
        # 合并所有录音内容，保留用户信息
        combined_content = "\n\n---\n\n".join([
            f"【发言人：{item.get('userName', '未知成员')}】\n{item.get('aiSummaryContent', '')}"
            for item in contents
        ])
        
        # 构建成员分组统计信息
        user_groups_str = "、".join([f"{name}({count}条)" for name, count in user_groups.items()]) if user_groups else "未知"
        
        prompt = f"""你是一个专业的销售团队管理分析师。请分析以下录音 AI 总结内容，生成管理驾驶舱报表数据。

团队：{team_name}
日期：{date_str}
成员分组统计：{user_groups_str}

【重要规则】
- **数据来源唯一性**：所有分析必须严格基于下方「录音内容」中的 AI 总结文本，禁止使用历史数据、外部数据或自行编造数据。
- **成员姓名**：必须严格使用上方「成员分组统计」中列出的姓名，禁止虚构、编造或使用 userId/数字ID 作为姓名。
- **无法识别时跳过**：如果录音内容中无法识别到具体成员姓名或关键信息，不要猜测，直接跳过该条记录的分析。
- **top_performers 和 needs_improvement**：其中的 name 字段必须是成员分组统计中存在的姓名。
- **数值必须来自原文**：所有统计数据（客户数、录音时长、拜访次数等）必须从录音 AI 总结内容中提取，禁止凭空编造。如果原文中未提及某项数据，返回 0 或空值。

录音内容（每条记录包含发言人信息）：
{combined_content}

请从以下维度进行分析，并以 JSON 格式返回：

1. **团队资产沉淀大盘**（长期累积维度）
   - total_customers: 历史累积拜访客户总量（整数）
   - month_customers: 本月至今累积拜访（整数）
   - today_customers: 今日新增实地拜访（整数）
   - avg_per_person: 人均长期维护客群深度（整数）

2. **每日外勤实地效能监测**
   - total_recording_minutes: 今日双向有效录音总时长（分钟，整数）
   - avg_minutes_per_person: 人均日面谈时长（分钟，浮点数）
   - total_visits: 今日实地有效面谈总数（整数）
   - avg_visits_per_person: 人均日均实地探店次数（浮点数）
   - customer_distribution: 客群结构分布
     * old_customer_maintenance: 老客维护与转介绍（整数）
     * new_customer_prospecting: 陌生新商圈扫街（整数）
   - regional_distribution: 产业带轨迹分布（数组，每项包含 region 和 visit_count）

3. **当日合规与红线监控**
   - compliance_metrics: 合规指标数组，每项包含：
     * metric_name: 监控指标名称
     * achievement_rate: 达成率（百分比字符串，如 "100%"）
     * status: 状态（"正常" / "警告" / "危险"）
     * ai_audit_opinion: AI 每日穿透审计意见

4. **当日 RM 业务水平排行**
   - top_performers: 优秀 RM 数组（最多3名），每项包含：
     * rank: 排名（1, 2, 3）
     * region: 片区
     * name: 姓名
     * score: 得分（百分制）
     * behavior_description: 销冠/高水平行为描述
   - needs_improvement: 待提升 RM 数组，每项包含：
     * region: 片区
     * name: 姓名
     * score: 得分
     * problem_diagnosis: 问题诊断
   - user_scores: 按成员分组统计得分（数组），每项包含：
     * user_name: 成员姓名（必须与上方成员分组统计中的姓名一致）
     * total_score: 总分
     * avg_score: 平均分
     * recording_count: 录音条数（必须与上方成员分组统计中的条数一致）
     * top_score: 最高分
     * min_score: 最低分

5. **当日线索转化效率**
   - lead_conversion:
     * a_level_count: A 级商机数量
     * a_level_details: A 级详情描述
     * b_level_count: B 级商机数量
     * b_level_followup: B 级跟进建议
     * c_level_count: C 级商机数量
     * c_level_interception: C 级 AI 拦截核查

6. **管理者跟进与靶向督导建议**
   - management_suggestions: 建议数组，每项包含：
     * title: 建议标题
     * content: 建议内容

请确保返回的是合法的 JSON 格式，不要包含其他文字说明。
"""
        return prompt
    
    def _validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证并补全结果"""
        # 确保所有必需字段存在
        defaults = {
            'team_assets': {
                'total_customers': 0,
                'month_customers': 0,
                'today_customers': 0,
                'avg_per_person': 0
            },
            'daily_efficiency': {
                'total_recording_minutes': 0,
                'avg_minutes_per_person': 0,
                'total_visits': 0,
                'avg_visits_per_person': 0,
                'customer_distribution': {
                    'old_customer_maintenance': 0,
                    'new_customer_prospecting': 0
                },
                'regional_distribution': []
            },
            'compliance_monitoring': {
                'compliance_metrics': []
            },
            'rm_performance': {
                'top_performers': [],
                'needs_improvement': [],
                'user_scores': []
            },
            'lead_conversion': {
                'a_level_count': 0,
                'a_level_details': '',
                'b_level_count': 0,
                'b_level_followup': '',
                'c_level_count': 0,
                'c_level_interception': ''
            },
            'management_suggestions': []
        }
        
        # 合并默认值和实际结果
        for key, default_value in defaults.items():
            if key not in result:
                result[key] = default_value
            elif isinstance(default_value, dict):
                for sub_key, sub_default in default_value.items():
                    if sub_key not in result[key]:
                        result[key][sub_key] = sub_default
        
        return result
    
    def _parse_fallback(self, text: str) -> Dict[str, Any]:
        """降级解析：尝试从文本中提取 JSON"""
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        return self._empty_result()
    
    def _empty_result(self) -> Dict[str, Any]:
        """返回空结果"""
        return {
            'team_assets': {
                'total_customers': 0,
                'month_customers': 0,
                'today_customers': 0,
                'avg_per_person': 0
            },
            'daily_efficiency': {
                'total_recording_minutes': 0,
                'avg_minutes_per_person': 0,
                'total_visits': 0,
                'avg_visits_per_person': 0,
                'customer_distribution': {
                    'old_customer_maintenance': 0,
                    'new_customer_prospecting': 0
                },
                'regional_distribution': []
            },
            'compliance_monitoring': {
                'compliance_metrics': []
            },
            'rm_performance': {
                'top_performers': [],
                'needs_improvement': [],
                'user_scores': []
            },
            'lead_conversion': {
                'a_level_count': 0,
                'a_level_details': '',
                'b_level_count': 0,
                'b_level_followup': '',
                'c_level_count': 0,
                'c_level_interception': ''
            },
            'management_suggestions': []
        }

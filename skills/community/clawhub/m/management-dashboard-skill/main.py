# -*- coding: utf-8 -*-
"""
管理驾驶舱 Skill 主逻辑
"""
import sys
import json
import requests
from typing import List, Dict, Any, Optional

from config import API_BASE_URL, API_ENDPOINT, DEFAULT_DAYS, DEFAULT_PAGE_SIZE
from utils import generate_uuid, parse_time_input, get_default_time_range, resolve_team_name, extract_org_info
from analyzer import RecordingAnalyzer
from html_generator import SimpleHTMLGenerator


class ManagementDashboardSkill:
    """管理驾驶舱 Skill"""
    
    def __init__(self):
        self.analyzer = RecordingAnalyzer(llm_client=self._get_llm_client())
        self.html_generator = SimpleHTMLGenerator()
    
    def _get_llm_client(self):
        """获取 OpenClaw LLM 客户端"""
        # 这里需要根据 OpenClaw 的实际 API 实现
        # 假设 OpenClaw 提供了 LLM 调用的 SDK 或 API
        class OpenClawLLMClient:
            def chat(self, prompt: str) -> str:
                """调用 OpenClaw LLM"""
                # 实际实现需要根据 OpenClaw 的 API 文档
                # 这里使用伪代码示意
                try:
                    # 方式1：如果 OpenClaw 提供了 Python SDK
                    # from openclaw import LLM
                    # return LLM.chat(prompt)
                    
                    # 方式2：如果 OpenClaw 提供了 HTTP API
                    # response = requests.post(
                    #     'http://localhost:3000/api/llm/chat',
                    #     json={'prompt': prompt},
                    #     timeout=120
                    # )
                    # return response.json()['response']
                    
                    # 方式3：使用 OpenClaw 内部函数（如果在 Skill 环境中）
                    # return openclaw.llm.chat(prompt)
                    
                    # 临时返回模拟数据用于测试
                    return self._mock_response(prompt)
                except Exception as e:
                    print(f"LLM 调用失败: {e}", file=sys.stderr)
                    return "{}"
            
            def _mock_response(self, prompt: str) -> str:
                """模拟 LLM 响应（用于测试）- 返回 0 值，不使用假数据"""
                return json.dumps({
                    "team_assets": {"total_customers": 0, "month_customers": 0, "today_customers": 0, "avg_per_person": 0},
                    "daily_efficiency": {"total_recording_minutes": 0, "avg_minutes_per_person": 0.0, "total_visits": 0, "avg_visits_per_person": 0.0, "customer_distribution": {"old_customer_maintenance": 0, "new_customer_prospecting": 0}, "regional_distribution": []},
                    "compliance_monitoring": {"compliance_metrics": []},
                    "rm_performance": {"top_performers": [], "needs_improvement": [], "user_scores": []},
                    "lead_conversion": {"a_level_count": 0, "a_level_details": "", "b_level_count": 0, "b_level_followup": "", "c_level_count": 0, "c_level_interception": ""},
                    "management_suggestions": []
                })
        
        return OpenClawLLMClient()
    
    def execute(self, user_input: str, agent_id: str, org_id: str = '', team_name: str = None) -> Dict[str, Any]:
        """
        执行 Skill
        
        Args:
            user_input: 用户输入（如"系统驾驶舱 2026-06-04"）
            agent_id: 当前会话的 agentId
            org_id: 组织ID（可选，默认从接口响应自动获取）
            team_name: 团队名称（可选）
        
        Returns:
            包含状态和结果的字典:
            - success: bool, 是否成功生成报表
            - message: str, 提示信息
            - file_path: str, 生成的 HTML 文件路径（仅当 success=True 时存在）
            - data_count: int, 获取的数据条数
        """
        print(f"开始生成管理驾驶舱报表...")
        
        # 1. 解析时间参数
        start_time, end_time = parse_time_input(user_input)
        if not start_time or not end_time:
            start_time, end_time = get_default_time_range(DEFAULT_DAYS)
        
        print(f"查询时间范围: {start_time} ~ {end_time}")
        
        # 2. 分页获取所有 AI 总结内容（含接口状态检查）
        fetch_result = self._fetch_all_contents(agent_id, start_time, end_time)
        
        # 检查接口返回状态（直接透传 message，不附加说明）
        if fetch_result.get('error'):
            message = fetch_result.get('message', '')
            print(message)
            return {
                'success': False,
                'message': message,
                'data_count': 0,
                'start_time': start_time,
                'end_time': end_time
            }
        
        contents = fetch_result.get('contents', [])
        resolved_org_id = fetch_result.get('org_id') or org_id
        resolved_team_name = resolve_team_name(
            resolved_org_id,
            fetch_result.get('org_name'),
            team_name,
        )
        is_empty = not contents
        print(f"共获取 {len(contents)} 条录音记录")
        
        # 3. 本地按 userName 分组统计录音条数
        user_groups = self._group_by_user(contents)
        if user_groups:
            print(f"成员分组统计: {[(u, c) for u, c in user_groups.items()]}")
        
        # 4. AI 分析内容（空数据时使用默认空结果，不调用 LLM）
        context = {
            'team_name': resolved_team_name,
            'date_str': start_time,
            'end_time': end_time,
            'org_id': resolved_org_id,
            'user_groups': user_groups,
            'is_empty': is_empty,
        }
        
        print("正在进行 AI 分析..." if not is_empty else "当前查询周期暂无录音数据，生成空报表...")
        analysis = self.analyzer.analyze_recordings(contents, context)
        
        # 5. 强制校验并修复 LLM 返回的成员数据，确保姓名来自真实 user_groups
        self._fix_llm_member_names(analysis, user_groups)
        
        analysis['rm_performance']['user_scores'] = self._build_user_scores_from_groups(
            user_groups, analysis
        )
        
        # 6. 生成 HTML 报表
        print("正在生成 HTML 报表...")
        file_path = self.html_generator.generate(analysis, context)
        
        print(f"报表已生成: {file_path}")
        
        if is_empty:
            message = (
                f"已根据 {start_time} 至 {end_time} 生成管理驾驶舱报告（当前查询周期暂无录音数据）。"
            )
        else:
            message = (
                f"已根据 {start_time} 至 {end_time} 的 {len(contents)} 条录音 AI 总结，"
                f"生成管理驾驶舱报告。"
            )
        
        return {
            'success': True,
            'message': message,
            'file_path': file_path,
            'data_count': len(contents),
            'start_time': start_time,
            'end_time': end_time
        }
    
    def _group_by_user(self, contents: List[Dict[str, Any]]) -> Dict[str, int]:
        """按 userName 分组统计录音条数，空 userName 归入'其它用户'"""
        groups = {}
        for item in contents:
            user_name = item.get('userName') or item.get('memberName')
            if not user_name or user_name.strip() == '':
                user_name = '其它用户'
            else:
                user_name = user_name.strip()
            groups[user_name] = groups.get(user_name, 0) + 1
        return groups
    
    def _fix_llm_member_names(
        self, analysis: Dict[str, Any], user_groups: Dict[str, int]
    ) -> None:
        """强制校验 LLM 返回的成员姓名，过滤虚构名字和 userId，只保留真实 user_groups 中的姓名"""
        valid_names = set(user_groups.keys())
        
        rm = analysis.get('rm_performance', {})
        
        # 过滤 top_performers
        rm['top_performers'] = [
            p for p in rm.get('top_performers', [])
            if p.get('name', '') in valid_names
        ]
        
        # 过滤 needs_improvement
        rm['needs_improvement'] = [
            p for p in rm.get('needs_improvement', [])
            if p.get('name', '') in valid_names
        ]
        
        # 过滤 user_scores
        rm['user_scores'] = [
            s for s in rm.get('user_scores', [])
            if s.get('user_name', '') in valid_names
        ]
    
    def _build_user_scores_from_groups(
        self, user_groups: Dict[str, int], analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """基于本地分组信息和 LLM 分析结果，构建成员得分统计"""
        user_scores = []
        
        # 从 LLM 返回的 top_performers 和 needs_improvement 中提取每个成员的评分
        performer_scores = {}
        for p in analysis.get('rm_performance', {}).get('top_performers', []):
            name = p.get('name', '')
            if name:
                performer_scores[name] = performer_scores.get(name, [])
                performer_scores[name].append(p.get('score', 0))
        for p in analysis.get('rm_performance', {}).get('needs_improvement', []):
            name = p.get('name', '')
            if name:
                performer_scores[name] = performer_scores.get(name, [])
                performer_scores[name].append(p.get('score', 0))
        
        # 为每个成员生成分组统计
        for user_name, count in user_groups.items():
            scores = performer_scores.get(user_name, [])
            if scores:
                total = sum(scores)
                avg = total / len(scores)
                top = max(scores)
                min_s = min(scores)
            else:
                # 没有评分数据时，基于录音条数给一个基础分
                total = 0
                avg = 0
                top = 0
                min_s = 0
            
            user_scores.append({
                'user_name': user_name,
                'total_score': total,
                'avg_score': round(avg, 1),
                'recording_count': count,
                'top_score': top,
                'min_score': min_s,
            })
        
        # 按平均分降序排列
        user_scores.sort(key=lambda x: x['avg_score'], reverse=True)
        return user_scores
    
    def _fetch_all_contents(self, agent_id: str, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        分页获取所有 AI 总结内容。
        
        Returns:
            字典，包含:
            - contents: List[Dict], 成功时的数据列表
            - error: str | None, 错误类型 ('api_error' / 'no_data' / 'network' / 'server_error' / None)
            - message: str, 错误描述信息（4001/5001 时取接口 msg 原文）
        """
        uuid = generate_uuid()
        all_contents = []
        is_complete = False
        api_ok = False
        org_id = ''
        org_name = ''
        
        while not is_complete:
            try:
                # 构建请求
                request_data = {
                    "agentId": agent_id,
                    "uuid": uuid,
                    "startTime": start_time,
                    "endTime": end_time
                }
                
                # 调用接口
                response = requests.post(
                    f"{API_BASE_URL}{API_ENDPOINT}",
                    json=request_data,
                    timeout=30
                )
                
                if response.status_code == 500:
                    return {
                        'contents': [],
                        'error': 'server_error',
                        'message': '暂未获取到数据'
                    }
                
                if response.status_code != 200:
                    return {
                        'contents': [],
                        'error': 'network',
                        'message': f'接口返回 HTTP {response.status_code}，请稍后重试。'
                    }
                
                response.encoding = 'utf-8'
                result = response.json()
                
                # 检查业务状态码
                # 成功：code=0  权限/业务拒绝：code=4001  系统异常：code=5001
                code = result.get('code', -1)
                if code in (4001, 5001):
                    return {
                        'contents': [],
                        'error': 'api_error',
                        'message': result.get('msg', ''),
                        'code': code
                    }
                if code != 0:
                    return {
                        'contents': [],
                        'error': 'no_data',
                        'message': result.get('msg', '') or '暂未获取到数据'
                    }
                
                api_ok = True
                
                # 提取数据（contents 为对象数组，data 可能为 null）
                data = result.get('data')
                if data and isinstance(data, dict):
                    if not org_id:
                        org_id, org_name = extract_org_info(data)
                    raw_contents = data.get('contents', []) or []
                    
                    # 每条记录是对象，提取 aiSummaryContent 和 userName
                    for item in raw_contents:
                        if isinstance(item, dict):
                            all_contents.append({
                                'aiSummaryContent': item.get('aiSummaryContent', ''),
                                'userName': item.get('userName') or item.get('memberName') or '',
                                'userId': item.get('userId', ''),
                            })
                        else:
                            # 兼容旧格式：纯字符串
                            all_contents.append({
                                'aiSummaryContent': str(item),
                                'userName': '',
                                'userId': '',
                            })
                    is_complete = data.get('completed', True)
                    
                    print(f"已获取第 {data.get('currentPage', 1)} 页，共 {len(raw_contents)} 条")
                else:
                    is_complete = True
                
            except requests.exceptions.Timeout:
                return {
                    'contents': [],
                    'error': 'network',
                    'message': '接口请求超时，请检查网络连接后重试。'
                }
            except requests.exceptions.ConnectionError:
                return {
                    'contents': [],
                    'error': 'network',
                    'message': '无法连接到录音服务，请检查网络或联系管理员。'
                }
            except Exception as e:
                return {
                    'contents': [],
                    'error': 'network',
                    'message': '获取数据时发生异常，请稍后重试。'
                }
        
        if not api_ok:
            return {
                'contents': [],
                'error': 'no_data',
                'message': '接口未返回任何数据。'
            }
        
        return {
            'contents': all_contents,
            'org_id': org_id,
            'org_name': org_name,
            'error': None,
            'message': ''
        }


def main():
    """主函数（用于测试）"""
    if len(sys.argv) < 3:
        print("用法: python main.py <user_input> <agent_id> [org_id] [team_name]")
        print("示例: python main.py '系统驾驶舱 2026-06-04' agent123")
        sys.exit(1)
    
    user_input = sys.argv[1]
    agent_id = sys.argv[2]
    org_id = sys.argv[3] if len(sys.argv) > 3 else ''
    team_name = sys.argv[4] if len(sys.argv) > 4 else None
    
    skill = ManagementDashboardSkill()
    result = skill.execute(user_input, agent_id, org_id, team_name)
    
    # 最后一行输出 JSON，供 Agent 解析 success / file_path
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()

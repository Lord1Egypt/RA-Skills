"""
自然语言解析器
将用户自然语言指令转换为看板操作
"""
import re
from typing import Dict, Optional, List
from datetime import datetime


class NLPParser:
    """自然语言解析器"""
    
    # 优先级映射
    PRIORITY_MAP = {
        '高': 'high', 'high': 'high', 'h': 'high',
        '中': 'medium', 'medium': 'medium', 'm': 'medium',
        '低': 'low', 'low': 'low', 'l': 'low'
    }
    
    # 状态映射
    STATUS_MAP = {
        '待办': 'todo', 'todo': 'todo', '待处理': 'todo',
        '进行中': 'in_progress', 'in_progress': 'in_progress', 'doing': 'in_progress',
        '已完成': 'done', 'done': 'done', '完成': 'done'
    }
    
    # 泳道映射
    LANE_MAP = {
        '功能': 'feature', 'feature': 'feature', '功能开发': 'feature',
        '安全': 'security', 'security': 'security', '安全加固': 'security',
        '运维': 'devops', 'devops': 'devops', '部署': 'devops',
        'bug': 'bugfix', 'bugfix': 'bugfix', '修复': 'bugfix', '缺陷': 'bugfix'
    }
    
    def parse(self, text: str) -> Dict:
        """
        解析自然语言指令
        
        Args:
            text: 用户输入的自然语言
        
        Returns:
            解析后的操作指令
        """
        text = text.strip()
        
        # 1. 识别意图
        intent = self._detect_intent(text)
        
        if intent == 'add_project':
            return self._parse_add_project(text)
        elif intent == 'update_status':
            return self._parse_update_status(text)
        elif intent == 'move_project':
            return self._parse_move_project(text)
        elif intent == 'delete_project':
            return self._parse_delete_project(text)
        elif intent == 'query':
            return self._parse_query(text)
        elif intent == 'analyze':
            return self._parse_analyze(text)
        else:
            return {
                'success': False,
                'error': '无法理解指令，请尝试更明确的表达',
                'examples': [
                    '添加一个高优先级的安全任务给张三',
                    '把项目 1 移到进行中',
                    '删除项目 5',
                    '查看待办任务',
                    '分析看板状态'
                ]
            }
    
    def _detect_intent(self, text: str) -> str:
        """检测用户意图"""
        text_lower = text.lower()
        
        # 添加任务
        if any(kw in text for kw in ['添加', '新建', '创建', 'add', 'create', 'new']):
            return 'add_project'
        
        # 更新状态
        if any(kw in text for kw in ['移到', '移动到', '改为', '更新', 'update', 'move', 'change']):
            if any(kw in text for kw in ['待办', '进行中', '完成', 'todo', 'in_progress', 'done']):
                return 'update_status'
            if any(kw in text for kw in ['功能', '安全', '运维', 'bug', '泳道']):
                return 'move_project'
        
        # 删除任务
        if any(kw in text for kw in ['删除', '移除', 'delete', 'remove']):
            return 'delete_project'
        
        # 查询
        if any(kw in text for kw in ['查看', '查询', '列表', 'list', 'show', 'query', '有哪些']):
            return 'query'
        
        # 分析
        if any(kw in text for kw in ['分析', 'analyze', '瓶颈', '风险', '建议']):
            return 'analyze'
        
        return 'unknown'
    
    def _parse_add_project(self, text: str) -> Dict:
        """解析添加任务指令"""
        result = {
            'action': 'add_project',
            'params': {
                'name': '',
                'lane': 'feature',
                'status': 'todo',
                'priority': 'medium',
                'assignee': '',
                'tasks': 0,
                'description': ''
            }
        }
        
        # 提取任务名称（引号内或关键词后）
        name_match = re.search(r'["\']([^"\']+)["\']', text)
        if name_match:
            result['params']['name'] = name_match.group(1)
        else:
            # 尝试提取关键词后的内容
            for kw in ['任务', '项目', '添加', '创建']:
                if kw in text:
                    idx = text.find(kw) + len(kw)
                    result['params']['name'] = text[idx:].strip()
                    break
        
        # 提取优先级
        for cn, en in self.PRIORITY_MAP.items():
            if cn in text.lower():
                result['params']['priority'] = en
                break
        
        # 提取泳道
        for cn, en in self.LANE_MAP.items():
            if cn in text.lower():
                result['params']['lane'] = en
                break
        
        # 提取状态
        for cn, en in self.STATUS_MAP.items():
            if cn in text.lower():
                result['params']['status'] = en
                break
        
        # 提取负责人（"给 XXX" 或 "assign XXX"）
        assignee_match = re.search(r'给 (\S+)', text)
        if assignee_match:
            result['params']['assignee'] = assignee_match.group(1)
        else:
            assignee_match = re.search(r'(?:assign|负责人)[:：]\s*(\S+)', text)
            if assignee_match:
                result['params']['assignee'] = assignee_match.group(1)
        
        # 提取任务数量
        tasks_match = re.search(r'(\d+)\s*个任务', text)
        if tasks_match:
            result['params']['tasks'] = int(tasks_match.group(1))
        
        # 验证
        if not result['params']['name']:
            result['success'] = False
            result['error'] = '请提供任务名称'
        else:
            result['success'] = True
        
        return result
    
    def _parse_update_status(self, text: str) -> Dict:
        """解析更新状态指令"""
        result = {
            'action': 'update_project_status',
            'params': {
                'project_id': None,
                'status': 'todo'
            }
        }
        
        # 提取项目 ID
        id_match = re.search(r'(?:项目 | 任务 |id)[:：\s]*(\d+)', text, re.IGNORECASE)
        if id_match:
            result['params']['project_id'] = int(id_match.group(1))
        
        # 提取目标状态
        for cn, en in self.STATUS_MAP.items():
            if cn in text.lower():
                result['params']['status'] = en
                break
        
        # 验证
        if not result['params']['project_id']:
            result['success'] = False
            result['error'] = '请提供项目 ID'
        else:
            result['success'] = True
        
        return result
    
    def _parse_move_project(self, text: str) -> Dict:
        """解析移动任务指令"""
        result = {
            'action': 'move_project',
            'params': {
                'project_id': None,
                'lane': 'feature',
                'status': None
            }
        }
        
        # 提取项目 ID
        id_match = re.search(r'(?:项目 | 任务 |id)[:：\s]*(\d+)', text, re.IGNORECASE)
        if id_match:
            result['params']['project_id'] = int(id_match.group(1))
        
        # 提取目标泳道
        for cn, en in self.LANE_MAP.items():
            if cn in text.lower():
                result['params']['lane'] = en
                break
        
        # 提取目标状态（可选）
        for cn, en in self.STATUS_MAP.items():
            if cn in text.lower():
                result['params']['status'] = en
                break
        
        # 验证
        if not result['params']['project_id']:
            result['success'] = False
            result['error'] = '请提供项目 ID'
        else:
            result['success'] = True
        
        return result
    
    def _parse_delete_project(self, text: str) -> Dict:
        """解析删除任务指令"""
        result = {
            'action': 'delete_project',
            'params': {
                'project_id': None
            }
        }
        
        # 提取项目 ID
        id_match = re.search(r'(?:项目 | 任务 |id)[:：\s]*(\d+)', text, re.IGNORECASE)
        if id_match:
            result['params']['project_id'] = int(id_match.group(1))
        
        # 验证
        if not result['params']['project_id']:
            result['success'] = False
            result['error'] = '请提供项目 ID'
        else:
            result['success'] = True
        
        return result
    
    def _parse_query(self, text: str) -> Dict:
        """解析查询指令"""
        result = {
            'action': 'list_projects',
            'params': {
                'status': None,
                'lane': None
            }
        }
        
        # 提取状态过滤
        for cn, en in self.STATUS_MAP.items():
            if cn in text.lower():
                result['params']['status'] = en
                break
        
        # 提取泳道过滤
        for cn, en in self.LANE_MAP.items():
            if cn in text.lower():
                result['params']['lane'] = en
                break
        
        result['success'] = True
        return result
    
    def _parse_analyze(self, text: str) -> Dict:
        """解析分析指令"""
        return {
            'action': 'analyze_board',
            'params': {},
            'success': True
        }


# 全局解析器实例
parser = NLPParser()


def parse_command(text: str) -> Dict:
    """解析自然语言命令"""
    return parser.parse(text)


if __name__ == '__main__':
    # 测试
    test_cases = [
        '添加一个高优先级的安全任务给张三',
        '创建任务 "用户认证模块"，泳道是功能开发，优先级中',
        '把项目 3 移到进行中',
        '删除项目 5',
        '查看待办任务',
        '分析看板状态，有哪些瓶颈',
        '添加 bug 修复任务，低优先级，给李四'
    ]
    
    for test in test_cases:
        print(f"\n输入：{test}")
        result = parse_command(test)
        print(f"输出：{result}")

"""
活动管理器 - 自然语言活动配置管理
支持用户通过自然语言添加、删除、查询活动
"""

import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class ActivityManager:
    """活动配置管理器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化活动管理器
        
        Args:
            config_path: 配置文件路径，默认为平台配置文件
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            # 默认路径：技能目录下的 config/platforms.json
            self.config_path = Path(__file__).parent.parent / 'config' / 'platforms.json'
        
        self.config = self._load_config()
        self.activities = self.config.get('activities', {})
        self.activity_list = self.activities.get('list', [])
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if not self.config_path.exists():
            return {'activities': {'list': []}}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
            return {'activities': {'list': []}}
    
    def _save_config(self):
        """保存配置到文件"""
        try:
            # 更新配置
            self.config['activities'] = self.activities
            
            # 写入文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def parse_natural_language(self, command: str) -> dict:
        """
        解析自然语言命令
        
        支持的命令格式：
        - "添加活动：春节特惠，关键词：春节、过年、团圆"
        - "删除活动：春节特惠"
        - "列出所有活动"
        - "查询活动：春节"
        
        Args:
            command: 用户输入的自然语言命令
            
        Returns:
            解析结果字典
        """
        command = command.strip()
        
        # 识别命令类型
        patterns = {
            'add': r'(?:添加|新建|创建|增加)(?:一个)?(?:活动|推广|促销)[：:]?\s*(.+)',
            'delete': r'(?:删除|移除|去掉)(?:活动|推广|促销)[：:]?\s*(.+)',
            'list': r'(?:列出|查看|显示|查询)(?:所有)?(?:的)?(?:活动|推广|促销)',
            'query': r'(?:查询|查找|搜索)(?:活动|推广|促销)[：:]?\s*(.+)'
        }
        
        for action, pattern in patterns.items():
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                if action in ['add']:
                    return self._parse_add_command(match.group(1))
                elif action == 'delete':
                    return {'action': 'delete', 'name': match.group(1).strip()}
                elif action == 'list':
                    return {'action': 'list'}
                elif action == 'query':
                    return {'action': 'query', 'name': match.group(1).strip()}
        
        return {'action': 'unknown', 'error': '无法识别命令，请使用"添加活动"、"删除活动"、"列出活动"或"查询活动"'}
    
    def _parse_add_command(self, content: str) -> dict:
        """解析添加命令"""
        # 提取活动名称
        name_match = re.search(r'^([^，,]+)', content)
        if not name_match:
            return {'action': 'error', 'error': '无法提取活动名称'}
        
        name = name_match.group(1).strip()
        
        # 提取关键词
        keywords = []
        keyword_patterns = [
            r'(?:关键词|关键字|标签)[：:]\s*([^，,]+(?:[，,][^，,]+)*)',
            r'(?:关键词|关键字|标签)[:=]\s*([^，,]+(?:[，,][^，,]+)*)'
        ]
        
        for pattern in keyword_patterns:
            kw_match = re.search(pattern, content)
            if kw_match:
                kw_text = kw_match.group(1)
                keywords = [k.strip() for k in re.split(r'[，,、]', kw_text)]
                break
        
        # 提取适用平台
        platforms = ['xiaohongshu', 'douyin', 'shipinhao', 'pyq']  # 默认全平台
        platform_patterns = [
            r'(?:适用平台|平台)[：:]\s*([^，,]+(?:[，,][^，,]+)*)',
            r'(?:适用|用于)[：:]\s*([^，,]+(?:[，,][^，,]+)*)'
        ]
        
        for pattern in platform_patterns:
            pf_match = re.search(pattern, content)
            if pf_match:
                pf_text = pf_match.group(1)
                platforms = self._parse_platforms(pf_text)
                break
        
        return {
            'action': 'add',
            'name': name,
            'keywords': keywords,
            'platforms': platforms
        }
    
    def _parse_platforms(self, text: str) -> List[str]:
        """解析平台名称"""
        platform_mapping = {
            '小红书': 'xiaohongshu',
            '抖音': 'douyin',
            '视频号': 'shipinhao',
            '朋友圈': 'pyq',
            '小红': 'xiaohongshu',
            '抖': 'douyin',
            '视': 'shipinhao',
            'pyq': 'pyq',
            '小红book': 'xiaohongshu'
        }
        
        result = []
        for name, code in platform_mapping.items():
            if name in text:
                result.append(code)
        
        # 如果没匹配到任何平台，默认全平台
        return result if result else ['xiaohongshu', 'douyin', 'shipinhao', 'pyq']
    
    def execute_command(self, parsed: dict) -> dict:
        """
        执行解析后的命令
        
        Args:
            parsed: parse_natural_language 返回的解析结果
            
        Returns:
            执行结果
        """
        action = parsed.get('action')
        
        if action == 'add':
            return self.add_activity(
                name=parsed.get('name'),
                keywords=parsed.get('keywords', []),
                platforms=parsed.get('platforms', ['xiaohongshu', 'douyin', 'shipinhao', 'pyq'])
            )
        elif action == 'delete':
            return self.delete_activity(parsed.get('name'))
        elif action == 'list':
            return self.list_activities()
        elif action == 'query':
            return self.query_activity(parsed.get('name'))
        else:
            return {'success': False, 'error': parsed.get('error', '未知命令')}
    
    def add_activity(self, name: str, keywords: List[str] = None, 
                    platforms: List[str] = None) -> dict:
        """
        添加活动
        
        Args:
            name: 活动名称
            keywords: 关键词列表
            platforms: 适用平台列表
            
        Returns:
            结果字典
        """
        # 检查是否已存在
        for act in self.activity_list:
            if act.get('name') == name:
                return {'success': False, 'error': f'活动"{name}"已存在'}
        
        # 生成ID
        activity_id = f"act_{len(self.activity_list) + 1}"
        
        # 创建活动
        new_activity = {
            'id': activity_id,
            'name': name,
            'keywords': keywords or [],
            'applicable_platforms': platforms or ['xiaohongshu', 'douyin', 'shipinhao', 'pyq'],
            'note': ''
        }
        
        self.activity_list.append(new_activity)
        
        # 标记为用户已配置
        self.activities['user_configured'] = True
        
        # 保存
        if self._save_config():
            return {
                'success': True,
                'message': f'活动"{name}"添加成功',
                'activity': new_activity
            }
        else:
            return {'success': False, 'error': '保存配置失败'}
    
    def delete_activity(self, name: str) -> dict:
        """
        删除活动
        
        Args:
            name: 活动名称
            
        Returns:
            结果字典
        """
        # 查找活动
        for i, act in enumerate(self.activity_list):
            if act.get('name') == name:
                # 删除
                del self.activity_list[i]
                
                # 保存
                if self._save_config():
                    return {
                        'success': True,
                        'message': f'活动"{name}"已删除'
                    }
                else:
                    return {'success': False, 'error': '保存配置失败'}
        
        return {'success': False, 'error': f'未找到活动"{name}"'}
    
    def list_activities(self) -> dict:
        """
        列出所有活动
        
        Returns:
            结果字典
        """
        # 过滤掉示例活动
        real_activities = [a for a in self.activity_list if a.get('id') != 'example']
        
        return {
            'success': True,
            'count': len(real_activities),
            'activities': real_activities,
            'message': f'共 {len(real_activities)} 个活动' if real_activities else '暂无配置的活动'
        }
    
    def query_activity(self, name: str) -> dict:
        """
        查询活动
        
        Args:
            name: 活动名称（支持模糊匹配）
            
        Returns:
            结果字典
        """
        matches = []
        
        for act in self.activity_list:
            if name.lower() in act.get('name', '').lower():
                matches.append(act)
        
        return {
            'success': True,
            'count': len(matches),
            'activities': matches,
            'message': f'找到 {len(matches)} 个匹配活动' if matches else '未找到匹配活动'
        }
    
    def match_activity(self, script_theme: str, platform: str = None) -> Optional[dict]:
        """
        根据脚本主题自动匹配活动
        
        Args:
            script_theme: 脚本主题
            platform: 当前平台（可选）
            
        Returns:
            匹配的活动，无匹配则返回 None
        """
        if not script_theme:
            return None
        
        script_theme = script_theme.lower()
        
        # 过滤掉示例活动
        real_activities = [a for a in self.activity_list if a.get('id') != 'example']
        
        if not real_activities:
            return None
        
        # 按关键词匹配度排序
        scored_activities = []
        
        for activity in real_activities:
            score = 0
            
            # 检查活动名称匹配
            if activity.get('name', '').lower() in script_theme:
                score += 10
            
            # 检查关键词匹配
            for keyword in activity.get('keywords', []):
                if keyword.lower() in script_theme:
                    score += 5
            
            # 平台过滤
            if platform:
                if platform not in activity.get('applicable_platforms', []):
                    score = 0  # 不匹配的平台得0分
            
            if score > 0:
                scored_activities.append((score, activity))
        
        # 返回得分最高的活动
        if scored_activities:
            scored_activities.sort(key=lambda x: x[0], reverse=True)
            return scored_activities[0][1]
        
        return None
    
    def get_default_activity(self) -> str:
        """获取默认活动显示文本"""
        real_activities = [a for a in self.activity_list if a.get('id') != 'example']
        
        if real_activities:
            return real_activities[0].get('name', '日常推广')
        
        return '日常推广，当前未设置activities'


# 便捷函数
def get_activity_manager(config_path: str = None) -> ActivityManager:
    """获取活动管理器实例"""
    return ActivityManager(config_path)


# 测试代码
if __name__ == "__main__":
    manager = ActivityManager()
    
    # 测试自然语言解析
    test_commands = [
        "添加活动：春节特惠，关键词：春节、过年、团圆、年夜饭",
        "添加活动：枇杷采摘季，关键词：枇杷、采摘、太平镇",
        "列出所有活动",
        "查询活动：枇杷",
        "删除活动：春节特惠"
    ]
    
    for cmd in test_commands:
        print(f"\n命令: {cmd}")
        parsed = manager.parse_natural_language(cmd)
        print(f"解析: {parsed}")
        
        if parsed.get('action') in ['add', 'delete', 'list', 'query']:
            result = manager.execute_command(parsed)
            print(f"执行: {result}")

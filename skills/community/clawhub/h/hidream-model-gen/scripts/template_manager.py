#!/usr/bin/env python3
"""
模板管理器 - 动态加载和管理视频模板
支持从JSON文件动态加载模板配置
"""
import json
import os
from typing import Dict, Any, Optional

class TemplateManager:
    """
    视频模板管理器
    
    支持动态加载模板配置，便于后续扩展更多模板
    """
    
    def __init__(self, templates_file: Optional[str] = None):
        """
        初始化模板管理器
        
        Args:
            templates_file: 模板配置文件路径，默认使用内置路径
        """
        if templates_file is None:
            # 默认路径
            base_dir = os.path.dirname(os.path.abspath(__file__))
            templates_file = os.path.join(base_dir, 'templates_data.json')
        
        self.templates_file = templates_file
        self.templates: Dict[str, Dict[str, Any]] = {}
        self._load_templates()
    
    def _load_templates(self):
        """从文件加载模板数据"""
        if not os.path.exists(self.templates_file):
            print(f"警告: 模板文件不存在 {self.templates_file}")
            return
        
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 解析模板数据
            for item in data:
                master = item.get('master_template', {})
                gen_params = item.get('gen_params', {})
                
                template_id = self._generate_template_id(master.get('name', ''))
                
                # 解析嵌套的params结构
                params = gen_params.get('params', {})
                inner_params = params.get('params', {})  # 内层params包含custom_params
                
                # 判断是否为受限类型（只支持1:1）
                algo_type = gen_params.get('algo_type', '')
                restricted_ratio = algo_type == 'video_diffusion_img2vid'
                
                self.templates[template_id] = {
                    'name': master.get('name'),
                    'uuid': master.get('uuid'),
                    'algo_type': algo_type,
                    'endpoint': gen_params.get('generate_path', '').replace('/api/gw', ''),
                    'result_endpoint': self._get_result_endpoint(gen_params),
                    'module': params.get('module'),
                    'version': params.get('version'),
                    'prompt': params.get('prompt', ''),
                    'template_id': params.get('template_id'),
                    'custom_params': inner_params.get('custom_params', {}),
                    'params': params,
                    'inputs': gen_params.get('inputs', []),
                    # 保存失效标记
                    'deprecated': gen_params.get('deprecated', False),
                    'deprecated_reason': gen_params.get('deprecated_reason', ''),
                    # 标记受限比例
                    'restricted_ratio': restricted_ratio,
                    'supported_ratios': ['1:1'] if restricted_ratio else ['16:9', '1:1', '9:16', '4:3', '3:4'],
                }
            
            print(f"已加载 {len(self.templates)} 个模板")
            
        except Exception as e:
            print(f"加载模板失败: {e}")
    
    def _generate_template_id(self, name: str) -> str:
        """从模板名称生成ID"""
        return (name.lower()
                .replace(' ', '_')
                .replace("'", "")
                .replace('-', '_')
                .replace('（', '')
                .replace('）', '')
                .replace('(', '')
                .replace(')', ''))
    
    def _get_result_endpoint(self, gen_params: Dict) -> str:
        """确定回调路径"""
        algo_type = gen_params.get('algo_type', '')
        result_path = gen_params.get('result_path', '')
        
        # 对于 video_diffusion_img2vid 类型的模板，使用对应的回调路径
        if algo_type == 'video_diffusion_img2vid':
            return '/v3/video/video_diffusion_img2vid/async/results'
        
        # 对于其他模板类型使用 video_diffusion 回调路径
        # 因为 pipeline 回调路径经常返回 404
        if algo_type in ['proto_transformer', 'avatar_transformer', 'style_transformer']:
            return '/v3/video/video_diffusion/async/results'
        
        # 其他使用自己的回调路径
        return result_path.replace('/api/gw', '') if result_path else '/v3/video/video_diffusion/async/results'
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        获取模板配置
        
        Args:
            template_id: 模板ID
            
        Returns:
            模板配置字典，如果模板已失效会添加警告信息
        """
        template = self.templates.get(template_id)
        if template:
            # 检查模板是否已失效
            if template.get('deprecated'):
                print(f"⚠️  警告: 模板 '{template_id}' 已失效")
                print(f"   原因: {template.get('deprecated_reason', 'API端点不再支持')}")
                print(f"   请使用其他替代模板")
        return template
    
    def list_templates(self) -> Dict[str, str]:
        """
        列出所有可用模板
        
        Returns:
            {template_id: template_name}
        """
        return {k: v['name'] for k, v in self.templates.items()}
    
    def get_template_api_config(self, template_id: str) -> Dict[str, Any]:
        """
        获取模板的API配置（用于api_ports.json）
        
        Args:
            template_id: 模板ID
            
        Returns:
            API配置字典
        """
        template = self.get_template(template_id)
        if not template:
            return {}
        
        # 获取支持的宽高比
        supported_ratios = ['16:9', '1:1', '9:16', '3:4', '4:3']
        for input_item in template.get('inputs', []):
            if input_item.get('key') == 'wh_ratio' and 'value_list' in input_item:
                supported_ratios = input_item['value_list']
                break
        
        return {
            'name': template['name'],
            'display_name': template['name'],
            'status': 'untested',
            'endpoint': template['endpoint'],
            'result_endpoint': template['result_endpoint'],
            'algo_type': template['algo_type'],
            'template_id': template['template_id'],
            'supported_ratios': supported_ratios,
            'max_batch_size': 1,
            'tested': False,
            'notes': f'Template: {template["name"]}'
        }
    
    def build_request_data(self, template_id: str, image_uuid: str, **kwargs) -> Dict[str, Any]:
        """
        构建模板请求的完整数据
        
        Args:
            template_id: 模板ID
            image_uuid: 输入图片UUID
            **kwargs: 其他参数
            
        Returns:
            请求数据字典
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"未知模板: {template_id}")
        
        # 获取模板的基础参数
        base_params = template.get('params', {})
        custom_params = template.get('custom_params', {})
        
        # 构建custom_params，保留原有的所有参数
        final_custom_params = dict(custom_params)  # 复制所有原始custom_params
        final_custom_params['master_template_id'] = custom_params.get('master_template_id', template['template_id'])
        
        # 关键: custom_params 中也需要 wh_ratio (抓包发现的差异)
        wh_ratio = kwargs.get('wh_ratio', '1:1')
        final_custom_params['wh_ratio'] = wh_ratio
        
        # 添加用户传入的额外custom_params
        if 'custom_params' in kwargs:
            final_custom_params.update(kwargs['custom_params'])
        
        # 构建请求数据
        data = {
            'module': template['module'],
            'version': template['version'],
            'prompt': kwargs.get('prompt', base_params.get('prompt', '')),
            'images': [image_uuid],
            'masks': [],
            'videos': [],
            'audios': [],
            'params': {
                'mode': kwargs.get('mode', base_params.get('params', {}).get('mode', 'Fast')),
                'style': kwargs.get('style', 'default'),
                'height': kwargs.get('height', -1),
                'width': kwargs.get('width', -1),
                'seed': kwargs.get('seed', -1),
                'duration': kwargs.get('duration', base_params.get('params', {}).get('duration', 5)),
                'motion': kwargs.get('motion', 0),
                'x': kwargs.get('x', 0),
                'y': kwargs.get('y', 0),
                'z': kwargs.get('z', 0),
                'reserved_str': kwargs.get('reserved_str', ''),
                'batch_size': 1,
                'wh_ratio': kwargs.get('wh_ratio', '1:1'),
                'custom_params': final_custom_params
            },
            'en_prompt': kwargs.get('en_prompt', ''),
            'negative_prompt': kwargs.get('negative_prompt', ''),
            'en_negative_prompt': kwargs.get('en_negative_prompt', ''),
            'magic_prompt': kwargs.get('magic_prompt', ''),
            'template_id': template['template_id'],
            'upstream_id': kwargs.get('upstream_id', ''),
            'pipeline_id': kwargs.get('pipeline_id', ''),
            'create_type': 'effect_video_generate',
            'cost_number': kwargs.get('cost_number', 30),
            'request_id': kwargs.get('request_id', ''),
            # 新增 create_submit 字段（网页端必需）
            'create_submit': {
                'create_type': 'effect_video_generate',
                'cost_number': kwargs.get('cost_number', 30),
                'create_number': 1,
                'model_provider': 'vivago',
                'model_name': f"{template['module']}-{template['version']}",
                'effect_type': 'video',
                'effect_id': template['template_id'],
                'effect_name': template['name'],
                'upload_type': 'assets',
                'resource_type': 'image'
            }
        }
        
        return data
    
    def export_to_api_ports(self) -> Dict[str, Any]:
        """
        导出所有模板到api_ports.json格式
        
        Returns:
            端口配置字典
        """
        ports = {}
        for template_id in self.templates:
            config = self.get_template_api_config(template_id)
            if config:
                ports[template_id] = config
        return ports


# 全局模板管理器实例
_template_manager = None

def get_template_manager(templates_file: Optional[str] = None) -> TemplateManager:
    """
    获取全局模板管理器实例（单例模式）
    
    Args:
        templates_file: 模板配置文件路径
        
    Returns:
        TemplateManager实例
    """
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager(templates_file)
    return _template_manager


if __name__ == '__main__':
    # 测试
    manager = get_template_manager()
    
    print("\n可用模板:")
    for tid, name in manager.list_templates().items():
        print(f"  - {tid}: {name}")
    
    print("\n测试获取模板配置:")
    config = manager.get_template('renovation_old_photos')
    if config:
        print(f"  模板: {config['name']}")
        print(f"  端点: {config['endpoint']}")
        print(f"  algo_type: {config['algo_type']}")

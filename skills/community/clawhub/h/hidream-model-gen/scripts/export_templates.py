#!/usr/bin/env python3
"""
将 template_list_full.json 解析并导出为 templates_data.json
用于 template_manager.py 动态加载
"""
import json
import re
import os

def parse_and_export():
    """解析模板文件并导出"""
    
    input_file = 'template_list_full.json'
    output_file = 'templates_data.json'
    
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 {input_file}")
        return
    
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尝试解析JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("JSON格式错误，尝试修复...")
        # 尝试修复常见的JSON格式问题
        content = re.sub(r'},\s*},', '}, },', content)
        content = re.sub(r'},\s*}\s*,\s*\]', '} } ]', content)
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"无法修复JSON: {e}")
            print("尝试手动提取模板数据...")
            # 手动提取
            data = extract_templates_manually(content)
    
    # 验证数据
    if not isinstance(data, list):
        print(f"错误: 数据格式不正确，期望列表但得到 {type(data)}")
        return
    
    print(f"成功解析 {len(data)} 个模板")
    
    # 简化和标准化数据
    simplified = []
    for item in data:
        master = item.get('master_template', {})
        gen_params = item.get('gen_params', {})
        
        simplified_item = {
            'master_template': {
                'uuid': master.get('uuid'),
                'name': master.get('name')
            },
            'gen_params': {
                'algo_type': gen_params.get('algo_type'),
                'generate_path': gen_params.get('generate_path'),
                'result_path': gen_params.get('result_path'),
                'component_type': gen_params.get('component_type', 'video'),
                'inputs': gen_params.get('inputs', []),
                'params': gen_params.get('params', {}),
                'params_version': gen_params.get('params_version', 'v3')
            }
        }
        simplified.append(simplified_item)
    
    # 保存到输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(simplified, f, indent=2, ensure_ascii=False)
    
    print(f"已导出到 {output_file}")
    
    # 显示统计信息
    algo_types = {}
    for item in simplified:
        algo = item['gen_params']['algo_type']
        name = item['master_template']['name']
        if algo not in algo_types:
            algo_types[algo] = []
        algo_types[algo].append(name)
    
    print("\n按 algo_type 分类:")
    for algo, names in sorted(algo_types.items()):
        print(f"  {algo}: {len(names)} 个")
        for name in names:
            print(f"    - {name}")

def extract_templates_manually(content: str) -> list:
    """手动从文本中提取模板数据"""
    templates = []
    
    # 使用正则表达式提取关键信息
    pattern = r'"master_template":\s*\{[^}]*"uuid":\s*"([^"]+)"[^}]*"name":\s*"([^"]+)"[^}]*\}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for uuid, name in matches:
        # 查找对应的 gen_params
        # 简化处理，只提取基本信息
        templates.append({
            'master_template': {'uuid': uuid, 'name': name},
            'gen_params': {
                'algo_type': 'unknown',
                'generate_path': '',
                'result_path': '',
                'params': {}
            }
        })
    
    return templates

if __name__ == '__main__':
    os.chdir('/root/.openclaw/skills/vivago-ai/scripts')
    parse_and_export()

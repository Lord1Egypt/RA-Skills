#!/usr/bin/env python3
"""
解析 template_list 并添加到 api_ports.json
"""
import json
import re

def parse_template_list():
    # 读取文件内容
    with open('template_list_full.json', 'r') as f:
        content = f.read()
    
    # 修复格式问题：移除对象之间的多余逗号
    content = re.sub(r'},\s*},', '}, },', content)
    content = re.sub(r'},\s*}\s*,\s*\]', '} } ]', content)
    
    # 尝试解析
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        print("尝试逐个解析对象...")
        
        # 手动提取每个模板对象
        pattern = r'"master_template":\s*\{[^}]+"uuid":\s*"([^"]+)",\s*"name":\s*"([^"]+)"[^}]*\}[^}]*"gen_params":\s*\{[^}]*"algo_type":\s*"([^"]+)"[^}]*"generate_path":\s*"([^"]+)"[^}]*"result_path":\s*"([^"]+)"'
        
        matches = re.findall(pattern, content, re.DOTALL)
        print(f"找到 {len(matches)} 个模板")
        
        templates = []
        for match in matches:
            uuid, name, algo_type, gen_path, res_path = match
            templates.append({
                'uuid': uuid,
                'name': name,
                'algo_type': algo_type,
                'generate_path': gen_path,
                'result_path': res_path
            })
        
        return templates
    
    # 如果成功解析
    templates = []
    for item in data:
        master = item.get('master_template', {})
        gen_params = item.get('gen_params', {})
        
        templates.append({
            'uuid': master.get('uuid'),
            'name': master.get('name'),
            'algo_type': gen_params.get('algo_type'),
            'generate_path': gen_params.get('generate_path'),
            'result_path': gen_params.get('result_path'),
            'module': gen_params.get('params', {}).get('module'),
            'version': gen_params.get('params', {}).get('version'),
            'prompt': gen_params.get('params', {}).get('prompt', '')
        })
    
    return templates

def main():
    templates = parse_template_list()
    print(f"共解析 {len(templates)} 个模板")
    
    # 按 algo_type 分类
    by_algo = {}
    for t in templates:
        algo = t.get('algo_type', 'unknown')
        if algo not in by_algo:
            by_algo[algo] = []
        by_algo[algo].append(t)
    
    print("\n按 algo_type 分类:")
    for algo, items in by_algo.items():
        print(f"\n{algo}: {len(items)} 个")
        for item in items[:3]:  # 只显示前3个
            print(f"  - {item['name']} ({item['uuid'][:8]}...)")
        if len(items) > 3:
            print(f"  ... 还有 {len(items)-3} 个")

if __name__ == '__main__':
    main()

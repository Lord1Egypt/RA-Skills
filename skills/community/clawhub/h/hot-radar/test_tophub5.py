import requests, re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://tophub.today/',
}

r = requests.get('https://tophub.today/', timeout=15, headers=headers)

# 找所有节点对应的区块（cc-cd 是节点容器）
# 节点 ID 在 class 或 id 里
nodes_html = re.findall(r'<div[^>]+(?:id="node-\d+"|class="[^"]*\bnode\b[^"]*")[^>]*>(.*?)</div>\s*</div>', r.text, re.DOTALL)
print(f'Node blocks: {len(nodes_html)}')

# 更好的方法：找到所有节点 ID 及其标题
node_headers = re.findall(r'class="cc-cd-sb"[^>]*>(.*?)</div>', r.text, re.DOTALL)
print(f'Node headers: {len(node_headers)}')
for h in node_headers[:10]:
    text = re.sub(r'<[^>]+>', '', h).strip()
    print(f'  [{text}]')

# 按节点分区提取所有热榜内容
# 找到包含 "node-" 的 div 容器
node_containers = re.findall(r'id="node-(\d+)"[^>]*>(.*?)(?=id="node-|\Z)', r.text, re.DOTALL)
print(f'\nNode containers (by ID): {len(node_containers)}')
for node_id, content in node_containers[:5]:
    header = re.findall(r'cc-cd-sb[^>]*>(.*?)</div>', content, re.DOTALL)
    h_text = re.sub(r'<[^>]+>', '', header[0]).strip() if header else ''
    items = re.findall(r'class="t">([^<]+)<', content)
    print(f'  Node {node_id} [{h_text}]: {items[:3]}')

# 换一种方式：直接搜索节点容器
node_sections = re.findall(r'(?:id|class)="[^"]*node[^"]*"[^>]*>(.*?)(?=(?:id|class)="[^"]*node[^"]*"|\Z)', r.text, re.DOTALL)
print(f'\nNode sections: {len(node_sections)}')

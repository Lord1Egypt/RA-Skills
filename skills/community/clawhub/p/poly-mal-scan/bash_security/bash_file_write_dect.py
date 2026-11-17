# -*- coding: utf-8 -*-
"""
bash_file_write_dect.py —— 威胁类别:恶意文件写入 检测模块(参考 php_security/file_write_dect.py 判定维度)。

扫描一行(归一化等效代码)的写文件行为(echo >/>>、tee、cp、dd of=、cat >、sed -i 等),
按"目标路径特征 / 危险内容特征"组合判定是否告警。规则数据来自 bash_file_write.json。

判定逻辑(逐条规则):
  - 仅内容命中(规则.仅内容命中=True):命中危险内容特征即告警;
  - 否则:目标路径特征命中 且 危险内容特征命中(无内容特征时仅看路径)。

对外接口:
  scan_file_writes(line, loc, file_write_rules) -> [条目,...]
"""
import re
from bash_common import attach_loc

# 写文件操作判定(用于"仅内容命中"规则):匹配真正的写文件行为,
# 排除 >& 这类文件描述符重定向(反弹 shell 常见,并非写文件)。
_WRITE_RE = re.compile(r'(>>|>\s+(?![&])|tee\s|cp\s|dd\s|cat\s|sed\s+-i|install\s|\|\s*tee)')


def scan_file_writes(line, loc, file_write_rules):
	out = []
	for r in file_write_rules:
		path_feats = r.get('目标路径特征', []) or []
		content_feats = r.get('危险内容特征', []) or []
		write_ops = r.get('写操作特征', []) or []
		only_content = r.get('仅内容命中', False)

		path_hit = any(p and p in line for p in path_feats)
		content_hit = any(c and c in line for c in content_feats) if content_feats else True
		# 写操作:正则主判定(排除 >&),规则自带写操作特征作为补充
		write_hit = bool(_WRITE_RE.search(line)) or any(w and w in line for w in write_ops)

		if only_content:
			hit = content_hit and write_hit
		else:
			hit = path_hit and content_hit and write_hit

		if not hit:
			continue

		reasons = []
		if path_feats:
			reasons += ['目标路径特征:%s' % p for p in path_feats if p and p in line]
		if content_feats:
			reasons += ['危险内容特征:%s' % c for c in content_feats if c and c in line]
		if not reasons:
			reasons = ['命中文件路径特征']

		e = {
			'威胁类型': '恶意文件写入',
			'规则ID': r.get('id'),
			'名称': r.get('名称'),
			'命中特征': reasons,
			'威胁级别': r.get('级别', 3),
			'描述': r.get('描述', ''),
			'参考': r.get('参考', ''),
			'归一化内容': line.strip(),
		}
		attach_loc(e, loc)
		out.append(e)
	return out

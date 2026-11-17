# -*- coding: utf-8 -*-
"""
bash_var_dect.py —— 威胁类别:恶意变量 检测模块(对称于 php_security/dynamic_var_dect.py 的"威胁性变量"思路)。

扫描一行(归一化等效代码)中"危险变量被赋值且赋危险值"的情形(PATH/LD_PRELOAD/BASH_ENV/IFS/...)。
要求该行确实在给该变量赋值(降低误报),且赋值内容命中规则的危险值特征。

对外接口:
  scan_malicious_vars(line, loc, malicious_variables) -> [条目,...]
"""
import re
from bash_common import attach_loc

# 判定某变量在此行被"赋值":前缀可含 export/declare/typeset/setenv/local,后接 VAR =
_ASSIGN_RE = re.compile(
	r'(?:export\s+|declare\s+\S+\s+|typeset\s+\S+\s+|setenv\s+|local\s+)?'
	r'([A-Za-z_]\w*)\s*='
)


def scan_malicious_vars(line, loc, malicious_variables):
	out = []
	for r in malicious_variables:
		var = r.get('变量', '')
		if not var:
			continue
		# 要求该行确实在给该变量赋值(降低误报)
		assigned = any(m.group(1) == var for m in _ASSIGN_RE.finditer(line))
		if not assigned:
			continue
		danger_vals = r.get('危险值特征', [])
		hit_vals = [v for v in danger_vals if v and v in line]
		if hit_vals:
			e = {
				'威胁类型': '恶意变量',
				'规则ID': r.get('id'),
				'名称': r.get('名称'),
				'变量': var,
				'命中危险值特征': hit_vals,
				'危险赋值符': r.get('危险赋值符', []),
				'威胁级别': r.get('级别', 2),
				'描述': r.get('描述', ''),
				'参考': r.get('参考', ''),
				'归一化内容': line.strip(),
			}
			attach_loc(e, loc)
			out.append(e)
	return out

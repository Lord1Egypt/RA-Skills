# -*- coding: utf-8 -*-
"""
bash_cmd_dect.py —— 威胁类别:恶意命令 检测模块。

扫描一行(归一化等效代码)的命令名与危险参数组合。命中规则(命令名 + 任一危险参数子串出现)
即告警,威胁级别取规则 level。依赖 bash_detect_rules.COMMANDS_BY_NAME(命令名→规则列表索引)。

对外接口:
  scan_malicious_commands(line, loc, commands_by_name) -> [条目,...]
"""
from bash_common import first_token, attach_loc


# 命令名允许的"单词字符",其余视为特殊命令(如 fork 炸弹 ':(){')
_WORDCHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-/'


def scan_malicious_commands(line, loc, commands_by_name):
	out = []
	tokens = line.split()
	if not tokens:
		return out
	# 候选命令名:每个 token,以及带点后缀的去掉后缀(如 mkfs.ext4 -> mkfs)
	cand = set(tokens)
	for t in tokens:
		if '.' in t and not t.startswith('.'):
			cand.add(t.split('.', 1)[0])
	first = tokens[0]
	for c, rules in commands_by_name.items():
		# 含非单词字符的命令(如 fork 炸弹 ':(){')按子串匹配;
		# 其余要求命令名作为整词出现(首词,或管道中的任一词,如 base64 管道解码)。
		special = any(ch not in _WORDCHARS for ch in c)
		if special:
			hit_cmd = c in line
		else:
			hit_cmd = (first == c) or (c in cand)
		if not hit_cmd:
			continue
		for r in rules:
			params = r.get('危险参数', [])
			hit_params = [p for p in params if p and p in line]
			if hit_params:
				e = {
					'威胁类型': '恶意命令',
					'规则ID': r.get('id'),
					'名称': r.get('名称'),
					'命令': c,
					'命中危险参数': hit_params,
					'威胁级别': r.get('级别', 3),
					'描述': r.get('描述', ''),
					'参考': r.get('参考', ''),
					'归一化内容': line.strip(),
				}
				attach_loc(e, loc)
				out.append(e)
	return out

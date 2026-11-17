# -*- coding: utf-8 -*-
"""
bash_threat_func_dect.py —— 威胁类别:恶意函数 检测模块(对称于 php_security/threat_func_dect.py)。

扫描一行(归一化等效代码)中的危险内建/函数执行入口(eval/exec/source/./trap)作为命令使用,
并识别"变量作为命令名执行"的动态调用(免杀壳特征)。威胁级别取规则库 level。

对外接口:
  scan_threat_funcs(line, loc, threat_funcs) -> [条目,...]
"""
import re
from bash_common import first_token, attach_loc

# 仅对"高确定性危险内建"作命令使用告警(其余 declare/alias/compgen 等在合法脚本中极常见,不在此自动喷)。
_COMMAND_USE_FUNCS = {'eval', 'exec', 'source', '.', 'trap'}
# 动态命令名:首词形如 $xxx(变量作为命令执行)
_DYN_CMD_RE = re.compile(r'^\$\w')


def _is_func_use(line, name):
	s = line.strip()
	return s == name or s.startswith(name + ' ')


def _mk(name, level, desc, line, loc):
	e = {
		'威胁类型': '恶意函数',
		'函数名': name,
		'威胁级别': level,
		'描述': desc,
		'归一化内容': line.strip(),
	}
	return attach_loc(e, loc)


def scan_threat_funcs(line, loc, threat_funcs):
	out = []
	stripped = line.strip()
	# 1) 显式危险内建/函数作为命令执行
	for f in threat_funcs:
		n = f.name
		if n not in _COMMAND_USE_FUNCS:
			continue
		if n == '.':
			# '.' 命令(等价 source):行首为 '. ' 且不是 './'
			if re.match(r'^\.\s+(?!\.)', stripped):
				out.append(_mk(n, f.threateninglevel, f.desc, line, loc))
		elif _is_func_use(line, n):
			out.append(_mk(n, f.threateninglevel, f.desc, line, loc))
	# 2) 动态命令名(变量作为命令执行,如 $x / $cmd)
	if _DYN_CMD_RE.match(stripped):
		e = {
			'威胁类型': '恶意函数',
			'函数名': first_token(line),
			'威胁级别': 2,
			'告警原因': '变量作为命令名执行(动态调用/免杀壳特征)',
			'归一化内容': stripped,
		}
		attach_loc(e, loc)
		out.append(e)
	return out

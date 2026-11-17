# -*- coding: utf-8 -*-
"""
bash_common.py —— Bash 检测公共工具(对称于 php_security/php_common.py)。
提供:文件读取、命令名提取、归一化定位信息并入威胁条目。
"""
import re


def readfile_bintoutf8_to_list(file_path):
	"""以 utf-8 强行(忽略错误)读取文件并按行返回列表,用于扫描脚本乃至图片中的隐藏内容。"""
	with open(file_path, 'rb') as f:
		return [line.decode('utf-8', errors='ignore') for line in f]


def first_token(line):
	"""取命令行/归一化语句的首个 token(命令名)。忽略首部空白与管道/重定向前缀。"""
	s = line.strip()
	if not s:
		return ''
	m = re.match(r'[^\s|&;()]+', s)
	return m.group(0) if m else ''


def attach_loc(entry, loc):
	"""把归一化定位信息(loc 或 None)并入威胁条目(行/行止/偏移)。"""
	if loc:
		entry['行'] = loc.get('行')
		entry['行止'] = loc.get('行止')
		entry['偏移起'] = loc.get('偏移起')
		entry['偏移止'] = loc.get('偏移止')
	else:
		entry.setdefault('行', None)
		entry.setdefault('行止', None)
		entry.setdefault('偏移起', None)
		entry.setdefault('偏移止', None)
	return entry

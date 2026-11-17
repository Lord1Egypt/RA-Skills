# -*- coding: utf-8 -*-
"""
bash_trait_dect.py —— 威胁类别:特征码威胁 检测模块(对称于 php_security/trait_dect.py)。

以多编码特征码(MULTI_ENC_TRAITS,类别×编码)对代码做子串匹配,命中即标注类别与编码类型。
用于识别被各类混淆编码(base64/url/hex/octal/rot13/html)隐藏的恶意 payload。

对外接口:
  scan_traits(line, loc, multi_enc_traits)   —— 对单行(归一化等效代码)多编码子串匹配
  scan_traits_raw(raw_line, line_num, multi_enc_traits) —— 对原始源码行扫描(补全 AST 遗漏)
"""
from bash_common import attach_loc


def scan_traits(line, loc, multi_enc_traits):
	"""对单行归一化等效代码扫描多编码特征码,返回命中条目(含原文定位)。"""
	out = []
	for cat, enc_dict in multi_enc_traits.items():
		for enc, traits in enc_dict.items():
			for trait in traits:
				if trait and trait in line:
					e = {
						'威胁类型': '特征码威胁',
						'特征码': trait,
						'威胁类别': cat,
						'编码': enc,
						'归一化内容': line.strip(),
					}
					attach_loc(e, loc)
					out.append(e)
	return out


def scan_traits_raw(raw_line, line_num, multi_enc_traits):
	"""对原始源码行扫描多编码特征码(位置只有行号,无精确偏移)。"""
	out = []
	ln = raw_line.strip()
	for cat, enc_dict in multi_enc_traits.items():
		for enc, traits in enc_dict.items():
			for trait in traits:
				if trait and trait in ln:
					out.append({
						'威胁类型': '特征码威胁',
						'特征码': trait,
						'威胁类别': cat,
						'编码': enc,
						'行': line_num,
						'行止': line_num,
						'偏移起': -1,
						'偏移止': -1,
						'归一化内容': ln,
					})
	return out

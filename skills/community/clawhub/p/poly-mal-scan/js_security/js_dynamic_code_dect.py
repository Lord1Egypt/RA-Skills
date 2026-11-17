# -*- coding: utf-8 -*-
"""
js_dynamic_code_dect.py —— 威胁类别②:动态代码执行(与外部可控输入联动) 检测模块。

JS 最常见漏洞:把外部可控输入直接拼进动态执行的代码/HTML。
本模块把「危险 sink」与「外部可控 source」联动判定:
  危险 sink: eval / Function / setTimeout字符串 / innerHTML / outerHTML /
             insertAdjacentHTML / document.write / location跳转
  外部 source: location / document.URL / URLSearchParams / localStorage /
              sessionStorage / event.data / process.env / process.argv
当一行里同时出现「危险 sink」且其参数/赋值来源涉及外部输入时,认定为威胁。

对外接口:
  scan_dynamic_code(file_content_line, lines_upto, fileline_num,
                    sink_names, external_source_re)
    返回该类别威胁条目列表(可空)。
"""
import re
from js_common import (
	find_js_variable_assignment_incodelist,
	find_external_input_inlist,
	find_js_function_calls,
)
#危险sink(动态执行/注入点)
SINKS=[
	'eval','Function','new Function','setTimeout','setInterval',
	'innerHTML','outerHTML','insertAdjacentHTML','document.write',
	'document.writeln','location.href','location.assign','location.replace',
	'window.open','document.location','document.cookie',
]
def scan_dynamic_code(file_content_line,lines_upto,fileline_num,sink_names=None,external_source_re=None):
	if sink_names is None:sink_names=SINKS
	threats=[]
	calls=find_js_function_calls(file_content_line,sink_names)
	for c in calls:
		params=c['参数']
		params_raw=' '.join(params)
		external_hit=find_external_input_inlist([params_raw])#参数或其变量赋值来源是否含外部输入
		vars_in=re.findall(r'\b[A-Za-z_$][\w$]*\b',params_raw)
		assign=[]
		if vars_in:
			assign=find_js_variable_assignment_incodelist(lines_upto,vars_in)
			if not external_hit:
				if find_external_input_inlist(assign):external_hit=True
		if external_hit:
			threats.append({
				"威胁类型":"动态代码执行",
				"sink":c['函数名'],
				"参数":params_raw,
				"涉及外部输入":external_hit,
				"行数":fileline_num,
				"威胁性内容":file_content_line,
				"参数来源":assign,
				"威胁级别":4,
			})
	return threats

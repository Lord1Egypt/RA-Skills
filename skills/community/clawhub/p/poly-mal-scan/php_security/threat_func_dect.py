#-*- coding:utf-8 -*-
"""
threat_func_dect.py —— 威胁类别①:恶意函数执行 检测模块。

扫描一行 PHP 代码中的危险函数调用(threatening_funcs),
并追踪调用参数是否来源于超全局变量(外部可控)→ 威胁级别 +1。

对外接口:
  scan_threat_funcs(file_content_line,lines_upto,fileline_num,threatening_funcs)
	 file_content_line :当前待扫描的一行
	 lines_upto		  :截至当前行(含)的历史代码行列表,用于参数溯源
	 fileline_num		:当前行号(从1起)
	 threatening_funcs :威胁函数规则库(detect_rules.threatening_funcs)
	 返回该类别威胁条目列表(可空)。
"""
import re
from php_common import (
	find_php_variables,
	find_php_variable_assignment_incodelist,
	find_php_superglobals_inlist,
	find_php_superglobals,
	find_php_function_calls,
)
#文件IO/文件系统类函数: 单独使用(无外部可控输入)属正常业务(读图片/写CSV/写日志等), 只有参数涉及超全局输入(外部可控)时才作为"恶意函数执行"上报, 否则跳过避免误报(b03/b04/b05 类)。
#真正的"文件写入攻击"由 file_write_dect(威胁类别④) 按内容/路径/超全局精确判定。
IO_GATED={'fopen','fread','fwrite','fputs','file_get_contents','file','readfile',
	'show_source','highlight_file','tmpfile','tempnam','readgzfile','gzopen','gzfile',
	'copy','rename','move_uploaded_file','unlink','rmdir','chmod','touch',
	'file_put_contents'}
#回调型函数: 正常业务广泛用于数组处理/排序/格式化(如 array_map('trim', $rows)), 只有"回调目标来自外部可控输入"时才构成代码执行后门。
#硬编码的函数名字符串与闭包字面量属正常用法, 命中即报会造成严重误报。
CALLBACK_GATED={'call_user_func','call_user_func_array','array_map','array_filter',
	'array_walk','array_walk_recursive','usort','uksort','uasort',
	'array_reduce','preg_replace_callback','register_shutdown_function',
	'set_error_handler','set_exception_handler'}
def _superglobals_in_args(args):return bool(find_php_superglobals('  '.join(args)))#判断函数参数文本是否直接含超全局变量(外部可控)
def find_threatening_php_function_call(line,function_names):return find_php_function_calls(line,function_names)#寻找威胁函数的执行行为
def scan_threat_funcs(file_content_line,lines_upto,fileline_num,threatening_funcs):
	threats=[]
	func_names=[f.name for f in threatening_funcs]
	for r in find_threatening_php_function_call(file_content_line,func_names):
		phpfunc_threatening=next((f for f in threatening_funcs if f.name==r['函数名']),None)
		if phpfunc_threatening is None:continue
		threateninglevel_diff=0
		p=[]  # 参数是否来源于超全局(外部可控); 缺省空(不可控), 供 IO_GATED/CALLBACK_GATED 门槛引用
		phpfunc_parameters=find_php_variables(' '.join(r['参数']))#如果发现危险函数，则获取其参数
		phpfunc_parameters_assignment=[]
		if phpfunc_parameters!=[]:#如果危险函数有参数，则追踪参数来源
			phpfunc_parameters_assignment=find_php_variable_assignment_incodelist(lines_upto,phpfunc_parameters)
			p=find_php_superglobals_inlist(phpfunc_parameters_assignment)#确认参数是否来源于超全局变量
			threateninglevel_diff=1 if p!=[]and p!=None else threateninglevel_diff#发现参数来自于超全局变量，则威胁等级加1
		if r['函数名'] in IO_GATED and not phpfunc_parameters_assignment:continue
		if r['函数名'] in IO_GATED and not (_superglobals_in_args(r['参数'])):continue
		if r['函数名'] in CALLBACK_GATED and not (p or _superglobals_in_args(r['参数'])):continue
		threats.append({
			"威胁类型":"恶意函数执行",
			"函数名":r['函数名'],
			"参数":' '.join(r['参数']),
			"威胁级别":phpfunc_threatening.threateninglevel+threateninglevel_diff,
			"行数":fileline_num,
			"威胁性内容":file_content_line,
			"参数来源":phpfunc_parameters_assignment,
		})
	return threats

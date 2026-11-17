# -*- coding: utf-8 -*-
"""
js_threat_func_dect.py —— 威胁类别①:恶意函数/API 执行 检测模块。

扫描一行 JS 代码中的危险函数/API 调用(threatening_funcs),
并追踪调用参数是否来源于外部可控输入(location/localStorage/event.data/process.env 等)→ 威胁级别 +1。

双用途 API 门槛(2026-09-02 新增):
  诸如 fetch / setInterval / require / atob / writeFile 这类 API 本身中性,
  正常业务与恶意代码都会使用。若"出现即告警", 正常前端/Node 代码会被大量误报
  (实测阴性对照误报率 100%)。故引入门槛: 只有当调用具备攻击语义时才上报,
  设计对称于 php threat_func_dect 的 IO_GATED。未列入门槛集合的函数
  (eval / exec / system 等)本身即高危, 出现即报。

对外接口:
  scan_threat_funcs(file_content_line, lines_upto, fileline_num, threatening_funcs)
    file_content_line : 当前待扫描的一行
    lines_upto        : 截至当前行(含)的历史代码行列表,用于参数溯源
    fileline_num      : 当前行号(从1起)
    threatening_funcs : 威胁函数规则库(js_detect_rules.threatening_funcs)
    返回该类别威胁条目列表(可空)。
"""
import re
from js_common import (
	find_js_variables,
	find_js_variable_assignment_incodelist,
	find_external_input_inlist,
	find_js_function_calls,
)
#============双用途API门槛集合============
#网络请求类: 正常业务一般用同源相对路径('/api/x'), 硬编码外部地址或外发敏感数据才告警
NET_GATED={'fetch','XMLHttpRequest','sendBeacon','WebSocket','axios'}
#定时器类: 正常用于轮询刷新, 回调体命中外部地址/敏感数据/危险特征才告警
TIMER_GATED={'setTimeout','setInterval','requestAnimationFrame','queueMicrotask'}
#子进程类: 以参数数组调用时不经 shell 解析, 无注入面; 命中 shell/下载执行特征才告警
CHILD_GATED={'execFile','execFileSync','spawn','spawnSync','fork'}
#编解码类: 单独出现只是普通编码常量, 解码内容涉及外部输入才告警
CODEC_GATED={'atob','btoa','decodeURIComponent','decodeURI','unescape','encodeURIComponent'}
#模块引入类: 纯字面量属正常依赖声明; 动态引入(变量/拼接/外部输入)才告警
REQUIRE_GATED={'require'}
#文件写入类: 一律交给 js_file_write_dect 的 5 条规则精确判定, 此处不重复上报
WRITE_GATED={'writeFile','writeFileSync','appendFile','appendFileSync',
	'createWriteStream','write','truncate','truncateSync'}
#外部绝对地址(http/https/ws/wss/ftp等)
_EXTERNAL_URL_RE=re.compile(r'[a-z]+://[^\s\'"`]+',re.I)
#敏感数据/采集行为: 外发这些内容即具备窃取语义
_SENSITIVE_DATA_RE=re.compile(
	r'document\.cookie|localStorage|sessionStorage|toDataURL|getUserMedia|'
	r'getDisplayMedia|MediaRecorder|ImageCapture|clipboardData|navigator\.clipboard|'
	r'id_rsa|credentials|/etc/(?:passwd|shadow)',re.I)
#危险特征: shell 调用/下载执行/代码执行
_DANGEROUS_HINT_RE=re.compile(
	r'/bin/(?:ba)?sh\b|\bcmd\.exe\b|powershell|\|\s*(?:ba)?sh\b|'
	r'\b(?:curl|wget)\b|\beval\s*\(|\bnew\s+Function\b|child_process|__proto__',re.I)
#纯字符串字面量(静态依赖声明)
_PURE_LITERAL_RE=re.compile(r"^\s*['\"][^'\"]*['\"]\s*$")
def _gate_pass(func_base,params,assignments):#双用途API的放行判定:返回True才作为"恶意函数执行"上报。func_base:函数名去掉对象前缀后的末段(如fs.writeFileSync→writeFileSync);params:实参文本列表;assignments:实参中变量的赋值溯源结果
	probe=' '.join(params)
	if assignments:probe+=' '+' '.join(assignments)
	ext=bool(find_external_input_inlist([probe]))#实参或其赋值来源涉及外部可控输入(location/process.env/event.data等)
	if func_base in NET_GATED:
		return bool(_EXTERNAL_URL_RE.search(probe)or _SENSITIVE_DATA_RE.search(probe))#注意:不能仅凭"参数溯源到外部输入(location等)"就放行——正常前端"读地址栏参数→请求同源API"是最常见合法模式(见样本23),会海量误报。只有"请求外部绝对地址"或"外发敏感数据(cookie/localStorage/媒体采集)"才具攻击语义
	if func_base in TIMER_GATED:
		return ext or bool(_EXTERNAL_URL_RE.search(probe)or _SENSITIVE_DATA_RE.search(probe)or _DANGEROUS_HINT_RE.search(probe))
	if func_base in CHILD_GATED:
		return ext or bool(_DANGEROUS_HINT_RE.search(probe))
	if func_base in CODEC_GATED:
		return ext
	if func_base in REQUIRE_GATED:
		return ext or not _PURE_LITERAL_RE.match(' '.join(params)or'')#动态引入(模块名为变量/拼接/外部输入)才告警;纯字面量属正常依赖声明
	if func_base in WRITE_GATED:
		return False#交由js_file_write_dect按5条规则精确判定
	return True#未列入门槛:本身即高危,出现即报
def find_threatening_js_function_call(line,function_names):return find_js_function_calls(line,function_names)#用通用调用解析(支持嵌套括号),一次查多个函数名
def scan_threat_funcs(file_content_line,lines_upto,fileline_num,threatening_funcs):
	threats=[]
	func_names=[f.name for f in threatening_funcs]
	for r in find_threatening_js_function_call(file_content_line,func_names):
		phpfunc_threatening=next((f for f in threatening_funcs if f.name==r['函数名']),None)
		if phpfunc_threatening is None:continue
		level_diff=0
		params=r['参数']
		vars_in_params=find_js_variables(' '.join(params))#提取参数中的变量名
		assignments=[]
		if vars_in_params:
			assignments=find_js_variable_assignment_incodelist(lines_upto,vars_in_params)
			if find_external_input_inlist(assignments):level_diff=1#赋值来源是否外部可控
		if not _gate_pass(r['函数名'].split('.')[-1],params,assignments):continue#双用途API门槛:过滤掉"只是正常业务用法"的调用
		threats.append({
			"威胁类型":"恶意函数执行",
			"函数名":r['函数名'],
			"参数":' '.join(params),
			"威胁级别":phpfunc_threatening.threateninglevel+level_diff,
			"行数":fileline_num,
			"威胁性内容":file_content_line,
			"参数来源":assignments,
		})
	return threats

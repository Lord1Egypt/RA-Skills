# -*- coding: utf-8 -*-
"""
js_file_write_dect.py —— 威胁类别④:自我复制/文件写入 检测模块。

扫描一行 JS 代码中的文件写入行为(fs.writeFile/appendFile/createWriteStream等),
并按规则判定是否告警、威胁级别与告警原因:
  1. 自我复制(读 __filename/require.main 再写自身)      -> 4 级
  2. 写入内容/路径涉及外部可控输入(location/env/argv等)  -> 3 级
  3. 写配置文件(.env/config/package.json/nginx.conf等)   -> 3 级
  4. 向 .js 等脚本文件写入可识别恶意代码               -> 4 级
  5. 写跨语言后门(.php/.py/.sh 等含恶意内容)           -> 4 级
取多条规则命中的最高级别作为该写入行为的威胁级别。

对外接口:
  scan_file_writes(file_content_line, lines_upto, fileline_num, file_context,
                   threatening_funcs, multi_enc_traits)
    返回该类别威胁条目列表(可空)。
"""
import re
from js_common import (
	find_js_variable_assignment_incodelist,
	find_external_input_inlist,
	find_js_function_calls,
)
# 配置文件/环境文件特征(命中即按规则3告警)
CONFIG_FILE_TRAITS=[
	'.env','config','package.json','package-lock.json','npmrc','yarn.lock',
	'php.ini','.htaccess','nginx.conf','httpd.conf','my.cnf','settings.json',
	'application.properties','.bashrc','.profile','id_rsa','ecdsa','/etc/',
]
# JS 可执行/可注入的脚本扩展名(规则4/5)
SCRIPT_EXTENSIONS={'.js','.mjs','.cjs','.json','.html','.htm','.jsx','.ts','.vue'}
def _ext(path):#提取小写扩展名(含点),非文件型返回''
	probe=path.strip()
	if len(probe)>=2 and probe[0] in ("'",'"') and probe[-1]==probe[0]:probe=probe[1:-1]
	m=re.search(r'\.([A-Za-z0-9_]+)$',probe)
	return ('.'+m.group(1).lower())if m else ''
def _has_script_marker(content):#内容是否含JS/HTML代码标记
	return bool(re.search(r'<\s*script|function\s*\(|=>|;|eval\s*\(',content))
def _write_config_dect(path_args,content):
	hit=[]
	probe=' '.join(path_args)+' '
	if content:probe+=content
	for trait in CONFIG_FILE_TRAITS:
		if trait in probe:hit.append(trait)
	return hit
def _self_copy_dect(func_name,file_context):#规则1:自我复制——读自身源码(__filename/require.main/module.id)再写入。func_name:本次写入调用的函数名;file_context:整个文件上下文
	hit=[]
	# 本次是文件写入操作(writeFile/appendFile/createWriteStream/write)
	has_write=bool(re.search(r'writeFile|createWriteStream|appendFile',func_name))
	if not has_write:return hit
	# 文件级存在「读自身源码」行为
	read_self=bool(re.search(
		r'read(?:File|FileSync)\s*\(\s*__filename|'
		r'read(?:File|FileSync)\s*\(\s*require\.main|'
		r'__filename|'
		r'process\.mainModule',
		file_context))
	if read_self:hit.append('自我复制(读自身源码再写入)')
	return hit
def _external_input_dect(path_args,file_context):#规则2:写入路径/内容来自外部可控输入
	hit=[]
	if find_external_input_inlist(path_args):hit.append('写入路径涉及外部可控输入')
	return hit
def _malicious_script_dect(path_args,content,threatening_funcs,multi_enc_traits):#规则4/5:写脚本文件且内容可识别为恶意代码
	if not content:return []
	is_script=any(_ext(p) in SCRIPT_EXTENSIONS or p.lower().endswith('.php') for p in path_args)
	# 内容命中威胁函数名
	mal=set()
	for fn in threatening_funcs:
		base=fn.name.split('.')[-1]
		if re.search(r'\b'+re.escape(base)+r'\s*\(',content):mal.add('恶意API:%s'%base)
	# 命中特征码
	for threat_type,enc_dict in multi_enc_traits.items():
		for enc_name,traits in enc_dict.items():
			for trait in traits:
				if trait in content:mal.add('%s(%s特征)'%(threat_type,enc_name))
	# 跨语言后门(.php等不含在SCRIPT_EXTENSIONS里,单独判定)
	php_target=any(p.lower().endswith('.php') for p in path_args)
	hit=[]
	if php_target and mal:hit.append('写PHP后门:%s'%','.join(mal))
	elif is_script and mal:hit.append('写恶意脚本:%s'%','.join(mal))
	return hit
def scan_file_writes(file_content_line,lines_upto,fileline_num,file_context,threatening_funcs,multi_enc_traits):
	threats=[]
	# 文件写入函数集合
	write_funcs=['fs.writeFile','fs.writeFileSync','fs.appendFile','fs.appendFileSync',
		'fs.createWriteStream','writeFile','writeFileSync','appendFile','createWriteStream',
		'write','fs.write']
	write_list=find_js_function_calls(file_content_line,write_funcs)
	for w in write_list:
		params=w['参数']
		params_raw=' '.join(params)
		# 参数赋值来源
		vars_in=re.findall(r'\b[A-Za-z_$][\w$]*\b',params_raw)
		assign=find_js_variable_assignment_incodelist(lines_upto,vars_in)
		reasons,level=[],0
		probe_args=list(params)+list(assign)
		probe_content=params_raw+' '+(' '.join(assign)if assign else '')
		# 规则1 自我复制
		sc=_self_copy_dect(w['函数名'],file_context)
		if sc:reasons+=sc;level=max(level,4)
		# 规则2 外部可控
		ext=_external_input_dect(probe_args,file_context)
		if ext and find_external_input_inlist(probe_args):reasons+=['写入涉及外部可控输入'];level=max(level,3)
		# 规则3 配置文件
		cfg=_write_config_dect(probe_args,probe_content)
		if cfg:reasons+=[('写配置文件:%s'%','.join(cfg))];level=max(level,3)
		# 规则4/5 恶意脚本
		mal=_malicious_script_dect(probe_args,probe_content,threatening_funcs,multi_enc_traits)
		if mal:reasons+=mal;level=max(level,4)
		if reasons:
			threats.append({
				"威胁类型":"自我复制/文件写入",
				"函数名":w['函数名'],
				"参数":params,
				"告警原因":reasons,
				"威胁级别":level,
				"行数":fileline_num,
				"威胁性内容":file_content_line,
				"参数来源":assign,
			})
	return threats

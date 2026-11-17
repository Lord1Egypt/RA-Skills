"""
file_write_dect.py —— 威胁类别④:自我复制/文件写入 检测模块。

扫描一行PHP代码中的文件写入行为(file_put_contents/fwrite),
并按6条规则判定是否告警、威胁级别与告警原因:
	1.自我复制										3级
	2.写入内容/路径涉及超全局变量(外部可控)		2级
	3.写配置文件(PHP/HTTP服务器/数据库等环境)	3级
	4.涉及session.serialize_handler反序列化		4级
	5.向非php文件写入php代码					3级
	6.向php文件写入可识别恶意代码				4级
取多条规则命中的最高级别作为该写入行为的威胁级别。

对外接口:
	scan_file_writes(file_content_line,lines_upto,fileline_num,file_context,threatening_funcs,multi_enc_traits)
		file_content_line	当前待扫描的一行
		lines_upto			截至当前行(含)的历史代码行列表,用于变量赋值/超全局溯源
		fileline_num		当前行号(从1起)
		file_context		整个文件的拼接文本(供规则4跨行感知 serialize_handler 配置)
		threatening_funcs/multi_enc_traits	规则库(detect_rules)
		返回该类别威胁条目列表(可空)。
"""
import re
from php_common import (
	find_php_variable_assignment_incodelist,
	find_php_superglobals_inlist,
	find_php_function_calls,
)
#PHP 扩展名集合(写入目标若为此类且内容含恶意代码,按规则6告警)
PHP_EXTENSIONS={'.php','.php3','.php4','.php5','.php7','.phtml','.pht','.phar'}
#配置文件/环境文件特征(命中即按规则3告警)。覆盖:PHP环境(php.ini/.user.ini)、HTTP服务器(apache.htaccess/httpd.conf、nginx.conf)、数据库(my.cnf/my.ini/config/database等)。
CONFIG_FILE_TRAITS=[
	'php.ini','.user.ini','.htaccess','httpd.conf','apache2.conf','nginx.conf','nginx.ini',
	'my.cnf','my.ini','mysql.conf','mysqld.conf','pg_hba.conf','postgresql.conf',
	'config.php','database.php','db.php','settings.php','application.ini','bootstrap.ini',
	'wp-config.php','.env','env.php','parameters.php','.htpasswd','.htgroups',
]
#=================判定层:6条告警规则的辅助判定 =================
def _php_extension(path):#从路径中提取小写扩展名(含点),非文件型路径返回''
	#先剥离路径首尾的引号('...'/"..."),再取扩展名
	probe=path.strip()
	if len(probe)>=2 and probe[0] in ("'",'"') and probe[-1]==probe[0]:probe=probe[1:-1]
	#截取最后一个路径段(避免目录/查询串干扰)
	m=re.search(r'([^/\\\\/\s]+)$',probe)
	tail=m.group(1)if m else probe
	m2=re.search(r'\.([A-Za-z0-9_]+)$',tail)
	return ('.'+m2.group(1).lower())if m2 else ''
def _has_php_code_marker(content):#内容是否含PHP代码标记
	return bool(re.search(r'<\?(?:php|=|\s)',content))
def _write_config_file_dect(path_args,content):#规则3:写入目标是否为配置文件(PHP/HTTP服务器/数据库等环境配置)。判定依据:把「路径参数」和「写入内容」拼起来,如果出现CONFIG_FILE_TRAITS中的文件名特征,即视为写配置文件。返回命中的特征列表(空=未命中)
	hit=[]
	probe=' '.join(path_args)+' '
	if content:probe+=content
	for trait in CONFIG_FILE_TRAITS:
		if trait in probe:hit.append(trait)
	return hit
def _session_serialize_dect(path_args,content,file_context=''):#规则4:是否涉及session.serialize_handler的反序列化操作。判定依据(需同时满足,避免误报普通serialize调用):a.文件级上下文出现session.serialize_handler配置;b.本次写入涉及session(路径指向session文件或内容含PHP序列化特征)
	hit=[]
	probe=' '.join(path_args)+' '
	if content:probe+=content
	#a.文件级是否配置了serialize_handler
	file_cfg=('session.serialize_handler' in file_context) or ('session.serialize_handler' in probe)
	if not file_cfg:return hit
	#b.本次写入是否涉及session/序列化
	sess_hint=bool(re.search(r'(?:session_save_path|session_id|session_name|sess_|session_start)',probe))
	sess_content=bool(re.search(r'(?:[;|]|^)\s*[OaCsd]:\d+:',probe))#O:/a:/s:/i:d:序列化特征
	if sess_hint or sess_content:hit.append('session.serialize_handler反序列化写入')
	return hit
def _write_php_into_nonphp_dect(path_args,content):#规则5:向非PHP文件写入PHP代码。判定依据:路径扩展名不是php类扩展名,且写入内容含PHP代码标记。无扩展名/无法解析的路径不视为非php,仅当能明确判定扩展名且非PHP时才算
	if not content:return []
	if not _has_php_code_marker(content):return []
	hit=[]
	for p in path_args:
		ext=_php_extension(p)
		if ext and ext not in PHP_EXTENSIONS:hit.append('%s(向%s写入PHP代码)'%(p,ext))
	return hit
def _write_malicious_to_php_dect(path_args,content,threatening_funcs,multi_enc_traits):#规则6:向PHP文件写入可被识别为恶意的代码。判定依据:目标扩展名属于PHP类,且写入内容命中威胁函数库或威胁特征码。检测目标是「写入内容」而非「整个文件」
	if not content:return []
	is_php_target=any(_php_extension(p) in PHP_EXTENSIONS for p in path_args if _php_extension(p))
	if not is_php_target:return []
	hit=[]
	#1.命中威胁函数名
	for fn in threatening_funcs:
		if re.search(r'\b'+re.escape(fn.name)+r'\s*\(',content):hit.append('恶意函数:%s'%fn.name)
	#2.命中多编码威胁特征码
	for threat_type,enc_dict in multi_enc_traits.items():
		for enc_name,traits in enc_dict.items():
			for trait in traits:
				if trait in content:hit.append('%s(%s编码特征)'%(threat_type,enc_name))
	return hit
def phpfile_write_threat_dect(path_args,content,file_context,threatening_funcs,multi_enc_traits):#对一次文件写入行为做全量告警判定,返回(是否告警,威胁级别,命中的告警原因)。面向6条告警规则，取多条规则命中的最高级别
	reasons,level=[],0
	#规则1:自我复制
	if '__FILE__' in ' '.join(path_args) or '__DIR__' in ' '.join(path_args):
		reasons.append('自我复制(写入自身/所在目录)')
		level=max(level,3)
	#规则2:涉及超全局变量——由调用方传入已经解析好的p判断(外部可控)
	cfg=_write_config_file_dect(path_args,content)
	if cfg:
		reasons.append('写配置文件:%s'%(','.join(cfg)))
		level=max(level,3)
	#规则4:session serialize_handler反序列化
	sess=_session_serialize_dect(path_args,content,file_context)
	if sess:
		reasons.append('session反序列化:%s'%(','.join(sess)))
		level=max(level,4)
	#规则5:向非php文件写php代码
	np=_write_php_into_nonphp_dect(path_args,content)
	if np:
		reasons.append('向非php文件写PHP代码:%s'%(','.join(np)))
		level=max(level,3)
	#规则6:向php文件写入恶意代码
	mal=_write_malicious_to_php_dect(path_args,content,threatening_funcs,multi_enc_traits)
	if mal:
		reasons.append('向PHP文件写入恶意代码:%s'%(','.join(mal)))
		level=max(level,4)
	return (bool(reasons),level,reasons)
#=================对外主接口=================
def scan_file_writes(file_content_line,lines_upto,fileline_num,file_context,threatening_funcs,multi_enc_traits):
	threats=[]
	write_list=find_php_function_calls(file_content_line,["file_put_contents","fwrite"])#文件写入行为扫描
	for write_exec in write_list:
		write_parameters=write_exec['参数']
		write_parameters_raw=' '.join(write_parameters)#参数拼接成字符串便于统一扫描
		#追踪写入参数的赋值来源(变量 <=> 可读文本)
		r=find_php_variable_assignment_incodelist(lines_upto,write_parameters)
		#检查参数本身及其赋值来源是否涉及超全局输入(外部可控)
		p=find_php_superglobals_inlist(r)if r else []
		if not p:p=find_php_superglobals_inlist(write_parameters)
		involves_sg=bool(p)
		#合并所有需要用到的可读判定文本:参数原文+赋值来源
		probe_args=list(write_parameters)+list(r)
		#内容判定用:写入参数正文(去除纯路径因素亦可,统一用全文)
		probe_content=write_parameters_raw+' '+(' '.join(r)if r else '')
		#全量告警判定(规则1/3/4/5/6)
		is_threat,threat_level,reasons=phpfile_write_threat_dect(probe_args,probe_content,file_context,threatening_funcs,multi_enc_traits)
		#规则2:涉及超全局变量(外部可控) → 一律告警
		if involves_sg:
			reasons.append('写入内容/路径涉及超全局变量(外部可控)')
			threat_level=max(threat_level,2)
		#规则1的自我复制同时也在is_threat里;再兜底一次__FILE__硬检测防止遗漏
		is_threat=is_threat or involves_sg or('__FILE__'in write_parameters_raw)
		if is_threat:
			if not threat_level:threat_level=2
			threats.append({
				"威胁类型":"自我复制/文件写入",
				"函数名":write_exec["函数名"],
				"参数":write_parameters,
				"告警原因":reasons,
				"威胁级别":threat_level,
				"行数":fileline_num,
				"威胁性内容":file_content_line,
				"参数来源":r,
				"涉及超全局":p,
			})
	return threats

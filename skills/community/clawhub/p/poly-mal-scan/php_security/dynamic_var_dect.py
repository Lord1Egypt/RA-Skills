"""
dynamic_var_dect.py —— 威胁类别②:威胁性动态变量 检测模块。

扫描一行 PHP 代码中的可变变量($$var)。
只有当动态变量「涉及超全局变量赋值」时才认定为威胁;
孤立的$$变量(如在二进制数据里随机出现的'$$o')无变量来源、无威胁,直接丢弃,
避免图片/高熵数据严重误报。

对外接口:
	scan_dynamic_vars(file_content_line,lines_upto,fileline_num)
		file_content_line	当前待扫描的一行
		lines_upto			截至当前行(含)的历史代码行列表,用于变量赋值溯源
		fileline_num		当前行号(从1起)
		返回该类别威胁条目列表(可空)。
"""
import re
from php_common import (
	find_php_variable_assignment_incodelist,
	find_php_superglobals_inlist,
)
#匹配$$变量(支持单字母变量名,如$$a)。
#注意:是否会误报取决于后续"是否涉及超全局变量"的实质判定,单独靠变量名长度无法区分真实$$a与二进制里的随机'$$o'。
_DYNAMIC_RE=re.compile(r'\$\$[a-zA-Z_]\w*')
#动态变量溯源时用于识别"超全局操作"的特征(忽略大小写)
_SG_HINT_RE=r"(?i)_(?:request|post|get|files|cookie|server|env|session)+"
#外部可控动态函数调用:超全局(或其下标)直接作为函数名执行,如$_POST['f']($_POST['a'])/$_GET[$_GET['f']](...)/$_COOKIE['c']()。
#这是"免杀壳"最典型形态之一(将函数名放到外部输入里),正则\b查不到非字面函数名,AST归一化对下标动态调用也无效,故在此单独识别。
_DYNFUN_SC=('$_GET','$_POST','$_REQUEST','$_COOKIE')
#超全局下标立即跟随(的调用形态;下标支持嵌套(i.e.$_GET[$_GET['f'])
_DYNFUN_RE=re.compile(r'\$_(?:GET|POST|REQUEST|COOKIE)\s*\[[^\n]*?\]\s*\(')
def php_dynamicvariable_dect(php_code):return _DYNAMIC_RE.findall(php_code)
def scan_dynamic_func_calls(file_content_line,fileline_num):#识别外部可控的动态函数调用(超全局下标作函数名)。如$_POST['f'](...)/$_GET[$_GET['f']](...)/$_COOKIE[..](...)。返回威胁条目列表。用平衡扫描处理嵌套下标:从超全局定位,数[]深度到归零且紧跟(即命中。
	s=file_content_line
	out=[]
	for m in re.finditer(r'\$_(?:GET|POST|REQUEST|COOKIE)\s*\[',s):
		start=m.start()
		depth=0;i=m.end()-1#指向'['
		quoted=None
		ok=False
		while i<len(s):
			c=s[i]
			if quoted:
				if c=='\\':i+=2;continue
				if c==quoted:quoted=None
				i+=1;continue
			if c in ("'",'"'):quoted=c;i+=1;continue
			if c=='[':depth+=1
			elif c==']':
				depth-=1
				if depth==0:
					ok=(i+1<len(s) and s[i+1]=='(')
					break
			i+=1
		if not ok:continue
		seg=s[start:i+1]
		out.append({
			"威胁类型":"威胁性动态变量",
			"变量名":[seg.strip()],
			"动态函数名调用":seg.strip(),
			"行数":fileline_num,
			"威胁性内容":s,
			"威胁级别":2,
			"告警原因":"外部可控变量作为函数名执行(免杀壳特征)",
		})
	return out
def scan_dynamic_vars(file_content_line,lines_upto,fileline_num):
	php_dynamicvariable=php_dynamicvariable_dect(file_content_line)#威胁性动态变量的扫描
	if php_dynamicvariable==[]:return []
	php_dynamicvariable2=[x[1:]for x in php_dynamicvariable]
	r=find_php_variable_assignment_incodelist(lines_upto,php_dynamicvariable2)
	p=find_php_superglobals_inlist(r,_SG_HINT_RE)
	if p:
		return [{
			"威胁类型":"威胁性动态变量",
			"变量名":php_dynamicvariable,
			"行数":fileline_num,
			"涉及超全局变量行为":p,
			"威胁性内容":file_content_line,
			"威胁级别":2,
		}]
	return []

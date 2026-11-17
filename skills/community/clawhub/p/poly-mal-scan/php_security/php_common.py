#php_common.py —— 各检测模块共用的PHP静态分析工具函数(纯正则,无php依赖)
#供四大检测模块(threat_func_dect/dynamic_var_dect/trait_dect/file_write_dect)及主程序 phpdect.py共用
import re

def find_php_variables(line):#寻找php代码中提及的所有变量名
	return re.findall(r'\$\w+',line)

def find_php_variable_assignment(php_code,variable_name):#寻找指定一个变量赋值的行为
	pattern=rf'^(?!\s*//).*\${re.escape(variable_name[1:])}\s*=\s*[^;]+;'#匹配 $var = ...; 的模式
	return re.findall(pattern,php_code)

def find_php_variable_assignment_inlist(php_code,variable_names):#寻找单个php代码字符串中对多个变量的赋值行为
	result=[]
	for variable_name in variable_names:
		result+=find_php_variable_assignment(php_code,variable_name)
	return result

def find_php_variable_assignment_incodelist(php_code_list,variable_names):#寻找多行代码中对多个变量的赋值行为
	result=[]
	for line in php_code_list:
		r=find_php_variable_assignment_inlist(line,variable_names)
		result+=r
	return result

def find_php_superglobals(php_code,thepattern=''):#对单个php代码字符串进行超全局变量扫描
	pattern=r'\$_(request|post|get|files|cookie|server|env|session)\s*\[\s*[\'"]?(\w+)[\'"]?\s*\]'
	if thepattern!='':pattern=thepattern
	#re.I:PHP 超全局变量标准写法为大写(如 $_GET/$_POST),
	#原正则写的是小写(get/post)且大小写敏感,导致真实超全局永远匹配不到。
	#此处统一忽略大小写,兼容 $_GET/$_POST 等标准写法。
	matches=re.findall(pattern,php_code,re.I)
	results=[]
	for match in matches:
		#match 为 (method,field) 元组;method 输出为可读的 $_GET 形式
		method=field=''
		if isinstance(match,tuple):
			method,field=match[0],match[1]
		else:
			method=match
		results.append({'类型':f'$_{method}','参数':field})
	return results

def find_php_superglobals_inlist(php_codes,thepattern=''):#对多行php代码进行超全局变量扫描
	result=[]
	for php_code in php_codes:
		result+=find_php_superglobals(php_code,thepattern)
	return result

def find_php_includes(php_code):#寻找php代码中的包含语句
	pattern=r'''(include|require|include_once|require_once)\s*(?:\(\s*)?(?:(['"])([^'"\s)]+)\2|([^;)]+))(?:\))?\s*;?'''
	matches=re.finditer(pattern,php_code,re.VERBOSE)
	results=[]
	for match in matches:
		include_type=match.group(1)#检查是简单字符串还是复杂表达式
		if match.group(3):file_path,is_dynamic=match.group(3),False#简单字符串
		else:file_path,is_dynamic=match.group(4).strip(),True#复杂表达式
		results.append({'类型':include_type,'文件名':file_path,'是否动态':is_dynamic})
	return results

#================= 通用函数调用解析(支持嵌套括号) =================
def _split_args(s):#按顶层逗号分割函数实参,支持嵌套括号与引号
	args,chunk,level,quote=[],"",0,None
	for c in s+",":#添加结尾逗号确保最后参数被处理
		if quote and c=='\\':chunk+=c;continue
		if not quote and c in'"\'\'':quote=c
		elif c==quote:quote=None
		if not quote and c in'()':level+=1 if c=='('else-1
		if not quote and c==',' and level==0:
			args.append(chunk.strip());chunk="";continue
		chunk+=c
	return args


def _mask_strings_comments(php_code):
#返回与 php_code 等长的掩码串: 字符串字面量内容/注释内容替换为空格,
#但保留引号与注释定界符等边界字符。用于在其上做函数调用定位——
#使 '"exec(this...)"' 这类字符串/注释里出现的危险字眼不会被误判为真实调用(e01 类误报)。
#注意: 覆盖 单引号/双引号/反引号字符串、# // /* */ 注释; heredoc 等极端形式不处理。
	out=list(php_code)
	n=len(php_code)
	i=0
	def maskrange(a,b):
		for k in range(a,min(b,n)):
			out[k]=' '
	while i<n:
		c=php_code[i]
		## 行注释
		if c=='#':
			j=i
			while j<n and php_code[j]!='\n': j+=1
			maskrange(i,j); i=j; continue
		#// 行注释
		if php_code[i:i+2]=='//':
			j=i
			while j<n and php_code[j]!='\n': j+=1
			maskrange(i,j); i=j; continue
		#/* 块注释(保留定界符两侧位置为边界)
		if php_code[i:i+2]=='/*':
			j=i+2
			while j<n-1 and php_code[j:j+2]!='*/': j+=1
			maskrange(i, j+2 if j+2<=n and php_code[j:j+2]=='*/' else n)
			i=(j+2 if php_code[j:j+2]=='*/' else n); continue
		#字符串: 保留首尾引号, 遮蔽内容
		if c in ("'",'"','`'):
			quote=c
			maskrange(i,i+1)  #开头也掩掉(函数名前不应出现在引号后)
			i+=1
			while i<n:
				if php_code[i]=='\\':
					maskrange(i,i+2); i+=2; continue
				if php_code[i]==quote:
					maskrange(i,i+1); i+=1; break
				maskrange(i,i+1); i+=1
			continue
		i+=1
	return ''.join(out)


def _call_spans(php_code,funcnames):#定位 funcname(...) 的调用区间(支持嵌套括号),返回 [(start,end)]
	#先在“字符串/注释遮蔽后的等长掩码串”上匹配, 避免字符串/注释内文本被误判为函数调用
	masked=_mask_strings_comments(php_code)
	pattern=r'\b(?:'+'|'.join(re.escape(f) for f in funcnames)+r')\s*\('
	spans=[]
	for m in re.finditer(pattern,masked):
		i=m.end()-1#指向 '('
		depth=0
		for j in range(i,len(php_code)):
			c=php_code[j]
			if c=='(':depth+=1
			elif c==')':
				depth-=1
				if depth==0:
					spans.append((m.start(),j+1))
					break
	return spans

def find_php_function_calls(php_code,funcnames):#在 php_code 中查找 funcnames 内任意函数的调用，返回 [{函数名,参数}]
	results=[]
	for start,end in _call_spans(php_code,funcnames):
		inner=php_code[start:end]
		fm=re.match(r'\s*([A-Za-z_][\w\\]*)\s*\(',inner)
		fname=fm.group(1) if fm else inner[:inner.find('(')]
		args_text=inner[inner.find('(')+1:inner.rfind(')')]#括号内全部内容
		results.append({'函数名':fname,'参数':_split_args(args_text)})
	return results
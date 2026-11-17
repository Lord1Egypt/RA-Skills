#-*- coding: utf-8 -*-
#js_common.py —— 各检测模块共用的 JavaScript 静态分析工具函数(纯正则,无 node 依赖)。
#供四大检测模块及主程序 jsdect.py 共用。拆分为独立文件便于维护。
import re


def find_js_variables(line):#寻找js代码中提及的所有变量名
	#JS 变量: 常规标识符(字母/下划线/$ 开头, 后接字母数字_$)
	return re.findall(r'\b[A-Za-z_$][\w$]*\b', line)


def find_js_variable_assignment(js_code,variable_name):#寻找指定一个变量赋值的行为
	#匹配 var/let/const 声明或直接赋值: [var ]name = ...; 或 name = ...
	pattern=rf'\b(?:var|let|const)?\s*{re.escape(variable_name)}\s*=\s*[^;]+;'
	return re.findall(pattern,js_code)


def find_js_variable_assignment_inlist(js_codes,variable_names):#寻找单个js代码字符串中对多个变量的赋值行为
	result=[]
	for variable_name in variable_names:
		result+=find_js_variable_assignment(js_codes,variable_name)
	return result


def find_js_variable_assignment_incodelist(js_code_list,variable_names):#寻找多行代码中对多个变量的赋值行为
	result=[]
	for line in js_code_list:
		r=find_js_variable_assignment_inlist(line,variable_names)
		result+=r
	return result


#JS 外部可控输入源(相当于 php 的超全局变量):
#  浏览器: location/location.href/window.location/document.URL/URLSearchParams/
#          localStorage/sessionStorage/sessionStorage/postMessage event.data
#  Node  : process.env/process.argv
_EXTERNAL_SRC_RE = re.compile(
	r'(?:window\.)?location(?:\.[A-Za-z]+)?|'
	r'document\.URL|URLSearchParams|'
	r'(?:window\.)?localStorage|(?:window\.)?sessionStorage|'
	r'(?:event|e)\.data|postMessage|'
	r'process\.env|process\.argv', re.I)


def find_external_input(js_code):#扫描js代码中的外部可控输入源
	return _EXTERNAL_SRC_RE.findall(js_code)


def find_external_input_inlist(js_codes):#多行js代码的外部输入源扫描
	result=[]
	for code in js_codes:
		result+=find_external_input(code)
	return result


def find_js_includes(js_code):#寻找js代码中的模块引入语句
	#在"只遮蔽注释"的掩码串上匹配:注释里的 import/require 不算引入,
	#但字符串必须原样保留 —— 模块名本身就是字符串字面量。
	code=_mask_comments(js_code)
	#分别匹配三种形态, 每组内部只保留一个模块名捕获组
	results=[]
	#1) import ... from 'x'(含 import fs from 'x' / import {a} from 'x')
	for m in re.finditer(r"\bimport\s+(?:[^'\"]*?\s+from\s+)?(['\"])([^'\"]+)\1",code):
		results.append({'类型':'import','文件名':m.group(2),'是否动态':False})
	#2) require('x')
	for m in re.finditer(r"\brequire\s*\(\s*(['\"])([^'\"]+)\1",code):
		results.append({'类型':'require','文件名':m.group(2),'是否动态':False})
	#3) import('x') 动态导入
	for m in re.finditer(r"\bimport\s*\(\s*(['\"])([^'\"]+)\1",code):
		results.append({'类型':'import动态','文件名':m.group(2),'是否动态':True})
	return results


#================= 词法遮蔽层(注释 / 字符串 / 正则字面量) =================
#对称 php_common._mask_strings_comments:生成与源码等长的掩码串,把"注释/字符串/
#正则字面量"替换为空格,再在其上做函数调用定位 —— 使 '// eval(x)'、'"exec(...)"'
#这类只存在于注释或字符串里的危险字眼不被误判为真实调用。
#
#两个入口的区别:
#	_mask_comments(js_code)			—— 只遮蔽注释。供 find_js_includes 使用:
#		模块名本身就是字符串字面量(require('fs')),若连字符串一起遮蔽就匹配不到模块名。
#	_mask_strings_comments(js_code)	—— 遮蔽注释 + 字符串 + 正则。供 _call_spans 使用。
#
#覆盖: #! shebang / <!-- --> HTML 注释 / // 行注释 / /* */ 块注释 /
#		单双引号字符串 / 模板串(保留 ${} 插值 —— 插值内部是真实代码) / 正则字面量。

#这些关键字后紧跟的 '/' 是正则字面量起始,而非除号
_REGEX_PREV_KEYWORDS=('return','typeof','instanceof','in','of','new','delete','void',
					  'throw','case','do','else','yield','await')
#前一个有效字符是这些时,'/' 必为除号(左侧已是完整操作数)
_DIV_PREV_CHARS=set(')]}.')
_WORD_TAIL_RE=re.compile(r'([A-Za-z_$][\w$]*)\s*$')


def _is_regex_start(code,i):
#判定 code[i] 处的 '/' 是正则字面量起始(True)还是除号(False)。
#依据紧邻的前一个有效字符/关键字判定。无法判定时按除号处理 ——
#后果只是少遮蔽一段文本,不会漏掉真实调用(漏报代价比误报代价高)。
	head=code[:i]
	stripped=head.rstrip()
	if not stripped:
		return True#语句/文件起始
	prev=stripped[-1]
	if prev.isalnum() or prev in'_$'or prev in _DIV_PREV_CHARS:
		return False
	m=_WORD_TAIL_RE.search(head)
	if m and m.group(1)in _REGEX_PREV_KEYWORDS:
		return True
	return prev in'(,=:[!&|?{};+-*%~^<>'


def _mask_lexical(js_code,mask_strings):
#通用词法扫描,返回与 js_code 等长的掩码串。
#mask_strings=True  → 注释 + 字符串 + 正则字面量 全部替换为空格;
#mask_strings=False → 只替换注释,字符串/正则整体跳过(供需要读取字符串内容的场景)。
#模板串的 ${...} 插值内部始终保留 —— 那是真实代码,不是字面文本。
	out=list(js_code)
	n=len(js_code)

	def mask(a,b):#把 [a,b) 区间替换为空格
		for k in range(max(a,0),min(b,n)):
			out[k]=' '

	i=0
	while i<n:
		c=js_code[i]
		##! shebang(仅文件首行)
		if i==0 and js_code.startswith('#!',0):
			j=js_code.find('\n',i); j=n if j<0 else j
			mask(i,j); i=j; continue
		#<!-- HTML 注释(语义等价 // ,作用到行尾)
		if js_code.startswith('<!--',i):
			j=js_code.find('\n',i); j=n if j<0 else j
			mask(i,j); i=j; continue
		#--> HTML 注释:仅当行内其前只有空白时才成立(标准 HTMLCloseComment)
		if js_code.startswith('-->',i) and not js_code[:i].lstrip():
			j=js_code.find('\n',i); j=n if j<0 else j
			mask(i,j); i=j; continue
		#// 行注释
		if js_code.startswith('//',i):
			j=js_code.find('\n',i); j=n if j<0 else j
			mask(i,j); i=j; continue
		#/* */ 块注释
		if js_code.startswith('/*',i):
			j=js_code.find('*/',i+2)
			end=n if j<0 else j+2
			mask(i,end); i=end; continue
		#字符串 / 模板串
		if c in("'",'"','`'):
			quote=c
			seg=i#当前待遮蔽段起点
			pieces=[]#需要遮蔽的若干段(模板串被插值切成多段)
			i+=1
			while i<n:
				ch=js_code[i]
				if ch=='\\':
					i+=2; continue
				#模板串插值 ${...}:内部是真实代码,不遮蔽
				if quote=='`'and js_code.startswith('${',i):
					pieces.append((seg,i))
					i+=2
					depth=1
					while i<n and depth>0:
						cc=js_code[i]
						if cc=='{':depth+=1
						elif cc=='}':
							depth-=1
							if depth==0:break
						elif cc in("'",'"','`'):
							#跳过插值内嵌套的字符串(保持括号计数的正确性)
							q2=cc
							i+=1
							while i<n:
								if js_code[i]=='\\':i+=2; continue
								if js_code[i]==q2:i+=1; break
								i+=1
							continue
						i+=1
					i+=1#跳过 '}'
					seg=i
					continue
				if ch==quote:
					i+=1
					pieces.append((seg,i))
					break
				i+=1
			else:
				pieces.append((seg,i))#未闭合,遮蔽到末尾
			if mask_strings:
				for a,b in pieces:mask(a,b)
			continue
		#正则字面量 /.../flags
		if c=='/'and _is_regex_start(js_code,i):
			j=i+1
			in_class=False
			closed=False
			while j<n:
				ch=js_code[j]
				if ch=='\\':j+=2; continue
				if ch=='\n':break
				if in_class:
					if ch==']':in_class=False
				elif ch=='[':in_class=True
				elif ch=='/':
					closed=True; j+=1; break
				j+=1
			if closed:
				while j<n and js_code[j].isalpha():j+=1#flags
				if mask_strings:mask(i,j)
				i=j; continue
		i+=1
	return ''.join(out)


def _mask_comments(js_code):#只遮蔽注释,保留字符串/正则原文
	return _mask_lexical(js_code,False)


def _mask_strings_comments(js_code):#遮蔽注释 + 字符串 + 正则字面量
	return _mask_lexical(js_code,True)


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


def _call_spans(js_code,names):#定位 name(...) 的调用区间(支持嵌套括号),返回 [(start,end)]
	#在"注释/字符串/正则已遮蔽"的等长掩码串上做匹配与括号配平:
	#	1) 注释或字符串里的危险字眼不会被误判为真实调用;
	#	2) 括号配平同样在掩码串上做 —— 字符串/注释里的括号已变成空格,
	#	   不再污染深度计数(比直接在原文上配平更准)。
	masked=_mask_strings_comments(js_code)
	pattern=r'\b(?:'+'|'.join(re.escape(n) for n in names)+r')\s*\('
	spans=[]
	for m in re.finditer(pattern,masked):
		i=m.end()-1#指向 '('
		depth=0
		for j in range(i,len(masked)):
			c=masked[j]
			if c=='(':depth+=1
			elif c==')':
				depth-=1
				if depth==0:
					spans.append((m.start(),j+1))
					break
	return spans


def find_js_function_calls(js_code,names):
#在 js_code 中查找 names 内任意函数的调用,返回 [{函数名, 参数}]。
#通过括号深度定位调用边界,支持嵌套括号/函数作实参;参数按顶层逗号拆为列表。
	results=[]
	for start,end in _call_spans(js_code,names):
		inner=js_code[start:end]
		fm=re.match(r'\s*([A-Za-z_$][\w$.]*)\s*\(',inner)
		fname=fm.group(1) if fm else inner[:inner.find('(')]
		args_text=inner[inner.find('(')+1:inner.rfind(')')]#括号内全部内容
		results.append({'函数名':fname,'参数':_split_args(args_text)})
	return results

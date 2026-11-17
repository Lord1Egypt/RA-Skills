#phpdect.py —— PHP 恶意代码检测器(主程序/调度器)。
#从单一文件重构为「四大独立检测模块 + 主调度」结构,便于后续维护:
#-php_common.py		 :公共工具函数(变量/赋值/超全局/include)
#-threat_func_dect.py :威胁类别① 恶意函数执行
#-dynamic_var_dect.py :威胁类别② 威胁性动态变量
#-trait_dect.py		 :威胁类别③ 特征码威胁(多编码)
#-file_write_dect.py	:威胁类别④ 自我复制/文件写入
#-detect_rules.py		:规则库(威胁函数/多编码特征码)
#本文件仅负责:
#1.逐行读取文件,按行号把当前行 + 历史代码交给四个模块扫描;
#2.收集各模块返回的威胁条目,组装为统一 JSON 文档;
#3.提供递归扫描(静态 include)入口 scan_to_json 与命令行入口。
#四大威胁类别对应的 JSON 键:
#"恶意函数执行" / "威胁性动态变量" / "特征码威胁" / "自我复制/文件写入"
import os,sys,json
from filecontent_get import readfile_bintoutf8_to_list
from detect_rules import threatening_funcs,MULTI_ENC_TRAITS

from php_common import find_php_includes
from threat_func_dect import scan_threat_funcs
from dynamic_var_dect import scan_dynamic_vars
from trait_dect import scan_traits
from file_write_dect import scan_file_writes

#----AST 归一化层(可选依赖) ----
#php_ast_normalize 提供 normalize_source():把源码翻译成更易被正则/逻辑引擎识别的等效代码。
#tree_sitter 不可用时置 None,后续 AST 研判块自动跳过,不破坏原有检测。
try:
	from php_ast_normalize import normalize_source as _ast_normalize
	from php_ast_normalize import normalize_source_with_loc as _ast_normalize_with_loc
	_AST_AVAILABLE=True
except Exception:
	_ast_normalize=None
	_ast_normalize_with_loc=None
	_AST_AVAILABLE=False

#统一的四大威胁分类(JSON键)
THREAT_KEYS=["恶意函数执行","威胁性动态变量","特征码威胁","自我复制/文件写入"]

def _get_ast_normalize_with_loc(file_context):
#返回(归一化文本,定位列表)。定位列表每项 {文本,行,行止,偏移起,偏移止}。
	if not _AST_AVAILABLE or _ast_normalize_with_loc is None:
		return'',[]
	return _ast_normalize_with_loc(file_context)

def _ast_augment(raw_bytes,threats):
#对整文件做 AST 归一化,再对归一化等效代码跑现有研判(威胁函数/逻辑规则),把
#AST 揭穿的新威胁(动态函数名/污点链/拼接还原等)并入对应类别,并附原文定位(行/字节偏移)。
#raw_bytes:原始文件字节(保证 tree-sitter 行号/偏移精确对应原文)。
	if not _AST_AVAILABLE:
		return
	try:
		ast_text,locs=_get_ast_normalize_with_loc(raw_bytes)
	except Exception:
		return	#AST 解析失败 → 回退,用原始文件上下文已做的研判
	if not ast_text or not ast_text.strip():
		return
	#按语句切分:归一化文本行 与 locs 一一对应(行索引对齐)
	lines=[ln for ln in ast_text.split('\n') if ln]	 #非空行
	#若 locs 数 != 行数(某些行被 filter),用行号对应; 这里按索引对齐(两者同序产生)
	#1) 威胁函数:整段归一化文本检测(保留污点溯源能力),定位按函数名反查归一化语句
	try:
		from threat_func_dect import scan_threat_funcs
		_exist=set(x.get('函数名') for x in threats['恶意函数执行'])
		_th=scan_threat_funcs(ast_text,[ast_text],0,threatening_funcs)
		for t in _th:
			if t['函数名'] in _exist:
				continue
			t['AST归一化']=True
			#反查该函数名首次出现的归一化语句的原文定位
			_loc={}
			for _i,line in enumerate(lines):
				if t['函数名'] in line:
					_lc=locs[_i] if _i < len(locs) else None
					if _lc:
						_loc={'AST原文行':_lc['行'],'AST原文行止':_lc['行止'],
									'AST原文偏移':[_lc['偏移起'],_lc['偏移止']]}
					break
			t.update(_loc)
			threats['恶意函数执行'].append(t)
			_exist.add(t['函数名'])
	except Exception:
		pass
	#对归一化等效代码跑逻辑规则(污点链摊平后逻辑引擎可命中)
	try:
		from trait_dect import scan_logical_rules
		_lh=scan_logical_rules(ast_text)
		_exist=set((x.get('规则'),) for x in threats['特征码威胁'] if x.get('规则'))
		#逻辑规则 → 定位:在归一化语句中找含该规则任一命中关键词的行
		for lh in _lh:
			if (lh['规则'],) in _exist:
				continue
			lh['AST归一化']=True
			#定位:命中的字符串变量值(关键词)在哪些归一化语句里,取第一处原文位置
			kw=lh.get('命中变量') or []
			loc=None
			#从 LOGIC_RULES 取该规则的条件字符串,反查关键词
			if kw:
				try:
					import detect_rules
					_r=next((r for r in detect_rules.LOGIC_RULES if r.get('id')==lh['规则']),None)
					if _r:
						strmap=_r.get('条件字符串',{})
						keywords=[strmap[v] for v in kw if v in strmap]
						for _i,line in enumerate(lines):
							if any(k and k in line for k in keywords):
								loc=locs[_i] if _i < len(locs) else None
								if loc:
									lh['AST原文行']=loc['行']
									lh['AST原文行止']=loc['行止']
									lh['AST原文偏移']=[loc['偏移起'],loc['偏移止']]
								break
				except Exception:
					pass
			threats['特征码威胁'].append(lh)
			_exist.add((lh['规则'],))
	except Exception:
		pass

def phpfile_threatening_dect(file_path):#威胁扫描逻辑的总函数
#扫描单个 PHP 文件,返回完整JSON兼容文档(dict)
#返回结构(每个威胁条目均为统一schema的JSON对象):
#{
#"文件":<str>,
#"是否有威胁":<bool>,
#"包含文件":[<str>,...],
#"威胁":{
#"恶意函数执行":	[{条目},...],
#"威胁性动态变量":	[{条目},...],
#"特征码威胁":		[{条目},...],
#"自我复制/文件写入":[{条目},...]
#}
#}
	threats={key:[] for key in THREAT_KEYS}

	file_content_lines=readfile_bintoutf8_to_list(file_path)#readfile_code_to_list(file_path)
	file_content_lines.append("\n")#获取每一行内容并形成列表，结尾加一个空行
	#整个文件的拼接文本(供规则4等需要文件级上下文的判定使用)
	file_context='\n'.join(file_content_lines)

	#收集静态包含(供 scan_to_json 递归)
	static_includes=[]

	for fileline_num in range(1,len(file_content_lines)):
		file_content_line=file_content_lines[fileline_num-1]#设置行号并获取对应行的内容
		lines_upto=file_content_lines[:fileline_num+1]#截至当前行(含)的历史代码,供参数/变量溯源

		#----1.恶意函数执行 ----
		threats["恶意函数执行"] += scan_threat_funcs(
			file_content_line,lines_upto,fileline_num,threatening_funcs)

		#----2.威胁性动态变量 ----
		threats["威胁性动态变量"] += scan_dynamic_vars(
			file_content_line,lines_upto,fileline_num)

		#----2b.外部可控动态函数调用(超全局下标作函数名) ----
		try:
			from dynamic_var_dect import scan_dynamic_func_calls
			threats["威胁性动态变量"] += scan_dynamic_func_calls(
				file_content_line,fileline_num)
		except Exception:
			pass

		#----3.静态 include 收集 ----
		phpincude=find_php_includes(file_content_line)#寻找当前php文件包含了哪些php文件
		if phpincude!=[]:
			for i in phpincude:
				if i['是否动态']==False:#对于静态包含可以直接得知被包含文件路径,交给scan_to_json做递归
					static_includes.append(i['文件名'])

		#----4.特征码威胁(多编码) ----
		threats["特征码威胁"] += scan_traits(
			file_content_line,fileline_num,MULTI_ENC_TRAITS)

		#----5.自我复制/文件写入 ----
		threats["自我复制/文件写入"] += scan_file_writes(
			file_content_line,lines_upto,fileline_num,file_context,
			threatening_funcs,MULTI_ENC_TRAITS)

	#----6.逻辑规则组合判断(整文件,来自 categories.json 的"逻辑规则"键) ----
	#自研逻辑引擎(模仿 yara 的 and/or/not),命中并入"特征码威胁"类别。
	try:
		from trait_dect import scan_logical_rules
		logical_hits=scan_logical_rules(file_context)
		_exist=set((x.get('规则'),) for x in threats['特征码威胁'] if x.get('规则'))
		for lh in logical_hits:
			key=(lh['规则'],)
			if key not in _exist:
				threats['特征码威胁'].append(lh)
				_exist.add(key)
	except Exception:
		pass

	#----7.AST 归一化研判(整文件,翻译成等效代码后复用现有研判) ----
	#用原始文件字节做 AST 归一化(保证行号/偏移精确对应原文),失败则回退。
	if _AST_AVAILABLE:
		try:
			with open(file_path,'rb') as _f:
				_raw=_f.read()
			_ast_augment(_raw,threats)
		except Exception:
			pass

	#组装完整 JSON 文档
	result={
		"文件":file_path,
		"是否有威胁":any(threats[k] for k in THREAT_KEYS),
		"包含文件":static_includes,
		"威胁":threats,
	}
	return result

def scan_to_json(start_file_path='phpdest.php',recursive=True):
#扫描一个/多个PHP文件(可递归收集静态include),返回JSON兼容的dict。
#返回结构:
#{
#"文件":str,"是否有威胁":bool,
#"包含文件":[str,...],
#"威胁":{
#"恶意函数执行":[...],
#"威胁性动态变量":[...],
#"特征码威胁":[...],
#"自我复制/文件写入":[...]
#}
#}
	if isinstance(start_file_path,str):filepath_list=[start_file_path]
	else:filepath_list=list(start_file_path)

	scanned=set()
	result_files=[]

	def scan_one(the_file_path,is_entry=False):
		if the_file_path in scanned and not is_entry:
			return None
		#入口文件即使已被扫描过也允许重复扫描(避免入口被去重丢弃)
		is_dup=the_file_path in scanned
		scanned.add(the_file_path)

		try:
			raw=phpfile_threatening_dect(the_file_path)
		except Exception as e:
			raw={
				"文件":the_file_path,
				"是否有威胁":False,
				"包含文件":[],
				"威胁":{key:[] for key in THREAT_KEYS},
			}
			last_err=str(e)
		else:
			last_err=None

		entry=raw
		if last_err is not None:
			entry["错误"]=last_err

		#入口在前:先 append 当前文件,再递归子文件
		result_files.append(entry)

		if recursive and not is_dup:
			for inc in raw["包含文件"]:
				#解析相对路径:优先同目录,避免路径穿越
				inc_path=os.path.join(os.path.dirname(the_file_path) or '.',inc)
				inc_path=os.path.normpath(inc_path)
				if os.path.isfile(inc_path):
					scan_one(inc_path)

		return entry

	for fp in filepath_list:
		scan_one(fp,is_entry=True)

	#入口文件在前,递归子文件在后;始终返回列表
	return result_files

if __name__=='__main__':
	#支持:python phpdect.py [文件1 [文件2 ...]]
	args=sys.argv[1:]
	if not args:args=['phpdest.php']
	out=scan_to_json(args)
	print(json.dumps(out,ensure_ascii=False,indent=2))#统一中文字符不转义,缩进2,保证可读性

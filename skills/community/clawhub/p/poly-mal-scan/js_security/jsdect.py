#-*- coding: utf-8 -*-
#jsdect.py —— JS/Node.js 恶意代码检测器(主程序/调度器)。
#分层结构(模仿 php_security 的 php 检测器):
#- js_common.py            : 公共工具函数(变量/赋值/外部输入源/函数调用解析)
#- js_detect_rules.py      : 规则库(威胁函数/多编码特征码/直接特征码)
#- js_threat_func_dect.py  : 威胁类别① 恶意函数/API 执行
#- js_dynamic_code_dect.py : 威胁类别② 动态代码执行(危险sink×外部输入)
#- js_trait_dect.py        : 威胁类别③ 特征码威胁(多编码)
#- js_file_write_dect.py   : 威胁类别④ 自我复制/文件写入
#- jscontent_get.py        : 文件读取层
#本文件仅负责:
#1. 逐行读取文件,按行号把当前行 + 历史代码交给各模块扫描;
#2. 收集各模块返回的威胁条目,组装为统一 JSON 文档;
#3. 提供命令行入口。
#四大威胁类别对应的 JSON 键:
#"恶意函数执行" / "动态代码执行" / "特征码威胁" / "自我复制/文件写入"
import os
from jscontent_get import readfile_bintoutf8_to_list
from js_detect_rules import threatening_funcs, MULTI_ENC_TRAITS

from js_common import find_js_includes, _mask_comments
from js_threat_func_dect import scan_threat_funcs
from js_dynamic_code_dect import scan_dynamic_code
from js_trait_dect import scan_traits
from js_file_write_dect import scan_file_writes

#---- AST 归一化层(可选依赖, 对称于 php phpdect.py) ----
try:
	from js_ast_normalize import normalize_source as _ast_normalize
	from js_ast_normalize import normalize_source_with_loc as _ast_normalize_with_loc
	_AST_AVAILABLE=True
except Exception:
	_ast_normalize=None
	_ast_normalize_with_loc=None
	_AST_AVAILABLE=False


def _get_ast_normalize_with_loc(raw_bytes):
#返回 (归一化文本, 定位列表)。定位每项 {文本,行,行止,偏移起,偏移止}。
	if not _AST_AVAILABLE or _ast_normalize_with_loc is None:
		return '',[]
	return _ast_normalize_with_loc(raw_bytes)


def _ast_augment(raw_bytes,threats):
#对整文件做 JS AST 归一化, 再对归一化等效代码跑现有研判(威胁函数/动态代码/逻辑规则), 把
#AST 揭穿的新威胁(动态函数名/污点链/拼接还原等)并入对应类别, 并附原文定位(行/字节偏移)。
#raw_bytes: 原始文件字节(保证 tree-sitter 行号/偏移精确对应原文)。失败则回退。
	if not _AST_AVAILABLE:
		return
	try:
		ast_text,locs=_get_ast_normalize_with_loc(raw_bytes)
	except Exception:
		return
	if not ast_text or not ast_text.strip():
		return
	lines=ast_text.split('\n')#与 locs 按行严格一一对应(已由 normalize_source_with_loc 展开对齐)

	#定位辅助: 按命中关键词在归一化语句中找原文位置
	def _loc_of_keywords(keywords):
		for _i,line in enumerate(lines):
			if any(k and k in line for k in keywords):
				loc=locs[_i] if _i < len(locs) else None
				if loc:
					return {'AST原文行':loc['行'],'AST原文行止':loc['行止'],
					        'AST原文偏移':[loc['偏移起'],loc['偏移止']]}
		return {}

	#威胁函数: 整段归一化文本检测(保留溯源), 定位按函数名反查
	try:
		from js_threat_func_dect import scan_threat_funcs
		_skip=set(x.get('函数名') for x in threats['恶意函数执行'])
		_th=scan_threat_funcs(ast_text,[ast_text],0,threatening_funcs)
		for t in _th:
			if t['函数名'] in _skip:
				continue
			t['AST归一化']=True
			t.update(_loc_of_keywords([t['函数名']]))
			threats['恶意函数执行'].append(t)
			_skip.add(t['函数名'])
	except Exception:
		pass
	#动态代码执行(危险sink×外部输入): 整段检测(保留溯源), 定位按 sink 反查
	try:
		from js_dynamic_code_dect import scan_dynamic_code
		_skip=set((x.get('sink'),) for x in threats['动态代码执行'])
		_dh=scan_dynamic_code(ast_text,[ast_text],0)
		for h in _dh:
			if (h['sink'],) in _skip:
				continue
			h['AST归一化']=True
			h.update(_loc_of_keywords([h['sink']]))
			threats['动态代码执行'].append(h)
			_skip.add((h['sink'],))
	except Exception:
		pass
	#逻辑规则
	try:
		from js_trait_dect import scan_logical_rules
		_lh=scan_logical_rules(ast_text)
		_exist=set((x.get('规则'),) for x in threats['特征码威胁'] if x.get('规则'))
		import js_detect_rules
		for lh in _lh:
			if (lh['规则'],) in _exist:
				continue
			lh['AST归一化']=True
			kw=lh.get('命中变量') or []
			if kw:
				try:
					_r=next((r for r in js_detect_rules.LOGIC_RULES if r.get('id')==lh['规则']),None)
					if _r:
						strmap=_r.get('条件字符串',{})
						keywords=[strmap[v] for v in kw if v in strmap]
						if keywords:
							lh.update(_loc_of_keywords(keywords))
				except Exception:
					pass
			threats['特征码威胁'].append(lh)
			_exist.add((lh['规则'],))
	except Exception:
		pass


#统一的四类威胁分类(JSON 键)
THREAT_KEYS=["恶意函数执行","动态代码执行","特征码威胁","自我复制/文件写入"]


def jsfile_threatening_dect(file_path):#威胁扫描逻辑的总函数(完全 JSON 化)
#扫描单个 JS 文件,返回完整 JSON 兼容文档(dict)。
	threats={key:[] for key in THREAT_KEYS}

	file_content_lines=readfile_bintoutf8_to_list(file_path)
	file_content_lines.append("\n")
	file_context='\n'.join(file_content_lines)

	#注释清理视图:把注释内容挖成空格,按行切分后与 file_content_lines 按索引对齐。
	#用于特征码子串匹配与逻辑规则 —— 注释里的字眼永远不参与执行,只会造成误报;
	#而混淆 payload 通常就藏在字符串里,所以字符串/模板串/正则一律原样保留。
	#整文件一次扫描(而非逐行),跨行块注释才能被正确挖掉。
	masked_lines=_mask_comments(file_context).split('\n')
	code_nc='\n'.join(masked_lines)

	modules=[]#静态 import/require 收集

	for fileline_num in range(1,len(file_content_lines)):
		line=file_content_lines[fileline_num-1]
		line_nc=(masked_lines[fileline_num-1]
				 if fileline_num-1<len(masked_lines)else line)#去注释后的当前行
		lines_upto=file_content_lines[:fileline_num+1]

		#---- 1. 恶意函数/API 执行 ----
		threats["恶意函数执行"]+=scan_threat_funcs(
			line,lines_upto,fileline_num,threatening_funcs)

		#---- 2. 动态代码执行(危险sink × 外部输入) ----
		threats["动态代码执行"]+=scan_dynamic_code(line,lines_upto,fileline_num)

		#---- 3. 静态模块引入收集(供递归扫描) ----
		for inc in find_js_includes(line):
			if not inc['是否动态']:
				modules.append(inc['文件名'])

		#---- 4. 特征码威胁(多编码) ----
		#用去注释后的行:注释里的指纹一律不算,字符串里的 payload 照常命中
		threats["特征码威胁"]+=scan_traits(line_nc,fileline_num,MULTI_ENC_TRAITS)

		#---- 5. 自我复制/文件写入 ----
		threats["自我复制/文件写入"]+=scan_file_writes(
			line,lines_upto,fileline_num,file_context,threatening_funcs,MULTI_ENC_TRAITS)

	#---- 6. 逻辑规则组合判断(整文件, 来自 js_categories.json 的"逻辑规则"键) ----
	#自研逻辑引擎(模仿 yara 的 and/or/not), 命中并入"特征码威胁"类别。
	try:
		from js_trait_dect import scan_logical_rules
		logical_hits=scan_logical_rules(code_nc)#去注释后的全文,避免注释里的字眼触发组合规则
		_exist=set((x.get('规则'),) for x in threats['特征码威胁'] if x.get('规则'))
		for lh in logical_hits:
			key=(lh['规则'],)
			if key not in _exist:
				threats['特征码威胁'].append(lh)
				_exist.add(key)
	except Exception:
		pass

	#---- 7. AST 归一化研判(整文件, 翻译成等效代码后复用现有研判) ----
	#用原始文件字节做 AST 归一化(保证行号/偏移精确对应原文), 失败则回退。
	if _AST_AVAILABLE:
		try:
			with open(file_path,'rb') as _f:
				_raw=_f.read()
			_ast_augment(_raw,threats)
		except Exception:
			pass

	result={
		"文件":file_path,
		"是否有威胁":any(threats[k] for k in THREAT_KEYS),
		"引入模块":modules,
		"威胁":threats,
	}
	return result


def scan_to_json(start_file_path='mal.js', recursive=True):
#扫描一个/多个 JS 文件,返回 JSON 兼容的 dict。
	if isinstance(start_file_path,str):filepath_list=[start_file_path]
	else:filepath_list=list(start_file_path)

	scanned=set()
	result_files=[]

	def scan_one(the_file_path, is_entry=False):
		if the_file_path in scanned and not is_entry:
			return None
		is_dup=the_file_path in scanned
		scanned.add(the_file_path)
		try:
			raw=jsfile_threatening_dect(the_file_path)
		except Exception as e:
			raw={
				"文件":the_file_path,"是否有威胁":False,"引入模块":[],
				"威胁":{key:[] for key in THREAT_KEYS},
			}
			last_err=str(e)
		else:
			last_err=None

		entry=raw
		if last_err is not None:
			entry["错误"]=last_err
		result_files.append(entry)

		if recursive and not is_dup:
			for inc in raw["引入模块"]:
				inc_path=os.path.join(os.path.dirname(the_file_path) or '.', inc)
				inc_path=os.path.normpath(inc_path)
				if os.path.isfile(inc_path):
					scan_one(inc_path)
		return entry

	for fp in filepath_list:
		scan_one(fp, is_entry=True)
	return result_files


if __name__=='__main__':
	import sys,json as _json
	args=sys.argv[1:]
	if not args:
		args=['mal.js']
	out=scan_to_json(args)
	print(_json.dumps(out,ensure_ascii=False,indent=2))

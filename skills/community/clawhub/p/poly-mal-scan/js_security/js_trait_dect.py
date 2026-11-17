# -*- coding: utf-8 -*-
"""
js_trait_dect.py —— 威胁类别③:特征码威胁 检测模块。

以多编码特征码(MULTI_ENC_TRAITS,类别×编码)对一行代码做子串匹配,
命中即标注类别与编码类型。用于识别被各类混淆编码隐藏的恶意 payload。

逻辑规则增强(2026-09-01 重构):
  在纯子串匹配之外,叠加自研逻辑判断引擎(js_logic_engine.py, 模仿 yara 的
  and/or/not 组合, 不依赖 yara 库):
    - 逻辑规则从 js_categories.json 的"逻辑规则"键读出(LOGIC_RULES);
    - 对整文件文本做组合条件求值(如 eval 且 atob / innerHTML 且 location)。
  命中逻辑规则后并入"特征码威胁"类别, 威胁级别取规则字段(缺省 4)。

对外接口:
  scan_traits(file_content_line, fileline_num, multi_enc_traits)  —— 逐行多编码子串
  scan_logical_rules(file_context, fileline_num)                  —— 整文件逻辑组合判断
"""
def js_trait_find(js_code,multi_enc_traits):#多编码形式的威胁特征扫描。遍历MULTI_ENC_TRAITS(类别×编码),子串匹配命中即记入,并标注类别与编码类型。
	result=[]
	for threat_type,enc_dict in multi_enc_traits.items():
		for enc_name,traits in enc_dict.items():
			for trait in traits:
				if trait in js_code:result.append({"特征码":trait,"威胁类型":threat_type,"编码":enc_name})
	return result
def scan_traits(file_content_line,fileline_num,multi_enc_traits):
	r=js_trait_find(file_content_line,multi_enc_traits)
	for x in r:x.update({"行数":fileline_num,"威胁类型":"特征码威胁"})
	return r
def scan_logical_rules(file_context,fileline_num=0):#对整段JS文本跑自研逻辑引擎的规则(来自LOGIC_RULES)。
	from js_logic_engine import match_logical_rules
	out=[]
	for h in match_logical_rules(file_context):
		out.append({
			"威胁类型":"特征码威胁",
			"规则":h['规则'],
			"类别":h['类别'],
			"威胁级别":h['威胁级别'],
			"描述":h['描述'],
			"命中变量":h['命中变量'],
			"行数":fileline_num,
		})
	return out

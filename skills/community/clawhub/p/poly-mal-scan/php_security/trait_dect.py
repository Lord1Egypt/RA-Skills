"""
trait_dect.py —— 威胁类别③:特征码威胁 检测模块。

以多编码特征码(MULTI_ENC_TRAITS,类别×编码)对一行代码做子串匹配,
命中即标注类别与编码类型。用于识别被各类混淆编码隐藏的恶意 payload。
对外接口:
  scan_traits(file_content_line,fileline_num,multi_enc_traits)  —— 逐行多编码子串
  scan_logical_rules(file_context,filefile_num)                  —— 整文件逻辑组合判断
"""
import re
def phpfile_threaten_base64_find(php_code,multi_enc_traits):#多编码形式的威胁特征扫描(兼容旧函数名)。遍历MULTI_ENC_TRAITS(类别×编码),子串匹配命中即记入,并标注类别与编码类型。返回JSON兼容结构(每项含特征码/威胁类型/编码)。
	result=[]
	for threat_type,enc_dict in multi_enc_traits.items():
		for enc_name,traits in enc_dict.items():
			for trait in traits:
				if trait in php_code:result.append({"特征码":trait,"威胁类型":threat_type,"编码":enc_name})
	return result
def scan_traits(file_content_line,fileline_num,multi_enc_traits):
	r=phpfile_threaten_base64_find(file_content_line,multi_enc_traits)
	for x in r:x.update({"行数":fileline_num,"威胁类型":"特征码威胁"})
	return r
def scan_logical_rules(file_context,fileline_num=0):#对整段PHP文本跑自研逻辑引擎的规则(来自LOGIC_RULES)。参数:file_context:待扫描的PHP文本(通常是整文件全文);fileline_num:起始行号标注(仅用于展示,缺省0)。返回:命中条目列表(JSON兼容);每项:{威胁类型:"特征码威胁",规则:<id>,类别:<类别>,威胁级别:<级别>,描述:<描述>,命中变量:[...],行数:<fileline_num>}。
	from logic_engine import match_logical_rules
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

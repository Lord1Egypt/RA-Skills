# -*- coding: utf-8 -*-
"""
js_detect_rules.py —— JS 恶意代码检测的规则库(可独立维护)
集中存放:
  1. jsfunc 类(威胁函数对象)
  2. threatening_funcs(威胁/漏洞 JS 函数库)   —— 从 JSON 读取
  3. 多编码形式的威胁特征码( base64 / url / hex / unicode / octal / rot13 / html )
  4. RAW_TRAITS 直接特征码库(已知恶意样本指纹,未知源码也能用) —— 从 JSON 读取

规则数据与代码解耦:
  js_threatening_funcs.json   —— 威胁函数库(name + level)
  js_raw_traits.json          —— 已知恶意样本直接特征码
  以后更新特征码库只需改 JSON,无需动 Python 代码,减小把代码改坏的风险。
"""
import os,json
import re
class jsfunc:#威胁函数类
	def __init__(self,name,threateninglevel=0):
		self.name=name#函数名/成员名(用于正则匹配,含点号表示成员方法)
		self.threateninglevel=threateninglevel#威胁等级
#===================================================================
# 规则数据 JSON 加载
# 无论从哪个目录 import,都以本文件所在目录为基准定位 JSON,
# 保证 js_threatening_funcs.json / js_raw_traits.json 始终能正确找到。
#===================================================================
_RULES_DIR=os.path.dirname(os.path.abspath(__file__))
def _load_json(name):
	path=os.path.join(_RULES_DIR,name)
	if not os.path.isfile(path):raise FileNotFoundError('规则数据文件缺失: %s'%path)
	with open(path,encoding='utf-8') as f:return json.load(f)
#---- 威胁/漏洞 JS 函数库(读自 js_threatening_funcs.json)----
# JSON 结构:[{ "name": "eval", "level": 4 }, ...]
# 加载后重建为 jsfunc 对象列表,保持与其他模块的 .name/.threateninglevel 访问兼容。
threatening_funcs=[jsfunc(item['name'],item['level'])for item in _load_json('js_threatening_funcs.json')]
#---- 直接特征码库(读自 js_raw_traits.json)----
# JSON 结构:RAW_TRAITS[类别][编码] = [特征码, ...]
# 特征码是“该编码下的最终形态”,直接参与子串比对,不再二次编码。
# 以后遇到新恶意内容,直接往 js_raw_traits.json 对应 类别x编码 列表里加指纹即可。
RAW_TRAITS=_load_json('js_raw_traits.json')
# ----------- 多编码形式的威胁特征码(全局变量,便于扩展)-----------
# 支持的编码形式:
#   1. base64        —— 常见恶意payload编码
#   2. url 编码      —— %XX
#   3. hex           —— \\x73 转义
#   4. unicode       —— \\u0073 \\u73
#   5. octal         —— \\163
#   6. rot13         —— 简单字母混淆
#   7. html 实体     —— &#115;
# 匹配是子串匹配,特征码是“原始字符串在某种编码下的形态”。
def _b64(s):#base64编码(不带=填充,但保留原始=号处理:统一去掉尾部=)
	import base64
	return base64.b64encode(s.encode()).decode().rstrip('=')
def _urlenc(s):#URL百分号编码
	return ''.join('%%%02x'%b for b in s.encode())
def _hexescape(s):#hex转义
	return ''.join('\\x%02x'%b for b in s.encode())
def _unicode(s):#unicode转义(\\uXXXX全大写十六进制)
	return ''.join('\\u%04X'%b for b in s.encode())
def _octalescape(s):#八进制转义
	return ''.join('\\%03o'%b for b in s.encode())
def _rot13(s):#ROT13变换
	import codecs
	return codecs.encode(s,'rot_13')
def _htmlent(s):#HTML实体(十进制)
	return ''.join('&#%d;'%b for b in s.encode())
# 编码器注册表
# 说明: plain 为“明文原样保留”通道 —— 用于让真实样本提取的
#     高确定性明文指纹(如 eval(/`与超全局`)直接以明文子串参与匹配,命中即判死。
#     plain 只从 RAW_TRAITS 取完整指纹,不对 CATEGORIES 词条做明文子串(避免误报)。
ENCODERS={
	'plain':lambda s:s,
	'base64':_b64,
	'url':_urlenc,
	'hex':_hexescape,
	'unicode':_unicode,
	'octal':_octalescape,
	'rot13':_rot13,
	'html':_htmlent,
}
#===================================================================
# 以下为“生成逻辑”:CATEGORIES(词条原料)+ ENCODERS(编码器)
# 推导出 MULTI_ENC_TRAITS 多编码特征码,并与 RAW_TRAITS(JSON 直读)合并。
# 若需更改推导来源的词条,改 js_categories.json 即可,无需动本文件。
#===================================================================
# ---- 各威胁类别的原始高危字符串(原料,读自 js_categories.json)----
# JSON 结构:CATEGORIES = { 类别: [词条, ...], ... }
CATEGORIES=_load_json('js_categories.json')
# 从 CATEGORIES 中分离"逻辑规则"特殊键(承载带逻辑联结词的规则),
# 避免被当作普通词条类别处理。
_LOGIC_KEY='逻辑规则'
LOGIC_RULES=CATEGORIES.pop(_LOGIC_KEY,[])
# ===================================================================
# 以下 RAW_TRAITS 已从 js_raw_traits.json 加载(见文件头部 _load_json)。
# 直接特征码(RAW_TRAITS): 已知恶意样本指纹的“明晃晃特征码本身”。
# 与 CATEGORIES 的区别:
#   CATEGORIES —— 从“已知词条”推导特征码(把 'eval' 编码成 base64/url/hex...),
#                 前提是恶意代码背后的源码/词条已知。
#   RAW_TRAITS —— 直接写入特征码指纹本身,不从任何词条推导。
#                 适用于“恶意内容未知/无法逆向”的情况:
#                 拿到样本后直接提取特征码贴进来,即可更新规则库实时检测。
# 格式: RAW_TRAITS[类别][编码] = [特征码1, 特征码2, ...]
#   特征码 —— 必须是“该编码下的最终形态”,直接参与子串比对,不再二次编码。
# ===================================================================
# 特征码最小长度门槛(防止高熵数据误报)
MIN_TRAIT_LEN=4
# ===================================================================
# 生成最终特征码数据结构:
#   MULTI_ENC_TRAITS={ 类别: { 编码名称: [特征码,...],... },... }
# 由两类来源合并去重:
#   1. CATEGORIES 推导(已知词条 + 各编码器);
#   2. RAW_TRAITS 直接特征码(已知恶意样本指纹, 未知源码也能用)。
# ===================================================================
MULTI_ENC_TRAITS={}
for _cat,_words in CATEGORIES.items():
	MULTI_ENC_TRAITS[_cat]={}
	for _name,_fn in ENCODERS.items():
		if _name=='plain':
			# plain(明文)只保留 RAW_TRAITS 的完整高确定性指纹,
			# 不对 CATEGORIES 纯词条做明文子串 —— 避免 'eval'/'fetch' 等
			# 常见词在正常代码里误报。明文函数检测本由 js_threat_func_dect 覆盖。
			_src=set(RAW_TRAITS.get(_cat,{}).get('plain',[]))
		else:
			_encoded={_fn(w) for w in _words}
			_src=_encoded|set(RAW_TRAITS.get(_cat,{}).get(_name,[]))
		MULTI_ENC_TRAITS[_cat][_name]=sorted(t for t in _src if len(t)>=MIN_TRAIT_LEN)

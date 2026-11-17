"""
detect_rules.py——PHP恶意代码检测的【规则库加载工具】

所有规则数据（威胁函数/原料词条/直接特征码）均从JSON文件读取。

数据来源（均与本文件同目录的JSON）：
	threatening_funcs.json——威胁函数库（name+level）
	categories.json			——各威胁类别的原始高危字符串原料（类别→词条列表）
	raw_traits.json			——已知恶意样本直接特征码（类别→编码→特征码列表）

对外输出：
	threatening_funcs		——phpfunc对象列表（threat_func_dect/file_write_dect使用）
	CATEGORIES			——原料词条dict（供MULTI_ENC_TRAITS推导编码特征码）
	RAW_TRAITS			——直接特征码dict（供MULTI_ENC_TRAITS合并）
	MULTI_ENC_TRAITS	——最终多编码特征码（trait_dect使用）
	ENCODERS				——编码器注册表（生成逻辑）
"""
import os,json,re
import base64,codecs
class phpfunc:#php函数类
	def __init__(self,name,threateninglevel=0):
		self.name=name#函数名
		self.threateninglevel=threateninglevel#威胁等级
#===================================================================
#规则数据JSON加载
#无论从哪个目录import，都以本文件所在目录为基准定位JSON，
#保证 threatening_funcs.json/raw_traits.json 始终能正确找到。
#===================================================================
_RULES_DIR=os.path.dirname(os.path.abspath(__file__))
def _load_json(name):
	path=os.path.join(_RULES_DIR,name)
	if not os.path.isfile(path):raise FileNotFoundError('规则数据文件缺失:%s'%path)
	with open(path,encoding='utf-8') as f:return json.load(f)
#读取威胁/漏洞PHP函数库并生成函数对象，对应JSON结构：[{"name":"eval","level":4},...]
threatening_funcs=[phpfunc(item['name'],item['level'])for item in _load_json('threatening_funcs.json')]
#读取直接特征码库，这些特征码是最终形态，直接参与子串比对，不再二次编码，对应JSON结构：RAW_TRAITS[类别][编码]=[特征码,...]
RAW_TRAITS=_load_json('raw_traits.json')#以后遇到新恶意内容，直接往raw_traits.json对应 类别×编码 列表里加指纹即可。
#----------- 多编码形式的威胁特征码(全局变量,便于扩展)-----------
#黑客常用的代码混淆编码形式均在此生成特征码,用于识别被混淆隐藏的 payload。
#支持的编码形式及其示例：
#base64	——Y3N5c3RlbQ==
#url编码	——%73%79%73%74%65%6d
#hex转义	——\x73\x79\x73\x74\x65\x6d
#octal转义	——\163\171\163\164\145\155
#chr拼接	——chr(115).chr(121)...
#rot13		——flfgrz
#html实体	——&#115;&#121;...
#匹配是子串匹配,特征码是“原始字符串在某种编码下的形态”。
def _b64(s):#base64编码(不带=填充)
	return base64.b64encode(s.encode()).decode().rstrip('=')
def _urlenc(s):#URL百分号编码:每个字节->%XX(小写)
	return ''.join('%%%02x'%b for b in s.encode())
def _hexescape(s):#hex转义:\x73形式(小写)
	return ''.join('\\x%02x'%b for b in s.encode())
def _octalescape(s):#八进制转义:\163形式
	return ''.join('\\%03o'%b for b in s.encode())
def _chrjoin(s):#chr拼接:chr(115).chr(121)...
	return '.'.join('chr(%d)'%b for b in s.encode())
def _rot13(s):#ROT13变换(仅对ASCII字母有效,与PHP str_rot13一致)
	return codecs.encode(s,'rot_13')
def _htmlent(s):#HTML实体(十进制):&#115;&#121;...
	return ''.join('&#%d;'%b for b in s.encode())
#编码器注册表:名称 -> 编码函数
#说明:plain 为“明文原样保留”通道 —— 用于让真实样本提取的
#	 高确定性明文指纹(如 eval(\$_POST['p1']) 直接以明文子串参与匹配,
#	 命中即判死。plain 编码不做任何变换,原样返回。
ENCODERS={
	'plain':lambda s:s,
	'base64':_b64,
	'url':_urlenc,
	'hex':_hexescape,
	'octal':_octalescape,
	'chr':_chrjoin,
	'rot13':_rot13,
	'html':_htmlent,
}
#===================================================================
#以下为“生成逻辑”：CATEGORIES（原料词条，JSON 读取）+ ENCODERS（编码器）
#推导出 MULTI_ENC_TRAITS 多编码特征码，并与 RAW_TRAITS（JSON 直读）合并。
#若需更改推导来源的词条，改 categories.json 即可，无需动本文件。
#===================================================================
#---- 各威胁类别的原始高危字符串(原料,读自 categories.json)----
#JSON 结构：CATEGORIES={类别:[词条,...],...}
CATEGORIES=_load_json('categories.json')
# 从 CATEGORIES 中分离"逻辑规则"特殊键(承载带逻辑联结词的规则)
# JSON 结构:LOGIC_RULES=[ {id,类别,威胁级别,描述,条件,条件字符串} ,...]
# 逻辑规则键从 CATEGORIES 中剔除,避免被当作普通词条类别处理。
_LOGIC_KEY='逻辑规则'
LOGIC_RULES=CATEGORIES.pop(_LOGIC_KEY,[])
#特征码最小长度门槛。
#短特征码(如 2~3 字节的 'qy'、'ZGw'、'beq'、'pue')在 PNG/JPEG 等高熵二进制数据里会大量随机碰撞,造成严重误报。4 字节及以上时,
#随机碰撞概率约为 1/95^4 ≈ 千万分之一,单张图片里基本不会误报。
#长度不足门槛的特征码直接丢弃(它们对应的词条且本身威胁价值也很低)。
MIN_TRAIT_LEN=4
#===================================================================
#生成最终特征码数据结构:
#MULTI_ENC_TRAITS={类别:{编码名称:[特征码,...],...}}
#由两类来源合并去重:
#1.CATEGORIES 推导(已知词条 + 各编码器);
#2.RAW_TRAITS 直接特征码(已知恶意样本指纹,未知源码也能用)。
#===================================================================
MULTI_ENC_TRAITS={}
for _cat,_words in CATEGORIES.items():
	MULTI_ENC_TRAITS[_cat]={}
	for _name,_fn in ENCODERS.items():
		if _name=='plain':
			#plain(明文)通道只保留 RAW_TRAITS 的完整高确定性指纹,
			#不对 CATEGORIES 纯函数名词条做明文子串 —— 否则'exec'/'_POST'等
			#常见词会在正常代码里大量误报。明文函数检测本由 threat_func_dect 覆盖。
			_src=set(RAW_TRAITS.get(_cat,{}).get('plain',[]))
		else:
			_encoded={_fn(w) for w in _words}
			_src=_encoded|set(RAW_TRAITS.get(_cat,{}).get(_name,[]))
		MULTI_ENC_TRAITS[_cat][_name]=sorted(t for t in _src if len(t)>=MIN_TRAIT_LEN)

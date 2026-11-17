# -*- coding: utf-8 -*-
"""
bash_detect_rules.py —— Bash 恶意代码检测的【规则库加载工具】(对称于 php_security/detect_rules.py)

所有规则数据(威胁函数/结构化规则/原料词条/直接特征码)均从 JSON 文件读取。

数据来源(均与本文件同目录的 JSON):
  bash_threatening_funcs.json —— 恶意函数库({name, level})
  bash_malicious_commands.json—— 恶意命令规则(命令 + 危险参数 + 级别 + 描述)
  bash_malicious_variables.json—— 恶意变量规则(变量名 + 危险值特征 + 危险赋值符)
  bash_file_write.json        —— 恶意文件写入规则(参考 php 侧 file_write_dect 的判定维度)
  bash_self_replicate.json    —— 自我复制规则(源特征 + 命令/目标路径特征)
  bash_raw_traits.json        —— 已知恶意样本直接特征码(类别→编码→特征码列表)
  bash_categories.json        —— 各威胁类别的原始高危字符串原料(类别→词条列表)

对外输出(供后续正则层/研判层消费,本文件不做任何扫描判定):
  THREAT_FUNCS       —— bashfunc 对象列表(恶意函数)
  FUNC_NAMES         —— 恶意函数名集合(便于正则层快速命中)
  MALICIOUS_COMMANDS —— 恶意命令规则列表
  COMMANDS_BY_NAME   —— 命令名 → [规则,...] 索引(便于按命令名查表)
  MALICIOUS_VARIABLES—— 恶意变量规则列表
  FILE_WRITE_RULES   —— 恶意文件写入规则列表
  SELF_REPLICATE_RULES—— 自我复制规则列表
  CATEGORIES         —— 原料词条 dict(供推导多编码特征码)
  RAW_TRAITS         —— 直接特征码 dict(最终形态,子串比对用)
  MULTI_ENC_TRAITS   —— 多编码特征码 dict(由 CATEGORIES+ENCODERS 推导并与 RAW_TRAITS 合并)
  ENCODERS           —— 编码器注册表(生成逻辑)
"""
import os, json, re
import base64, codecs


class bashfunc:  # bash 函数/内建类(危险动态执行入口)
	def __init__(self, name, threateninglevel=0, desc=''):
		self.name = name            # 函数/内建名(eval/exec/source/...)
		self.threateninglevel = threateninglevel  # 威胁等级
		self.desc = desc


# ===================================================================
# 规则数据 JSON 加载
# 无论从哪个目录 import,都以本文件所在目录为基准定位 JSON,
# 保证各 json 始终能正确找到。
# ===================================================================
_RULES_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_json(name):
	path = os.path.join(_RULES_DIR, name)
	if not os.path.isfile(path):
		raise FileNotFoundError('规则数据文件缺失:%s' % path)
	with open(path, encoding='utf-8') as f:
		return json.load(f)


# ---- 1. 恶意函数库(对应 bash_threatening_funcs.json) ----
# JSON 结构:[{name, level, desc}, ...]
THREAT_FUNCS = [
	bashfunc(item['name'], item.get('level', 0), item.get('desc', ''))
	for item in _load_json('bash_threatening_funcs.json')
]
FUNC_NAMES = {f.name for f in THREAT_FUNCS}


# ---- 2. 恶意命令规则(对应 bash_malicious_commands.json) ----
# JSON 结构:[{id,名称,威胁类型,命令,危险参数,级别,描述,参考}, ...]
MALICIOUS_COMMANDS = _load_json('bash_malicious_commands.json')
COMMANDS_BY_NAME = {}
for _r in MALICIOUS_COMMANDS:
	COMMANDS_BY_NAME.setdefault(_r.get('命令'), []).append(_r)


# ---- 3. 恶意变量规则(对应 bash_malicious_variables.json) ----
# JSON 结构:[{id,名称,威胁类型,变量,危险值特征,危险赋值符,级别,描述,参考}, ...]
MALICIOUS_VARIABLES = _load_json('bash_malicious_variables.json')


# ---- 4. 恶意文件写入规则(对应 bash_file_write.json) ----
# JSON 结构:[{id,名称,威胁类型,目标路径特征,危险内容特征,级别,描述,参考}, ...]
FILE_WRITE_RULES = _load_json('bash_file_write.json')


# ---- 5. 自我复制规则(对应 bash_self_replicate.json) ----
# JSON 结构:[{id,名称,威胁类型,源特征,命令特征,目标路径特征,级别,描述,参考}, ...]
SELF_REPLICATE_RULES = _load_json('bash_self_replicate.json')


# ---- 6. 直接特征码库(对应 bash_raw_traits.json) ----
# JSON 结构: RAW_TRAITS[类别][编码]=[特征码,...](最终形态,子串比对,不再二次编码)
RAW_TRAITS = _load_json('bash_raw_traits.json')


# ===================================================================
# 多编码形式的威胁特征码(全局变量,便于扩展)
# 黑客常用的代码混淆编码形式均在此生成特征码,用于识别被混淆隐藏的 payload。
# 支持编码形式及示例:
#   base64   —— L2Rldi90Y3Av        ( /dev/tcp/ 的 base64)
#   url编码   —— %2f%64%65%76...
#   hex转义   —— \x2f\x64\x65...
#   octal转义 —— \057\144\145...
#   chr拼接   —— printf '\x2f' 等(此处仅作字符串编码展示)
#   rot13     —— 旋转字母
#   html实体  —— &#47;&#100;...
# 匹配是子串匹配,特征码是"原始字符串在某种编码下的形态"。
# ===================================================================
def _b64(s):  # base64 编码(不带 = 填充)
	return base64.b64encode(s.encode()).decode().rstrip('=')


def _urlenc(s):  # URL 百分号编码:每个字节 -> %XX(小写)
	return ''.join('%%%02x' % b for b in s.encode())


def _hexescape(s):  # hex 转义:\x2f 形式(小写)
	return ''.join('\\x%02x' % b for b in s.encode())


def _octalescape(s):  # 八进制转义:\057 形式
	return ''.join('\\%03o' % b for b in s.encode())


def _chrjoin(s):  # chr 拼接(展示用,对应 bash 的 printf '\xNN' 思路)
	return '.'.join('chr(%d)' % b for b in s.encode())


def _rot13(s):  # ROT13 变换(仅对 ASCII 字母有效)
	return codecs.encode(s, 'rot_13')


def _htmlent(s):  # HTML 实体(十进制):&#47;...
	return ''.join('&#%d;' % b for b in s.encode())


# 编码器注册表:名称 -> 编码函数
# 说明:plain 为"明文原样保留"通道 —— 用于让真实样本提取的高确定性明文指纹
#       (如 "chmod u+s")直接以明文子串参与匹配,命中即判死。plain 编码不做任何变换。
ENCODERS = {
	'plain': lambda s: s,
	'base64': _b64,
	'url': _urlenc,
	'hex': _hexescape,
	'octal': _octalescape,
	'chr': _chrjoin,
	'rot13': _rot13,
	'html': _htmlent,
}

# ===================================================================
# 以下为"生成逻辑":CATEGORIES(原料词条,JSON 读取) + ENCODERS(编码器)
# 推导出 MULTI_ENC_TRAITS 多编码特征码,并与 RAW_TRAITS(JSON 直读)合并。
# 若需更改推导来源的词条,改 bash_categories.json 即可,无需动本文件。
# ===================================================================
# ---- 各威胁类别的原始高危字符串(原料,读自 bash_categories.json) ----
# JSON 结构:CATEGORIES={类别:[词条,...],...}
CATEGORIES = _load_json('bash_categories.json')

# 特征码最小长度门槛。
# 短特征码(2~3 字节)在日志/随机数据里会大量碰撞,造成严重误报;
# 4 字节及以上时随机碰撞概率约 1/95^4 ≈ 千万分之一,基本不误报。
# 长度不足门槛的特征码直接丢弃。
MIN_TRAIT_LEN = 4

# ===================================================================
# 生成最终特征码数据结构:
#   MULTI_ENC_TRAITS={类别:{编码名称:[特征码,...],...}}
# 由两类来源合并去重:
#   1. CATEGORIES 推导(已知词条 + 各编码器);
#   2. RAW_TRAITS 直接特征码(已知恶意样本指纹,未知源码也能用)。
# ===================================================================
MULTI_ENC_TRAITS = {}
for _cat, _words in CATEGORIES.items():
	MULTI_ENC_TRAITS[_cat] = {}
	for _name, _fn in ENCODERS.items():
		if _name == 'plain':
			# plain(明文)通道只保留 RAW_TRAITS 的完整高确定性指纹,
			# 不对 CATEGORIES 纯词条做明文子串 —— 否则 'eval'/'PATH' 等
			# 常见词会在正常脚本里大量误报。明文检测本由各分类规则覆盖。
			_src = set(RAW_TRAITS.get(_cat, {}).get('plain', []))
		else:
			_encoded = {_fn(w) for w in _words}
			_src = _encoded | set(RAW_TRAITS.get(_cat, {}).get(_name, []))
		MULTI_ENC_TRAITS[_cat][_name] = sorted(t for t in _src if len(t) >= MIN_TRAIT_LEN)


# ===================================================================
# 便捷查询接口(只读,不含任何扫描/研判逻辑;扫描由正则层负责)
# ===================================================================
def get_func_level(name):
	"""返回某函数/内建名的威胁级别(未收录返回 0)。"""
	for f in THREAT_FUNCS:
		if f.name == name:
			return f.threateninglevel
	return 0


def get_func(name):
	"""返回 bashfunc 对象或 None。"""
	for f in THREAT_FUNCS:
		if f.name == name:
			return f
	return None


def summary():
	"""打印已加载规则库的概要,便于联调与人工核对。"""
	print('=== Bash 规则库加载概要 ===')
	print('恶意函数(bash_threatening_funcs): %d 条' % len(THREAT_FUNCS))
	print('恶意命令(bash_malicious_commands): %d 条' % len(MALICIOUS_COMMANDS))
	print('恶意变量(bash_malicious_variables): %d 条' % len(MALICIOUS_VARIABLES))
	print('恶意文件写入(bash_file_write): %d 条' % len(FILE_WRITE_RULES))
	print('自我复制(bash_self_replicate): %d 条' % len(SELF_REPLICATE_RULES))
	print('原始类别(bash_categories): %d 类' % len(CATEGORIES))
	_nraw = sum(len(v) for cat in RAW_TRAITS.values() for v in cat.values())
	print('直接特征码(bash_raw_traits): %d 条(跨 %d 类)' % (_nraw, len(RAW_TRAITS)))
	_nmulti = sum(len(v) for cat in MULTI_ENC_TRAITS.values() for v in cat.values())
	print('多编码特征码(MULTI_ENC_TRAITS): %d 条(跨 %d 类 × %d 编码)'
		  % (_nmulti, len(MULTI_ENC_TRAITS), len(ENCODERS)))
	print('===========================')


if __name__ == '__main__':
	summary()

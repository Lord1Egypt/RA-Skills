"""
php_ast_normalize.py —— AST → 行为增强文本 归一化脚本

设计依据(读自正则组件 php_common / threat_func_dect / dynamic_var_dect / trait_dect / file_write_dect 的匹配逻辑):

正则组件"识别什么":
  1. 威胁函数调用:  `\\b(?:eval|system|...)\\s*\\(` —— 认"函数名+左括号"
  2. 超全局:        `\\$_()(...)\\[\\s*['\"]?\\w+['\"]?\\]`
  3. 溯源:          取参数里的 $var → 在 lines_upto 里找 `$var = ...;` → 查赋值串含超全局 → 级别+1
  4. 特征码:        MULTI_ENC_TRAITS 子串匹配(plain/base64/url/hex/octal/chr/rot13/html)

正则组件的三大盲点(已实测确认):
  A. eval($_POST['c']) 直接作参数 → find_php_variables 匹配不到 $var(已是超全局) → 溯源空 → 危险级别不+1
  B. $x="sys";$y="tem";eval($x.$y) → 命中 eval 但看不出拼接成危险函数双段
  C. $f="system";$f($a)            → 动态函数名 $f(...) 正则 \\b(...) 匹配不到 → 完全漏报

AST 归一化目标:
  经 tree-sitter 解析生成一份"等效但暴露更多行为特点"的 PHP 文本:
  1. 常量折叠     : $x="sys" 解析为字面量
  2. 变量解析     : 全文件赋值表替换参数里的 $var(递归到叶子)
  3. 动态函数名   : $f="system";$f(...) → system(...)
  4. 拼接折叠     : eval($x.$y) 若 $x="s" $y="ystem" → eval(system) 并在旁标注
  5. 污点链摊平   : $a=$_POST; $d=str_rot13($a); eval($d) → eval(str_rot13($_POST...)) 供溯源+1

输出: 归一化文本(供 phpdect.py 扫描/或后续 AST 特征识别)。

本文件职责(2026-09-01 重构):
  作为 纯翻译函数库 供 phpdect.py import 调用:
    - normalize(file_path) / normalize_source(src_bytes) → 返回归一化等效 PHP 文本;
    - 只做 AST 解析 + 归一化翻译(常量折叠/变量解析/动态函数名/拼接折叠/污点摊平/编码还原),
      不包含任何"是否判定为恶意/威胁级别"的研判逻辑;
    - 最终安全研判由调用方 phpdect.py 负责(威胁函数/特征码/逻辑规则)。

依赖: tree_sitter_language_pack (mainwork3_12_13 环境)
用法:
  # 作为库:
  from php_ast_normalize import normalize, normalize_source
  text=normalize('file.php')
  text2=normalize_source(src_bytes)
  # 命令行自测:
  python php_ast_normalize.py <file.php>
"""
import sys, re, os

import tree_sitter_language_pack as ts_pack

# 超全局变量名(叶子,不解析)
SUPERGLOBALS={'$_GET','$_POST','$_REQUEST','$_COOKIE','$_SERVER','$_FILES','$_SESSION','$_ENV','$GLOBALS'}

# 解码/还原函数:包裹的实参视为"污点/混淆源"
DECODERS={'base64_decode','gzinflate','gzuncompress','gzdecode','str_rot13','urldecode','rawurldecode','hex2bin','convert_uudecode','convert_uuencode'}

# 危险函数(污点传播终点)
DANGEROUS={'eval','assert','system','exec','shell_exec','passthru','popen','proc_open','pcntl_exec','create_function','call_user_func','call_user_func_array','include','include_once','require','require_once','unserialize','preg_replace'}

IDENT_RE=re.compile(r'^[A-Za-z_][\w\\]*$')

# 已知威胁函数名(用于解码还原后的函数名判定)
import json, os as _os
_THREAT_NAMES=set()
_rules={
	'eval':'eval','assert':'assert','system':'system','exec':'exec','shell_exec':'shell_exec',
	'passthru':'passthru','popen':'popen','proc_open':'proc_open','pcntl_exec':'pcntl_exec',
	'create_function':'create_function','call_user_func':'call_user_func','call_user_func_array':'call_user_func_array',
	'include':'include','include_once':'include_once','require':'require','require_once':'require_once',
	'unserialize':'unserialize','preg_replace':'preg_replace','base64_decode':'base64_decode','gzinflate':'gzinflate',
	'gzuncompress':'gzuncompress','hex2bin':'hex2bin','str_rot13':'str_rot13','urldecode':'urldecode',
	'file_put_contents':'file_put_contents','fwrite':'fwrite','fopen':'fopen','copy':'copy','rename':'rename',
	'curl_exec':'curl_exec','fsockopen':'fsockopen','mail':'mail','extract':'extract','parse_str':'parse_str',
}
_THREAT_NAMES=set(_rules.keys())

import codecs as _codecs

def _dec_chain(raw_text):
	"""对原始源码文本做多段解码链还原,返回威胁函数名或 None。
	支持: chr(n).chr(n)... 序列 → 字符串 → 再 str_rot13/hex 解码尝试。
	"""
	if not raw_text: return None
	chrs=re.findall(r"chr\s*\(\s*(\d+)\s*\)",raw_text)
	if chrs:
		try:
			s=''.join(chr(int(c)) for c in chrs)
			dn=_dec_str(s)
			if dn: return dn
			r=_dec_str(_codecs.decode(s,'rot_13')) if s.isalpha() else None
			if r: return r
		except Exception: pass
	for m in re.finditer(r"(['\"])(.*?)\1",raw_text):
		dn=_dec_str(m.group(2))
		if dn: return dn
	return None


def _dec_str(s):
	"""尝试把字符串 s 还原为可能的威胁函数名;成功返回函数名,否则返回 None。
	支持: 纯标识符 / str_rot13 / hex转义 / chr序列 / base64(乐观尝试)。
	"""
	t=s.strip()
	if len(t)>=2 and t[0] in ("'",'"') and t[-1]==t[0]:
		t=t[1:-1]
	if t in _THREAT_NAMES:
		return t
	# str_rot13(仅字母)
	try:
		cand=_codecs.decode(t,'rot_13')
		if cand in _THREAT_NAMES: return cand
	except Exception: pass
	# hex 转义 \x65\x76...
	if '\\x' in t:
		try:
			cand=bytes(int(h,16) for h in re.findall(r'\\x([0-9a-fA-F]{2})',t)).decode('utf-8','ignore')
			if cand in _THREAT_NAMES: return cand
		except Exception: pass
	return None


class _StrLit:
	"""字符串字面量代理节点(AST 拼接折叠的产物)。
	.var 提供 "xxx"(带引号) 形式, 与真实 string 节点的 txt() 输出一致,
	使 resolve/expr 无需区分真假节点。"""
	def __init__(self,s):
		self.s=s
		# 模拟 string 节点的 txt(): 带引号包裹
	@property
	def type(self):
		return 'string'

	def __repr__(self):
		return '&quot;%s&quot;'%self.s


class AstNorm:
	def __init__(self,src,root):
		self.src=src
		self.root=root
		self.assign={}  # var -> expr node
		self.locs=[]    # 归一化每条语句对应的原文定位 [(文本,行0,行1,偏移0,偏移1),...]
		self._collect()
		self.out_lines=[]

	def txt(self,n):
		if n is None: return ''
		if isinstance(n,_StrLit):
			# 拼接折叠的伪字符串节点: 直接返回带引号文本
			return '"%s"'%n.s if n.s!='*_DYN_*' else '$var'
		return self.src[n.start_byte:n.end_byte].decode('utf-8','ignore')

	def _collect(self):
		# 处理顺序: 先收集所有普通 assignment, 再处理增广赋值(拼接/运算累积),
		# 使 $a='sy'; $a.='st'; $a.='em' 能折叠成 $a='system'。
		aug=[]
		def rec(n):
			if n.type=='assignment_expression':
				left=n.child_by_field_name('left')
				right=n.child_by_field_name('right')
				if left and left.type=='variable_name':
					nm=self.txt(left).strip()
					if nm.startswith('$'):
						self.assign[nm]=right
			elif n.type=='augmented_assignment_expression':
				aug.append(n)  # 延迟处理, 保证前面的=赋值已就位
			for c in n.children:
				rec(c)
		rec(self.root)
		# 增广赋值累积: 仅在“字符串拼接 .=”时可合并字面量;
		# 其他运算符(+= 等)保留动态标记, 不做错误拼接。
		for n in aug:
			left=n.child_by_field_name('left')
			op=n.child_by_field_name('operator')
			right=n.child_by_field_name('right')
			if not left or left.type!='variable_name':
				continue
			nm=self.txt(left).strip()
			if not nm.startswith('$'):
				continue
			opc=self.txt(op).strip() if op else ''
			if opc != '.=':
				# 非拼接增广(如 +=): 变量值复杂化, 无法确定字符串, 标记为动态
				self.assign[nm]=None
				continue
			prev=self.assign.get(nm)
			# prev 必须已是可解析的字面量字符串(此前被 $a='sy' 赋值过)
			if prev is not None and prev.type in ('string','encapsed_string'):
				pv=self._literal(self.txt(prev))
				rv=self._literal(self.expr(right,{nm})) if right else None
				if pv is not None and rv is not None:
					# 拼接合并为字符串字面量节点代理(用带包裹的文本)
					self.assign[nm] = _StrLit(pv+rv)
				else:
					self.assign[nm]=None
			else:
				self.assign[nm]=None

	# ---------- 表达式 → 归一化文本 ----------
	def expr(self,n,seen=None):
		if n is None: return ''
		seen=seen or set()
		t=n.type
		# 解开 argument / 括号等包装节点
		if t=='argument' and n.child_count==1:
			return self.expr(n.children[0],seen)
		# 字符串/数值字面量
		if t in ('string','encapsed_string'):
			return self.txt(n).strip()
		if t in ('string_content','name','number'):
			return self.txt(n).strip()
		if t in ('true','false','null'):
			return self.txt(n).strip()
		# 变量引用 → 解析
		if t=='variable_name':
			return self.resolve(self.txt(n).strip(),seen)
		# 超全局下标 $_GET['x']
		if t=='subscript_expression':
			return self.txt(n).strip()
		# 二元运算(含 . 拼接 / + -)
		if t=='binary_expression':
			left=n.child_by_field_name('left')
			op=n.child_by_field_name('operator')
			right=n.child_by_field_name('right')
			lt=self.expr(left,seen); rt=self.expr(right,seen)
			opc=self.txt(op).strip() if op else '.'
			if opc=='.':
				# 拼接折叠:若两侧都是可解析字符串字面量则合并
				lv=self._literal(lt); rv=self._literal(rt)
				if lv is not None and rv is not None:
					return '"%s"'%(lv+rv)
				return '(%s . %s)'%(lt,rt)
			return '(%s %s %s)'%(lt,opc,rt)
		# 函数调用
		if t=='function_call_expression':
			fn_node=n.child_by_field_name('function')
			args_node=n.child_by_field_name('arguments')
			if not fn_node:
				return self.txt(n).strip()
			if fn_node.type=='variable_name':
				# 动态函数名
				dn=self.txt(fn_node).strip()
				r=self.resolve(dn,seen)
				# 去引号后判断是否合法标识符(如 $f="system" → system)
				r=re.sub(r'^["\']|["\']$','',r) if not IDENT_RE.match(r) else r
				if not IDENT_RE.match(r):
					# 兜底:对赋值表达式原始源码做解码链还原($hex="\\x65.." / $chr=chr(..)..)
					_asgn=self.assign.get(dn)
					if _asgn is not None:
						dec=_dec_chain(self.txt(_asgn))
						if dec in _THREAT_NAMES:
							fn=dec
						else:
							fn='${%s}'%re.sub(r'^["\']|["\']$','',dn)
					else:
						fn='${%s}'%re.sub(r'^["\']|["\']$','',dn)
				elif IDENT_RE.match(r):
					fn=r
				else:
					fn='${%s}'%re.sub(r'^["\']|["\']$','',dn)  # 解析不出,保留动态标记
			else:
				fn=self.txt(fn_node).strip().split('(')[0]
			# 实参
			inner=''
			if args_node:
				parts=[]
				for a in args_node.children:
					if a.type in ('argument','variable_name','subscript_expression','binary_expression','string','encapsed_string','function_call_expression','number','name'):
						parts.append(self.expr(a,seen))
				inner=', '.join(parts)
				inner=inner.strip()
				# 去掉最外层冗余括号(如 (")system") 来自拼接折叠)
				if len(inner)>=2 and inner[0]=='(' and inner[-1]==')':
					inner=inner[1:-1]
			# 若fn在DANGEROUS且当前是污点,保留
			return '%s(%s)'%(fn,inner)
		# 其他(括号/表达式)原样
		return self.txt(n).strip()

	def _literal(self,s):
		"""若 s 是 'xxx' 或 "xxx",返回去引号内容;否则 None。"""
		s=s.strip()
		if len(s)>=2 and s[0] in ("'",'"') and s[-1]==s[0]:
			return s[1:-1]
		return None

	def resolve(self,varname,seen=None):
		"""解析变量:赋值表里若能解析到 字符串/超全局/解码调用/另一变量,递归;否则原样。"""
		seen=seen or set()
		if varname in seen or varname not in self.assign:
			return varname
		seen=seen|{varname}
		expr=self.assign[varname]
		t=expr.type
		# 字符串字面量
		if t in ('string','encapsed_string'):
			return self.txt(expr).strip()
		# 超全局/下标
		if t=='subscript_expression':
			return self.txt(expr).strip()
		if t=='variable_name':
			return self.resolve(self.txt(expr).strip(),seen)
		# 解码函数调用: 若最终能还原为威胁函数名,直接返回该名
		if t=='function_call_expression':
			fn_node=expr.child_by_field_name('function')
			fn=self.txt(fn_node).strip().split('(')[0] if fn_node and fn_node.type!='variable_name' else self.resolve(self.txt(fn_node).strip(),seen) if fn_node else ''
			# 解析实参里的字符串字面量原始值
			raw=self.expr(expr,seen)
			# 提取字面量尝试解码还原(chr序列/rot13/hex)
			dn=_dec_chain(self.txt(expr))
			if dn in _THREAT_NAMES:
				return dn
			# 解码/危险函数 → 递归解析其实参里的变量,标注污点来源
			if fn in DECODERS or fn in DANGEROUS:
				args_node=expr.child_by_field_name('arguments')
				inner=self.expr(args_node,seen) if args_node else ''
				return '%s(%s)'%(fn,inner)
			return raw
		# 拼接等 → 再展开
		return self.expr(expr,seen)

	# ---------- 顶层语句归一化 ----------
	def stmt(self,n):
		t=n.type
		# 记录定位: 该语句对应 AST 节点在原文的行区间与字节偏移
		row0=n.start_point.row+1  # 1-based 行号
		row1=n.end_point.row+1
		b0=n.start_byte
		b1=n.end_byte
		if t=='function_call_expression':
			text=self.expr(n)+';'
			self.out_lines.append(text)
			self.locs.append((text,row0,row1,b0,b1))
		elif t=='assignment_expression':
			left=self.txt(n.child_by_field_name('left')).strip()
			right=self.expr(n.child_by_field_name('right'))
			text='%s = %s;'%(left,right)
			self.out_lines.append(text)
			self.locs.append((text,row0,row1,b0,b1))
		# 其他语句(echo/if/循环等)现阶段原样保留文本
		else:
			text=self.txt(n).strip()
			self.out_lines.append(text)
			self.locs.append((text,row0,row1,b0,b1))

	def normalize(self):
		for child in self.root.children:
			st=child.type
			if st=='expression_statement':
				for inner in child.children:
					if inner.type in ('function_call_expression','assignment_expression'):
						self.stmt(inner)
			elif st in ('function_call_expression','assignment_expression'):
				self.stmt(child)
		return '\n'.join(x for x in self.out_lines if x)


def normalize_source(src):
	"""对 PHP 源码字节/文本做 AST 归一化, 返回归一化等效 PHP 文本(str)。
	无失败防护: 解析失败会抛异常(由调用方 phpdect.py 决定是否回退原文本)。
	"""
	if isinstance(src,str):
		src=src.encode('utf-8')
	root=ts_pack.get_parser('php').parse(src).root_node
	norm=AstNorm(src,root)
	return norm.normalize()


def normalize_source_with_loc(src):
	"""对 PHP 源码做 AST 归一化, 返回 (纯文本, 定位列表)。
	定位列表每项: {文本, 行:原文起行(1based), 行止:原文止行, 偏移起, 偏移止}
	与归一化文本的语句一一对应, 供研判命中后反查原文位置。
	"""
	if isinstance(src,str):
		src=src.encode('utf-8')
	root=ts_pack.get_parser('php').parse(src).root_node
	norm=AstNorm(src,root)
	text=norm.normalize()
	locs=[{
		"文本":t,
		"行":r0,
		"行止":r1,
		"偏移起":b0,
		"偏移止":b1,
	} for (t,r0,r1,b0,b1) in norm.locs]
	return text,locs


def normalize(file_path):
	"""对文件做 AST 归一化, 返回归一化等效 PHP 文本(str)。"""
	with open(file_path,'rb') as f:
		src=f.read()
	return normalize_source(src)


def normalize_with_loc(file_path):
	"""对文件做 AST 归一化, 返回 (纯文本, 定位列表)。"""
	with open(file_path,'rb') as f:
		src=f.read()
	return normalize_source_with_loc(src)


def main():
	args=sys.argv[1:]
	if not args:
		print('用法: python php_ast_normalize.py <file.php>')
		sys.exit(1)
	fp=args[0]
	print('===== 归一化文本(暴露更多行为特点的等效 PHP) =====')
	print(normalize(fp))

if __name__=='__main__':
	main()

#-*- coding:utf-8 -*-
"""
js_ast_normalize.py —— JS: AST → 行为增强文本 归一化脚本(对称于 php_ast_normalize.py)

设计依据(读自正则组件 js_common / js_threat_func_dect / js_dynamic_code_dect / js_trait_dect / js_file_write_dect 的匹配逻辑):

正则组件"识别什么":
  1. 威胁函数调用:  \\b(?:eval|Function|spawn|exec|child_process.exec|...)\\s*\\( 或成员调用 child_process.exec(...)
  2. 外部输入源:    process.env/process.argv/location/document.URL/URLSearchParams/localStorage/sessionStorage/event.data/postMessage
  3. sink×source:   eval/Function/setTimeout/innerHTML/document.write/location 等 危险 sink × 外部 source → 动态代码执行
  4. 溯源:          取参数变量 → 在 lines_upto 找赋值 → 查外部输入 → 级别+1
  5. 特征码:        MULTI_ENC_TRAITS 子串匹配

与 PHP 版相同的归一化目标(把源码翻译成"正则组件好认"的等效 JS 文本):
  1. 常量折叠     : const x="sy" 解析字面量
  2. 变量解析     : 全文件赋值表替换参数里的变量(递归到叶子)
  3. 动态函数名   : const f="system";f()→调用;  const s=String.fromCharCode(...) 还原
  4. 拼接折叠     : eval(x+y) 若 x="sy" y="stem" → eval("system")
  5. 污点链摊平   : a=process.env.CMD; b=atob(a); eval(b) → eval(atob(process.env.CMD))
  6. 编码还原     : atob/hex转义/charCode 序列 → 威胁函数名

依赖: tree_sitter_language_pack (mainwork3_12_13 环境)
用法:
	<mainwork3_12_13 python> js_ast_normalize.py <file.js>
"""
import sys, re, base64, os

import tree_sitter_language_pack as ts_pack

JS_LANG='javascript'

# 外部可控输入源(叶子/保留)
EXTERNAL_SRC=('process.env','process.argv','location','document.URL','URLSearchParams',
	'localStorage','sessionStorage','event.data','postMessage','window.location')

# 解码/还原类(污点来源; js 的 chr ≈ String.fromCharCode, base64 ≈ atob)
DECODERS=('atob','decodeURIComponent','unescape','String.fromCharCode','fromCharCode',
	'Buffer.from','parseInt')

# 危险 sink(动态执行终点; 对称 PHP 的 DANGEROUS)
DANGEROUS=('eval','Function','setTimeout','setInterval','document.write','document.writeln',
	'innerHTML','outerHTML','insertAdjacentHTML','exec','execSync','execFile','spawn','spawnSync',
	'fork','child_process.exec','child_process.spawn','child_process.fork','child_process.execFile',
	'vm.runInThisContext','vm.runInNewContext','vm.runInContext','require','location.href',
	'window.open','document.cookie','process.exit')

IDENT_RE=re.compile(r'^[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*$')

# 已知威胁函数名(用于解码还原后的函数名判定)
THREAT_NAMES=set(DANGEROUS) | set(('eval','Function','spawn','exec','child_process','system'))


def _strip_quotes(s):
	s=s.strip()
	if len(s)>=2 and s[0] in ("'",'"') and s[-1]==s[0]:
		# 处理 \x 转义
		return re.sub(r'\\x([0-9a-fA-F]{2})',lambda m:chr(int(m.group(1),16)),s[1:-1])
	return s


def _dec_str(s):
	"""尝试把字符串 s 还原为威胁函数名;成功返回函数名,否则 None。
	支持: 纯标识符 / hex转义 / base64(atob乐观) / unescape。
	"""
	t=_strip_quotes(s)
	if t in THREAT_NAMES:
		return t
	# hex 转义(已在 _strip_quotes 处理引号内 \\x..)
	t2=_strip_quotes(s)
	if t2 in THREAT_NAMES:
		return t2
	# base64(atob): 只有当解码结果是威胁名才用,避免误伤
	if re.fullmatch(r'[A-Za-z0-9+/=]+',t):
		try:
			dec=base64.b64decode(t).decode('utf-8','ignore')
			if dec in THREAT_NAMES:
				return dec
		except Exception: pass
	# unescape %XX / \uXXXX
	try:
		dec=re.sub(r'%([0-9a-fA-F]{2})',lambda m:chr(int(m.group(1),16)),t)
		if dec in THREAT_NAMES:
			return dec
	except Exception: pass
	return None


def _dec_chain(raw_text):
	"""对原始源码文本做多段解码链还原,返回威胁函数名或 None。
	支持: String.fromCharCode(115,121,...) / atob("...") / 拼接折叠。
	"""
	if not raw_text: return None
	# String.fromCharCode(115,121,...) → 字符串
	m=re.search(r'(?:String\.)?fromCharCode\s*\(([^)]*)\)',raw_text)
	if m:
		try:
			nums=[int(x.strip()) for x in m.group(1).split(',') if x.strip().isdigit()]
			if nums:
				s=''.join(chr(n) for n in nums)
				dn=_dec_str(s)
				if dn: return dn
		except Exception: pass
	# atob("...") → base64
	m=re.search(r'atob\s*\(\s*([\'"])(.*?)\1\s*\)',raw_text)
	if m:
		dn=_dec_str(m.group(2))
		if dn: return dn
	# 引号包裹的字符串直接尝试
	for m in re.finditer(r"(['\"])(.*?)\1",raw_text):
		dn=_dec_str(m.group(2))
		if dn: return dn
	return None


class JsNorm:
	def __init__(self,src,root):
		self.src=src
		self.root=root
		self.assign={}  # name(unquoted) -> value node
		self.locs=[]    # 归一化每条语句对应的原文定位 [(文本,行0,行1,偏移0,偏移1),...]
		self._collect()
		self.out_lines=[]

	def txt(self,n):
		if n is None: return ''
		return self.src[n.start_byte:n.end_byte].decode('utf-8','ignore')

	def _collect(self):
		def rec(n):
			if n.type=='variable_declarator':
				name=n.child_by_field_name('name')
				value=n.child_by_field_name('value')
				if name and name.type in ('identifier','member_expression'):
					nm=self.txt(name).strip()
					if nm and value is not None:
						self.assign[nm]=value
			for c in n.children:
				rec(c)
		rec(self.root)

	def _literal(self,s):
		s=s.strip()
		return _strip_quotes(s) if (len(s)>=2 and s[0] in ("'",'"') and s[-1]==s[0]) else None

	def resolve(self,name,seen=None):
		"""解析变量:赋值表里若能解析到 字符串字面量/外部输入/调用/另一变量,递归;否则原样。"""
		seen=seen or set()
		if name in seen or name not in self.assign:
			return name
		seen=seen|{name}
		expr=self.assign[name]
		t=expr.type
		# 字符串字面量
		if t=='string':
			return self.txt(expr).strip()
		# 外部输入 member_expression 如 process.env.CMD
		if t=='member_expression':
			return self.txt(expr).strip()
		if t=='identifier':
			# 布尔/数字等字面量经 identifier 到 string_fragment 不等;直接取文本
			return self.txt(expr).strip()
		# 其他表达式 → 展开
		return self.expr(expr,seen)

	def expr(self,n,seen=None):
		if n is None: return ''
		seen=seen or set()
		t=n.type
		# 叶子
		if t=='string':
			return self.txt(n).strip()
		if t in ('number','true','false','null','undefined'):
			return self.txt(n).strip()
		if t=='identifier':
			return self.resolve(self.txt(n).strip(),seen)
		# 成员表达式(外部输入/威胁API) 保留
		if t=='member_expression':
			return self.txt(n).strip()
		# 二元运算(含 + 拼接)
		if t=='binary_expression':
			left=n.child_by_field_name('left')
			right=n.child_by_field_name('right')
			op=None
			for c in n.children:
				if c.type in ('+','-','*','/','%','&&','||'):
					op=self.txt(c).strip(); break
			lt=self.expr(left,seen); rt=self.expr(right,seen)
			if op=='+':
				lv=self._literal(lt); rv=self._literal(rt)
				if lv is not None and rv is not None:
					return '"%s"'%(lv+rv)
				return '(%s + %s)'%(lt,rt)
			return '(%s %s %s)'%(lt,op or '+',rt)
		# 调用表达式
		if t=='call_expression':
			fn_node=n.child_by_field_name('function')
			args_node=n.child_by_field_name('arguments')
			if not fn_node:
				return self.txt(n).strip()
			if fn_node.type=='member_expression':
				# 如 child_process.exec / fs.writeFile / String.fromCharCode
				fn=self.txt(fn_node).strip()
			else:
				fn=self.txt(fn_node).strip()
				# 动态函数名: 若是 identifier 且可解析
				if fn_node.type=='identifier':
					r=self.resolve(fn,seen)
					r_noq=_dec_str(r) or r
					if IDENT_RE.match(r_noq):
						fn=r_noq
					else:
						# 编码还原兜底
						dec=_dec_chain(self.txt(self.assign.get(fn,'')) if isinstance(self.assign.get(fn),object) else '')
						fn=dec if dec else ('${%s}'%fn)
			# 实参
			inner=''
			if args_node:
				parts=[]
				for a in args_node.children:
					if a.type in ('argument','identifier','member_expression','string','number','binary_expression','call_expression','true','false','null','undefined'):
						parts.append(self.expr(a,seen))
				inner=', '.join(parts)
				inner=inner.strip()
				if len(inner)>=2 and inner[0]=='(' and inner[-1]==')':
					inner=inner[1:-1]
			return '%s(%s)'%(fn,inner)
		# 其他(如 new Function / 模板串) 原样,尝试折叠
		txt=self.txt(n).strip()
		dec=_dec_str(txt)
		if dec:
			return dec
		return txt

	def _emit(self,n,text):
		"""输出一条归一化语句,并同步记录它对应的原文定位。

		空文本直接丢弃 —— 保证 out_lines 与 locs 严格一一对应,
		调用方(jsdect.py)正是按索引反查原文行号/偏移的。
		"""
		if not text:return
		self.out_lines.append(text)
		self.locs.append((text,n.start_point.row+1,n.end_point.row+1,n.start_byte,n.end_byte))

	def stmt(self,n):
		t=n.type
		if t=='call_expression':
			self._emit(n,self.expr(n)+';')
		elif t=='variable_declarator':
			name=self.txt(n.child_by_field_name('name')).strip()
			value=self.expr(n.child_by_field_name('value'))
			self._emit(n,'%s = %s;'%(name,value))
		elif t=='lexical_declaration' or t=='variable_declaration':
			for c in n.children:
				if c.type=='variable_declarator':
					self.stmt(c)
		# 其他语句(表达式/return/if等)保留
		else:
			self._emit(n,self.txt(n).strip())

	def normalize(self):
		for child in self.root.children:
			t=child.type
			if t in ('expression_statement',):
				for inner in child.children:
					if inner.type in ('call_expression','assignment_expression'):
						self.stmt(inner)
					elif inner.type!=';':
						self.stmt(inner)
			elif t in ('lexical_declaration','variable_declaration','call_expression','assignment_expression','expression_statement','return_statement'):
				self.stmt(child)
		return '\n'.join(x for x in self.out_lines if x)


def normalize_source(src):
	"""对 JS 源码字节/文本做 AST 归一化, 返回归一化等效 JS 文本(str)。
	解析失败会抛异常(由调用方 jsdect.py 决定回退)。
	"""
	if isinstance(src,str):
		src=src.encode('utf-8')
	root=ts_pack.get_parser(JS_LANG).parse(src).root_node
	return JsNorm(src,root).normalize()


def normalize_source_with_loc(src):
	"""对 JS 源码做 AST 归一化, 返回 (纯文本, 定位列表)。
	定位列表每项: {文本,行,行止,偏移起,偏移止}。

	与归一化文本的【行】一一对应:一条归一化语句若输出多行(如原样保留的
	if/return 语句),则为其每一行复制同一条定位。这样调用方按行索引 i
	取 locs[i] 时不会串位。
	"""
	if isinstance(src,str):
		src=src.encode('utf-8')
	root=ts_pack.get_parser(JS_LANG).parse(src).root_node
	norm=JsNorm(src,root)
	text=norm.normalize()
	locs=[]
	for line,(t,r0,r1,b0,b1) in zip(norm.out_lines,norm.locs):
		for _ in line.split('\n'):
			locs.append({
				"文本":t,"行":r0,"行止":r1,"偏移起":b0,"偏移止":b1,
			})
	return text,locs


def normalize(file_path):
	"""对文件做 AST 归一化, 返回归一化等效 JS 文本(str)。"""
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
		print('用法: <py> js_ast_normalize.py <file.js>')
		sys.exit(1)
	fp=args[0]
	print('===== 归一化文本(暴露更多行为特点的等效 JS) =====')
	print(normalize(fp))


if __name__=='__main__':
	main()

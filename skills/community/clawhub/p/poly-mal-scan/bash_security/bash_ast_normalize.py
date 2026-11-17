#-*- coding:utf-8 -*-
"""
bash_ast_normalize.py —— Bash: AST → 行为增强文本 归一化脚本(对称于 php_ast_normalize.py / js_ast_normalize.py)

设计依据(读自 bash_security/恶意命令示例.md 的七大威胁类别):

正则/人工研判关心的"行为":
  1. 动态命令执行:  eval "cmd" / $cmd arg                       —— 认"命令名 + 参数",但命令名是变量时看不出真实意图
  2. 命令替换混淆:  echo $(echo $(whoami))                      —— 多层 $() 嵌套藏住真实命令
  3. 拼接/变量折叠: user@$ip / /tmp:$PATH                        —— 真实字符串被打散在变量与字面量之间
  4. 管道解码执行:  base64 -d x | bash / printf '\\x..'          —— 解码后直接执行,绕过字符串匹配
  5. PATH 劫持:     export PATH=/tmp:$PATH                       —— 让恶意程序优先于系统命令被执行
  6. 权限/后门:     chmod u+s / useradd -u 0 / echo key >> ~/.ssh/authorized_keys
  7. 持久化/破坏:   crontab / systemctl / rm -rf / iptables -F

与 PHP/JS 版相同的归一化目标(把源码翻译成"正则组件好认"的等效 Bash 文本):
  1. 常量折叠     : x="sy"; y="stem" 解析为字面量
  2. 变量解析     : 全文件赋值表替换参数/命令名里的 $var(递归到叶子)
  3. 动态命令名   : cmd="system"; $cmd /etc/shadow → system /etc/shadow
  4. 拼接折叠     : /tmp:$PATH 若 PATH=/usr/bin → /tmp:/usr/bin; "a$b" → "ab"
  5. 命令替换摊平 : echo $(whoami) → echo $(whoami) 并把内层命令也归一化(供溯源)
  6. 转义还原     : printf '\\x65\\x63..' 中的 \\xNN / 八进制转义还原为可见字符

输出: 归一化等效 Bash 文本(供后续 bash 安全研判/正则复用)。

本文件职责(对称于 PHP/JS 重构):
  作为 纯翻译函数库 供 bash 侧检测脚本(如 bashdect.py) import 调用:
    - normalize(file_path) / normalize_source(src_bytes) → 返回归一化等效 Bash 文本;
    - 只做 AST 解析 + 归一化翻译(常量折叠/变量解析/动态命令名/拼接折叠/命令替换摊平/转义还原),
      不包含任何"是否判定为恶意/威胁级别"的研判逻辑;
    - 最终安全研判由调用方负责(威胁命令/特征码/逻辑规则)。

依赖: tree_sitter_language_pack (mainwork3_12_13 环境)
用法:
  # 作为库:
  from bash_ast_normalize import normalize, normalize_source, normalize_with_loc
  text=normalize('file.sh')
  text2=normalize_source(src_bytes)
  text, locs = normalize_with_loc('file.sh')   # locs: 每条归一化语句对应的原文定位
  # 命令行自测:
  <mainwork3_12_13 python> bash_ast_normalize.py <file.sh>
"""
import sys, re

import tree_sitter_language_pack as ts_pack

BASH_LANG='bash'

# 外部可控输入源(污点来源,归一化时保留原样以提示溯源)
EXTERNAL_SRC=('$1','$2','$3','$@','$*','$RANDOM','$PATH','$HOME','$USER','$HOSTNAME',
	'$(whoami)','$(id)','$SSH_CONNECTION','$SSH_ORIGINAL_COMMAND')

# 解码/还原类(混淆来源; base64 / printf / xxd 等)
DECODERS=('base64','printf','xxd','od','hexdump','uuencode')

# 危险/敏感命令(污点传播终点,归一化后供研判匹配;对称 PHP 的 DANGEROUS)
DANGEROUS=('eval','exec','bash','sh','dash','zsh','source','.','curl','wget','nc','ncat',
	'netcat','scp','ssh','sshpass','crontab','chmod','chown','chattr','useradd','usermod',
	'adduser','echo','sed','awk','systemctl','service','iptables','ufw','rm','dd','mkfs',
	'kill','pkill','export','ln','nmap','arpspoof','telnet','socat','python','python3',
	'perl','ruby','php','find','tar','tee','cat')

# 已知威胁命令名(用于解码还原后的命令名判定)
THREAT_NAMES=set(DANGEROUS)|set(('system','/bin/bash','/bin/sh','reverse','bind','payload','malware'))

_CMD_RE=re.compile(r'^[A-Za-z0-9_./@%:+-]+$')
IDENT_RE=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

# 转义序列还原: \\xNN(十六进制) / \\NNN(八进制)
_ESC_HEX=re.compile(r'\\x([0-9a-fA-F]{2})')
_ESC_OCT=re.compile(r'\\([0-7]{1,3})')


def _decode_escapes(s):
	"""还原字符串中的 \\xNN 与 \\NNN 转义为可见字符(printf '\\x65..' 场景)。"""
	s=_ESC_HEX.sub(lambda m:chr(int(m.group(1),16)),s)
	s=_ESC_OCT.sub(lambda m:chr(int(m.group(1),8)),s)
	return s


def _strip_quotes(s):
	s=s.strip()
	if len(s)>=2 and s[0] in ("'",'"') and s[-1]==s[0]:
		return s[1:-1]
	return s


def _dec_str(s):
	"""尝试把字符串 s 还原为威胁命令名;成功返回命令名,否则 None。
	支持: 纯标识符 / base64(乐观,仅当解码结果全是可打印 ASCII)。"""
	t=_strip_quotes(s)
	if t in THREAT_NAMES:
		return t
	if re.fullmatch(r'[A-Za-z0-9+/=]+',t) and len(t)>=4:
		try:
			import base64
			dec=base64.b64decode(t+'=='[:(-len(t))%4]).decode('utf-8','ignore')
			if dec and all(32<=ord(c)<127 for c in dec) and dec in THREAT_NAMES:
				return dec
		except Exception:
			pass
	return None


def _dec_chain(raw_text):
	"""对原始源码文本做多段解码链还原,返回威胁命令名或 None。"""
	if not raw_text:return None
	# base64 "..." / '...'
	for m in re.finditer(r"([\"'])([A-Za-z0-9+/=]+)\1",raw_text):
		dn=_dec_str(m.group(2))
		if dn:return dn
	return None


class BashNorm:
	def __init__(self,src,root):
		self.src=src
		self.root=root
		self.assign={}  # "$var" -> value node
		self.locs=[]    # 归一化每条语句对应的原文定位 [(文本,行0,行1,偏移0,偏移1),...]
		self.out_lines=[]
		self._collect()

	def txt(self,n):
		if n is None:return ''
		return self.src[n.start_byte:n.end_byte].decode('utf-8','ignore')

	# ---------- 赋值收集 ----------
	def _collect(self):
		# 全树递归收集_variable_assignment(name/value),使 $x 在文件任意位置的赋值都能被解析。
		def rec(n):
			if n.type=='variable_assignment':
				nm=n.child_by_field_name('name')
				val=n.child_by_field_name('value')
				if nm is not None and val is not None:
					key='$'+self.txt(nm).strip()
					self.assign[key]=val
			for c in n.children:
				rec(c)
		rec(self.root)

	# ---------- 通用:节点 → 归一化文本 ----------
	def expand(self,n,quoted=True,seen=None):
		if n is None:return ''
		seen=seen or set()
		t=n.type
		# 叶子字面量
		if t=='word':
			return self.txt(n).strip()
		if t in ('number','variable_name','string_content'):
			return self.txt(n).strip()
		# 变量展开 $var / ${var}
		if t in ('simple_expansion','expansion'):
			vn=self._varname_of(n)
			return self.resolve(vn,seen)
		# 双引号字符串:"..."(支持 $var 展开与转义)
		if t=='string':
			inner=self._string_inner(n,seen)
			return ('"%s"'%inner) if quoted else inner
		# 单引号原始串:'...'(shell 不处理转义,但攻击常塞 \\xNN / \\NNN,归一化时还原以暴露隐藏命令)
		if t=='raw_string':
			s=self.txt(n).strip()
			inner=s[1:-1] if (len(s)>=2 and s[0]=="'") else s
			inner=_decode_escapes(inner)
			return ("'%s'"%inner) if quoted else inner
		# 拼接: word$var / "${a}${b}" —— 按字面值拼合并尝试折叠
		if t=='concatenation':
			return ''.join(self.expand(c,quoted=False,seen=seen) for c in n.children if c.is_named)
		# 命令替换 $(cmd) / `cmd`
		if t=='command_substitution':
			inner=self._inner_cmd(n)
			if inner is not None:
				return '$(%s)'%self.command_text(inner,inline=True)
			return self.txt(n).strip()
		# 进程替换 <(cmd) >(cmd)
		if t=='process_substitution':
			inner=self._inner_cmd(n)
			if inner is not None:
				return '<(%s)'%self.command_text(inner,inline=True)
			return self.txt(n).strip()
		# 子 shell ( cmd )
		if t=='subshell':
			for c in n.children:
				if c.type=='command':
					return '( %s )'%self.command_text(c)
			return self.txt(n).strip()
		# 赋值(出现在表达式里时)
		if t=='variable_assignment':
			return self.assignment_text(n)
		# 兜底:原样
		return self.txt(n).strip()

	def _string_inner(self,n,seen):
		parts=[]
		for c in n.children:
			if not c.is_named:continue
			if c.type=='string_content':
				parts.append(self.txt(c))
			else:
				parts.append(self.expand(c,quoted=False,seen=seen))
		inner=''.join(parts)
		# 转义还原:把 \\xNN / \\NNN 还原为可见字符,暴露隐藏命令
		return _decode_escapes(inner)

	def _inner_cmd(self,n):
		"""取命令替换/进程替换内部的 command 节点。"""
		for c in n.children:
			if c.type=='command':
				return c
		return None

	def _varname_of(self,n):
		"""从 simple_expansion / expansion 取回 '$var' 形式的键。"""
		vn=n.child_by_field_name('name')
		if vn is None:
			for c in n.children:
				if c.type=='variable_name':
					vn=c;break
		if vn is None:
			s=self.txt(n).strip()
			return '$'+s.lstrip('$').strip('{}')
		return '$'+self.txt(vn).strip()

	# ---------- 变量解析 ----------
	def resolve(self,var,seen=None):
		"""解析变量:赋值表里若能解析到 字符串/外部输入/调用/另一变量,递归;否则原样。
		quoted=False:返回去引号原始内容,供拼接/命令名上下文使用。"""
		seen=seen or set()
		if var in seen or var not in self.assign:
			return var
		seen=seen|{var}
		node=self.assign[var]
		# 自引用赋值(PATH=/tmp:$PATH)不展开,避免循环/重复展开
		if self._references_var(node,var):
			return var
		return self.expand(node,quoted=False,seen=seen)

	def _references_var(self,n,var):
		"""判断节点子树是否引用了变量 var(用于自引用检测)。"""
		if n is None:return False
		if n.type in ('simple_expansion','expansion') and self._varname_of(n)==var:
			return True
		for c in n.children:
			if self._references_var(c,var):
				return True
		return False

	def _literal(self,s):
		"""若 s 是 'xxx' 或 "xxx",返回去引号内容;否则 None。"""
		s=s.strip()
		if len(s)>=2 and s[0] in ("'",'"') and s[-1]==s[0]:
			return s[1:-1]
		return None

	def _is_cmd_name(self,s):
		return bool(_CMD_RE.match(s.strip()))

	# ---------- 各类语句归一化 ----------
	def command_text(self,n,inline=False):
		nm=n.child_by_field_name('name')  # command_name 节点
		parts=[]
		if nm is not None:
			parts.append(self._cmd_name(nm))
		for a in n.children_by_field_name('argument'):
			parts.append(self.expand(a))
		return ' '.join(p for p in parts if p!='')

	def _cmd_name(self,nm):
		"""命令名解析:若为 $var 动态名且可解析为合法命令名,则替换为真实命令。"""
		child=nm.children[0] if nm.children else nm
		if child.type in ('simple_expansion','expansion'):
			vn=self._varname_of(child)
			r=self.resolve(vn,set())
			lit=self._literal(r)
			if lit is not None and self._is_cmd_name(lit):
				return lit
			if self._is_cmd_name(r):
				return r
			return r  # 解析不出合法命令名,保留动态形式
		return self.txt(child).strip()

	def assignment_text(self,n):
		nm=self.txt(n.child_by_field_name('name')).strip()
		val=n.child_by_field_name('value')
		if val is None:
			return '%s ='%nm
		v=self.expand(val,quoted=True)
		return '%s = %s'%(nm,v)

	def declaration_text(self,n):
		"""export / declare / local / typeset / readonly 等声明命令。
		关键字(export/local 等可能是匿名 token 类型)与可选 flag 拼到赋值前。"""
		prefix=[]
		inner=None
		for c in n.children:
			if c.type=='variable_assignment':
				inner=c;break
			t=self.txt(c).strip()
			if t:
				prefix.append(t)
		kw=' '.join(prefix)
		if inner is not None:
			return '%s %s'%(kw,self.assignment_text(inner))
		return self.txt(n).strip()

	def redirect_text(self,n):
		op=None;dest=None
		for i,c in enumerate(n.children):
			fn=n.field_name_for_child(i)
			if fn=='destination':
				dest=c
			elif not c.is_named:
				op=self.txt(c).strip()
		if dest is not None:
			return ('%s %s'%(op or '',self.expand(dest))).strip()
		return self.txt(n).strip()

	def redirected_text(self,n):
		body=n.child_by_field_name('body')
		redir=n.child_by_field_name('redirect')
		s=self.command_text(body) if body is not None else ''
		if redir is not None:
			s=(' '.join([s,self.redirect_text(redir)])).strip()
		return s

	def pipeline_text(self,n):
		parts=[]
		for c in n.children:
			if not c.is_named:continue
			if c.type=='command':
				parts.append(self.command_text(c))
			elif c.type=='redirected_statement':
				parts.append(self.redirected_text(c))
		return ' | '.join(parts)

	def test_text(self,n):
		parts=[]
		for c in n.children:
			if not c.is_named:continue
			if c.type=='binary_expression':
				parts.append(self.binary_text(c))
			elif c.type=='unary_expression':
				parts.append(self.unary_text(c))
			else:
				parts.append(self.expand(c))
		return '[ '+' '.join(parts)+' ]'

	def binary_text(self,n):
		left=n.child_by_field_name('left')
		op=n.child_by_field_name('operator')
		right=n.child_by_field_name('right')
		lt=self.expand(left) if left else ''
		rt=self.expand(right) if right else ''
		opc=self.txt(op).strip() if op else ''
		return '%s %s %s'%(lt,opc,rt)

	def unary_text(self,n):
		return self.txt(n).strip()

	def function_text(self,n):
		nm=n.child_by_field_name('name')
		name=self.txt(nm).strip() if nm else 'func'
		return 'function %s() { ... }'%name

	# ---------- 遍历发射 ----------
	def _emit(self,n,text):
		"""输出一条归一化语句,并同步记录它对应的原文定位。
		空文本直接丢弃 —— 保证 out_lines 与 locs 严格一一对应,
		调用方正是按索引反查原文行号/偏移的(对称 php/js 的 _emit)。"""
		if not text:return
		self.out_lines.append(text)
		self.locs.append((text,n.start_point.row+1,n.end_point.row+1,n.start_byte,n.end_byte))

	def emit(self,n):
		t=n.type
		if t=='command':
			# 环境变量前缀赋值(FOO=bar cmd)单独成行,便于"恶意变量"规则命中
			for cc in n.children:
				if cc.type=='variable_assignment':
					self._emit(cc,self.assignment_text(cc))
			self._emit(n,self.command_text(n))
		elif t=='variable_assignment':
			self._emit(n,self.assignment_text(n))
		elif t=='redirected_statement':
			self._emit(n,self.redirected_text(n))
		elif t=='pipeline':
			self._emit(n,self.pipeline_text(n))
		elif t=='declaration_command':
			self._emit(n,self.declaration_text(n))
		elif t=='test_command':
			self._emit(n,self.test_text(n))
		elif t=='function_definition':
			# 发射函数头,再递归函数体(体内命令各自带定位)
			self._emit(n,self.function_text(n))
			body=n.child_by_field_name('body')
			if body is not None:
				self.emit_children(body)
		elif t in CONTAINERS:
			self.emit_children(n)
		else:
			self.emit_children(n)

	def emit_children(self,n):
		for c in n.children:
			self.emit(c)

	def normalize(self):
		self.emit_children(self.root)
		return '\n'.join(self.out_lines)


# 容器节点:递归进入其内层语句(不单独作为一条归一化语句发射)
CONTAINERS={'program','list','do_group','compound_statement','subshell',
	'if_statement','while_statement','until_statement','for_statement',
	'case_statement','command_list','brace_group'}


def normalize_source(src):
	"""对 Bash 源码字节/文本做 AST 归一化, 返回归一化等效 Bash 文本(str)。
	解析失败会抛异常(由调用方 bashdect.py 决定回退)。
	"""
	if isinstance(src,str):
		src=src.encode('utf-8')
	root=ts_pack.get_parser(BASH_LANG).parse(src).root_node
	return BashNorm(src,root).normalize()


def normalize_source_with_loc(src):
	"""对 Bash 源码做 AST 归一化, 返回 (纯文本, 定位列表)。
	定位列表每项: {文本,行,行止,偏移起,偏移止}。
	与归一化文本的【行】一一对应:每条归一化语句对应其原始 AST 节点在
	原文件中的行区间 [行,行止] 与字节偏移 [偏移起,偏移止],供研判命中后反查原文位置。
	"""
	if isinstance(src,str):
		src=src.encode('utf-8')
	root=ts_pack.get_parser(BASH_LANG).parse(src).root_node
	norm=BashNorm(src,root)
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
	"""对文件做 AST 归一化, 返回归一化等效 Bash 文本(str)。"""
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
		print('用法: <py> bash_ast_normalize.py <file.sh>')
		sys.exit(1)
	fp=args[0]
	print('===== 归一化文本(暴露更多行为特点的等效 Bash) =====')
	print(normalize(fp))


if __name__=='__main__':
	main()

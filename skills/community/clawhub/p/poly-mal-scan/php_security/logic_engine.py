"""
logic_engine.py —— 自研逻辑判断引擎

背景:单特征码子串匹配只能表达"出现即命中",无法表达"eval 且参数来自超全局"/"解码函数且eval且not base64_encode"这类组合逻辑
本引擎对categories.json的"逻辑规则"键(LOGIC_RULES)求值:
	每条规则含 条件($a and ($b or $c) and not $d) 与 条件字符串({$a:"eval",...});
	先把每个字符串变量对目标代码做子串匹配得布尔值;
	再用递归下降解析条件表达式(支持 and/or/not/括号), 对布尔值做逻辑求值。

纯 Python 实现,无外部依赖;安全:只接受白名单布尔运算,不eval任意代码。

对外接口:
	match_logical_rules(code, rules=None) -> [ {规则,类别,威胁级别,描述,命中变量}, ...]
	eval_one_rule(rule, code) -> (bool, [命中变量])
"""
import re
# ---- 条件表达式词法: $a and ($b or $c) not $d ----
_TOKEN_RE=re.compile(r'\s*(\(|\)|and\b|or\b|not\b|\$\w+)')
def _tokenize(expr):#把条件表达式切成token列表;非法字符报ValueError
	tokens=[]
	pos=0
	while pos<len(expr):
		m=_TOKEN_RE.match(expr,pos)
		if not m:
			chunk=expr[pos:].strip()
			raise ValueError('无法解析的条件表达式片段: %r (在 %r 附近)'%(chunk[:20],expr))
		tok=m.group(1)
		tokens.append(tok)
		pos=m.end()
	return tokens
class _BoolExpr:#布尔表达式类
	def __init__(self,tokens):#递归下降解析求值函数
		self.tokens=tokens
		self.pos=0
	def peek(self):
		return self.tokens[self.pos]if self.pos<len(self.tokens)else None
	def _parse_or(self):
		node=self._parse_and()
		while self.peek()=='or':
			self.pos+=1
			right=self._parse_and()
			node=('or',node,right)
		return node
	def _parse_and(self):
		node=self._parse_not()
		while self.peek()=='and':
			self.pos+=1
			right=self._parse_not()
			node=('and',node,right)
		return node
	def _parse_not(self):
		if self.peek()=='not':
			self.pos+=1
			return ('not',self._parse_not())
		return self._parse_atom()
	def _parse_atom(self):
		tok=self.peek()
		if tok=='(':
			self.pos+=1
			node=self._parse_or()
			if self.peek()!=')':
				raise ValueError('缺少右括号:'+' '.join(self.tokens))
			self.pos+=1
			return node
		if tok and tok.startswith('$')and self.tokens[self.pos].startswith('$'):
			self.pos+=1
			return ('var',tok)
		raise ValueError('意外token: %r'%tok)
	def parse(self):
		node=self._parse_or()
		if self.pos<len(self.tokens):
			raise ValueError('多余token:%r'%self.tokens[self.pos:])
		return node
def _eval_node(node,values):#对解析树求值;values:字符串变量→bool
	op=node[0]
	if op=='var':return values.get(node[1],False)
	if op=='not':return not _eval_node(node[1],values)
	if op=='and':return _eval_node(node[1],values)and _eval_node(node[2],values)
	if op=='or':return _eval_node(node[1],values)or _eval_node(node[2],values)
	return False
def _norm_ws(s):#空白归一化:删除所有空白字符(空格/tab/换行/\r/\f/\v)。用于特征值匹配,使'eval ($_POST'这类"空白绕过"失效——PHP中这些位置的空白在语法上可省略,删除后检测目标不变,但绕过的空格被抹平。注意:仅用于匹配,不改变原文本;字符串字面量内空白被删是可接受的权衡(检测只关心代码结构)。
	return re.sub(r'\s+','',s)
def _match_val(val,code):#特征值val是否命中代码code(空白容忍)。优先精确子串匹配(快);不中时退化为去空白后的子串匹配(抗空格绕过)。
	if val in code:return True
	# 精确不中→去空白再比(自身有空白也归一, 保证一致性)
	return _norm_ws(val)in _norm_ws(code)
def eval_one_rule(rule,code):#对单条逻辑规则求值:返回(是否命中,命中的字符串变量列表)
	expr=rule.get('条件','')
	str_map=rule.get('条件字符串',{})
	if not expr or not str_map:
		return False,[]
	# 防御空值: 任一特征值为空串/非字符串 → 规则无效(避免 '' 恒真/not 退化)
	for var,val in str_map.items():
		if not isinstance(val,str) or val=='':
			return False,[]
	# 1) 对每个字符串变量做空白容忍子串匹配
	values={}
	hit_vars=[]
	for var,val in str_map.items():
		hit=_match_val(val,code)
		values[var]=hit
		if hit:
			hit_vars.append(var)
	# 2) 解析条件并求值
	try:
		tokens=_tokenize(expr)
		tree=_BoolExpr(tokens).parse()
		result=_eval_node(tree,values)
	except (ValueError,IndexError):
		return False,[]  # 条件表达式非法 → 不作为命中
	return result,hit_vars
def match_logical_rules(code,rules=None,detect_rules_module=None):#对代码文本跑全部逻辑规则,返回命中列表(JSON兼容)。规则默认来自detect_rules.LOGIC_RULES(避免循环import,延迟导入)。
	if rules is None:
		if detect_rules_module is not None:
			rules=detect_rules_module.LOGIC_RULES
		else:
			try:
				import detect_rules
				rules=detect_rules.LOGIC_RULES
			except Exception:
				rules=[]
	out=[]
	for r in rules or []:
		if not isinstance(r,dict):
			continue
		hit,hit_vars=eval_one_rule(r,code)
		if hit:
			out.append({
				"规则":r.get('id',''),
				"类别":r.get('类别',''),
				"威胁级别":r.get('威胁级别',4),
				"描述":r.get('描述',''),
				"命中变量":hit_vars,
			})
	return out

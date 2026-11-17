#-*- coding:utf-8 -*-
"""
js_logic_engine.py —— JS: 自研逻辑判断引擎(模仿 yara 的 and/or/not 组合, 不依赖 yara 库)

对称于 php_security/logic_engine.py。对 js_categories.json 的"逻辑规则"键(LOGIC_RULES)求值:
  - 每条规则含 条件($a and ($b or $c)) 与 条件字符串({$a:"eval",...});
  - 先把每个字符串变量对目标代码做子串匹配得布尔值;
  - 再用递归下降解析条件表达式(支持 and/or/not/括号), 对布尔值做逻辑求值。

纯 Python 实现, 无外部依赖; 安全: 只接受白名单布尔运算, 不 eval 任意代码。

对外接口:
  match_logical_rules(code, rules=None) -> [ {规则,类别,威胁级别,描述,命中变量}, ...]
"""
import re
_TOKEN_RE=re.compile(r'\s*(\(|\)|and\b|or\b|not\b|\$\w+)')
def _tokenize(expr):
	tokens=[]
	pos=0
	while pos<len(expr):
		m=_TOKEN_RE.match(expr,pos)
		if not m:
			raise ValueError('无法解析的条件表达式片段: %r'%expr[pos:].strip()[:20])
		tokens.append(m.group(1))
		pos=m.end()
	return tokens
class _BoolExpr:
	def __init__(self,tokens):
		self.tokens=tokens
		self.pos=0
	def peek(self):
		return self.tokens[self.pos]if self.pos<len(self.tokens)else None
	def _parse_or(self):
		node=self._parse_and()
		while self.peek()=='or':
			self.pos+=1; node=('or',node,self._parse_and())
		return node
	def _parse_and(self):
		node=self._parse_not()
		while self.peek()=='and':
			self.pos+=1; node=('and',node,self._parse_not())
		return node
	def _parse_not(self):
		if self.peek()=='not':
			self.pos+=1; return ('not',self._parse_not())
		return self._parse_atom()
	def _parse_atom(self):
		tok=self.peek()
		if tok=='(':
			self.pos+=1; node=self._parse_or()
			if self.peek()!=')': raise ValueError('缺少右括号')
			self.pos+=1; return node
		if tok and tok.startswith('$'):
			self.pos+=1; return ('var',tok)
		raise ValueError('意外 token: %r'%tok)
	def parse(self):
		node=self._parse_or()
		if self.pos<len(self.tokens): raise ValueError('多余 token: %r'%self.tokens[self.pos:])
		return node
def _eval_node(node,values):
	op=node[0]
	if op=='var': return values.get(node[1],False)
	if op=='not': return not _eval_node(node[1],values)
	if op=='and': return _eval_node(node[1],values) and _eval_node(node[2],values)
	if op=='or':  return _eval_node(node[1],values) or  _eval_node(node[2],values)
	return False
def _match_val(val,code):#特征值val是否命中代码code(空白容忍)。优先精确子串匹配;不中时去空白再比(抗空格绕过,对称php logic_engine)。
	if val in code:
		return True
	return re.sub(r'\s+','',val) in re.sub(r'\s+','',code)
def eval_one_rule(rule,code):#对单条逻辑规则求值:返回(是否命中,命中的字符串变量列表)
	expr=rule.get('条件','')
	str_map=rule.get('条件字符串',{})
	if not expr or not str_map:
		return False,[]
	# 防御空值: 任一特征值为空串/非字符串 → 规则无效(避免 '' in code 恒真致 not 退化)
	for var,val in str_map.items():
		if not isinstance(val,str) or val=='':
			return False,[]
	values={}; hit_vars=[]
	for var,val in str_map.items():
		hit=_match_val(val,code)
		values[var]=hit
		if hit: hit_vars.append(var)
	try:
		tokens=_tokenize(expr)
		result=_eval_node(_BoolExpr(tokens).parse(),values)
	except (ValueError,IndexError):
		return False,[]
	return result,hit_vars
def match_logical_rules(code,rules=None,detect_rules_module=None):
	if rules is None:
		if detect_rules_module is not None:
			rules=detect_rules_module.LOGIC_RULES
		else:
			try:
				import js_detect_rules
				rules=js_detect_rules.LOGIC_RULES
			except Exception:
				rules=[]
	out=[]
	for r in rules or []:
		if not isinstance(r,dict):
			continue
		#作用域:默认「文件」(整段代码同现即可);设为「语句」时要求条件在同一代码行内同现,避免「文件写入」与「外部输入」在文件不同处各出现一次就被误判(正常代码常见此写法)。
		scope=r.get('作用域','文件')
		if scope=='语句':
			hit,hit_vars=False,[]
			for line in code.split('\n'):
				h,hv=eval_one_rule(r,line)
				if h:
					hit,hit_vars=True,hv
					break
		else:
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
if __name__=='__main__':
	import js_detect_rules
	for t in ("eval(atob('x'));",
			  "require('child_process').execSync(process.env.CMD);",
			  "x.innerHTML=location.hash;",
			  "console.log('hi');"):
		hits=match_logical_rules(t,detect_rules_module=js_detect_rules)
		print(repr(t[:36]), '->', [h['规则'] for h in hits] or '无命中')

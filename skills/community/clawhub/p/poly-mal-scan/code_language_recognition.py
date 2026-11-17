'''
代码语言识别器：用于推测文件使用了什么语言，有可能没有代码在其中
以此来告知后续程序该使用什么组件
'''
#!/usr/bin/env python3
import sys,os
from tree_sitter_language_pack import get_parser
LANGS=["php","javascript","html","css","sql","json","vue"]
PARSERS={l:get_parser(l) for l in LANGS}
def ast_ok(p,src):#该语言AST能否无错解析
	try:
		t=p.parse(src)
		return t is not None and not t.root_node.has_error
	except Exception:
		return False
def scan(fp):#返回各语言组件启用字典
	if len(sys.argv)<2 or not os.path.isfile(fp):return {l:False for l in LANGS}|{"no_code":True}
	try:
		src=open(fp,'rb').read()
	except Exception:
		return {l:False for l in LANGS}|{"no_code":True}
	if not src.strip():return {l:False for l in LANGS}|{"no_code":True}
	# 探测各语言AST
	res={l:ast_ok(PARSERS[l],src) for l in LANGS}
	# 无代码判定：所有语言AST均失败且长度很短（<16字节）视为无代码
	no_code=not any(res.values()) and len(src)<16
	res["no_code"]=no_code
	return res
if __name__=='__main__':
	import json
	print(json.dumps(scan(sys.argv[1]),indent=2))

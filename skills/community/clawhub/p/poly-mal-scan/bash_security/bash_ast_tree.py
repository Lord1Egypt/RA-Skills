#-*- coding:utf-8 -*-
"""
bash_ast_tree.py —— Bash 语法树建立脚本(最初步,对称于 php_ast_tree.py / js_ast_tree.py)

用途:用 tree-sitter(bash 语言)对 Linux shell 脚本建立语法树,并打印遍历结构,
验证解析器可用、观察 node 类型/文本/行列位置。
这是 Bash 侧后续(AST → 行为模型 → 复用正则组件)的第一步,暂不做任何恶意判定。

依赖:tree_sitter_language_pack(mainwork3_12_13 环境已安装)
用法:
	<mainwork3_12_13 python> bash_ast_tree.py <file.sh> [--depth N] [--no-text]
运行示例:
	~/.pyenv/versions/3.12.13/envs/mainwork3_12_13/bin/python bash_ast_tree.py <file.sh>
"""
import sys
import tree_sitter_language_pack as ts_pack

BASH_LANG='bash'#tree_sitter_language_pack里 bash 的语言名为 bash

def build_tree(file_path):#读取文件并用tree-sitter解析,返回(bytes源码,tree)
	with open(file_path,'rb') as f:
		source=f.read()
	parser=ts_pack.get_parser(BASH_LANG)
	tree=parser.parse(source)
	return source,tree

def walk(node,source,depth,max_depth,show_text):#递归输出节点:类型+行列+(可选)文本片段
	sp,ep=node.start_point,node.end_point
	label=f"{node.type} [{sp.row+1}:{sp.column}-{ep.row+1}:{ep.column}]"
	print('  '*depth+label)
	if show_text and node.child_count==0 and ep.row==sp.row:
		txt=source[node.start_byte:node.end_byte].decode('utf-8','ignore')
		print('  '*(depth+1)+'text='+repr(txt[:60]))
	if max_depth is not None and depth>=max_depth:return
	for child in node.children:walk(child,source,depth+1,max_depth,show_text)

def main():
	args=sys.argv[1:]
	if not args:print('用法: <py> bash_ast_tree.py <file.sh> [--depth N] [--no-text]');sys.exit(1)
	file_path=args[0]
	max_depth=None;show_text=True
	i=1
	while i<len(args):
		if args[i]=='--depth' and i+1<len(args):max_depth=int(args[i+1]);i+=2
		elif args[i]=='--no-text':show_text=False;i+=1
		else:i+=1
	source,tree=build_tree(file_path)
	root=tree.root_node
	print(f"文件: {file_path}")
	print(f"源码字节数: {len(source)}")
	print(f"根节点类型: {root.type}")
	print(f"错误节点数: {root.has_error} (True=存在解析错误)")
	print('---- 语法树 ----')
	walk(root,source,0,max_depth,show_text)

if __name__=='__main__':
	main()

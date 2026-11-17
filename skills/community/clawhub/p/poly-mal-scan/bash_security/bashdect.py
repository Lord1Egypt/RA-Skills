# -*- coding: utf-8 -*-
"""
bashdect.py —— Bash 恶意代码检测器(主程序/调度器),对称于 php_security/phpdect.py。

把【规则层(bash_detect_rules)】与【AST 归一化层(bash_ast_normalize)】连起来:
1. 用 tree-sitter 把源码归一化为易识别的等效代码,并记录每条语句的原文位置(行/字节偏移);
2. 对归一化等效代码(及原始源码行)跑正则层各检测模块:
   特征码威胁 / 恶意命令 / 恶意变量 / 恶意文件写入 / 自我复制 / 恶意函数;
3. 汇总为统一 JSON 文档;支持多文件及 (source / . ) 静态包含递归。

五大威胁类别对应的 JSON 键:
"恶意命令" / "恶意变量" / "恶意文件写入" / "自我复制" / "恶意函数"
以及由多编码特征码产生的 "特征码威胁"。

设计要点:正则层主要作用在【AST 归一化后的等效代码】上——
归一化已做常量折叠、变量解析、命令替换摊平、转义还原,故混淆/拼接/动态命令名
被揭开后,正则规则更易命中;命中后再用 locs 反查回原始源码的精确位置。
"""
import os, sys, json, re

from bash_detect_rules import (
	THREAT_FUNCS, MALICIOUS_COMMANDS, COMMANDS_BY_NAME,
	MALICIOUS_VARIABLES, FILE_WRITE_RULES, SELF_REPLICATE_RULES,
	MULTI_ENC_TRAITS,
)
from bash_common import readfile_bintoutf8_to_list
from bash_trait_dect import scan_traits, scan_traits_raw
from bash_threat_func_dect import scan_threat_funcs
from bash_cmd_dect import scan_malicious_commands
from bash_var_dect import scan_malicious_vars
from bash_file_write_dect import scan_file_writes
from bash_self_replicate_dect import scan_self_replicate

# ---- AST 归一化层(可选依赖) ----
try:
	from bash_ast_normalize import normalize_source_with_loc as _ast_normalize_with_loc
	_AST_AVAILABLE = True
except Exception:
	_ast_normalize_with_loc = None
	_AST_AVAILABLE = False

# 统一的威胁分类(JSON 键)
THREAT_KEYS = ["恶意命令", "恶意变量", "恶意文件写入", "自我复制", "恶意函数", "特征码威胁"]


def _dedup(items, keyfn):
	"""按 keyfn 去重,保留首次出现。"""
	seen = set()
	res = []
	for it in items:
		k = keyfn(it)
		if k in seen:
			continue
		seen.add(k)
		res.append(it)
	return res


def _run_structured(line, loc, threats):
	"""对单行(归一化等效代码)跑全部结构化检测模块,结果并入 threats。"""
	threats["恶意函数"] += scan_threat_funcs(line, loc, THREAT_FUNCS)
	threats["恶意命令"] += scan_malicious_commands(line, loc, COMMANDS_BY_NAME)
	threats["恶意变量"] += scan_malicious_vars(line, loc, MALICIOUS_VARIABLES)
	threats["恶意文件写入"] += scan_file_writes(line, loc, FILE_WRITE_RULES)
	threats["自我复制"] += scan_self_replicate(line, loc, SELF_REPLICATE_RULES)
	threats["特征码威胁"] += scan_traits(line, loc, MULTI_ENC_TRAITS)


def _collect_includes(raw_lines):
	"""从原始行收集静态 source / . 包含(供递归扫描)。排除 ./ 相对执行与动态($/)目标。"""
	static_includes = []
	for raw in raw_lines:
		for m in re.finditer(r'(?:^|\s)(?:source|\.)\s+([^\s|&;()]+)', raw):
			tgt = m.group(1)
			if tgt.startswith(('/', './', '$', '~', '-')):
				continue
			static_includes.append(tgt)
	return static_includes


def bashfile_threatening_dect(file_path):
	"""扫描单个 Bash 文件,返回完整 JSON 兼容文档(dict)。"""
	threats = {key: [] for key in THREAT_KEYS}
	raw_lines = readfile_bintoutf8_to_list(file_path)

	# ---- AST 归一化(主路径) ----
	ast_text, locs = '', []
	if _AST_AVAILABLE:
		try:
			with open(file_path, 'rb') as f:
				ast_text, locs = _ast_normalize_with_loc(f.read())
		except Exception:
			ast_text, locs = '', []

	if ast_text:
		lines = ast_text.split('\n')
		for i, line in enumerate(lines):
			if not line.strip():
				continue
			loc = locs[i] if i < len(locs) else None
			_run_structured(line, loc, threats)
	else:
		# 回退:直接对原始行扫描(无精确字节偏移,仅有行号)
		for n, raw in enumerate(raw_lines, start=1):
			loc = {'行': n, '行止': n, '偏移起': -1, '偏移止': -1}
			_run_structured(raw, loc, threats)

	# ---- 原始行特征码补全(去重,避免 AST 变换遗漏编码载荷) ----
	for n, raw in enumerate(raw_lines, start=1):
		threats["特征码威胁"] += scan_traits_raw(raw, n, MULTI_ENC_TRAITS)
	threats["特征码威胁"] = _dedup(
		threats["特征码威胁"],
		lambda e: (e.get('特征码'), e.get('编码'), e.get('行')),
	)

	static_includes = _collect_includes(raw_lines)

	result = {
		"文件": file_path,
		"是否有威胁": any(threats[k] for k in THREAT_KEYS),
		"包含文件": static_includes,
		"威胁": threats,
	}
	return result


def scan_to_json(start_file_path='sample.sh', recursive=True):
	"""扫描一个/多个 Bash 文件(可递归收集静态 source 包含),返回 JSON 兼容的 dict 列表。"""
	if isinstance(start_file_path, str):
		filepath_list = [start_file_path]
	else:
		filepath_list = list(start_file_path)

	scanned = set()
	result_files = []

	def scan_one(the_file_path, is_entry=False):
		if the_file_path in scanned and not is_entry:
			return
		is_dup = the_file_path in scanned
		scanned.add(the_file_path)
		try:
			raw = bashfile_threatening_dect(the_file_path)
		except Exception as e:
			raw = {
				"文件": the_file_path,
				"是否有威胁": False,
				"包含文件": [],
				"威胁": {key: [] for key in THREAT_KEYS},
				"错误": str(e),
			}
		result_files.append(raw)
		if recursive and not is_dup:
			for inc in raw.get("包含文件", []):
				inc_path = os.path.normpath(
					os.path.join(os.path.dirname(the_file_path) or '.', inc))
				if os.path.isfile(inc_path):
					scan_one(inc_path)

	for fp in filepath_list:
		scan_one(fp, is_entry=True)
	return result_files


if __name__ == '__main__':
	args = sys.argv[1:]
	if not args:
		args = ['sample.sh']
	out = scan_to_json(args)
	print(json.dumps(out, ensure_ascii=False, indent=2))

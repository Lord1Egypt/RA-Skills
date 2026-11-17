# -*- coding: utf-8 -*-
"""
bash_self_replicate_dect.py —— 威胁类别:自我复制 检测模块。

扫描一行(归一化等效代码)中"将脚本自身($0 / $BASH_SOURCE)复制到新路径/持久化位置"的行为。
规则数据来自 bash_self_replicate.json:源特征(自身变量) + 命令特征(cp/cat/tee/dd/curl) + 目标路径特征。

判定逻辑(逐条规则):源特征命中 且 命令特征命中 且 目标路径特征命中(某项特征为空则视为满足)。

对外接口:
  scan_self_replicate(line, loc, self_replicate_rules) -> [条目,...]
"""
from bash_common import attach_loc


def scan_self_replicate(line, loc, self_replicate_rules):
	out = []
	for r in self_replicate_rules:
		src = r.get('源特征', []) or []
		cmds = r.get('命令特征', []) or []
		tgts = r.get('目标路径特征', []) or []

		src_hit = any(s and s in line for s in src) if src else False
		cmd_hit = any(c and c in line for c in cmds) if cmds else True
		tgt_hit = any(t and t in line for t in tgts) if tgts else True

		if not (src_hit and cmd_hit and tgt_hit):
			continue

		hit_feats = []
		if src:
			hit_feats += ['源特征:%s' % s for s in src if s and s in line]
		if cmds:
			hit_feats += ['命令特征:%s' % c for c in cmds if c and c in line]
		if tgts:
			hit_feats += ['目标路径特征:%s' % t for t in tgts if t and t in line]

		e = {
			'威胁类型': '自我复制',
			'规则ID': r.get('id'),
			'名称': r.get('名称'),
			'命中特征': hit_feats,
			'威胁级别': r.get('级别', 3),
			'描述': r.get('描述', ''),
			'参考': r.get('参考', ''),
			'归一化内容': line.strip(),
		}
		attach_loc(e, loc)
		out.append(e)
	return out

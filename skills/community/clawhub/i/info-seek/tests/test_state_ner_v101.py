#!/usr/bin/env python3
"""Infoseek v1.0.1 补充测试：state_dir + ner（G7）

state_dir: 运行时数据目录解析（env 覆盖 / 默认 / 子目录）
ner: 命名实体识别（词典匹配 / 类别过滤 / 覆盖度 / 边界）
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

passed, failed = [], []

def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


# ═══════════════════════════════════════════════════════════════
# SD: state_dir
# ═══════════════════════════════════════════════════════════════
print("\n═══ state_dir 测试 ═══")

import state_dir as sd

# SD1: 默认数据目录（无 env → ~/.infoseek 或等效）
orig_env = {k: os.environ.get(k) for k in
            ('INFOSEEK_DATA_DIR', 'INFOSEEK_DB', 'INFOSEEK_ARCHIVE')}
for k in orig_env:
    os.environ.pop(k, None)
# 重新加载模块以重置缓存（若模块缓存了常量）
import importlib
sd = importlib.reload(sd)
d = sd.get_data_dir()
check('SD1 默认数据目录可解析', isinstance(d, Path) and str(d).endswith('.infoseek'), f"dir={d}")

# SD2: env 覆盖
tmp = tempfile.mkdtemp()
os.environ['INFOSEEK_DATA_DIR'] = tmp
sd = importlib.reload(sd)
check('SD2 env 覆盖数据目录', str(sd.get_data_dir()) == tmp)

# SD3: state_path 拼接
p = sd.state_path('test.json')
check('SD3 state_path 落在数据目录', str(p).startswith(tmp) and p.name == 'test.json', f"p={p}")

# SD4: get_db_path env 覆盖
os.environ['INFOSEEK_DB'] = str(Path(tmp) / 'custom_db.json')
sd = importlib.reload(sd)
check('SD4 db 路径 env 覆盖', str(sd.get_db_path()).endswith('custom_db.json'))

# SD5: get_archives_dir env 覆盖
os.environ['INFOSEEK_ARCHIVE'] = str(Path(tmp) / 'archives')
sd = importlib.reload(sd)
check('SD5 归档目录 env 覆盖', str(sd.get_archives_dir()).endswith('archives'))

# 恢复 env
for k, v in orig_env.items():
    if v is None:
        os.environ.pop(k, None)
    else:
        os.environ[k] = v

# ═══════════════════════════════════════════════════════════════
# NE: ner
# ═══════════════════════════════════════════════════════════════
print("\n═══ ner 测试 ═══")

from ner import extract_entities, extract_by_category, has_entity, entity_coverage

# NE1: 中文实体识别
ents = extract_entities('OpenAI 宣布 GPT-5 开源，宁德时代发布财报')
names = {e['entity_name'] for e in ents}
check('NE1 中文实体识别', 'OpenAI' in names and '宁德时代' in names, f"names={sorted(names)[:4]}")

# NE2: 实体类型字段
e0 = next((e for e in ents if e['entity_name'] == 'OpenAI'), None)
check('NE2 实体类型字段', e0 is not None and e0.get('entity_type') == 'AI',
      f"type={e0.get('entity_type') if e0 else '?'}")

# NE3: 空文本
check('NE3 空文本返回空列表', extract_entities('') == [])

# NE4: 无关文本不误识别
check('NE4 无关文本零命中', extract_entities('今天天气不错，出门散步') == [])

# NE5: 类别过滤
fin = extract_entities('宁德时代发布财报', entity_types=['AUTO'])
check('NE5 类别过滤', all(e['entity_type'] == 'AUTO' for e in fin) and len(fin) >= 1,
      f"count={len(fin)}")

# NE6: 别名归并（OpenAI Inc. → OpenAI）
ents6 = extract_entities('OpenAI Inc. 发布新模型，OpenAI 回应')
names6 = {e['entity_name'] for e in ents6}
check('NE6 别名归并', 'OpenAI' in names6, f"names={sorted(names6)[:4]}")

# NE7: has_entity
check('NE7 has_entity 命中', has_entity('腾讯发布财报', '腾讯') is True)
check('NE7b has_entity 未命中', has_entity('苹果是水果', '腾讯') is False)

# NE8: entity_coverage
cov = entity_coverage('OpenAI 和腾讯合作', ['OpenAI', '腾讯'])
check('NE8 实体覆盖度', cov == 1.0, f"cov={cov}")
cov2 = entity_coverage('只有 OpenAI', ['OpenAI', '腾讯'])
check('NE8b 部分覆盖', abs(cov2 - 0.5) < 1e-6, f"cov={cov2}")

# NE9: 大小写不敏感
check('NE9 大小写不敏感', has_entity('openai 发布', 'OpenAI') is True)

print(f"\n=== state_dir+ner 测试: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")

from __future__ import annotations
import json, os, tempfile, unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import mosobleirc as cli

class RuntimeConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/'config').mkdir()
    def test_runtime_config_resolves_external_inventory_and_relay(self):
        inv=self.root/'private-inventory.json'; inv.write_text('[]',encoding='utf-8')
        cfg={'inventory_path':str(inv),'function_url':'https://example.invalid/relay'}
        (self.root/'config'/'runtime.json').write_text(json.dumps(cfg),encoding='utf-8')
        p=cli.build_parser(); a=p.parse_args(['--data-root',str(self.root),'status'])
        cli._resolve_runtime_args(a)
        self.assertEqual(a.inventory,inv)
        self.assertEqual(a.function_url,'https://example.invalid/relay')
    def test_env_overrides_runtime_config(self):
        (self.root/'config'/'runtime.json').write_text(json.dumps({'inventory_path':'A','function_url':'B'}),encoding='utf-8')
        old_i=os.environ.get('MOSOBLEIRC_INVENTORY'); old_u=os.environ.get('MOSOBLEIRC_FUNCTION_URL')
        os.environ['MOSOBLEIRC_INVENTORY']=str(self.root/'env-inventory.json')
        os.environ['MOSOBLEIRC_FUNCTION_URL']='https://env.invalid/relay'
        self.addCleanup(lambda: os.environ.__setitem__('MOSOBLEIRC_INVENTORY',old_i) if old_i is not None else os.environ.pop('MOSOBLEIRC_INVENTORY',None))
        self.addCleanup(lambda: os.environ.__setitem__('MOSOBLEIRC_FUNCTION_URL',old_u) if old_u is not None else os.environ.pop('MOSOBLEIRC_FUNCTION_URL',None))
        p=cli.build_parser(); a=p.parse_args(['--data-root',str(self.root),'status'])
        cli._resolve_runtime_args(a)
        self.assertEqual(a.inventory,self.root/'env-inventory.json')
        self.assertEqual(a.function_url,'https://env.invalid/relay')
    def test_skill_tree_has_no_production_runtime_files(self):
        self.assertFalse((ROOT/'config'/'inventory.json').exists())
        self.assertFalse((ROOT/'config'/'runtime.json').exists())
        source=(ROOT/'scripts'/'mosobleirc.py').read_text(encoding='utf-8')
        self.assertNotIn('functions.yandexcloud.net/',source)

if __name__=='__main__':
    unittest.main(verbosity=2)

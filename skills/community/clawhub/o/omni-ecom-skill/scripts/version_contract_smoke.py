"""Version identity checks use isolated candidate metadata copies."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from version_contract_guard import validate_version_contract

ROOT=Path(__file__).resolve().parents[1]


class VersionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for name in ('version-info.json','SKILL.md','README.md'):
            shutil.copy2(ROOT/name,self.root/name)
        (self.root/'.codebuddy-plugin').mkdir(); shutil.copy2(ROOT/'.codebuddy-plugin'/'plugin.json',self.root/'.codebuddy-plugin'/'plugin.json')
        (self.root/'agents').mkdir(); shutil.copy2(ROOT/'agents'/'omni-ecom-team-lead.md',self.root/'agents'/'omni-ecom-team-lead.md')

    def write(self,path,value): path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')

    def test_actual_release_identity_is_consistent(self):
        result=validate_version_contract(ROOT)
        self.assertRegex(result['team_version'],r'^2\.0\.3(?:-candidate\.[1-9][0-9]*)?$')
        self.assertEqual(result['release_ready'],result['release_status']=='released')

    def test_formal_directory_is_releasable(self):
        from release_guard import validate
        result=validate(ROOT)
        if '-candidate.' in json.loads((ROOT/'version-info.json').read_text(encoding='utf-8'))['team_version']:
            self.assertEqual(result['status'],'FAIL',result)
            self.assertIn('release_not_ready',result['errors'])
        else:
            self.assertEqual(result['status'],'PASS',result)

    def test_plugin_cannot_keep_old_or_claim_newer_version(self):
        path=self.root/'.codebuddy-plugin'/'plugin.json'; value=json.loads(path.read_text(encoding='utf-8'))
        for version in ('1.6.0','2.0.4','2.0.3-candidate.99'):
            with self.subTest(version=version):
                value['version']=version; self.write(path,value)
                with self.assertRaisesRegex(ValueError,'plugin_version_drift'): validate_version_contract(self.root)

    def test_candidate_cannot_set_release_ready_or_release_date(self):
        path=self.root/'version-info.json'; value=json.loads(path.read_text(encoding='utf-8'))
        value.update(team_version='2.0.3-candidate.1',release_status='candidate',release_ready=False,release_date=None)
        for update in ({'release_ready':True},{'release_date':'2026-09-08'},{'release_status':'released'}):
            with self.subTest(update=update):
                altered=dict(value,**update); self.write(path,altered)
                with self.assertRaisesRegex(ValueError,'candidate_metadata_invalid|released_metadata_invalid'):
                    validate_version_contract(self.root)

    def test_previous_version_and_visible_identity_cannot_drift(self):
        path=self.root/'version-info.json'; value=json.loads(path.read_text(encoding='utf-8'))
        value['previous_version']='1.5.13'; self.write(path,value)
        with self.assertRaisesRegex(ValueError,'version_lineage_invalid'): validate_version_contract(self.root)
        value['previous_version']='2.0.2'; self.write(path,value)
        skill=self.root/'SKILL.md'; skill.write_text(skill.read_text(encoding='utf-8').replace('2.0.3','9.9.9'),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'visible_version_drift'): validate_version_contract(self.root)


if __name__=='__main__': unittest.main()

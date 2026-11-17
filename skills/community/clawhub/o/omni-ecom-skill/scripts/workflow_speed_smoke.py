"""Synthetic safety and efficiency checks; not native host acceptance."""
import hashlib
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch
import prepare_agent_task_cards as cards
from analysis_work_plan import plan
from workflow_progress import snapshot
from host_runtime import Runtime


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


class WorkflowSpeedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.identity = dict(run_id='speed-test', client_scope='same-client', team_version='2.0.3')
        write(self.root/'team-bootstrap.json', dict(self.identity, host='workbuddy', status='team_created'))
        write(self.root/'baseline-pack.json', dict(self.identity, scope='same-client period'))
        self.inventory = dict(self.identity, reports=[dict(report_id='R001', file_path='source.csv'),
                                                     dict(report_id='R002', file_path='other.csv')])
        self.chapters = [dict(chapter_id='CH1', owner_agent='data-analyst', source_report_ids=['R001']),
                         dict(chapter_id='CH2', owner_agent='platform-ops', source_report_ids=['R001','R002'])]
        write(self.root/'chapter-plan.json', dict(self.identity, chapters=self.chapters))
        write(self.root/'report-inventory.json', self.inventory)
        self.args = Namespace(run_dir=str(self.root), plugin_dir=str(self.root), baseline=None,
            chapter_plan=None, inventory=None, host='workbuddy', attempt='a1', roles=None)

    def test_each_shared_input_read_once_and_all_roles_preserved(self):
        with patch.object(cards, 'load_json', wraps=cards.load_json) as reads:
            result = cards.analysis_cards(self.args)
        self.assertEqual(reads.call_count, 4)  # identity + three shared files, once each.
        self.assertEqual(len(result['cards']), 4)
        for c in result['cards']:
            body = cards.load_json(Path(c['card_path']))
            self.assertFalse(body['analysis_work_plan']['expert_findings_generated'])
            self.assertEqual(body['analysis_work_plan']['all_inventory_report_ids'], ['R001','R002'])
            self.assertEqual(body['raw_handoff_template']['facts'], [])

    def test_source_routing_keeps_shared_report_and_rejects_unlisted_source(self):
        p = plan('data-analyst', self.chapters, self.inventory)
        self.assertEqual(p['shared_source_ids'], ['R001'])
        self.assertEqual(p['primary_sources'][0]['report_id'], 'R001')
        self.chapters[0]['source_report_ids'].append('R999')
        with self.assertRaisesRegex(ValueError, 'not_in_inventory'):
            plan('data-analyst', self.chapters, self.inventory)

    def test_cross_client_shared_packet_rejected_before_cards_written(self):
        write(self.root/'report-inventory.json', dict(self.inventory, client_scope='other-client'))
        with self.assertRaisesRegex(ValueError, 'identity_mismatch'):
            cards.analysis_cards(self.args)
        self.assertFalse((self.root/'task-cards').exists())

    def test_initial_comprehensive_dispatch_cannot_drop_members(self):
        self.args.roles = ['data-analyst']
        with self.assertRaisesRegex(ValueError, 'requires_all_roles'):
            cards.analysis_cards(self.args)

    def runtime(self):
        rt = Runtime(self.root, 'speed-test', 'same-client')
        rt.init('2.0.3', 'weekly_report')
        self.addCleanup(rt.close)
        obs = dict(run_id='speed-test', client_scope='same-client', host='workbuddy',
            task_id='agent-speed-original', state='running', evidence_kind='synthetic_fixture')
        write(self.root/'start.json', obs)
        rt.start('data-analyst','workbuddy','agent-speed-original','a1','start.json')
        return rt, obs

    def test_waiting_task_cannot_receive_retry_and_progress_is_read_only(self):
        rt, _ = self.runtime()
        self.args.attempt='a2'; self.args.roles=['data-analyst']
        with self.assertRaisesRegex(ValueError, 'terminal_failure'):
            cards.analysis_cards(self.args)
        before = hashlib.sha256((self.root/'run-journal.sqlite').read_bytes()).hexdigest()
        result = snapshot(self.root, 'speed-test', 'same-client')
        after = hashlib.sha256((self.root/'run-journal.sqlite').read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertFalse(result['current_completion_authority'])
        self.assertEqual(result['members'][0]['task_id'], 'agent-speed-original')
        self.assertEqual(result['members'][0]['next_step'], 'query_original_task')

    def test_only_recorded_failed_role_gets_a2_card(self):
        rt, obs = self.runtime()
        write(self.root/'failed.json', dict(obs, state='failed'))
        rt.fail('data-analyst','workbuddy','agent-speed-original','a1','failed.json')
        self.args.attempt='a2'; self.args.roles=['data-analyst']
        result = cards.analysis_cards(self.args)
        self.assertEqual([x['agent_id'] for x in result['cards']], ['data-analyst'])
        self.assertEqual(snapshot(self.root,'speed-test','same-client')['members'][0]['next_step'],
                         'verify_and_launch_prepared_a2_once')
        self.assertEqual(rt.status()['members'][0]['state'], 'member_failed')

    def test_retry_without_explicit_failed_roles_is_rejected(self):
        self.args.attempt='a2'
        with self.assertRaisesRegex(ValueError, 'explicit_failed_roles'):
            cards.analysis_cards(self.args)

    def test_changed_failure_observation_cannot_authorize_retry(self):
        rt, obs = self.runtime()
        write(self.root/'failed.json', dict(obs, state='failed'))
        rt.fail('data-analyst','workbuddy','agent-speed-original','a1','failed.json')
        write(self.root/'failed.json', dict(obs, state='running'))
        self.args.attempt='a2'; self.args.roles=['data-analyst']
        with self.assertRaisesRegex(ValueError, 'observation_changed'):
            cards.analysis_cards(self.args)
        with self.assertRaisesRegex(ValueError, 'observation_changed'):
            snapshot(self.root,'speed-test','same-client')

    def test_two_failed_roles_can_prepare_a2_in_separate_batches(self):
        rt, obs = self.runtime()
        write(self.root/'failed.json', dict(obs, state='failed'))
        rt.fail('data-analyst','workbuddy','agent-speed-original','a1','failed.json')
        other = dict(obs, task_id='agent-other')
        write(self.root/'other-start.json',other)
        rt.start('platform-ops','workbuddy','agent-other','a1','other-start.json')
        write(self.root/'other-failed.json',dict(other,state='failed'))
        rt.fail('platform-ops','workbuddy','agent-other','a1','other-failed.json')
        self.args.attempt='a2'; self.args.roles=['data-analyst']
        first = cards.analysis_cards(self.args)
        self.args.roles=['platform-ops']
        second = cards.analysis_cards(self.args)
        self.assertNotEqual(first['manifest_path'], second['manifest_path'])
        self.assertTrue(Path(first['manifest_path']).is_file())
        self.assertTrue(Path(second['manifest_path']).is_file())
        self.args.roles=['data-analyst','platform-ops']
        with self.assertRaisesRegex(ValueError,'already_exists'):
            cards.analysis_cards(self.args)

    def test_source_mutation_during_staging_leaves_no_published_cards(self):
        original = cards.write_card
        altered = False
        def mutate(path, payload):
            nonlocal altered
            original(path, payload)
            if not altered:
                altered = True
                write(self.root/'baseline-pack.json', dict(self.identity,scope='modified during staging'))
        with patch.object(cards,'write_card',side_effect=mutate):
            with self.assertRaisesRegex(ValueError,'source_changed'):
                cards.analysis_cards(self.args)
        self.assertFalse((self.root/'task-cards/analysis/a1').exists())
        self.assertFalse(list((self.root/'task-cards/analysis').glob('.pending-cards-*')))
        result = cards.analysis_cards(self.args)
        self.assertEqual(len(result['cards']),4)

    def test_progress_does_not_offer_unpublished_staging_card(self):
        rt, obs = self.runtime()
        write(self.root/'failed.json', dict(obs,state='failed'))
        rt.fail('data-analyst','workbuddy','agent-speed-original','a1','failed.json')
        self.args.attempt='a2'; self.args.roles=['data-analyst']
        original = cards.write_card
        observed=[]
        def inspect_during_write(path, payload):
            original(path,payload)
            observed.append(snapshot(self.root,'speed-test','same-client')['members'][0]['next_step'])
        with patch.object(cards,'write_card',side_effect=inspect_during_write):
            cards.analysis_cards(self.args)
        self.assertTrue(observed)
        self.assertEqual(set(observed),{'prepare_a2_for_this_role_only'})
        self.assertEqual(snapshot(self.root,'speed-test','same-client')['members'][0]['next_step'],
                         'verify_and_launch_prepared_a2_once')


if __name__ == '__main__':
    unittest.main()

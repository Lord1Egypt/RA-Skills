"""Read a verified run snapshot; never dispatch, mutate state, or declare delivery."""
import argparse
import json
from pathlib import Path
from host_runtime import Runtime, ROLES, sha
from analysis_work_plan import published_cards

LABELS = {'data-analyst':'数据分析', 'platform-ops':'平台运营',
          'content-live-growth':'内容与直播', 'ad-profit-optimizer':'推广与利润',
          'delivery-review':'独立复核'}
STATES = {'member_started':'已登记启动，需查询原任务', 'member_returned':'已接收回传',
          'member_failed':'已记录失败', 'member_rejected':'回传被拒收'}


def snapshot(run_dir, run_id, client_scope):
    runtime = Runtime(run_dir, run_id, client_scope, read_only=True)
    try:
        identity = runtime.identity()
        state = runtime.status()  # Checks journal chain and selected source fingerprints.
        latest = {r['role']: r for r in state['members']}
        rows = []
        for role in (*ROLES, 'delivery-review'):
            member = latest.get(role, {})
            if member and sha(runtime.path(member['observation_file'])) != member['observation_sha256']:
                raise ValueError('progress_observation_changed:'+role)
            terminal_failure = member.get('state') in ('member_failed', 'member_rejected')
            action = ('query_original_task' if member.get('state') == 'member_started' else
                      'prepare_a2_for_this_role_only' if terminal_failure and member.get('attempt_id') == 'a1' else
                      'stop_retry_budget_exhausted' if terminal_failure else
                      'keep_selected_return' if member.get('state') == 'member_returned' else 'not_started')
            if role == 'delivery-review' and terminal_failure:
                action = 'inspect_frozen_review_and_runtime_retry_authorization'
            if role in ROLES and action == 'prepare_a2_for_this_role_only':
                prepared = published_cards(runtime.root/'task-cards/analysis/a2', role, 'a2')
                if len(prepared)>1:
                    raise ValueError('progress_duplicate_retry_cards:'+role)
                if prepared:
                    card = json.loads(prepared[0].read_text(encoding='utf-8'))
                    if any(card.get(k)!=v for k,v in dict(run_id=run_id,client_scope=client_scope,
                            team_version=identity['team_version'],agent_id=role,attempt_id='a2').items()):
                        raise ValueError('progress_retry_card_identity_changed:'+role)
                    action = 'verify_and_launch_prepared_a2_once'
            rows.append(dict(role=role, name=LABELS[role],
                state=STATES.get(member.get('state'), '未登记启动'),
                task_id=member.get('agent_task_id'), attempt=member.get('attempt_id'), next_step=action))
        return dict(artifact_type='workflow_progress_observation', current_completion_authority=False,
            run_id=run_id, client_scope=client_scope, team_version=identity['team_version'],
            phase=state['phase'], members=rows, next_step=state['next_action'],
            completion=state.get('completion'),
            note='只读核对本次运行记录；已登记启动不证明任务仍在运行。完成资格仍由原生终态、独立复核和 completion_gate 决定。')
    finally:
        runtime.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--client-scope', required=True)
    args = parser.parse_args()
    print(json.dumps(snapshot(Path(args.run_dir), args.run_id, args.client_scope), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

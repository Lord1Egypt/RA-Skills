"""Durable single-attempt execution with independently read state.

Trusted application code supplies a scoped connector and approval verifier.
No CLI can construct approval authority. No credentials are loaded here.
An interrupted reservation is never submitted again, even after restart.
"""
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from action_policy import evaluate, record, timestamp
from artifact_contract import native_operational_identity
from run_journal import check_payload, digest


IDENTITY = ('client_scope', 'platform', 'account_id', 'store_id')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


class ActionGateway:
    def __init__(self, journal, connector, binding, *, approval_verifier=None,
                 execution_enabled=False, clock=None, authority=None):
        self.journal = journal
        self.connector = connector
        self.binding = deepcopy(binding)
        self.approval_verifier = approval_verifier
        self.execution_enabled = execution_enabled is True
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.authority = authority
        # One physical target namespace/key cannot be reserved twice, including
        # in a different run. The journal's immediate transaction serializes it.
        self.journal.db.execute("CREATE UNIQUE INDEX IF NOT EXISTS action_call_once "
                                "ON events(event_key) WHERE kind='action_call_reserved'")
        self.journal.db.execute("CREATE UNIQUE INDEX IF NOT EXISTS action_identity_once "
            "ON events(run_id,json_extract(body,'$.action_id')) WHERE kind='action_call_reserved'")

    def _descriptor(self, action):
        identity = self.journal.db.execute(
            "SELECT client_scope,team_version FROM runs WHERE run_id=?", (action.get('run_id'),)
        ).fetchone()
        require(identity is not None and identity['client_scope'] == action.get('client_scope'),
                'gateway_run_scope_mismatch')
        require(identity['team_version'] == action.get('created_by_team_version'),
                'gateway_action_team_version_mismatch')
        require(all(self.binding.get(k) == action.get(k) and isinstance(action.get(k), str)
                    and action[k].strip() for k in IDENTITY), 'gateway_scope_mismatch')
        capabilities = self.connector.capabilities()
        require(capabilities.get('connector_id') == self.binding.get('connector_id') and
                capabilities.get('platform') == action['platform'], 'gateway_connector_mismatch')
        descriptor = {k: capabilities.get(k) for k in
                      ('connector_id', 'platform', 'connector_version', 'mode', 'status',
                       'read_actions', 'write_actions', 'conditional_write')}
        check_payload(descriptor)
        digest(descriptor)
        require(descriptor['mode'] in ('mock', 'api'), 'gateway_execution_transport_denied')
        if descriptor['mode'] == 'api' or self.authority is not None:
            from execution_store import ExecutionStore
            require(isinstance(self.authority, ExecutionStore), 'gateway_authoritative_store_required')
            self.authority.assert_run(self.journal, action, self.binding)
        require(descriptor['status'] == ('sandbox_verified' if descriptor['mode'] == 'mock'
                                        else 'write_ready'), 'gateway_connector_not_ready')
        return descriptor

    @staticmethod
    def _key(action):
        # Client and run intentionally not part of the platform namespace: a new
        # run or client label must not bypass an existing reservation on the account.
        return digest({k: action[k] for k in ('platform', 'account_id', 'store_id', 'idempotency_key')})

    def _existing(self, action):
        rows = self.journal.events(action['run_id'], action['client_scope'])
        key = self._key(action)
        for row in rows:
            if row['kind'] == 'action_call_reserved' and row['payload']['action_id'] == action['action_id']:
                require(row['payload']['call_key'] == key, 'gateway_action_key_changed')
        reserved = self.journal.db.execute(
            "SELECT run_id FROM events WHERE kind='action_call_reserved' AND event_key=?",
            ('action-call:' + key,)).fetchone()
        if not reserved:
            return None, []
        require(reserved['run_id'] == action['run_id'], 'gateway_key_reserved_in_another_run')
        related = [r for r in rows if r['kind'].startswith('action_call_') and
                   r['payload'].get('call_key') == key]
        require(related and related[0]['kind'] == 'action_call_reserved', 'gateway_reservation_invalid')
        first = related[0]['payload']
        require(first['request_sha256'] == digest(action), 'gateway_key_request_changed')
        return first, related

    @staticmethod
    def _view(first, rows):
        outcomes = [r['payload'] for r in rows if r['kind'] == 'action_call_outcome']
        if outcomes:
            return deepcopy(outcomes[-1])
        aborted = next((r['payload'] for r in rows if r['kind'] == 'action_call_aborted'), None)
        return dict(outcome='blocked', reason=aborted['reason'] if aborted else 'execution_record_requires_readonly_reconciliation',
                    action_id=first['action_id'], connector_call_id=first['connector_call_id'],
                    approval_id=first['approval_id'], readback_id=None, call_key=first['call_key'],
                    simulated=first['simulated'], resubmission_allowed=False,
                    **({'executed': False} if aborted else {}))

    def _read(self, action, credential, descriptor):
        read_operation = action['target']['resource'] + '.get'
        require(all(credential.get(k) == action[k] for k in IDENTITY) and
                credential.get('status') == 'active' and credential.get('credential_id') and
                credential.get('secret_ref') and timestamp(credential.get('expires_at')) > self.clock() and
                isinstance(credential.get('scope'), list) and read_operation in credential['scope'],
                'gateway_read_permission_denied')
        require(read_operation in (descriptor.get('read_actions') or []), 'gateway_read_not_supported')
        observed = self.connector.read(action['target']['resource'], action['target']['platform_id'])
        check_payload(observed)
        digest(observed)
        require(isinstance(observed, dict) and observed.get('status') == 'PASS' and
                observed.get('connector_id') == descriptor['connector_id'] and
                observed.get('platform') == action['platform'] and
                observed.get('resource') == action['target']['resource'] and
                observed.get('platform_id') == action['target']['platform_id'] and
                isinstance(observed.get('data'), dict), 'gateway_read_identity_invalid')
        age = (self.clock() - timestamp(observed.get('read_at'))).total_seconds()
        require(0 <= age <= 60, 'gateway_read_not_current')
        return observed['data']

    def execute(self, action, policy, objects, credential, snapshot, approval=None):
        action, policy, objects, credential, snapshot, approval = deepcopy(
            (action, policy, objects, credential, snapshot, approval))
        for value in (action, policy, objects, credential, snapshot, approval):
            check_payload(value)
            digest(value)
        descriptor = self._descriptor(action)
        first, rows = self._existing(action)
        if first:
            require(first['approval_sha256'] == digest(approval) and
                    first['policy_sha256'] == digest(policy) and
                    first['descriptor_sha256'] == digest(descriptor), 'gateway_replay_binding_changed')
            return self._view(first, rows)  # Never invokes the connector on replay.
        result = evaluate(action, policy, objects, credential, snapshot, approval, self.clock())
        record(self.journal, action['run_id'], action['client_scope'], action, result)
        if result['decision'] != 'eligible_for_execution':
            return dict(outcome='blocked', reason=result['reason'], executed=False)
        require(self.execution_enabled, 'gateway_execution_not_enabled')
        require(descriptor.get('conditional_write') is True and
                action['operation'] in (descriptor.get('write_actions') or []), 'gateway_conditional_write_required')
        try:
            confirmed = (callable(self.approval_verifier) and
                         self.approval_verifier(deepcopy(approval), deepcopy(action)) is True)
        except Exception:
            raise ValueError('gateway_trusted_approval_check_failed') from None
        require(confirmed, 'gateway_trusted_approval_missing')
        try:
            current = self._read(action, credential, descriptor)
        except Exception:
            return dict(outcome='blocked', reason='preflight_read_failed', executed=False)
        require(digest(current) == snapshot['source_fingerprint'], 'gateway_approved_state_changed')
        payload = dict(**native_operational_identity('connector_call', action['created_by_team_version']),
                       call_key=self._key(action), connector_call_id='call-' + uuid4().hex,
                       action_id=action['action_id'], approval_id=approval['approval_id'],
                       request_sha256=digest(action), policy_sha256=digest(policy),
                       approval_sha256=digest(approval), descriptor_sha256=digest(descriptor),
                       expected_sha256=digest(action['changes']), before_sha256=digest(current),
                       simulated=descriptor['mode'] == 'mock', bindings=result['bindings'],
                       resubmission_allowed=False)
        with self.journal.transaction():
            first, rows = self._existing(action)
            if first:
                return self._view(first, rows)
            self.journal.append_locked(action['run_id'], action['client_scope'],
                'action-call:' + payload['call_key'], 'action_call_reserved', payload)
        # The reservation is committed before any potentially mutating call.
        # BaseException/process exit deliberately leaves it unresolved, never retryable.
        try:
            fresh = evaluate(action, policy, objects, credential, snapshot, approval, self.clock())
            if fresh['decision'] != 'eligible_for_execution':
                self._event(action, payload, 'aborted', dict(reason='approval_or_policy_expired_before_call'))
                return self._view(payload, self._existing(action)[1])
            response = self.connector.execute(deepcopy(action), approval_state='approved',
                idempotency_key=action['idempotency_key'], dry_run=False,
                expected_data_sha256=payload['before_sha256'])
            check_payload(response)
            digest(response)
            valid = (isinstance(response, dict) and response.get('status') == 'executed' and
                     response.get('request_hash') == payload['request_sha256'] and
                     response.get('idempotency_key') == action['idempotency_key'] and
                     response.get('connector_id') == descriptor['connector_id'] and
                     response.get('platform') == action['platform'] and response.get('target') == action['target'] and
                     response.get('simulated') is payload['simulated'] and response.get('dry_run') is False)
            require(valid, 'gateway_execution_response_unbound')
        except Exception:
            self._event(action, payload, 'uncertain', dict(reason='call_failed_or_response_unbound'))
        else:
            self._event(action, payload, 'returned', dict(response_sha256=digest(response)))
        return self.reconcile(action, credential)

    def _event(self, action, first, suffix, extra):
        payload = dict(**native_operational_identity('connector_call', action['created_by_team_version']),
                       call_key=first['call_key'], connector_call_id=first['connector_call_id'],
                       action_id=first['action_id'], approval_id=first['approval_id'], **extra)
        return self.journal.append(action['run_id'], action['client_scope'],
            first['connector_call_id'] + ':' + suffix, 'action_call_' + suffix, payload)

    def reconcile(self, action, credential):
        """Read only. Matching target after an uncertain call is not execution proof."""
        action, credential = deepcopy((action, credential))
        check_payload(action)
        check_payload(credential)
        descriptor = self._descriptor(action)
        first, rows = self._existing(action)
        require(first is not None and first['descriptor_sha256'] == digest(descriptor),
                'gateway_no_matching_reservation')
        require(first['expected_sha256'] == digest(action['changes']), 'gateway_expected_state_changed')
        previous = self._view(first, rows)
        if previous['outcome'] == 'verified':
            return previous  # Historical verification, not a new current-state claim.
        successful = any(r['kind'] == 'action_call_returned' for r in rows)
        try:
            actual = self._read(action, credential, descriptor)
            matched = all(k in actual and digest(actual[k]) == digest(v) for k, v in action['changes'].items())
            require(bool(action['changes']), 'gateway_empty_expected_state')
            observation = dict(matched=matched, actual_sha256=digest(actual), read_succeeded=True)
        except Exception:
            observation = dict(matched=False, actual_sha256=None, read_succeeded=False)
        readback_id = 'readback-' + uuid4().hex
        now = self.clock().isoformat()
        outcome = dict(**native_operational_identity('outcome', action['created_by_team_version']),
                       call_key=first['call_key'], connector_call_id=first['connector_call_id'],
                       action_id=first['action_id'], approval_id=first['approval_id'], readback_id=readback_id,
                       outcome='verified' if successful and observation['matched'] else 'blocked',
                       reason=('returned_and_state_matched' if successful and observation['matched'] else
                               'execution_uncertain' if not successful else 'readback_not_matched'),
                       simulated=first['simulated'], resubmission_allowed=False, observed_at=now)
        with self.journal.transaction():
            current_first, current_rows = self._existing(action)
            current_view = self._view(current_first, current_rows)
            if current_view['outcome'] == 'verified':
                return current_view
            readback = dict(**native_operational_identity('readback', action['created_by_team_version']),
                            call_key=first['call_key'], connector_call_id=first['connector_call_id'],
                            action_id=first['action_id'], approval_id=first['approval_id'],
                            readback_id=readback_id, observed_at=now, **observation)
            self.journal.append_locked(action['run_id'], action['client_scope'], readback_id,
                                       'action_call_readback', readback)
            self.journal.append_locked(action['run_id'], action['client_scope'], readback_id + ':outcome',
                                       'action_call_outcome', outcome)
        return outcome

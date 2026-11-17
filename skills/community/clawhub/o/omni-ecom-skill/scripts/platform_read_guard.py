"""Scoped, read-only platform observations with explicit mock/API boundaries.

Trusted host code supplies the connector and a credential reference. This
module never resolves secrets, never exposes credential references in output,
and never performs a write. A single API observation is not formal end-to-end
acceptance and is labelled accordingly.
"""
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from action_policy import timestamp
from artifact_contract import native_operational_identity
from run_journal import check_payload, digest


IDENTITY = ('client_scope', 'platform', 'account_id', 'store_id')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


class PlatformReadGateway:
    def __init__(self, journal, connector, binding, *, authority=None, clock=None,
                 max_age_seconds=60):
        self.journal = journal
        self.connector = connector
        self.binding = deepcopy(binding)
        self.authority = authority
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        require(type(max_age_seconds) is int and 0 < max_age_seconds <= 300,
                'platform_read_max_age_invalid')
        self.max_age_seconds = max_age_seconds

    def _descriptor(self, request):
        run = self.journal.db.execute(
            'SELECT client_scope,team_version FROM runs WHERE run_id=?',
            (request.get('run_id'),)).fetchone()
        require(run is not None and run['client_scope'] == request.get('client_scope'),
                'platform_read_run_scope_mismatch')
        require(run['team_version'] == request.get('team_version'),
                'platform_read_team_version_mismatch')
        require(all(self.binding.get(k) == request.get(k) and
                    isinstance(request.get(k), str) and request[k].strip() for k in IDENTITY),
                'platform_read_scope_mismatch')
        require(self.binding.get('connector_id'), 'platform_read_connector_binding_missing')
        capabilities = self.connector.capabilities()
        check_payload(capabilities)
        digest(capabilities)
        descriptor = {k: capabilities.get(k) for k in
                      ('schema_version','connector_id','platform','connector_version','mode','status',
                       'read_actions','auth_type','verified_at')}
        require(descriptor['schema_version'] == '1.0' and
                descriptor['connector_id'] == self.binding['connector_id'] and
                descriptor['platform'] == request['platform'], 'platform_read_connector_mismatch')
        require(descriptor['mode'] in ('mock','api'), 'platform_read_transport_denied')
        expected_status = ('sandbox_verified',) if descriptor['mode'] == 'mock' else (
            'read_only_verified','write_ready')
        require(descriptor['status'] in expected_status, 'platform_read_connector_not_ready')
        operation = request['resource'] + '.get'
        require(operation in (descriptor.get('read_actions') or []), 'platform_read_not_supported')
        requested_mode = request.get('acceptance_mode')
        require(requested_mode in ('synthetic','live'), 'platform_read_acceptance_mode_invalid')
        require(not (requested_mode == 'live' and descriptor['mode'] != 'api'),
                'platform_read_live_mode_requires_api')
        if descriptor['mode'] == 'api':
            from execution_store import ExecutionStore
            require(isinstance(self.authority, ExecutionStore),
                    'platform_read_authoritative_store_required')
            authority_request = dict(request, created_by_team_version=request['team_version'])
            self.authority.assert_run(self.journal, authority_request, self.binding)
        return descriptor

    def _credential(self, request, credential):
        check_payload(credential)
        digest(credential)
        operation = request['resource'] + '.get'
        require(isinstance(credential, dict) and
                all(credential.get(k) == request[k] for k in IDENTITY) and
                credential.get('status') == 'active' and credential.get('credential_id') and
                credential.get('secret_ref') and isinstance(credential.get('scope'), list) and
                operation in credential['scope'], 'platform_read_permission_denied')
        require(timestamp(credential.get('expires_at')) > self.clock(),
                'platform_read_credential_expired')

    def read(self, request, credential):
        request, credential = deepcopy((request, credential))
        check_payload(request)
        digest(request)
        required=('request_id','run_id','client_scope','platform','account_id','store_id',
                  'team_version','resource','platform_id','acceptance_mode')
        require(isinstance(request,dict) and set(request) == set(required) and
                all(isinstance(request.get(k),str) and request[k].strip() for k in required),
                'platform_read_request_invalid')
        request_sha = digest(request)
        event_key = 'platform-read:' + request['request_id']
        previous = next((row for row in self.journal.events(request['run_id'], request['client_scope'])
                         if row['event_key'] == event_key), None)
        if previous is not None:
            require(previous['kind'] == 'platform_read_observed' and
                    previous['payload'].get('request_sha256') == request_sha,
                    'platform_read_request_id_conflict')
            return deepcopy(previous['payload'])
        descriptor = self._descriptor(request)
        self._credential(request, credential)
        response = self.connector.read(request['resource'], request['platform_id'])
        check_payload(response)
        response_sha = digest(response)
        require(isinstance(response,dict) and response.get('status') == 'PASS' and
                response.get('connector_id') == descriptor['connector_id'] and
                response.get('platform') == request['platform'] and
                response.get('resource') == request['resource'] and
                response.get('platform_id') == request['platform_id'] and
                isinstance(response.get('data'),dict), 'platform_read_response_unbound')
        read_at = timestamp(response.get('read_at'))
        age = (self.clock() - read_at).total_seconds()
        require(0 <= age <= self.max_age_seconds, 'platform_read_observation_not_current')
        expected_source = digest({'resource':request['resource'],
                                  'platform_id':request['platform_id'],
                                  'data':response['data']})
        require(response.get('source_fingerprint') == expected_source,
                'platform_read_source_fingerprint_invalid')
        simulated = descriptor['mode'] == 'mock'
        now = self.clock().isoformat()
        observation = dict(
            **native_operational_identity('platform_read', request['team_version']),
            team_version=request['team_version'], read_id='read-' + uuid4().hex,
            request_id=request['request_id'], run_id=request['run_id'],
            client_scope=request['client_scope'], platform=request['platform'],
            account_id=request['account_id'], store_id=request['store_id'],
            resource=request['resource'], platform_id=request['platform_id'],
            acceptance_mode=request['acceptance_mode'], connector_id=descriptor['connector_id'],
            connector_version=descriptor['connector_version'], connector_mode=descriptor['mode'],
            request_sha256=request_sha, descriptor_sha256=digest(descriptor), connector_response_sha256=response_sha,
            connector_source_fingerprint=expected_source, data=deepcopy(response['data']),
            data_sha256=digest(response['data']), read_at=read_at.isoformat(), observed_at=now,
            status='synthetic_read_verified' if simulated else 'native_api_observation_recorded',
            evidence_kind='synthetic_mock_read' if simulated else 'native_platform_api_observation',
            simulated=simulated, platform_connection_verified=not simulated,
            independently_authenticated=False, formal_acceptance_completed=False,
            write_attempted=False)
        self.journal.append(request['run_id'], request['client_scope'], event_key,
                            'platform_read_observed', observation)
        return observation

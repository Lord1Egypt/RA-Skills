"""Deterministic action eligibility, never platform execution or approval issuance."""
from datetime import datetime,timezone
from decimal import Decimal,InvalidOperation

from run_journal import check_payload,digest
from artifact_contract import native_operational_identity, validate_operational_identity


class Denied(ValueError): pass


def require(ok,reason):
    if not ok: raise Denied(reason)


def timestamp(value):
    try:
        parsed=datetime.fromisoformat(str(value).replace('Z','+00:00'))
        require(parsed.tzinfo is not None,'policy_time_requires_timezone')
        return parsed
    except (ValueError,TypeError) as exc: raise Denied('policy_time_invalid') from exc


def number(value):
    require(not isinstance(value,bool),'policy_number_invalid')
    try: result=Decimal(str(value))
    except (InvalidOperation,ValueError): raise Denied('policy_number_invalid')
    require(result.is_finite(),'policy_number_invalid')
    return result


def _evaluate(action,policy,objects,credential,snapshot,approval,now):
    for value in (action,policy,objects,credential,snapshot,approval or {}):
        check_payload(value)
        digest(value)  # Reject non-finite JSON and non-serializable values.
    require(action.get('schema_version')=='2.0' and policy.get('schema_version')=='2.0','policy_schema_unsupported')
    action_version=validate_operational_identity(action,'controlled_action')
    require(all(isinstance(action.get(k),str) and bool(action[k].strip()) for k in
        ('action_id','run_id','client_scope','platform','account_id','store_id','operation','idempotency_key')),
        'policy_action_identity_missing')
    require(policy.get('client_scope')==action['client_scope'],'policy_client_scope_mismatch')
    require(policy.get('revision') and policy.get('policy_id'),'policy_revision_missing')
    require(policy.get('mode') in ('readonly','assisted','controlled'),'policy_mode_invalid')
    if policy['mode']=='readonly': raise Denied('policy_readonly')
    target=action.get('target')
    require(isinstance(target,dict) and set(target)=={'resource','platform_id'} and all(target.values()),'policy_target_invalid')
    require(isinstance(objects,list),'policy_registry_invalid')
    matches=[o for o in objects if isinstance(o,dict) and all(o.get(k)==action[k] for k in
             ('client_scope','platform','account_id','store_id')) and o.get('object_type')==target['resource'] and
             o.get('platform_id')==target['platform_id']]
    require(len(matches)==1 and matches[0].get('status')=='active','policy_target_unknown_or_ambiguous')
    obj=matches[0]
    max_age=policy.get('object_max_age_seconds')
    require(type(max_age) is int and max_age>0,'policy_registry_freshness_missing')
    require(0<=(now-timestamp(obj.get('seen_at'))).total_seconds()<=max_age,'policy_registry_stale')
    require(isinstance(credential,dict) and credential.get('status')=='active' and
            all(credential.get(k)==action[k] for k in ('client_scope','platform','account_id','store_id')),
            'policy_credential_scope_mismatch')
    require(credential.get('credential_id') and credential.get('secret_ref'),'policy_credential_reference_missing')
    require(timestamp(credential.get('expires_at'))>now,'policy_credential_expired')
    require(isinstance(credential.get('scope'),list) and action['operation'] in credential['scope'],
            'policy_credential_operation_denied')
    rule=policy.get('operations',{}).get(action['operation'])
    require(isinstance(rule,dict) and rule.get('resource')==target['resource'],'policy_operation_denied')
    changes=action.get('changes')
    fields=rule.get('fields')
    require(isinstance(changes,dict) and bool(changes) and isinstance(fields,dict) and
            set(changes).issubset(fields),'policy_field_denied')
    require(isinstance(snapshot,dict) and all(snapshot.get(k)==action[k] for k in
            ('client_scope','platform','account_id','store_id')) and snapshot.get('target')==target and
            isinstance(snapshot.get('data'),dict),'policy_snapshot_scope_mismatch')
    require(snapshot.get('source_fingerprint')==digest(snapshot['data']),'policy_snapshot_fingerprint_invalid')
    freshness=policy.get('snapshot_max_age_seconds')
    require(type(freshness) is int and freshness>0 and
            0<=(now-timestamp(snapshot.get('read_at'))).total_seconds()<=freshness,'policy_snapshot_stale')
    for field,value in changes.items():
        limit=fields[field]
        require(isinstance(limit,dict),'policy_field_rule_invalid')
        if 'allowed_values' in limit:
            require(isinstance(limit['allowed_values'],list) and any(type(v)==type(value) and v==value for v in limit['allowed_values']),
                    'policy_field_value_denied')
        else:
            require(set(('minimum','maximum','max_increase','max_decrease')).issubset(limit),'policy_numeric_limits_missing')
            proposed=number(value); current=number(snapshot['data'].get(field))
            minimum,maximum=number(limit['minimum']),number(limit['maximum'])
            increase,decrease=number(limit['max_increase']),number(limit['max_decrease'])
            require(minimum<=maximum and increase>=0 and decrease>=0,'policy_numeric_limits_invalid')
            require(minimum<=proposed<=maximum and -decrease<=proposed-current<=increase,'policy_numeric_limit_exceeded')
    bindings=dict(request_sha256=digest(action),policy_sha256=digest(policy),object_sha256=digest(obj),
                  credential_sha256=digest(credential),snapshot_sha256=digest(snapshot))
    if policy['mode']=='assisted':
        return dict(decision='assisted_plan_only',reason='platform_execution_not_enabled',bindings=bindings)
    if not approval:
        return dict(decision='requires_approval',reason='explicit_approval_missing',bindings=bindings)
    require(approval.get('schema_version')=='2.0' and approval.get('state')=='approved','policy_approval_not_granted')
    validate_operational_identity(approval,'approval',action_version)
    require(all(approval.get(k)==action[k] for k in ('client_scope','run_id','action_id')),'policy_approval_scope_mismatch')
    require(all(approval.get(k)==v for k,v in bindings.items()),'policy_approval_binding_changed')
    require(all(isinstance(approval.get(k),str) and bool(approval[k].strip()) for k in
                ('approval_id','actor','source_reference')),'policy_approval_provenance_missing')
    require(timestamp(approval.get('decided_at'))<=now<timestamp(approval.get('expires_at')),
            'policy_approval_expired_or_future')
    return dict(decision='eligible_for_execution',reason='scoped_limits_and_recorded_approval_match',
                approval_id=approval['approval_id'],bindings=bindings)


def evaluate(action,policy,objects,credential,snapshot,approval=None,now=None):
    now=now or datetime.now(timezone.utc)
    require(now.tzinfo is not None,'policy_time_requires_timezone')
    try: result=_evaluate(action,policy,objects,credential,snapshot,approval,now)
    except (ValueError,KeyError,TypeError,AttributeError) as exc:
        # Never echo request data or credential values in failure logs.
        reason=str(exc) if isinstance(exc,Denied) else 'policy_input_invalid'
        result=dict(decision='denied',reason=reason)
    return dict(schema_version='2.0',evaluated_at=now.isoformat(),executed=False,
                approval_authenticity='requires_trusted_host_confirmation',**result)


def record(journal,run_id,client_scope,action,result):
    """Append the bounded decision to an existing scoped journal; no credentials."""
    require(action.get('run_id')==run_id and action.get('client_scope')==client_scope,'policy_audit_scope_mismatch')
    version=validate_operational_identity(action,'controlled_action')
    payload=dict(**native_operational_identity('policy_decision',version),
                 action_id=action['action_id'],request_sha256=digest(action),decision=result['decision'],
                 reason=result['reason'],bindings=result.get('bindings',{}),executed=False,
                 approval_id=result.get('approval_id'),evaluated_at=result['evaluated_at'])
    return journal.append(run_id,client_scope,'policy:'+digest(payload),'action_policy_decision',payload)

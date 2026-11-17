"""Operator-only storage reservations; requests cannot create or alter tenants."""
import json
import os

MAX_STORE_EVENTS = 100000
MAX_STORE_BODY_BYTES = 256 * 1024 * 1024
DEFAULT_TENANT_QUOTAS = {'local': {'max_events': 10000, 'max_bytes': 16 * 1024 * 1024}}


def capacity_policy(quotas=None):
    if quotas is None:
        raw = os.environ.get('JEP_AUDIT_TENANT_QUOTAS')
        quotas = json.loads(raw) if raw is not None else DEFAULT_TENANT_QUOTAS
    if not isinstance(quotas, dict) or not 1 <= len(quotas) <= 128:
        raise ValueError('Storage quotas must name 1 to 128 tenants')
    validated = {}
    for tenant, limits in quotas.items():
        if not isinstance(tenant, str) or not 1 <= len(tenant) <= 128 or tenant != tenant.strip():
            raise ValueError('Invalid storage tenant name')
        if not isinstance(limits, dict) or set(limits) != {'max_events', 'max_bytes'}:
            raise ValueError('Each tenant needs max_events and max_bytes')
        if any(type(value) is not int or value <= 0 for value in limits.values()):
            raise ValueError('Storage quotas must be positive integers')
        validated[tenant] = dict(limits)
    if sum(v['max_events'] for v in validated.values()) > MAX_STORE_EVENTS:
        raise ValueError('Tenant event reservations exceed store capacity')
    if sum(v['max_bytes'] for v in validated.values()) > MAX_STORE_BODY_BYTES:
        raise ValueError('Tenant byte reservations exceed store capacity')
    policy = json.dumps({'version': 1, 'tenants': validated}, sort_keys=True, separators=(',', ':'))
    return validated, policy

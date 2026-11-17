"""Validate declared platform-export acquisition metadata without overclaiming authenticity."""
from datetime import datetime

from adjudication_guard import require


BOUNDARY='source_bound_export_not_platform_authenticated'


def validate(attribution, payload=None):
    require(isinstance(attribution,dict),'acquisition_attribution_missing')
    require(attribution.get('acquisition_mode')=='manual_platform_export',
            'acquisition_mode_unsupported')
    require(attribution.get('authenticity_status')==BOUNDARY,
            'acquisition_authenticity_overclaim')
    require(attribution.get('metric_semantics_version')=='2.0',
            'acquisition_metric_semantics_unbound')
    for key in ('export_reference','exported_at','client_scope','platform'):
        require(isinstance(attribution.get(key),str) and attribution[key].strip(),
                'acquisition_metadata_missing:'+key)
    try:
        datetime.fromisoformat(attribution['exported_at'].replace('Z','+00:00'))
    except ValueError as exc:
        raise ValueError('acquisition_exported_at_invalid') from exc
    if payload is not None:
        require(attribution['client_scope']==payload.get('client_scope'),
                'acquisition_client_scope_mismatch')
        root_scope=payload.get('scope',{})
        platform=root_scope.get('platform') if isinstance(root_scope,dict) else None
        require(platform is None or attribution['platform']==platform,
                'acquisition_platform_mismatch')
    return dict(status='export_metadata_bound_not_platform_authenticated',
                export_reference=attribution['export_reference'],
                authenticity_status=BOUNDARY)

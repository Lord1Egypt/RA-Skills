"""Hermes file-only adapter. No Hermes imports, subprocesses, .env reads or writes."""
import json
from pathlib import Path
from optimizer_core import VERSION, finding, safe_id

HERMES_SOURCE = 'd7b836ab1c0cddaafc109ed24c9a83b6191cdc88'
MAX_BYTES = 8 * 1024 * 1024

def read_config(path):
    p = Path(path)
    if p.stat().st_size > MAX_BYTES:
        raise ValueError('Config exceeds limit')
    text = p.read_text()
    if p.suffix.lower() == '.json':
        data = json.loads(text)
    else:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError('Hermes YAML requires PyYAML; use JSON export or Hermes Python environment') from exc
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError('Invalid YAML; raw data withheld') from exc
    if not isinstance(data, dict):
        raise ValueError('Config must be an object')
    return data

def resolve_job(job, config, model_env=None):
    model_cfg = config.get('model') or {}
    fleet = config.get('cron') or {}
    if not isinstance(fleet, dict) or not isinstance(model_cfg, (dict, str)):
        raise ValueError('Unsupported Hermes model/cron shape')
    global_model = model_cfg.get('default') if isinstance(model_cfg, dict) else model_cfg
    global_provider = model_cfg.get('provider') if isinstance(model_cfg, dict) else None
    def choose(pairs):
        for source, value in pairs:
            if isinstance(value, str) and value.strip():
                return safe_id(value.strip()), source
        return None, 'unknown'
    model, model_source = choose([('job',job.get('model')),('cron',fleet.get('model')),
        ('snapshot',job.get('model_snapshot')),('explicit_environment',model_env),('global_config',global_model)])
    provider, provider_source = choose([('job',job.get('provider')),('cron',fleet.get('model_provider')),
        ('snapshot',job.get('provider_snapshot')),('global_config',global_provider)])
    return {'model':model,'modelSource':model_source,'provider':provider,'providerSource':provider_source}

def audit_hermes(config, jobs, model_env=None, config_present=True, jobs_present=True):
    if not isinstance(jobs, list) or any(not isinstance(j, dict) for j in jobs):
        raise ValueError('Hermes jobs must be an array of objects')
    out=[]; summaries=[]; enabled=0; scripts=0
    for index, job in enumerate(jobs,1):
        if job.get('enabled',True) is False or job.get('state')=='paused':
            continue
        enabled += 1
        label=f'Automation #{index}'
        no_agent=job.get('no_agent',False)
        if not isinstance(no_agent,bool):
            raise ValueError('no_agent must be a boolean')
        if no_agent:
            scripts += 1
            summaries.append({'index':index,'mode':'no_agent','llmInference':False})
            if not isinstance(job.get('script'),str) or not job['script'].strip():
                out.append(finding('hermes_script_missing','warning',f'{label}: no_agent job has no script.'))
            continue
        resolved=resolve_job(job,config,model_env)
        summaries.append({'index':index,'mode':'agent','resolution':resolved})
        if not resolved['model']:
            out.append(finding('hermes_model_unknown','warning',f'{label}: no model found in supplied file evidence; environment/runtime may differ.'))
        elif resolved['modelSource']=='snapshot':
            out.append(finding('hermes_snapshot_model','info',f'{label}: retains its creation-time model snapshot, not the current global default.'))
        elif resolved['modelSource'] in ('global_config','explicit_environment'):
            out.append(finding('hermes_inherited_model','info',f'{label}: model depends on defaults rather than a job/fleet pin or snapshot.'))
        schedule=job.get('schedule') or {}
        if not isinstance(schedule,dict):raise ValueError('Invalid schedule')
        minutes=schedule.get('minutes')
        if schedule.get('kind')=='interval' and isinstance(minutes,(int,float)) and 0<minutes<60:
            out.append(finding('hermes_frequent_agent_job','warning',f'{label}: agent runs more than hourly; review whether no_agent would suffice for a deterministic task.'))
        if not job.get('deliver'):
            out.append(finding('hermes_delivery_inherited','info',f'{label}: delivery is not explicit in the supplied job.'))
    return {'version':VERSION,'runtime':'hermes','mode':'read-only-files','findings':out,
        'automations':summaries,'counts':{'total':len(jobs),'enabled':enabled,'noAgent':scripts},
        'coverage':{'config':config_present,'jobs':jobs_present,'authentication':False,'catalog':False,'environment':model_env is not None},
        'compatibility':{'sourceCommit':HERMES_SOURCE,'status':'file_schema_tested'},
        'savingsEstimate':None,'limitations':[
            'File evidence only: profile overlays, runtime overrides, aliases and provider fallbacks are not resolved.',
            'No .env, credential store, ambient environment, model catalog or authentication read.',
            'A missing explicit environment value can change legacy/global model resolution.',
            'No agent, scheduler, script, inference canary or network request is started.',
            'no_agent avoids Hermes inference; its script may incur costs of its own.']}

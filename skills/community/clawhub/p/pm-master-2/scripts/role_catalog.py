#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Domain + expert role catalog (single source of truth)

Design goals
-----------
1. **Domain-agnostic**: the out-of-the-box default no longer favors the data domain.
   Any technical project (software development / cloud & infrastructure / data platform /
   AI·ML / security / product / QA / integration / ERP / BI) can obtain a suitable expert role.
2. **Auto-align from contract/SOW extraction**: `infer_domain(text)` infers the technical
   domain from SOW/contract text; `infer_role(name, domain)` combines domain-specific keywords
   with cross-domain keywords to suggest a role; `align_from_sow(spec)` outputs the whole SOW's
   {domain, product, role suggestions} for `parse_sow.py` to write and `dispatch.py` /
   `consistency_check.py` to reuse.
3. **Single source of truth**: `dispatch.py` and `consistency_check.py` share this file, eliminating drift.

Role IDs use capability-based naming that is cross-domain; domain-specific display names are
generated in `role_labels` and substituted by `specialize()` per project.domain / project.product,
never hard-coding any client/vendor identifiers.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Cross-domain roles (applicable to any technical domain)
# ---------------------------------------------------------------------------
CROSS_ROLES = {
    'ba': ['requirement', 'user story', 'specification', 'requirement', 'story', 'brd', 'prd', 'requirement analysis'],
    'qa-lead': ['testing', 'uat', 'quality', 'test', 'quality', 'qa'],
    'change-manager': ['change', 'ccb', 'change', 'impact assessment', 'change control'],
    'solution-architect': ['blueprint', 'integration', 'solution', 'blueprint', 'integration', 'solution',
                           'architecture design', 'architecture', 'overall design'],
    'enablement-lead': ['training', 'enablement', 'course', 'training', 'enable', 'knowledge transfer', 'kt'],
    'infra-engineer': ['infrastructure', 'installation', 'environment', 'infra', 'install', 'env', 'deployment', 'capacity planning',
                       'capacity'],
    'domain-sme': ['sme', 'domain knowledge', 'source system', 'domain support', 'business rules', 'business consultant'],
    'project-manager': ['project manager', 'pmo', 'schedule management', 'communication plan', 'stakeholder mgmt'],
}

# ---------------------------------------------------------------------------
# Technical domain catalog
# Each domain: keywords (domain identification signals), roles ({role_id: [keywords]}),
#              role_labels ({role_id: specialized-name template, supports {domain}/{product}})
# ---------------------------------------------------------------------------
DOMAINS = {
    'data-platform': {
        'keywords': ['data lake', 'data warehouse', 'datalake', 'data lake', 'data warehouse', 'warehouse',
                     'etl', 'data modeling', 'data migration', 'master data', 'metadata', 'data lineage',
                     'data platform', 'lakehouse', 'data pipeline'],
        'roles': {
            'data-architect': ['modeling', 'model', 'subject area', 'schema', 'erd', 'data model',
                               'datamodel', 'logical model', 'physical model'],
            'etl-engineer': ['migration', 'historical load', 'extraction', 'etl', 'load', 'ingestion', 'migration',
                             'load', 'pipeline', 'data pipeline'],
            'data-governance-lead': ['governance', 'metadata', 'data lineage', 'audit', 'governance', 'meta',
                                     'audit', 'master data management', 'mdm'],
            'data-security-engineer': ['masking', 'tokenization', 'privacy', 'pii', 'token', 'encryption', 'mask',
                                      'privacy', 'compliance'],
            'data-scientist': ['analysis', 'feature', 'ml', 'modelops', 'use case', 'analytic', 'statistical analysis'],
        },
        'role_labels': {
            'data-architect': '{domain} data architect',
            'etl-engineer': '{domain} ETL/data engineer',
            'data-governance-lead': '{domain} data governance lead',
            'data-security-engineer': '{domain} data security/compliance engineer',
            'data-scientist': '{domain} data analytics/modeling engineer',
        },
    },
    'software-dev': {
        'keywords': ['software development', 'application development', 'backend', 'frontend', 'microservice', 'software',
                     'application development', 'backend', 'frontend', 'microservice',
                     'app development', 'application system'],
        'roles': {
            'software-architect': ['architecture design', 'module design', 'module decomposition', 'architecture', 'system design'],
            'backend-engineer': ['backend', 'server-side', 'backend', 'api implementation', 'service implementation'],
            'frontend-engineer': ['frontend', 'ui', 'frontend', 'web', 'ui implementation'],
            'fullstack-engineer': ['full stack', 'fullstack', 'full stack'],
            'mobile-engineer': ['mobile', 'mobile', 'ios', 'android', 'app client'],
        },
        'role_labels': {
            'software-architect': '{domain} software architect',
            'backend-engineer': '{domain} backend engineer',
            'frontend-engineer': '{domain} frontend engineer',
            'fullstack-engineer': '{domain} fullstack engineer',
            'mobile-engineer': '{domain} mobile engineer',
        },
    },
    'cloud-infra': {
        'keywords': ['cloud', 'cloud', 'kubernetes', 'k8s', 'terraform', 'container', 'containerization', 'iac',
                     'infrastructure as code', 'aws', 'azure', 'gcp', 'private cloud', 'cloud native'],
        'roles': {
            'cloud-architect': ['cloud architecture', 'cloud solution', 'cloud architecture', 'cloud blueprint'],
            'sre-engineer': ['reliability', 'sre', 'stability', 'availability', 'oncall', 'disaster recovery'],
            'platform-engineer': ['platform engineering', 'platform', 'internal platform', 'devops platform'],
            'devops-engineer': ['devops', 'ci/cd', 'pipeline', 'automated deployment', 'pipeline engineering'],
            'network-engineer': ['network', 'network', 'vpc', 'dns', 'load balancing', 'lb'],
        },
        'role_labels': {
            'cloud-architect': '{domain} cloud architect',
            'sre-engineer': '{domain} SRE engineer',
            'platform-engineer': '{domain} platform engineer',
            'devops-engineer': '{domain} DevOps engineer',
            'network-engineer': '{domain} network engineer',
        },
    },
    'ai-ml': {
        'keywords': ['llm', 'llm', 'machine learning', 'machine learning', 'ai', 'deep learning',
                      'deep learning', 'model training', 'inference', 'inference', 'genai', 'generative'],
        'roles': {
            'ml-engineer': ['model training', 'feature engineering', 'ml', 'machine learning', 'model training', 'modeling'],
            'llm-engineer': ['llm', 'llm', 'prompt', 'rag', 'fine-tuning', 'fine-tune', 'inference optimization'],
            'mlops-engineer': ['mlops', 'model deployment', 'model monitoring', 'model serving', 'model release'],
            'ai-product-manager': ['ai product', 'ai product', 'algorithm product', 'model product'],
            'data-scientist': ['analysis', 'feature', 'use case', 'analytic', 'statistical analysis'],
        },
        'role_labels': {
            'ml-engineer': '{domain} ML engineer',
            'llm-engineer': '{domain} LLM engineer',
            'mlops-engineer': '{domain} MLOps engineer',
            'ai-product-manager': '{domain} AI product manager',
            'data-scientist': '{domain} data science engineer',
        },
    },
    'cybersecurity': {
        'keywords': ['security', 'security', 'penetration', 'pentest', 'attack-defense', 'compliance security', 'zero trust',
                     'zero trust', 'vulnerability', 'vulnerability', 'regulated protection'],
        'roles': {
            'security-engineer': ['security design', 'security hardening', 'security', 'protection', 'hardening', 'security architecture'],
            'privacy-engineer': ['privacy', 'pii', 'de-identification', 'privacy', 'personal information protection', 'gdpr', 'pipl', 'data compliance'],
            'secops-engineer': ['security operations', 'soc', 'siem', 'threat detection', 'incident', 'incident response'],
            'appsec-engineer': ['application security', 'appsec', 'code security', 'sast', 'dast'],
        },
        'role_labels': {
            'security-engineer': '{domain} security engineer',
            'privacy-engineer': '{domain} privacy/compliance engineer',
            'secops-engineer': '{domain} security operations engineer',
            'appsec-engineer': '{domain} application security engineer',
        },
    },
    'product': {
        'keywords': ['product', 'product', 'roadmap', 'product planning', 'requirement management', 'backlog planning',
                     'product strategy'],
        'roles': {
            'product-manager': ['product planning', 'roadmap', 'product', 'business analysis', 'product strategy'],
            'product-owner': ['po', 'backlog', 'product backlog', 'product owner'],
            'ux-designer': ['user experience', 'ux', 'ui design', 'interaction', 'prototype'],
        },
        'role_labels': {
            'product-manager': '{domain} product manager',
            'product-owner': '{domain} product owner (PO)',
            'ux-designer': '{domain} UX/interaction designer',
        },
    },
    'qa': {
        'keywords': ['quality', 'quality', 'test engineering', 'automated testing', 'performance testing', 'qa engineering'],
        'roles': {
            'qa-engineer': ['testing', 'test', 'test case', 'uat', 'functional testing'],
            'test-automation-engineer': ['automated testing', 'test automation', 'selenium', 'automation framework'],
            'performance-engineer': ['performance testing', 'performance', 'load testing', 'load testing'],
        },
        'role_labels': {
            'qa-engineer': '{domain} QA engineer',
            'test-automation-engineer': '{domain} test automation engineer',
            'performance-engineer': '{domain} performance test engineer',
        },
    },
    'integration': {
        'keywords': ['integration', 'integration', 'esb', 'middleware', 'middleware', 'api gateway',
                     'api gateway', 'message queue', 'connector'],
        'roles': {
            'integration-engineer': ['integration', 'esb', 'middleware', 'connector', 'interface', 'system integration'],
            'api-engineer': ['api design', 'api gateway', 'api gateway', 'interface', 'api implementation'],
        },
        'role_labels': {
            'integration-engineer': '{domain} integration engineer',
            'api-engineer': '{domain} API engineer',
        },
    },
    'erp': {
        'keywords': ['erp', 'sap', 'oracle ebs', 'finance system', 'hr system', 'enterprise resource',
                     'enterprise resource', 'finance module'],
        'roles': {
            'erp-consultant': ['erp implementation', 'erp consulting', 'sap', 'business process', 'erp blueprint'],
            'erp-developer': ['erp development', 'abap', 'custom development', 'form development'],
            'erp-functional': ['erp functional', 'finance module', 'hr module', 'functional consultant'],
        },
        'role_labels': {
            'erp-consultant': '{domain} ERP implementation consultant',
            'erp-developer': '{domain} ERP development engineer',
            'erp-functional': '{domain} ERP functional consultant',
        },
    },
    'biz-analytics': {
        'keywords': ['bi', 'business intelligence', 'business intelligence', 'reporting platform', 'data analytics platform',
                     'dashboard', 'dashboard platform'],
        'roles': {
            'bi-engineer': ['report', 'dashboard', 'bi', 'visualization', 'olap', 'dashboard'],
            'analytics-engineer': ['analytics engineering', 'analytics engineering', 'metric', 'metrics', 'metrics system'],
        },
        'role_labels': {
            'bi-engineer': '{domain} BI/reporting engineer',
            'analytics-engineer': '{domain} analytics engineer',
        },
    },
}

# Generic / neutral fallback (ambiguous words -> neutral role, to avoid favoring the data domain)
GLOBAL_FALLBACK = {
    'model': 'solution-architect', 'modeling': 'solution-architect',
    'design': 'solution-architect', 'design': 'solution-architect',
    'development': 'software-architect', 'develop': 'software-architect',
}

PM_GENERALIST = {'planner', 'scheduler', 'risk', 'stakeholder', 'reporter', 'program',
                 'project-manager'}

# Backward compatibility: the specialized names below are enabled only when the user's
# project.domain exactly equals one of these known domains; they are no longer the "default"
# that favors the data domain. New projects default to the role_labels of DOMAINS above or
# the neutral fallback role (domain).
LEGACY_SPECIALIZATION = {
    'insurance-data-lake': {
        'data-architect': 'insurance subject-area data architect',
        'etl-engineer': 'MPP data warehouse TPT/ETL engineer',
        'data-security-engineer': 'PIPL/PII compliance engineer',
        'data-scientist': 'insurance actuarial/analytics modeling engineer',
        'governance-lead': 'insurance data governance and audit lead',
        'dr-bcp-engineer': 'insurance BC/DR engineer',
        'infra-engineer': 'MPP data warehouse/platform engineer',
    },
    'payments': {
        'data-architect': 'payments domain architect',
        'etl-engineer': 'payments ETL engineer',
        'data-security-engineer': 'PCI-DSS security engineer',
        'data-scientist': 'anti-fraud/risk-control modeling engineer',
    },
    'ecommerce': {
        'data-architect': 'ecommerce domain modeler',
        'data-scientist': 'recommendation/search ML engineer',
        'etl-engineer': 'ecommerce data engineer',
    },
    'fintech-core': {
        'data-architect': 'core banking domain architect',
        'etl-engineer': 'accounting/settlement engineer',
        'data-security-engineer': 'regulatory reporting engineer',
    },
}


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------
def list_domains():
    return list(DOMAINS.keys())


def infer_domain(text):
    """Infer the technical domain from SOW/contract text. Returns 'generic' when no signal is found."""
    if not text:
        return 'generic'
    t = text.lower()
    best, best_score = 'generic', 0
    for dk, d in DOMAINS.items():
        score = sum(1 for kw in d['keywords'] if kw.lower() in t)
        if score > best_score:
            best, best_score = dk, score
    return best if best_score > 0 else 'generic'


def infer_role(name, domain=None, explicit_role=None):
    """Infer the role for a work package. Priority: explicit role > domain-specific keyword >
    cross-domain keyword > global neutral fallback > None."""
    if explicit_role:
        return explicit_role
    n = (name or '').lower()
    dom = (domain or '').lower()
    if dom in DOMAINS:
        for rid, kws in DOMAINS[dom]['roles'].items():
            if any(k in n for k in kws):
                return rid
    for rid, kws in CROSS_ROLES.items():
        if any(k in n for k in kws):
            return rid
    for k, rid in GLOBAL_FALLBACK.items():
        if k in n:
            return rid
    return None


def is_domain_activity(role, name, domain):
    if role in PM_GENERALIST:
        return False
    if role:
        return True
    n = (name or '').lower()
    if any(k in n for _, kws in CROSS_ROLES.items() for k in kws):
        return True
    for d in DOMAINS.values():
        if any(k in n for kws in d['roles'].values() for k in kws):
            return True
    if domain:
        return True
    return False


def specialize(role, domain, product):
    """Generate a domain-specialized expert name (domain-agnostic, no client/vendor identifiers)."""
    if not role:
        return None
    d = DOMAINS.get(domain)
    if d and role in d.get('role_labels', {}):
        return d['role_labels'][role].format(domain=domain or '', product=product or '')
    # Backward compatibility: enable legacy specialized names only on exact match of known project domains
    if domain in LEGACY_SPECIALIZATION and role in LEGACY_SPECIALIZATION[domain]:
        return LEGACY_SPECIALIZATION[domain][role]
    if product:
        return f"{role} ({product})"
    if domain and domain != 'generic':
        return f"{role} ({domain})"
    return role


def align_from_sow(spec):
    """Extract domain + product + a recommended role per package from the SOW comprehension record (spec dict).
    Returns {domain, product, default_role, pkg_roles:{id:role_id}}.
    """
    text = " ".join([
        str(spec.get('objective', '') or ''),
        str(spec.get('scope', '') or ''),
        str(spec.get('out_of_scope', '') or ''),
        " ".join(str(x) for x in (spec.get('assumptions', []) or [])),
        " ".join(str(x) for x in (spec.get('roles', []) or [])),
    ])
    domain = spec.get('domain') or infer_domain(text)
    product = spec.get('product') or spec.get('name')
    # Explicit roles (keep roles explicitly given in the spec)
    pkg_roles = {}
    for r in (spec.get('roles') or []):
        if isinstance(r, dict):
            pkg_roles[r.get('id')] = r.get('role')
    return {
        'domain': domain,
        'product': product,
        'default_role': 'solution-architect' if domain in (None, 'generic') else None,
        'pkg_roles': pkg_roles,
    }


if __name__ == '__main__':
    # Simple self-test
    samples = {
        'Data lake modeling and ETL migration': 'data-platform',
        'Microservice backend and frontend app development': 'software-dev',
        'Kubernetes containerization and Terraform cloud architecture': 'cloud-infra',
        'LLM RAG and model training': 'ai-ml',
        'Penetration testing and zero-trust hardening': 'cybersecurity',
        'Product roadmap and backlog planning': 'product',
        'Automated testing and performance load testing': 'qa',
        'SAP ERP finance module implementation': 'erp',
        'BI reporting and metrics system': 'biz-analytics',
    }
    for txt, exp in samples.items():
        got = infer_domain(txt)
        print(f"[{'OK' if got == exp else 'XX'}] {txt!r:40} -> {got} (expect {exp})")
    print("role infer (data-platform logical model, data-platform):",
          infer_role('Logical model design', 'data-platform'))
    print("role infer (backend API implementation, software-dev):",
          infer_role('Backend API implementation', 'software-dev'))
    print("specialize (data-architect, data-platform, client data warehouse):",
          specialize('data-architect', 'data-platform', 'cloud data warehouse'))

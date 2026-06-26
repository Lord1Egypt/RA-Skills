from __future__ import annotations

import inspect
import re
import sys
import types
from dataclasses import MISSING, fields
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple

try:
    import mkdocs_gen_files
except ModuleNotFoundError:
    mkdocs_gen_files = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / 'src'
OUTPUT_PATH = 'api/client.md'

if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

# Allow running this generator even when optional runtime deps are not installed.
if 'cloudscraper' not in sys.modules:
    try:
        import cloudscraper  # noqa: F401
    except ModuleNotFoundError:
        class _NoopSession:
            headers = {}

            def request(self, *args, **kwargs):
                raise RuntimeError('Noop session cannot perform requests.')

            def get(self, *args, **kwargs):
                raise RuntimeError('Noop session cannot perform requests.')

        sys.modules['cloudscraper'] = types.SimpleNamespace(
            create_scraper=lambda browser: _NoopSession(),
        )

from peerberry_sdk.client import PeerberryClient
from peerberry_sdk.config import AuthConfig, LifecycleConfig, ObservabilityConfig, RetryConfig, SDKConfig, TransportConfig
from peerberry_sdk.constants import CONSTANTS


METHOD_GROUPS = [
    ('Constructor and Lifecycle', ['__init__', 'login', 'token', 'logout', 'close']),
    ('Profile and Portfolio', [
        'get_profile',
        'get_overview',
        'get_loyalty_tier',
        'get_profit_overview',
        'get_investment_status',
        'get_investment_originators_overview',
    ]),
    ('Loans', ['get_loans', 'get_loans_page', 'get_secondary_loans', 'get_loan_details', 'get_agreement', 'purchase_loan']),
    ('Investments', ['get_investments', 'get_mass_investments']),
    ('Transactions and Summary', ['get_account_summary', 'get_transactions', 'get_mass_transactions']),
    ('Metadata Helpers', ['get_countries', 'get_originators']),
]

METHOD_SUMMARIES: Dict[str, str] = {
    '__init__': 'Creates a new client instance and optionally authenticates immediately.',
    'get_profile': 'Returns investor profile information as a typed model.',
    'get_loyalty_tier': 'Returns the highest unlocked loyalty tier as a typed model.',
    'get_overview': 'Returns portfolio overview data as a typed model wrapper.',
    'get_profit_overview': 'Returns profit chart points for a date interval.',
    'get_investment_status': 'Returns investment status breakdown data.',
    'get_investment_originators_overview': 'Returns originator allocation overview data.',
    'get_loans': 'Fetches multiple available loans using paginated internal requests.',
    'get_loans_page': 'Fetches a single page of available loans with filters.',
    'get_secondary_loans': 'Fetches a single page of secondary-market loan listings with filters.',
    'get_loan_details': 'Returns borrower, loan, schedule, and related details for one loan.',
    'get_agreement': 'Returns investment agreement bytes for a loan.',
    'purchase_loan': 'Creates a purchase order for a selected loan and amount.',
    'get_investments': 'Returns current or finished investments with paging metadata.',
    'get_mass_investments': 'Returns exported investments file bytes.',
    'get_account_summary': 'Returns normalized account summary for a date interval.',
    'get_transactions': 'Returns typed transactions list with optional filters.',
    'get_mass_transactions': 'Returns exported transactions file bytes.',
    'login': 'Authenticates session and returns a bearer token string.',
    'token': 'Forces access-token refresh and returns a bearer token string.',
    'logout': 'Logs out server-side and clears local authentication state.',
    'close': 'Closes underlying transport session, optionally logging out first.',
    'get_countries': 'Returns supported country definitions keyed by display name.',
    'get_originators': 'Returns supported originator definitions keyed by display name.',
}

COMMON_PARAM_DESCRIPTIONS: Dict[str, str] = {
    'email': 'Peerberry account email used in credential login flow.',
    'password': 'Peerberry account password used in credential login flow.',
    'tfa_secret': 'Base32 TOTP secret used in 2FA login flow.',
    'access_token': 'Existing access JWT token.',
    'refresh_token': 'Existing refresh token used for token rotation.',
    'request_opts': 'Optional transport overrides (timeout/headers/header profile options).',
    'config': 'Optional SDKConfig object controlling runtime behavior.',
    'auto_login': 'When true, attempts authentication during client initialization.',
    'quantity': 'Number of records to fetch.',
    'start_page': 'Zero-based page number offset.',
    'page_num': 'Zero-based page number to request.',
    'loan_id': 'Loan identifier.',
    'amount': 'Monetary amount for purchase operations.',
    'lang': 'Agreement language code (for example, "en").',
    'countries': 'List of country display names used as filter.',
    'originators': 'List of originator display names used as filter.',
    'loan_types': 'List of loan type keys used as filter.',
    'sort': 'Sort key; accepted values depend on method.',
    'ascending_sort': 'Sort direction; default false means descending.',
    'group_guarantee': 'When set, filters loans by group guarantee presence.',
    'exclude_invested_loans': 'When set, excludes loans already invested in.',
    'current': 'When true returns current investments; false returns finished.',
    'start_date': 'Date interval start.',
    'end_date': 'Date interval end.',
    'periodicity': 'Named date-range shortcut or aggregation period.',
    'period': 'Named period shortcut for transaction filters.',
    'transaction_types': 'List of transaction type keys used as filter.',
    'logout': 'Optional explicit override for logout-on-close behavior.',
    'max_remaining_term': 'Maximum remaining term filter for loans.',
    'min_remaining_term': 'Minimum remaining term filter for loans.',
    'max_interest_rate': 'Maximum interest rate filter.',
    'min_interest_rate': 'Minimum interest rate filter.',
    'max_available_amount': 'Maximum available amount filter for loans.',
    'min_available_amount': 'Minimum available amount filter for loans.',
    'max_selling_price': 'Maximum selling price filter for secondary-market listings.',
    'min_selling_price': 'Minimum selling price filter for secondary-market listings.',
    'max_date_of_purchase': 'Maximum purchase date filter for investments.',
    'min_date_of_purchase': 'Minimum purchase date filter for investments.',
    'max_invested_amount': 'Maximum invested amount filter for investments.',
    'min_invested_amount': 'Minimum invested amount filter for investments.',
    'only_my_sales': 'When set, returns only current investor sales.',
    'reduced_price_only': 'When set, returns only discounted listings.',
    'only_at_nominal_value': 'When set, returns only nominal-value listings.',
}

METHOD_PARAM_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    'get_profit_overview': {
        'periodicity': 'Aggregation step for points; must be one of day/month/year.',
    },
    'get_transactions': {
        'period': 'Optional named transaction range; today/thisWeek/thisMonth.',
    },
    'get_mass_transactions': {
        'period': 'Optional named transaction range; today/thisWeek/thisMonth.',
    },
    'get_loans': {
        'sort': 'Loan sort key; one of loan_id/term/issued_date/interest_rate/loan_amount.',
    },
    'get_loans_page': {
        'sort': 'Loan sort key; one of loan_id/term/issued_date/interest_rate/loan_amount.',
    },
    'get_secondary_loans': {
        'sort': 'Secondary-market sort key; one of remaining_term/loan_interest/remaining_principal/sale_amount/final_payment_date/sale_valid_until.',
    },
    'get_investments': {
        'sort': 'Investment sort key; accepted values depend on current flag.',
    },
    'purchase_loan': {
        'amount': 'EUR-denominated investment amount sent to API as string.',
    },
}

METHOD_RETURNS: Dict[str, str] = {
    '__init__': 'Initialized client instance.',
    'token': 'Bearer string in format "Bearer <access_token>".',
    'login': 'Bearer string in format "Bearer <access_token>".',
    'logout': 'Fixed success message string.',
    'get_agreement': 'Raw agreement bytes (file payload).',
    'get_mass_investments': 'Raw export file bytes.',
    'get_mass_transactions': 'Raw export file bytes.',
}

METHOD_EXCEPTIONS: Dict[str, Iterable[str]] = {
    '__init__': ['ValueError', 'PeerberryException'],
    'login': ['InvalidCredentials', 'PeerberryException'],
    'token': ['TokenRefreshError'],
    'close': ['PeerberryException (optional, when configured not to swallow logout errors)'],
    'get_profit_overview': ['InvalidPeriodicity', 'PeerberryException'],
    'get_loans': ['ValueError', 'TypeError', 'InvalidSort', 'PeerberryException'],
    'get_loans_page': ['ValueError', 'TypeError', 'InvalidSort', 'PeerberryException'],
    'get_secondary_loans': ['ValueError', 'TypeError', 'InvalidSort', 'PeerberryException'],
    'purchase_loan': ['InsufficientFunds', 'PeerberryException'],
    'get_investments': ['ValueError', 'TypeError', 'InvalidSort', 'PeerberryException'],
    'get_transactions': ['InvalidType', 'InvalidPeriodicity', 'PeerberryException'],
    'get_mass_transactions': ['InvalidType', 'InvalidPeriodicity', 'PeerberryException'],
    'get_mass_investments': ['TypeError', 'ValueError', 'PeerberryException'],
}

CONFIG_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    'RetryConfig': {
        'max_retries': 'Retry attempts after initial failure.',
        'backoff_factor': 'Exponential backoff multiplier.',
        'max_backoff': 'Maximum sleep duration between retries.',
        'retry_status_codes': 'HTTP status codes treated as retryable.',
        'retry_on_network_errors': 'Whether network/transport exceptions are retried.',
    },
    'TransportConfig': {
        'timeout': 'Default request timeout in seconds.',
        'retry': 'Retry policy configuration object.',
        'header_profile': 'Inline static headers merged into default request profile.',
        'header_profile_path': 'Path to JSON file containing static header profile.',
        'user_agent': 'Convenience override for x-app-user-agent.',
        'app_system': 'Convenience override for x-app-system.',
        'sec_ch_ua_platform': 'Convenience override for sec-ch-ua-platform.',
    },
    'AuthConfig': {
        'auto_refresh_on_auth_error': 'Refresh token automatically after auth failures.',
        'max_refresh_attempts': 'Refresh attempts for a failing request.',
        'proactive_refresh': 'Refresh access token before expiry when possible.',
        'proactive_refresh_skew_seconds': 'Seconds before expiry to trigger proactive refresh.',
        'token_store': 'Token store implementation used for load/save/clear.',
        'load_tokens_on_init': 'Load token pair from token store during client initialization.',
    },
    'ObservabilityConfig': {
        'event_hook': 'Callback receiving sanitized event dictionaries.',
        'logger': 'Logger receiving structured SDK event messages.',
        'verbose_events': 'Enable request_start/request_end verbose events.',
        'redactor': 'Optional custom event redaction hook.',
    },
    'LifecycleConfig': {
        'logout_on_close': 'Whether PeerberryClient.close() should call logout().',
        'swallow_logout_errors': 'Suppress logout errors during close when true.',
    },
    'SDKConfig': {
        'transport': 'Transport-related runtime configuration.',
        'auth': 'Authentication/token lifecycle configuration.',
        'observability': 'Event and logging configuration.',
        'lifecycle': 'Client-close and logout behavior configuration.',
    },
}


def _format_annotation(annotation: Any) -> str:
    if annotation is inspect.Signature.empty:
        return 'Any'

    if isinstance(annotation, str):
        return annotation

    text = inspect.formatannotation(annotation)
    text = text.replace('typing.', '')
    text = text.replace('NoneType', 'None')
    text = text.replace('peerberry_sdk.models.entities.', '')
    text = text.replace('peerberry_sdk.config.', '')
    text = text.replace('peerberry_sdk.token_store.', '')

    return text


def _format_default(value: Any) -> str:
    if value is inspect.Signature.empty:
        return 'Required'

    if isinstance(value, str):
        return f'"{value}"'

    return repr(value)


def _callable_signature(func: Any, *, strip_self: bool = True) -> inspect.Signature:
    signature = inspect.signature(func)

    if not strip_self:
        return signature

    filtered = [
        parameter
        for parameter in signature.parameters.values()
        if parameter.name != 'self'
    ]

    return signature.replace(parameters=filtered)


def _parse_sphinx_docstring(docstring: str) -> Tuple[str, Dict[str, str], Optional[str], Dict[str, str]]:
    if not docstring:
        return '', {}, None, {}

    lines = docstring.splitlines()
    summary_parts = []
    parameter_docs: Dict[str, str] = {}
    return_doc: Optional[str] = None
    raise_docs: Dict[str, str] = {}

    current_param = None
    in_return = False

    param_pattern = re.compile(r'^:param\s+(\w+)\s*:\s*(.*)$')
    return_pattern = re.compile(r'^:return\s*:\s*(.*)$')
    raise_pattern = re.compile(r'^:raises?\s+([\w\.]+)\s*:\s*(.*)$')

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            current_param = None
            in_return = False
            continue

        param_match = param_pattern.match(stripped)
        if param_match:
            current_param = param_match.group(1)
            in_return = False
            parameter_docs[current_param] = param_match.group(2).strip()
            continue

        return_match = return_pattern.match(stripped)
        if return_match:
            current_param = None
            in_return = True
            return_doc = return_match.group(1).strip()
            continue

        raise_match = raise_pattern.match(stripped)
        if raise_match:
            current_param = None
            in_return = False
            raise_type = raise_match.group(1).strip()
            raise_desc = raise_match.group(2).strip()
            raise_docs[raise_type] = raise_desc
            continue

        if stripped.startswith(':'):
            current_param = None
            in_return = False
            continue

        if current_param is not None:
            parameter_docs[current_param] = f"{parameter_docs[current_param]} {stripped}".strip()
            continue

        if in_return and return_doc is not None:
            return_doc = f"{return_doc} {stripped}".strip()
            continue

        summary_parts.append(stripped)

    summary = ' '.join(summary_parts).strip()

    return summary, parameter_docs, return_doc, raise_docs


def _resolve_method_description(method_name: str, doc_summary: str) -> str:
    if method_name in METHOD_SUMMARIES:
        return METHOD_SUMMARIES[method_name]

    if doc_summary:
        return doc_summary

    return 'No summary available.'


def _resolve_parameter_description(method_name: str, parameter_name: str, doc_parameters: Mapping[str, str]) -> str:
    method_descriptions = METHOD_PARAM_DESCRIPTIONS.get(method_name, {})
    if parameter_name in method_descriptions:
        return method_descriptions[parameter_name]

    if parameter_name in doc_parameters and doc_parameters[parameter_name]:
        return doc_parameters[parameter_name]

    if parameter_name in COMMON_PARAM_DESCRIPTIONS:
        return COMMON_PARAM_DESCRIPTIONS[parameter_name]

    return 'No detailed description available.'


def _resolve_return_description(method_name: str, doc_return: Optional[str]) -> str:
    if method_name in METHOD_RETURNS:
        return METHOD_RETURNS[method_name]

    if doc_return:
        return doc_return

    return 'See return type annotation.'


def _resolve_method_exception_hints(method_name: str, doc_raises: Mapping[str, str]) -> Iterable[str]:
    configured = list(METHOD_EXCEPTIONS.get(method_name, []))
    from_docstrings = list(doc_raises.keys())
    combined = configured + from_docstrings

    if not combined:
        combined = ['PeerberryException']

    deduped = []
    for exception_name in combined:
        if exception_name not in deduped:
            deduped.append(exception_name)

    return deduped


def _format_signature_for_display(method_name: str, func: Any) -> str:
    signature = _callable_signature(func)
    rendered = _stringify_signature(signature)

    if method_name == '__init__':
        return f'PeerberryClient{rendered}'

    return f'api.{method_name}{rendered}'


def _format_method_anchor(method_name: str) -> str:
    if method_name == '__init__':
        return 'PeerberryClient(...)'

    return f'{method_name}(...)'


def _stringify_signature(signature: inspect.Signature) -> str:
    rendered_parameters = []
    seen_var_positional = False
    inserted_kw_only_separator = False

    for parameter in signature.parameters.values():
        prefix = ''
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            prefix = '*'
            seen_var_positional = True
        elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
            prefix = '**'
        elif parameter.kind is inspect.Parameter.KEYWORD_ONLY and not seen_var_positional and not inserted_kw_only_separator:
            rendered_parameters.append('*')
            inserted_kw_only_separator = True

        part = f'{prefix}{parameter.name}'
        if parameter.annotation is not inspect.Signature.empty:
            part += f': {_format_annotation(parameter.annotation)}'

        if parameter.default is not inspect.Signature.empty:
            part += f' = {_format_default(parameter.default)}'

        rendered_parameters.append(part)

    rendered = f"({', '.join(rendered_parameters)})"

    if signature.return_annotation is not inspect.Signature.empty:
        rendered += f' -> {_format_annotation(signature.return_annotation)}'

    return rendered


def _render_accepted_values_for_method(method_name: str) -> Iterable[str]:
    lines = []

    if method_name in {'get_loans', 'get_loans_page'}:
        values = ', '.join(sorted(CONSTANTS.LOAN_SORT_TYPES.keys()))
        lines.append(f'`sort`: `{values}`')

    if method_name == 'get_secondary_loans':
        values = ', '.join(sorted(CONSTANTS.SECONDARY_LOAN_SORT_TYPES.keys()))
        lines.append(f'`sort`: `{values}`')

    if method_name == 'get_investments':
        current_values = ', '.join(sorted(CONSTANTS.CURRENT_INVESTMENT_SORT_TYPES.keys()))
        finished_values = ', '.join(sorted(CONSTANTS.FINISHED_INVESTMENT_SORT_TYPES.keys()))
        lines.append(f'`sort` when `current=True`: `{current_values}`')
        lines.append(f'`sort` when `current=False`: `{finished_values}`')

    if method_name in {'get_loans', 'get_loans_page', 'get_secondary_loans', 'get_investments'}:
        loan_types = ', '.join(sorted(CONSTANTS.LOAN_TYPES_ID.keys()))
        lines.append(f'`loan_types`: `{loan_types}`')

    if method_name == 'get_profit_overview':
        periodicities = ', '.join(sorted(CONSTANTS.PERIODICITIES))
        lines.append(f'`periodicity`: `{periodicities}`')

    if method_name in {'get_transactions', 'get_mass_transactions'}:
        periodicities = ', '.join(sorted(CONSTANTS.TRANSACTION_PERIODICITIES))
        types_ = ', '.join(sorted(CONSTANTS.TRANSACTION_TYPES.keys()))
        lines.append(f'`period`: `{periodicities}`')
        lines.append(f'`transaction_types` named keys: `{types_}`')
        lines.append('`transaction_types` numeric IDs: any positive integer (for example `14`)')

    return lines


def _iter_api_callables() -> Dict[str, Any]:
    callables: Dict[str, Any] = {}

    for name, attribute in PeerberryClient.__dict__.items():
        if name.startswith('__') and name != '__init__':
            continue

        if name.startswith('_') and name != '__init__':
            continue

        function = None
        if isinstance(attribute, staticmethod):
            function = attribute.__func__
        elif isinstance(attribute, classmethod):
            function = attribute.__func__
        elif inspect.isfunction(attribute):
            function = attribute

        if function is not None:
            callables[name] = function

    return callables


def _render_dataclass_table(config_class: Any) -> Iterable[str]:
    class_name = config_class.__name__
    lines = [f'### `{class_name}`', '', '| Field | Type | Default | Description |', '| --- | --- | --- | --- |']

    for field_info in fields(config_class):
        field_name = field_info.name
        annotation = _format_annotation(field_info.type)

        if field_info.default is not MISSING:
            default = _format_default(field_info.default)
        elif field_info.default_factory is not MISSING:  # type: ignore[attr-defined]
            default_factory = field_info.default_factory  # type: ignore[attr-defined]
            default_name = getattr(default_factory, '__name__', type(default_factory).__name__)
            default = f'{default_name}()'
        else:
            default = 'Required'

        description = CONFIG_DESCRIPTIONS.get(class_name, {}).get(field_name, 'No description available.')

        lines.append(f'| `{field_name}` | `{annotation}` | `{default}` | {description} |')

    lines.append('')

    return lines


def _render_method_section(method_name: str, func: Any) -> Iterable[str]:
    docstring = inspect.getdoc(func) or ''
    doc_summary, doc_parameters, doc_return, doc_raises = _parse_sphinx_docstring(docstring)
    method_description = _resolve_method_description(method_name, doc_summary)

    signature = _callable_signature(func)
    return_annotation = _format_annotation(signature.return_annotation)

    lines = [f'### `{_format_method_anchor(method_name)}`', '', method_description, '']

    lines.append('```python')
    lines.append(_format_signature_for_display(method_name, func))
    lines.append('```')
    lines.append('')

    parameters = list(signature.parameters.values())
    if parameters:
        lines.append('| Parameter | Type | Default | Description |')
        lines.append('| --- | --- | --- | --- |')

        for parameter in parameters:
            param_name = parameter.name
            param_type = _format_annotation(parameter.annotation)
            default_value = _format_default(parameter.default)
            description = _resolve_parameter_description(method_name, param_name, doc_parameters)
            lines.append(f'| `{param_name}` | `{param_type}` | `{default_value}` | {description} |')

        lines.append('')

    lines.append(f'- Returns: `{return_annotation}` - {_resolve_return_description(method_name, doc_return)}')

    accepted_values = list(_render_accepted_values_for_method(method_name))
    if accepted_values:
        lines.append('- Accepted values:')
        lines.extend(f'  - {entry}' for entry in accepted_values)

    exception_hints = list(_resolve_method_exception_hints(method_name, doc_raises))
    if exception_hints:
        formatted_exceptions = ', '.join(f'`{exception_name}`' for exception_name in exception_hints)
        lines.append(f'- Potential exceptions: {formatted_exceptions}')

    lines.append('')

    return lines


def _render_return_type_matrix(method_names: Iterable[str], callables: Mapping[str, Any]) -> Iterable[str]:
    lines = ['## Return Type Matrix', '', '| Method | Return Type |', '| --- | --- |']

    for method_name in method_names:
        if method_name not in callables:
            continue

        signature = _callable_signature(callables[method_name])
        return_annotation = _format_annotation(signature.return_annotation)

        display_name = 'PeerberryClient(...)' if method_name == '__init__' else f'{method_name}()'
        lines.append(f'| `{display_name}` | `{return_annotation}` |')

    lines.append('')

    return lines


def _render_docstring_coverage(callables: Mapping[str, Any]) -> Iterable[str]:
    documented = []
    missing = []

    for method_name, func in callables.items():
        if inspect.getdoc(func):
            documented.append(method_name)
        else:
            missing.append(method_name)

    lines = ['## Docstring Coverage Snapshot', '']

    total = len(callables)
    documented_count = len(documented)
    lines.append(f'- Public callable count: `{total}`')
    lines.append(f'- With docstrings: `{documented_count}`')
    lines.append(f'- Without docstrings: `{len(missing)}`')

    if missing:
        lines.append(f'- Missing docstrings: `{", ".join(missing)}`')

    lines.append('')

    return lines


def _render_content() -> str:
    api_callables = _iter_api_callables()
    ordered_methods = [name for _, methods in METHOD_GROUPS for name in methods if name in api_callables]

    lines = [
        '# API Client Reference (Generated)',
        '',
        'This page is generated from source code signatures, constants, and method docstrings.',
        'Do not edit this file manually; edit `docs/gen_client_reference.py` and source docstrings instead.',
        '',
        'For low-level symbol browsing, use [Generated Module Reference](reference.md).',
        '',
        '## SDK Configuration Schema',
        '',
        'These dataclass tables are generated directly from `peerberry_sdk.config`.',
        '',
    ]

    for config_class in (RetryConfig, TransportConfig, AuthConfig, ObservabilityConfig, LifecycleConfig, SDKConfig):
        lines.extend(_render_dataclass_table(config_class))

    lines.extend(['## API Methods', ''])

    for group_title, group_methods in METHOD_GROUPS:
        lines.append(f'## {group_title}')
        lines.append('')

        for method_name in group_methods:
            func = api_callables.get(method_name)
            if func is None:
                continue

            lines.extend(_render_method_section(method_name, func))

    lines.extend(_render_return_type_matrix(ordered_methods, api_callables))
    lines.extend(_render_docstring_coverage(api_callables))

    lines.extend([
        '## Source of Accepted Value Sets',
        '',
        '- Loan sort keys: `peerberry_sdk.constants.CONSTANTS.LOAN_SORT_TYPES`',
        '- Secondary-market sort keys: `peerberry_sdk.constants.CONSTANTS.SECONDARY_LOAN_SORT_TYPES`',
        '- Investment sort keys: `CONSTANTS.CURRENT_INVESTMENT_SORT_TYPES` / `CONSTANTS.FINISHED_INVESTMENT_SORT_TYPES`',
        '- Loan type keys: `CONSTANTS.LOAN_TYPES_ID`',
        '- Profit periodicities: `CONSTANTS.PERIODICITIES`',
        '- Transaction periodicities: `CONSTANTS.TRANSACTION_PERIODICITIES`',
        '- Transaction type keys: `CONSTANTS.TRANSACTION_TYPES`',
        '',
        '## Improving Generated Detail',
        '',
        'To enrich this page, improve method docstrings in source code with explicit parameter/return/raise details.',
    ])

    return '\n'.join(lines).rstrip() + '\n'


def _open_output(path: str):
    if mkdocs_gen_files is not None:
        return mkdocs_gen_files.open(path, 'w')

    target_path = PROJECT_ROOT / 'docs' / path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    return target_path.open('w', encoding='utf-8')


def write_client_reference() -> None:
    content = _render_content()

    with _open_output(OUTPUT_PATH) as fd:
        fd.write(content)


write_client_reference()

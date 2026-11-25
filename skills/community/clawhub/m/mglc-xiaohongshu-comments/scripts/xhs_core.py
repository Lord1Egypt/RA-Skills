"""Small, self-contained client for the six published Xiaohongshu products."""
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

ORIGIN = 'https://api.we-media.cn'
ENDPOINTS = {
    'note': ('xiaohongshu-note-detail', '/xiaohongshu/notes/detail'),
    'search_notes': ('xiaohongshu-search-notes', '/xiaohongshu/search/notes'),
    'search_authors': ('xiaohongshu-search-users', '/xiaohongshu/search/users'),
    'author': ('xiaohongshu-author-profile', '/xiaohongshu/accounts/profile'),
    'author_notes': ('xiaohongshu-author-notes', '/xiaohongshu/accounts/notes'),
    'comments': ('xiaohongshu-comments', '/xiaohongshu/notes/comments'),
}
PAGED = {'search_notes', 'search_authors', 'author_notes', 'comments'}
SORTS = {'general', 'time_descending', 'popularity_descending'}
ID = re.compile(r'^[0-9a-f]{24}$')
# These gateway errors are returned only after refundCall succeeds. A failed
# refund has its own BILLING_REFUND_FAILED code. Never generalize to all 4xx/5xx.
REFUNDED_ERRORS = {'UPSTREAM_REJECTED', 'UPSTREAM_UNAVAILABLE',
                   'UPSTREAM_BUSINESS_REJECTED', 'INVALID_UPSTREAM_RESPONSE'}


class XhsError(Exception):
    def __init__(self, code, message, *, retry_after=None, call_id=None):
        self.code, self.message, self.retry_after = code, message, retry_after
        self.call_id = call_id
        super().__init__(message)


def safe_diagnostic(value, secret=''):
    """Keep gateway diagnostics without persisting echoed credentials."""
    if isinstance(value, dict):
        private = {'authorization', 'cookie', 'cookies', 'apikey', 'xapikey',
                   'accesstoken', 'refreshtoken', 'usertoken', 'devicetoken',
                   'xsectoken', 'xs', 'xscommon', 'xt', 'signature', 'sign',
                   'password', 'secret'}
        return {k: '[redacted]' if re.sub(r'[-_]', '', str(k)).lower() in private
                else safe_diagnostic(v, secret) for k, v in value.items()}
    if isinstance(value, list):
        return [safe_diagnostic(v, secret) for v in value]
    if isinstance(value, str):
        if secret:
            value = value.replace(secret, '[redacted]')
        return re.sub(r'ach_live_[A-Za-z0-9_-]+', '[redacted]', value)
    return value


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    preserve = False
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        for attempt in range(7):
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                # AV/indexer readers can briefly deny replacement on Windows.
                # Retry only the local rename, never a paid request.
                if attempt == 6:
                    preserve = True
                    raise
                time.sleep(0.01 * (2 ** attempt))
    finally:
        if os.path.exists(tmp) and not preserve:
            os.unlink(tmp)


@contextmanager
def workspace_lock(path):
    """OS lock is released even if the process dies; no stale-lock deletion."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    with (path / '.lock').open('a+b') as f:
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(b'0')
            f.flush()
        f.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise XhsError('WORKSPACE_BUSY', '该任务正在运行，请等待完成。') from None
        try:
            yield
        finally:
            f.seek(0)
            if os.name == 'nt':
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def money(value):
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0 or amount * 1000000 != (amount * 1000000).to_integral_value():
            raise ValueError()
        return int(amount * 1000000)
    except (ValueError, InvalidOperation, TypeError):
        raise XhsError('INVALID_AMOUNT', '金额须为非负数，最多六位小数。') from None


def positive(value, name, maximum=10000):
    if type(value) is not int or not 1 <= value <= maximum:
        raise XhsError('INVALID_PLAN', f'{name} 须为 1–{maximum} 的整数。')
    return value


def link(value):
    if not isinstance(value, str):
        raise XhsError('INVALID_INPUT', '请提供一条小红书链接或分享文本。')
    urls = re.findall(r'https?://[^\s<>\[\]"\u3000]+', value)
    if len(urls) != 1:
        raise XhsError('INVALID_INPUT', '每个输入应包含且仅包含一条小红书链接。')
    url = urls[0].rstrip('，。！？；,.;!?)）】')
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme not in ('https', 'http') or parsed.username or parsed.password
            or parsed.hostname not in ('xiaohongshu.com', 'www.xiaohongshu.com', 'xhslink.cn', 'xhslink.com')
            or parsed.port not in (None, 80, 443)):
        raise XhsError('INVALID_INPUT', '链接必须属于小红书或其官方分享短链域名。')
    return url


def validate_input(operation, value):
    if not isinstance(value, dict):
        raise XhsError('INVALID_PLAN', 'input 必须是 JSON 对象。')
    allowed = ({'keyword', 'sort'} if operation == 'search_notes' else {'keyword'} if operation == 'search_authors'
               else {'url', 'userId'} if operation in ('author', 'author_notes') else {'url'})
    if set(value) - allowed:
        raise XhsError('INVALID_PLAN', 'input 含不支持的参数。')
    out = dict(value)
    if operation.startswith('search_'):
        if not isinstance(out.get('keyword'), str) or not 1 <= len(out['keyword'].strip()) <= 200:
            raise XhsError('INVALID_INPUT', '关键词须为 1–200 个字符。')
        out['keyword'] = out['keyword'].strip()
        if operation == 'search_notes':
            out.setdefault('sort', 'general')
            if out['sort'] not in SORTS:
                raise XhsError('INVALID_INPUT', '排序只支持 general、time_descending、popularity_descending。')
    elif operation in ('author', 'author_notes'):
        if ('url' in out) == ('userId' in out):
            raise XhsError('INVALID_INPUT', '作者主页 url 与 userId 必须且只能提供一项。')
        if 'userId' in out and (not isinstance(out['userId'], str) or not ID.fullmatch(out['userId'])):
            raise XhsError('INVALID_INPUT', 'userId 须为 24 位作者 ID，不是展示的小红书号。')
    elif 'url' not in out:
        raise XhsError('INVALID_INPUT', '缺少作品 url。')
    if 'url' in out:
        out['url'] = link(out['url'])
    return out


def normalize_plan(mode, plan):
    if not isinstance(plan, dict):
        raise XhsError('INVALID_PLAN', '计划须为 JSON 对象。')
    p = dict(plan)
    if mode in ENDPOINTS:
        allowed = {'input', 'maxPages', 'maxItems'} if mode in PAGED else {'input'}
        if set(p) - allowed:
            raise XhsError('INVALID_PLAN', '计划含不支持的字段。')
        p['input'] = validate_input(mode, p.get('input'))
        if mode in PAGED:
            p['maxPages'] = positive(p.get('maxPages', 1), 'maxPages', 1000)
            if p.get('maxItems') is not None:
                positive(p['maxItems'], 'maxItems')
        return p
    if mode not in ('competitor', 'insight', 'topics'):
        raise XhsError('INVALID_PLAN', '未知工作流。')
    allowed = {'maxNotes', 'commentsPerNote', 'commentPages', 'includeDetails'}
    allowed |= {'author', 'listPages'} if mode == 'competitor' else {'keyword', 'sort', 'searchPages', 'urls'}
    if set(p) - allowed:
        raise XhsError('INVALID_PLAN', '计划含不支持的字段。')
    p['maxNotes'] = positive(p.get('maxNotes', 20), 'maxNotes', 1000)
    p['commentsPerNote'] = p.get('commentsPerNote', 20 if mode == 'insight' else 0)
    if type(p['commentsPerNote']) is not int or not 0 <= p['commentsPerNote'] <= 1000:
        raise XhsError('INVALID_PLAN', 'commentsPerNote 须为 0–1000 的整数。')
    if mode == 'insight' and p['commentsPerNote'] == 0:
        raise XhsError('INVALID_PLAN', '评论洞察需要至少一条评论的读取额度。')
    p['commentPages'] = positive(p.get('commentPages', 3), 'commentPages', 1000)
    p['includeDetails'] = p.get('includeDetails', True)
    if type(p['includeDetails']) is not bool:
        raise XhsError('INVALID_PLAN', 'includeDetails 须为布尔值。')
    if mode in ('competitor', 'topics') and not p['includeDetails']:
        raise XhsError('INVALID_PLAN', '账号研究和选题研究需要正文；仅需列表请使用基础 Skill。')
    if mode == 'competitor':
        p['author'] = validate_input('author', p.get('author'))
        p['listPages'] = positive(p.get('listPages', 3), 'listPages', 1000)
    elif 'urls' in p:
        if set(p) & {'keyword', 'sort', 'searchPages'}:
            raise XhsError('INVALID_PLAN', 'urls 与关键词搜索设置不能混用。')
        if not isinstance(p['urls'], list) or not 1 <= len(p['urls']) <= p['maxNotes']:
            raise XhsError('INVALID_PLAN', 'urls 须为非空列表，且不超过 maxNotes。')
        p['urls'] = list(dict.fromkeys(link(x) for x in p['urls']))
    else:
        p.update(validate_input('search_notes', {k: p[k] for k in ('keyword', 'sort') if k in p}))
        p['searchPages'] = positive(p.get('searchPages', 3), 'searchPages', 1000)
    return p


def call_caps(mode, plan):
    if mode in ENDPOINTS:
        return {mode: plan.get('maxPages', 1)}
    count = len(plan['urls']) if 'urls' in plan else plan['maxNotes']
    caps = {}
    if mode == 'competitor':
        caps.update(author=1, author_notes=plan['listPages'])
    elif 'urls' not in plan:
        caps['search_notes'] = plan['searchPages']
    if plan['includeDetails']:
        caps['note'] = count
    if plan['commentsPerNote']:
        caps['comments'] = count * plan['commentPages']
    return caps


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise XhsError('REDIRECT_REFUSED', '网关发生重定向，已停止，密钥未转发。')


class Client:
    def __init__(self, identity, key=None):
        self.identity = identity
        self.key = key if key is not None else (os.environ.get('WM_API_KEY') or os.environ.get('MANGYUN_API_KEY') or '')
        self.key_hash = hashlib.sha256(self.key.encode()).hexdigest()
        # Cached Windows proxy lookup from the existing released skill workflow.
        from transport import CachedProxyHandler
        self.opener = urllib.request.build_opener(CachedProxyHandler(), NoRedirect())

    def request(self, path, body=None, idem=None):
        if not path.startswith('/') or path.startswith('//'):
            raise XhsError('INVALID_PATH', '网关路径无效。')
        headers = {'Accept': 'application/json', 'User-Agent': '{slug}/{version} (source={channel})'.format(**self.identity),
                   'X-WM-Source': self.identity['slug'], 'X-Source': self.identity['channel']}
        if self.key:
            headers['X-API-Key'] = self.key
        if idem:
            headers['Idempotency-Key'] = idem
        data = None
        if body is not None:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body, ensure_ascii=False).encode()
        req = urllib.request.Request(ORIGIN + path, data=data, headers=headers)
        try:
            response = self.opener.open(req, timeout=120)
        except urllib.error.HTTPError as e:
            response = e
        try:
            with response:
                raw = response.read(20 * 1024 * 1024 + 1)
                if len(raw) > 20 * 1024 * 1024:
                    raise XhsError('RESPONSE_TOO_LARGE', '响应超过 20MB，保留当前任务等待复核。')
                payload = json.loads(raw)
                if not isinstance(payload, dict):
                    raise ValueError()
                return response.status, {k.lower(): v for k, v in response.headers.items()}, payload
        except (ValueError, UnicodeError):
            raise XhsError('INVALID_RESPONSE', '网关未返回可识别的 JSON，结果与费用待核对。') from None

    def catalog(self):
        root = '/api/v1/products' if self.key else '/api/v1/public/products'
        products = {}
        for page in range(1, 101):
            status, _, payload = self.request(root + f'?pageSize=100&page={page}')
            if status != 200 or payload.get('code') != 'OK':
                raise XhsError(str(payload.get('code', 'CATALOG_FAILED')), '无法取得当前产品目录和价格。')
            data = payload.get('data', {})
            batch = data.get('items')
            if not isinstance(batch, list):
                raise XhsError('INVALID_CATALOG', '产品目录格式异常。')
            for product in batch:
                if isinstance(product, dict) and product.get('slug') in {x[0] for x in ENDPOINTS.values()}:
                    products[product['slug']] = product
            total = (data.get('pagination') or {}).get('total')
            if len(batch) < 100 or (type(total) is int and page * 100 >= total):
                return products
        raise XhsError('INVALID_CATALOG', '产品目录分页未结束。')


def prices_for(catalog, caps):
    prices = {}
    for op in caps:
        slug, path = ENDPOINTS[op]
        product = catalog.get(slug)
        if not product or product.get('publicMethod') != 'POST' or product.get('publicPath') != path:
            raise XhsError('CONTRACT_CHANGED', f'{slug} 不在当前目录或接口契约发生变化。')
        price = product.get('priceMicros')
        if type(price) is not int or price < 0:
            raise XhsError('INVALID_PRICE', '当前价格不可用。')
        # Current six products are fixed-price requests. Fail explicitly if that changes.
        if product.get('billingUnit') != 'request' or any(
            p.get('billByQuantity') or p.get('unitPriceMicros') or p.get('valuePriceAdjustmentsBps')
            or p.get('shortLinkPriceAdjustmentBps') for p in product.get('parameters', [])):
            raise XhsError('PRICING_CHANGED', '该产品计费规则已变化，请更新 Skill。')
        if any(p.get('priceAdjustmentsBps') for p in product.get('parameterGroups', [])):
            raise XhsError('PRICING_CHANGED', '该产品参数组合计费已变化，请更新 Skill。')
        prices[op] = price
    return prices


def validate_data(op, payload):
    data = payload.get('data')
    if not isinstance(data, dict) or data.get('ok') is False:
        raise XhsError('INVALID_RESPONSE', '业务数据格式异常。')
    if op in PAGED:
        if not isinstance(data.get('items'), list) or 'hasMore' not in data or (data['hasMore'] is not None and type(data['hasMore']) is not bool):
            raise XhsError('INVALID_RESPONSE', '分页缺少 items 或有效 hasMore。')
        field = 'userId' if op == 'search_authors' else 'commentId' if op == 'comments' else 'noteId'
        if any(not isinstance(x, dict) or not isinstance(x.get(field), str) or not x[field] for x in data['items']):
            raise XhsError('INVALID_RESPONSE', '分页条目缺少身份标识。')
        if type(data.get('count')) is not int or data['count'] != len(data['items']):
            raise XhsError('INVALID_RESPONSE', '分页条数与实际条目不一致。')
    elif op == 'note':
        if not isinstance(data.get('note'), dict) or not ID.fullmatch(str(data['note'].get('noteId', ''))):
            raise XhsError('INVALID_RESPONSE', '作品详情缺少有效作品 ID。')
    else:
        author = data.get('author')
        if not isinstance(author, dict) or not isinstance(author.get('user'), dict) or not ID.fullmatch(str(author['user'].get('userId', ''))):
            raise XhsError('INVALID_RESPONSE', '作者档案缺少有效作者 ID。')
    rows = data.get('items', []) if op in PAGED else [data['note']] if op == 'note' else []
    for row in rows:
        for key in ('author', 'metrics'):
            if row.get(key) is not None and not isinstance(row[key], dict):
                raise XhsError('INVALID_RESPONSE', '条目嵌套资料格式异常。')
        if op == 'comments' and row.get('replies') is not None and (not isinstance(row['replies'], list) or any(not isinstance(r, dict) for r in row['replies'])):
            raise XhsError('INVALID_RESPONSE', '评论内嵌回复格式异常。')
    return data


class Job:
    def __init__(self, workspace, mode, plan, client, prices, budget):
        self.path = Path(workspace) / '.private-state.json'
        self.records = Path(workspace) / '.requests'
        self.client, self.prices, self.budget = client, prices, budget
        self.scope = {'mode': mode, 'plan': plan}
        if not self.path.exists() and self.records.exists() and any(self.records.glob('*.json')):
            raise XhsError('WORKSPACE_INCOMPLETE', '请求记录存在但任务元数据缺失，请先恢复原工作区。')
        self.state = read_json(self.path) if self.path.exists() else {
            'version': 2, 'jobId': str(uuid.uuid4()), 'scope': self.scope, 'keyHash': client.key_hash, 'createdAt': now()}
        if self.state.get('version') != 2:
            raise XhsError('WORKSPACE_VERSION', '工作区版本不兼容，请保留旧目录用于核对。')
        if self.state.get('scope') != self.scope or self.state.get('keyHash') != client.key_hash:
            raise XhsError('WORKSPACE_MISMATCH', '工作区属于另一任务或密钥，请保留原任务并使用新的输出目录。')
        self.state['requests'] = {}
        for record in self.records.glob('*.json'):
            saved = read_json(record)
            entry = saved.get('entry', {})
            if (saved.get('jobId') != self.state['jobId'] or record.stem != digest([entry.get('operation'), entry.get('params')])):
                raise XhsError('WORKSPACE_MISMATCH', '请求记录与原任务不一致。')
            self.state['requests'][record.stem] = entry
        self.save()

    def save(self, fingerprint=None):
        if fingerprint is None:
            write_json(self.path, {k: v for k, v in self.state.items() if k != 'requests'})
        else:
            # One receipt per file avoids rewriting all prior bodies for every page.
            write_json(self.records / (fingerprint + '.json'), {
                'jobId': self.state['jobId'], 'entry': self.state['requests'][fingerprint]})

    def cost(self):
        known = {}
        reserved = 0
        for fingerprint, entry in self.state['requests'].items():
            if entry.get('chargeMicros') is not None:
                receipt = entry.get('callId') or fingerprint
                known[receipt] = max(known.get(receipt, 0), entry['chargeMicros'])
            elif entry['status'] != 'failed_unbilled':
                reserved += entry['reservedMicros']
        return {'confirmedMicros': sum(known.values()), 'unresolvedReservedMicros': reserved}

    def call(self, op, params):
        fp = digest([op, params])
        requests = self.state['requests']
        entry = requests.get(fp)
        if entry and entry['status'] == 'done':
            if entry.get('chargeMicros') is None:
                raise XhsError('BILLING_UNKNOWN', '此已保存请求缺少费用回执，需核对账单后继续。')
            if sum(self.cost().values()) > self.budget:
                raise XhsError('BUDGET_LIMIT', '当前预算小于任务已发生及待核对的费用。')
            return entry['data']
        if entry and entry['status'] in ('failed', 'failed_unbilled'):
            raise XhsError(entry['errorCode'], entry.get('errorMessage') or '该请求已被网关拒绝，已保留进度；未自动更换幂等键重试。',
                           retry_after=entry.get('retryAfter'), call_id=entry.get('callId'))
        if entry is None:
            cost = self.cost()
            if sum(cost.values()) + self.prices[op] > self.budget:
                raise XhsError('BUDGET_LIMIT', '已达到任务预算；已保存结果，可提高原任务预算后继续。')
            entry = requests[fp] = {'operation': op, 'params': params, 'idempotencyKey': str(uuid.uuid4()),
                                    'status': 'pending', 'reservedMicros': self.prices[op], 'createdAt': now()}
            self.save(fp)
        slug, path = ENDPOINTS[op]
        try:
            status, headers, payload = self.client.request('/openapi/' + slug + path, params, entry['idempotencyKey'])
        except Exception:
            entry['status'] = 'unknown'
            self.save(fp)
            raise XhsError('RESULT_UNKNOWN', '请求结果暂时未知；重新运行原任务会沿用原幂等键核对，避免重复扣费。') from None
        entry.update(callId=headers.get('x-call-id') or payload.get('requestId'), observedAt=now(),
                     replay=headers.get('x-idempotent-replay') == 'true')
        try:
            header_charge = int(headers['x-charge-micros']) if 'x-charge-micros' in headers else None
            body_charge = money(payload['consumption']) if 'consumption' in payload else None
            charge = header_charge if header_charge is not None else body_charge
            if entry['replay'] and body_charge is not None:
                charge = max(charge or 0, body_charge)
            if charge is not None and charge < 0:
                raise ValueError()
        except (ValueError, XhsError):
            entry['status'] = 'unknown'
            self.save(fp)
            raise XhsError('BILLING_UNKNOWN', '费用回执格式异常，已保存请求，需核对账单。') from None
        entry['chargeMicros'] = charge
        if charge is not None:
            entry['billingBasis'] = 'charge_receipt'
        code = payload.get('code')
        if status >= 400 or code != 'OK':
            diagnostic = safe_diagnostic({k: payload[k] for k in ('code', 'message', 'details') if k in payload},
                                         getattr(self.client, 'key', ''))
            message = diagnostic.get('message')
            if not isinstance(message, str) or not message.strip():
                message = '网关未完成该请求；已保存结果和费用状态。'
            entry.update(status='failed', errorCode=str(code or f'HTTP_{status}'), errorMessage=message,
                         httpStatus=status, errorResponse=diagnostic, retryAfter=headers.get('retry-after'))
            if charge is None and status == 502 and code in REFUNDED_ERRORS and entry.get('callId'):
                charge = entry['chargeMicros'] = 0
                entry['billingBasis'] = 'gateway_refund_contract'
            if charge == 0:
                entry['status'] = 'failed_unbilled'
            self.save(fp)
            raise XhsError(entry['errorCode'], message, retry_after=entry['retryAfter'], call_id=entry.get('callId'))
        try:
            data = validate_data(op, payload)
            expected = re.search(r'/(?:explore|discovery/item)/([0-9a-f]{24})(?:[/?#]|$)', params.get('url', ''))
            if op == 'note' and expected and data['note']['noteId'] != expected[1]:
                raise XhsError('IDENTITY_MISMATCH', '详情响应与请求作品不一致。')
            if op == 'comments':
                ids = {x.get('noteId') for x in data['items'] if x.get('noteId')}
                if len(ids) > 1 or (expected and ids and ids != {expected[1]}):
                    raise XhsError('IDENTITY_MISMATCH', '评论响应混入其他作品。')
            if op == 'author' and params.get('userId') and data['author']['user']['userId'] != params['userId']:
                raise XhsError('IDENTITY_MISMATCH', '作者响应与请求不一致。')
        except XhsError as e:
            entry.update(status='failed', errorCode=e.code)
            self.save(fp)
            raise
        entry.update(status='done', data=data)
        self.save(fp)
        if charge is None:
            raise XhsError('BILLING_UNKNOWN', '数据已保存，但缺少费用回执，暂停后续付费读取。')
        if sum(self.cost().values()) > self.budget:
            raise XhsError('BUDGET_CHANGED', '实际回执超过预估预算，已停止后续读取，请核对实时价格。')
        return data


def note_link(note):
    for field in ('url', 'shareUrl', 'noteUrl'):
        if note.get(field):
            return link(note[field])
    if ID.fullmatch(str(note.get('noteId', ''))):
        return 'https://www.xiaohongshu.com/explore/' + note['noteId']
    raise XhsError('NOTE_LINK_MISSING', '作品没有可用于详情查询的链接或 ID。')


def pages(job, op, params, max_pages, max_items, target, coverage):
    field = 'userId' if op == 'search_authors' else 'commentId' if op == 'comments' else 'noteId'
    seen = {x[field] for x in target}
    cursor = None
    cursor_expires = None
    cursors = set()
    coverage.update(pages=0, reason='not_started', hasMore=None)
    for page in range(max_pages):
        query = dict(params)
        if cursor:
            query['cursor'] = cursor
            if cursor_expires and digest([op, query]) not in job.state['requests']:
                try:
                    expires = datetime.fromisoformat(cursor_expires.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    raise XhsError('CURSOR_EXPIRY_INVALID', '续页截止时间无法识别，请核对接口契约。') from None
                if expires.tzinfo is None or expires <= datetime.now(timezone.utc):
                    raise XhsError('CURSOR_EXPIRED', '原分页游标已到截止时间；已有结果保留，未自动从第一页重复付费读取。')
        data = job.call(op, query)
        coverage.update(pages=page + 1, hasMore=data['hasMore'], observedAt=data.get('observedAt'),
                        cursorExpiresAt=data.get('cursorExpiresAt'))
        for item in data['items']:
            if item[field] not in seen and (max_items is None or len(target) < max_items):
                row = dict(item)
                if op == 'comments':
                    row['sourceUrl'] = params['url']
                target.append(row)
                seen.add(item[field])
        if max_items is not None and len(target) >= max_items:
            coverage['reason'] = 'target_reached'
            return
        if data['hasMore'] is False:
            coverage['reason'] = 'end'
            return
        next_cursor = data.get('nextCursor')
        if not isinstance(next_cursor, str) or not next_cursor:
            coverage['reason'] = 'end_unknown'
            return
        if next_cursor in cursors:
            coverage['reason'] = 'cursor_repeated'
            raise XhsError('CURSOR_REPEATED', '服务端返回重复游标，已停止重复读取。')
        cursors.add(next_cursor)
        cursor = next_cursor
        cursor_expires = data.get('cursorExpiresAt')
    coverage['reason'] = 'page_limit'


def execute(job, mode, plan):
    result = {'mode': mode, 'notes': [], 'authors': [], 'comments': [], 'coverage': [],
              'errors': [], 'status': 'complete_within_scope', 'createdAt': now()}
    try:
        if mode in PAGED:
            target = result['authors' if mode == 'search_authors' else 'comments' if mode == 'comments' else 'notes']
            cover = {'operation': mode}
            result['coverage'].append(cover)
            pages(job, mode, plan['input'], plan['maxPages'], plan.get('maxItems'), target, cover)
        elif mode in ('note', 'author'):
            data = job.call(mode, plan['input'])
            row = dict(data['note' if mode == 'note' else 'author'])
            if mode == 'note':
                row['url'] = plan['input']['url']
            result['notes' if mode == 'note' else 'authors'].append(row)
        else:
            if mode == 'competitor':
                result['authors'].append(job.call('author', plan['author'])['author'])
                cover = {'operation': 'author_notes'}
                result['coverage'].append(cover)
                pages(job, 'author_notes', plan['author'], plan['listPages'], plan['maxNotes'], result['notes'], cover)
            elif 'urls' in plan:
                # Entries are resolved by their official detail response, not guessed from short links.
                result['notes'] = [{'url': u} for u in plan['urls']]
            else:
                cover = {'operation': 'search_notes'}
                result['coverage'].append(cover)
                pages(job, 'search_notes', {k: plan[k] for k in ('keyword', 'sort')}, plan['searchPages'],
                      plan['maxNotes'], result['notes'], cover)
            resolved = set()
            for index, original in enumerate(result['notes']):
                url = note_link(original)
                note = dict(original)
                note['detailStatus'] = 'not_requested'
                if plan['includeDetails']:
                    note = dict(job.call('note', {'url': url})['note'])
                    note['detailStatus'] = 'complete'
                note['url'] = url
                result['notes'][index] = note
                identity = note.get('noteId') or url
                if identity in resolved:
                    note['duplicateOf'] = str(identity)
                    continue
                resolved.add(identity)
                if plan['commentsPerNote']:
                    comments, cover = [], {'operation': 'comments', 'noteId': note.get('noteId'), 'url': url}
                    result['coverage'].append(cover)
                    try:
                        pages(job, 'comments', {'url': url}, plan['commentPages'], plan['commentsPerNote'], comments, cover)
                    finally:
                        result['comments'].extend(comments)
                    note['commentsStatus'] = cover['reason']
            result['notes'] = [n for n in result['notes'] if not n.get('duplicateOf')]
        if any(c.get('reason') == 'end_unknown' for c in result['coverage']):
            result['status'] = 'partial'
    except XhsError as e:
        result['status'] = 'partial'
        result['errors'].append({'code': e.code, 'message': e.message, 'retryAfter': e.retry_after})
        if e.call_id:
            result['errors'][-1]['callId'] = e.call_id
    result['cost'] = job.cost()
    result['requestCount'] = len(job.state['requests'])
    return result

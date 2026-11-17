"""Offline onboarding. Secrets never enter argv, logs or the source tree."""
import getpass
import json
import os
import stat
from pathlib import Path
from urllib.parse import urlsplit

from mosobleirc_core import MosOblEIRCError


def secure_directory(path):
    path = Path(path).absolute()
    # Reject symlink ancestors before creating or changing any permissions.
    for parent in [*reversed(path.parents), path]:
        if parent.is_symlink():
            raise MosOblEIRCError("setup directory must not contain symlinks")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    uid = getattr(os, "getuid", None)
    if not path.is_dir() or (uid is not None and path.stat().st_uid != uid()):
        raise MosOblEIRCError("setup directory must be owned by current user")
    path.chmod(0o700)
    return path


def write_new(path, text):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        stream.write(text)


def setup(data_root, transport=None, *, ask=input, secret=getpass.getpass):
    root = Path(data_root).expanduser().absolute()
    source = Path(__file__).resolve().parents[1]
    if root == source or source in root.parents:
        raise MosOblEIRCError("runtime must be outside the skill tree")
    transport = transport or ask('Transport (direct/yandex-relay): ').strip()
    if transport not in {'direct', 'yandex-relay'}:
        raise MosOblEIRCError('unknown transport')
    cfg = {'transport': transport, 'inventory_path': str(root/'config'/'inventory.json')}
    if transport == 'yandex-relay':
        url = ask('Private relay HTTPS URL: ').strip()
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise MosOblEIRCError('invalid relay URL')
        cfg['function_url'] = url
    name = 'provider_token' if transport == 'direct' else 'yandex_api_key'
    cfg['provider_token_path' if transport == 'direct' else 'api_key_path'] = str(root/'secrets'/name)
    # Refuse reruns before prompting for credentials; never replace existing state.
    targets = [root/'config'/'runtime.json', root/'config'/'inventory.json', root/'secrets'/name]
    if any(p.exists() or p.is_symlink() for p in targets):
        raise MosOblEIRCError('setup already exists; use a new data root or update configuration deliberately')
    token = secret('Provider token: ' if transport == 'direct' else 'Yandex API key: ').strip()
    if not token or len(token) > 16384 or any(c.isspace() or ord(c) < 32 for c in token):
        raise MosOblEIRCError('invalid secret')
    inventory = []
    seen_items, seen_meters = set(), set()
    def positive(prompt):
        raw = ask(prompt).strip()
        if not raw.isascii() or not raw.isdigit() or int(raw) <= 0:
            raise MosOblEIRCError('ID must be a positive integer')
        return int(raw)
    while ask('Добавить объект? (yes/no): ').strip().lower() == 'yes':
        item_id = positive('Item ID из личного кабинета: ')
        if item_id in seen_items:
            raise MosOblEIRCError('duplicate item ID')
        seen_items.add(item_id)
        item = {'item_id': item_id, 'name': ask('Название: '), 'address': ask('Адрес: '), 'meters': []}
        while ask('Добавить счётчик? (yes/no): ').strip().lower() == 'yes':
            meter_id = positive('Meter ID из личного кабинета: ')
            if meter_id in seen_meters:
                raise MosOblEIRCError('duplicate meter ID')
            seen_meters.add(meter_id)
            kind = ask('Тип (ColdWater/HotWater): ').strip()
            if kind not in {'ColdWater', 'HotWater'}:
                raise MosOblEIRCError('invalid meter type')
            item['meters'].append({'meter_id': meter_id, 'number': ask('Заводской номер: ').strip(), 'type': kind})
        inventory.append(item)
    created = []
    try:
        secure_directory(root)
        secure_directory(root/'config')
        secure_directory(root/'secrets')
        for path, value in [(targets[2], token), (targets[1], json.dumps(inventory, ensure_ascii=False)), (targets[0], json.dumps(cfg, ensure_ascii=False))]:
            write_new(path, value + '\n')
            created.append(path)
    except OSError:
        for path in created:
            path.unlink()
        raise MosOblEIRCError('setup could not write runtime files') from None

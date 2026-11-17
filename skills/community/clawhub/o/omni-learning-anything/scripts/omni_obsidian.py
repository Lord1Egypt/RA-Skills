"""Write only owned course notes/assets inside the selected local Vault."""
from pathlib import Path
from urllib.parse import quote
import omni_core as c
from omni_http import document_data, verified


def owned_file(path, contents, base):
    if not path.resolve().is_relative_to(base):
        raise ValueError('Vault output escapes selected directory.')
    if path.exists():
        if path.read_bytes() != contents:
            raise ValueError('Vault file already exists with different content; preserve user edits.')
        return
    try:
        with path.open('xb') as f:
            f.write(contents)
    except FileExistsError:
        if path.read_bytes() != contents:
            raise ValueError('Concurrent Vault file collision.') from None


def publish(root, manifest, target, receipt, checkpoint):
    dest = target['destination']; vault = Path(dest['vault_path']).expanduser().resolve()
    directory = vault / dest['subdir']
    if not vault.is_dir() or not directory.resolve().is_relative_to(vault):
        raise ValueError('Output must stay inside the existing selected Vault.')
    directory.mkdir(parents=True, exist_ok=True); directory = directory.resolve()
    asset_dir = directory / 'assets'
    if not asset_dir.resolve().is_relative_to(directory):
        raise ValueError('Vault asset symlink escapes course directory.')
    asset_dir.mkdir(exist_ok=True)
    data = document_data(root, manifest)
    image_path = root / manifest['report']['figure']; image = asset_dir / image_path.name
    text = (root / manifest['artifacts']['markdown']).read_text()
    text = text.replace('../assets/' + quote(image_path.name), 'assets/' + quote(image.name))
    text = f'---\nomni_delivery_id: {receipt["delivery_id"]}\n---\n\n' + text
    note = directory / (manifest['key'] + '.md')
    # A marker records ownership; existence alone never authorizes overwriting notes.
    owned_file(image, image_path.read_bytes(), directory)
    owned_file(note, text.encode(), directory)
    checkpoint(note_path=str(note), status='pending')
    if note.read_text() != text or image.read_bytes() != image_path.read_bytes():
        raise ValueError('Vault readback failed.')
    return dict(verified(note='Read back Vault Markdown and matching image bytes'),
                note_path=str(note), note_hash=c.digest(note), asset_path=str(image), asset_hash=c.digest(image),
                url='obsidian://open?path=' + quote(str(note), safe=''))

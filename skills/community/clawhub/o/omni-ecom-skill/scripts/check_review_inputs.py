"""Read-only bulk fingerprint check; never authors a review decision."""
import argparse
import json
from pathlib import Path
from review_guard import validate_manifest, changed_entries


def check(card):
    manifest = json.loads(Path(card['manifest']).read_text(encoding='utf-8-sig'))
    validate_manifest(manifest)
    if manifest['manifest_sha256'] != card['manifest_sha256']:
        raise ValueError('review_card_manifest_mismatch')
    artifacts, sources = changed_entries(manifest)
    if artifacts or sources:
        raise ValueError('review_frozen_files_changed:'+str(artifacts+sources))
    return dict(status='review_inputs_unchanged', review_decision=None,
                artifact_count=len(manifest['artifacts']), source_count=len(manifest['sources']),
                files=[{'file': item['file'], 'path': item['path']} for item in manifest['artifacts']+manifest['sources']],
                note='指纹一致不是业务或视觉复核通过，必须由真实复核岗独立判断。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--task-card', required=True)
    args = parser.parse_args()
    print(json.dumps(check(json.loads(Path(args.task_card).read_text(encoding='utf-8-sig'))), ensure_ascii=False))

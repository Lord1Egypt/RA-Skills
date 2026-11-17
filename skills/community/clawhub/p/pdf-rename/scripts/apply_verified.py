#!/usr/bin/env python3
"""
Stage 2: Inject verified metadata into manifest.
"""
import os, re, json

MANIFEST_IN  = os.path.join(os.path.dirname(__file__), 'manifest.json')
MANIFEST_OUT = os.path.join(os.path.dirname(__file__), 'manifest_verified.json')

VERIFIED_DATA = {
    # === 文本鉴伪文件夹 ===
    "2023ConDA- Contrastive Domain Adaptation for AI-generated Text Detection.pdf": {
        "title": "ConDA: Contrastive Domain Adaptation for AI-Generated Text Detection",
        "year": "2023", "venue": "EMNLP", "confirmed": True
    },
    "2023Fighting Fire with Fire- Can ChatGPT Detect AI-generated Text.pdf": {
        "title": "Fighting Fire with Fire: Can ChatGPT Detect AI-Generated Text?",
        "year": "2023", "venue": "arXiv", "confirmed": True
    },
    "2023Ghostbuster- Detecting Text Ghostwritten by Large Language Models.pdf": {
        "title": "Ghostbuster: Detecting Text Ghostwritten by Large Language Models",
        "year": "2023", "venue": "EMNLP", "confirmed": True
    },
    "2023LLMDet- AThird Party Large Language Models Generated Text Detection Tool.pdf": {
        "title": "LLMDet: A Third Party Large Language Models Generated Text Detection Tool",
        "year": "2023", "venue": "arXiv", "confirmed": True
    },
    "2023SeqXGPT- Sentence-Level AI-Generated Text Detection.pdf": {
        "title": "SeqXGPT: Sentence-Level AI-Generated Text Detection",
        "year": "2023", "venue": "EMNLP", "confirmed": True
    },
    "2023Token Prediction as Implicit Classification to Identify LLM-Generated Text.pdf": {
        "title": "Token Prediction as Implicit Classification to Identify LLM-Generated Text",
        "year": "2023", "venue": "EMNLP", "confirmed": True
    },
    "2024A Survey on LLM-Generated Text Detection- Necessity Methods and Future Directions.pdf": {
        "title": "A Survey on LLM-Generated Text Detection: Necessity, Methods, and Future Directions",
        "year": "2024", "venue": "arXiv", "confirmed": True
    },
    "2024Detecting AI-generated Text via Multi-Level Contrastive Learning.pdf": {
        "title": "DeTeCtive: Detecting AI-Generated Text via Multi-Level Contrastive Learning",
        "year": "2024", "venue": "NeurIPS", "confirmed": True
    },
    "2025Iron Sharpens Iron- Defending Against Attacks in Machine-Generated Text Detection with Adversarial Training.pdf": {
        "title": "Iron Sharpens Iron: Defending Against Attacks in Machine-Generated Text Detection with Adversarial Training",
        "year": "2025", "venue": "ICLR", "confirmed": True
    },
    "OUTFOX-LLM-Generated Essay Detection Through In-Context Learning with Adversarially Generated Examples.pdf": {
        "title": "OUTFOX: LLM-Generated Essay Detection Through In-Context Learning with Adversarially Generated Examples",
        "year": "2024", "venue": "AAAI", "confirmed": True
    },
}
try:
    from VERIFIED_DATA import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_FSP import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_MAIN import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_OTHER import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_GAMETHEORY import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_GAMETHEORY_SUB import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_GAMUT import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_TMP import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass
try:
    from VERIFIED_DATA_LLM import VERIFIED_DATA as EXTRA_VERIFIED
    VERIFIED_DATA.update(EXTRA_VERIFIED)
except ImportError:
    pass


def run(folder):
    if not os.path.exists(MANIFEST_IN):
        print(f'[ERROR] {MANIFEST_IN} not found. Run extract.py first.')
        return

    with open(MANIFEST_IN, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    ready_count = 0
    skip_count = 0

    for m in manifest:
        fname = m['filename']
        vdata = VERIFIED_DATA.get(fname)

        if vdata and vdata.get('confirmed'):
            m['title'] = vdata['title']
            m['title_source'] = 'verified'
            m['year'] = vdata.get('year') or m['year']
            m['year_source'] = 'verified'
            m['venue'] = vdata.get('venue') or m['venue']
            m['venue_source'] = 'verified'
            m['status'] = 'ready'
            ready_count += 1
        else:
            if m['status'] == 'needs_verification':
                m['status'] = 'manual_review'
                skip_count += 1

    with open(MANIFEST_OUT, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f'[OK] Manifest saved -> {MANIFEST_OUT}')
    print(f'     {ready_count} files ready to rename')
    print(f'     {skip_count} files require manual review / skipped')

    print(f'\n{"=":*>80}')
    print('Rename preview:')
    print(f'{"=":*>80}\n')
    dup_groups = {}
    for m in manifest:
        if m['status'] == 'ready':
            if m['is_duplicate']:
                grp = m['duplicate_group']
                if grp not in dup_groups:
                    dup_groups[grp] = 0
                dup_groups[grp] += 1
                counter = dup_groups[grp]
            else:
                counter = None

            base = f'[{m["year"]}]' if m['year'] else '[????]'
            venue_str = f' [{m["venue"]}]' if m['venue'] else ''
            title_str = f'{base}{venue_str} {m["title"]}'
            title_str = re.sub(r'\s+', ' ', title_str).strip()
            if counter:
                title_str += f' ({counter})'
            title_str += '.pdf'

            dup = ' [DUPLICATE]' if m['is_duplicate'] else ''
            print(f'  [OK] {m["filename"]}')
            print(f'      -> {title_str}{dup}')
            print()
        else:
            print(f'  [SKIP] {m["filename"]} -> {m["status"]} | title="{m["title"]}"')
            print()

    print(f'\nTo execute: python execute.py "{folder}" --execute')


if __name__ == '__main__':
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run(folder)
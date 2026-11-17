import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'references' / 'catalog.json'
STOP_WORDS = set('a an and are as at be by for from how i in is it me my of on or podcast podcasts show shows that the to with'.split())


def words(text):
    return [word for word in re.findall(r'\w+', text.casefold()) if word not in STOP_WORDS]


def search(catalog, query, limit):
    query_words = set(words(query))
    documents = [(podcast, Counter(words(podcast['title'] + ' ' + podcast['description'] + ' ' + podcast['category'])))
                 for podcast in catalog['podcasts']]
    frequencies = Counter(word for _, counts in documents for word in query_words if word in counts)
    ranked = []
    for podcast, counts in documents:
        score = sum((1 + math.log(counts[word])) * math.log(1 + len(documents) / (1 + frequencies[word]))
                    for word in query_words if word in counts)
        if score:
            title_words = set(words(podcast['title']))
            score += sum(2 for word in query_words if word in title_words)
            ranked.append((score, podcast))
    ranked.sort(key=lambda row: (-row[0], row[1]['id']))
    return [podcast for _, podcast in ranked[:limit]]


def validate_records(records, filename):
    fields = ('id', 'title', 'description', 'category')
    if type(records) is not list or any(
        type(record) is not dict or any(type(record.get(field)) is not str for field in fields)
        for record in records
    ):
        raise ValueError(f'Invalid podcast records in {filename}')
    return records


def load_catalog():
    catalog = json.loads(CATALOG.read_text())
    if type(catalog) is not dict or any(
        type(catalog.get(field)) is not str or not catalog[field] for field in ('source', 'captured_at')
    ):
        raise ValueError('Catalog source or capture date is missing')
    if 'shards' not in catalog:
        validate_records(catalog.get('podcasts'), CATALOG.name)
        return catalog
    if type(catalog['shards']) is not list or type(catalog.get('record_count')) is not int:
        raise ValueError('Catalog shards or total record count is invalid')
    podcasts = []
    for shard in catalog['shards']:
        if type(shard) is not dict or type(shard.get('path')) is not str or type(shard.get('record_count')) is not int:
            raise ValueError('Catalog shard entry is invalid')
        payload = json.loads((CATALOG.parent / shard['path']).read_text())
        records = validate_records(payload['podcasts'], shard['path'])
        if len(records) != shard['record_count']:
            raise ValueError(f"Record count mismatch in {shard['path']}")
        podcasts.extend(records)
    if len(podcasts) != catalog['record_count']:
        raise ValueError('Total catalog record count mismatch')
    catalog['podcasts'] = podcasts
    return catalog


def main():
    parser = argparse.ArgumentParser(description='Search the bundled public PodPitch snapshot without network access.')
    parser.add_argument('query', nargs='?')
    parser.add_argument('--limit', type=int, choices=range(1, 11), default=3)
    parser.add_argument('--id')
    args = parser.parse_args()
    if not args.id and (not args.query or not args.query.strip()):
        parser.error('Provide a topic, show name, or --id returned by search.')
    try:
        catalog = load_catalog()
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(f'Bundled PodPitch catalog is unavailable or incomplete: {error}')
    podcasts = ([podcast for podcast in catalog['podcasts'] if podcast['id'] == args.id]
                if args.id else search(catalog, args.query, args.limit))
    print(json.dumps({'source': catalog['source'], 'captured_at': catalog['captured_at'],
                      'is_live': False, 'is_complete_catalog': False, 'podcasts': podcasts}, ensure_ascii=False))


if __name__ == '__main__':
    main()

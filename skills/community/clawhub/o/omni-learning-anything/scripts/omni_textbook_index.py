"""Resolve an explicit mainland K–12 textbook identity from a pinned catalog."""
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / 'references/textbook-index.json'
GRADES = dict(zip(range(1, 10), '一二三四五六七八九'))
STAGES = ('小学', '初中', '高中')
SUBJECT_ALIASES = {'生物': '生物学', '信息科技': '信息技术', '体育': '体育与健康',
                   '书法': '语文·书法练习指导', '道法': '道德与法治', '政治': '思想政治'}
EDITION_ALIASES = {'人教': '人教版', '人民教育出版社': '人教版', '部编版': '统编版',
                   '北师大': '北师大版', '北京师范大学出版社': '北师大版',
                   '华师大版': '华东师大版', '人教社': '人教版'}


@lru_cache(maxsize=1)
def catalog():
    data = json.loads(INDEX.read_text(encoding='utf-8'))
    if data.get('schema_version') != 1 or not data.get('books'):
        raise ValueError('Invalid textbook index.')
    return data


def get(book_id):
    for book in catalog()['books']:
        if book['book_id'] == book_id:
            return book
    raise KeyError(f'Unknown textbook ID: {book_id}')


def normalize(value):
    return re.sub(r'[^\w\u3400-\u9fff]', '', unicodedata.normalize('NFKC', str(value)).casefold())


def volume_key(value):
    result = normalize(value)
    for number, numeral in GRADES.items():
        result = result.replace(f'第{numeral}册', str(number)).replace(f'第{number}册', str(number))
    return result


def longest(values, query):
    matches = {value for value in values if value and normalize(value) in query}
    return sorted((a for a in matches if not any(a != b and normalize(a) in normalize(b)
                                                and len(normalize(a)) < len(normalize(b)) for b in matches)),
                  key=lambda value: (-len(normalize(value)), value))


def resolve(query, *, grade=None, subject=None, edition=None, volume=None, year=None,
            school_system=None, stage=None, book_id=None, allow_default=False):
    if not isinstance(query, str) or not query.strip():
        raise ValueError('Enter a textbook or learning request.')
    original = unicodedata.normalize('NFKC', query)
    pieces = re.split(r'[，,。；;：:]?\s*(?:重点(?:想)?学(?:习)?|深入(?:学(?:习)?|讲解)|深度(?:学(?:习)?|理解)|聚焦|只想学|只学)\s*', original, maxsplit=1)
    identity, focus = pieces[0], pieces[1].strip(' ，,。；;：:') if len(pieces) > 1 else ''
    if not focus:
        inside = re.search(r'(?<=[册学文理语学科])(?:里面的|里边的|里的|中的)(.+)$', identity)
        if inside:
            focus = inside[1].strip()
            identity = identity[:inside.start()]
    if not focus:
        match = re.search(r'(?:上册|下册|全一册|数学|语文|物理|化学|英语)\s*(?:里|中|的)?\s*((?:第[零一二三四五六七八九十\d]+[章节课单元]|[“「《]).*)$', identity)
        if match:
            focus = match[1].strip()
            identity = identity[:match.start(1)]
    short_volume = re.search(r'([一二三四五六七八九1-9]年级)([上下])(?!册)', identity)
    if not volume and short_volume:
        volume = short_volume[2] + '册'
    q = normalize(identity)
    books = catalog()['books']
    defaults = {}

    def answer(status, candidates=(), clarify=()):
        return {'status': status, 'book': candidates[0] if status == 'matched' else None,
                'candidates': list(candidates)[:12], 'candidate_count': len(candidates),
                'clarify': list(clarify), 'focus': focus, 'defaults': defaults}

    if book_id:
        return answer('matched', [get(book_id)])
    if re.search(r'最新版|最新修订|最新版本', identity):
        return answer('not_found')
    year_match = re.search(r'(?<!\d)((?:19|20)\d{2})(?:年|版)', identity)
    year = str(year) if year else (year_match[1] if year_match else None)
    if not stage:
        stage = next((name for name in STAGES if name in q), None)
    if re.search(r'高[一二三123]', q):
        stage = stage or '高中'
    if not grade:
        grade_match = re.search(r'([一二三四五六七八九1-9])年级', q)
        middle = re.search(r'初([一二三123])', q)
        if grade_match:
            value = grade_match[1]
            grade = (GRADES.get(int(value), value) if value.isascii() else value) + '年级'
        elif middle:
            value = '一二三'.find(middle[1]) + 1 if not middle[1].isascii() else int(middle[1])
            grade = GRADES[value + 6] + '年级'
            stage = stage or '初中'
    if grade:
        grade = normalize(grade)
        if grade[0:1] in '123456789' and grade[1:] == '年级':
            grade = GRADES[int(grade[0])] + '年级'
    if not school_system:
        school_system = next((name for name in ('五四学制', '六三学制') if name in q), None)
    subjects = {book['subject'] for book in books}
    if not subject:
        found = longest(subjects | SUBJECT_ALIASES.keys(), q)
        if len(found) > 1:
            return answer('needs_clarification', clarify=['subject'])
        subject = found[0] if found else None
    subject = SUBJECT_ALIASES.get(subject, subject)
    if subject == '思想政治' and stage == '初中':
        subject = '道德与法治'
    if not subject:
        if stage or grade:
            return answer('needs_clarification', clarify=['subject'])
        return answer('not_found')
    if not stage and not grade:
        return answer('needs_clarification', clarify=['grade'])
    books = [b for b in books if b['subject'] == subject and (not stage or b['stage'] == stage)
             and (not grade or grade in b['grade_levels'])
             and (not school_system or normalize(b['school_system']) == normalize(school_system))
             and (not year or str(b['year']) == year)]
    if not volume:
        found = longest((b['volume'] for b in books), q)
        module = re.search(r'(选择性必修|选修|必修)(?:第)?([一二三四五六七八九十\d]+)(?:册)?', q)
        volume = (module[1] + (str(next((n for n,v in GRADES.items() if v == module[2]), 10))
                               if not module[2].isascii() else module[2])) if module else (found[0] if found else None)
    if volume:
        books = [b for b in books if b['volume'] and volume_key(b['volume']) == volume_key(volume)]
    if not edition:
        named = longest({b['edition'] for b in books} | {b['edition_family'] for b in books} | EDITION_ALIASES.keys(), q)
        edition = named[0] if named else None
        if '人教a版' in q or '人教b版' in q:
            edition = next((b['edition'] for b in books if normalize(b['edition']) in q), edition)
        if not edition and re.search(r'[\u4e00-\u9fff]版(?!本|次)', q):
            return answer('not_found')
    if edition:
        edition = EDITION_ALIASES.get(edition, edition)
        books = [b for b in books if normalize(edition) in {normalize(b['edition']), normalize(b['edition_family'])}]
        subtype = next((token for token in ('pep', '精通', '一年级起点', '三年级起点', 'a版', 'b版') if token in q), None)
        if subtype:
            books = [b for b in books if subtype in normalize(b['edition'])]
    elif allow_default:
        recommended = ('统编版' if subject in ('语文', '历史', '道德与法治', '思想政治')
                       else '人教版' if subject == '数学' and grade == '三年级' else None)
        if recommended:
            preferred = [b for b in books if b['edition_family'] == recommended]
            if preferred:
                defaults['edition'] = recommended
                books = preferred
                edition = recommended
    if not books:
        return answer('not_found')
    if len(books) == 1:
        return answer('matched', books)
    clarify = [field for field in ('stage', 'grade', 'edition', 'school_system', 'volume', 'year')
               if len({b[field] for b in books}) > 1]
    return answer('needs_clarification', books, clarify or ['book_id'])

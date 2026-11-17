"""Offline course discovery and immutable, source-located learning pathways."""
import copy
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

CATALOG=Path(__file__).resolve().parents[1]/'references/course-catalog.json'

PROVIDER_ALIASES = {
    'harvard': ('harvard', 'harvardx', '哈佛'),
    'yale': ('yale', '耶鲁'),
    'mit': ('mit', '麻省理工'),
    'stanford': ('stanford', '斯坦福'),
    'tsinghua': ('tsinghua', '清华'),
    'pku': ('pku', 'peking university', '北大', '北京大学'),
    'fudan': ('fudan', '复旦'),
    'sjtu': ('sjtu', 'shanghai jiao tong university', '上海交大', '上海交通大学'),
    'helsinki': ('helsinki', '赫尔辛基', 'minnalearn'),
    'berkeley': ('berkeley', 'uc berkeley', '伯克利'),
    'zju': ('zju', 'zhejiang university', '浙大', '浙江大学'),
    'bnu': ('bnu', 'beijing normal university', '北师大', '北京师范大学'),
    'openai': ('openai',),
    'anthropic': ('anthropic', 'claude academy'),
    'hugging-face': ('hugging face', 'hugging-face', 'huggingface', 'hf'),
    'deeplearning-ai': ('deeplearning.ai', 'deeplearning-ai', 'deeplearning ai'),
    'microsoft': ('microsoft', '微软'),
    'google': ('google', '谷歌'),
    'smarthistory': ('smarthistory',),
}


def require(ok,message):
    if not ok:raise ValueError(message)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def text(value):return isinstance(value,str) and bool(value.strip())


def validate_course(course):
    require(isinstance(course,dict),'Course snapshot must be an object.')
    for field in ('id','title','institution','code','edition','domain','level','audience'):
        require(text(course.get(field)),'Course needs '+field+'.')
    require(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',course['id']),'Invalid course ID.')
    for field in ('instructors','aliases','prerequisites'):
        require(isinstance(course.get(field),list) and all(text(x) for x in course[field]),'Course needs '+field+' as a text list.')
    provider_type = course.get('provider_type', 'university')
    pathway_type = course.get('pathway_type', 'course')
    require(provider_type in ('university', 'ai_organization', 'cultural_organization'), 'Unknown provider type.')
    require(pathway_type in ('course', 'reference'), 'Unknown pathway type.')
    require(course['aliases'] and (course['instructors'] or provider_type != 'university' or pathway_type == 'reference'),
            'Pathway needs discoverable aliases and university courses need instructors.')
    require(isinstance(course.get('pace'),dict) and text(course['pace'].get('description')),'Original course pacing is required.')
    require(course.get('evidence_level') in ('syllabus_only','syllabus_and_sessions'),'State the available original-course evidence.')
    for field in ('source_access', 'original_language'):
        if field in course:
            require(text(course[field]), 'Course needs ' + field + ' as non-empty text.')
    sources=course.get('sources');units=course.get('units')
    require(isinstance(sources,list) and sources and isinstance(units,list) and units,'Course needs sources and ordered units.')
    source_ids=[]
    for source in sources:
        require(isinstance(source,dict) and all(text(source.get(k)) for k in ('id','title','url','locator','checked_at','kind')),'Incomplete course source.')
        url=urlsplit(source['url'])
        require(url.scheme=='https' and url.netloc and not url.username and not url.password,'Course sources need public HTTPS URLs.')
        require(source['kind'] in ('official','university_archive') and re.fullmatch(r'\d{4}-\d{2}-\d{2}',source['checked_at']),'State source provenance and check date.')
        source_ids.append(source['id'])
    require(len(source_ids)==len(set(source_ids)),'Duplicate original source ID.')
    require([u.get('id') if isinstance(u,dict) else None for u in units]==[f'u{i:02d}' for i in range(1,len(units)+1)],'Original unit IDs must be consecutive and ordered.')
    for unit in units:
        require(all(text(unit.get(k)) for k in ('title','locator','source_id','focus')) and unit['source_id'] in source_ids,'Every unit needs an original source locator and focus.')


def catalog():
    value=json.loads(CATALOG.read_text(encoding='utf-8'))
    require(isinstance(value,dict) and value.get('schema')==1 and isinstance(value.get('courses'),list),'Unsupported course catalog.')
    ids=[]
    for course in value['courses']:validate_course(course);ids.append(course['id'])
    require(ids and len(ids)==len(set(ids)),'Catalog course IDs must be unique.')
    return value


def summary(course):
    fields = ('id', 'title', 'institution', 'code', 'edition', 'domain', 'level',
              'prerequisites', 'audience', 'source_access', 'original_language')
    result = {key: copy.deepcopy(course[key]) for key in fields if key in course}
    result['provider_type'] = course.get('provider_type', 'university')
    result['pathway_type'] = course.get('pathway_type', 'course')
    return result


def listing():
    value=catalog()
    return {'catalog_checked_at':value['checked_at'],'courses':[summary(c) for c in value['courses']]}


def show(course_id):
    result=next((c for c in catalog()['courses'] if c['id']==course_id),None)
    require(result is not None,'Unknown built-in course; inspect courses list or research the requested course without claiming it is built in.')
    return copy.deepcopy(result)


def normalized(value):
    return re.sub(r'[^\w\u3400-\u9fff]+','',unicodedata.normalize('NFKC',value).casefold())


def resolve(query):
    require(text(query),'Provide a course name or learning interest.')
    q=normalized(query);records=catalog()['courses']
    raw=unicodedata.normalize('NFKC',query).casefold()
    named={provider for provider,aliases in PROVIDER_ALIASES.items() if any(
        bool(re.search(r'(?<![a-z])'+re.escape(a)+r'(?![a-z])',raw)) if a.isascii() else normalized(a) in q
        for a in aliases)}
    hits=[]
    for course in records:
        if named and not any(course['id'].startswith(provider+'-') for provider in named):
            continue
        terms={normalized(term) for term in (course['id'],course['title'],*course['aliases'])}
        for term in terms-{''}:
            hits.extend((match.start(),match.end(),course) for match in re.finditer(re.escape(term),q))
    scores={}
    # "AI Foundations" inside "Applied AI Foundations" is a single mention.
    for start,end,course in hits:
        if any(left<=start and end<=right and right-left>end-start for left,right,_ in hits):
            continue
        course_id=course['id']
        scores[course_id]=max(scores.get(course_id,0),end-start)
    matches=[(scores[course['id']],course) for course in records if course['id'] in scores]
    matches.sort(key=lambda x:(-x[0],x[1]['id']))
    candidates=[summary(c) for _,c in matches[:5]]
    vague=any(token in q for token in ('幸福课','happiness','心理学','psychology','机器学习','machinelearning','计算机','computerscience'))
    # A broad subject alone cannot establish institution, course identity or edition.
    broad=vague and not named and not any(normalized(c['id']) in q for _,c in matches)
    year_pattern=r'(?<!\d)(?:19|20)\d{2}(?!\d)'
    years=Counter(re.findall(year_pattern,raw))
    wrong_edition=False
    if matches and years:
        best=matches[0][1]
        subject_years=Counter()
        for term in (best['title'], best['id'], *best['aliases']):
            if normalized(term) in q:
                subject_years |= Counter(re.findall(year_pattern,term))
        wrong_edition=any(year not in best['edition'] for year in years-subject_years)
    status='not_found' if not matches else 'needs_clarification' if broad or wrong_edition or len(matches)>1 else 'matched'
    return {'status':status,'matches':candidates,'note':'Candidate matching only. Confirm material ambiguity and verify selected original sources before authoring; an unknown request is not an included course.'}


def bind(course_id,unit_ids=None,pace='adapted',practice='light'):
    course=show(course_id);units=[u['id'] for u in course['units']]
    value={'schema':1,'course':course,'sha256':fingerprint(course),'unit_ids':list(unit_ids) if unit_ids is not None else units,
           'pace':pace,'practice':practice}
    validate_binding(value)
    return value


def validate_binding(value):
    require(isinstance(value,dict) and set(value)=={'schema','course','sha256','unit_ids','pace','practice'} and value['schema']==1,'Invalid course pathway binding.')
    validate_course(value['course'])
    require(value['sha256']==fingerprint(value['course']),'Course snapshot changed; preserve the approved version and review a new course version.')
    require(value['pace'] in ('adapted','original_units') and value['practice'] in ('light','original_assignments'),'Choose course pacing and practice explicitly.')
    require(value['course'].get('pathway_type') != 'reference' or value['practice'] == 'light',
            'Open reference pathways support light practice.')
    selected=value['unit_ids'];all_units=[u['id'] for u in value['course']['units']]
    require(isinstance(selected,list) and selected and all(isinstance(u,str) and u in all_units for u in selected),'Select actual original course units.')
    require(selected==[u for u in all_units if u in selected],'Selected units must be unique and in original course order.')


def validate_course_plan(config,plan):
    if 'course_pathway' not in config:return
    binding=config['course_pathway'];validate_binding(binding);selected=binding['unit_ids'];seen=[];last=-1
    require(isinstance(plan.get('days'),list) and plan['days'],'Course plan needs mapped days.')
    for day in plan['days']:
        units=day.get('course_units')
        require(isinstance(units,list) and units and all(isinstance(u,str) and u in selected for u in units),'Each day must map to selected original course units.')
        require(len(units)==len(set(units)),'A day cannot duplicate a unit.')
        for unit in units:
            index=selected.index(unit)
            require(index>=last,'Days must preserve original course sequence; split units before moving forward.')
            last=index
            if unit not in seen:seen.append(unit)
    require(seen==selected,'Plan must cover every selected unit; explicitly select a smaller scope for a partial course.')
    if binding['pace']=='original_units':
        require([day['course_units'] for day in plan['days']]==[[u] for u in selected],'Original-unit mode needs one original unit per day; select adapted mode to split or group units.')


def source_ref(binding,source_id,unit_ids):
    validate_binding(binding)
    require(source_id in [s['id'] for s in binding['course']['sources']],'Unknown original source.')
    require(isinstance(unit_ids,list) and unit_ids and all(u in binding['unit_ids'] for u in unit_ids),'Source reference needs selected unit IDs.')
    return {'course_id':binding['course']['id'],'sha256':binding['sha256'],'source_id':source_id,'unit_ids':list(unit_ids)}


def validate_sources(data,config,plan):
    binding=config.get('course_pathway')
    refs=[s for s in data.get('sources',[]) if 'course_ref' in s]
    if not binding:
        require(not refs,'Original course references require a configured pathway.');return
    validate_course_plan(config,plan)
    if 'day' in data:
        day=data['day'];require(type(day) is int and 1<=day<=len(plan['days']),'Invalid pathway lesson day.')
        expected=plan['days'][day-1]['course_units']
        require(data.get('course_units')==expected,'Lesson original-unit mapping differs from the approved plan.')
    else:expected=binding['unit_ids']
    require(refs,'Course guides need at least one actual original-course source; a catalog match is not teaching evidence.')
    covered=set()
    originals={s['id']:s for s in binding['course']['sources']}
    for source in refs:
        ref=source['course_ref']
        require(isinstance(ref,dict) and set(ref)=={'course_id','sha256','source_id','unit_ids'},'Invalid original-course source reference.')
        require(ref['course_id']==binding['course']['id'] and ref['sha256']==binding['sha256'],'Source references a different course snapshot.')
        require(isinstance(ref['source_id'],str) and ref['source_id'] in originals,'Unknown original source ID.')
        require(source.get('url')==originals[ref['source_id']]['url'],'Original-course source URL differs from its bound source.')
        units=ref['unit_ids']
        require(isinstance(units,list) and units and all(isinstance(u,str) and u in expected for u in units) and len(set(units))==len(units),'Source references units outside this document.')
        require(all(next(u for u in binding['course']['units'] if u['id']==unit)['source_id']==ref['source_id'] for unit in units),'Source is not the catalog anchor for this original unit.')
        covered.update(units)
    require(covered==set(expected),'Original-course references must cover this document’s mapped units.')


_CONTEXT={
 'en':('Original course and learning scope','Independent learning guide; not official course materials or completion credit.','Personal-time adaptation: units may be split; this is not the full original workload.','Follow original unit order; original viewing, reading and assignment time is additional.','Light checks only; original assignments require a separate explicit choice.'),
 'zh':('原课程与学习范围','独立编写的学习辅导，不是来源方的官方教材，不代表修完原课或获得学分。','按个人时间改编：原单元可拆分，并不等于原课程全部工作量。','按原单元顺序跟学；原视频、阅读与作业另需时间。','默认只做轻量自检；原课作业需另行明确选择。'),
 'ja':('元の授業と学習範囲','独自の学習ガイドです。提供元の公式教材や修了・単位の認定ではありません。','学習時間に合わせて単元を分割します。元の授業全体の学習量とは異なります。','元の単元順で学びます。動画・読書・課題には別途時間が必要です。','基本は短い理解チェックです。元の課題は明示的に選択してください。'),
 'ko':('원 강좌와 학습 범위','독립적으로 작성한 학습 안내이며 제공 기관의 공식 교재나 이수·학점 인증이 아닙니다.','개인 시간에 맞춰 단원을 나눕니다. 원 강좌 전체 학습량과 같지 않습니다.','원 단원 순서로 학습하며 영상·읽기·과제에는 추가 시간이 필요합니다.','기본은 짧은 이해 확인이며 원 과제는 별도로 선택해야 합니다.'),
 'es':('Curso original y alcance','Guía independiente; no es material oficial ni acredita haber completado el curso.','Adaptación al tiempo personal: las unidades pueden dividirse; no equivale a toda la carga original.','Se mantiene el orden original; vídeos, lecturas y tareas requieren tiempo adicional.','Comprobaciones breves por defecto; las tareas originales requieren una elección expresa.'),
 'fr':('Cours original et périmètre','Guide indépendant : ni support officiel ni attestation de réussite du cours.','Adaptation au temps personnel : les unités peuvent être divisées, sans équivaloir à toute la charge originale.','L’ordre original est conservé ; vidéos, lectures et devoirs demandent du temps supplémentaire.','Vérifications brèves par défaut ; les devoirs originaux nécessitent un choix explicite.'),
 'de':('Originalkurs und Lernumfang','Unabhängiger Lernleitfaden, kein offizielles Kursmaterial und kein Leistungsnachweis.','An die persönliche Zeit angepasst: Einheiten können aufgeteilt werden; dies ersetzt nicht den gesamten Originalaufwand.','Die ursprüngliche Reihenfolge bleibt erhalten; Videos, Lektüre und Aufgaben benötigen zusätzliche Zeit.','Standardmäßig kurze Verständnisfragen; Originalaufgaben müssen ausdrücklich gewählt werden.'),
 'pt':('Curso original e âmbito','Guia independente; não é material oficial nem comprova a conclusão do curso.','Adaptação ao tempo pessoal: as unidades podem ser divididas; não equivale à carga original completa.','A ordem original é mantida; vídeos, leituras e tarefas exigem tempo adicional.','Verificações breves por padrão; tarefas originais exigem escolha explícita.'),
 'ru':('Исходный курс и объём обучения','Независимое учебное руководство, не официальный материал и не подтверждение прохождения курса.','Адаптация к личному времени: разделы можно дробить; это не полный объём исходного курса.','Сохраняется исходный порядок; видео, чтение и задания требуют дополнительного времени.','По умолчанию — краткая проверка; исходные задания нужно выбрать отдельно.'),
 'ar':('المقرر الأصلي ونطاق التعلم','دليل تعلم مستقل، وليس مادة رسمية أو إثبات إتمام للمقرر أو اعتماداً أكاديمياً.','تكييف مع الوقت الشخصي: يمكن تقسيم الوحدات، ولا يعادل ذلك عبء المقرر الأصلي كاملاً.','نحافظ على ترتيب الوحدات الأصلي؛ تحتاج الفيديوهات والقراءات والواجبات إلى وقت إضافي.','الأصل أسئلة قصيرة للفهم؛ تتطلب الواجبات الأصلية اختياراً صريحاً منفصلاً.'),
}


_REFERENCE_CONTEXT = {
    'en': ('Source and reading scope', 'Independent reading guide based on an open reference. Study time and light exercises are adapted to your plan.'),
    'zh': ('参考资料与阅读范围', '这是基于开放参考资料编排的阅读指南。阅读时间与轻量练习按你的计划安排。'),
    'ja': ('資料と読書範囲', '公開資料に基づく読書ガイドです。読む時間と短い練習は学習計画に合わせます。'),
    'ko': ('자료 및 읽기 범위', '공개 자료를 바탕으로 만든 읽기 안내입니다. 읽기 시간과 짧은 연습은 학습 계획에 맞춥니다.'),
    'es': ('Fuente y alcance de la lectura', 'Guía independiente basada en una referencia abierta. El tiempo de lectura y los ejercicios breves se adaptan a tu plan.'),
    'fr': ('Source et périmètre de lecture', 'Guide de lecture indépendant fondé sur une ressource ouverte. Le temps de lecture et les exercices courts suivent votre plan.'),
    'de': ('Quelle und Leseumfang', 'Unabhängiger Leitfaden zu einer frei zugänglichen Quelle. Lesezeit und kurze Übungen richten sich nach deinem Plan.'),
    'pt': ('Fonte e escopo da leitura', 'Guia independente baseado em uma referência aberta. O tempo de leitura e os exercícios curtos seguem seu plano.'),
    'ru': ('Источник и объём чтения', 'Самостоятельный маршрут по открытому источнику. Время чтения и короткие задания определяются вашим планом.'),
    'ar': ('المصدر ونطاق القراءة', 'دليل مستقل للقراءة يستند إلى مرجع مفتوح. يحدد جدولك وقت القراءة والتمارين القصيرة.'),
}


def context_section(binding,unit_ids,language='en'):
    validate_binding(binding);require(language in _CONTEXT,'Unsupported pathway language.')
    course=binding['course'];title,disclosure,adapted,original,light=_CONTEXT[language]
    locations='; '.join(u['locator'] for u in course['units'] if u['id'] in unit_ids)
    if course.get('pathway_type') == 'reference':
        title, disclosure = _REFERENCE_CONTEXT[language]
        body = (f"{course['institution']} · {course['title']} · {course['edition']}\n\n"
                f"{locations}\n\n{len(binding['unit_ids'])}/{len(course['units'])} · {disclosure}")
        return {'title': title, 'body': body}
    body=f"{course['institution']} · {course['title']} · {course['code']} · {course['edition']}\n\n{locations}\n\n{len(binding['unit_ids'])}/{len(course['units'])} · {disclosure}\n\n{adapted if binding['pace']=='adapted' else original}"
    body+='\n\n'+light if binding['practice']=='light' else '\n\n'+original
    return {'title':title,'body':body}


def with_context(data,config,plan):
    if not config.get('course_pathway'):return data
    result=copy.deepcopy(data);binding=config['course_pathway']
    units=binding['unit_ids'] if 'day' not in data else plan['days'][data['day']-1]['course_units']
    result['sections']=[context_section(binding,units,config.get('language','zh')),*result['sections']]
    return result


def welcome():
    available={c['id']:c for c in catalog()['courses']}
    ids=('harvard-positive-psychology','yale-listening-music','tsinghua-chinese-architecture-history',
         'sjtu-tang-poetry-song-lyrics','openai-ai-foundations')
    return {'courses':[summary(available[i]) for i in ids if i in available],
            'instruction':'In the current installation/first-use conversation only, if the learner has no explicit topic, introduce 3–5 varied pathways in their language. Offer the full catalog or any other topic; wait for a choice and reuse existing intake. Never open a new chat, repeat an already shown menu, interrupt an ongoing course, or create a course/schedule from silence.'}

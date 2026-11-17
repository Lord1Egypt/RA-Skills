"""Supported course languages, interface text and script-aware font choices.

Authored teaching content is never translated by deterministic exporters.
"""
_KEYS=('name','plan','day','further','optional','published','checked','guide','grounded')
_ROWS={
 'en':('English','Learning plan / {days} days','{key}/{days} | Read {reading} min + practice {practice} min','Further reading (optional)','Optional; outside the daily core time budget.','Published','Checked','Learning guide','Source-grounded learning'),
 'zh':('简体中文','学习计划 / {days} 天','{key}/{days} | 阅读 {reading} 分钟 + 练习 {practice} 分钟','扩展学习（选读）','以下为选读，不计入每日必做时间。','发布','核验','学习手册','有来源的学习'),
 'ja':('日本語','学習計画 / {days}日','{key}/{days} | 読む時間 {reading}分 + 練習 {practice}分','参考資料（任意）','任意の資料です。毎日の必須学習時間には含まれません。','公開日','確認日','学習ガイド','出典に基づく学習'),
 'ko':('한국어','학습 계획 / {days}일','{key}/{days} | 읽기 {reading}분 + 연습 {practice}분','추가 읽기 자료 (선택)','선택 자료이며 일일 필수 학습 시간에 포함되지 않습니다.','게시일','확인일','학습 가이드','출처에 기반한 학습'),
 'es':('Español','Plan de estudio | Días: {days}','{key}/{days} | Lectura: {reading} min + práctica: {practice} min','Lecturas complementarias (opcional)','Lectura opcional, fuera del tiempo diario de estudio.','Publicado','Verificado','Guía de aprendizaje','Aprendizaje basado en fuentes'),
 'fr':('Français','Plan d’étude | Jours : {days}','{key}/{days} | Lecture : {reading} min + pratique : {practice} min','Pour aller plus loin (facultatif)','Lecture facultative, en dehors du temps quotidien prévu.','Publié','Vérifié','Guide d’apprentissage','Apprentissage fondé sur des sources'),
 'de':('Deutsch','Lernplan | Tage: {days}','{key}/{days} | Lesen: {reading} Min. + Übung: {practice} Min.','Weiterführende Literatur (optional)','Freiwillige Lektüre außerhalb der täglichen Lernzeit.','Veröffentlicht','Geprüft','Lernleitfaden','Quellenbasiertes Lernen'),
 'pt':('Português','Plano de estudo | Dias: {days}','{key}/{days} | Leitura: {reading} min + prática: {practice} min','Leituras complementares (opcional)','Leitura opcional, fora do tempo diário de estudo.','Publicado','Verificado','Guia de aprendizagem','Aprendizagem baseada em fontes'),
 'ru':('Русский','Учебный план | Дней: {days}','{key}/{days} | Чтение: {reading} мин + практика: {practice} мин','Дополнительные материалы (по желанию)','Необязательное чтение сверх ежедневного времени занятий.','Опубликовано','Проверено','Учебное руководство','Обучение на основе источников'),
 'ar':('العربية','خطة التعلم | عدد الأيام: {days}','{key}/{days} | القراءة بالدقائق: {reading} + التدريب بالدقائق: {practice}','قراءات إضافية (اختيارية)','قراءات اختيارية خارج وقت التعلم اليومي الأساسي.','تاريخ النشر','تاريخ التحقق','دليل التعلم','تعلم يستند إلى المصادر'),
}
LANGUAGES=tuple(_ROWS)
CJK_FONTS={
 'zh':('FangSong','FangSong_GB2312','STSong','Songti SC','Noto Serif CJK SC','Source Han Sans CN','SimSun','Arial Unicode MS'),
 'ja':('Hiragino Mincho ProN','Noto Serif CJK JP','Yu Mincho','MS Mincho','Arial Unicode MS'),
 'ko':('Apple SD Gothic Neo','Noto Serif CJK KR','Malgun Gothic','Batang','Arial Unicode MS'),
}
ARABIC_FONTS=('Amiri','Noto Naskh Arabic','Geeza Pro','Arial Unicode MS')


def language(code='zh'):
 if not isinstance(code,str) or code not in _ROWS:raise ValueError('Choose a supported course language: '+', '.join(LANGUAGES)+'.')
 return dict(zip(_KEYS,_ROWS[code]),code=code,dir='rtl' if code=='ar' else 'ltr')


def subtitle(data,plan,config,date,key):
 labels=language(config.get('language','zh'))
 template=labels['plan'] if key=='plan' else labels['day']
 return date+' | '+template.format(days=len(plan['days']),key=key,reading=data.get('reading_minutes'),practice=data.get('practice_minutes'))


def source_labels(config):
    labels=dict(language(config.get('language','zh')))
    if config.get('materials') or config.get('course_pathway'):
        labels['further']={'en':'Sources and original locations','zh':'资料来源与原文位置','ja':'資料と原文の位置','ko':'자료 출처와 원문 위치','es':'Fuentes y ubicaciones originales','fr':'Sources et passages originaux','de':'Quellen und Originalstellen','pt':'Fontes e trechos originais','ru':'Источники и исходные фрагменты','ar':'المصادر ومواضع النص الأصلي'}[labels['code']]
        labels['optional']=''
    return labels

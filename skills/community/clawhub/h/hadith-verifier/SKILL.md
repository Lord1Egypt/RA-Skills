---
name: hadith-verifier
description: Verify hadith authenticity before publishing any Islamic content. Checks hadith text against major hadith collections (Bukhari, Muslim, Tirmidhi, Abu Dawud, Nasai, Ibn Majah, Malik) via open-source hadith API. Use when: (1) a user asks to verify a hadith, (2) before publishing any content that quotes a hadith, (3) when building Islamic content that references prophetic sayings, (4) when another agent or user claims a hadith is from a specific source. Triggers: "verify hadith", "check hadith", "is this hadith authentic", "hadith verification", "authenticate hadith", "search hadith", "hadith checker", "تحقق من حديث", "صحة الحديث".
---

# 🕌 Hadith Verifier — تحقق من صحة الأحاديث

> «مَنْ كَذَبَ عَلَيَّ مُتَعَمِّدًا فَلْيَتَبَوَّأْ مَقْعَدَهُ مِنَ النَّارِ»
> — البخاري (107) ومسلم (1)

**⚠️ قاعدة مطلقة:** لا تنشر أي حديث بدون تحقق. إذا لم تستطع التحقق → **"لا أعلم"**.

---

## المنهجية

### ترتيب المصادر (إلزامي):

1. **القرآن الكريم** (النص العربي فقط)
2. **السنة الصحيحة** (بسند متصل للصحابي)
3. **إجماع الصحابة** (بسند متصل)

> ❌ لا يُعتمد على: رأي فقيه بذاته، مذهب معين، أو اجتهاد بشري بدون دليل

---

## الاستخدام

### 1. البحث عن حديث:

```bash
python3 scripts/hadith_db.py search '<كلمات البحث>' --limit 5
```

```bash
# مثال: البحث عن حديث بالنوايا
python3 scripts/hadith_db.py search "intention actions judged"

# مثال: بالعربي
python3 scripts/hadith_db.py search "من غشنا ليس منا"

# مثال: تحديد المجموعة
python3 scripts/hadith_db.py search "prayer" --collections bukhari,muslim
```

### 2. جلب حديث برقم معين:

```bash
python3 scripts/hadith_db.py get bukhari 1
python3 scripts/hadith_db.py get muslim 102
```

### 3. التحقق من حديث محدد:

```bash
python3 scripts/verify_hadith.py '<نص الحديث>' --source <المجموعة> --رقم <الرقم>
```

---

## المجموعات المدعومة

| المجموعة | الاسم | الوزن |
|-----------|-------|-------|
| bukhari | صحيح البخاري | highest |
| muslim | صحيح مسلم | highest |
| tirmidhi | جامع الترمذي | high |
| abudawud | سنن أبي داود | high |
| nasai | سنن النسائي | high |
| ibnmajah | سنن ابن ماجه | medium |
| malik | موطأ مالك | high |
| nawawi | الأربعون النووية | reference |
| qudsi | الأحاديث القدسية | reference |

---

## درجات التحقق

| الدرجة | المعنى | الإجراء |
|--------|--------|---------|
| **verified** | صحيح — متطابق مع المصدر | ✅ انشر مع المصدر |
| **likely_authentic** | غالبًا صحيح — تطابق عالي | ✅ انشر مع الإشارة |
| **possible_match** | تطابق جزئي | ⚠️ راجع يدويًا |
| **weak_match** | تطابق ضعيف | ⚠️ لا تنشر بدون مراجعة |
| **not_found** | غير موجود في المصادر | ❌ لا تنشر |
| **text_mismatch** | النص لا يطابق المصدر المذكور | ❌ لا تنشر — يُرجّح أنه موضوع |

---

## المصادر المفتوحة المستخدمة

- **fawazahmed0/hadith-api** — قاعدة بيانات مفتوحة المصدر للإحاديث
- تشمل: البخاري، مسلم، الترمذي، أبو داود، النسائي، ابن ماجه، مالك
- اللغات: عربي + إنجليزي + 6 لغات أخرى

---

## قواعد النشر

### ✅ يُسمح بالنشر فقط إذا:
- وُجد الحديث في أحد الكتب الستة (أو الموطأ)
- المصدر مذكور بوضوح (الكتاب + الرقم)
- النص متطابق أو قريب جدًا من الأصل

### ❌ يُمنع النشر:
- إذا لم يُوجد الحديث في أي مصدر
- إذا كان المصدر غير موثق
- إذا كان النص مختصرًا بشكل يُغيّر المعنى
- إذا كان الحديث "مشهورًا على الإنترنت" فقط بدون أصل

### 🚫 ممنوع تمامًا:
- نسب حديث للنبي ﷺ بدون سند
- نشر أحاديث ضعيفة/موضوعك على أنها صحيحة
- الاعتماد على الذكاء الاصطناعي كمصدر للأحاديث

---

## التعامل مع الأحاديث الضعيفة

من درج الحديث | هل يُنشر؟ | الشرط
--- | --- | ---
**Sahih** (صحيح) | ✅ نعم | مع ذكر المصدر
**Hasan** (حسن) | ⚠️ بحذر | مع ذكر الدرجة والمصدر
**Daif** (ضعيف) | ❌ لا | إلا في فضائل الأعمال مع التنبيه
**Maudu** (موضوع) | ❌ أبدًا | يُحذفورًا

---

## عند الشك

إذا لم تستطع التحقق من حديث:
> «هذا الحديث لا أستطيع التحقق منه. أرجع لأهل العلم. لا أنشره حتى يتثبت منه.»

---

## تنبيه مهم

> هذا النظام أداة مساعدة فقط. لستَ محدثًا ولا مُحقق أحاديث. المرجع النهائي لأهل العلم.
> عند التناقض بين النظام وأهل العلم → حكم أهل العلم هو المعتمد.

---

*بفضل الله — التوفيق من الله*

# 📸 PhotoIndexWithLLM — العربية

## نظرة عامة

PhotoIndexWithLLM هو نظام ذكي لفهرسة الصور وتحليلها والبحث فيها يعتمد على نماذج الرؤية واللغة الكبيرة (VL).

## البدء السريع

```bash
# تثبيت التبعيات
pip install requests

# مسح الصور ضوئياً
python skill.py scan --dir /home/user/Photos

# البحث عن الصور
python skill.py search "شاطئ غروب"

# إخراج JSON
python skill.py search "شاطئ" --format json
```

## المنصات المدعومة

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## صيغ الصور المدعومة (17 نوعاً)

| النوع | الصيغ |
|-------|-------|
| شائعة | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| RAW أخرى | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## حماية الخصوصية

- الوضع المحلي فقط افتراضياً
- الصور لا تغادر جهازك أبداً
- النقل عن بُعد يتطلب موافقة المستخدم

## الأوامر الكاملة

```bash
# مسح الصور ضوئياً
python skill.py scan --dir /home/user/Photos

# البحث عن الصور
python skill.py search "شاطئ غروب"

# مسح وبحث
python skill.py scan_and_search --dir /home/user/Photos --query "شاطئ"

# إضافة ملاحظات
python skill.py annotate --photo /photos/img001.jpg --type person --name أحمد

# تدريب النموذج
python skill.py train

# عرض الإحصائيات
python skill.py stats

# اختبار الاتصال
python skill.py test
```

## التواصل

**المؤلف**: 北京老李（beijingLL）
**ClawHub ID**: 43622283

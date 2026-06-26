# li_nvvideocodec - ضاغط فيديو NVIDIA AV1

**الإصدار**: 1.0.1  
**اللغة**: العربية (ar)

## 📋 نظرة عامة

أداة ضغط فيديو دفعات تستخدم ترميز AV1 المسرع بواسطة وحدة معالجة الرسومات NVIDIA. ضغط الفيديو بكفاءة مع التحقق الذكي وملفات ضغط متعددة.

## ✨ المميزات

- 🎯 **التحقق الذكي** - اختبار تلقائي لفعالية الضغط
- 📊 **ثلاثة ملفات** - محافظ/متوازن/عدواني
- 🖥️ **عبر الأنظمة** - Windows و Ubuntu Linux
- 📈 **التقدم في الوقت الفعلي** - عرض مباشر
- 🔒 **آمن** - حماية الملفات الأصلية

## 🚀 البدء السريع

```bash
# الوضع التفاعلي
python scripts/compress_videos.py

# وضع سطر الأوامر
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# وضع الاختبار
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 ملفات الضغط

| الملف | الدقة | CRF | FPS | الصوت | التوفير |
|-------|-------|-----|-----|-------|---------|
| **A** | أصلي | 23 | أصلي | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ المتطلبات

- **FFmpeg** مع دعم av1_nvenc
- **NVIDIA GPU** (GTX 1650+)
- **Python 3.7+**

## 🤖 الاستخدام مع Agent

```bash
# التحقق من البيئة
python agent_interface.py --action check

# تحليل الفيديو
python agent_interface.py --action analyze -i "/path/to/videos"

# ضغط
python agent_interface.py --action compress -i "/path/to/videos" -p B
```

---
name: google-free-media
description: สร้างรูปภาพและวิดีโอ AI ฟรีผ่าน Google Gemini และ Google Flow โดยใช้ browser automation ไม่ต้องจ่าย API fee ใช้เมื่อต้องการสร้างสื่อ visual (รูปปก, thumbnail, วิดีโอสั้น) โดยไม่เสียค่าใช้จ่าย
---

# Google Free Media Generator

Skill สำหรับสร้างรูปภาพและวิดีโอ AI ฟรีผ่าน Google Gemini และ Google Flow โดยใช้ browser automation

## 🎯 เมื่อไหร่ควรใช้ Skill นี้

ใช้เมื่อผู้ใช้ต้องการ:
- สร้างรูปภาพ AI สำหรับ cover, thumbnail, banner
- สร้างวิดีโอจากข้อความหรือรูปภาพ (text-to-video, image-to-video)
- ประหยัดค่า API (0 บาท vs 1-3 บาท/รูป ผ่าน API ปกติ)
- สร้างสื่อจำนวนมากโดยไม่กังวลเรื่องต้นทุน

## ⚠️ ข้อจำกัดที่ต้องรู้

1. **Quota ฟรีจำกัด**: Gemini ~100 รูป/วัน, Flow ~50 credits/วัน (อาจเปลี่ยนแปลง)
2. **ช้ากว่า API**: ต้องเปิด browser และรอ UI load (5-10x ช้ากว่า)
3. **เสี่ยง UI เปลี่ยน**: Google เปลี่ยนปุ่ม/ตำแหน่งบ่อย → อาจต้อง update skill
4. **Terms of Service**: Automation อาจขัดกับ ToS ของ Google free tier

## 📋 ขั้นตอนการทำงาน

### 1. ตรวจสอบ Quota ก่อนเริ่ม
```bash
node scripts/quota_manager.mjs check
```
- ดูว่าเหลือ quota เท่าไหร่
- แจ้งเตือนถ้าใกล้หมด

### 2. สร้างรูปภาพ (Gemini)
```bash
node scripts/generate_image.mjs --prompt "คำอธิบายรูป" --output /path/to/output.jpg
```

**การทำงาน:**
1. เปิด browser ไปยัง gemini.google.com
2. Login (ถ้ายังไม่ได้ login)
3. กดปุ่มสร้างรูป (Image generation)
4. ส่ง prompt ที่ enhance แล้ว
5. รอ generate และดึงรูป full resolution (=s0 trick)
6. บันทึกลงไฟล์

### 3. สร้างวิดีโอ (Google Flow)
```bash
node scripts/generate_video.mjs --prompt "คำอธิบายวิดีโอ" --output /path/to/output.mp4
```

**การทำงาน:**
1. เปิด browser ไปยัง labs.google/flow
2. เลือกโหมด (Text-to-Video หรือ Image-to-Video)
3. ส่ง prompt หรืออัพโหลดรูป
4. รอ generate
5. ดาวน์โหลดวิดีโอ

## 🔧 Scripts

### generate_image.mjs
สร้างรูปภาพผ่าน Google Gemini

**Arguments:**
- `--prompt`: คำอธิบายรูป (required)
- `--output`: path ไฟล์ output (required)
- `--style`: style ของรูป (optional: realistic, artistic, minimalist)
- `--enhance`: ให้ AI enhance prompt อัตโนมัติ (default: true)

### generate_video.mjs
สร้างวิดีโอผ่าน Google Flow (Veo 3.1)

**Arguments:**
- `--prompt`: คำอธิบายวิดีโอ (required)
- `--output`: path ไฟล์ output (required)
- `--mode`: โหมดการสร้าง (text-to-video, image-to-video)
- `--image`: path รูปต้นทาง (สำหรับ image-to-video)
- `--duration`: ระยะเวลาวิดีโอ (5-10 วินาที)

### quota_manager.mjs
จัดการและติดตาม quota การใช้งาน

**Commands:**
- `check`: ตรวจสอบ quota ที่เหลือ
- `reset`: รีเซ็ต counter (เริ่มวันใหม่)
- `log`: ดู log การใช้งาน

**Config File:** `configs/quota.json`
```json
{
  "dailyLimits": {
    "images": 100,
    "videoCredits": 50
  },
  "currentUsage": {
    "images": 0,
    "videoCredits": 0
  },
  "lastReset": "2026-03-02T00:00:00+07:00"
}
```

## 💡 เทคนิคสำคัญ

### 1. ดึงรูป Full Resolution
รูปบน Gemini แสดงที่ 1024px แต่สามารถดึง full resolution (1408x768) ได้โดยเปลี่ยน URL:
```
จาก: https://.../image=s1024
เป็น: https://.../image=s0
```

### 2. Session Persistence
- Login ครั้งเดียวแล้วเก็บ cookie ไว้ใช้ต่อ
- ไม่ต้อง login ใหม่ทุกครั้งที่สร้างรูป
- ใช้ Puppeteer/Playwright session storage

### 3. Prompt Enhancement
ก่อนส่งให้ Gemini ควร enhance prompt ให้มี:
- Lighting (soft lighting, dramatic lighting, golden hour)
- Composition (rule of thirds, centered, wide angle)
- Style (photorealistic, cinematic, minimalist, vibrant)
- Quality keywords (4K, ultra detailed, professional)

**ตัวอย่าง:**
```
Input: "รูปแมวใส่แว่น"
Enhanced: "A photorealistic portrait of a cute cat wearing round glasses, 
soft studio lighting, centered composition, professional photography, 
4K ultra detailed, warm tones"
```

## 📁 Storage Organization

ไฟล์ที่สร้างจะเก็บที่:
```
/mnt/storage/ada_projects/ai_media/
├── images/YYYY-MM/
├── videos/YYYY-MM/
└── metadata.json
```

## 🔄 Fallback Strategy

ถ้า Google ใช้ไม่ได้ มีทางเลือกสำรอง:
1. Bing Image Creator (ฟรี)
2. Leonardo.ai (ฟรี tier)
3. Stable Diffusion Online

## 🚨 การแก้ปัญหา

### Login ไม่ได้
- ตรวจสอบว่า browser ไม่ใช่ headless mode
- ถ้าใช้ VPS ต้องตั้ง Xvfb เป็นจอเสมือน
- ลอง clear cookie แล้ว login ใหม่

### UI เปลี่ยน/ปุ่มหาย
- Update selector ใน scripts
- ตรวจสอบ Google เปลี่ยนตำแหน่งฟีเจอร์

### Quota หมด
- รอวันถัดไป (reset ตอน 00:00)
- ใช้ fallback services แทน

## 📝 ตัวอย่างการใช้งาน

```bash
# สร้างรูปปกโพสต์
node scripts/generate_image.mjs \
  --prompt "AI workflow diagram, futuristic style, blue and purple gradient" \
  --output /mnt/storage/ada_projects/ai_media/images/2026-03/cover_001.jpg \
  --style artistic

# สร้างวิดีโอจากข้อความ
node scripts/generate_video.mjs \
  --prompt "Ocean waves at sunset, cinematic slow motion" \
  --output /mnt/storage/ada_projects/ai_media/videos/2026-03/sunset.mp4 \
  --duration 8

# ตรวจสอบ quota
node scripts/quota_manager.mjs check
```

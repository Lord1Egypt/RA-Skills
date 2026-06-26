# Google Free Media Skill - Quick Start

## 🚀 เริ่มใช้งานใน 3 ขั้นตอน

### 1. ติดตั้ง Dependencies
```bash
cd /mnt/storage/ada_projects/google-free-media-skill
npm install puppeteer
```

### 2. Login Google ครั้งเดียว
เปิด browser และ login ที่:
- https://gemini.google.com
- https://labs.google/flow

### 3. ทดสอบสร้างรูป
```bash
node scripts/generate_image.mjs \
  --prompt "futuristic city at night, neon lights, cyberpunk style" \
  --output /mnt/storage/ada_projects/ai_media/images/2026-03/test_001.jpg
```

## 📋 คำสั่งที่ใช้บ่อย

```bash
# ตรวจสอบ quota
node scripts/quota_manager.mjs check

# สร้างรูป
node scripts/generate_image.mjs --prompt "..." --output path/to/file.jpg

# สร้างวิดีโอ
node scripts/generate_video.mjs --prompt "..." --output path/to/file.mp4

# ดู log การใช้งาน
node scripts/quota_manager.mjs log
```

## ⚙️ การ Config

แก้ไข `configs/quota.json` เพื่อปรับ quota ตามความต้องการ:
```json
{
  "dailyLimits": {
    "images": 100,
    "videoCredits": 50
  }
}
```

## 📁 โครงสร้างไฟล์
```
google-free-media-skill/
├── SKILL.md              # เอกสารหลักของ skill
├── README.md             # Quick start guide
├── scripts/
│   ├── generate_image.mjs    # สร้างรูป
│   ├── generate_video.mjs    # สร้างวิดีโอ
│   └── quota_manager.mjs     # จัดการ quota
├── configs/
│   ├── quota.json            # Quota config
│   └── quota_log.jsonl       # Log การใช้งาน
└── output/                   # ไฟล์ที่สร้าง (ถ้ามี)
```

## 🆘 Troubleshooting

### Login ไม่ได้
- ใช้ browser ปกติ login ก่อน แล้วค่อยรัน script
- ถ้าใช้ VPS ต้องตั้ง Xvfb

### UI เปลี่ยน/Script พัง
- ตรวจสอบ selector ใน scripts
- Update ตาม UI ล่าสุดของ Google

### Quota หมด
- รอวันถัดไป (auto-reset ตอน 00:00)
- ใช้ fallback services แทน

---

**หมายเหตุ:** Scripts นี้เป็น skeleton สำหรับ demonstration
การ implement จริงต้องเขียน browser automation ด้วย Puppeteer/Playwright

---
name: "openclaw-plugin-intelligence"
slug: openclaw-plugin-intelligence
version: 1.1.0
homepage: https://github.com/pmuhammadagus-byte/openclaw-settings
description: "Use when activating high-level plugin reasoning: capability-first discovery, plugin selection, multi-plugin orchestration, connection/permission checks, result validation, failure recovery, and plugin security."
changelog: ClawHub professional standard: Overview, When to Use, How to Use, Common Mistakes, Red Flags, Rationalizations, Quick Reference
emoji: "🔌"
  openclaw:
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
metadata:
  openclaw:
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
---
## Overview

This skill activates high-level plugin reasoning: capability-first discovery, plugin selection, multi-plugin orchestration, dependency conflict resolution, and rollback-safe updates for the OpenClaw plugin ecosystem.


# OPENCLAW PLUGIN INTELLIGENCE — BRAIN CORE EXTENSION

## When to Use

Gunakan skill ini ketika:
- task membutuhkan kemampuan eksternal yang mungkin disediakan plugin;
- perlu menentukan apakah plugin diperlukan sebelum memanggilnya;
- perlu menemukan, mengevaluasi, atau memilih plugin yang sesuai;
- perlu menggabungkan beberapa plugin dalam satu workflow;
- perlu memeriksa koneksi, permission, dan validasi hasil plugin;
- perlu recovery ketika plugin gagal atau tidak tersedia.

Jangan gunakan untuk:
- menjalankan skill native yang sudah ada;
- menggantikan Brain Core untuk reasoning umum;
- operasi destruktif tanpa validasi;
- mengarang plugin yang belum diketahui tersedia.

---

## IDENTITY

Kamu adalah PLUGIN INTELLIGENCE ENGINE, bagian dari BRAIN CORE ULTRA.

Tugasmu adalah membuat OpenClaw mampu:
- mengenali kebutuhan plugin;
- menentukan apakah plugin diperlukan;
- menemukan plugin yang sesuai;
- memahami kemampuan plugin;
- memilih plugin terbaik;
- memeriksa koneksi dan permission;
- menggunakan plugin dengan benar;
- menggabungkan beberapa plugin;
- menangani kegagalan plugin;
- dan mengevaluasi hasil plugin.

Plugin adalah alat eksternal yang memperluas kemampuan agent.
Jangan menggunakan plugin hanya karena plugin tersedia.

---

## CORE LOOP

TASK
↓
NEED EXTERNAL CAPABILITY?
├── NO → NATIVE REASONING / TOOLS
└── YES
 ↓
PLUGIN AVAILABLE?
├── NO → DISCOVER / REPORT
└── YES
 ↓
CONNECTED?
├── NO → CONNECTION FLOW
└── YES
 ↓
AUTHORIZED?
├── NO → REQUEST/SETUP REQUIRED
└── YES
 ↓
EXECUTE
 ↓
VERIFY RESULT
 ↓
SUCCESS?
├── YES → COMPLETE
└── NO → RECOVER / FALLBACK

---

## 1. CAPABILITY-FIRST

Jangan berpikir:
«"Plugin apa yang saya punya?"»

Berpikir:
«"Kemampuan apa yang dibutuhkan untuk menyelesaikan task?"»

Contoh:
USER NEED → SEND EMAIL → REQUIRED CAPABILITY = EMAIL → FIND EMAIL PLUGIN

Bukan:
PLUGIN A tersedia → pakai Plugin A

---

## 2. PLUGIN DETECTION

Untuk setiap task, tanyakan secara internal:

APAKAH TASK INI MEMBUTUHKAN KEMAMPUAN EKSTERNAL?

Jika YA, lanjut ke discovery/evaluation.
Jika TIDAK, jangan memanggil plugin yang tidak diperlukan.

---

## 3. PLUGIN DISCOVERY

Jika plugin yang dibutuhkan belum diketahui:

Cari plugin berdasarkan kemampuan, bukan hanya nama.

Kategori kemampuan yang umum:
- EMAIL
- CALENDAR
- DATABASE
- GITHUB
- SLACK
- TELEGRAM
- WEB
- SEARCH
- FILES
- CLOUD
- NOTION
- AUTOMATION
- ANALYTICS
- PAYMENT
- AI

Jika sistem menyediakan mekanisme pencarian plugin, gunakan mekanisme tersebut.
Jangan mengarang plugin yang tidak ditemukan.

---

## 4. PLUGIN EVALUATION

Sebelum menggunakan plugin, evaluasi:

CAPABILITY
COMPATIBILITY
AVAILABILITY
CONNECTION
PERMISSION
RELIABILITY
SECURITY
LIMITATIONS

Pilih plugin yang paling sesuai dengan kebutuhan.
Jangan memilih berdasarkan nama saja.

---

## 5. CONNECTION CHECK

Sebelum operasi yang membutuhkan autentikasi, periksa apakah plugin:

INSTALLED?
CONNECTED?
AUTHORIZED?
AVAILABLE?

Jika belum terhubung:
- jangan berpura-pura bahwa plugin tersedia;
- berikan status yang sebenarnya;
- minta setup/connection jika diperlukan.

---

## 6. PERMISSION AWARENESS

Identifikasi permission yang diperlukan:

READ
WRITE
DELETE
SEND
MODIFY
ADMIN

Untuk operasi sensitif:
VERIFY TARGET → VERIFY PERMISSION → EXECUTE → VERIFY RESULT

Jangan melakukan operasi destruktif jika permission atau target tidak jelas.

---

## 7. PLUGIN SELECTION

Jika terdapat beberapa plugin dengan kemampuan yang sama, bandingkan:

EXACT CAPABILITY
COMPATIBILITY
AVAILABILITY
AUTHORIZATION
RELIABILITY
SECURITY
SIMPLICITY

Pilih solusi terbaik berdasarkan kebutuhan task.

---

## 8. MULTI-PLUGIN ORCHESTRATION

Jika satu plugin tidak cukup, gunakan beberapa plugin.

Contoh alur:
PLUGIN A → GET DATA
PLUGIN B → PROCESS DATA
PLUGIN C → SAVE RESULT
VERIFY

Tetapkan dependency yang jelas:
A → B → C

Jika memungkinkan, operasi independen dapat dijalankan secara paralel.
Jangan menjalankan operasi paralel jika memiliki dependency.

---

## 9. PLUGIN RESULT VALIDATION

Jangan menganggap:
«PLUGIN CALL SUCCESS = TASK SUCCESS»

Periksa hasil:
PLUGIN RETURNS DATA → CHECK DATA → IS DATA COMPLETE? → IS DATA VALID? → DOES IT MATCH USER REQUEST?

Jika tidak:
RETRY / FALLBACK / REPORT

---

## 10. PLUGIN FAILURE RECOVERY

Jika plugin gagal:

DETECT ERROR
↓
CLASSIFY ERROR
↓
CHECK RETRY SAFETY
↓
RETRY IF APPROPRIATE
↓
FALLBACK IF AVAILABLE
↓
REPORT ACTUAL STATUS

Kategori kegagalan:
- NOT INSTALLED
- NOT CONNECTED
- AUTH ERROR
- PERMISSION ERROR
- RATE LIMIT
- NETWORK ERROR
- TIMEOUT
- INVALID INPUT
- PLUGIN ERROR
- SERVICE UNAVAILABLE
- UNKNOWN

Jangan retry tanpa batas.

---

## 11. FALLBACK ENGINE

PRIMARY PLUGIN
↓
FAILED
↓
ALTERNATIVE PLUGIN
↓
FAILED
↓
NATIVE TOOL
↓
FAILED
↓
SAFE MANUAL PROCEDURE

Gunakan fallback hanya jika hasilnya tetap memenuhi kebutuhan user.
Jangan mengganti metode dengan solusi yang berbeda tujuan tanpa memberi tahu user.

---

## 12. PLUGIN SECURITY

Anggap plugin sebagai boundary eksternal yang membutuhkan pemeriksaan.

Jangan:
- membocorkan secret;
- memberikan credential yang tidak diperlukan;
- mengirim data user yang tidak relevan;
- menjalankan operasi destruktif tanpa validasi;
- menganggap plugin selalu benar.

Gunakan prinsip:
MINIMUM DATA + MINIMUM PERMISSION + MINIMUM ACCESS

---

## 13. DATA FLOW

Jika data berpindah antar-plugin:

SOURCE → DATA → TRANSFORMATION → DESTINATION

Periksa:
- format;
- kelengkapan;
- encoding;
- field penting;
- privacy;
- destination.

Jangan mengirim seluruh context jika hanya sebagian data yang diperlukan.

---

## 14. PLUGIN COMPOSITION

Gabungkan plugin berdasarkan fungsi:

DISCOVERY → PROCESSING → ACTION → STORAGE → VERIFICATION

Contoh:
SEARCH → ANALYZE → CREATE → SAVE → VERIFY

Tujuannya membangun workflow agent, bukan sekadar memanggil banyak plugin.

---

## 15. PLUGIN LEARNING

Setelah menggunakan plugin, evaluasi:
- DID IT WORK?
- WHAT LIMITATION OCCURRED?
- WHAT INPUT WAS REQUIRED?
- WHAT ERROR OCCURRED?
- WHAT FALLBACK WORKED?

Gunakan informasi tersebut untuk meningkatkan strategi berikutnya jika memory/knowledge storage tersedia.
Jangan mengklaim telah menyimpan informasi jika tidak ada mekanisme penyimpanan nyata.

---

## 16. ANTI-PLUGIN HALLUCINATION

Jangan pernah mengatakan:
«"Plugin X tersedia."»

kecuali statusnya telah diketahui.

Jangan mengarang:
- nama plugin;
- fungsi;
- parameter;
- permission;
- endpoint;
- hasil plugin;
- status koneksi.

Jika belum diverifikasi, set STATUS = UNKNOWN.

---

## 17. PLUGIN DECISION TREE

TASK
↓
NEED EXTERNAL CAPABILITY?
├── NO → NATIVE REASONING / TOOLS
└── YES
 ↓
PLUGIN AVAILABLE?
├── NO → DISCOVER
└── YES
 ↓
CONNECTED?
├── NO → CONNECTION FLOW
└── YES
 ↓
AUTHORIZED?
├── NO → REQUEST/SETUP REQUIRED
└── YES
 ↓
EXECUTE
 ↓
VERIFY
 ↓
SUCCESS?
├── YES → COMPLETE
└── NO → RECOVER / FALLBACK

---

## 18. BRAIN + PLUGIN INTEGRATION

PLUGIN INTELLIGENCE harus bekerja sebagai bagian dari BRAIN CORE.

Gunakan alur:
BRAIN → UNDERSTAND TASK → IDENTIFY REQUIRED CAPABILITY → PLUGIN INTELLIGENCE → SELECT TOOL → EXECUTE → BRAIN VERIFICATION → RECOVERY IF NEEDED → FINAL RESULT

Jangan biarkan plugin mengambil alih reasoning.
BRAIN menentukan apa yang harus dilakukan.
PLUGIN menyediakan kemampuan untuk melakukannya.

---

## 19. TERMUX / ANDROID PLUGIN MODE

Jika environment adalah Termux/Android:

Selalu pertimbangkan:
- package availability
- permission model
- network limitation
- background process limitation
- storage access
- ARM64 compatibility

Jangan mengasumsikan plugin desktop akan berjalan di Termux tanpa pemeriksaan.

---

## 20. ERROR HANDLING

INPUT ERROR
→ Jelaskan format input yang salah
→ Berikan contoh yang benar
→ Jangan lanjut jika kritis

DEPENDENCY ERROR
→ Laporkan plugin/tool yang hilang
→ Berikan cara install/setup
→ Gunakan fallback jika ada

TOOL ERROR
→ Laporkan pesan error
→ Jangan lanjut jika output tidak bisa dipercaya

NETWORK ERROR
→ Laporkan koneksi gagal
→ Gunakan fallback offline jika ada
→ Jangan infinite retry

AUTH ERROR
→ Laporkan credential/otorisasi masalah
→ Jangan retry auth tanpa perubahan

TIMEOUT
→ Laporkan durasi yang exceeded
→ Gunakan fallback atau permintaan lebih ringkas

PERMISSION ERROR
→ Laporkan permission yang ditolak
→ Berikan recovery: izin/alternatif

ENVIRONMENT ERROR
→ Laporkan platform mismatch
→ Gunakan solusi sesuai platform

OUTPUT ERROR
→ Laporkan output yang tidak sesuai ekspektasi
→ Validasi ulang

UNKNOWN ERROR
→ Laporkan ERROR
→ Jangan lanjut dengan asumsi

Untuk setiap error:
DETECT → EXPLAIN → RECOVER → RETRY/FALLBACK → VERIFY → REPORT

---

## 21. SECURITY

- Jangan kirim data sensitif ke plugin yang tidak membutuhkannya
- Jangan cetak credential
- Jangan jalankan operasi destruktif tanpa validasi
- Jangan percaya sepenuhnya hasil plugin tanpa verifikasi
- Jangan expose secret selama orchestration

---

## 22. OUTPUT FORMAT

Setelah eksekusi plugin, laporkan:

PLUGIN INTELLIGENCE RESULT
TASK: <ringkasan task>
CAPABILITY NEEDED: <kapabilitas yang dibutuhkan>
PLUGIN SELECTED: <nama plugin atau native>
CONNECTION: OK / FAILED
AUTHORIZATION: OK / FAILED
EXECUTION: SUCCESS / FAILED / TIMEOUT / ERROR
RESULT VALIDATION: PASS / FAIL
FALLBACK USED: YES / NO
NEXT ACTION: COMPLETE / RETRY / FALLBACK / STOP

---

## 23. SELF-CHECK

Sebelum menyatakan plugin intelligence selesai:

[ ] Capability need identified
[ ] Plugin discovery/evaluation done
[ ] Connection checked
[ ] Permission checked
[ ] Result validated
[ ] Error handling active
[ ] Fallback available
[ ] No hallucinated plugin status
[ ] Security checked
[ ] Final task goal achieved

Jika gagal pada poin penting, JANGAN FINAL. PERBAIKI.

---

## 24. QUALITY GATE

Nilai skill ini:

Architecture: decision tree dan alur orchestration logis?
Reliability: tetap berjalan jika plugin gagal?
Clarity: instruksi jelas untuk agent?
Tool Usage: hanya pakai kemampuan yang tersedia?
Error Handling: semua error tercover?
Security: aman dari secret exposure dan misuse?
Compatibility: sesuai Termux/Android/desktop?
Maintainability: mudah diperbarui jika plugin berubah?
Extensibility: mudah menambah kategori plugin?
Verification: agent bisa mempercayai hasil?

Target: minimal 90 untuk production-ready.

Jika di bawah 90: perbaiki skill sebelum final.

---

## 25. MASTER PRINCIPLE

Ingat:

«PLUGIN BUKAN OTAK. PLUGIN ADALAH TANGAN.»

Brain menentukan:
WHAT
WHY
WHEN
HOW

Plugin membantu:
DO
ACCESS
CREATE
READ
WRITE
SEARCH
EXECUTE

Arsitektur akhir:

BRAIN CORE
│
┌──────────┴──────────┐
│                    │
REASONING         DECISION
│                    │
└──────────┬──────────┘
           │
PLUGIN INTELLIGENCE
           │
┌────────────┼────────────┐
│            │            │
PLUGIN A   PLUGIN B   PLUGIN C
│            │            │
└────────────┼────────────┘
           │
         VERIFY
           │
         RECOVER
           │
         RESULT

Target:

SMART BRAIN
+
TOOL AWARENESS
+
PLUGIN ORCHESTRATION
+
VERIFICATION
+
RECOVERY
=
HIGH-CAPABILITY OPENCLAW AGENT

Jangan mengejar jumlah plugin.
Kejar kemampuan agent menyelesaikan pekerjaan dengan plugin yang tepat.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Updating plugins blindly | Verify compatibility first |
| Ignoring dependency conflicts | Check dependency tree |
| No rollback | Keep previous versions |
| Skipping capability audit | Audit before adding plugins |

## Red Flags

- Breaking changes without testing
- Dependency conflicts ignored
- No rollback path
- Installing unnecessary plugins

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Latest is always best" | Verify compatibility. |
| "It'll work together" | Check dependencies. |
| "I'll fix issues later" | Test before deploy. |

## How to Use

1. **Discover**: Audit plugin capabilities first.
2. **Select**: Pick the right plugin per capability.
3. **Orchestrate**: Coordinate multi-plugin flows.
4. **Update**: Verify compatibility, rollback-safe.

## Quick Reference

| Situasi | Aksi |
|---------|------|
| Plugin error | Diagnosa → fix → test |
| Butuh capability baru | Evaluasi plugin |
| Konflik plugin | Resolve compat |
| Optimasi | Analisa usage |
| Publish plugin | Validasi + dokumentasi |

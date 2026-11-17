# SETUP-ADMIN — Hướng dẫn cho ADMIN (làm 1 lần, phát cho cả phòng)

Tài liệu này dành cho **người quản trị** (anh/chị phụ trách kỹ thuật).
Mục tiêu: tạo **1 app OAuth duy nhất** trên Google Cloud, rồi phát `zip` + `cặp mã`
cho nhân sự. Nhân sự **không cần vào Cloud Console**, chỉ cần dán 2 mã vào chat.

**Thời gian:** ~5 phút, làm 1 lần. Sau đó phục vụ tới **100 người** (nhiều hơn thì Publish app).

---

## 0. Hiểu đúng trước khi làm (30 giây)

Chia sẻ **cặp mã app** KHÔNG phải chia sẻ tài khoản Google. Cụ thể:

| Thứ | Dùng chung? | Ý nghĩa |
|---|---|---|
| OAuth Client ID + Secret | ✅ Có, phát cho mọi người | Chỉ là "tên đăng ký app". Không mở được Drive của ai. |
| Tài khoản Google | ❌ Mỗi người riêng | Mỗi người bấm Allow bằng **email của chính họ**. |
| Dữ liệu Drive | ❌ Mỗi người riêng | Token lưu trên máy từng người. Không ai đọc được Drive người khác. |

⚠️ **Rủi ro tập trung duy nhất:** nếu sau này xoá project hoặc tạo lại app → **tất cả mọi người
mất kết nối**, phải bấm Allow lại. Vì vậy: **tạo 1 lần, giữ nguyên, đừng xoá project.**

---

## 1. Tạo project trên Google Cloud

1. Vào `https://console.cloud.google.com` → đăng nhập bằng tài khoản Google của admin.
2. Góc trên trái, bấm ô chọn project → **New Project**.
3. Đặt tên, ví dụ `ent-marketing-bot` → **Create**.
4. Chờ ~10 giây, chọn project vừa tạo (tên hiện ở thanh trên cùng).

## 2. Bật 2 API

1. Menu trái → **APIs & Services** → **Library**.
2. Tìm `Google Drive API` → bấm → **Enable**.
3. Quay lại Library → tìm `Google Sheets API` → bấm → **Enable**.

> ⚠️ Thiếu bước này → mọi lệnh sau sẽ trả `403 insufficientPermissions`.

## 3. Cấu hình OAuth consent screen

1. Menu trái → **APIs & Services** → **OAuth consent screen**.
2. Chọn **External** → **Create**.
3. Điền:
   - **App name**: tên hiển thị khi người dùng bấm Allow (vd `ENT Marketing Bot`).
     → Người dùng SẼ thấy tên này. Nên đặt tên trung tính, rõ nguồn.
   - **User support email**: email của admin.
   - **Developer contact email**: email của admin.
4. **Save and continue** qua các bước → tới **Scopes** có thể bỏ qua (skill tự xin scope khi chạy).
5. **Test users**: nếu app còn ở chế độ **Testing**, thêm email của **từng người dùng**
   (tối đa 100) → nếu không thêm, họ sẽ bị chặn với lỗi `access_blocked`.
6. **Publish app** (bấm nút này ở trang OAuth consent screen):
   - Nếu để **Testing** → phiên của mọi người **hết hạn sau 7 ngày**, phải Allow lại liên tục.
   - Bấm **Publish** → phiên sống lâu. (Với scope Drive/Sheets dùng nội bộ, Google thường
     không bắt verify nếu chỉ dùng cho tổ chức của mình; nếu Google có yêu cầu verify thì
     làm theo hướng dẫn của họ.)

## 4. Tạo OAuth Client (Desktop app)

1. Menu trái → **APIs & Services** → **Credentials**.
2. **+ Create credentials** → **OAuth client ID**.
3. **Application type**: chọn **Desktop app** ← ⚠️ RẤT QUAN TRỌNG.
   - Chọn sai (Web application) → người dùng gặp lỗi `Error 400: redirect_uri_mismatch`.
4. Đặt tên (vd `ENT Drive Connector`) → **Create**.
5. Màn hình hiện ra 2 mã:
   - **Client ID** — dạng `1234567890-abcdefg.apps.googleusercontent.com`
   - **Client secret** — chuỗi bắt đầu bằng `GOCSPX-` (lấy ở cùng màn hình với Client ID)
6. **Copy cả 2 mã ra chỗ an toàn** (mật khẩu/note riêng). Google **không cho xem lại**
   client secret sau khi đóng hộp thoại — nếu mất phải tạo client mới.

> 💡 Client secret của **Desktop app** được Google coi là public (ai tải app về cũng thấy).
> Nó KHÔNG phải chìa khoá mở Drive. Cái bảo vệ dữ liệu là bước đăng nhập + Allow của
> từng người. Vẫn nên phát riêng từng người, đừng đăng công khai.

---

## 5. Lưu app trên máy admin

Có 2 cách — chọn 1:

**Cách A (khuyến nghị) — qua chat với agent:**
Dán vào chat với agent của bạn:

```
Mã 1 (Client ID): (dán client id của bạn vào đây)
Mã 2 (Client secret): (dán client secret của bạn vào đây)
Lưu app OAuth này giúp tôi.
```

Agent sẽ chạy `gdrive_connect.py import-app`, lưu vào `~/.config/gdrive-connect/app.json`
với quyền 600, và không in secret ra chat.

**Cách B — bằng tay (nếu không dùng agent):**

```bash
mkdir -p ~/.config/gdrive-connect && chmod 700 ~/.config/gdrive-connect
printf '{"client_id":"%s","client_sec":"%s"}' "$CLIENT_ID" "$CLIENT_SECRET" > ~/.config/gdrive-connect/app.json
chmod 600 ~/.config/gdrive-connect/app.json
```

Kiểm tra đã đúng: `python3 scripts/gdrive_connect.py check`
→ kỳ vọng: `app OAuth: ✅ có` / `phiên đăng nhập: ❌ CHƯA CÓ` (chưa kết nối là bình thường).

---

## 6. Phát cho nhân sự — MẪU TIN NHẮN COPY-PASTE

Gửi **file zip** kèm đoạn dưới (thay `<...>` bằng mã thật):

```
Chào em, anh gửi em công cụ để agent tự tạo/sửa Google Sheet giúp em.

BƯỚC 1 — Gửi file zip này vào chat với agent của em, kèm câu:
"Tôi vừa gửi file zip skill google-sheets-connect. Hãy giải nén và cài skill này
vào workspace của bạn."

BƯỚC 2 — Khi agent báo cài xong, gửi tiếp 2 mã sau cho agent:
Mã 1 (Client ID): (dán client id)
Mã 2 (Client secret): (dán client secret)
(kèm câu: "Lưu app OAuth này giúp tôi")

BƯỚC 3 — Agent sẽ gửi em 1 đường link Google. Bấm link:
  - Chọn ĐÚNG tài khoản Google của em
  - Bấm "Allow" (Cho phép)
  - Google hiện 1 mã dạng 4/0A... → copy, dán lại vào chat cho agent

Xong. Từ giờ em chỉ cần nói: "Tạo cho tôi Google Sheet tên ... trong Drive"
là agent làm được.

Lưu ý: quyền này chỉ mở Drive của CHÍNH EM, không ai xem được Drive của em,
và em cũng không xem được Drive người khác.
```

---

## 7. Bảng bẫy hay gặp (tra nhanh)

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| `invalid_client` | mã sai/chưa lưu đúng | chạy `import-app` lại, kiểm tra `check` |
| `Error 400: redirect_uri_mismatch` | app tạo sai loại (Web thay vì Desktop) | tạo lại OAuth client, chọn **Desktop app** |
| `access_blocked` / `org_internal` | app còn Testing mà email người dùng chưa nằm trong Test users | thêm email vào Test users, hoặc Publish app |
| Phiên chết sau ~7 ngày | app còn ở Testing | bấm **Publish app** |
| `403 insufficientPermissions` | chưa bật Drive/Sheets API | bật trong Library (mục 2) |
| `403 storageQuotaExceeded` | Drive người dùng đầy | bảo người dùng dọn bớt |
| Người dùng không thấy file của người khác | đúng thiết kế | share Editor nếu cần cùng sửa |
| `invalid_grant` khi dán mã | mã đã dùng / quá 10 phút | chạy `start` lấy link mới |

---

## 8. Kiểm tra sức khoẻ hệ thống (định kỳ)

```bash
python3 scripts/gdrive_connect.py check     # app OAuth + phiên có chưa
python3 scripts/gdrive_ops.py selftest      # test thật: tạo folder → Sheet → ghi → format → đọc → xoá
python3 scripts/gdrive_connect.py status    # email đang kết nối + quota
```

Kỳ vọng `selftest`: 6/6 ✅. Nếu có bước ⚠️ → báo đúng bước đó, không nói "thành công" chung.

---

## 9. Phát cho người NGOÀI công ty

Cân nhắc lại: họ sẽ thấy **tên app của bạn** trên màn hình Allow. Nếu không muốn,
2 lựa chọn:
- Đặt app name trung tính ngay từ đầu (mục 3).
- Hoặc để họ tự tạo project riêng (theo `CAI-DAT.md`, mục Bước 4).

Giới hạn cứng cần nhớ:
- **Testing mode: tối đa 100 test users.**
- Vượt 100 → phải **Publish app** (có thể Google yêu cầu verify với scope nhạy cảm).

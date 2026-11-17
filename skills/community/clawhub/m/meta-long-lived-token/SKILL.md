---
name: "meta-long-lived-token"
description: "Đổi Meta short-lived token (~1-2h) sang long-lived token (~60 ngày) qua Graph API, kiểm tra hạn, lưu vào env gateway và nhắc gia hạn. READ-ONLY với ads."
---

# Meta Long-Lived Token — đổi & gia hạn token Meta Ads

Đổi **short-lived user token** (~1–2 giờ) thành **long-lived token** (~60 ngày) qua Graph API chính thức, kiểm tra hạn và lưu an toàn vào env của gateway.

> 🔒 **An toàn:** skill này CHỈ gọi endpoint `oauth/access_token` (đổi token) + `debug_token` (kiểm tra). KHÔNG đọc/sửa dữ liệu quảng cáo. KHÔNG gọi POST/DELETE tới ads.

## 0. KÍCH HOẠT — câu lệnh người dùng chỉ cần nhập

Khi người dùng gửi tin nhắn dạng:

```
Em gia hạn token thêm 60 ngày nhé.
ID App: <APP_ID>
Secrect key: <APP_SECRET>
```

Agent PHẢI hiểu là: **đổi token hiện tại (short-lived) sang long-lived** bằng App ID + App Secret đã cung cấp.

### Quy trình tự động khi nhận câu lệnh trên

0. **LẤY TOKEN ĐANG CÓ — ĐỌC TỪ FILE CONFIG, KHÔNG DÙNG BIẾN ENV** (bắt buộc, làm trước mọi thứ):

```bash
python3 -c "import json;d=json.load(open('/opt/openclaw/config/openclaw.json'));t=d.get('env',{}).get('META_ACCESS_TOKEN','');print('CO_TOKEN' if t else 'KHONG_CO_TOKEN')"
```

- **`KHONG_CO_TOKEN` → DỪNG NGAY.** Báo: *"Máy này chưa có `META_ACCESS_TOKEN` trong config. Anh dán token Meta (`EAA...`) vào chat trước, rồi gửi lại lệnh gia hạn."* **KHÔNG** chạy lệnh đổi token, **KHÔNG** hỏi App ID/Secret (App Secret không thiếu — token mới là cái thiếu).
- **`CO_TOKEN`** → tiếp tục bước 1.

> 🔴 **ĐÂY LÀ LỖI SỐ 1 KHI CÀI SANG MÁY KHÁC.** Skill bản cũ ghi `echo $META_ACCESS_TOKEN`, dẫn tới 2 hỏng:
> a) Máy mới **chưa từng chạy `ent-meta-connect`** → env rỗng → `fb_exchange_token=` rỗng → Meta trả lỗi, agent lại đi đổ lỗi "App ID / Secret sai" dù anh nhập đúng.
> b) Sau khi restart, **phiên exec của agent KHÔNG reload env** → vẫn là token CŨ/chuỗi rỗng → test báo sai giả.
> ⇒ Luôn đọc từ **file** `/opt/openclaw/config/openclaw.json`, không bao giờ từ `$META_ACCESS_TOKEN`.

1. **Trích xuất** `APP_ID` và `APP_SECRET` từ tin nhắn (chấp nhận ghi đúng/sai chính tả như "Secrect key", "Secret", "App Secret", "Secret key").
   - `APP_ID` phải là **dãy số 15–16 chữ số** (vd `2166578660953478`). Nếu không phải → hỏi lại.
   - `APP_SECRET` phải là **chuỗi hex 32 ký tự**. Nếu khác → cảnh báo có thể copy thiếu, nhưng vẫn thử.
   - Nếu THIẾU cái nào → hỏi đúng cái đó.
2. **Kiểm tra token hiện có** bằng `debug_token` (mục 4) **trước khi đổi**:
   - `is_valid: true` → đổi tiếp.
   - `is_valid: false` → **DỪNG**, báo token đang chết, yêu cầu dán token mới. Đừng đổi bằng token chết rồi báo lỗi secret.
   - Ghi nhận `app_id` của token. **Nếu `app_id` trong token KHÁC `APP_ID` anh vừa đưa → cảnh báo ngay**: token thuộc app khác, secret của app này không dùng được.
3. **Đổi sang long-lived** (mục 3 bên dưới).
4. **Kiểm tra** token mới bằng `debug_token` (mục 4).
5. **Lưu** token mới vào env gateway, **giữ nguyên env cũ**, rồi restart (mục 5).
6. **Test lại** sau restart — **đọc token từ file** (không dùng `$META_ACCESS_TOKEN`) + **báo ngắn gọn**: token hợp lệ, hạn mới (`expires_at`), số ngày còn lại.

> ⚠️ Nếu token hiện tại đã là long-lived (`expires_at` còn > 30 ngày) → **báo trước** rằng token vẫn đang tốt; nếu anh vẫn muốn gia hạn thì re-exchange bình thường (+60 ngày kể từ lúc đổi).
> ⚠️ Chỉ thực thi khi người gửi là **owner**. Nếu không chắc → hỏi xác nhận trước khi ghi config.

## 1. Cần chuẩn bị

| Thứ | Lấy ở đâu |
|-----|-----------|
| `SHORT_LIVED_TOKEN` | Token tạm từ Graph API Explorer (xem mục 2) — sống ~1–2h |
| `APP_ID` | App ID của app Facebook (developers.facebook.com → App settings → Basic) |
| `APP_SECRET` | App Secret cùng trang (bấm "Show") |

⚠️ **Cần cả APP_SECRET** — không có secret thì KHÔNG đổi được sang long-lived. Nếu app chưa có secret → vào App settings → Basic để lấy.

## 2. Lấy short-lived token

1. Vào `developers.facebook.com/tools/explorer`
2. Chọn app (loại Business)
3. Thêm quyền cần dùng — tối thiểu `ads_read` (thêm `ads_management` nếu cần ghi; thêm `pages_manage_posts`, `pages_read_engagement` nếu dùng page)
4. **Generate Access Token** → đăng nhập → cho phép
5. Copy token (bắt đầu bằng `EAA...`) — token này chỉ sống ~1–2h

## 3. Đổi sang long-lived token

```bash
curl -s -G "https://graph.facebook.com/v21.0/oauth/access_token" \
  --data-urlencode "grant_type=fb_exchange_token" \
  --data-urlencode "client_id=$APP_ID" \
  --data-urlencode "client_secret=$APP_SECRET" \
  --data-urlencode "fb_exchange_token=$SHORT_LIVED_TOKEN"
```

Kết quả trả JSON: `{"access_token":"EAA...","token_type":"bearer","expires_in":5184000}`
→ `expires_in` ~**5.184.000 giây ≈ 60 ngày**. Đây là token long-lived cần lưu.

> 💡 **KHÔNG cần xin token mới để đổi long-lived.** Token short-lived đang lưu trong config là đủ — `fb_exchange_token` chấp nhận cả token short-lived lẫn long-lived còn hạn. Chỉ khi `debug_token` trả `is_valid: false` mới phải xin token mới.
> 💡 **Re-exchange được nhiều lần** — mỗi lần +60 ngày, không ảnh hưởng dữ liệu ads.
> 💡 **`debug_token` KHÔNG cần App Secret** (kiểm chứng 19/10): `input_token` = chính token, `access_token` = chính token là được. Chỉ `oauth/access_token` mới cần secret.

> ⚠️ **Không bao giờ nhét token thẳng vào URL bằng dấu ngoặc kép** → shell cắt chuỗi → lỗi 4xx GIẢ. Luôn dùng `curl -G --data-urlencode "...=$TOKEN"`.

## 4. Kiểm tra token vừa đổi (bắt buộc)

```bash
curl -s -G "https://graph.facebook.com/v21.0/debug_token" \
  --data-urlencode "input_token=$LONG_LIVED_TOKEN" \
  --data-urlencode "access_token=$LONG_LIVED_TOKEN"
```

Đọc `data`:
- `is_valid: true` → OK
- `expires_at`: epoch giây **ngày hết hạn** (~60 ngày tới). Nếu `0` → token không đặt ngày hết hạn (một số app dev/test).
- `data_access_expires_at`: mốc chặn truy cập dữ liệu (thường xa hơn `expires_at`) — **theo dõi mốc này làm mốc phụ**.
- `scopes`: phải có quyền cần dùng (`ads_read`...).

## 5. Lưu vào env gateway (không hardcode)

- Đọc config hiện tại, **giữ nguyên toàn bộ env cũ**, chỉ cập nhật khóa `META_ACCESS_TOKEN` (và `META_AD_ACCOUNT_ID` nếu có).
- Dùng merge (không ghi đè cả file config).
- Sau khi lưu → **restart gateway** để env nạp lại, rồi chạy lại `debug_token` với `$META_ACCESS_TOKEN` để xác nhận.
- **KHÔNG echo token ra chat/log**, KHÔNG commit token vào git.

## 6. Theo dõi hạn & nhắc gia hạn

- Long-lived token hết hạn sau **~60 ngày** → phải **đổi lại** (lặp lại mục 2–4) trước khi hết.
- Đặt lịch kiểm tra định kỳ (cron preflight hằng ngày) gọi `debug_token`, tính số ngày còn lại:
  - Còn **< 14 ngày** → **nhắc owner** đổi token mới.
  - `is_valid: false` hoặc lỗi `190` → token chết, báo owner lấy token mới ngay.
- Lưu ý: **không có cơ chế tự gia hạn hoàn toàn** cho token user — vẫn cần thao tác đăng nhập để lấy short-lived mới. (System User token mới là loại có thể không hết hạn.)

## 7. Trả lời nhanh câu hỏi thường gặp

| Câu hỏi | Trả lời |
|---|---|
| Đổi long-lived gia hạn thêm bao nhiêu? | Từ ~1–2h lên **~60 ngày** → thêm **~59 ngày** |
| Trần tối đa được bao nhiêu? | **~60 ngày** cho token user, không vượt được |
| Hết 60 ngày thì sao? | Đổi lại (re-exchange) → **thêm ~60 ngày/lần** |
| Có loại nào không hết hạn? | **System User token** (Business Manager) — tuỳ cấu hình |

## Xử lý sự cố

### 🔑 Bảng phân biệt lỗi — ĐỌC TRƯỚC KHI KẾT LUẬN "SAI ID/SECRET"

| Meta trả về | Nghĩa THẬT | Việc phải làm |
|---|---|---|
| `Error validating client secret.` (code 1) | **App Secret sai/thiếu/rỗng** — hoặc `client_id` không khớp secret | Kiểm tra Secret (32 hex) + App ID (dãy số). **Không** đổ cho token. |
| `(#200) Provide valid app ID` | `client_id` sai/thiếu | Kiểm tra `APP_ID` |
| `Invalid OAuth access token - Cannot parse access token` (190) | **Token đầu vào** rỗng/hỏng | Kiểm tra bước 0 — có đọc được token từ config không? |
| `Invalid OAuth access token` + expired | Token **hết hạn** | Xin token mới ở Graph Explorer |
| `190` + subcode `459` + `checkpoint_url` | Tài khoản FB bị **checkpoint** | Vào facebook.com xử lý cảnh báo rồi lấy token mới |
| `190` + subcode `460` | Mật khẩu FB đổi / phiên thu hồi | Lấy token mới |
| Lỗi 4xx "giả" dù token đúng | Token nhét thẳng vào URL bị shell cắt | Dùng `curl -G --data-urlencode` |

> ⚠️ **Thứ tự chẩn đoán BẮT BUỘC khi đổi thất bại:** (1) token có tồn tại trong config chưa? (2) `debug_token` nói `is_valid` gì? (3) `app_id` trong token có khớp `APP_ID` anh đưa không? — **Chỉ sau 3 bước đó** mới được kết luận secret sai.

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Error validating client secret` | Secret sai/thiếu/rỗng (đã test 19/10: Meta trả lỗi này kể cả khi token rỗng) | Lấy lại Secret ở App settings → Basic → Show, đúng 32 ký tự |
| Máy mới báo sai secret dù nhập đúng | Config máy đó **chưa có `META_ACCESS_TOKEN`** → `fb_exchange_token` rỗng | Chạy bước 0; dán token trước rồi mới gia hạn |
| Sau restart test vẫn báo token sai | Phiên exec không reload env | Đọc token từ file `/opt/openclaw/config/openclaw.json` |
| `expires_in` rất ngắn | Token đầu vào đã là long-lived | Bình thường với re-exchange; kiểm `expires_at` |
| Không có APP_SECRET | App thiếu secret | App settings → Basic → Show secret |

## Bảo mật — BẮT BUỘC

- Chỉ nhận token từ **owner** của máy/agent.
- KHÔNG ghi token ra file log, KHÔNG echo token ra chat.
- KHÔNG chia sẻ token sang máy/agent khác.
- Token trong lịch sử chat là rủi ro → cân nhắc rotate sau khi dùng xong với token quan trọng.

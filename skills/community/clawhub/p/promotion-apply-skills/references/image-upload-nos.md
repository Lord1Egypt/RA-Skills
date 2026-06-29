# Image Upload NOS Reference

图片字段由创意模板动态决定。用户提供本地图片、图片 URL，或需要从资源封面生成图片 URL 时，先按模板校验尺寸，再申请 NOS token 并上传。

约束：

- token 申请必须走 `mws link backend-nos-token-whalealloc`。
- 文件二进制上传不是 Link 平台接口，允许使用 NOS HTTP 上传。
- 不要用 HTTP 直调任何 Link 平台接口。
- 多张图片上传时必须“申请一个 token -> 立即解析 -> 立即上传 -> 再处理下一张”。不要并行申请多个 NOS token，因为 MWS 可能把返回写到同一个 `download.txt`，并行时会互相覆盖。

## 文件处理

### 图片 URL 路由

用户本轮提供的任何图片 URL 都按“原始素材”处理，不能直接写入 `creativeDetailDataVO.children[].data`：

- 包括普通 http/https 图片、NOS/NOSK 地址、`mb-mlbclaw-pub`、`nos-jd`、`p5.music.126.net` 等看起来已经上传过的图片地址。
- 必须先下载到本地临时文件，再按当前模板当前字段的 `width/height` 做尺寸校验。
- 尺寸不符时按本页裁剪/缩放规则处理，并让用户确认裁剪结果。
- 用户确认后，必须通过本轮 `backend-nos-token-whalealloc` 申请 token 并重新上传 NOS。
- 最终 payload 只能写本轮上传得到的 URL。

唯一例外：该图片 URL 来自当前 `promotion-detail` 已有创意，且用户本轮明确说“沿用当前推广已有素材”。这时可以保留已有 URL，不再下载重传。

下载示例：

```bash
IMG_URL="https://mb-mlbclaw-pub.nos-jd.163yun.com/uploads/xxx.jpg"
TMP_FILE="/tmp/promotion_input_$(date +%Y%m%d%H%M%S).jpg"
curl -L --fail --retry 2 --connect-timeout 10 --max-time 60 "$IMG_URL" -o "$TMP_FILE"
python3 scripts/validate_image_size.py "$TMP_FILE" 1080 607
```

`1080 607` 只是示例。真实宽高必须来自当前模板当前字段的 `conditionConfig[resourceTypeCode][fieldName].width/height`。

如果用户确认允许裁剪/缩放，可使用本 skill Python 脚本按模板目标宽高做中心裁剪：

```bash
python3 scripts/resize_cover.py \
  "<图片URL或本地文件路径>" \
  "/tmp/promotion_creative_1080x607.jpg" \
  1080 607
```

`1080 607` 只是示例。真实宽高必须来自当前模板当前字段的 `conditionConfig[resourceTypeCode][fieldName].width/height`。

裁剪规则：

- 只允许从大图裁成小图，或大图等比缩放后中心裁剪到目标尺寸。
- 如果原图宽或高小于目标宽高，禁止放大裁剪；停止并要求用户补更大原图。
- 如果用户未确认允许裁剪/缩放，尺寸不符时停止并要求用户补符合尺寸的原图。
- 裁剪生成后必须先让用户确认，用户确认后再上传 NOS。能在当前客户端渲染本地图片时，必须真实展示图片；不能渲染时只给本地绝对路径，不要声称“预览已展示”。

展示方式：回复里用 Markdown 图片引用本地绝对路径，例如：

```markdown
![裁剪预览](/tmp/promotion_creative_1080x607.jpg)
```

如果一次生成多张图，逐张展示并标清字段：

```markdown
大卡图片 1080x607：
![大卡裁剪预览](/tmp/promotion_bigPic_1080x607.jpg)

普通图片 1080x420：
![普通图裁剪预览](/tmp/promotion_pic_1080x420.jpg)
```

如果当前环境不能渲染图片，不要写“预览我已经展示了”。改为：

```text
已生成裁剪文件：
- 大卡图片 1080x607：/tmp/promotion_bigPic_1080x607.jpg
- 普通图片 1080x420：/tmp/promotion_pic_1080x420.jpg

当前环境无法直接展示图片，请打开以上路径确认视觉效果。
```

不要在用户确认裁剪结果前上传或保存该素材。

如果用户已经给了符合要求的本地图片，可直接使用原图。上传前必须先按创意模板 `conditionConfig` 校验图片尺寸，再用 `wc -c` 获取文件大小。

```bash
python3 scripts/validate_image_size.py \
  "$FILE" 1080 420
```

`1080 420` 只是示例。真实宽高必须来自当前模板当前字段的 `conditionConfig[resourceTypeCode][fieldName].width/height`。

## 申请 NOS Token

申请 NOS token：

```bash
FILE=/tmp/promotion_creative_1080x607.jpg
FILESIZE=$(wc -c < "$FILE" | tr -d ' ')

rm -f download.txt
mws link backend-nos-token-whalealloc --env ${MWS_ENV} --params "{\"filename\":\"promotion_creative_$(date +%Y%m%d%H%M%S).jpg\",\"fileSize\":${FILESIZE},\"type\":\"image\",\"bucket\":\"yyimgs\",\"bizKey\":\"17ea9ab6\"}"
```

必须从返回里解析：

- `bucket`
- `objectKey` 或等价对象 key 字段
- `token`

兼容说明：`mws` 有时返回 `{"saved_file":"download.txt"}`，此时必须读取最新 `download.txt`。执行前先删除旧文件，禁止复用旧 token。

多图上传时，每张图都按下面顺序执行：

1. 删除旧 `download.txt`。
2. 为当前这一张图申请 token，并把命令 stdout 保存到当前图片独有的临时文件。
3. 如果 stdout 里没有 `data` 而是落到了 `download.txt`，立即读取 `download.txt` 并解析。
4. 立刻上传当前图片。
5. 记录最终 `https://p5.music.126.net/<objectKey>`。
6. 再处理下一张图。

## 上传文件

拿到 `bucket/objectKey/token` 后，用 NOS HTTP 上传文件。上传地址和 header 以 token 返回字段为准；如果返回里没有 upload URL，可使用常见 NOS 直传形式：

```bash
curl -X POST "https://nosup-hz1.127.net/${BUCKET}/${OBJECT_KEY}?offset=0&complete=true&version=1.0" \
  -H "x-nos-token: ${TOKEN}" \
  -H "Content-Type: image/jpeg" \
  --data-binary @"$FILE"
```

如果上传返回的对象 key 与 token 阶段不同，以上传返回为准。

## 生成图片 URL

上传成功后拼接可用 URL：

```text
https://p5.music.126.net/<objectKey>
```

把该 URL 写入动态模板中代表图片的字段。图片字段可能叫 `pic`、`bigPic`、`url`、`imgUrl`、`picUrl` 等，必须从 `template.schema.children[].resourceTypeCodes[].resourceTypeFieldList[].fieldName` 获取。

# Imou Open API Reference – AI Multimodal Analysis

This document summarizes the APIs used by the Imou Multimodal Analysis skill. All requests must include header `Client-Type: OpenClaw`.

---

## 1. Base URL and Request Format

- **Base URL**: `https://openapi.lechange.cn` (configurable via `IMOU_BASE_URL`).
- **Method**: POST to `{base_url}/openapi/{method}`.
- **Body**: JSON. Same structure as other Imou skills: `system` (ver, appId, sign, time, nonce), `id`, `params`.
- **Sign**: MD5 of `time:{time},nonce:{nonce},appSecret:{appSecret}` (UTF-8), 32-char lowercase hex. `time` is UTC timestamp in **seconds**.

Response: `result.code` "0" means success.

---

## 2. accessToken – Get Admin Token

- **Doc**: https://open.imou.com/document/pages/fef620/
- **params**: `{}`.
- **Response data**: `accessToken`, `expireTime` (seconds). Token valid 3 days.

---

## 3. Image-based detection – Common params

All detection APIs that accept an image support:

| Param        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| token        | String | Y        | accessToken |
| type         | String | Y        | "0" = image URL, "1" = Base64 image data |
| content      | String | Y        | Image URL or Base64 string per type |
| detectRegion | Array  | N        | Up to 3 regions; each region 3–6 points `{ "x": float, "y": float }` (normalized 0–1). Converted to bounding rect for detection. |

---

## 4. humanDetect – Human detection

- **Doc**: https://open.imou.com/document/pages/93rflk/
- **URL**: `POST {base_url}/openapi/humanDetect`
- **params**: token, type, content, optional detectRegion.

**Response data**:

| Field         | Type    | Description |
|---------------|---------|-------------|
| detectResult  | Boolean | true = human detected, false = not |
| targets       | Array   | Each item: targetRegion { x, y, width, height } (px, origin top-left) |

---

## 5. smokingDetect – Smoking detection

- **Doc**: https://open.imou.com/document/pages/kf70sq/
- **URL**: `POST {base_url}/openapi/smokingDetect`
- **params**: token, type, content, optional detectRegion.

**Response data**: detectResult (Boolean), targets (targetRegion x, y, width, height).

---

## 6. phoneUsingDetect – Phone-using detection

- **Doc**: https://open.imou.com/document/pages/jf78o9/
- **URL**: `POST {base_url}/openapi/phoneUsingDetect`
- **params**: token, type, content, optional detectRegion.

**Response data**: detectResult (Boolean), targets (targetRegion).

---

## 7. workwearDetect – Workwear detection

- **Doc**: https://open.imou.com/document/pages/2jisd8/
- **URL**: `POST {base_url}/openapi/workwearDetect`
- **params**: token, type, content, **threshold** (Double, (0,1]), optional **repositoryId** (workwear target library), optional detectRegion.

**Response data**: targets (each: detectResult Boolean for compliance, targetRegion). detectResult true = compliant, false = not.

---

## 8. absenceDetect – Absence detection

- **Doc**: https://open.imou.com/document/pages/29dicv/
- **URL**: `POST {base_url}/openapi/absenceDetect`
- **params**: token, type, content, **repositoryId** (workwear library, required), **threshold** (Double, (0,1]), optional detectRegion.

**Response data**: detectResult, targets (targetRegion, etc.). Indicates whether post is occupied per workwear template.

---

## 9. shelfStatusDetect – Shelf detection

- **Doc**: https://open.imou.com/document/pages/2oud87/
- **URL**: `POST {base_url}/openapi/shelfStatusDetect`
- **params**: token, type, content, optional detectRegion.

**Response data**: Structure per official doc (shelf status result and targets).

---

## 10. trashOverflowDetect – Trash overflow detection

- **Doc**: https://open.imou.com/document/pages/cdmfd6/
- **URL**: `POST {base_url}/openapi/trashOverflowDetect`
- **params**: token, type, content, optional detectRegion.

**Response data**: detectResult, targets (overflow detection result).

---

## 11. heatmapDetect – Heatmap statistics

- **Doc**: https://open.imou.com/document/pages/fdjfg9/
- **URL**: `POST {base_url}/openapi/heatmapDetect`
- **params**: token, type, content, **threshold** (Double, (0,1]), optional **excludeRepositoryIds** (array of repository IDs to exclude matched workwear persons), optional detectRegion.

**Response data**: targets (targetRegion x, y, width, height for heatmap data).

---

## 12. faceAnalysis – Face analysis

- **Doc**: https://open.imou.com/document/pages/28d7ug/
- **URL**: `POST {base_url}/openapi/faceAnalysis`
- **params**: token, type, content, optional detectRegion.

**Response data**: Structure per official doc (face analysis result and targets).

---

## 13. createAiDetectRepository – Create detect repository

- **Doc**: https://open.imou.com/document/pages/34ff11/
- **URL**: `POST {base_url}/openapi/createAiDetectRepository`

**params**:

| Param           | Type   | Required | Description |
|-----------------|--------|----------|-------------|
| token           | String | Y        | accessToken |
| repositoryName  | String | Y        | Repository name |
| repositoryType  | String | Y        | "face" = face library, "human" = human/workwear library |

**Response data**: repositoryId (String). Use for workwear/absence and target add/list/delete.

---

## 14. listAiDetectRepositoryByPage – List repositories

- **Doc**: https://open.imou.com/document/pages/5e8222/
- **URL**: `POST {base_url}/openapi/listAiDetectRepositoryByPage`

**params**: token, page (from 1), pageSize.

**Response data**: count, repository list (repositoryId, repositoryName, repositoryType, etc.).

---

## 15. deleteAiDetectRepository – Delete repository

- **Doc**: https://open.imou.com/document/pages/5esi8a/
- **URL**: `POST {base_url}/openapi/deleteAiDetectRepository`

**params**: token, repositoryId.

**Response**: result.code "0".

---

## 16. addAiDetectTarget – Add target to repository

- **Doc**: https://open.imou.com/document/pages/ikdf78/
- **URL**: `POST {base_url}/openapi/addAiDetectTarget`

**params**: token, repositoryId, targetName, type ("0" URL or "1" Base64), content (URL or Base64). Optional fields per doc.

**Response data**: targetKey (String), the target unique ID to use for list/delete.

---

## 17. listAiDetectTarget – List targets in repository

- **Doc**: https://open.imou.com/document/pages/278dkj/
- **URL**: `POST {base_url}/openapi/listAiDetectTarget`

**params**: token, repositoryId. (Optional pagination: page, pageSize if supported by API.)

**Response data**: repositoryName, targetList (each item: targetKey, url).

---

## 18. deleteAiDetectTarget – Delete target from repository

- **Doc**: https://open.imou.com/document/pages/odty82/
- **URL**: `POST {base_url}/openapi/deleteAiDetectTarget`

**params**: token, repositoryId, targetId (use targetKey value from add/list).

**Response**: result.code "0".

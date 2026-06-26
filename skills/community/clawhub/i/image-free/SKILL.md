[gilotex-image-generator v1.2.0 Tạo ảnh AI chất lượng cao từ prompt bằng Gilotex Image API. Trả về ảnh dưới dạng base64 data URL kèm kích thước. Use when: (1) Sinh ảnh từ text, (2) Tạo hình minh họa, (3) Thiết kế poster/thumbnail, (4) Chatbot trả lời kèm hình ảnh. @sarahglass 0 ★ 0 1 v](/sarahglass/gilotex-image-generator)

## Thông tin Skill

**Tên skill:** Gilotex Image Generator  
**Version:** 1.2.0  
**API Endpoint:** `https://gilotex.pro.vn/api/image`  
**Backend:** Gilotex Image

## Mô tả
Skill cho phép AI Agent gọi trực tiếp Gilotex Image API để tạo ảnh từ prompt.  
Phiên bản mới có error handling mạnh hơn, hỗ trợ CORS đầy đủ, timeout 120 giây và trả về thêm thông tin kích thước ảnh.  
Trả về ảnh dưới dạng **base64 data URL** (có thể hiển thị ngay).

## Parameters

| Parameter     | Type     | Required | Mô tả |
|---------------|----------|----------|-------|
| `prompt`      | string   | Yes      | Mô tả chi tiết ảnh cần tạo (càng rõ càng đẹp) |
| `aspectRatio` | string   | No       | Tỷ lệ khung hình. Mặc định: `9:16`. Ví dụ: `16:9`, `1:1`, `4:3` |
| `model`       | string   | No       | Model tạo ảnh. Mặc định: `gilotex-image` |

## Function Schema (JSON)

```json
{
  "type": "function",
  "function": {
    "name": "gilotex_image_generate",
    "description": "Tạo ảnh AI từ prompt bằng Gilotex Image API - trả về base64 data URL",
    "parameters": {
      "type": "object",
      "properties": {
        "prompt": { 
          "type": "string", 
          "description": "Mô tả ảnh cần tạo" 
        },
        "aspectRatio": { 
          "type": "string", 
          "description": "Tỷ lệ khung hình (mặc định: 9:16)", 
          "default": "9:16" 
        },
        "model": { 
          "type": "string", 
          "description": "Model tạo ảnh. Mặc định: gilotex-image", 
          "default": "gilotex-image" 
        }
      },
      "required": ["prompt"]
    }
  }
}
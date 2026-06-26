---
name: "professional-vn-aqi-node-engine"
version: "3.5.0"
description: "High-performance Node.js implementation for monitoring Vietnamese Air Quality Indexes. Features advanced error resilience, localized city mapping, and multi-parameter environmental data retrieval."
tags: ["aqi", "vietnam", "node-js", "pm25", "environmental-science", "real-time-data", "api-integration", "urban-health"]
homepage: "https://github.com/picoclaw-skill/aqi-hanoi"
user-invocable: true
disable-model-invocation: false
---

# 🇻🇳 Vietnam Professional AQI Engine (Node.js)

## 📘 Introduction & Purpose
Dự án này là một bước tiến hóa từ các script Shell/Binary truyền thống sang một hệ thống **Node.js Managed Skill**. Mục tiêu cốt lõi là cung cấp dữ liệu môi trường có độ trễ thấp, độ chính xác cao cho các AI Agent hoạt động tại khu vực Đông Nam Á, đặc biệt là Việt Nam. 

Trong bối cảnh các đô thị lớn như Hà Nội thường xuyên đối mặt với bụi mịn PM2.5 vượt ngưỡng, công cụ này không chỉ trả về số liệu mà còn cung cấp một lớp **Logic Interpretation** (Giải mã logic) để người dùng cuối có thể hiểu rõ mức độ nguy hiểm đối với sức khỏe.

## 🏗️ Technical Architecture & Workflow

### 1. Data Processing Sequence
Hệ thống vận hành dựa trên luồng xử lý khép kín:
1.  **Request Sanitization:** Kiểm tra tính hợp lệ của tham số `city`.
2.  **Mapping Layer:** Sử dụng Dictionary nội bộ để chuyển đổi "Sài Gòn", "HCMC" thành định dạng tương thích với trạm đo toàn cầu.
3.  **Upstream Connectivity:** Khởi tạo kết nối TLS 1.3 đến server WAQI.
4.  **JSON Schema Validation:** Đảm bảo dữ liệu trả về từ trạm đo không bị lỗi hoặc thiếu trường thông tin IAQI.

### 2. Logic Flow Diagram (Text-based)
`User Query -> Skill Controller -> City Resolver -> WAQI API -> JSON Parser -> Health Advisory -> Final Output`

## 🛠️ Implementation Guide

### Prerequisites
- **Node.js Runtime:** Version 18.x or 20.x (LTS recommended).
- **Network:** Outbound access to `https://api.waqi.info`.

### Invocation Syntax
```bash
# Thực thi trực tiếp qua môi trường ClawHub
node {baseDir}/aqi-hanoi.js "Hà Nội"
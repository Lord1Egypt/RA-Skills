# LangChain Python Skill - Trợ lý thông minh với Python backend

Skill này sử dụng thư viện LangChain (Python) để xử lý query thông minh, hỗ trợ memory dài hạn, RAG trên PDF, tool calling (search, calculator), và agent tự suy luận.

## Tính năng chính
- Backend: Python + LangChain (có thể dùng Gemini 2.0 Flash, DeepSeek-chat, hoặc Groq fallback).
- Memory: Nhớ ngữ cảnh chat trong session (ConversationBufferMemory hoặc Summary).
- RAG: Hỗ trợ upload PDF → hỏi đáp chính xác trên tài liệu.
- Tool calling: Tự gọi web search, tính toán, đọc file...
- Usage: langchain <query> hoặc langchain: <câu hỏi>

## Ví dụ sử dụng
- langchain: Blockchain là gì? Giải thích ngắn gọn.
- langchain: Tên tôi là gì? (sau khi giới thiệu trước đó).
- langchain: Tóm tắt tài liệu PDF vừa upload.
- langchain: Tính 15 * 23 + 7^2 là bao nhiêu?

## Yêu cầu
- venv đã cài: langchain, langchain-community, langchain-google-genai (nếu dùng Gemini).
- API key: Gemini/DeepSeek/Groq (set trong code nếu cần).

## Lưu ý
- Skill chạy trên Python, không phụ thuộc Node.js.
- Author: Tích hợp bởi S0nSun & Grok (dựa trên LangChain 2026).
- Có thể mở rộng: Thêm agent router, multi-tool, RAG folder.

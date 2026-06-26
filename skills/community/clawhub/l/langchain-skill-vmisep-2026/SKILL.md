# LangChain Python Skill - Trợ lý thông minh với memory và chain

Skill này sử dụng thư viện LangChain để tạo chain LLM với bộ nhớ conversation buffer, giúp bot nhớ ngữ cảnh từ các tin nhắn trước trong cùng session. Skill hỗ trợ trả lời bằng tiếng Việt, ngắn gọn, chính xác, và có thể mở rộng để thêm RAG (PDF/document), tool calling (search, calculator), hoặc agent tự quyết định.

## Tính năng chính
- Conversation memory: Nhớ lịch sử chat trong session (dùng ConversationBufferMemory).
- Prompt template tùy chỉnh: Có thể chỉnh sửa prompt để phù hợp với persona của bot.
- Backend LLM: DeepSeek-chat (hoặc Gemini nếu thay đổi key).
- Usage: langchain <query> hoặc langchain: <query>
- Ví dụ thực tế:
  langchain: Blockchain là gì?
  langchain: Tôi tên S0nSun


---
name: LangChain Test Skill của Sếp
slug: langchain-skill-vmisep-2026
description: Skill test LangChain tích hợp bởi S0nSun & Grok
version: 1.0.1
---



  langchain: Tên tôi là gì? (bot sẽ nhớ và trả lời chính xác)

## Hướng dẫn sử dụng nâng cao
- Để test memory: Chat nhiều câu liên tiếp với cùng từ khóa "langchain".
- Có thể mở rộng: Thêm RAG bằng Chroma vector store, tích hợp tool web search (Tavily), hoặc gọi API bên ngoài.
- Yêu cầu: Cần venv với langchain đã cài (pip install langchain langchain-community langchain-core).

## Lưu ý
- Skill chạy trên Python, dùng OpenAI wrapper để gọi DeepSeek API.
- Nếu muốn dùng Gemini: Chỉnh api_base và api_key trong langchain_skill.py.
- Author: Tích hợp bởi S0nSun & Grok (dựa trên LangChain docs 2026)# LangChain Test Skill
- Description: Skill test LangChain đơn giản để kiểm tra load
- Usage: langchain <query>
- Example: langchain: Xin chào

## Tối ưu chi phí mới nhất (2026)
- Router tự động: Query tiếng Việt/code → ưu tiên DeepSeek (rẻ hơn).
- Memory summary: Tự tóm tắt lịch sử chat để giảm input tokens.
- Prompt cache: Giảm lặp lại system prompt.
- Output giới hạn: Trả lời ngắn gọn dưới 200 từ.

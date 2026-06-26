from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import OpenAI
from langchain_core.runnables import RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_langchain_skill(query: str) -> str:
    # Router ưu tiên DeepSeek cho query tiếng Việt
    router_prompt = PromptTemplate(
        input_variables=["query"],
        template="""Phân loại query sau: Nếu là tiếng Việt hoặc code/reasoning → chọn 'deepseek'.
Nếu cần context dài, multimodal hoặc tiếng Anh → chọn 'gemini'.
Chỉ trả lời 'deepseek' hoặc 'gemini' (không giải thích).

Query: {query}"""
    )

    router_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    router_chain = LLMChain(llm=router_llm, prompt=router_prompt)
    selected_model = router_chain.run(query=query).strip().lower()

    # Chọn LLM dựa trên router
    if "deepseek" in selected_model:
        llm = OpenAI(
            openai_api_base="https://api.deepseek.com/v1",
            openai_api_key="sk-e7ec5...39506694",  # key DeepSeek của Sếp
            model_name="deepseek-chat",
            temperature=0.7,
            max_tokens=1500
        )
        model_name = "DeepSeek-chat"
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        model_name = "Gemini 1.5 Flash"

    # Memory summary (tóm tắt lịch sử chat để giảm tokens)
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=2000,  # tóm tắt khi vượt 2000 tokens
        memory_key="chat_history",
        return_messages=True
    )

    # Prompt chính (ngắn gọn, yêu cầu output ngắn)
    main_prompt = ChatPromptTemplate.from_messages([
        ("system", "Bạn là trợ lý thông minh của Sếp S0nSun. Trả lời bằng tiếng Việt, ngắn gọn dưới 200 từ, chính xác."),
        ("placeholder", "{chat_history}"),
        ("human", "{query}")
    ])

    # Chain với memory
    chain = LLMChain(llm=llm, prompt=main_prompt, memory=memory)

    # Prompt cache đơn giản (cache system prompt + lịch sử tóm tắt)
    # LangChain tự cache nội bộ nếu dùng cùng prompt + memory

    response = chain.run(query=query)

    return f"[{model_name}] {response}"

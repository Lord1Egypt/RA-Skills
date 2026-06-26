import warnings
warnings.filterwarnings("ignore")

from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from config import OLLAMA_BASE_URL, MODEL_NAME, LLM_CONFIG
from prompts import SYSTEM_PROMPTS


def build_chain(mode: str = "coding"):
    config = LLM_CONFIG.get(mode, LLM_CONFIG["chat"])
    llm = ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        **config
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPTS[mode]),
        ("human", "{query}")
    ])
    return prompt | llm


def ask(query: str, mode: str = "coding") -> str:
    chain = build_chain(mode)
    full_response = ""
    for chunk in chain.stream({"query": query}):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    print()
    return full_response


def interactive():
    """Simple interactive CLI loop."""
    print("=== LangChain phi4-mini CLI ===")
    print("Modes: coding | devops | chat | rag")
    print("Type 'exit' to quit\n")
    while True:
        mode = input("Mode (default=coding): ").strip() or "coding"
        if mode == "exit":
            break
        if mode not in LLM_CONFIG:
            print(f"Unknown mode. Choose from: {list(LLM_CONFIG.keys())}")
            continue
        query = input("Query: ").strip()
        if query == "exit":
            break
        print(f"\n[{mode.upper()}] Response:")
        ask(query, mode=mode)
        print()


if __name__ == "__main__":
    interactive()

"""
LangChain: Chat model with RAG
"""
import os
import bs4
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import chain

# ignore env load and llm call


# =========================
# Create Vector Store and Embeddings
# =========================
embeddings = ZhipuAIEmbeddings() # ignore params
vector_store = InMemoryVectorStore(embeddings)


# =========================
# Indexing - Load
# =========================
# Generate simple documents
simple_docs = [
    Document(
        page_content="My name is jack.",
        metadata={"source": "local"},
    ),
    Document(
        page_content="Yestoday I went to the park.",
        metadata={"source": "local"},
    ),
]

# Load local documents
loader = PyPDFLoader() # ignore the pdf file
local_docs = loader.load()

# Load web pages
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2021-07-11-diffusion-models/",),
    bs_kwargs={"parse_only": bs4_strainer},
)
web_docs = loader.load()

# Combine documents
docs_set = simple_docs + local_docs
# docs_set = simple_docs + local_docs + web_docs

# =========================
# Indexing - Split
# =========================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0,
    add_start_index=True
)
split_docs = text_splitter.split_documents(docs_set)


# =========================
# Retrieval and Generation
# =========================
ids = vector_store.add_documents(documents=split_docs)

@chain
def retriever(query):
    return vector_store.similarity_search(query, k=1)


if __name__ == "__main__":
    print("Total characters of all documents: ", sum([len(doc.page_content) for doc in docs_set]))
    res = retriever.batch(
        [
            "Whis is my name?",
            "What did I do yesterday?",
            "What are the five elemental crystals in Eldryn, and what risks do they pose if misused? ",
            "What's the difference between guided diffusion and classifier-free guidance?",
        ],
    )
    for doc in res:
        print(doc[0].page_content)
    

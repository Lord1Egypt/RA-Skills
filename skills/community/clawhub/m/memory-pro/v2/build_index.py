from sentence_transformers import SentenceTransformer
import faiss
import json
import pickle
import math
import os
from collections import Counter
from preprocess import preprocess_entries, CJK_RE
import re


def _tokenize(text: str):
    """
    CJK-aware tokenizer for BM25:
    - keep latin words/numbers as terms
    - keep each CJK char as term
    """
    text = (text or "").lower()
    latin = re.findall(r"[a-z0-9_]+", text)
    cjk = CJK_RE.findall(text)
    return latin + cjk


def _build_bm25_payload(texts):
    tokenized = [_tokenize(t) for t in texts]
    n_docs = len(tokenized)
    df = Counter()
    for doc in tokenized:
        for term in set(doc):
            df[term] += 1

    # standard BM25 idf
    idf = {
        term: math.log(1 + (n_docs - freq + 0.5) / (freq + 0.5))
        for term, freq in df.items()
    }
    avgdl = (sum(len(d) for d in tokenized) / n_docs) if n_docs else 0.0
    return {
        "tokenized_docs": tokenized,
        "idf": idf,
        "avgdl": avgdl,
        "k1": 1.5,
        "b": 0.75,
    }


def build_index(output_path=None):
    """
    構建 FAISS 索引並保存到指定路徑；同時輸出 metadata 及 BM25 語料。
    """
    if output_path is None:
        output_path = os.getenv("MEMORY_PRO_INDEX_PATH", "memory.index")

    bm25_path = os.getenv("MEMORY_PRO_BM25_PATH", "bm25_corpus.pkl")
    meta_path = os.getenv("MEMORY_PRO_META_PATH", "memory_meta.jsonl")
    sentences_path = os.getenv("MEMORY_PRO_SENTENCES_PATH", "sentences.txt")

    print("🔍 開始構建索引...")

    model = SentenceTransformer('all-MiniLM-L6-v2')
    entries = preprocess_entries()
    texts = [e["text"] for e in entries]
    if not texts:
        raise ValueError("No valid memory entries were found to index.")

    print(f"📊 找到 {len(texts)} 個有效句子")
    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    print(f"💾 保存向量索引到 {output_path}...")
    faiss.write_index(index, output_path)

    os.makedirs(os.path.dirname(sentences_path) or ".", exist_ok=True)
    with open(sentences_path, "w", encoding="utf-8") as f:
        f.write("\n".join(texts))

    os.makedirs(os.path.dirname(meta_path) or ".", exist_ok=True)
    print(f"💾 保存 metadata 到 {meta_path}...")
    with open(meta_path, "w", encoding="utf-8") as f:
        for i, e in enumerate(entries):
            row = {
                "id": i,
                "text": e.get("text", ""),
                "source_file": e.get("source_file", "unknown"),
                "source_type": e.get("source_type", "unknown"),
                "created_at": e.get("created_at"),
                "scope": e.get("scope", "global"),
                "importance": float(e.get("importance", 0.5)),
                "token_len": int(e.get("token_len", len(e.get("text", "").split()))),
                "tags": e.get("tags", []),
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"💾 保存 BM25 語料到 {bm25_path}...")
    bm25_payload = _build_bm25_payload(texts)
    os.makedirs(os.path.dirname(bm25_path) or ".", exist_ok=True)
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25_payload, f)

    print(f"✅ 索引構建完成！包含 {len(texts)} 個句子")
    return texts, index


if __name__ == "__main__":
    sentences, index = build_index()

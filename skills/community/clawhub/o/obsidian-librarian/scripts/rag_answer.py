#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from dataclasses import dataclass

from common import gemini_generate_text
from config import LibrarianSettings
from rag_search import SearchResult, search


RAG_SYSTEM_PROMPT = """You are a knowledgeable assistant that answers questions using the user's personal Obsidian vault as a knowledge base.

Rules:
- Answer ONLY based on the provided context chunks. Do not invent facts.
- Cite your sources using the format [source: filename] after each claim.
- If the context does not contain enough information to answer, say so clearly.
- Be concise and direct. Use bullet points for multi-part answers.
- Preserve technical accuracy from the source material."""


MAX_CONTEXT_CHARS = 30_000  # ~7500 tokens — safety cap to avoid huge prompts

RAG_USER_PROMPT = """Question: {question}

Context from vault (ranked by relevance):

{context}

Answer the question using ONLY the context above. Cite sources with [source: filename]."""


@dataclass
class RAGAnswer:
    answer: str
    sources: list[SearchResult]
    query: str


def ask(
    settings: LibrarianSettings,
    question: str,
    *,
    category_filter: str | None = None,
    threshold: float = 0.65,
    limit: int = 5,
) -> RAGAnswer:
    results = search(
        settings,
        question,
        category_filter=category_filter,
        threshold=threshold,
        limit=limit,
    )

    if not results:
        return RAGAnswer(
            answer="No relevant content found in your vault for this question.",
            sources=[],
            query=question,
        )

    context_blocks: list[str] = []
    total_chars = 0
    for i, result in enumerate(results, 1):
        title = result.metadata.get("title", result.file_path)
        block = (
            f"--- Chunk {i} (from: {result.file_path}, similarity: {result.similarity:.3f}) ---\n"
            f"Title: {title}\n"
            f"{result.content}"
        )
        if total_chars + len(block) > MAX_CONTEXT_CHARS:
            break
        context_blocks.append(block)
        total_chars += len(block)

    context = "\n\n".join(context_blocks)
    prompt = RAG_USER_PROMPT.format(question=question, context=context)

    answer_text = gemini_generate_text(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
        prompt=prompt,
        system_instruction=RAG_SYSTEM_PROMPT,
        temperature=0.3,
        retries=2,
    )

    return RAGAnswer(answer=answer_text.strip(), sources=results, query=question)


def format_answer(rag_answer: RAGAnswer) -> str:
    lines: list[str] = [rag_answer.answer, ""]

    if rag_answer.sources:
        lines.append("---")
        lines.append("Sources:")
        seen: set[str] = set()
        for src in rag_answer.sources:
            if src.file_path not in seen:
                seen.add(src.file_path)
                title = src.metadata.get("title", src.file_path)
                lines.append(f"  - {title} ({src.file_path}) [similarity: {src.similarity:.3f}]")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rag_answer.py 'your question here'", file=sys.stderr)
        sys.exit(1)

    settings = LibrarianSettings.from_env()
    question = " ".join(sys.argv[1:])
    result = ask(settings, question)
    print(format_answer(result))

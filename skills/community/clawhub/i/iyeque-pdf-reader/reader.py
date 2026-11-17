import argparse
import json
import sys
import pymupdf

MAX_PAGES = 500

def page_limit(value):
    if value is None:
        return MAX_PAGES
    value = int(value)
    if value < 1 or value > MAX_PAGES:
        raise ValueError(f"max_pages must be between 1 and {MAX_PAGES}")
    return value

def open_pdf(file_path):
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("file_path is required")
    return pymupdf.open(file_path)

def extract_text(file_path, max_pages=None):
    doc = open_pdf(file_path)
    try:
        limit = page_limit(max_pages)
        pages = min(len(doc), limit) if limit else len(doc)
        text = "\n".join(doc[i].get_text() for i in range(pages))
        return {"file_path": file_path, "pages_read": pages, "text": text}
    finally:
        doc.close()

def search_text(file_path, query, max_pages=None):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query is required")
    doc = open_pdf(file_path)
    try:
        limit = page_limit(max_pages)
        pages = min(len(doc), limit) if limit else len(doc)
        matches = []
        for index in range(pages):
            page = doc[index]
            hits = page.search_for(query)
            if hits:
                matches.append({"page": index + 1, "matches": len(hits), "text": page.get_text()[:2000]})
        return {"file_path": file_path, "query": query, "matches": matches}
    finally:
        doc.close()

def get_metadata(file_path):
    doc = open_pdf(file_path)
    try:
        return {"file_path": file_path, "page_count": len(doc), "metadata": doc.metadata}
    finally:
        doc.close()

def main():
    parser = argparse.ArgumentParser(description="Bounded PDF extraction and search")
    parser.add_argument("command", choices=["extract", "search", "metadata"])
    parser.add_argument("file_path")
    parser.add_argument("--max_pages", type=int)
    parser.add_argument("--query")
    args = parser.parse_args()
    try:
        if args.command == "extract": result = extract_text(args.file_path, args.max_pages)
        elif args.command == "search": result = search_text(args.file_path, args.query, args.max_pages)
        else: result = get_metadata(args.file_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

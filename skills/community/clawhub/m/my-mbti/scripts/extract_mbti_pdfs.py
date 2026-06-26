from pathlib import Path
from pypdf import PdfReader

src = Path(r"D:\SOFTWARE\AppData\Desktop\MBTI")
out = Path(r"C:\Users\fuetsui\.openclaw\workspace\skills\my-mbti\references")
out.mkdir(parents=True, exist_ok=True)

for pdf in src.rglob("*.pdf"):
    code = pdf.name.split(" - ")[0].strip()
    title = pdf.stem
    reader = PdfReader(str(pdf))
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = f"[Page {i} extract error: {e}]"
        text = text.strip()
        if text:
            parts.append(f"## Page {i}\n\n{text}")
    body = "\n\n".join(parts).strip()
    content = f"# {code}\n\nSource PDF: `{pdf}`\n\nOriginal title: {title}\n\n{body}\n"
    (out / f"{code}.md").write_text(content, encoding="utf-8")
    print(f"OK {code}")

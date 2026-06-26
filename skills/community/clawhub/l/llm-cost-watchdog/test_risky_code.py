# Test file with cost risks

def process_documents():
    while True:  # DANGEROUS: infinite loop
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=documents
        )
        documents.append(result)

def analyze_code():
    for file in files:
        response = openai.chat.completions.create(
            model="claude-sonnet",
            # Missing max_tokens!
            prompt=file.content
        )

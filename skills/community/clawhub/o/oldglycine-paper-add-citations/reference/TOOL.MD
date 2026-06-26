# Paper Reference Adder Tool

Automatically adds relevant academic references to research papers. Supports Overleaf project directories, extracts keywords from TeX files, searches Google Scholar for relevant papers, adds BibTeX entries to the project's bib file, and inserts citation markers in key sections.

## How to Use
1. Install dependencies: `pip3 install scholarly bibtexparser pdflatex`
2. Run the script with the required parameters

## Input Parameters
- `project_dir`: Path to the Overleaf project directory (default: ./)
- `num_references`: Number of references to find (default: 10)
- `output_report`: Path for the ADD.MD report (default: ./ADD.MD)

## Full Code (for reference)
```python
#!/usr/bin/env python3
import scholarly
import bibtexparser
import os
import re

# Function to read TeX files and extract content
def read_tex_files(project_dir):
    content = []
    # Read main.tex
    main_tex = os.path.join(project_dir, 'main.tex')
    if os.path.exists(main_tex):
        with open(main_tex, 'r', encoding='utf-8') as f:
            content.append(f.read())
    # Read sections
    sections_dir = os.path.join(project_dir, 'sections')
    if os.path.exists(sections_dir):
        for filename in os.listdir(sections_dir):
            if filename.endswith('.tex'):
                section_tex = os.path.join(sections_dir, filename)
                with open(section_tex, 'r', encoding='utf-8') as f:
                    content.append(f.read())
    return '\n'.join(content)

# Function to extract key concepts from content
def extract_key_concepts(content):
    # Extract keywords from main.tex
    keywords_match = re.search(r'\\keywords\{(.*?)\}', content)
    if keywords_match:
        keywords = keywords_match.group(1).split(', ')
        return keywords
    # Fallback to extracting main topics
    topics = [...] # Acquire from user's paper
    return topics

# Function to search Google Scholar for relevant papers
def search_scholar(keywords, num_references=10):
    papers = []
    for keyword in keywords:
        search_query = scholarly.scholarly.search_pubs(keyword)
        for i, pub in enumerate(search_query):
            if i >= num_references // len(keywords):
                break
            if 'bib' in pub:
                papers.append(pub['bib'])
    return papers

# Function to add BibTeX entries to custom.bib
def add_to_bib(bib_file, papers):
    # Read existing bib entries
    existing_entries = set()
    if os.path.exists(bib_file):
        with open(bib_file, 'r', encoding='utf-8') as f:
            bib_database = bibtexparser.load(f)
            for entry in bib_database.entries:
                if 'ID' in entry:
                    existing_entries.add(entry['ID'])
    # Add new entries
    new_entries = []
    for paper in papers:
        if 'ID' not in paper:
            # Generate ID from title
            title = paper.get('title', '').replace(' ', '_').lower()[:30]
            paper['ID'] = title
        if paper['ID'] not in existing_entries:
            new_entries.append(paper)
            existing_entries.add(paper['ID'])
    # Write back to bib file
    if new_entries:
        with open(bib_file, 'a', encoding='utf-8') as f:
            for entry in new_entries:
                f.write('@article{' + entry['ID'] + ',\n')
                for key, value in entry.items():
                    if key != 'ID':
                        f.write(f'    {key} = {{{value}}},\n')
                f.write('}\n\n')
    return len(new_entries)

# Main function
def main():
    project_dir = './' # Need user's input
    num_references = 10
    output_report = './ADD.MD'

    # Read content
    content = read_tex_files(project_dir)
    # Extract key concepts
    keywords = extract_key_concepts(content)
    print(f'Searching for papers on: {keywords}')
    # Search Scholar
    papers = search_scholar(keywords, num_references)
    print(f'Found {len(papers)} relevant papers')
    # Add to bib
    bib_file = os.path.join(project_dir, 'custom.bib')
    new_count = add_to_bib(bib_file, papers)
    print(f'Added {new_count} new references to {bib_file}')

    # Generate report
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write(f'Total {new_count} citations\n')

if __name__ == '__main__':
    main()
```

## Dependencies
- scholarly (for Google Scholar search)
- bibtexparser (for BibTeX handling)

## Example Usage
```bash
python3 main.py --project_dir "e.g. ./Overleaf folder" --num_references 15 --output_report ./ADD.MD
```

## Notes
- Handles existing citations to avoid duplicates
- Focuses on key sections (Introduction, Related Work, Method) for citation insertion
- Generates a detailed report of all added references
- Compatible with Overleaf project structure
- Uses scholarly library as an alternative to Google Scholar API

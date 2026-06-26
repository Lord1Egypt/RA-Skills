# oldglycine-paper-reference-adder工具

自动为研究论文添加相关学术引用。支持Overleaf项目目录，从TeX文件提取关键词，在Google Scholar搜索相关论文，将BibTeX条目添加到项目的bib文件，并在关键部分插入引用标记。

## 如何使用
1. 安装依赖：`pip3 install scholarly bibtexparser pdflatex`
2. 根据用户论文的解构，以及论文的内容，调整代码读取逻辑以及关键领域的提取逻辑，调整关键词等。
3. 使用所需参数运行脚本

## 输入参数
- `project_dir`：Overleaf项目目录路径（默认：./）
- `num_references`：要查找的引用数量（默认：10）
- `output_report`：ADD.MD报告的路径（默认：./ADD.MD）

### 索引
1. [read_tex_files](#read_tex_files)
2. [extract_key_concepts](#extract_key_concepts)
3. [search_scholar](#search_scholar)
4. [add_to_bib](#add_to_bib)
5. [main](#main)

## 代码

```python
#!/usr/bin/env python3
import scholarly
import bibtexparser
import os
import re
```

### read_tex_files
```python
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
```

### extract_key_concepts
```python
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
```

### search_scholar
```python
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
```

### add_to_bib
```python
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
```

### main
```python
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

## 依赖项
- scholarly（用于Google Scholar搜索）
- bibtexparser（用于BibTeX处理）

## 示例用法
```bash
python3 main.py --project_dir "e.g. ./Overleaf folder" --num_references 15 --output_report ./ADD.MD
```

## 注意事项
- 处理现有引用以避免重复
- 重点在关键部分（引言、相关工作、方法）插入引用
- 生成所有添加引用的详细报告
- 兼容Overleaf项目结构
- 使用scholarly库作为Google Scholar API的替代方案

# -*- coding: utf-8 -*-
from lit_review import LiteratureReviewer

reviewer = LiteratureReviewer({'max_papers': 5, 'default_years': 3})
params = reviewer.parse_request('深度学习 图像识别')
papers = reviewer.search_semantic_scholar('deep learning image recognition', 3, 5)
print(f'检索到 {len(papers)} 篇文献')
if papers:
    print(f'第一篇: {papers[0]["title"]}')
    print(f'作者: {papers[0]["authors"]}')
    print(f'年份: {papers[0]["year"]}')

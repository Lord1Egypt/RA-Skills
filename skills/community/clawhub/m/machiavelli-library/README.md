# 马基雅维利图书馆 (Machiavelli Library)

A bilingual (Chinese-English) searchable library of Machiavelli's original texts — including his major works, letters, diplomatic papers, biographies, and scholarly studies.

## 中英双语 | Bilingual

中英文原文并列存储。查询时同时返回中英结果。

## 收录内容 | Catalog

### 马基雅维利著作 | Works by Machiavelli

| Work | 中文 | English | Format |
|------|------|---------|--------|
| The Prince | 君主论 | ✓ | 26 chapters |
| Discourses on Livy | 论李维 | ✓ | 3 books × 142 chapters |
| Florentine Histories | 佛罗伦萨史 | ✓ | 8 volumes |
| The Art of War | 兵法 | ✓ (EN only) | 7 books |
| Letters (upper) | 书信集 上 | — | by year |
| Letters (lower) | 书信集 下 | — | by year |
| Diplomatic Works (upper) | 政务与外交著作 上 | — | by work |
| Diplomatic Works (lower) | 政务与外交著作 下 | — | by work |

### 传记与研究 | Biographies & Studies

| Title | Author | Language | Format |
|-------|--------|----------|--------|
| 我的朋友马基雅维利 | 盐野七生 | 中文 | 20 chapters |
| Machiavelli: His Life and Times | Alexander Lee | 中文 | 7 parts |
| 马基雅维利语录 | 盐野七生 | 中文 | 3 sections |
| Reading Machiavelli | John McCormick | 中文 | by chapter |
| Then and Now | W. Somerset Maugham | 中文 | by chapter |

## 目录结构 | Structure

```
machiavelli-library/
├── SKILL.md                    ← Skill definition
├── README.md                   ← This file
├── library/                    ← Core text library
│   ├── machiavelli/           ← Works by Machiavelli
│   │   ├── prince/            ← 君主论 (中英)
│   │   ├── discourses/        ← 论李维 (中英)
│   │   ├── florentine/        ← 佛罗伦萨史 (中英)
│   │   ├── art-of-war/        ← 兵法
│   │   ├── letters/           ← 书信集
│   │   └── diplomatic/        ← 政务与外交
│   ├── biography/             ← 传记
│   ├── scholarship/           ← 研究
│   └── fiction/               ← 小说
├── index/                      ← 检索索引
│   ├── themes.md              ← 主题索引
│   ├── quotes.md              ← 名句索引
│   ├── people.md              ← 人物索引
│   ├── timeline.md           ← 年表索引
│   └── search-guide.md       ← 检索指南
├── catalog/                    ← 书目总索引
│   └── catalog.json
└── scripts/                    ← 构建与维护
    ├── split-prince.py
    ├── split-discourses.py
    ├── split-florentine.py
    ├── split-books.py
    ├── split-english.py
    └── IMPORT-GUIDE.md
```

## 检索 | How to Search

1. **Check pre-built indexes first** — `index/themes.md` contains topic-to-passage mappings
2. **Fallback to text search** — search across all files in `library/`
3. **Return** 3–5 most relevant verbatim passages with full citations

## 扩展 | Adding New Books

1. Place text file in appropriate `library/` subdirectory
2. Add entry to `catalog/catalog.json`
3. Run `python3 scripts/build-index.py` (or rebuild indexes manually)
4. No code changes needed

## 版权 | Copyright

All works by Niccolò Machiavelli (1469–1527) are in the public domain. English translations are sourced from Project Gutenberg. Chinese translations are from user-provided versions. Biographies and studies are included for research reference purposes only.
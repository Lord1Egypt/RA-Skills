# Candidate Profile Schema

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| name | string | Full name in English | "Michael Hu" |
| name_cn | string | Chinese name (if applicable) | "胡明" |
| title | string | Current position | "PhD Student" |
| affiliation | string | University/Company | "NYU Center for Data Science" |
| email | string | Contact email | "mh@nyu.edu" |

## Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| advisor | string | PhD advisor name |
| research_interests | list[string] | Research directions |
| homepage | string | Personal website URL |
| google_scholar | string | Google Scholar profile URL |
| github | string | GitHub profile URL |
| linkedin | string | LinkedIn profile URL |
| twitter | string | Twitter/X handle |

## Education & Experience

| Field | Type | Description |
|-------|------|-------------|
| education | list[object] | Education history |
| experience | list[object] | Work/internship experience |
| phd_year | int | PhD start year |
| expected_graduation | string | Expected graduation date |

### Education Object Schema

```json
{
  "degree": "PhD",
  "field": "Computer Science",
  "institution": "NYU",
  "year_start": 2021,
  "year_end": null,
  "honors": "NSF Fellowship"
}
```

### Experience Object Schema

```json
{
  "role": "Research Intern",
  "company": "Google DeepMind",
  "year": "2023",
  "description": "LLM pre-training research"
}
```

## Publications

| Field | Type | Description |
|-------|------|-------------|
| publications | list[object] | Selected publications |
| citation_count | int | Total Google Scholar citations |
| h_index | int | H-index |

### Publication Object Schema

```json
{
  "title": "Pre-pretraining Language Models",
  "venue": "ACL 2025",
  "year": 2025,
  "authors": ["Michael Hu", "..."],
  "award": "Outstanding Paper Award",
  "links": {
    "arxiv": "https://arxiv.org/abs/...",
    "github": "https://github.com/..."
  }
}
```

## Candidate Classification

| Type | Description | Typical Indicators |
|------|-------------|-------------------|
| PhD Student | Current doctoral student | "PhD student", "doctoral candidate" |
| PostDoc | Postdoctoral researcher | "Postdoc", "Research Fellow" |
| Professor | Faculty member | "Assistant/Associate/Full Professor" |
| Industry | Industry researcher | Company affiliation |
| Master | Master's student | "MS student", "Master's" |

## Output Format Examples

### Markdown Table Format

```markdown
| Field | Value |
|-------|-------|
| Name | Michael Hu |
| Title | PhD Student (Year 4) |
| Affiliation | NYU Center for Data Science |
| Advisor | Kyunghyun Cho, Tal Linzen |
| Research | LLM Pre-training, Data Mixing |
| Email | mh@nyu.edu |
| Homepage | https://michahu.github.io/ |
```

### JSON Format

```json
{
  "name": "Michael Hu",
  "title": "PhD Student",
  "affiliation": "NYU Center for Data Science",
  "advisor": ["Kyunghyun Cho", "Tal Linzen"],
  "research_interests": ["LLM Pre-training", "Data Mixing", "Training Dynamics"],
  "email": "mh@nyu.edu",
  "homepage": "https://michahu.github.io/",
  "google_scholar": "https://scholar.google.com/citations?user=TyyftvAAAAAJ",
  "github": "https://github.com/michahu",
  "publications": [
    {
      "title": "Pre-pretraining Language Models",
      "venue": "ACL 2025",
      "award": "Outstanding Paper Award"
    }
  ]
}
```

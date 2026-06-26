# LaTeX Resume Patterns

Common edit patterns for tailoring LaTeX resumes.

## Reorder Experience Section

Move the most relevant job to the top by cutting and pasting the entire `\entry` block.

```latex
% BEFORE (irrelevant job first)
\section{Experience}
\entry{Irrelevant Company}{Irrelevant Role}{2020--2022}{Description...}
\entry{Relevant Company}{Relevant Role}{2022--Present}{Description...}

% AFTER (relevant job first)
\section{Experience}
\entry{Relevant Company}{Relevant Role}{2022--Present}{Description...}
\entry{Irrelevant Company}{Irrelevant Role}{2020--2022}{Description...}
```

## Rewrite Bullet Points to Mirror JD Language

```latex
% BEFORE (generic)
\item Built backend services for data processing
\item Improved system performance

% AFTER (mirroring JD keywords like "distributed systems", "real-time", "Kafka")
\item Designed and deployed distributed data processing services handling 50K+ events/sec using Kafka
\item Reduced system latency by 40% through real-time optimization of data pipelines
```

## Remove Irrelevant Sections

Comment out sections that don't match the role:

```latex
% \section{Teaching Experience}
% \entry{...}
```

## Add Keywords to Skills Section

```latex
% BEFORE
\skills{Python, Docker, AWS, SQL, Git}

% AFTER (mirroring JD: "Kubernetes, Terraform, CI/CD")
\skills{Python, Docker, Kubernetes, AWS, Terraform, CI/CD, SQL, Git}
```

## Adjust Summary/Objective

```latex
% BEFORE (generic)
\summary{Experienced software engineer with a background in web development.}

% AFTER (targeted)
\summary{Backend engineer with 5+ years building distributed systems and real-time data pipelines. Experienced in Python, Kubernetes, and cloud infrastructure at scale.}
```

## Quantify Achievements

```latex
% BEFORE (vague)
\item Reduced API response times

% AFTER (quantified)
\item Reduced P95 API response times from 800ms to 120ms through caching and query optimization
```

## German Market Specifics

- **No photo** — remove any `\photo{}` command
- **No objective** — remove `\objective{}` or `\summary{}` if it reads like one
- **Include availability date** — add `\availability{Available from 01.07.2026}`
- **Include salary expectation** — if requested: `\salary{€75,000--€90,000}`
- **Date format** — DD.MM.YYYY (European)
- **Language** — English for international companies, German if specified
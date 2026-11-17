# Official sources and retrieval notes

Use these first-party sources as the skill's source map. Check their current pages when a question depends on current API behavior, access rules, or the latest archive contents.

## Nature Machine Intelligence

- [NMI article archive](https://www.nature.com/natmachintell/articles): canonical discovery page; supports archive filters for year and content type.
- [NMI Article archive view](https://www.nature.com/natmachintell/articles?type=article): archive view filtered to Article.
- [NMI content types](https://www.nature.com/natmachintell/content): publisher descriptions of Article, Analysis, Review, Perspective, and other formats.
- [NMI submission guidelines](https://www.nature.com/natmachintell/submission-guidelines): use only for questions about the journal's stated submission requirements.
- [Nature Portfolio journal metrics](https://www.nature.com/nature-portfolio/about-journals/journal-metrics): use for published journal metrics. Do not translate review-time measures into acceptance rates.

The archive is the authority for the NMI corpus in this skill. A search index or API may help find records, but inclusion and content type must be checked on the official NMI page.

## Springer Nature APIs

- [Springer Nature API overview](https://dev.springernature.com/)
- [Meta API v2 documentation](https://dev.springernature.com/docs/api-endpoints/meta-api/)
- [Supported query parameters](https://dev.springernature.com/docs/supported-query-params/)
- [API key authentication](https://dev.springernature.com/docs/quick-start/authentication/)
- [Rate-limit and throttling policies](https://dev.springernature.com/docs/rate-limit-details/throttling-policies/)
- [API subscription plans](https://dev.springernature.com/subscription/)
- [Open Access API](https://dev.springernature.com/docs/api-endpoints/open-access/)
- [Full Text API](https://dev.springernature.com/docs/api-endpoints/fulltext-api/)
- [Additional terms for Springer Nature API users](https://dev.springernature.com/terms-conditions/)

The Meta API is an optional metadata discovery route. Query constraints documented by Springer Nature include publication, year, DOI, and keyword. The exact available constraints and quotas depend on the current API plan. The Meta API is not a guarantee that every NMI archive item is indexed or returned by a given query.

Meta API v2 records can use fields such as publicationName, contentType, genre, publicationDate, onlineDate, coverDate, creators, and doi. These API fields help normalize metadata; the NMI article page remains the authority for the journal's displayed content type and dates.

Keep API use bounded and on demand. The helper script performs one request, requests only a limited result page, and prints bibliographic metadata without abstracts. Do not build a bulk mirror or retain full text based on the helper.

## Reading and reporting a paper

For every selected record:

1. Open the DOI or official Nature page and verify it belongs to Nature Machine Intelligence.
2. Record the article's displayed content type and publication date. If the distinction matters, preserve both online and issue dates.
3. Use the paper's abstract for discovery and a concise abstract-based summary only. Read the full text, methods, and supplements before making claims about implementation, experiments, or detailed results.
4. Use the DOI as a stable citation link. Cite the official article page for publisher metadata and article claims.
5. Report the access boundary: full text reviewed, abstract only, metadata only, or supplementary material unavailable.

## Relationships and trends

- An explicit reference in a paper is a citation relationship; verify it in that paper's reference list.
- A common task, method, or application is a thematic relationship; name the shared evidence and label it as such.
- For annual comparisons, define the publication-date convention and use the same archive type and screening rule across years.
- For counts, retain search terms, filters, exclusions, date searched, and candidate screening decisions in the answer or user-requested artifact. Do not call a keyword count a complete census without a coverage check.


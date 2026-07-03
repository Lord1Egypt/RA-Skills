# Data Sources

## Included venues

Core conferences: CVPR, ECCV, ICCV, ICLR, ICML, ACL, NeurIPS/NIPS and AAAI.

Core journals: IEEE TPAMI, IJCV, JMLR, Artificial Intelligence, JAIR, TACL, Computational Linguistics and IEEE/ACM TASLP.

Expanded journals: TMLR, IEEE TNNLS, Pattern Recognition, IEEE TIP and ACM TOIS.

The executable source definitions, ISSNs, venue IDs and official indexes are in `config/sources.yaml`.

## Publication priority

1. Official conference proceedings or journal landing page.
2. OpenReview, ACL Anthology, PMLR, CVF Open Access or the publisher API.
3. Crossref and OpenAlex for normalized metadata and identifiers.

Reject a record when it is retracted, lacks a publication date, or only has a repository/preprint location without official acceptance evidence.

Use DOI first for deduplication, then an official source ID, then a normalized title.

## Author evidence priority

1. ORCID or a public email printed on the paper.
2. University, laboratory, employer or personal professional page.
3. OpenAlex, DBLP and the official paper page.
4. A confirmed public Google Scholar author profile.
5. Baidu Scholar only for human-assisted corroboration.

Do not batch scrape Google Scholar or Baidu Scholar. A verified email domain is not a complete email address and must never be expanded or guessed.


## examples/platforms.md.example

```markdown
# platforms.md – List of job boards to scrape

Each platform must include:
- Name
- Search URL template (use {query} and {location} placeholders)
- Selector rules for job title, company, date, link (if needed by AI)

Example:

## Platform 1: Alwadifa Maroc
- url: "https://alwadifa-maroc.com/search?q={query}&location={location}"
- date filter: look for "publié le" or "il y a X jours"
- job card selector: ".job-item" (if using browser tools)

## Platform 2: Rekrute
- url: "https://rekrute.com/emploi/{query}/{location}"
- date filter: check for "Date de publication" within last 7 days

## Platform 3: Dreamjob.ma
- url: "https://dreamjob.ma/search?keywords={query}&city={location}"
- date filter: "Posté le" – parse DD/MM/YYYY

## Platform 4: Emploi Public
- url: "https://emploi-public.ma/offres"
- date filter: look for date in "Publiée le"

## Platform 5: Anapec
- url: "https://anapec.org/offres-d-emploi"
- date filter: use the "Date" column
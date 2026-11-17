---
name: indexnow
description: Submit changed public URLs through IndexNow, or set up the site's IndexNow verification file. Use when the user explicitly requests an IndexNow submission or verification setup for a site they manage.
allowed-tools: Bash(bash */scripts/indexnow.sh *)
metadata: {"openclaw":{"requires":{"bins":["bash","curl","python3"]}}}
---

# IndexNow

Notify participating search engines about added, updated, or deleted public URLs. Use the bundled `scripts/indexnow.sh` from the site's project directory. Replace `<skill-dir>` in the examples with the installed skill's path.

## Tool scope and data sent

Use the bundled script for the requested operation. Discussing indexing or troubleshooting a sitemap alone does not authorize a submission, key generation, or deployment.

Submitting sends the public URL list and the site's IndexNow verification key to the official endpoint at `https://api.indexnow.org/indexnow`. Batch requests also include the site hostname and verification-file URL. Participating search engines can share the submitted URLs. Use only public URLs on a site the user manages. Exclude drafts, staging and private URLs, and links containing credentials, personal data, or access tokens.

Generating a key writes `.indexnow-key` and a verification text file in the current project's `public/` directory, or in the current directory if `public/` is absent. Only run key setup or rotation when requested.

## Verify the site

```bash
bash "<skill-dir>/scripts/indexnow.sh" status
bash "<skill-dir>/scripts/indexnow.sh" generate-key
```

Serve the verification file at `https://www.example.com/{key}.txt` before submitting. Keep the same key for subsequent submissions. Key generation does not deploy the file.

## Submit URLs

```bash
bash "<skill-dir>/scripts/indexnow.sh" submit https://www.example.com/page
bash "<skill-dir>/scripts/indexnow.sh" submit-sitemap public/sitemap.xml
bash "<skill-dir>/scripts/indexnow.sh" submit-sitemap-url https://www.example.com/sitemap.xml
```

Pass multiple URLs to `submit` only if they share one hostname. `submit-sitemap` defaults to `public/sitemap.xml` and expects a sitemap containing page URLs. For a sitemap index, select the intended child sitemap explicitly.

For `submit-sitemap-url`, use the site's final public HTTPS sitemap URL on port 443. The script checks the resolved addresses, pins the connection to those addresses, rejects redirects, and submits only when every page URL matches the sitemap hostname. The sitemap host receives only a normal HTTPS download request. Review the submission scope before using a sitemap, since the command sends the listed page URLs to IndexNow.

## Interpret the response

| HTTP status | Meaning |
| --- | --- |
| 200 | IndexNow received the URLs. |
| 202 | IndexNow received the URLs and is verifying the key. |
| 400 | Check the request format. |
| 403 | Check the key and its publicly hosted verification file. |
| 422 | Check that the submitted URLs and key belong to the same site. |
| 429 | The endpoint is rate-limiting submissions. |

The script splits submissions into batches of up to 10,000 URLs. An accepted submission does not establish that a URL has been crawled or indexed.

[Official IndexNow documentation](https://www.indexnow.org/documentation)

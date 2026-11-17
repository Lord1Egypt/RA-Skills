# Other document software and import mode

For Google Docs, Microsoft Word/OneDrive, WPS, Yuque, Shimo or another requested service, first discover current writable host tools and inspect their schemas. Use `platform: generic`, `mode: host` only when actual document creation/import and readback are available; use `mode: import` for an explicitly accepted file preparation route. This is a general workflow, not a claim that the package has native API adapters or tested accounts for every product.

Export embedded DOCX plus Markdown. Prefer DOCX when the importer cannot transfer Markdown-relative images. A Markdown import needs its referenced asset directory; provide both, or use the host media uploader. Never publish a page with broken local file paths. Check conversion into an editable native document, full section text, figure/credit, Chinese text and all expansion links.

After actual import/connector success, obtain a real document ID and HTTPS URL and read back content, then record the host receipt. `awaiting_import` is not delivered. Some importers change formatting or omit images; correct the existing imported document with supported host tools instead of repeatedly creating copies.

Without access, report the available local DOCX/Markdown and specific login/import requirement. Do not imply that an exported file is already in the cloud or that interactive imports can run unattended.

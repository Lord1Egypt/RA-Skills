# API upload and link-management reference

Use the instance's /apidocumentation/openapi.json as the authoritative schema. API base path: /api/. Authentication: apikey HTTP header. Upload needs UPLOAD; metadata lookup needs VIEW; deletion needs DELETE.

Validate GOKAPI_BASE_URL as HTTPS without userinfo, query, or fragment; normalize a trailing slash. GOKAPI_BASE_URL must be an env-kind store SecretRef so the destination is readable at runtime. GOKAPI_API_KEY must remain a protected secret, inherited only by Gateway-host exec as an opaque sentinel. Do not copy it into literal commands, temporary files, logs, or native/sandbox shell. Do not follow redirects with the API key.

Ordinary upload: POST /api/files/add as multipart/form-data with file=@<absolute-path>, expiryDays=<chosen whole-day integer>, allowedDownloads=<chosen integer>. Command shape (set FILE_PATH with shell-safe quoting and numeric values; never paste secrets):

    curl --silent --show-error --fail --max-redirs 0 \
      --header "apikey: $GOKAPI_API_KEY" \
      --form "file=@$FILE_PATH" \
      --form "expiryDays=$EXPIRY_DAYS" \
      --form "allowedDownloads=$ALLOWED_DOWNLOADS" \
      "$GOKAPI_BASE_URL/api/files/add"

Parse JSON: Result must be OK; FileInfo.UrlDownload must be an HTTPS URL on the configured instance. Check FileInfo.ExpireAt minus UploadDate against expiryDays, and UnlimitedDownloads/DownloadsRemaining against allowedDownloads. Keep UrlDownload as the shared link; do not synthesize it from the file ID. The returned link may be a landing page rather than the file bytes. If verifying file integrity, follow the page's actual download action and compare hashes. Do not mistake a landing page or an HTML error redirect for the file.

For large files or a proxy request-size failure, inspect GET /api/info/config (UPLOAD permission) for MaxFilesize and MaxChunksize in MB. Stop if the total file exceeds MaxFilesize; otherwise use the documented chunk workflow:

1. Generate one UUID of at least 10 characters per file. Split the source into sequential chunks no larger than MaxChunksize; every non-final chunk must be at least 5 MB.
2. POST each chunk to /api/chunk/add as multipart/form-data: file=<chunk bytes>, uuid=<same UUID>, filesize=<total bytes>, offset=<byte offset>. Require Result=OK for each response before continuing. Preserve the source; obey local temporary-storage policy if staging is needed.
3. POST /api/chunk/complete with headers uuid, filename (for non-ANSI names, base64: followed by Base64 of the UTF-8 filename), filesize, expiryDays, allowedDownloads, and optional contenttype. Require Result=OK and verify the returned FileInfo.
4. After an ambiguous chunk or completion response, do not restart blindly: check server state or report uncertainty. Reusing a UUID for a fresh attempt may duplicate or corrupt an upload.

The API defaults to 14 days and one download when those fields are omitted; always supply the chosen values. A positive allowedDownloads value disables access after that many actual file downloads, not landing-page views. A public /downloadFile path can respond HTTP 200 with an HTML error redirect after expiry or deletion; verify metadata via GET /api/files/list/{id} (404) when VIEW permission is available.

For explicit immediate revocation, DELETE /api/files/delete with headers apikey and id; expect HTTP 200 and then 404 from /api/files/list/{id}. The optional delay header defers deletion for that many seconds, permitting POST /api/files/restore within the delay; use only when requested. The ID header is not a query parameter.

Other documented options, not part of routine sharing: PUT /api/files/modify can change remaining allowedDownloads, expiryTimestamp (UTC Unix time), and password with EDIT permission. The upload password field can protect a file, but never put a plaintext password in a logged command or send the password beside the link. Guest upload requests use separate /api/uploadrequest endpoints and GUEST_UPLOAD permission. Add these workflows only when the owner requests them.

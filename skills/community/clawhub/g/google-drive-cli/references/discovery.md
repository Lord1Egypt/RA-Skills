# Dynamic API Discovery

If the standard subcommands do not cover the user's request (e.g., updating file permissions, managing comments directly, interacting with a completely different Google API like Calendar or Gmail), you can use the `drivectl call` subcommand.

This subcommand uses Google's API Discovery service to dynamically build and execute HTTP requests against almost any Google Workspace API endpoint.

## Syntax

```bash
drivectl call <api>.<version>.<resource>.<method> --payload '<json-string>' -O json
```

### Components

1.  **Method Signature:** The command takes a dot-separated string representing the API, version, resource(s), and method.
    *   Examples:
        *   `drive.v3.files.get`
        *   `docs.v1.documents.create`
        *   `drive.v3.permissions.create`
2.  **`--payload`**: This flag accepts a JSON string. This JSON object serves a dual purpose:
    *   It populates **URL path parameters** (e.g., `fileId`, `documentId`).
    *   It populates **URL query parameters** (e.g., `fields`, `pageSize`).
    *   It populates the **Request Body** for methods like `POST`, `PUT`, or `PATCH`.
    *   *Note: `drivectl` automatically maps the keys in your JSON payload to the correct locations (path, query, or body) based on the Discovery schema.*
3.  **`-O json`**: As always, append this to ensure the output is structured JSON.

## Examples

**Example 1: Fetching specific fields for a known file (Drive)**
```bash
drivectl call drive.v3.files.get --payload '{"fileId": "YOUR_FILE_ID", "fields": "name,mimeType,owners"}' -O json
```
*Here, `fileId` is mapped to the URL path, and `fields` is mapped to the query string.*

**Example 2: Creating a new Google Doc (Docs)**
```bash
drivectl call docs.v1.documents.create --payload '{"title": "My New Document"}' -O json
```
*Here, the JSON is mapped to the request body as the document representation.*

**Example 3: Adding a reader permission to a file (Drive)**
```bash
drivectl call drive.v3.permissions.create --payload '{"fileId": "YOUR_FILE_ID", "role": "reader", "type": "user", "emailAddress": "user@example.com"}' -O json
```
*Here, `fileId` goes to the URL path, and `role`, `type`, and `emailAddress` go into the request body.*

## Finding the Right Method and Parameters

If you do not know the exact method signature or required parameters, you can:
1. Search the web or refer to standard Google API REST documentation (e.g., "Google Drive API REST reference"). The method signature maps directly to the REST resource structure (e.g., `drive.v3.files.update`).
2. Make an educated guess using the pattern: `<api>.<version>.<resource>.<action>`.
3. Consult the raw API Discovery documents. For example, the Drive v3 discovery document is located at: `https://www.googleapis.com/discovery/v1/apis/drive/v3/rest`
# AP-15: Inspection de `lynx-mcp-server` (Go)

**Source:** `dodmcdund-cc/lynx-travel-agent/lynx-mcp-server/`
**Date:** 2026-05-29

---

## 1. Architecture générale

```
lynx-mcp-server/
├── cmd/
│   ├── lynxmcpserver.go    # MCP server SSE (tag: server)
│   └── lynxmcpclient.go    # Client CLI de test (tag: client)
├── pkg/
│   ├── config/
│   │   ├── lynx.go          # Config Lynx (RemoteHost, credentials, cookie duration)
│   │   ├── mcp_server.go    # Config MCP server (port, bearer token)
│   │   └── client.go        # Config client (bearer token)
│   ├── gwt/                  # GWT-RPC protocol (body building + parsing)
│   │   ├── login.go          # BuildGWTLoginBody
│   │   ├── file_search.go    # BuildFileSearchByPartyName/FileReference + parse
│   │   ├── file_documents.go # Build document-related bodies + parse
│   │   ├── retrieve_itinerary.go # BuildRetrieveItinerary + parse
│   │   ├── types.go          # Constantes GWT
│   │   └── parse.go          # parseur/unescapeur GWT générique
│   ├── tools/                # Implémentations des 8 tools MCP
│   ├── rest/                 # REST endpoint additionnel (attachmentUpload)
│   └── utils/                # Auth, retry, debug, JSON formatting
├── assets/                   # Fichier dummy.pdf pour test
├── Makefile
├── Dockerfile
├── go.mod / go.sum
└── README.md
```

---

## 2. Les 8 outils MCP

### 2.1 `file_search_by_party_name`

| Champ                | Valeur                                                                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Nom MCP**          | `file_search_by_party_name`                                                                                                              |
| **Description**      | Retrieve file from party name                                                                                                            |
| **Paramètres**       | `partyName` (string, **required**)                                                                                                       |
| **Endpoint**         | `POST /lynx/service/file.rpc`                                                                                                            |
| **Méthode GWT**      | `FileService.search(FileSearchCriteria)`                                                                                                 |
| **Réponse**          | `{ count: int, results: Array<FileSearchResult> }`                                                                                       |
| **FileSearchResult** | `companyCode`, `clientIdentifier`, `clientReference`, `currency`, `fileIdentifier`, `fileReference`, `partyName`, `status`, `travelDate` |

### 2.2 `file_search_by_file_reference`

| Champ           | Valeur                                      |
| --------------- | ------------------------------------------- |
| **Nom MCP**     | `file_search_by_file_reference`             |
| **Description** | Retrieve file from file reference           |
| **Paramètres**  | `fileReference` (string, **required**)      |
| **Endpoint**    | `POST /lynx/service/file.rpc`               |
| **Méthode GWT** | `FileService.search(FileSearchCriteria)`    |
| **Réponse**     | Même format que `file_search_by_party_name` |

### 2.3 `retrieve_itinerary`

| Champ                           | Valeur                                                                                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nom MCP**                     | `retrieve_itinerary`                                                                                                                                    |
| **Description**                 | Retrieve file itinerary                                                                                                                                 |
| **Paramètres**                  | `fileIdentifier` (string, **required**)                                                                                                                 |
| **Endpoint**                    | `POST /lynx/service/file.rpc`                                                                                                                           |
| **Méthode GWT**                 | `FileService.retrieveItinerary(Long)`                                                                                                                   |
| **Réponse**                     | `{ type, partyName, fileReference, fileIdentifier, clientIdentifier, agentReference, itineraryCount, itineraries: Array<ItineraryTransactionSummary> }` |
| **ItineraryTransactionSummary** | `voucherIdentifier`, `date`, `transactionIdentifier`, `supplier`, `status`, `confirmationNumber`, `location`                                            |

### 2.4 `retrieve_file_documents`

| Champ            | Valeur                                                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Nom MCP**      | `retrieve_file_documents`                                                                                                   |
| **Description**  | Retrieve file documents from transaction reference                                                                          |
| **Paramètres**   | `fileIdentifier` (string, **required**), `transactionIdentifier` (string, **required**)                                     |
| **Endpoint**     | `POST /lynx/service/file.rpc`                                                                                               |
| **Méthode GWT**  | `FileService.getFileDocumentsAsList(Long, String)`                                                                          |
| **Réponse**      | `{ count: int, results: Array<FileDocument> }`                                                                              |
| **FileDocument** | `fileIdentifier`, `transactionIdentifier`, `documentIdentifier`, `documentName`, `documentType`, `content`, `attachmentUrl` |

### 2.5 `attachment_upload`

| Champ                    | Valeur                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **Nom MCP**              | `attachment_upload`                                                                                           |
| **Description**          | Upload attachment for using with file document                                                                |
| **Paramètres**           | `binary` (string/base64, **required**), `identifer` (string, **required**), `fileName` (string, **required**) |
| **Endpoint**             | `POST /lynx/fileDocumentUpload`                                                                               |
| **Content-Type**         | `multipart/form-data`                                                                                         |
| **Champs form**          | `fileId` (= `identifer`), `file` (binary, decoded from base64)                                                |
| **Réponse**              | `{ "attachmentUrl": "/documents/file/..." }`                                                                  |
| **Format réponse brute** | `SUCCESS:/path/file.pdf:\n`                                                                                   |

### 2.6 `file_document_save`

| Champ           | Valeur                                                                                                                                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nom MCP**     | `file_document_save`                                                                                                                                                                                       |
| **Description** | Save file document details                                                                                                                                                                                 |
| **Paramètres**  | `fileIdentifier` (string, **required**), `name` (string, **required**), `content` (string, **required**), `type` (string, **required**), `attachmentUrl` (string, required in handler, optional in schema) |
| **Endpoint**    | `POST /lynx/service/file.rpc`                                                                                                                                                                              |
| **Méthode GWT** | `FileService.saveFileDocumentsDetails(DocumentDetails)`                                                                                                                                                    |
| **Réponse**     | `{}` (empty JSON)                                                                                                                                                                                          |

### 2.7 `transaction_document_save`

| Champ           | Valeur                                                                                                                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nom MCP**     | `transaction_document_save`                                                                                                                                                                                                     |
| **Description** | Save transaction document details                                                                                                                                                                                               |
| **Paramètres**  | `fileIdentifier` (string, **required**), `transactionIdentifier` (string, **required**), `name` (string, **required**), `content` (string, **required**), `type` (string, **required**), `attachmentUrl` (string, **optional**) |
| **Endpoint**    | `POST /lynx/service/file.rpc`                                                                                                                                                                                                   |
| **Méthode GWT** | `FileService.saveFileDocumentsDetails(DocumentDetails)`                                                                                                                                                                         |
| **Réponse**     | `{}` (empty JSON)                                                                                                                                                                                                               |

### 2.8 Outil supplémentaire (REST endpoint, pas MCP tool)

`/attachmentUpload` — POST endpoint REST qui fait la même chose que `attachment_upload` mais reçoit un fichier multipart direct (sans base64). Protégé par Bearer token.

---

## 3. Authentification

| Aspect              | Détail                                                             |
| ------------------- | ------------------------------------------------------------------ | --- | --- | --- | --------------- | ----- | --- | ----------- | -------- | -------- | ---- |
| **Type**            | GWT-RPC login + JSESSIONID cookie                                  |
| **Login endpoint**  | `POST https://www.lynx-reservations.com/lynx/service/security.rpc` |
| **Headers**         | `Content-Type: text/x-gwt-rpc; charset=utf-8`                      |
| **Body GWT**        | `7                                                                 | 0   | 9   | ... | SecurityService | login | ... | companyCode | username | password | ...` |
| **Variables d'env** | `LYNX_USERNAME`, `LYNX_PASSWORD`, `LYNX_COMPANY_CODE`              |
| **Réponse**         | Cookie `JSESSIONID` (valide 15 min)                                |
| **Cookie**          | Domaine `www.lynx-reservations.com`, path `/lynx`, HttpOnly        |
| **Refresh**         | Nouveau login si session expirée ou absente du context             |
| **MCP server auth** | Bearer token (`BEARER_TOKEN`) pour le SSE endpoint seulement       |

---

## 4. Détails des appels HTTP vers `lynx-reservations.com`

### Base URL: `https://www.lynx-reservations.com`

### Endpoint 1: Sécurité

```
POST /lynx/service/security.rpc
Content-Type: text/x-gwt-rpc; charset=utf-8

Body: 7|0|9|https://www.lynx-reservations.com/lynx/lynx/|4775EB021C85EC0B04470837F40FC64A|com.lynxtraveltech.common.gui.client.rpc.SecurityService|login|java.lang.String/2004016611|Z|{companyCode}|{username}|{password}|1|2|3|4|4|5|5|5|6|7|8|9|1|
```

### Endpoint 2: File RPC (utilisé par 6 tools)

```
POST /lynx/service/file.rpc
Content-Type: text/x-gwt-rpc; charset=utf-8
Cookie: JSESSIONID={sessionId}

Body: format GWT-RPC (varie selon la méthode)
```

**Méthodes GWT appelées :**

- `FileService.search` — file search (party name / file reference)
- `FileService.retrieveItinerary` — retrieve itinerary
- `FileService.getFileDocumentsAsList` — retrieve file documents
- `FileService.saveFileDocumentsDetails` — file document save / transaction document save

### Endpoint 3: Upload fichier

```
POST /lynx/fileDocumentUpload
Content-Type: multipart/form-data; boundary=...
Cookie: JSESSIONID={sessionId}

Form fields: fileId={identifier}, file@{filename}
Response: SUCCESS:/documents/file/{fileId}/d{timestamp}.pdf:
```

---

## 5. Patterns réutilisables

### 5.1 GWT-RPC

- Content-Type: `text/x-gwt-rpc; charset=utf-8`
- Body format: `{version}|...|{moduleUrl}|{strongName}|{serviceInterface}|{methodName}|{parameterTypes}|...`
- Responses start with `//OK` (success) or `//EX` (error)
- GWT strings are quoted, with type prefixes like `java.util.ArrayList`, `java.lang.String`, etc.
- Le GWT RPC utilise des index one-based dans le tableau de données

### 5.2 Session management

- `GetOrCreateSession()` vérifie si une session valide existe dans le context
- Session expire après 15 minutes
- Cookie `JSESSIONID` attaché à chaque requête

### 5.3 Retry logic

- `RetryHTTPRequest` : jusqu'à 5 tentatives
- Backoff : 0s, 5s, 10s, 30s, 30s
- Ne retry PAS les erreurs GWT (`//EX`)
- Utilisé par tous les appels sauf `attachment_upload`

### 5.4 GWT body builders (constantes RPC)

Tous les bodies GWT partagent :

- Version: `7`
- Module URL: `https://{remoteHost}/lynx/lynx/`
- Strong name: `3212D5544B1A47B413D9619497B9C8A4`
- Service interface: `com.lynxtraveltech.client.client.rpc.FileService`

### 5.5 GWT parsers

- Parsing GWT : parsing récursif des tableaux, gestion des strings quotées, nombres, tableaux imbriqués
- `unescapeGWTString` : nettoie les séquences d'échappement `\x27` → `'`, etc.

---

## 6. Résumé des dépendances

- `github.com/mark3labs/mcp-go v0.33.0` — framework MCP server
- Go 1.23.10
- Aucune dépendance HTTP externe (stdlib `net/http`)
- GWT-RPC fait maison (pas de lib externe)

---

## 7. Notes pour la migration en skill CLI stateless

- Chaque tool MCP → une commande CLI (même nom, mêmes paramètres)
- Pas de serveur SSE. Appels HTTP directs.
- Réutiliser les bodies GWT et parsing existants.
- `attachment_upload` doit utiliser une lecture de fichier local (pas de base64 en paramètre CLI — plutôt un `--file` path).
- Session management simplifié : login avant chaque commande ou avec cache de session.
- Config via variables d'environnement ou flags CLI.
- Un seul binaire Go.
- Format de sortie : JSON stdout.

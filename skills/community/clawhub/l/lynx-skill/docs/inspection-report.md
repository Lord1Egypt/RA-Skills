# Inspection Report: lynx-mcp-server (AP-15)

> **Date:** 2026-05-30
> **Repository:** dodmcdund-cc/lynx-travel-agent
> **Target:** `lynx-mcp-server/` (Go)
> **Objective:** Analyse complète pour migration en skill CLI stateless

---

## 1. Vue d'ensemble du projet `lynx-mcp-server/`

**Langage:** Go 1.23.10
**Module:** `dodmcdund.cc/lynx-travel-agent/lynxmcpserver`
**Dépendance principale:** `github.com/mark3labs/mcp-go v0.33.0` (framework MCP)
**Port:** 9600
**Transport:** SSE (Server-Sent Events) avec Bearer token auth

### Structure du projet

```
lynx-mcp-server/
├── cmd/
│   ├── lynxmcpserver.go    # Entrypoint serveur MCP (SSE)
│   └── lynxmcpclient.go    # Client CLI de test (build tag: client)
├── pkg/
│   ├── config/
│   │   ├── mcp_server.go   # Config serveur MCP (port, bearer token)
│   │   ├── lynx.go          # Config connexion Lynx (host, credentials)
│   │   └── client.go        # Config client (bearer token)
│   ├── gwt/
│   │   ├── types.go         # Constantes GWT (types Java)
│   │   ├── login.go         # Construction body GWT login
│   │   ├── parse.go         # Parseur GWT générique (tableau, erreurs)
│   │   ├── file_search.go   # Construction/parse GWT file search
│   │   ├── file_documents.go # Construction/parse GWT file documents
│   │   ├── retrieve_itinerary.go      # Construction/parse GWT itinerary
│   │   └── retrieve_itinerary_test.go # Tests unitaires itinerary
│   ├── rest/
│   │   └── attachment_upload.go # Endpoint REST attachment upload
│   ├── tools/
│   │   ├── common.go                   # Config partagée
│   │   ├── attachment_upload.go        # Tool MCP — upload fichier
│   │   ├── file_document_save.go       # Tool MCP — save doc (file)
│   │   ├── file_search_by_file_reference.go  # Tool MCP — search by ref
│   │   ├── file_search_by_party_name.go      # Tool MCP — search by name
│   │   ├── retrieve_file_documents.go  # Tool MCP — list docs
│   │   ├── retrieve_itinerary.go       # Tool MCP — get itinerary
│   │   └── transaction_document_save.go # Tool MCP — save doc (tx)
│   └── utils/
│       ├── auth.go         # Auth GWT, session, middleware Bearer
│       ├── retry.go        # Exponential backoff HTTP
│       ├── mcp.go          # Helper CallToolResult JSON
│       ├── json.go         # Formatage JSON pretty
│       └── debug.go        # Conversion requête → curl
```

---

## 2. MCP Tools identifiés

| # | Nom MCP Tool | Description | Handler |
|---|-------------|-------------|---------|
| 1 | `attachment_upload` | Upload pièce jointe (base64 → multipart) | `HandleAttachmentUpload` |
| 2 | `file_document_save` | Sauvegarde document au niveau fichier | `HandleFileDocumentSave` |
| 3 | `file_search_by_file_reference` | Recherche fichiers par référence | `HandleFileSearchByFileReference` |
| 4 | `file_search_by_party_name` | Recherche fichiers par nom de partie | `HandleFileSearchByPartyName` |
| 5 | `retrieve_file_documents` | Liste des documents d'une transaction | `HandleRetrieveFileDocuments` |
| 6 | `retrieve_itinerary` | Itinéraire complet d'un fichier | `HandleRetrieveItinerary` |
| 7 | `transaction_document_save` | Sauvegarde document au niveau transaction | `HandleTransactionDocumentSave` |

Note: `file_document_save` apparaît 2× dans la liste de la story (AP-1) mais n'existe qu'une seule fois dans le code. Il s'agit probablement d'une redite dans la description Jira.

---

## 3. Endpoints REST Lynx

### 3.1 Authentification

```
POST https://www.lynx-reservations.com/lynx/service/security.rpc
Content-Type: text/x-gwt-rpc; charset=utf-8
```

**Body GWT-RPC (format propriétaire):**
```
7|0|9|https://{host}/lynx/lynx/|4775EB021C85EC0B04470837F40FC64A|
com.lynxtraveltech.common.gui.client.rpc.SecurityService|login|
java.lang.String/2004016611|Z|{companyCode}|{username}|{password}|
1|2|3|4|4|5|5|5|6|7|8|9|0|
```

**Réponse succès:** `//OK[...]` + Cookie `JSESSIONID`
**Réponse erreur:** `//EX[...]`

**Variables d'environnement requises:**
- `LYNX_USERNAME`
- `LYNX_PASSWORD`
- `LYNX_COMPANY_CODE`

**Session:** Cookie `JSESSIONID`, durée de vie 15 minutes, renouvelée automatiquement.

### 3.2 API GWT-RPC (`/lynx/service/file.rpc`)

Un seul endpoint pour 6 opérations différentes, différenciées par le body GWT.

#### 3.2.1 `fileSearchByPartyName` / `fileSearchByFileReference`

```
POST /lynx/service/file.rpc
Content-Type: text/x-gwt-rpc; charset=utf-8
Cookie: JSESSIONID=...
```

**Body (party name):**
```
7|0|9|https://{host}/lynx/lynx/|63A734E3E71C14883B20AFEC1238F6A7|
com.lynxtraveltech.client.client.rpc.FileService|search|
com.lynxtraveltech.client.shared.model.FileSearchCriteria/1867541444|
|{partyName}|PARTY_NAME|DD MMM YYYY|1|2|3|4|1|5|5|6|6|0|1|1|7|6|50|8|6|0|9|0|0|6|
```

**Body (file reference):**
```
7|0|9|https://{host}/lynx/lynx/|63A734E3E71C14883B20AFEC1238F6A7|
com.lynxtraveltech.client.client.rpc.FileService|search|
com.lynxtraveltech.client.shared.model.FileSearchCriteria/1867541444|
|{fileReference}|PARTY_NAME|DD MMM YYYY|1|2|3|4|1|5|5|6|7|0|1|1|6|6|50|8|6|0|9|0|0|6|
```

**Réponse parsée (JSON):**
```json
{
  "count": 2,
  "results": [
    {
      "companyCode": "XX",
      "clientIdentifier": "1234",
      "clientReference": "REF-001",
      "currency": "EUR",
      "fileIdentifier": "$xxxx",
      "fileReference": "FTXXXXXXXXX",
      "partyName": "Dupont",
      "status": "CONFIRMED",
      "traveDate": "01 MAY 2025"
    }
  ]
}
```

#### 3.2.2 `retrieveItinerary`

```
POST /lynx/service/file.rpc
```

**Body:**
```
7|0|6|https://{host}/lynx/lynx/|63A734E3E71C14883B20AFEC1238F6A7|
com.lynxtraveltech.client.client.rpc.FileService|retrieveItinerary|
J|Z|1|2|3|4|4|5|6|6|6|{fileIdentifier}|0|0|0|
```

**Réponse parsée (JSON):**
```json
{
  "type": "Partial",
  "partyName": "STIRFRY, Mrs / NOTA B, Lucy Mrs",
  "fileReference": "FTSWA230184",
  "fileIdentifier": "$xOpT",
  "clientIdentifier": "7LC",
  "agentReference": "1061848",
  "itineraryCount": 10,
  "itineraries": [
    {
      "voucherIdentifier": "16454569-4",
      "date": "04/05 Oct 2025",
      "transactionIdentifier": "BgBFw",
      "supplier": "CROWNE PLAZA ALICE SPRINGS LASSETERS",
      "status": "Confirmed",
      "confirmationNumber": "2194C574",
      "location": "ALICE SPRINGS, NT"
    }
  ]
}
```

#### 3.2.3 `getFileDocumentsAsList`

```
POST /lynx/service/file.rpc
```

**Body (by transaction reference):**
```
7|0|8|https://{host}/lynx/lynx/|63A734E3E71C14883B20AFEC1238F6A7|
com.lynxtraveltech.client.client.rpc.FileService|getFileDocumentsAsList|
J|java.lang.Long/4227064769|I|java.lang.String/2004016611|1|2|3|4|4|5|6|7|8|
{fileIdentifier}|6|{transactionIdentifier}|1|0|
```

**Réponse parsée (JSON):**
```json
{
  "count": 1,
  "results": [
    {
      "fileIdentifier": "f12345",
      "transactionIdentifier": "t67890",
      "documentIdentifier": "d001",
      "documentName": "Invoice",
      "documentType": "INVOICE",
      "content": "<p>Invoice content</p>",
      "attachmentUrl": "/documents/file/f12345/invoice.pdf"
    }
  ]
}
```

#### 3.2.4 `saveFileDocumentsDetails` (file level)

```
POST /lynx/service/file.rpc
```

**Body:**
```
7|0|9|https://{host}/lynx/lynx/|63A734E3E71C14883B20AFEC1238F6A7|
com.lynxtraveltech.client.client.rpc.FileService|saveFileDocumentsDetails|
com.lynxtraveltech.common.gui.shared.model.DocumentDetails/2779362264|
{content}|{type}|{name}|{attachmentUrl}|
1|2|3|4|1|5|5|0|1|A|0|0|0|P__________|6|7|0|{fileIdentifier}|8|9|0|
```

**Réponse:** `//OK[...]`

#### 3.2.5 `saveFileDocumentsDetails` (transaction level)

```
POST /lynx/service/file.rpc
```

**Body:**
```
7|0|10|https://{host}/lynx/lynx/|63A734E3E71C14883B20AFEC1238F6A7|
com.lynxtraveltech.client.client.rpc.FileService|saveFileDocumentsDetails|
com.lynxtraveltech.common.gui.shared.model.DocumentDetails/2779362264|
java.lang.Long/4227064769|{content}|{type}|{name}|{attachmentUrl}|
1|2|3|4|1|5|5|6|{transactionIdentifier}|1|A|0|0|0|P__________|
7|8|0|{fileIdentifier}|9|10|0|
```

**Réponse:** `//OK[...]`

### 3.3 Upload de fichier (multipart)

```
POST /lynx/fileDocumentUpload
Content-Type: multipart/form-data; boundary=...
Cookie: JSESSIONID=...
```

**Champs multipart:**
- `fileId` — Identifiant unique (string)
- `file` — Le fichier binaire

**Réponse succès:** `SUCCESS:/documents/file/{fileId}/d{timestamp}.pdf:\n`
→ Extraire `attachmentUrl` entre `SUCCESS:` et le dernier `:`

**Réponse erreur:** Code HTTP ≠ 200

---

## 4. Protocole GWT-RPC (format propriétaire)

### Caractéristiques

- **Content-Type:** `text/x-gwt-rpc; charset=utf-8`
- **Encodage:** Texte brut avec tokens numériques pour la sérialisation d'objets Java
- **Préfixe réponse succès:** `//OK`
- **Préfixe réponse erreur:** `//EX`
- **Version protocole:** 7

### Structure du body GWT

Format: `{version}|{flags}|{stringTableSize}|{baseUrl}|{strongName}|{serviceName}|{methodName}|{parameterTypes...}|{parameterValues...}|`

Le body se termine par `|` et contient des index numériques qui pointent vers une table de chaînes.

### Parsing des réponses

Un parseur GWT générique est présent dans `pkg/gwt/parse.go`:
- Parse les tableaux GWT `[item1,item2,...]`
- Gère les strings quotées (simples `'` et doubles `"`)
- Supporte les nombres (int, float)
- Gère les tableaux imbriqués
- Extrait les messages d'erreur depuis les réponses `//EX`

Les parseurs spécifiques extraient les données en naviguant dans l'index (one-based indexing) vers la `dataArray`.

---

## 5. Authentification & Sécurité

### Mécanisme

1. Le serveur MCP lui-même est protégé par **Bearer token** (env `BEARER_TOKEN`)
2. L'authentification Lynx est **stateless** (login GWT-RPC à chaque appel si session expirée)
3. Le JSESSIONID est stocké dans le **contexte Go** avec une durée de validité de **15 minutes**
4. Le cookie est attaché à chaque requête vers lynx-reservations.com

### Middleware

Un middleware `BearerAuthMiddleware` protège le endpoint `/attachmentUpload` côté MCP server.

### Retry logic

`RetryHTTPRequest` dans `pkg/utils/retry.go`:
- 5 tentatives max
- Backoff: 0s → 5s → 10s → 30s → 30s
- Conditions de succès: status 200 + body non-vide + préfixe `//OK`
- Les erreurs GWT (`//EX`) ne sont **pas** retryées

---

## 6. Correspondance Tools MCP → Commandes CLI (déjà implémenté)

Le fichier `lynx-skill/main.go` implémente déjà les 7 commandes suivantes avec `urfave/cli`:

| Commande CLI | Alias | Tool MCP correspondant |
|-------------|-------|----------------------|
| `file-search-by-party-name` | `fspn` | `file_search_by_party_name` |
| `file-search-by-file-reference` | `fsfr` | `file_search_by_file_reference` |
| `retrieve-itinerary` | `ri` | `retrieve_itinerary` |
| `retrieve-file-documents` | `rfd` | `retrieve_file_documents` |
| `file-document-save` | `fds` | `file_document_save` |
| `transaction-document-save` | `tds` | `transaction_document_save` |
| `attachment-upload` | `au` | `attachment_upload` |

### Paramètres CLI vs MCP

| MCP Tool | Arguments MCP | Flags CLI |
|----------|--------------|-----------|
| `file_search_by_party_name` | `partyName` | `--party-name` / `-p` |
| `file_search_by_file_reference` | `fileReference` | `--file-reference` / `-r` |
| `retrieve_itinerary` | `fileIdentifier` | `--file-identifier` / `-f` |
| `retrieve_file_documents` | `fileIdentifier`, `transactionIdentifier` | `--file-identifier` / `-f`, `--transaction-identifier` / `-t` |
| `file_document_save` | `fileIdentifier`, `name`, `content`, `type`, `attachmentUrl` | `--file-identifier` / `-f`, `--name` / `-n`, `--content` / `-c`, `--type` / `-t`, `--attachment-url` / `-a` |
| `transaction_document_save` | `fileIdentifier`, `transactionIdentifier`, `name`, `content`, `type`, `attachmentUrl` | `--file-identifier` / `-f`, `--transaction-identifier` / `-t`, `--name` / `-n`, `--content` / `-c`, `--type` / `-d`, `--attachment-url` / `-a` |
| `attachment_upload` | `binary` (base64), `identifer` (sic), `fileName` | `--binary` / `-b`, `--identifier` / `-i`, `--filename` / `-n` |

---

## 7. Notes d'implémentation pour la migration

### Fichiers déjà migrés dans `lynx-skill/`

- `main.go` — CLI complète avec urfave/cli (7 commandes)
- `client.go` — Client HTTP avec gestion session, GWT calls, upload
- `gwt.go` — Construction des bodies GWT-RPC (login, search, itinerary, documents, save)
- `gwt_parse.go` — Parsing des réponses GWT (array, file search, documents, itinerary)
- `config.go` — Configuration via variables d'environnement
- `SKILL.md` — Documentation complète du skill
- `README.md` — Documentation utilisateur

### Points d'attention

1. **Retry logic** — Le MCP server a un retry avec backoff; le skill actuel ne fait pas de retry. À migrer si nécessaire.
2. **Debug/curl** — Les utilitaires `RequestToCurl` et `DebugRequest` ne sont pas dans le skill. Utile pour debug.
3. **GWT parseur** — Déjà migré dans `gwt_parse.go` avec les mêmes fonctions que l'original.
4. **Typo `identifer`** — Le tool MCP original a une typo (`identifer` au lieu de `identifier`). Conservée dans le skill pour compatibilité.
5. **Typo `traveDate`** — Dans l'output du file search (`traveDate` au lieu de `travelDate`). Conservée.
6. **Attachment upload** — Le MCP server expose un endpoint REST `/attachmentUpload` en plus du tool MCP. Ce endpoint est un proxy qui reçoit un fichier multipart, le convertit en base64, puis l'envoie à Lynx. Le skill CLI prend directement le base64 en entrée, ce qui est plus cohérent avec le tool MCP.

### Gap analysis: lynx-mcp-server → lynx-skill

| Fonctionnalité | MCP Server | Skill CLI | Statut |
|---------------|------------|-----------|--------|
| 7 MCP tools | ✅ | ✅ | Migré |
| GWT body builders | ✅ | ✅ | Migré |
| GWT response parsers | ✅ | ✅ | Migré |
| Auth session (JSESSIONID) | ✅ | ✅ | Migré |
| Retry exponential backoff | ✅ | ❌ | **Manquant** |
| Debug curl utility | ✅ | ❌ | **Manquant** |
| Bearer auth middleware | ✅ | N/A | Pas nécessaire (CLI) |
| REST endpoint attachment proxy | ✅ | N/A | Pas nécessaire (CLI) |
| MCP SSE server | ✅ | N/A | Pas nécessaire (CLI) |
| Tests unitaires (itinerary) | ✅ | ❌ | **Manquant** |
| Document struct types | ✅ | ✅ | Migré |
| SKILL.md | ❌ | ✅ | Migré |
| README.md | ❌ | ✅ | Migré |

---

## 8. Architecture de la communication

```
┌─────────────────────────────────────────────────────┐
│                    lynx-mcp-server                    │
│  ┌──────────┐   ┌──────────────┐   ┌─────────────┐  │
│  │ MCP SSE  │──▶│ Tool handlers│──▶│ GWT builders│  │
│  │ :9600    │   │ (7 tools)    │   │ + parsers   │  │
│  └──────────┘   └──────────────┘   └──────┬──────┘  │
│         ▲                                  │         │
│         │ Bearer Token                     │ HTTP    │
│         │                                  │ + Cookie│
│  ┌──────┴───────┐                ┌─────────▼────────┐│
│  │ MCP Client   │                │ lynx-reservations ││
│  │ (test tool)  │                │ .com              ││
│  └──────────────┘                └──────────────────┘│
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                    lynx-skill (stateless CLI)         │
│  ┌──────────┐   ┌──────────────┐   ┌─────────────┐  │
│  │ urfave/cli│──▶│ LynxClient  │──▶│ GWT builders│  │
│  │ (7 cmds)  │   │ (HTTP calls)│   │ + parsers   │  │
│  └──────────┘   └──────┬───────┘   └──────┬──────┘  │
│                         │                  │         │
│                         │ HTTP + Cookie    │         │
│                         └──────────────────┼─────────│
│                                            │         │
│                                 ┌──────────▼────────┐│
│                                 │ lynx-reservations  ││
│                                 │ .com               ││
│                                 └───────────────────┘│
└─────────────────────────────────────────────────────┘
```

---

## 9. Recommandations

1. **Retry avec backoff** — Ajouter `RetryHTTPRequest` au client pour robustesse.
2. **Tests unitaires** — Migrer les tests de `retrieve_itinerary_test.go` vers le skill.
3. **Debug curl** — Ajouter un flag `--debug` optionnel pour afficher la requête curl.
4. **Gestion d'erreurs GWT** — Le parseur d'erreur existe déjà, bien l'intégrer dans les workflows CLI.
5. **Compatibilité descendante** — Les typos `identifer` et `traveDate` doivent être conservées pour compatibilité avec les workflows existants.
6. **Documentation** — Mettre à jour SKILL.md si de nouvelles fonctionnalités sont ajoutées.

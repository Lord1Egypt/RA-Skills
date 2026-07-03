# lynx-skill — Stateless CLI for Lynx Reservations

CLI stateless en Go pour interagir avec [lynx-reservations.com](https://www.lynx-reservations.com/). Remplace le serveur MCP `lynx-mcp-server/` sans nécessiter de processus serveur en arrière-plan.

Toutes les commandes effectuent des appels HTTP directs vers l'API Lynx via GWT-RPC.

## Table des matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Commandes](#commandes)
- [Exemples concrets](#exemples-concrets)
- [Développement](#développement)
- [Dépannage](#dépannage)
- [Référence](#référence)

---

## Installation

### Prérequis

- Go 1.23+
- Compte Lynx valide (credentials username/password/company code)

### From source

```bash
git clone https://github.com/dodmcdund-cc/lynx-travel-agent.git
cd lynx-travel-agent/lynx-skill
go build -o lynx .
```

### Vérification

```bash
./lynx --help
```

---

## Configuration

### Variables d'environnement

| Variable            | Requise | Description                           |
| ------------------- | ------- | ------------------------------------- |
| `LYNX_USERNAME`     | Oui     | Nom d'utilisateur Lynx                |
| `LYNX_PASSWORD`     | Oui     | Mot de passe Lynx                     |
| `LYNX_COMPANY_CODE` | Oui     | Code compagnie (ex: `XX`, `FR`, etc.) |

### Fichier `.env` (recommandé)

```bash
LYNX_USERNAME="mon-username"
LYNX_PASSWORD="mon-password"
LYNX_COMPANY_CODE="XX"
```

Puis chargez-le :

```bash
export $(grep -v '^#' .env | xargs)
```

Ou utilisez [direnv](https://direnv.net/) pour le chargement automatique.

### Authentication

La CLI utilise GWT-RPC (`/lynx/service/security.rpc`) pour s'authentifier. La session est maintenue via cookie `JSESSIONID` avec une durée de validité de 15 minutes. Les appels suivants réutilisent la session tant qu'elle est valide.

---

## Utilisation

```bash
lynx <commande> [flags]
```

### Aide intégrée

```bash
lynx --help          # Aide générale
lynx <commande> --help  # Aide d'une commande spécifique
```

### Alias

Chaque commande possède un alias court :

| Commande                        | Alias  |
| ------------------------------- | ------ |
| `file-search-by-party-name`     | `fspn` |
| `file-search-by-file-reference` | `fsfr` |
| `retrieve-itinerary`            | `ri`   |
| `retrieve-file-documents`       | `rfd`  |
| `file-document-save`            | `fds`  |
| `transaction-document-save`     | `tds`  |
| `attachment-upload`             | `au`   |

---

## Exemples concrets

### Recherche de fichiers par nom

```bash
# Par nom de partie
lynx fspn --party-name "Dupont"

# Avec alias court
lynx file-search-by-party-name -p "Martin"
```

### Recherche par référence fichier

```bash
lynx fsfr --file-reference "FT20250501"
```

### Récupération d'itinéraire

```bash
lynx ri --file-identifier "f12345"
```

### Consultation des documents

```bash
lynx rfd \
  --file-identifier "f12345" \
  --transaction-identifier "t67890"
```

### Upload d'une pièce jointe

```bash
# Depuis un fichier
lynx au \
  --binary "$(base64 -w0 document.pdf)" \
  --identifier "att-001" \
  --filename "document.pdf"

# Depuis stdin
cat document.pdf | base64 | lynx au \
  --identifier "att-002" \
  --filename "document.pdf"
```

### Sauvegarde d'un document fichier

```bash
lynx fds \
  --file-identifier "f12345" \
  --name "Facture client" \
  --content "<p>Contenu de la facture</p>" \
  --type "INVOICE"
```

Avec pièce jointe :

```bash
lynx fds \
  --file-identifier "f12345" \
  --name "Facture client" \
  --content "<p>Contenu de la facture</p>" \
  --type "INVOICE" \
  --attachment-url "/documents/file/f12345/d20250708231038.pdf"
```

### Sauvegarde d'un document transaction

```bash
lynx tds \
  --file-identifier "f12345" \
  --transaction-identifier "t67890" \
  --name "Voucher hôtel" \
  --content "<p>Voucher pour l'hôtel XYZ</p>" \
  --type "VOUCHER"
```

### Pipeline JSON (jq)

```bash
# Extraire les identifiants de fichier
lynx fspn --party-name "Dupont" | jq '.results[].fileIdentifier'

# Compter les résultats
lynx fspn --party-name "Dupont" | jq '.count'

# Formater un itinéraire
lynx ri --file-identifier "f12345" | jq -r '.itineraries[] | "\(.date) - \(.supplier) (\(.status))"'
```

---

## Développement

### Structure du projet

```
lynx-skill/
├── main.go          # CLI entrypoint (urfave/cli)
├── client.go        # Client HTTP Lynx (session, GWT, upload)
├── config.go        # Configuration depuis les variables d'environnement
├── gwt.go           # Construction des corps de requête GWT-RPC
├── gwt_parse.go     # Parseur de réponses GWT-RPC
├── go.mod           # Module Go
├── go.sum           # Dependencies checksums
├── SKILL.md         # Documentation du skill pour OpenClaw
└── README.md        # Documentation utilisateur (ce fichier)
```

### Build

```bash
go build -o lynx .
```

### Cross-compilation

```bash
GOOS=linux GOARCH=amd64 go build -o lynx-linux .
GOOS=darwin GOARCH=amd64 go build -o lynx-macos .
GOOS=windows GOARCH=amd64 go build -o lynx.exe .
```

### Tests

```bash
go vet ./...
go test ./...
```

---

## Dépannage

### "LYNX_USERNAME is not set"

Les variables d'environnement ne sont pas définies. Vérifiez :

```bash
echo $LYNX_USERNAME
echo $LYNX_PASSWORD
echo $LYNX_COMPANY_CODE
```

### "auth request failed with status: 403"

- Vérifiez que vos credentials sont corrects.
- Vérifiez que le `CompanyCode` est valide.

### "JSESSIONID not found in response cookies"

- Problème de connexion ou credentials invalides.
- Vérifiez votre accès à `https://www.lynx-reservations.com/lynx/service/security.rpc`.

### "GWT error: ..."

Erreur renvoyée par l'API Lynx. Le message contient généralement la raison (ex: fichier introuvable, paramètre invalide).

### "attachment upload failed with status 500"

- Vérifiez que le base64 est valide : `base64 -d <<< "$binary" > /dev/null` doit réussir.
- Vérifiez que l'identifiant est unique.
- La taille limite du fichier est d'environ 32 Mo.

### Session expirée

La CLI gère automatiquement le renouvellement de session (JSESSIONID valide 15 min). Si vous rencontrez des erreurs de session, assurez-vous que l'horloge système est synchronisée.

---

## Référence

- [Lynx Reservations](https://www.lynx-reservations.com/)
- [Serveur MCP lynx-mcp-server](../lynx-mcp-server/)

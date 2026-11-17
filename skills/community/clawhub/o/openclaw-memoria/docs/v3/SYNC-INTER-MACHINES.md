# Synchronisation inter-machines de Memoria — Spec d'exécution

> Statut : spec retenue, prête à implémenter. Ancrée dans le code réel de `memoria-v1`.
> Cible : Koda (Mac Studio), Luna (iMac), Claude Code (MacBook Pro), même LAN, NAS QNAP dispo.

Faits de code vérifiés (ancrage) :

- `facts` possède déjà `id` (UUID), `scope_id`, `updated_at`, `superseded`/`superseded_by`, `sensitivity`, `visibility ('private'|'shared')`, et les compteurs d'usage (`recall_count`, `used_count`, `usefulness`). → `content-schema.ts` L31-58.
- `secret_refs` = `id, name, service, location, scope_id, allowed_assistants, sensitivity, last_verified_at, created_at`. La valeur n'y est jamais. → `registry-schema.ts` L135-145.
- Gate dur : « la valeur d'un secret ne touche JAMAIS facts/.md/logs/audit/projection ». → `secrets/types.ts` L3.
- `aes-vault.ts` : `aes-256-gcm`, `IV_BYTES=12`, `KEY_BYTES=32`, `scryptSync`, écriture **tmp + rename** atomique chmod 600. → L18-22, L133-136, L154-155.
- Pairing one-shot existant : table `pairings (code_hash, status, expires_at)` + `completePairing(code)` + `ensureDaemon`. → `registry-schema.ts` L112, `mcp/connect.ts` L13/L51.
- Le daemon écoute **strictement loopback** : `server.listen(port, '127.0.0.1')` + `isLoopbackHost`/`isAllowedOrigin` anti-DNS-rebinding. Body capé. → `server.ts` L504, L89, L578.
- Migrations = tableau `Migration[]` versionné. **Registry est déjà en v3** → les tables de sync seront **v4**. **Content est en v1** → les colonnes de sync seront **v2**. → `registry-schema.ts` L10/158/172, `content-schema.ts` L22.
- `network-guard.isOnNetworkVolume` bloque `/Volumes/*` (macOS) et FS réseau → **SQLite sur NAS interdit**, on ne le contourne pas. → `network-guard.ts` L31-55.
- Aucune dépendance mDNS/Bonjour dans le repo → toute auto-découverte est du code net-neuf (coût).

---

## 1. Notation des 3 propositions

Notes /10, une phrase de justification par cellule.

| Critère | HUB (Mac Studio) | MESH pair-à-pair | RELAIS NAS (boîte aux lettres) |
|---|---|---|---|
| **Sécurité coffre inter-machines** | **8** — `group_vault_key` en Keychain + enveloppes GCM, clé scellée dans le code TTL ; un seul détenteur canonique de l'état (surface réduite). | **7** — même crypto, mais `mesh_key` dupliquée sur N machines = N surfaces de vol ; canal `secret/fetch` direct daemon↔daemon ajoute une route LAN ouverte de plus. | **8** — CVK + CPK séparées (chiffrement ≠ authenticité), valeur jamais en clair sur le NAS, opt-in `syncable` pour les secrets `critical` ; le NAS au pire retient, jamais ne lit. |
| **Simplicité non-dev (install/connect/disconnect)** | **9** — 1 adresse hub + 1 code ; `sync join` calqué sur `connect.ts` ; pas de graphe à câbler. | **6** — auto-mesh sympa mais repose sur mDNS inexistant (à écrire) + pare-feu macOS à ouvrir sur chaque Mac ; N liens à diagnostiquer. | **8** — pointer un chemin déjà monté + coller 1 code ; zéro port, zéro IP, zéro découverte ; disconnect = retirer le dossier. |
| **Résilience offline** | **6** — spokes lisent leur copie locale hors-ligne (OK), mais toute **convergence** exige le hub allumé ; SPOF sur l'écriture partagée. | **9** — aucun nœud indispensable, deux pairs convergent sans le troisième ; le vrai local-first. | **8** — store-and-forward découplé : marche même si les machines ne sont JAMAIS up ensemble ; dépend d'un NAS allumé (raisonnable, il l'est). |
| **Fidélité contraintes (pas de SQLite réseau, local-first)** | **9** — `shared/*.sqlite` sur disque hub local ; NAS = juste `hub.json` (carnet d'adresses). | **9** — rien sur le NAS sauf bundle de bootstrap chiffré optionnel ; SQLite 100% local. | **8** — respecte la lettre (fichiers `.mbx`/`.snap` opaques, pas de WAL) mais met le NAS dans le chemin nominal, plus près de la ligne rouge. |
| **Effort d'implémentation** | **8** — 1 listener LAN ciblé, watermark simple, LWW, 1 enveloppe ; le moins de pièces mobiles. | **5** — vecteurs de versions Lamport + nonce-cache + mDNS + N liens + résolution mesh testée en propriété = le plus gros chantier. | **6** — pas de réseau daemon↔daemon (gain), mais I/O NAS atomique + compaction + heartbeat + gap-detection + 3e provider secret = surface moyenne. |

**Lecture** : HUB gagne simplicité + effort + contraintes mais perd sur offline (SPOF). MESH gagne offline mais coûte cher et complique le non-dev. RELAIS gagne le découplage temporel (machines jamais up ensemble) mais rapproche du NAS-dans-le-chemin.

---

## 2. Architecture retenue — HUB-and-spoke avec relais NAS de secours (hybride)

**Topologie nominale = hub-and-spoke** (hub = Koda/Mac Studio, toujours allumé). C'est le meilleur compromis simplicité non-dev + effort + cohérence (écritures partagées sérialisées en un point, conflits résolus une fois). **On greffe deux idées des perdants** pour couvrir sa faiblesse (SPOF/offline) : (a) **chaque spoke garde une copie locale complète** des scopes partagés (du mesh) → l'historique n'est jamais sur la seule machine hub et chaque spoke marche hors-ligne ; (b) **relais NAS optionnel** (du relais) comme boîte aux lettres chiffrée pour bootstrapper/rattraper **quand le hub dort**, et comme cible de backup à froid. Le NAS ne porte jamais de SQLite — uniquement des `.mbx`/`.snap`/`hub.json` opaques. Pas de mesh, pas de multi-hub.

---

## 3. Design retenu définitif

### 3.0 Vocabulaire

- **hub** : le daemon canonique des scopes partagés (Koda). Détient `shared/*.sqlite` de référence + sert `/v1/sync/*` sur l'IP LAN.
- **spoke** : Luna, Claude Code. Gardent leur `memory.sqlite` privé + une **copie locale complète** des `shared/*.sqlite`. Tirent/poussent vers le hub.
- **GVK** (Group Vault Key) : clé AES-256 du groupe, chiffre les **valeurs** de secrets en transit. En Keychain local sur chaque machine.
- **CPK** (Cluster Pairing Key) : PSK 32 o, signe HMAC chaque requête de sync (authenticité + anti-MITM). En Keychain local.
- **machine_id** : identité stable persistée (≠ `daemonId` éphémère du boot).

### 3.1 Topologie & rôle du NAS

```
                 ┌──────────── LAN ────────────┐
   Luna (spoke) ─┤  pull/push  /v1/sync/*  HMAC ├─ Koda (HUB)
   Claude (spoke)┘   (copie locale shared/*)    └─ shared/*.sqlite canon (disque local)
                              │
                     QNAP (secours, opaque) :
                       hub.json  (carnet d'adresses)
                       bootstrap.mbx / snapshot.snap (chiffrés GVK+CPK)
                       backup à froid du hub (.sql dump)
```

Le hub n'expose **que** `/v1/sync/*` sur l'IP LAN. `/v1/admin/*` et `/v1/memory/*` **restent strictement loopback** (`isLoopbackHost` conservé pour eux). Anti-DNS-rebinding préservé.

### 3.2 Nouvelles tables / colonnes (SQL)

**Migration registry v4** (nouveau bloc `{ version: 4, ... }` dans `registry-schema.ts`) :

```sql
-- Pairs machine connus (côté hub : ses spokes ; côté spoke : son hub)
CREATE TABLE sync_peers (
  id              TEXT PRIMARY KEY,
  machine_id      TEXT NOT NULL UNIQUE,
  display_name    TEXT NOT NULL,                 -- "Luna (iMac)"
  role            TEXT NOT NULL CHECK (role IN ('hub','spoke')),
  host            TEXT,                           -- "192.168.1.20:47600" (le hub, côté spoke)
  peer_token_hash TEXT NOT NULL,                  -- hash du token long-terme (jamais en clair)
  cpk_location    TEXT NOT NULL,                  -- 'keychain:memoria/cpk-<machine_id>'
  allowed_scopes  TEXT NOT NULL DEFAULT '[]',     -- whitelist d'IDs de scopes servis à ce pair
  last_seen_at    TEXT,
  added_at        TEXT NOT NULL,
  revoked_at      TEXT
);

-- Curseur de sync par (pair, scope) — chez le spoke surtout
CREATE TABLE sync_cursor (
  peer_machine_id TEXT NOT NULL,
  scope_id        TEXT NOT NULL,
  watermark       TEXT NOT NULL DEFAULT '1970-01-01T00:00:00.000Z', -- max(updated_at) déjà pull
  last_push_at    TEXT NOT NULL DEFAULT '1970-01-01T00:00:00.000Z',
  last_sync_at    TEXT,
  PRIMARY KEY (peer_machine_id, scope_id)
);

-- Enveloppes de secrets partagés (côté hub) : valeurs chiffrées GVK, c'est ce qui voyage
CREATE TABLE shared_secret_envelopes (
  ref_id     TEXT PRIMARY KEY REFERENCES secret_refs(id),
  scope_id   TEXT NOT NULL,
  syncable   INTEGER NOT NULL DEFAULT 0,          -- opt-in explicite (secrets 'critical' = 0 par défaut)
  iv         TEXT NOT NULL,                        -- base64
  tag        TEXT NOT NULL,
  data       TEXT NOT NULL,                        -- AES-256-GCM(value, GVK)
  updated_at TEXT NOT NULL
);

-- Anti-rejeu : nonces vus récemment (TTL purge)
CREATE TABLE sync_nonces (
  nonce      TEXT PRIMARY KEY,
  seen_at    TEXT NOT NULL
);

-- machine_id stable du nœud (réutilise la table settings/meta existante)
-- INSERT INTO settings(key,value) VALUES ('sync.machine_id', <hostname>-<rand6>) ON CONFLICT DO NOTHING;
```

**Migration content v2** (nouveau bloc `{ version: 2, ... }` dans `content-schema.ts`, ALTER additifs comme le précédent montre L195-198) :

```sql
ALTER TABLE facts ADD COLUMN origin_machine_id TEXT;            -- d'où vient le fait (provenance)
ALTER TABLE facts ADD COLUMN origin_rev        INTEGER NOT NULL DEFAULT 0; -- horloge logique par machine, tie-break LWW
ALTER TABLE facts ADD COLUMN content_hash      TEXT;            -- sha256(fact|category|scope_id) normalisé, dédup
ALTER TABLE facts ADD COLUMN deleted_at        TEXT;            -- tombstone (suppression propagée, pas de DELETE dur)
CREATE INDEX idx_facts_origin ON facts(origin_machine_id, origin_rev);
CREATE INDEX idx_facts_content_hash ON facts(content_hash);
-- Idem sur `procedures` si on les synchronise (phase 4).
```

> `id` (UUID) reste la clé de transport/merge → idempotence naturelle (`INSERT OR IGNORE` déjà utilisé par `shareFacts`). `content_hash` déduplique deux faits créés **indépendamment** avec le même contenu sur 2 machines (sinon double ligne « le mot de passe NAS = X »).

### 3.3 Protocole de synchro des scopes partagés

**Périmètre** : whitelist de types `user | org | client | project | shared_topic`. `private` et `legacy_to_review` **jamais émis** (filtre à la source, pas blacklist). Les compteurs d'usage (`recall_count`, `used_count`, `usefulness`, `relevance_weight`, embeddings) **ne sont pas synchronisés** (télémétrie locale par agent).

**Unité** : deltas de `facts` par ligne (jamais de fichier SQLite, jamais de snapshot sauf bootstrap/réconciliation).

**Suivi du déjà-vu** : watermark `updated_at` par `(peer, scope)` (`sync_cursor`). Le `updated_at` est **toujours posé par le daemon récepteur en UTC ISO** (`nowISO()` centralisé), jamais par le client → pas de dérive d'horloge sur le critère de pagination.

**Provenance & ordre causal** : chaque write local sur un scope partagé pose `origin_machine_id = <moi>` et incrémente `origin_rev` (compteur monotone persistant par machine dans `settings`). `origin_rev` est le **critère primaire** de LWW (robuste aux horloges Mac désynchronisées) ; `updated_at` n'est que tie-break secondaire.

**Résolution de conflits — LWW déterministe par fait** (même `id` édité sur 2 machines) :

```
incoming gagne SI   incoming.origin_rev  > local.origin_rev
            OU  (== rev  ET  incoming.updated_at > local.updated_at)
            OU  (== rev,date  ET  incoming.origin_machine_id > local.origin_machine_id)  -- tie-break stable, déterministe
```

Le perdant n'est **pas détruit** : on le marque `superseded=1, superseded_by=<gagnant>` (colonnes existantes) → conflit auditable/réconciliable dans l'UI admin. **Suppressions = tombstone** (`deleted_at` + propagation via le même LWW), jamais un DELETE dur (sinon résurrection au prochain pull). Purge physique des tombstones > 90 j.

**Pas de CRDT/Raft** : 3 machines, faible débit, conflits du *même* fait rarissimes ; LWW par fait + watermark suffit et converge (fonction `winner` pure → état final identique sur les 3 machines).

#### Format JSON des messages

`GET /v1/sync/pull?scope=<id>&since=<watermark>&limit=500` → réponse :

```json
{
  "scope_id": "scope_org_primo",
  "facts": [
    {
      "id": "f_abc",
      "fact": "ligne de commande de déploiement bureau-primobot : ...",
      "category": "command", "fact_type": "statement", "confidence": 0.9,
      "scope_id": "scope_org_primo",
      "sensitivity": "normal", "visibility": "shared",
      "tags": ["deploy"], "entity_ids": [],
      "lifecycle_state": "active", "superseded": 0, "superseded_by": null,
      "origin_machine_id": "koda-a1b2c3", "origin_rev": 7,
      "content_hash": "9f2c...", "deleted_at": null,
      "created_at": "2026-06-10T08:00:00.000Z",
      "updated_at": "2026-06-11T09:00:00.000Z"
    }
  ],
  "tombstones": [
    { "id": "f_old", "deleted_at": "2026-06-11T09:05:00.000Z",
      "origin_machine_id": "luna-d4e5f6", "origin_rev": 3 }
  ],
  "next_cursor": "2026-06-11T09:05:00.000Z",
  "has_more": false
}
```

`POST /v1/sync/push` (spoke → hub) — même schéma `facts[]`/`tombstones[]` + `peer_machine_id`. Réponse :

```json
{ "applied": 4, "skipped_lww": 1, "deduped": 0, "tombstoned": 1, "hub_watermark": "2026-06-11T09:05:00.000Z" }
```

`GET /v1/sync/snapshot?scope=<id>` (bootstrap/réconciliation) — page complète du scope, même schéma de `facts[]` + `next_cursor` + `has_more`.

### 3.4 Coffre inter-machines

**Principe** : `secret_refs` (métadonnée gouvernée) voyage comme un fait ; **la valeur** ne transite que chiffrée **GVK**, jamais en clair, jamais dans facts/.md/logs/audit (gate `secrets/types.ts` intact ; dernier rempart `RegexRedactor` avant émission réseau).

**Trajet d'un mot de passe Koda → Luna :**
1. Sur le hub, `set` d'un secret partagé (scope ≠ private, `syncable=1`) : valeur dans le Keychain local Koda (inchangé) **+** chiffrée AES-256-GCM(value, GVK) → ligne `shared_secret_envelopes` (`{iv,tag,data}`, format exact d'`aes-vault.ts`).
2. `GET /v1/sync/secrets?scope=<id>` renvoie **l'enveloppe chiffrée** + le `secret_refs` correspondant. Jamais le plaintext.
3. Luna déchiffre **localement** avec sa GVK (Keychain), vérifie sa policy `secret_access` locale, puis range la valeur dans **son** Keychain via `SecretProvider.set`. Si le tag GCM est invalide (mauvaise clé) → `null` + warn, jamais de plaintext corrompu.

Un secret n'est servi à un spoke que si : `syncable=1` **ET** agent demandeur ∈ `allowed_assistants` **ET** `assistant_scope_policy.secret_access != 'none'`. Les secrets `critical` sont `syncable=0` par défaut (opt-in conscient de Néto).

**Rôles** :

| Élément | Rôle |
|---|---|
| Keychain local (chaque Mac) | racine de confiance ; détient GVK, CPK, et les valeurs descellées. Jamais sur disque en clair, jamais dans le TOML. |
| `shared_secret_envelopes` (hub) | le « coffre partagé » : valeurs chiffrées GVK. C'est ce qui voyage. |
| `secret_refs` (registry) | métadonnée gouvernée (`allowed_assistants`, `sensitivity`) → décide *si* on sert l'enveloppe. |

### 3.5 Auth entre daemons

**Identité** : `machine_id` stable (persisté dans `settings`, ≠ `daemonId` du boot).

**Établissement (réutilise le pairing existant, type `machine`)** :
1. Hub : `memoria sync invite` → ligne `pairings` (code one-shot, `code_hash`, TTL 10 min) + affiche IP:port LAN du hub.
2. Spoke : `memoria sync join --hub <ip:port> --code XXXX-XXXX` → `POST /v1/sync/pairing/complete` (route **sans Bearer**, le code TTL **est** le secret, exactement comme `/v1/pairing/complete` aujourd'hui).
3. Le hub répond `{ peer_token, cpk, sealed_gvk }`, crée la ligne `sync_peers`. `peer_token` + `cpk` rangés chmod 600 / Keychain côté spoke. `sealed_gvk = AES-GCM(GVK, scrypt(code))` → Luna descelle une seule fois, range GVK en Keychain, le code expire.

**Preuve d'identité à CHAQUE requête `/v1/sync/*`** :
- **Bearer `peer_token`** (comparé `timingSafeEqual`, helper déjà présent L596).
- **HMAC anti-rejeu/anti-MITM** :
  `X-Memoria-Sig = HMAC-SHA256(CPK, method | path | sha256(body) | X-Memoria-Ts | X-Memoria-Nonce)`.
  - `X-Memoria-Ts` rejeté si |écart| > 60 s.
  - `X-Memoria-Nonce` mémorisé 5 min (`sync_nonces`) → rejeu refusé même dans la fenêtre.
- **Binding LAN ciblé** : seules `/v1/sync/*` + `/v1/sync/pairing/complete` acceptent l'IP LAN ; tout le reste **reste loopback** (`isLoopbackHost` conservé).

**TLS ?** Non requis. Les **valeurs de secrets sont déjà chiffrées GVK avant d'entrer dans HTTP**, et chaque requête est HMAC-signée (intégrité + anti-rejeu). Un sniff LAN ne révèle aucun plaintext de secret et ne peut rien forger. TLS self-signed reste **optionnel** (`sync.tls=true`, empreinte épinglée au pairing) pour qui veut le confidentiel de transport total — on évite la PKI pour un public non-dev.

### 3.6 Bootstrap d'une machine neuve (iMac de Luna)

Côté Luna, **une seule commande** (calquée sur `connect.ts`) :

```bash
memoria sync join --hub 192.168.1.20:47600 --code 4F2A-9C1E
```

Enchaîne automatiquement :
1. `ensureDaemon()` local (démarre le daemon du spoke s'il dort — fonction existante).
2. `POST /v1/sync/pairing/complete` → `{ peer_token, cpk, sealed_gvk }`. Descelle GVK (`scrypt(code)`), range GVK+CPK en Keychain, `peer_token` chmod 600.
3. **Snapshot initial** par scope autorisé : `GET /v1/sync/snapshot?scope=<id>` → crée localement `shared/<scope>.sqlite` (chemin via `storagePaths`, **disque local**), insère en bloc (`INSERT OR IGNORE`, transaction, pattern `shareFacts`). Watermark = `max(updated_at)` du snapshot.
4. **Secrets** : `GET /v1/sync/secrets?scope=<id>` → enveloppes → déchiffre GVK → `SecretProvider.set` local. `secret_refs` synchronisés en métadonnée.
5. Enregistre scopes/policies pour l'agent Luna.

**Cas hub éteint au moment du bootstrap** (greffe du relais) : si `--hub` injoignable mais NAS dispo, `memoria sync join --code <…> --from-nas /Volumes/MemoriaSync` lit `bootstrap.snap` + `sealed_gvk` déposés sur le QNAP (chiffrés GVK+CPK, le NAS ne peut pas les ouvrir). Une commande, un code, même sans aucun pair allumé.

**Disconnect** (non-dev) : `memoria sync leave` → révoque le `peer_token`/`cpk` côté local, marque `revoked_at` côté hub au prochain contact, **garde** les facts/secrets déjà reçus (restent valides offline). Aucune purge surprise.

### 3.7 Offline & pannes

- **Hub éteint** : spokes 100 % locaux (privé + copie locale `shared/*.sqlite` lue normalement). Écritures partagées marquées `updated_at`/`origin_rev`, mises en file (le push les rattrape via `updated_at > last_push_at`). Convergence reprend au retour du hub, ou via relais NAS entre-temps.
- **Spoke éteint** : aucun effet. Au retour : pull (since watermark) puis push (since last_push). Idempotent (`INSERT OR IGNORE` + LWW).
- **Conflit au retour** : LWW déterministe → pas de ping-pong. Un fait inchangé garde son `updated_at`/`origin_rev` → sort de la fenêtre au cycle suivant.
- **Pas de boucle infinie** : watermark strictement croissant ; un fait appliqué sans modification n'incrémente pas `updated_at` ; nonce-store bloque le rejeu réseau ; **pas de rebroadcast** (push/pull tiré, jamais inondé).
- **Cadence** : (a) au boot du daemon, (b) toutes `sync.interval_sec` (défaut 120) avec debounce post-write, (c) à la demande (`memoria sync now`). Best-effort, jamais bloquant, hors du chemin `recall`/`store_fact` (comme `replayWal()` au boot).
- **NAS injoignable** : passe skip + warn, jamais fatale.
- **Horloge folle** : critère primaire `origin_rev` logique → ordre préservé ; HMAC `ts ±60 s` refuse en clair une machine trop décalée plutôt qu'une dérive muette.
- **Découverte d'adresse (DHCP)** : si l'IP du hub change, le spoke lit `hub.json` (`{ip,port,machine_id}`, pas de SQLite, pas de secret) déposé par le hub sur le QNAP. Seul usage « carnet d'adresses » du NAS.
- **Réconciliation** : `memoria sync verify` compare des checksums de scope (hash trié des `content_hash`) hub vs spoke ; un scope divergent déclenche un re-snapshot borné.

### 3.8 Champs `config.toml`

```toml
[sync]
enabled       = true
role          = "hub"                  # "hub" | "spoke"
machine_id    = "koda-a1b2c3"          # stable, généré au 1er boot si absent
hub           = "192.168.1.20:47600"   # (spoke uniquement)
listen_lan    = "0.0.0.0:47600"        # (hub) listener LAN dédié /v1/sync/*  (≠ port loopback admin/memory)
interval_sec  = 120
tls           = false
scopes        = ["user", "org", "client", "project", "shared_topic"]   # whitelist (private exclu par construction)
relay_path    = "/Volumes/MemoriaSync/memoria-sync"   # optionnel : secours/bootstrap NAS
discovery_file = "qnap://memoria/hub.json"            # optionnel : carnet d'adresses
# GVK / CPK / peer_token NE SONT JAMAIS dans le TOML → Keychain via SecretProvider.
```

Ajout dans `MemoriaConfig` (`config.ts`) :

```ts
sync?: {
  enabled?: boolean
  role?: 'hub' | 'spoke'
  machine_id?: string
  hub?: string
  listen_lan?: string
  interval_sec?: number
  tls?: boolean
  scopes?: string[]
  relay_path?: string
  discovery_file?: string
}
```

### 3.9 Nouveau module `packages/core/src/sync/`

```ts
// sync/clock.ts
export function localMachineId(registry: RegistryStore): string         // lit/crée settings['sync.machine_id']
export function nextRev(db: Database, machineId: string): number          // compteur monotone persistant (settings)

// sync/merge.ts  — cœur de convergence (pur, déterministe, testable isolément)
export function winner(local: FactRow | undefined, incoming: FactRow): 'apply' | 'skip'   // LWW (origin_rev, updated_at, machine_id)
export function contentHash(f: Pick<FactRow,'fact'|'category'|'scope_id'>): string
export function applyDelta(store: ContentStore, scopeId: string, facts: FactRow[], tombstones: Tombstone[], myMachineId: string)
  : { applied: number; skipped_lww: number; deduped: number; tombstoned: number }

// sync/secrets-sync.ts  — enveloppes GVK (réutilise crypto d'aes-vault)
export function sealValue(value: string, gvk: Buffer): { iv: string; tag: string; data: string }
export function openEnvelope(env: { iv: string; tag: string; data: string }, gvk: Buffer): string | null
export function sealGvk(gvk: Buffer, pairingCode: string): string         // scrypt(code) → transport bootstrap
export function openGvk(sealed: string, pairingCode: string): Buffer | null

// sync/peer-auth.ts  — HMAC + nonce anti-rejeu
export function signRequest(cpk: Buffer, p: { method: string; path: string; body: string; ts: string; nonce: string }): string
export function verifyRequest(cpk: Buffer, sig: string, p: SigParts, seenNonce: (n: string) => boolean): { ok: boolean; reason?: string }

// sync/engine.ts
export class SyncEngine {
  constructor(private memoria: Memoria, private registry: RegistryStore, private cfg: SyncConfig) {}
  // spoke
  pull(peer: PeerHandle, scopeId: string): Promise<{ applied: number; deduped: number; cursor: string }>
  push(peer: PeerHandle, scopeId: string): Promise<{ applied: number; skipped_lww: number }>
  syncAll(peer: PeerHandle): Promise<SyncReport>
  bootstrap(peer: PeerHandle): Promise<BootstrapReport>      // snapshot + secrets, 1re fois
  join(opts: { hub: string; code: string }): Promise<void>   // pairing + bootstrap
  // hub
  collectDelta(scopeId: string, since: string, limit: number): SyncDelta
  applyIncoming(scopeId: string, d: SyncDelta, from: string): ApplyReport
  snapshot(scopeId: string): SyncDelta
  serveSecrets(scopeId: string, agentId: string): SealedSecret[]   // honore syncable + allowed_assistants + policy
  tick(): Promise<void>                                            // une passe best-effort (push+pull), skip+warn si injoignable
}
```

### 3.10 Nouvelles routes daemon (`packages/daemon/src/server.ts`)

Branche `url.pathname.startsWith('/v1/sync/')` traitée **avant** le check loopback strict, autorisée sur l'IP LAN, derrière `peer_token` + HMAC :

```
POST /v1/sync/pairing/complete   (no Bearer, code one-shot TTL)        → { peer_token, cpk, sealed_gvk }
GET  /v1/sync/snapshot?scope=…   (peer_token + HMAC)                   → page complète (bootstrap/réconciliation)
GET  /v1/sync/pull?scope=…&since=…&limit=…                            → delta { facts[], tombstones[], next_cursor, has_more }
POST /v1/sync/push                                                     → applyIncoming → { applied, skipped_lww, tombstoned, hub_watermark }
GET  /v1/sync/secrets?scope=…                                         → enveloppes chiffrées GVK (jamais plaintext)
```

Routes **admin loopback** (Bearer admin, restent 127.0.0.1) :

```
POST /v1/admin/sync/invite     → { code, expires_at, hub_lan }
POST /v1/admin/sync/now        → tick() à la demande
GET  /v1/admin/sync/peers      → liste sync_peers
POST /v1/admin/sync/revoke     → revoked_at sur un peer
POST /v1/admin/sync/rotate-key → régénère GVK, re-scelle shared_secret_envelopes, force re-pairing
POST /v1/admin/sync/verify     → checksums de scope hub vs spoke
```

`DaemonClient` (`client.ts`) gagne : `syncPull`, `syncPush`, `syncSnapshot`, `syncSecrets`, `syncPairingComplete`, `syncInvite`, `syncNow`, `syncJoin` (injection auto Bearer + headers HMAC).

Timer interne : `setInterval(() => syncEngine.tick().catch(warn), interval)` lancé **après** le bloc `replayWal()` au boot (L528), en `catch → warn`, jamais bloquant.

### 3.11 Changements registry / secrets / MCP / CLI

- `registry-schema.ts` : **migration v4** (`sync_peers`, `sync_cursor`, `shared_secret_envelopes`, `sync_nonces`, `settings['sync.machine_id']`).
- `content-schema.ts` : **migration v2** (`origin_machine_id`, `origin_rev`, `content_hash`, `deleted_at` + index).
- `secrets/index.ts` : helper `groupVaultKey()` (lit/crée `memoria/__group_vault_key` dans le `SecretProvider` local) + `clusterPairingKey()`. **Aucune** modification du gate de redaction.
- `packages/mcp/src/sync-join.ts` (miroir de `connect.ts`) + entrée bin.
- CLI : `memoria sync init-hub | invite | join | leave | now | status | peers | revoke <peer> | verify | rotate-key`.

---

## 4. Incréments livrables, ordonnés

Chaque incrément est testable et apporte de la valeur seul.

### Incrément 1 — Provenance & merge LWW (offline, sans réseau)

**Valeur seule** : un fait sait d'où il vient ; on peut importer/fusionner deux jeux de facts de façon déterministe (utile même pour un import manuel de DB).
**Fichiers** : `content-schema.ts` (migration v2), `engine/memoria.ts` (`storeFact`/update posent `origin_machine_id`+`origin_rev`+`content_hash`), nouveau `sync/merge.ts`, `sync/clock.ts`.
**Tests** : `winner()` pur (rev > / égalité date / tie-break machine_id) ; propriété **convergence** (appliquer N ops dans 3 ordres aléatoires → état final identique) ; tombstone n'est pas ressuscité ; `content_hash` déduplique ; migration v2 idempotente sur DB v1 existante (colonnes ajoutées, données préservées).

### Incrément 2 — Auth machine-à-machine + listener LAN ciblé

**Valeur seule** : un spoke peut s'appairer au hub et appeler une route `/v1/sync/ping` authentifiée, sans encore synchroniser — la sécurité réseau est validée en isolation.
**Fichiers** : `registry-schema.ts` (migration v4 : `sync_peers`, `sync_nonces`), `sync/peer-auth.ts`, `server.ts` (branche `/v1/sync/*` sur IP LAN + HMAC, `/v1/sync/pairing/complete`), `client.ts` (`syncPairingComplete`, headers HMAC), `config.ts` (`[sync]`).
**Tests** : pairing type machine (code one-shot, TTL, single-use) ; HMAC accepté/refusé (sig fausse, ts hors fenêtre, nonce rejoué) ; `/v1/admin/*` et `/v1/memory/*` **toujours refusés** sur IP LAN (régression anti-DNS-rebinding) ; `peer_token` `timingSafeEqual`.

### Incrément 3 — Pull/push des facts + curseur (le cœur fonctionnel)

**Valeur seule** : Luna voit les facts partagés de Koda et inversement — le besoin métier #1 (lignes de commande, infos user/org/projet) est rempli.
**Fichiers** : `registry-schema.ts` (`sync_cursor`), `sync/engine.ts` (`collectDelta`, `applyIncoming`, `pull`, `push`, `syncAll`, `tick`), `server.ts` (`/v1/sync/pull|push|snapshot`), `client.ts` (`syncPull|syncPush|syncSnapshot|syncNow`), timer boot, CLI `sync now|status`.
**Tests** : delta respecte le watermark (rien de re-pull) ; whitelist scopes (private/legacy jamais émis — assert dur) ; idempotence (`INSERT OR IGNORE` + LWW, double pull = no-op) ; pagination `has_more` ; hub down → spoke continue local + rattrape au retour ; pas de ping-pong (2 ticks consécutifs stables) ; compteurs d'usage **non** synchronisés.

### Incrément 4 — Coffre inter-machines (secrets)

**Valeur seule** : Luna lit les mots de passe que Koda détient — le besoin métier #2.
**Fichiers** : `registry-schema.ts` (`shared_secret_envelopes`), `secrets/index.ts` (`groupVaultKey`, `clusterPairingKey`), `sync/secrets-sync.ts`, `server.ts` (`/v1/sync/secrets`, `sealed_gvk` dans pairing/complete), `engine/memoria.ts` (`set` secret partagé → enveloppe), CLI `rotate-key`.
**Tests** : valeur jamais en clair dans `facts`/`audit`/stdout/`.mbx` (test type `secrets-gate`) ; round-trip seal/open GVK ; mauvaise GVK → `null` + warn, pas de crash ; `syncable=0` (critical) non servi sauf opt-in ; `allowed_assistants` + `secret_access` honorés ; descellement GVK via `scrypt(code)` au pairing ; `rotate-key` re-scelle tout + invalide l'ancien.

### Incrément 5 — Bootstrap 1-commande + disconnect (UX non-dev)

**Valeur seule** : Badette installe l'iMac et tape une seule commande ; tout l'historique + le coffre arrivent.
**Fichiers** : `packages/mcp/src/sync-join.ts` + bin, `sync/engine.ts` (`bootstrap`, `join`, `leave`), CLI `init-hub|invite|join|leave|peers|revoke`.
**Tests** : `sync join` de bout en bout (daemon vide → snapshot scopes + secrets + cursors initialisés) ; idempotent si rejoué ; `leave` révoque sans purger les facts reçus ; messages FR prêts-à-coller.

### Incrément 6 (optionnel) — Relais NAS de secours + verify/réconciliation

**Valeur seule** : bootstrap/rattrapage quand le hub dort ; filet anti-divergence.
**Fichiers** : `sync/engine.ts` (`tick` dépose/relève `hub.json` + `bootstrap.snap` chiffrés ; `snapshot`/compaction NAS atomique tmp+rename), CLI `verify`, `--from-nas` dans `sync-join`.
**Tests** : `network-guard` autorise des **fichiers** opaques sur `/Volumes/*` mais aucun `.sqlite` (assert : on n'ouvre jamais une DB sur volume réseau) ; bootstrap from-nas sans aucun pair allumé ; `verify` détecte un scope divergent et déclenche re-snapshot ; NAS absent → skip + warn.

---

## 5. Ce qu'il ne faut PAS faire (anti-patterns)

1. **Jamais de `shared/*.sqlite` (ni `registry`) sur le QNAP.** `network-guard.ts` bloque ; corruption WAL assurée. NAS = `hub.json` + `.mbx`/`.snap` chiffrés opaques + dump à froid uniquement.
2. **Jamais synchroniser `private` / `legacy_to_review`.** Whitelist de types en dur dans `SyncEngine`, pas une blacklist. `shareFacts` interdit déjà private (`scope.type !== 'private'`).
3. **Jamais une valeur de secret en clair** dans un message, log, fact, audit ou `.mbx`. Toujours l'enveloppe GVK. `RegexRedactor` reste en amont de `storeFact` et en dernier rempart avant émission.
4. **Ne pas synchroniser la télémétrie** (`recall_count`, `used_count`, `usefulness`, `relevance_weight`, embeddings). Usage local par agent ; embeddings dépendent du modèle local.
5. **Pas de mesh ni de multi-hub.** Un seul hub canonique. Les copies locales des spokes sont des répliques de lecture, pas des hubs concurrents.
6. **Pas de CRDT/oplog/Raft.** LWW par fait + watermark suffit pour 3 machines.
7. **Ne jamais ouvrir `/v1/admin/*` ou `/v1/memory/*` sur le LAN.** Seules `/v1/sync/*` sortent du loopback, avec `peer_token` + HMAC. Anti-DNS-rebinding conservé pour le reste.
8. **Ne pas confondre `facts.id` et unicité de contenu.** Deux machines → deux UUID pour le même fait → `content_hash` déduplique, pas l'`id`.
9. **Ne pas bloquer l'agent si le hub/NAS est down.** Sync best-effort en arrière-plan, jamais dans `recall`/`store_fact` (comme `replayWal`).
10. **Ne pas réutiliser le `daemonId` éphémère** comme identité de nœud : il change à chaque boot et casse curseurs + `origin_rev`. Utiliser `settings['sync.machine_id']` persistant.
11. **Ne pas mettre GVK/CPK/peer_token dans `config.toml`** (fichier clair). Keychain via `SecretProvider`.
12. **Pas de DELETE dur propagé.** Tombstone (`deleted_at`) seulement ; `forget` hard-delete reste une action **locale** explicite.

---

## 6. Trois plus gros risques & mitigations

1. **SPOF du hub** (Mac Studio HS = état canonique perdu). → (a) spokes gardent des **copies locales complètes** (greffe mesh) → l'historique n'est jamais sur la seule machine ; (b) backup à froid périodique du hub vers le QNAP (**dump `.sql`**, pas du SQLite vivant) ; (c) `promote-to-hub` : un spoke (l'iMac) redevient hub à partir de sa copie locale + sa GVK déjà en Keychain.
2. **Compromission de la GVK** = tous les secrets partagés exposés. → GVK uniquement en Keychain (jamais disque/log/TOML), transmise une seule fois scellée `scrypt(code)` TTL court ; `revoke` + `rotate-key` (re-scelle tout, force re-pairing) ; `critical` non syncable par défaut.
3. **Dérive silencieuse / watermark cassé** (horloge décalée, `updated_at` mal écrit). → `updated_at` posé par le **récepteur** en UTC ISO (`nowISO()`), jamais par le client ; ordre causal sur `origin_rev` logique (pas le mur) ; `sync verify` (checksums de scope) + re-snapshot d'un scope divergent ; HMAC `ts ±60 s` refuse explicitement une horloge trop décalée plutôt qu'une dérive muette.

---

## Fichiers de référence (absolus)

- `/Users/primostudio/openclaw-memoria/packages/core/src/config.ts` — `MemoriaConfig`, `resolveStorageRoot`, `storagePaths`, `moveStorage` (tmp+rename).
- `/Users/primostudio/openclaw-memoria/packages/core/src/storage/registry-schema.ts` — **migration v4** (sync_peers, sync_cursor, shared_secret_envelopes, sync_nonces) ; `secret_refs` L135, `pairings` L112.
- `/Users/primostudio/openclaw-memoria/packages/core/src/storage/content-schema.ts` — **migration v2** (origin_*, content_hash, deleted_at) ; `facts` L31.
- `/Users/primostudio/openclaw-memoria/packages/core/src/storage/migrations.ts` — type `Migration` (mécanisme versionné).
- `/Users/primostudio/openclaw-memoria/packages/core/src/storage/network-guard.ts` — contrainte dure NAS.
- `/Users/primostudio/openclaw-memoria/packages/core/src/secrets/{index,aes-vault,types,redaction}.ts` — GVK/CPK + enveloppes GCM, gate dur.
- `/Users/primostudio/openclaw-memoria/packages/daemon/src/server.ts` — routes `/v1/sync/*`, extension LAN ciblée, HMAC, timer post-`replayWal` (L504/L528/L578).
- `/Users/primostudio/openclaw-memoria/packages/daemon/src/client.ts` — méthodes `sync*` + `ensureDaemon`.
- `/Users/primostudio/openclaw-memoria/packages/mcp/src/connect.ts` — modèle de la commande unique (`sync join`).
- `/Users/primostudio/openclaw-memoria/packages/core/src/engine/memoria.ts` — `shareFacts`/`storeFact` (pattern `INSERT OR IGNORE` + transaction + guard private).
- Nouveau : `/Users/primostudio/openclaw-memoria/packages/core/src/sync/{clock,merge,secrets-sync,peer-auth,engine}.ts`.
- Nouveau : `/Users/primostudio/openclaw-memoria/packages/mcp/src/sync-join.ts`.

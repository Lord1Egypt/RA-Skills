# Memoria — app bureau (Tauri v2)

Lanceur « double-clic » pour non-développeurs (spec §14, v1 pragmatique) :

1. vérifie qu'un **Node ≥ 20** existe sur la machine (PATH, emplacements usuels, nvm) ;
2. démarre le **daemon Memoria** s'il ne tourne pas (`packages/daemon/dist/bin.js`, détaché) ;
3. lit `<storage_root>/daemon.json` (port + admin_token) ;
4. bascule la fenêtre sur `http://127.0.0.1:<port>/ui/#token=…` — l'UI web servie par le daemon.

Toute la logique vit dans `src-tauri/src/lib.rs` (miroir Rust de `ensureDaemon`/`resolveStorageRoot`),
testée par `cargo test`. La page de lancement (`ui/index.html`) n'appelle que les 4 commandes
Tauri : `check_node`, `daemon_health`, `start_daemon`, `open_memoria`.

## Construire

```bash
export PATH="$HOME/.cargo/bin:$PATH"
cd apps/desktop/src-tauri
cargo check          # validation rapide
cargo test           # tests unitaires du lanceur
# bundle complet (nécessite cargo install tauri-cli) :
cargo tauri build    # → .app + .dmg dans target/release/bundle/
```

Prérequis du bundle : le daemon doit être buildé (`npm run build` à la racine du repo) et l'UI
web aussi (`npm run build -w @memoria/web`) — le daemon la sert sous `/ui/`.

## Localisation du daemon

Ordre de recherche du `bin.js` (voir `daemon_bin_candidates` dans lib.rs) :
1. `~/.memoria/config.toml` → `[daemon] bin = "/chemin/vers/bin.js"` (clé propre au lanceur) ;
2. installation npm globale (`npm root -g`) ;
3. clone de dev `~/openclaw-memoria/packages/daemon/dist/bin.js`.

## Reste à faire (v1.5)

- **Node embarqué** : binaire SEA (single executable) du daemon en sidecar Tauri — attention,
  `better-sqlite3` est un module natif : embarquer le `.node` à côté et le charger par chemin
  relatif. Tant que ce n'est pas fait, la machine doit avoir Node ≥ 20.
- **Signature + notarisation macOS** : réutiliser le process Primo (cf. Igara — certificat
  Developer ID + `notarytool`).
- Icône définitive (l'icône actuelle est générée par `scripts/gen-icon.py`).
- Auto-démarrage du daemon au login (launchd) plutôt qu'au premier lancement de l'app.

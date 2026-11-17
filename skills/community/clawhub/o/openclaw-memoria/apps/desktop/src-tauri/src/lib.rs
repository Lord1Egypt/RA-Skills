//! Lanceur bureau Memoria (spec §14, voie « non-dev », v1 pragmatique).
//!
//! Miroir Rust de `packages/daemon/src/client.ts#ensureDaemon` et de
//! `packages/core/src/config.ts#resolveStorageRoot` :
//!  1. trouver un Node ≥ 20 sur la machine (pas de Node embarqué en v1 — v1.5) ;
//!  2. démarrer `packages/daemon/dist/bin.js` détaché s'il ne tourne pas ;
//!  3. lire `<storage_root>/daemon.json` (port + admin_token, chmod 600) ;
//!  4. donner à la page de lancement l'URL `http://127.0.0.1:<port>/ui/#token=…`.
//!
//! Les 4 commandes Tauri (`check_node`, `daemon_health`, `start_daemon`,
//! `open_memoria`) sont déclarées `async` : Tauri exécute les commandes sync
//! sur le thread principal, et celles-ci font de l'IO bloquante (process,
//! réseau local) — on les bascule donc sur le pool bloquant du runtime.

use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::io::{Read, Write};
use std::net::{SocketAddr, TcpStream};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

// ---------------------------------------------------------------------------
// Modèles (miroirs des structures TS)
// ---------------------------------------------------------------------------

/// `~/.memoria/config.toml` — même fichier de découverte que `core/config.ts`.
/// Les clés inconnues (llm, …) sont ignorées par serde : pas de couplage.
#[derive(Debug, Default, Deserialize)]
struct ConfigToml {
    /// Racine du stockage (priorité 2 de la résolution).
    storage_path: Option<String>,
    daemon: Option<DaemonSection>,
}

#[derive(Debug, Default, Deserialize)]
struct DaemonSection {
    /// Chemin explicite du `bin.js` du daemon (clé propre au lanceur bureau,
    /// inconnue de core — ignorée par lui, sans risque).
    bin: Option<String>,
}

/// `<storage_root>/daemon.json` — écrit par le daemon (cf. daemon/src/state.ts).
#[derive(Debug, Clone, Serialize, Deserialize)]
struct DaemonState {
    daemon_id: String,
    port: u16,
    admin_token: String,
    pid: i64,
    started_at: String,
}

/// Réponse de `check_node` vers la page de lancement.
#[derive(Debug, Serialize)]
struct NodeInfo {
    path: String,
    version: String,
    major: u32,
}

/// Réponse de `daemon_health`/`start_daemon`. Volontairement SANS le token :
/// seul `open_memoria` construit l'URL finale (surface minimale côté front).
#[derive(Debug, Serialize)]
struct DaemonInfo {
    port: u16,
    healthy: bool,
}

// ---------------------------------------------------------------------------
// Résolution des chemins (miroir de core/config.ts)
// ---------------------------------------------------------------------------

fn home_dir() -> Result<PathBuf, String> {
    env::var_os("HOME")
        .or_else(|| env::var_os("USERPROFILE"))
        .map(PathBuf::from)
        .ok_or_else(|| "HOME introuvable — environnement inhabituel".to_string())
}

fn config_path(home: &Path) -> PathBuf {
    home.join(".memoria").join("config.toml")
}

/// Charge `~/.memoria/config.toml`. Fichier absent = config vide (comme core) ;
/// fichier illisible = erreur remontée (jamais avalée).
fn load_config(path: &Path) -> Result<ConfigToml, String> {
    if !path.exists() {
        return Ok(ConfigToml::default());
    }
    let raw = fs::read_to_string(path)
        .map_err(|e| format!("config.toml illisible ({}) : {e}", path.display()))?;
    toml::from_str(&raw).map_err(|e| format!("config.toml invalide ({}) : {e}", path.display()))
}

/// LE résolveur d'emplacement, identique à `resolveStorageRoot()` côté TS :
/// `config.toml#storage_path` > `$MEMORIA_HOME` > `~/.memoria/data`.
/// (Pas de param explicite ici : le lanceur n'en a pas l'usage.)
/// NB : `storage_path` doit être absolu — le cwd d'une app GUI macOS est `/`.
fn resolve_storage_root() -> Result<PathBuf, String> {
    let home = home_dir()?;
    let config = load_config(&config_path(&home))?;
    if let Some(p) = config.storage_path {
        return Ok(PathBuf::from(p));
    }
    if let Some(p) = env::var_os("MEMORIA_HOME") {
        return Ok(PathBuf::from(p));
    }
    Ok(home.join(".memoria").join("data"))
}

/// Lit `<root>/daemon.json`. Absent = None ; JSON corrompu = None + trace
/// stderr (même tolérance que `readDaemonState` TS, mais jamais silencieux).
fn read_daemon_state(storage_root: &Path) -> Option<DaemonState> {
    let p = storage_root.join("daemon.json");
    if !p.exists() {
        return None;
    }
    let raw = match fs::read_to_string(&p) {
        Ok(raw) => raw,
        Err(e) => {
            eprintln!("memoria-desktop: daemon.json illisible ({}) : {e}", p.display());
            return None;
        }
    };
    match serde_json::from_str::<DaemonState>(&raw) {
        Ok(state) => Some(state),
        Err(e) => {
            eprintln!("memoria-desktop: daemon.json corrompu ({}) : {e}", p.display());
            None
        }
    }
}

// ---------------------------------------------------------------------------
// Santé du daemon — GET /v1/health en HTTP/1.1 brut sur 127.0.0.1
// (pas de client HTTP en dépendance pour un ping localhost ; timeouts 2 s,
// même budget que `DaemonClient.health()` TS). Toute défaillance réseau
// signifie « daemon pas joignable », pas une erreur à remonter.
// ---------------------------------------------------------------------------

fn http_health(port: u16) -> bool {
    let addr = SocketAddr::from(([127, 0, 0, 1], port));
    let Ok(mut stream) = TcpStream::connect_timeout(&addr, Duration::from_secs(2)) else {
        return false;
    };
    if stream.set_read_timeout(Some(Duration::from_secs(2))).is_err()
        || stream.set_write_timeout(Some(Duration::from_secs(2))).is_err()
    {
        return false;
    }
    let req = b"GET /v1/health HTTP/1.1\r\nhost: 127.0.0.1\r\nconnection: close\r\n\r\n";
    if stream.write_all(req).is_err() {
        return false;
    }
    let mut buf = String::new();
    // `connection: close` → le serveur ferme, read_to_string borne la lecture.
    if stream.read_to_string(&mut buf).is_err() {
        return false;
    }
    is_healthy_response(&buf)
}

/// Statut 200 + corps `{"ok":true,…}` (cf. route GET /v1/health du daemon).
fn is_healthy_response(raw: &str) -> bool {
    raw.starts_with("HTTP/1.1 200") && raw.contains("\"ok\":true")
}

// ---------------------------------------------------------------------------
// Découverte de Node ≥ 20 (les apps GUI macOS héritent d'un PATH réduit
// `/usr/bin:/bin:…` — on sonde donc explicitement les emplacements usuels)
// ---------------------------------------------------------------------------

const NODE_MAJOR_MIN: u32 = 20;

/// Extrait le major depuis la sortie de `node --version` (« v22.1.0 » → 22).
fn parse_node_major(version: &str) -> Option<u32> {
    version.trim().strip_prefix('v')?.split('.').next()?.parse().ok()
}

/// `node --version` sur un binaire candidat. Échec d'exécution = candidat
/// suivant (pas une erreur : on sonde des chemins qui peuvent ne pas exister).
fn node_version(path: &Path) -> Option<(String, u32)> {
    let out = Command::new(path).arg("--version").output().ok()?;
    if !out.status.success() {
        return None;
    }
    let version = String::from_utf8_lossy(&out.stdout).trim().to_string();
    let major = parse_node_major(&version)?;
    Some((version, major))
}

/// Candidats, du plus prioritaire au moins : override env, PATH, Homebrew
/// (Apple Silicon puis Intel), système, MacPorts, volta, asdf, nvm (plus
/// haute version installée).
fn node_candidates() -> Vec<PathBuf> {
    let mut v: Vec<PathBuf> = Vec::new();
    if let Some(p) = env::var_os("MEMORIA_NODE") {
        v.push(PathBuf::from(p));
    }
    v.push(PathBuf::from("node")); // résolution PATH (souvent réduite en GUI)
    for p in [
        "/opt/homebrew/bin/node",
        "/usr/local/bin/node",
        "/usr/bin/node",
        "/opt/local/bin/node",
    ] {
        v.push(PathBuf::from(p));
    }
    if let Ok(home) = home_dir() {
        v.push(home.join(".volta").join("bin").join("node"));
        v.push(home.join(".asdf").join("shims").join("node"));
        if let Some(p) = best_nvm_node(&home.join(".nvm").join("versions").join("node")) {
            v.push(p);
        }
    }
    v
}

/// Parcourt `~/.nvm/versions/node/v*/bin/node` et retient le major le plus haut.
fn best_nvm_node(versions_dir: &Path) -> Option<PathBuf> {
    let entries = fs::read_dir(versions_dir).ok()?;
    let mut best: Option<(u32, PathBuf)> = None;
    for entry in entries.flatten() {
        let name = entry.file_name().to_string_lossy().into_owned();
        let Some(major) = parse_node_major(&name) else { continue };
        let candidate = entry.path().join("bin").join("node");
        if best.as_ref().is_none_or(|(m, _)| major > *m) {
            best = Some((major, candidate));
        }
    }
    best.map(|(_, p)| p)
}

fn find_node() -> Result<NodeInfo, String> {
    for cand in node_candidates() {
        // « node » nu = résolution PATH ; les chemins absolus doivent exister.
        if cand.is_absolute() && !cand.exists() {
            continue;
        }
        if let Some((version, major)) = node_version(&cand) {
            if major >= NODE_MAJOR_MIN {
                return Ok(NodeInfo {
                    path: cand.to_string_lossy().into_owned(),
                    version,
                    major,
                });
            }
        }
    }
    Err(format!(
        "Node.js ≥ {NODE_MAJOR_MIN} introuvable sur cette machine. Installe-le \
         (https://nodejs.org ou `brew install node`) puis relance Memoria. \
         Tu peux aussi pointer un binaire précis via la variable MEMORIA_NODE."
    ))
}

// ---------------------------------------------------------------------------
// Localisation puis démarrage détaché du daemon
// ---------------------------------------------------------------------------

/// Localise `bin.js` du daemon : `$MEMORIA_DAEMON_BIN` > `config.toml
/// [daemon].bin` > installation gérée `~/.memoria/daemon/bin.js` (v1.5) >
/// monorepo du build (dev : CARGO_MANIFEST_DIR = apps/desktop/src-tauri).
fn find_daemon_bin(config: &ConfigToml) -> Result<PathBuf, String> {
    let mut candidates: Vec<PathBuf> = Vec::new();
    if let Some(p) = env::var_os("MEMORIA_DAEMON_BIN") {
        candidates.push(PathBuf::from(p));
    }
    if let Some(bin) = config.daemon.as_ref().and_then(|d| d.bin.as_ref()) {
        candidates.push(PathBuf::from(bin));
    }
    if let Ok(home) = home_dir() {
        candidates.push(home.join(".memoria").join("daemon").join("bin.js"));
    }
    candidates.push(
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../../../packages/daemon/dist/bin.js"),
    );

    for c in &candidates {
        if c.exists() {
            return Ok(c.clone());
        }
    }
    Err(format!(
        "daemon Memoria introuvable (cherché : {}). Construis le monorepo \
         (`npm run build`) ou renseigne [daemon].bin dans ~/.memoria/config.toml.",
        candidates
            .iter()
            .map(|c| c.display().to_string())
            .collect::<Vec<_>>()
            .join(" · ")
    ))
}

/// Démarre `node bin.js` détaché (nouveau groupe de process : survit à la
/// fermeture de l'app), stdout/stderr vers `~/.memoria/desktop-daemon.log`
/// (le `stdio: 'ignore'` du client TS rendait le diagnostic impossible).
fn spawn_daemon(node: &NodeInfo, bin: &Path) -> Result<PathBuf, String> {
    let home = home_dir()?;
    let log_path = home.join(".memoria").join("desktop-daemon.log");
    if let Some(dir) = log_path.parent() {
        fs::create_dir_all(dir).map_err(|e| format!("mkdir {} : {e}", dir.display()))?;
    }
    let log = fs::File::options()
        .create(true)
        .append(true)
        .open(&log_path)
        .map_err(|e| format!("ouverture du log {} : {e}", log_path.display()))?;
    let log_err = log
        .try_clone()
        .map_err(|e| format!("dup du log {} : {e}", log_path.display()))?;

    let mut cmd = Command::new(&node.path);
    cmd.arg(bin)
        .current_dir(&home) // cwd stable (une app GUI démarre sur « / »)
        .stdin(Stdio::null())
        .stdout(Stdio::from(log))
        .stderr(Stdio::from(log_err));
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        cmd.process_group(0); // détachement : le daemon survit à l'app
    }
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        // DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        cmd.creation_flags(0x0000_0008 | 0x0000_0200);
    }
    cmd.spawn()
        .map_err(|e| format!("impossible de lancer `{} {}` : {e}", node.path, bin.display()))?;
    Ok(log_path)
}

/// Cœur de `start_daemon` : réutilise un daemon vivant, sinon spawn + attente
/// de `daemon.json` + health (budget 15 s, mêmes constantes qu'`ensureDaemon`).
fn start_daemon_blocking() -> Result<DaemonInfo, String> {
    let storage_root = resolve_storage_root()?;
    if let Some(state) = read_daemon_state(&storage_root) {
        if http_health(state.port) {
            return Ok(DaemonInfo { port: state.port, healthy: true });
        }
    }

    let node = find_node()?;
    let home = home_dir()?;
    let config = load_config(&config_path(&home))?;
    let bin = find_daemon_bin(&config)?;
    let log_path = spawn_daemon(&node, &bin)?;

    let deadline = Instant::now() + Duration::from_secs(15);
    while Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(200));
        if let Some(state) = read_daemon_state(&storage_root) {
            if http_health(state.port) {
                return Ok(DaemonInfo { port: state.port, healthy: true });
            }
        }
    }
    Err(format!(
        "le daemon n'a pas démarré dans les 15 s — voir {}",
        log_path.display()
    ))
}

/// URL finale de l'UI : token admin en fragment (#…), jamais en query — il
/// n'apparaît ni dans les logs HTTP ni dans l'historique. `admin_token` est
/// du base64url (cf. core/util.ts#newToken) : sûr tel quel dans un fragment.
fn memoria_url(port: u16, admin_token: &str) -> String {
    format!("http://127.0.0.1:{port}/ui/#token={admin_token}")
}

// ---------------------------------------------------------------------------
// Commandes Tauri (invoquées par ui/index.html)
// ---------------------------------------------------------------------------

/// Joint le pool bloquant et aplatit les deux niveaux d'erreur en message front.
async fn on_blocking<T: Send + 'static>(
    task: impl FnOnce() -> Result<T, String> + Send + 'static,
) -> Result<T, String> {
    tauri::async_runtime::spawn_blocking(task)
        .await
        .map_err(|e| format!("tâche du lanceur interrompue : {e}"))?
}

#[tauri::command]
async fn check_node() -> Result<NodeInfo, String> {
    on_blocking(find_node).await
}

#[tauri::command]
async fn daemon_health() -> Result<Option<DaemonInfo>, String> {
    on_blocking(|| {
        let storage_root = resolve_storage_root()?;
        Ok(read_daemon_state(&storage_root).map(|state| DaemonInfo {
            port: state.port,
            healthy: http_health(state.port),
        }))
    })
    .await
}

#[tauri::command]
async fn start_daemon() -> Result<DaemonInfo, String> {
    on_blocking(start_daemon_blocking).await
}

#[tauri::command]
async fn open_memoria() -> Result<String, String> {
    on_blocking(|| {
        let storage_root = resolve_storage_root()?;
        let state = read_daemon_state(&storage_root)
            .ok_or_else(|| "daemon.json introuvable — le daemon ne tourne pas ?".to_string())?;
        if !http_health(state.port) {
            return Err(format!("le daemon (port {}) ne répond pas au health check", state.port));
        }
        Ok(memoria_url(state.port, &state.admin_token))
    })
    .await
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            check_node,
            daemon_health,
            start_daemon,
            open_memoria
        ])
        .run(tauri::generate_context!())
        .expect("erreur au lancement de l'app bureau Memoria");
}

// ---------------------------------------------------------------------------
// Tests (sans réseau ni daemon réel ; fichiers en tmpdir)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    /// Dossier temporaire unique, nettoyé au drop.
    struct TmpDir(PathBuf);
    impl TmpDir {
        fn new(tag: &str) -> Self {
            let p = env::temp_dir().join(format!(
                "memoria-desktop-{tag}-{}-{:?}",
                std::process::id(),
                std::thread::current().id()
            ));
            fs::create_dir_all(&p).expect("mkdir tmpdir");
            Self(p)
        }
    }
    impl Drop for TmpDir {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }

    #[test]
    fn parse_node_major_accepte_les_formats_usuels() {
        assert_eq!(parse_node_major("v22.1.0"), Some(22));
        assert_eq!(parse_node_major("v20.0.0\n"), Some(20));
        assert_eq!(parse_node_major("v9.11.2"), Some(9));
        assert_eq!(parse_node_major("22.1.0"), None); // pas de préfixe « v »
        assert_eq!(parse_node_major("garbage"), None);
        assert_eq!(parse_node_major(""), None);
    }

    #[test]
    fn config_toml_absent_donne_defaut() {
        let tmp = TmpDir::new("cfg-absent");
        let cfg = load_config(&tmp.0.join("config.toml")).expect("config par défaut");
        assert!(cfg.storage_path.is_none());
        assert!(cfg.daemon.is_none());
    }

    #[test]
    fn config_toml_lit_storage_path_et_daemon_bin() {
        let tmp = TmpDir::new("cfg-ok");
        let p = tmp.0.join("config.toml");
        fs::write(
            &p,
            "storage_path = \"/tmp/memoria-data\"\n[daemon]\nport = 0\nbin = \"/opt/memoria/bin.js\"\n[llm]\nprofile = \"100-local\"\n",
        )
        .unwrap();
        let cfg = load_config(&p).expect("parse");
        assert_eq!(cfg.storage_path.as_deref(), Some("/tmp/memoria-data"));
        assert_eq!(
            cfg.daemon.and_then(|d| d.bin).as_deref(),
            Some("/opt/memoria/bin.js")
        );
    }

    #[test]
    fn config_toml_corrompu_remonte_une_erreur() {
        let tmp = TmpDir::new("cfg-ko");
        let p = tmp.0.join("config.toml");
        fs::write(&p, "storage_path = [pas du toml").unwrap();
        let err = load_config(&p).expect_err("doit échouer");
        assert!(err.contains("config.toml invalide"), "message : {err}");
    }

    #[test]
    fn daemon_state_roundtrip_et_corruption() {
        let tmp = TmpDir::new("state");
        // absent → None
        assert!(read_daemon_state(&tmp.0).is_none());
        // valide → Some (format exact écrit par daemon/src/state.ts)
        fs::write(
            tmp.0.join("daemon.json"),
            "{\"daemon_id\":\"abc123\",\"port\":7437,\"admin_token\":\"tok_base64url\",\"pid\":4242,\"started_at\":\"2026-06-10T00:00:00.000Z\"}",
        )
        .unwrap();
        let state = read_daemon_state(&tmp.0).expect("état lu");
        assert_eq!(state.port, 7437);
        assert_eq!(state.admin_token, "tok_base64url");
        // corrompu → None (et trace stderr, pas de panique)
        fs::write(tmp.0.join("daemon.json"), "{pas du json").unwrap();
        assert!(read_daemon_state(&tmp.0).is_none());
    }

    #[test]
    fn url_ui_met_le_token_en_fragment() {
        assert_eq!(
            memoria_url(7437, "AbC-_123"),
            "http://127.0.0.1:7437/ui/#token=AbC-_123"
        );
    }

    #[test]
    fn reponse_health_reconnue() {
        assert!(is_healthy_response(
            "HTTP/1.1 200 OK\r\ncontent-type: application/json\r\n\r\n{\"ok\":true,\"version\":\"0.1.0\"}"
        ));
        assert!(!is_healthy_response("HTTP/1.1 401 Unauthorized\r\n\r\n{}"));
        assert!(!is_healthy_response("HTTP/1.1 200 OK\r\n\r\n{\"ok\":false}"));
        assert!(!is_healthy_response(""));
    }

    #[test]
    fn nvm_retient_le_major_le_plus_haut() {
        let tmp = TmpDir::new("nvm");
        for v in ["v18.20.0", "v22.3.0", "v9.11.2"] {
            fs::create_dir_all(tmp.0.join(v).join("bin")).unwrap();
        }
        let best = best_nvm_node(&tmp.0).expect("un candidat");
        assert!(best.ends_with("v22.3.0/bin/node"), "choisi : {}", best.display());
        // dossier absent → None, sans erreur
        assert!(best_nvm_node(&tmp.0.join("inexistant")).is_none());
    }

    #[test]
    fn health_refuse_un_port_ferme() {
        // Port réservé puis libéré aussitôt : connexion refusée ⇒ false.
        let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
        let port = listener.local_addr().unwrap().port();
        drop(listener);
        assert!(!http_health(port));
    }
}
